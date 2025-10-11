# BIKEWAY Analytics
# About us
**BIKEWAY** is a growing bike retail company operating multiple stores across different cities. We specialize in selling bikes, cycling accessories, and related products from various popular brands.\
\
As a data analyst at BIKEWAY, I work with our sales, inventory, and customer data to help the business make informed decisions. Our analytics focus on: 
- **Sales Performance**: Tracking revenue across different stores and time
- **Product Analytics**: Identifying best-selling products and popular brands
- **Customer Insights**: Analysing customer buying patterns and loyalty
- **Inventory Management**: Monitoring stock levels for prevention of shortages
- **Staff Performance**: Analyzing our team's efficiency 

# Main Analytics
![Monthly Sales](analytics/charts/4_line_monthly_sales.png)
![Top Products](analytics/charts/3_horizontal_bar_top_products.png)

# Installation
## Prerequisites
- PostgreSQL (version 12 or higher)
- Python 3.8+
## Tool installation (Windows 10)
1. Download PostgreSQL from https://www.postgresql.org/download/windows/ 
   - run installer, set password for postgres user (remember it)
   - keep default port 5432
2. Download Python from https://www.python.org/downloads/
   - get latest 3.x version
   - run installer
   - check "Add Python to PATH"
3. Open Command Prompt (Win+R, type `cmd`)
4. Check installations
   ```cmd
   python --version
   psql --version
   ```
5. Navigate to your project folder
   ```cmd
   cd C:\path\to\your\project
   ```
6. Install libraries
   - `pip install pandas matplotlib plotly openpyxl sqlalchemy numpy psycopg2`
   - `pip install mysql-connector-python`
   - `pip install psycopg2-binary`

## Database Connection
- In the `installation` folder open `db_create.py` and enter your desired database name on the line 14 (`NEW_DB_NAME = 'bike_sales_test1'  # CHANGE THE NAME`), as well as your PosgtreSQL username and password.
- In the same folder, run `python db_create.py`, `python tables_create.py` and `python data_import.py` in this order.
- Run `python main.py` from the main folder.
   ```cmd
   cd C:\path\to\your\folder
   pip install psycopg2-binary
   python main.py
   ```
- For data analytics, run `python analytics.py` from the analytics folder.

# Tools and Resources
Bike Store Relational Database by Dillon Myrick \
PostgreSQL - Relational database management system \
SQL - Query language for data analysis \
Python - Data manipulation and automation \
Apache Superset - Data visualization platform \
VS Code - Code editor 
