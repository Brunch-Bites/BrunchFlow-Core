from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..agents.demand_predictor import DemandPredictor
from ..agents.fleet_router import FleetRouter

app = FastAPI(
    title="BrunchFlow Core API",
    description="Next-Generation Gastronomy Orchestration Engine",
    version="1.0.0"
)

# 初始化 Agent
demand_agent = DemandPredictor("DP-001")
router_agent = FleetRouter("FR-001")

class OrchestrationRequest(BaseModel):
    location: str
    priority: Optional[str] = "standard"

@app.get("/")
async def root():
    return {"message": "BrunchFlow Core Orchestrator is operational"}

@app.post("/orchestrate")
async def run_orchestration(request: OrchestrationRequest):
    """
    运行完整的调度流程：由于预测阶段启动，随后优化路由。
    """
    try:
        # 1. 需求预测
        prediction = await demand_agent.process({"location": request.location})
        
        # 2. 路由优化
        routing = await router_agent.process({"demand_predictions": prediction})
        
        return {
            "status": "success",
            "orchestration_id": "ORC-" + request.location[:3].upper(),
            "results": {
                "demand": prediction,
                "logistics": routing
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
