from agents.llm import llm
def detect_intent(customer_message, chat_history=None):
    conversation = ""
    if chat_history:
        conversation = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in chat_history
        )
    prompt = f"""
    You are an intent classification agent for a customer support system.

    Classify the customer's latest message into exactly one category:

    1. knowledge
       Questions about product information, FAQs, returns,
       refunds, warranty, and company policies.

    2. order_status
       Questions about tracking an order, checking delivery status,
       or follow-up questions about a previously discussed order.

    3. create_ticket
       Complaints, damaged products, missing items, or unresolved issues
       that require a support ticket.

    4. escalation
       Requests to speak with a human support representative.

    IMPORTANT:
    - Use previous conversation to understand follow-up questions.
    - If the customer asks "When will it arrive?" after discussing
      an order, classify it as order_status.
    - If the customer asks "Is it delivered?" after discussing
      an order, classify it as order_status.
    - Classify based on the latest customer message and its context.

    Previous Conversation:
    {conversation}

    Latest Customer Message:
    {customer_message}

    Return ONLY the category name.
    Do not provide explanations.
    """
    response = llm.invoke(prompt)
    intent = response.content.strip().lower()
    allowed_intents = [
        "knowledge",
        "order_status",
        "create_ticket",
        "escalation"
    ]
    if intent not in allowed_intents:
        return "knowledge"
    return intent
