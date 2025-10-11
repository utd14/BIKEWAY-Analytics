-- 1. Total revenue by store
-- Shows a store that generates the most revenue
SELECT s.store_name, 
       SUM(oi.quantity * oi.list_price * (1 - oi.discount)) as total_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN stores s ON o.store_id = s.store_id
GROUP BY s.store_name
ORDER BY total_revenue DESC;

-- 2. Top 10 best-selliers
-- Identifies most popular products by sales
SELECT p.product_name, 
       b.brand_name,
       SUM(oi.quantity) as total_quantity_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN brands b ON p.brand_id = b.brand_id
GROUP BY p.product_name, b.brand_name
ORDER BY total_quantity_sold DESC
LIMIT 10;

-- 3. Monthly sales trend
-- Shows sales performance over time
SELECT DATE_TRUNC('month', order_date) as month,
       COUNT(o.order_id) as total_orders,
       SUM(oi.quantity * oi.list_price * (1 - oi.discount)) as monthly_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;


-- 4. Loyal customers
-- Identifies most loyal customers (purchase frequency)
SELECT c.customer_id,
       c.first_name || ' ' || c.last_name as customer_name,
       c.city,
       COUNT(o.order_id) as total_orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.city
ORDER BY total_orders DESC
LIMIT 10;


-- 5. Average order value by store
-- Calculates average revenue per item and compares customer spending across stores
SELECT s.store_name,
       COUNT(o.order_id) as total_orders,
       AVG(oi.quantity * oi.list_price * (1 - oi.discount)) as avg_order_value
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN stores s ON o.store_id = s.store_id
GROUP BY s.store_name
ORDER BY avg_order_value DESC;


-- 6. Product category performance
-- Shows which categories sell best
SELECT c.category_name,
       COUNT(DISTINCT oi.order_id) as orders_count,
       SUM(oi.quantity) as total_units_sold,
       SUM(oi.quantity * oi.list_price * (1 - oi.discount)) as category_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_name
ORDER BY category_revenue DESC;


-- 7. Inventory levels by store
-- Helps identify which items are low in stock
SELECT s.store_name,
       p.product_name,
       st.quantity as stock_quantity
FROM stocks st
JOIN stores s ON st.store_id = s.store_id
JOIN products p ON st.product_id = p.product_id
WHERE st.quantity < 10
ORDER BY st.quantity ASC;


-- 8. Staff performance by sales
-- Shows which staff members handle most orders
SELECT st.first_name || ' ' || st.last_name as staff_name,
       s.store_name,
       COUNT(o.order_id) as orders_processed
FROM orders o
JOIN staffs st ON o.staff_id = st.staff_id
JOIN stores s ON st.store_id = s.store_id
GROUP BY st.first_name, st.last_name, s.store_name
ORDER BY orders_processed DESC;


-- 9. Brand popularity analysis
-- Compares sales performance across brands
SELECT b.brand_name,
       COUNT(DISTINCT oi.order_id) as orders_with_brand,
       SUM(oi.quantity) as units_sold,
       AVG(oi.list_price) as avg_price -- for products of a brand across all order items
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN brands b ON p.brand_id = b.brand_id
GROUP BY b.brand_name
ORDER BY units_sold DESC;


-- 10. Order status distribution
-- Shows how many orders are in each status
-- 1: Pending, 2: Processing, 3: Rejected, 4: Completed
SELECT order_status,
       COUNT(*) as order_count,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;