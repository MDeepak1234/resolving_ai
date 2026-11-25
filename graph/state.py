from typing import TypedDict, List

class SupportState(TypedDict):
    customer_message: str
    chat_history: List[dict]
    intent: str
    order_id: str
    answer: str
    sources: List[str]