-- InsightSQL - Sales Analytics Dashboard
-- Schema Definition

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(100) UNIQUE,
    city        VARCHAR(50),
    joined_date DATE
);

CREATE TABLE IF NOT EXISTS products (
    product_id     INT PRIMARY KEY AUTO_INCREMENT,
    name           VARCHAR(100) NOT NULL,
    category       VARCHAR(50),
    price          DECIMAL(10,2),
    stock_quantity INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS orders (
    order_id    INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    order_date  DATE,
    status      VARCHAR(20) DEFAULT 'completed',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    item_id    INT PRIMARY KEY AUTO_INCREMENT,
    order_id   INT,
    product_id INT,
    quantity   INT,
    unit_price DECIMAL(10,2),
    FOREIGN KEY (order_id)   REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Indexes for optimised lookups
CREATE INDEX idx_order_date    ON orders(order_date);
CREATE INDEX idx_customer_id   ON orders(customer_id);
CREATE INDEX idx_product_id    ON order_items(product_id);

-- Sales summary view
CREATE OR REPLACE VIEW sales_summary AS
SELECT
    p.name                            AS product_name,
    p.category,
    SUM(oi.quantity)                  AS units_sold,
    SUM(oi.quantity * oi.unit_price)  AS total_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name, p.category;
