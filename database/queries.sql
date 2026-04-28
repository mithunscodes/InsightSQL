-- InsightSQL - Reference Queries

-- 1. Total revenue per customer (multi-table JOIN + aggregation)
SELECT
    c.name,
    c.city,
    COUNT(DISTINCT o.order_id)          AS total_orders,
    SUM(oi.quantity * oi.unit_price)    AS total_spent
FROM customers c
JOIN orders     o  ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id   = oi.order_id
GROUP BY c.customer_id, c.name, c.city
ORDER BY total_spent DESC;

-- 2. Monthly revenue trend
SELECT
    YEAR(o.order_date)                   AS year,
    MONTH(o.order_date)                  AS month,
    SUM(oi.quantity * oi.unit_price)     AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY YEAR(o.order_date), MONTH(o.order_date)
ORDER BY year, month;

-- 3. Revenue by product category
SELECT
    p.category,
    SUM(oi.quantity)                     AS units_sold,
    SUM(oi.quantity * oi.unit_price)     AS revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY revenue DESC;

-- 4. Top 5 products by revenue
SELECT
    p.name,
    p.category,
    SUM(oi.quantity)                     AS units_sold,
    SUM(oi.quantity * oi.unit_price)     AS revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name, p.category
ORDER BY revenue DESC
LIMIT 5;

-- 5. Sales summary view usage
SELECT * FROM sales_summary ORDER BY total_revenue DESC;

-- 6. Customer order history with items
SELECT
    c.name        AS customer,
    o.order_date,
    o.status,
    p.name        AS product,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) AS line_total
FROM customers c
JOIN orders      o  ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id    = oi.order_id
JOIN products    p  ON oi.product_id = p.product_id
ORDER BY o.order_date DESC;

-- 7. Low stock alert
SELECT name, category, stock_quantity
FROM products
WHERE stock_quantity < 50
ORDER BY stock_quantity ASC;
