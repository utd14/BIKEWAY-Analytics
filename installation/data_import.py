import pandas as pd
import psycopg2
from psycopg2 import sql
import os
import numpy as np
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_CONFIG

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(BASE_DIR, 'datasets')

csv_files = {
    'brands': 'brands.csv',
    'categories': 'categories.csv',
    'customers': 'customers.csv',
    'order_items': 'order_items.csv',
    'orders': 'orders.csv',
    'products': 'products.csv',
    'staffs': 'staffs.csv',
    'stocks': 'stocks.csv',
    'stores': 'stores.csv'
}

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

tables_to_clear = ['order_items', 'orders', 'stocks', 'products', 'staffs', 
                   'customers', 'stores', 'categories', 'brands']

for table in tables_to_clear:
    cursor.execute(f"TRUNCATE TABLE {table} CASCADE")

conn.commit()

for table_name, csv_file in csv_files.items():
    file_path = os.path.join(DATASETS_DIR, csv_file)
    
    #if not os.path.exists(file_path):
        #print(f"File not found: {file_path}")
        #continue
    
    df = pd.read_csv(file_path)

    df = pd.read_csv(file_path)
    df = df.replace({np.nan: None})
    
    columns = ', '.join(df.columns)
    placeholders = ', '.join(['%s'] * len(df.columns))
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    
    for index, row in df.iterrows():
        cursor.execute(insert_query, tuple(row))
    
    conn.commit()
    print(f"Imported {len(df)} rows into {table_name}")

cursor.close()
conn.close()


print("Success.")
