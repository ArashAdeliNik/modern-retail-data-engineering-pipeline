import os

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://pipeline:pipeline@postgres:5432/warehouse")

st.set_page_config(page_title="Retail Pipeline Dashboard", page_icon="📊", layout="wide")
st.title("Modern Retail Data Pipeline")
st.caption("Synthetic portfolio data • PostgreSQL • Airflow • dbt")

engine = create_engine(DATABASE_URL)
daily = pd.read_sql("select * from mart_daily_sales order by order_date", engine)
category = pd.read_sql("select * from mart_category_performance order by net_revenue desc", engine)

if daily.empty:
    st.warning("No transformed data is available yet. Run the pipeline first.")
    st.stop()

latest = daily.iloc[-1]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Latest revenue", f"€{latest['net_revenue']:,.2f}")
c2.metric("Completed orders", f"{int(latest['completed_orders']):,}")
c3.metric("Unique customers", f"{int(latest['unique_customers']):,}")
c4.metric("Average order", f"€{latest['average_order_value']:,.2f}")

left, right = st.columns(2)
with left:
    st.plotly_chart(px.line(daily, x="order_date", y="net_revenue", markers=True, title="Daily net revenue"), use_container_width=True)
with right:
    st.plotly_chart(px.bar(category, x="category", y="net_revenue", title="Revenue by category"), use_container_width=True)

st.subheader("Daily warehouse mart")
st.dataframe(daily.sort_values("order_date", ascending=False), use_container_width=True, hide_index=True)

