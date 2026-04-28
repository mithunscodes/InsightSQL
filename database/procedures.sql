-- InsightSQL - Stored Procedures

DELIMITER //

-- Get top N products by revenue
CREATE PROCEDURE GetTopProducts(IN n INT)
BEGIN
    SELECT
        p.name,
        p.category,
        SUM(oi.quantity)                    AS units_sold,
        SUM(oi.quantity * oi.unit_price)    AS revenue
    FROM products p
    JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.name, p.category
    ORDER BY revenue DESC
    LIMIT n;
END //

-- Get customer summary by city
CREATE PROCEDURE GetCityRevenue()
BEGIN
    SELECT
        c.city,
        COUNT(DISTINCT c.customer_id)       AS customers,
        COUNT(DISTINCT o.order_id)          AS orders,
        SUM(oi.quantity * oi.unit_price)    AS revenue
    FROM customers c
    JOIN orders      o  ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id    = oi.order_id
    GROUP BY c.city
    ORDER BY revenue DESC;
END //

-- Get monthly revenue for a given year
CREATE PROCEDURE GetMonthlyRevenue(IN yr INT)
BEGIN
    SELECT
        MONTH(o.order_date)                 AS month,
        SUM(oi.quantity * oi.unit_price)    AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE YEAR(o.order_date) = yr
    GROUP BY MONTH(o.order_date)
    ORDER BY month;
END //

DELIMITER ;
