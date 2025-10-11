import psycopg2
from sqlalchemy import create_engine

DB_CONFIG = {
    'dbname': 'bike_sales',
    'user': 'postgres',
    'password': 'utedana1404',
    'host': 'localhost',
    'port': '5432'
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_engine():
    connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    return create_engine(connection_string)
