import psycopg2
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_CONFIG

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

tables = [
    """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INT PRIMARY KEY,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        phone VARCHAR(25),
        email VARCHAR(255),
        street VARCHAR(255),
        city VARCHAR(50),
        state VARCHAR(25),
        zip_code VARCHAR(5)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS stores (
        store_id INT PRIMARY KEY,
        store_name VARCHAR(255),
        phone VARCHAR(25),
        email VARCHAR(255),
        street VARCHAR(255),
        city VARCHAR(50),
        state VARCHAR(25),
        zip_code VARCHAR(5)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS staffs (
        staff_id INT PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        email VARCHAR(255),
        phone VARCHAR(25),
        active INT,
        store_id INT,
        manager_id INT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS categories (
        category_id INT PRIMARY KEY,
        category_name VARCHAR(255)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS brands (
        brand_id INT PRIMARY KEY,
        brand_name VARCHAR(255)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS products (
        product_id INT PRIMARY KEY,
        product_name VARCHAR(255),
        brand_id INT,
        category_id INT,
        model_year INT,
        list_price DECIMAL(10, 2)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS orders (
        order_id INT PRIMARY KEY,
        customer_id INT,
        order_status INT,
        order_date DATE,
        required_date DATE,
        shipped_date DATE,
        store_id INT,
        staff_id INT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS order_items (
        order_id INT,
        item_id INT,
        product_id INT,
        quantity INT,
        list_price DECIMAL(10, 2),
        discount DECIMAL(4, 2),
        PRIMARY KEY (order_id, item_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS stocks (
        store_id INT,
        product_id INT,
        quantity INT,
        PRIMARY KEY (store_id, product_id)
    );
    """
]

for table_sql in tables:
    cursor.execute(table_sql)

conn.commit()

foreign_keys = [
    # staffs 
    """
    ALTER TABLE staffs ADD CONSTRAINT fk_staffs_store 
        FOREIGN KEY (store_id) REFERENCES stores(store_id);
    """,
    """
    ALTER TABLE staffs ADD CONSTRAINT fk_staffs_manager 
        FOREIGN KEY (manager_id) REFERENCES staffs(staff_id);
    """,
    # orders 
    """
    ALTER TABLE orders ADD CONSTRAINT fk_orders_customer 
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id);
    """,
    """
    ALTER TABLE orders ADD CONSTRAINT fk_orders_store 
        FOREIGN KEY (store_id) REFERENCES stores(store_id);
    """,
    """
    ALTER TABLE orders ADD CONSTRAINT fk_orders_staff 
        FOREIGN KEY (staff_id) REFERENCES staffs(staff_id);
    """,
    # order_items 
    """
    ALTER TABLE order_items ADD CONSTRAINT fk_order_items_order 
        FOREIGN KEY (order_id) REFERENCES orders(order_id);
    """,
    """
    ALTER TABLE order_items ADD CONSTRAINT fk_order_items_product 
        FOREIGN KEY (product_id) REFERENCES products(product_id);
    """,
    # products 
    """
    ALTER TABLE products ADD CONSTRAINT fk_products_category 
        FOREIGN KEY (category_id) REFERENCES categories(category_id);
    """,
    """
    ALTER TABLE products ADD CONSTRAINT fk_products_brand 
        FOREIGN KEY (brand_id) REFERENCES brands(brand_id);
    """,
    # stocks 
    """
    ALTER TABLE stocks ADD CONSTRAINT fk_stocks_store 
        FOREIGN KEY (store_id) REFERENCES stores(store_id);
    """,
    """
    ALTER TABLE stocks ADD CONSTRAINT fk_stocks_product 
        FOREIGN KEY (product_id) REFERENCES products(product_id);
    """
]

cursor.close()
conn.close()


print("Success.")
