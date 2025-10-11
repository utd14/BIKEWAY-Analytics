import psycopg2
from psycopg2 import sql
import os

DB_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'utedana1404',
    'host': 'localhost',
    'port': '5432'
}

NEW_DB_NAME = 'bike_sales_test1'  # CHANGE THE NAME

conn = psycopg2.connect(**DB_CONFIG)
conn.autocommit = True
cursor = conn.cursor()

cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [NEW_DB_NAME])
exists = cursor.fetchone()

if not exists:
    cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(NEW_DB_NAME)))
    print(f"'{NEW_DB_NAME}' created.")
else:
    print(f"'{NEW_DB_NAME}' already exists.")

cursor.close()
conn.close()

# Creates config.py
config_content = f"""import psycopg2
from sqlalchemy import create_engine

DB_CONFIG = {{
    'dbname': '{NEW_DB_NAME}',
    'user': '{DB_CONFIG['user']}',
    'password': '{DB_CONFIG['password']}',
    'host': '{DB_CONFIG['host']}',
    'port': '{DB_CONFIG['port']}'
}}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_engine():
    connection_string = f"postgresql://{{DB_CONFIG['user']}}:{{DB_CONFIG['password']}}@{{DB_CONFIG['host']}}:{{DB_CONFIG['port']}}/{{DB_CONFIG['dbname']}}"
    return create_engine(connection_string)
"""

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file_path = os.path.join(parent_dir, 'config.py')

with open(config_file_path, 'w') as f:
    f.write(config_content)

print(f"'{config_file_path}' created.")