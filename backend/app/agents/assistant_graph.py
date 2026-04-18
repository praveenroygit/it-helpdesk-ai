from langgraph.graph import StateGraph

# -------------------------
# RAG NODE
# -------------------------
def rag_node(state):
    from app.services.rag_service import query_rag

    query = state["query"]
    response = query_rag(query)

    # SMART ROUTING
    keywords = ["password", "account", "login"]

    if any(word in query.lower() for word in keywords):
        confidence = 0.8
    else:
        confidence = 0.2

    return {
        "response": response,
        "confidence": confidence
    }

# -------------------------
# TICKET NODE
# -------------------------
def ticket_node(state):
    return {
        "response": "Ticket created successfully. Our support team will contact you shortly."
    }

# -------------------------
# ROUTER
# -------------------------
def router(state):
    if state["confidence"] > 0.5:
        return "end"
    else:
        return "ticket"

# -------------------------
# GRAPH
# -------------------------
graph = StateGraph(dict)

graph.add_node("rag", rag_node)
graph.add_node("ticket", ticket_node)

graph.set_entry_point("rag")

graph.add_conditional_edges(
    "rag",
    router,
    {
        "end": "__end__",
        "ticket": "ticket"
    }
)

graph.set_finish_point("ticket")

app_graph = graph.compile()