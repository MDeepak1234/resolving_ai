
import re

from graph.state import SupportState
from agents.intent_agent import detect_intent
from agents.knowledge_agent import knowledge_agent
from agents.action_agent import action_agent


def intent_node(state: SupportState):
    customer_message = state["customer_message"]
    chat_history = state.get("chat_history", [])

    intent = detect_intent(
        customer_message,
        chat_history
    )

    print("Detected Intent:", intent)

    return {"intent": intent}


def knowledge_node(state: SupportState):
    customer_message = state["customer_message"]
    chat_history = state.get("chat_history", [])

    result = knowledge_agent(
        customer_message,
        chat_history
    )

    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }


def action_node(state: SupportState):
    intent = state["intent"]
    customer_message = state["customer_message"]
    chat_history = state.get("chat_history", [])

    order_id = None

    if intent == "order_status":

        # First check the latest customer message
        match = re.search(
            r"\bORD\d+\b",
            customer_message,
            re.IGNORECASE
        )

        if match:
            order_id = match.group(0).upper()

        else:
            # Search previous conversation messages
            for message in reversed(chat_history):
                match = re.search(
                    r"\bORD\d+\b",
                    message["content"],
                    re.IGNORECASE
                )

                if match:
                    order_id = match.group(0).upper()
                    break

    result = action_agent(
        intent=intent,
        customer_message=customer_message,
        order_id=order_id
    )

    return {"answer": result["message"]}


def escalation_node(state: SupportState):
    customer_message = state["customer_message"]

    print("Escalation requested for:", customer_message)

    return {
        "answer": (
            "I understand you need assistance from a human support "
            "representative. Your request has been identified for "
            "human assistance. Please contact our support team "
            "for further help."
        )
    }
