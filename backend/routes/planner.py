from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.schemas import GenerateRequest, GenerateResponse
from services.llm_client import LLMClient
from services.planner_logic import PlannerLogic

router = APIRouter()
llm = LLMClient()
logic = PlannerLogic()

@router.post("/generate_plan", response_model=GenerateResponse)
async def generate_plan(payload: GenerateRequest):
    try:
        # Generate plan using LLM
        raw = llm.generate_plan(payload.dict())
        
        # Process the response
        processed = logic.process_llm_response(raw, payload.dict())
        
        # Return the processed plan directly (no database storage)
        resp = {
            "plan_id": f"plan_{len(raw.get('variants', {}).get('balanced', {}).get('tasks', []))}_{hash(payload.goal) % 10000}",
            "variants": processed["variants"],
            "summary": processed.get("summary", ""),
            "assumptions": processed.get("assumptions", ""),
        }
        return resp
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")