from fastapi import APIRouter
from app.agents.assistant_graph import app_graph

router = APIRouter()

@router.get("/chat")
def chat(query: str):
    result = app_graph.invoke({
        "query": query
    })
    return {"response": result["response"]}