from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class GenerateRequest(BaseModel):
    goal: str
    team_size: Optional[int] = Field(default=1, ge=1)
    mode: Optional[str] = Field(default="balanced")

class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    est_hours: float
    dependencies: List[str] = []
    risk_score: Optional[int] = 1
    start: Optional[str] = None
    end: Optional[str] = None

class VariantPlan(BaseModel):
    tasks: List[Task]
    critical_path: List[str]
    reasoning: Optional[str] = None

class GenerateResponse(BaseModel):
    plan_id: str
    variants: Dict[str, VariantPlan]
    summary: Optional[str] = None
    assumptions: Optional[str] = None