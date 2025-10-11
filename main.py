import psycopg2
from config import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("SELECT * FROM customers LIMIT 10;")
for row in cursor.fetchall():
    print(" | ".join(str(x) for x in row))
print()

cursor.execute("""
SELECT customer_id, first_name, last_name, city, state
FROM customers
WHERE city = 'New York'
ORDER BY last_name;
""")
for row in cursor.fetchall():
    print(" | ".join(str(x) for x in row))
print()

cursor.execute("""
SELECT c.category_name, 
       COUNT(p.product_id) as product_count,
       AVG(p.list_price) as avg_price,
       MIN(p.list_price) as min_price,
       MAX(p.list_price) as max_price
FROM products p
JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_name
ORDER BY avg_price DESC;
""")
for row in cursor.fetchall():
    print(" | ".join(str(x) for x in row))
print()

cursor.execute("""
SELECT o.order_id, o.order_date, o.order_status,
       c.first_name, c.last_name, c.email
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
LIMIT 10;
""")
for row in cursor.fetchall():
    print(" | ".join(str(x) for x in row))

print("Queries\n")

print("-- 1. Total revenue by store\n-- Shows a store that generates the most revenue")
cursor.execute("""
SELECT s.store_name, 
       SUM(oi.quantity * oi.list_price * (1 - oi.discount)) as total_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN stores s ON o.store_id = s.store_id
GROUP BY s.store_name
ORDER BY total_revenue DESC;
""")
print(" | ".join([desc[0] for desc in cursor.description]))
for row in cursor.fetchall():
    print(" | ".join(str(x) for x in row))

#############################################

print("\n-- 2. Top 10 best-selliers\n-- Identifies most popular products by sales")
cursor.execute("""
SELECT p.product_name, 
       b.brand_name,
       SUM(oi.quantity) as total_quantity_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN brands b ON p.brand_id = b.brand_id
GROUP BY p.product_name, b.brand_name
ORDER BY total_quantity_sold DESC
LIMIT 10;
""")
print(" | ".join([desc[0] for desc in cursor.description]))
for row in cursor.fetchall():
    print(" | ".join(str(x) for x in row))

#############################################

print("\n--3. Monthly sales trend\n-- Shows sales performance over time")
cursor.execute("""
SELECT DATE_TRUNC('month', order_date) as month,
       COUNT(o.order_id) as total_orders,
       SUM(oi.quantity * oi.list_price * (1 - oi.discount)) as monthly_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;
""")
print(" | ".join([desc[0] for desc in cursor.description]))
for row in cursor.fetchall():
    print(" | ".join(str(x) for x in row))

#############################################

print("\n--4. Loyal customers\n-- Identifies most loyal customers (purchase frequency)")
cursor.execute("""
SELECT c.customer_id,
       c.first_name || ' ' || c.last_name as customer_name,
       c.city,
       COUNT(o.order_id) as total_orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.city
ORDER BY total_orders DESC
LIMIT 10;
""")
print(" | ".join([desc[0] for desc in cursor.description]))
for row in cursor.fetchall():
    print(" | ".join(str(x) for x in row))

#############################################

print("\n--5. Average order value by store\n-- Calculates average revenue per item and compares customer spending across stores")
cursor.execute("""
SELECT s.store_name,
       COUNT(o.order_id) as total_orders,
       AVG(oi.quantity * oi.list_price * (1 - oi.discount)) as avg_order_value
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN stores s ON o.store_id = s.store_id
GROUP BY s.store_name
ORDER BY avg_order_value DESC;
""")
print(" | ".join([desc[0] for desc in cursor.description]))
for row in cursor.fetchall():
    print(" | ".join(str(x) for x in row))

#############################################

print("\n-- 6. Product category performance\n-- Shows which categories sell best")
cursor.execute("""
SELECT c.category_name,
       COUNT(DISTINCT oi.order_id) as orders_count,
       SUM(oi.quantity) as total_units_sold,
       SUM(oi.quantity * oi.list_price * (1 - oi.discount)) as category_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_name
ORDER BY category_revenue DESC;
""")
print(" | ".join([desc[0] for desc in cursor.description]))
for row in cursor.fetchall():
    print(" | ".join(str(x) for x in row))

#############################################

print("\n-- 7. Inventory levels by store\n-- Helps identify which items are low in stock")
cursor.execute("""
SELECT s.store_name,
       p.product_name,
       st.quantity as stock_quantity
FROM stocks st
JOIN stores s ON st.store_id = s.store_id
JOIN products p ON st.product_id = p.product_id
WHERE st.quantity < 10
ORDER BY st.quantity ASC
LIMIT 30;
""")
print(" | ".join([desc[0] for desc in cursor.description]))
for row in cursor.fetchall():
    print(" | ".join(str(x) for x in row))

#############################################

print("\n-- 8. Staff performance by sales\n-- Shows which staff members handle most orders")
cursor.execute("""
SELECT st.first_name || ' ' || st.last_name as staff_name,
       s.store_name,
       COUNT(o.order_id) as orders_processed
FROM orders o
JOIN staffs st ON o.staff_id = st.staff_id
JOIN stores s ON st.store_id = s.store_id
GROUP BY st.first_name, st.last_name, s.store_name
ORDER BY orders_processed DESC;
""")
print(" | ".join([desc[0] for desc in cursor.description]))
for row in cursor.fetchall():
    print(" | ".join(str(x) for x in row))

#############################################

print("\n--9. Brand popularity analysis\n-- Compares sales performance across brands")
cursor.execute("""
SELECT b.brand_name,
       COUNT(DISTINCT oi.order_id) as orders_with_brand,
       SUM(oi.quantity) as units_sold,
       AVG(oi.list_price) as avg_price -- for products of a brand across all order items
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN brands b ON p.brand_id = b.brand_id
GROUP BY b.brand_name
ORDER BY units_sold DESC;
""")
print(" | ".join([desc[0] for desc in cursor.description]))
for row in cursor.fetchall():
    print(" | ".join(str(x) for x in row))

#############################################

print("\n-- 10. Order status distribution\n-- Shows how many orders are in each status\n-- 1: Pending, 2: Processing, 3: Rejected, 4: Completed")
cursor.execute("""
SELECT order_status,
       COUNT(*) as order_count,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;
""")
print(" | ".join([desc[0] for desc in cursor.description]))
for row in cursor.fetchall():
    print(" | ".join(str(x) for x in row))

cursor.close()
connection.close()