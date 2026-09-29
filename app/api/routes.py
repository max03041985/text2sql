from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import urllib.parse
import httpx

from app.llm.client import generate_sql
from app.sql.validator import validate_sql, SQLValidationError
from app.sql.executor import execute_query_preview, stream_query_to_csv
from app.config import settings

router = APIRouter(prefix="/api/v1", tags=["Text-to-SQL"])

class TextToSQLRequest(BaseModel):
    query: str = Field(..., description="Natural language query", min_length=3)

class TextToSQLResponse(BaseModel):
    sql: str
    explanation: str
    preview: list[dict]

@router.post("/text-to-sql", response_model=TextToSQLResponse)
async def text_to_sql(request: TextToSQLRequest):
    print("✅ [STEP 1/4] Request received by FastAPI")
    try:
        print("⏳ [STEP 2/4] Calling Ollama LLM (this may take 30-60s on first run)...")
        llm_result = await generate_sql(request.query)
        print("✅ [STEP 3/4] LLM responded. Validating SQL...")
        
        raw_sql = llm_result.get("sql", "")
        explanation = llm_result.get("explanation", "")

        if not raw_sql:
            raise HTTPException(status_code=400, detail="LLM failed to generate SQL")

        validated_sql = validate_sql(raw_sql)
        
        print("⏳ [STEP 4/4] Executing preview query on PostgreSQL...")
        preview = await execute_query_preview(validated_sql, limit=10)
        print("🎉 [DONE] Successfully returning response to Streamlit!")

        return {"sql": validated_sql, "explanation": explanation, "preview": preview}
    except SQLValidationError as e:
        print(f"❌ SQL Validation Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except httpx.TimeoutException:
        print(f"❌ LLM Timeout after {settings.LLM_TIMEOUT}s")
        raise HTTPException(
            status_code=504,
            detail=f"LLM timed out after {settings.LLM_TIMEOUT} seconds; increase LLM_TIMEOUT or use a faster model",
        )
    except Exception as e:
        print(f"❌ Unexpected Error: {type(e).__name__}: {e}")
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