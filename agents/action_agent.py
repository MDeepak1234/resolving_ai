
from tools.order_tools import get_order_status
from tools.ticket_tools import create_support_ticket

def action_agent(intent, customer_message, order_id=None):
    if intent == "order_status":

        if not order_id:
            return {
                "success": False,
                "message": "Please provide your order ID so I can check its status."
            }

        result = get_order_status(order_id)

        if not result["found"]:
            return {
                "success": False,
                "message": result["message"]
            }

        return {
            "success": True,
            "message": (
                f"Order {result['order_id']} is currently "
                f"{result['status']}. "
                f"Estimated delivery: {result['estimated_delivery']}."
            )
        }

    elif intent == "create_ticket":

        result = create_support_ticket(
            customer_id="CUST1001",
            subject="Customer Support Request",
            description=customer_message
        )

        return {
            "success": result["success"],
            "message": (
                f"Your support ticket has been created successfully. "
                f"Ticket ID: {result['ticket_id']}. "
                f"Status: {result['status']}."
            )
        }

    return {
        "success": False,
        "message": "This action is not supported."
    }
