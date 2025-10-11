import psycopg2

connection = psycopg2.connect(
    host="localhost",
    database="bike_sales_new",
    user="postgres",
    password="utedana1404"
)

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

cursor.close()
connection.close()