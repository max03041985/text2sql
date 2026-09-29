import sqlglot
from sqlglot import exp
from app.config import settings

SCHEMA_REGISTRY = {
    "marketingdb.map_bank_campaign_data": {"active": True, "description": "Core behavioral profile"},
}

class SQLValidationError(Exception):
    pass

def validate_sql(sql: str, for_streaming: bool = False) -> str:
    try:
        parsed = sqlglot.parse_one(sql, read="postgres")
    except sqlglot.ParseError as e:
        raise SQLValidationError(f"Invalid SQL syntax: {e}")

    # 1. Read-only enforcement (universal)
    for node in parsed.walk():
        if isinstance(node, (exp.Delete, exp.Update, exp.Insert, exp.Drop,
                             exp.Create, exp.Truncate, exp.Alter)):
            raise SQLValidationError("Security Violation: Only SELECT queries are allowed.")

    # 2. Block SELECT * on Greenplum only (to avoid interconnect shuffling)
    #    On PostgreSQL it's allowed but discouraged — we leave it permissive.
    if settings.DB_TYPE == "greenplum":
        for node in parsed.walk():
            if isinstance(node, exp.Star):
                raise SQLValidationError(
                    "SELECT * is forbidden on Greenplum. Explicitly list required columns."
                )

    # 3. Schema validation (universal)
    active_tables = {k for k, v in SCHEMA_REGISTRY.items() if v["active"]}
    for node in parsed.walk():
        if isinstance(node, exp.Table):
            table_name = node.sql().lower().replace('"', '')
            full_name = table_name if "." in table_name else f"marketingdb.{table_name}"
            if full_name not in active_tables:
                raise SQLValidationError(
                    f"Access denied to table '{full_name}'. Active: {', '.join(active_tables)}"
                )

    # 4. Enforce LIMIT for streaming (universal safety net)
    if for_streaming:
        has_limit = any(isinstance(n, exp.Limit) for n in parsed.walk())
        if not has_limit:
            sql = sql.rstrip(";") + f" LIMIT {settings.MAX_STREAM_ROWS}"
            parsed = sqlglot.parse_one(sql, read="postgres")

    return parsed.sql(dialect="postgres")