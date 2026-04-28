from db import get_cursor

def get_top_products(n=5):
    cursor = get_cursor()
    cursor.execute("""
        SELECT
            p.name,
            p.category,
            SUM(oi.quantity)                    AS units_sold,
            SUM(oi.quantity * oi.unit_price)    AS revenue
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY p.product_id, p.name, p.category
        ORDER BY revenue DESC
        LIMIT %s
    """, (n,))
    return cursor.fetchall()

def get_all_products():
    cursor = get_cursor()
    cursor.execute("""
        SELECT
            p.product_id,
            p.name,
            p.category,
            p.price,
            p.stock_quantity,
            COALESCE(SUM(oi.quantity), 0)                   AS units_sold,
            COALESCE(SUM(oi.quantity * oi.unit_price), 0)   AS revenue
        FROM products p
        LEFT JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY p.product_id, p.name, p.category, p.price, p.stock_quantity
        ORDER BY revenue DESC
    """)
    return cursor.fetchall()

def get_low_stock(threshold=50):
    cursor = get_cursor()
    cursor.execute("""
        SELECT name, category, stock_quantity
        FROM products
        WHERE stock_quantity < %s
        ORDER BY stock_quantity ASC
    """, (threshold,))
    return cursor.fetchall()

def get_sales_summary():
    cursor = get_cursor()
    cursor.execute("SELECT * FROM sales_summary ORDER BY total_revenue DESC")
    return cursor.fetchall()
