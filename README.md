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

# ER Diagram
The database consists of 8 columns: customers, staffs, stores, orders, order_items, products, categories, brands, stocks \
You can see infomration about the field of each colum, relationships and keys in the following diagram:
![](diagram.png)

# Installation
## Prerequisites
- PostgreSQL (version 12 or higher)
- Python 3.8+
- Docker Desktop installed and running
## Tool installation (Windows 10)
1. Download PostgreSQL from https://www.postgresql.org/download/windows/ 
   - run installer, set password for postgres user (remember it)
   - keep default port 5432
2. Download Python from https://www.python.org/downloads/
   - get latest 3.x version
   - run installer
   - check "Add Python to PATH"
3. Download Docker Desktop from https://www.docker.com/products/docker-desktop/
4. Open Command Prompt (Win+R, type `cmd`)
5. Check installations
   ```bash
   python --version
   psql --version
   ```
6. Navigate to your project folder
   ```bash
   cd C:\path\to\your\project
   ```
7. Install dependencies
   - `pip install -r requirements.txt`

## Database Connection
- In the `installation` folder open `db_create.py` and enter your desired database name on the line 14 (`NEW_DB_NAME = 'bike_sales_test1'  # CHANGE THE NAME`), as well as your PosgtreSQL username and password.
- In the same folder, run `python db_create.py`, `python tables_create.py` and `python data_import.py` in this order.

# Usage
## Test
- Run `python main.py` from the main folder.
   ```bash
   cd C:\path\to\your\folder
   pip install psycopg2-binary
   python main.py
   ```
## Data Analytics
- Run `python analytics.py` from the analytics folder.
## Grafana and Prometheus
- Start all services using Docker Compose:
```bash
docker-compose up -d
```
- Start custom exporter
   ```bash
   python custom_exporter.py
   ```
- Access URLs \
	**Prometheus**: http://localhost:9090 \
	**Grafana**: http://localhost:3001 (admin/admin) \
	**PostgreSQL Exporter**: http://localhost:9187/metrics \
	**Node Exporter**: http://localhost:9100/metrics \
	**Custom Exporter**: http://localhost:8000/metrics
- Login to Grafana: admin admin
- Add Prometheus Data Source (http://prometheus:9090)
- Import Dashboards
	1. Click **+** (plus icon in left sidebar) → **Import**
	2. Click **Upload JSON file**
	3. Select `dashboards/dashboard_1_database.json`
	4. **Select datasource:** Choose `Prometheus`
	5. Click **Import**
	6. Do the same with remaining dahsboards.

# Tools and Resources
Bike Store Relational Database by Dillon Myrick \
PostgreSQL - Relational database management system \
SQL - Query language for data analysis \
Python - Data manipulation and automation \
Apache Superset - Data visualization platform \
VS Code - Code editor \
Prometheus \
Grafana \
Docker Desktop
