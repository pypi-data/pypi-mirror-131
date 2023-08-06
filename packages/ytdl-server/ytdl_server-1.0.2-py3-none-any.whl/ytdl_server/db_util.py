"""Utility functions for accessing the SQL database"""

from __future__ import annotations

__all__ = (
    'get_job', 'get_job_status', 'get_logs', 'get_progress', 'insert_job',
    'insert_logs', 'update_job', 'upsert_progress', 'CURRENT_TIMESTAMP'
)

from typing import TYPE_CHECKING

import sqlalchemy as sql
from sqlalchemy.dialects.postgresql import insert as postgres_insert

from . import database
from .error import JobNotFoundError
from .util import Job, Log, Progress, StatusEnum

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable, Sequence
    from typing import Any, Final
    from uuid import UUID

_db = database.db

CURRENT_TIMESTAMP: Final = sql.func.current_timestamp()
"""SQL function that represents the current date and time

This can be used as a column value for `update_job()`
"""


def get_job(job_id: UUID) -> Job:
    """Returns the job that matches the given job ID

    If no job is found, it raises `JobNotFoundError`
    """
    result = _db.session.get(database.Job, job_id)
    if result is None:
        raise JobNotFoundError(job_id)

    job = Job(
        id=result.id,
        status=result.status,
        error=result.error,
        urls=result.urls,
        ytdl_opts=result.ytdl_opts,
        started=result.started,
        finished=result.finished
    )
    return job


def get_job_status(job_id: UUID) -> StatusEnum:
    """Returns just the status of the job that matches the given job ID

    If no job is found, it raises `JobNotFoundError`
    """
    statement = sql.select(database.Job.status).filter(
        database.Job.id == job_id
    )
    result = _db.session.execute(statement).one_or_none()

    if result is None:
        raise JobNotFoundError(job_id)
    else:
        status: StatusEnum = result.status
        return status


def get_logs(job_id: UUID) -> tuple[Log, ...]:
    statement = sql.select(
        database.Log.level, database.Log.message, database.Log.timestamp
    ).where(
        database.Log.job_id == job_id
    ).order_by(database.Log.timestamp)
    result = _db.session.execute(statement)

    logs = []
    for log in result:
        logs.append(Log(
            level=log.level,
            message=log.message,
            timestamp=log.timestamp
        ))
    return tuple(logs)


def get_progress(job_id: UUID) -> tuple[Progress, ...]:
    statement = sql.select(
        database.Progress.progress, database.Progress.timestamp
    ).where(
        database.Progress.job_id == job_id
    ).order_by(database.Progress.timestamp)
    result = _db.session.execute(statement)

    progress_list = []
    for progress in result:
        progress_list.append(Progress(
            progress=progress.progress,
            timestamp=progress.timestamp
        ))
    return tuple(progress_list)


def update_job(job_id: UUID, **columns: Any) -> None:
    """Update all given columns for the job that matches the job ID"""
    statement = sql.update(database.Job).where(
        database.Job.id == job_id
    ).values(**columns)

    with _db.session.begin():
        _db.session.execute(statement)


def insert_job(urls: Sequence[str]) -> UUID:
    """Insert a new job and return the job ID

    This must be called before starting the download via `ytdl`
    """
    statement = sql.insert(database.Job).values(
        status=StatusEnum.queued, urls=urls,
    ).returning(database.Job.id)
    with _db.session.begin():
        result = _db.session.execute(statement)

    job_id: UUID = result.scalar()
    return job_id


def insert_logs(job_id: UUID, logs: Iterable[Log]) -> None:
    """Insert multiple log rows"""
    # Convert the `utils` Logs to `database` Logs
    db_logs: list[database.Log] = []
    for log in logs:
        db_log = database.Log(
            job_id=job_id, level=log.level, message=log.message,
            timestamp=log.timestamp
        )
        db_logs.append(db_log)

    with _db.session.begin():
        for log in db_logs:
            _db.session.add(log)


def _dedup_progress(
    progress_list: Sequence[Progress]
) -> Generator[Progress, None, None]:
    """Filter the given Progress list by only returning a single entry
    for each filename

    The last Progress entry in the list is yielded for each filename.

    The Progress entries are yielded in reverse order.

    This is needed because `on_conflict_do_update()` will raise an
    exception if you give it multiple rows that have the same conflict.
    """
    yielded_filenames = set()
    for progress in reversed(progress_list):
        if progress.filename not in yielded_filenames:
            yield progress
            yielded_filenames.add(progress.filename)


def upsert_progress(job_id: UUID, progress_list: Sequence[Progress]) -> None:
    """Update or insert multiple progress rows"""
    # Convert the `utils` Progress entries to dicts that we can pass to
    # the statement
    db_progress_list: list[dict[str, Any]] = []
    for progress in _dedup_progress(progress_list):
        db_progress = {
            'job_id': job_id,
            'filename': progress.filename,
            'progress': progress.progress,
            'timestamp': progress.timestamp
        }
        db_progress_list.append(db_progress)

    # Postgres dialect is used because it supports
    # `on_conflict_do_update()`
    #
    # The values are baked into the statement instead of being passed to
    # `execute()` because SQLAlchemy will execute a separate statement
    # for each row otherwise when using `on_conflict_do_update()`
    statement = postgres_insert(database.Progress)
    statement = statement.on_conflict_do_update(
        # Replace existing row if a row already exists for the file
        # that's currently downloading (same job_id and filename)
        index_elements=(database.Progress.job_id, database.Progress.filename),
        set_={
            database.Progress.progress: statement.excluded.progress,
            database.Progress.timestamp: statement.excluded.timestamp,
        }
    ).values(db_progress_list)
    with _db.session.begin():
        _db.session.execute(statement)
