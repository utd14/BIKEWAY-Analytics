import pandas as pd
import matplotlib.pyplot as plt
import os
from config import get_engine

plt.style.use('seaborn-v0_8-darkgrid')

CHARTS_DIR = 'charts'
os.makedirs(CHARTS_DIR, exist_ok=True)

engine = get_engine()
# PLOTLY - Interactive Time Slider
import plotly.express as px

print()
print("Plotly Interactive Time Slider")

# Daily revenue by month for each store
query_plotly = """
SELECT DATE_TRUNC('month', o.order_date)::date as month,
       s.store_name,
       COUNT(o.order_id) as monthly_orders,
       SUM(oi.quantity * oi.list_price * (1 - oi.discount)) as monthly_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN stores s ON o.store_id = s.store_id
WHERE o.order_date IS NOT NULL
GROUP BY DATE_TRUNC('month', o.order_date)::date, s.store_name
ORDER BY month, store_name;
"""

df_plotly = pd.read_sql(query_plotly, engine)
print(f"\nRows retrieved: {len(df_plotly)}")
print(df_plotly.head(10))

fig = px.scatter(df_plotly, 
                 x="monthly_orders", 
                 y="monthly_revenue",
                 animation_frame="month",
                 animation_group="store_name",
                 size="monthly_revenue",
                 color="store_name",

                 hover_name="store_name",
                 size_max=60,
                 range_x=[0, df_plotly['monthly_orders'].max() + 20],
                 range_y=[0, df_plotly['monthly_revenue'].max() * 1.1],
                 title="Monthly Sales Performance by Store Over Time (All Years)",
                 labels={"monthly_orders": "Number of Orders", 
                         "monthly_revenue": "Monthly Revenue ($)",
                         "store_name": "Store"})

fig.update_layout(
    width=1200,
    height=700,
    font=dict(size=14),
    title_font=dict(size=18, family="Arial Black")
)

fig.show()

# print("Shows sales performance over time (montly) for each store")