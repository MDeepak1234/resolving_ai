from database.db import get_connection
def create_support_ticket(customer_id, subject, description):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO tickets (customer_id, subject, description)
        VALUES (?, ?, ?)
    """, (customer_id, subject, description))
    ticket_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return {
        "success": True,
        "ticket_id": ticket_id,
        "status": "Open",
        "message": "Support ticket created successfully."
    }
