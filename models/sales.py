from db import get_cursor

def get_monthly_revenue():
    cursor = get_cursor()
    cursor.execute("""
        SELECT
            YEAR(o.order_date)                  AS year,
            MONTH(o.order_date)                 AS month,
            SUM(oi.quantity * oi.unit_price)    AS revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY YEAR(o.order_date), MONTH(o.order_date)
        ORDER BY year, month
    """)
    return cursor.fetchall()

def get_revenue_by_category():
    cursor = get_cursor()
    cursor.execute("""
        SELECT
            p.category,
            SUM(oi.quantity)                    AS units_sold,
            SUM(oi.quantity * oi.unit_price)    AS revenue
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY p.category
        ORDER BY revenue DESC
    """)
    return cursor.fetchall()

def get_total_revenue():
    cursor = get_cursor()
    cursor.execute("SELECT SUM(quantity * unit_price) AS total FROM order_items")
    row = cursor.fetchone()
    return float(row["total"] or 0)

def get_total_orders():
    cursor = get_cursor()
    cursor.execute("SELECT COUNT(*) AS total FROM orders")
    return cursor.fetchone()["total"]

def get_recent_orders(limit=10):
    cursor = get_cursor()
    cursor.execute("""
        SELECT
            o.order_id,
            c.name          AS customer,
            o.order_date,
            o.status,
            SUM(oi.quantity * oi.unit_price) AS order_total
        FROM orders o
        JOIN customers   c  ON o.customer_id = c.customer_id
        JOIN order_items oi ON o.order_id    = oi.order_id
        GROUP BY o.order_id, c.name, o.order_date, o.status
        ORDER BY o.order_date DESC
        LIMIT %s
    """, (limit,))
    return cursor.fetchall()
