"""Class and helper functions for running youtube-dl"""

from __future__ import annotations

__all__ = ('Downloader', 'sanitize_opts')

import json
from collections.abc import Sequence
from typing import TYPE_CHECKING

from . import db_util
from .util import LogEnum, StatusEnum

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping
    from logging import Logger
    from typing import Any
    from uuid import UUID


class Downloader:
    """Class used by `task` to run YoutubeDL

    `db_util.insert_job()` must be called before initializing this class
    so that the job exists in the database
    """

    __slots__ = (
        'job_id', 'urls', 'ytdl_opts', 'ytdl_class', 'logger', '_ytdl_logger',
        '_download_started'
    )

    job_id: UUID
    """ID of the job that's being downloaded"""
    urls: tuple[str, ...]
    """List of URLs to download"""
    ytdl_opts: dict[str, Any]
    """Dict of kwargs that will be passed to `ytdl_class`"""
    ytdl_class: type
    """YoutubeDL class to use

    Normally, this should be `youtube_dl.YoutubeDL` unless you're using
    a fork with a different module name
    """
    logger: Logger
    """Logger object to log to"""

    _ytdl_logger: YTDLLogger
    """YTDLLogger instance that's used for the job"""
    _download_started: bool
    """Whether or not `download()` has been called already"""

    def __init__(
        self, job_id: UUID, urls: Iterable[str], ytdl_opts: Mapping[str, Any],
        ytdl_class: type, logger: Logger
    ) -> None:
        self.job_id = job_id
        self.urls = tuple(urls)
        self.ytdl_opts = dict(ytdl_opts)
        self.ytdl_class = ytdl_class
        self.logger = logger
        self._download_started = False

        if 'progress_hooks' not in self.ytdl_opts:
            self.ytdl_opts['progress_hooks'] = (self.progress_hook,)
        else:
            self.ytdl_opts['progress_hooks'] = (
                tuple(ytdl_opts['progress_hooks']) + (self.progress_hook,)
            )

        # Prevent ytdl from injecting ANSI escape codes into the logs
        self.ytdl_opts['no_color'] = True
        # Prevent progress from being printed to the debug log (the
        # progress hook is used instead)
        self.ytdl_opts['noprogress'] = True
        # Disable youtube-dl version check
        # This is disabled by default. Set it explicitly so it can't be
        # enabled
        self.ytdl_opts['call_home'] = False

        self._ytdl_logger = self.YTDLLogger(self.job_id)
        self.ytdl_opts['logger'] = self._ytdl_logger

    @staticmethod
    def _dump_json(obj: Any) -> str:
        # TODO: add a custom encoder
        return json.dumps(obj)

    def progress_hook(self, progress: Mapping[str, Any]) -> None:
        db_util.upsert_progress(self.job_id, progress)

    class YTDLLogger:
        ___slots__ = ('job_id',)

        job_id: UUID

        def debug(self, msg: str) -> None:
            db_util.insert_log(self.job_id, LogEnum.debug, msg)

        def warning(self, msg: str) -> None:
            db_util.insert_log(self.job_id, LogEnum.warning, msg)

        def error(self, msg: str) -> None:
            db_util.insert_log(self.job_id, LogEnum.error, msg)

        def __init__(self, job_id: UUID) -> None:
            self.job_id = job_id

    def download(self) -> None:
        """Start the download

        This function can only be run once per instance. Attempting to
        run it again will raise `RuntimeError`
        """
        if self._download_started:
            raise RuntimeError('downloader can only be run once')
        self._download_started = True

        self.logger.info('Starting downloader for job %s', self.job_id)
        db_util.update_job(
            self.job_id,
            status=StatusEnum.downloading, started=db_util.CURRENT_TIMESTAMP
        )

        try:
            with self.ytdl_class(self.ytdl_opts) as ytdl:
                ytdl.download(self.urls)
        except Exception as e:
            self.logger.exception('Job failed: %s', self.job_id)
            error_msg = f'{type(e).__name__}: {e}'
            db_util.update_job(
                self.job_id,
                status=StatusEnum.error, finished=db_util.CURRENT_TIMESTAMP,
                # The error message is only logged from within `ytdl`
                # so that the user is only shown it when the error is
                # from youtube-dl
                error=error_msg
            )
        else:
            self.logger.info('Job finished: %s', self.job_id)
            db_util.update_job(
                self.job_id,
                status=StatusEnum.finished, finished=db_util.CURRENT_TIMESTAMP
            )


def _sanitize_postprocessor(pp: Mapping[str, Any]) -> Mapping[str, Any]:
    """Return a sanitized version of the given postprocessor"""
    if pp['key'] == 'MetadataParser':
        # Serialize the Actions enum used by the MetadataParser pp
        sanitized_pp = dict(pp)
        sanitized_actions = []

        for action in pp['actions']:
            sanitized_action = list(action)

            action_enum = action[0]
            sanitized_action[0] = f'Actions.{action_enum.name}'

            sanitized_actions.append(sanitized_action)

        sanitized_pp['actions'] = sanitized_actions
        return sanitized_pp
    else:
        # No change needed. Return the PP as-is
        return pp


def sanitize_opts(
    ytdl_opts: Mapping[str, Any], sensitive_opts: Iterable[str]
) -> dict[str, Any]:
    """Return a sanitized version of the given youtube-dl option dict
    that's safe to show to the user

    Sensitive options such as passwords are set to `None`, and some
    options that aren't JSONable are lossily serialized

    ytdl_opts: Uncensored youtube-dl options
    sensitive_opts: List of keys that should be censored. If any of
        these options are in ytdl_opts, the value will be set to None
    """
    opts = dict(ytdl_opts)

    for opt in sensitive_opts:
        if opt in opts:
            opts[opt] = None

    if 'daterange' in opts:
        daterange_str = f'DateRange({opts["daterange"]})'
        opts['daterange'] = daterange_str

    postprocessors = opts.get('postprocessors', None)
    if isinstance(postprocessors, Sequence):
        sanitized_pps = []

        for pp in postprocessors:
            try:
                sanitized_pp = _sanitize_postprocessor(pp)
            except Exception:
                # Give up on sanitizing the PP if it's the wrong type or
                # has an unexpected value
                sanitized_pps.append(pp)
            else:
                sanitized_pps.append(sanitized_pp)

        opts['postprocessors'] = sanitized_pps

    return opts
