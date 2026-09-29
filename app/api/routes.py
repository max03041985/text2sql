import logging
import time
import urllib.parse
import uuid

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.config import settings
from app.llm.client import generate_sql
from app.sql.executor import execute_query_preview, stream_query_to_csv
from app.sql.validator import SQLValidationError, validate_sql

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Text-to-SQL"])

class TextToSQLRequest(BaseModel):
    query: str = Field(..., description="Natural language query", min_length=3)

class TextToSQLResponse(BaseModel):
    sql: str
    explanation: str
    preview: list[dict]

@router.post("/text-to-sql", response_model=TextToSQLResponse)
async def text_to_sql(request: TextToSQLRequest):
    request_id = uuid.uuid4().hex[:8]
    request_started = time.perf_counter()
    stage = "request_received"
    logger.info(
        "request_id=%s text_to_sql request received query_length=%d",
        request_id,
        len(request.query),
    )

    try:
        stage = "llm"
        stage_started = time.perf_counter()
        logger.info(
            "request_id=%s stage=llm started model=%s timeout_seconds=%d",
            request_id,
            settings.LLM_MODEL,
            settings.LLM_TIMEOUT,
        )
        llm_result = await generate_sql(request.query)
        logger.info(
            "request_id=%s stage=llm completed duration_seconds=%.2f",
            request_id,
            time.perf_counter() - stage_started,
        )

        raw_sql = llm_result.get("sql", "")
        explanation = llm_result.get("explanation", "")

        if not raw_sql:
            raise HTTPException(status_code=400, detail="LLM failed to generate SQL")

        stage = "sql_validation"
        stage_started = time.perf_counter()
        logger.info("request_id=%s stage=sql_validation started", request_id)
        validated_sql = validate_sql(raw_sql)
        logger.info(
            "request_id=%s stage=sql_validation completed duration_seconds=%.2f sql_length=%d",
            request_id,
            time.perf_counter() - stage_started,
            len(validated_sql),
        )

        stage = "postgresql_preview"
        stage_started = time.perf_counter()
        logger.info(
            "request_id=%s stage=postgresql_preview started row_limit=10 statement_timeout=%s",
            request_id,
            settings.STATEMENT_TIMEOUT,
        )
        preview = await execute_query_preview(validated_sql, limit=10)
        logger.info(
            "request_id=%s stage=postgresql_preview completed duration_seconds=%.2f rows=%d",
            request_id,
            time.perf_counter() - stage_started,
            len(preview),
        )
        logger.info(
            "request_id=%s text_to_sql completed duration_seconds=%.2f",
            request_id,
            time.perf_counter() - request_started,
        )

        return {"sql": validated_sql, "explanation": explanation, "preview": preview}
    except SQLValidationError as e:
        logger.warning(
            "request_id=%s stage=%s failed duration_seconds=%.2f error=%s",
            request_id,
            stage,
            time.perf_counter() - request_started,
            e,
        )
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except httpx.TimeoutException:
        logger.exception(
            "request_id=%s stage=%s timed out duration_seconds=%.2f",
            request_id,
            stage,
            time.perf_counter() - request_started,
        )
        raise HTTPException(
            status_code=504,
            detail=f"LLM timed out after {settings.LLM_TIMEOUT} seconds; increase LLM_TIMEOUT or use a faster model",
        )
    except Exception as e:
        logger.exception(
            "request_id=%s stage=%s failed duration_seconds=%.2f error_type=%s",
            request_id,
            stage,
            time.perf_counter() - request_started,
            type(e).__name__,
        )
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/stream-csv")
async def stream_csv(sql_query: str):
    try:
        validated_sql = validate_sql(sql_query)
    except SQLValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    filename = "campaign_cohort_export.csv"
    encoded_filename = urllib.parse.quote(filename)

    return StreamingResponse(
        stream_query_to_csv(validated_sql),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"}
    )
