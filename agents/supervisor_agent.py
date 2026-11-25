
import re
from agents.intent_agent import detect_intent
from agents.knowledge_agent import knowledge_agent
from agents.action_agent import action_agent

def supervisor_agent(customer_message):
    intent = detect_intent(customer_message)
    if intent == "knowledge":
        result = knowledge_agent(customer_message)
        return {
            "intent": intent,
            "answer": result["answer"],
            "sources": result["sources"]
        }
    elif intent == "order_status":
        match = re.search(
            r"\bORD\d+\b",
            customer_message,
            re.IGNORECASE
        )
        order_id = match.group(0).upper() if match else None
        result = action_agent(
            intent=intent,
            customer_message=customer_message,
            order_id=order_id
        )
        return {
            "intent": intent,
            "answer": result["message"],
            "sources": []
        }
    elif intent == "create_ticket":
        result = action_agent(
            intent=intent,
            customer_message=customer_message
        )
        return {
            "intent": intent,
            "answer": result["message"],
            "sources": []
        }
    elif intent == "escalation":
        return {
            "intent": intent,
            "answer": (
                "I understand you would like to speak with a human "
                "support representative. Your request needs human assistance."
            ),
            "sources": []
        }
    return {
        "intent": "unknown",
        "answer": "Sorry, I could not understand your request.",
        "sources": []
    }
