
from langgraph.graph import StateGraph, START, END

from graph.state import SupportState
from graph.nodes import (
    intent_node,
    knowledge_node,
    action_node,
    escalation_node
)

def route_by_intent(state: SupportState):
    intent = state["intent"]

    if intent == "knowledge":
        return "knowledge"

    elif intent in ["order_status", "create_ticket"]:
        return "action"

    elif intent == "escalation":
        return "escalation"

    return "knowledge"


def build_workflow():

    graph = StateGraph(SupportState)

    graph.add_node("intent", intent_node)
    graph.add_node("knowledge", knowledge_node)
    graph.add_node("action", action_node)
    graph.add_node("escalation", escalation_node)

    graph.add_edge(START, "intent")

    graph.add_conditional_edges(
        "intent",
        route_by_intent,
        {
            "knowledge": "knowledge",
            "action": "action",
            "escalation": "escalation"
        }
    )

    graph.add_edge("knowledge", END)
    graph.add_edge("action", END)
    graph.add_edge("escalation", END)

    return graph.compile()


support_workflow = build_workflow()
