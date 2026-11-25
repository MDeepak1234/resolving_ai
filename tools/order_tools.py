
from database.db import get_connection

def get_order_status(order_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT order_id, customer_name, status, estimated_delivery
        FROM orders
        WHERE order_id = ?
    """, (order_id,))

    order = cursor.fetchone()
    connection.close()

    if order is None:
        return {
            "found": False,
            "message": f"No order found with ID {order_id}."
        }

    return {
        "found": True,
        "order_id": order["order_id"],
        "customer_name": order["customer_name"],
        "status": order["status"],
        "estimated_delivery": order["estimated_delivery"]
    }
