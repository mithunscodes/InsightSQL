from db import get_db

def get_top_customers(limit=10):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            c.customer_id,
            c.name,
            c.city,
            COUNT(DISTINCT o.order_id)          AS total_orders,
            SUM(oi.quantity * oi.unit_price)    AS total_spent
        FROM customers c
        JOIN orders      o  ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id    = oi.order_id
        GROUP BY c.customer_id, c.name, c.city
        ORDER BY total_spent DESC
        LIMIT %s
    """, (limit,))
    return cursor.fetchall()

def get_revenue_by_city():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            c.city,
            COUNT(DISTINCT c.customer_id)       AS customers,
            COUNT(DISTINCT o.order_id)          AS orders,
            SUM(oi.quantity * oi.unit_price)    AS revenue
        FROM customers c
        JOIN orders      o  ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id    = oi.order_id
        GROUP BY c.city
        ORDER BY revenue DESC
    """)
    return cursor.fetchall()

def get_customer_detail(customer_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            c.name,
            c.email,
            c.city,
            c.joined_date,
            o.order_id,
            o.order_date,
            o.status,
            SUM(oi.quantity * oi.unit_price) AS order_total
        FROM customers c
        JOIN orders      o  ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id    = oi.order_id
        WHERE c.customer_id = %s
        GROUP BY o.order_id, c.name, c.email, c.city, c.joined_date, o.order_date, o.status
        ORDER BY o.order_date DESC
    """, (customer_id,))
    return cursor.fetchall()

def get_all_customers():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            c.customer_id,
            c.name,
            c.email,
            c.city,
            c.joined_date,
            COUNT(DISTINCT o.order_id)                              AS total_orders,
            COALESCE(SUM(oi.quantity * oi.unit_price), 0)           AS total_spent
        FROM customers c
        LEFT JOIN orders      o  ON c.customer_id = o.customer_id
        LEFT JOIN order_items oi ON o.order_id    = oi.order_id
        GROUP BY c.customer_id, c.name, c.email, c.city, c.joined_date
        ORDER BY total_spent DESC
    """)
    return cursor.fetchall()
