import asyncio
import csv
import io
import psycopg
from app.config import settings

def _get_sync_dsn() -> str:
    return settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

def _apply_session_settings(conn: psycopg.Connection) -> None:
    """Apply DB-specific session settings. Safe on both PG and GP."""
    conn.execute(f"SET statement_timeout = '{settings.STATEMENT_TIMEOUT}'")
    conn.execute(f"SET work_mem = '{settings.WORK_MEM}'")

    if settings.DB_TYPE == "greenplum":
        # These SET commands are Greenplum-specific and will ERROR on PostgreSQL
        conn.execute(f"SET statement_mem = '{settings.GP_STATEMENT_MEM}'")
        conn.execute(f"SET max_cursor_memory = '{settings.GP_MAX_CURSOR_MEMORY}'")

async def execute_query_preview(sql: str, limit: int = 10) -> list[dict]:
    """Preview query — works identically on PG and GP."""
    if "limit" not in sql.lower():
        sql = sql.rstrip(";") + f" LIMIT {limit}"

    def _sync_preview():
        with psycopg.connect(_get_sync_dsn()) as conn:
            _apply_session_settings(conn)
            with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                cur.execute(sql)
                return cur.fetchall()

    return await asyncio.to_thread(_sync_preview)

async def stream_query_to_csv(sql: str):
    """
    Universal streaming via COPY TO STDOUT.
    Works on both PostgreSQL (streams from single node) and
    Greenplum (streams in parallel from all segments).
    """
    queue: asyncio.Queue = asyncio.Queue(maxsize=50)

    def _producer():
        try:
            conn = psycopg.connect(_get_sync_dsn())
            try:
                _apply_session_settings(conn)
                copy_sql = f"COPY ({sql.rstrip(';')}) TO STDOUT WITH (FORMAT CSV, HEADER TRUE)"

                def _sink(data: bytes):
                    # psycopg calls this synchronously; push to async queue
                    asyncio.run_coroutine_threadsafe(
                        queue.put(data.decode("utf-8")), asyncio.get_event_loop()
                    ).result()

                with conn.cursor() as cur:
                    cur.copy(copy_sql, sink=_sink)
            finally:
                conn.close()
        finally:
            asyncio.run_coroutine_threadsafe(queue.put(None), asyncio.get_event_loop()).result()

    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, _producer)

    while True:
        chunk = await queue.get()
        if chunk is None:
            break
        yield chunk