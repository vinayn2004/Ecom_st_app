import streamlit as st
import pandas as pd
import plotly.express as px

# ──────────────────────────────────────────────────────────────
# 🔧 Page Config & Sidebar
# ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Customer Satisfaction Case Study", layout="wide")

st.sidebar.title("Navigation")
PAGES = [
    "Welcome",
    "Understanding the Problem",
    "Factors and Causes",
    "Conclusion and Insights",
]
page = st.sidebar.radio("Select Page:", PAGES)

st.sidebar.title("Upload Dataset")
file = st.sidebar.file_uploader("Upload your CSV", type=["csv"], key="uploader")

# ──────────────────────────────────────────────────────────────
# 📦 Read & Feature‑Engineer (inline)
# ──────────────────────────────────────────────────────────────
if file:
    df = pd.read_csv(
        file,
        parse_dates=[
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    )

    df["delivery_delay"] = (df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]).dt.days
    df["processing_time"] = (df["order_approved_at"] - df["order_purchase_timestamp"]).dt.days

    df["delay_category"] = df["delivery_delay"].apply(
    lambda d: "On-time" if d <= 0 else ("Slightly Late" if d <= 7 else "Very Late")
)

    df["review_category"] = df["review_score"].apply(
    lambda s: "Bad" if s <= 2 else ("Neutral" if s == 3 else "Good")
)
else:
    df = None

# ──────────────────────────────────────────────────────────────
# 1️⃣  Welcome (always visible)
# ──────────────────────────────────────────────────────────────
if page == "Welcome":
    st.title("🚀 Customer Satisfaction Case Study")
    st.markdown(
        """
### Why this app?
Late deliveries or slow processing can turn 5‑star fans into refund requests 🥲.
Upload your logistics CSV and explore *where* things break and *how* to fix them.

— **Sections** —
*Understanding the Problem* → KPI vs review deep‑dives.
*Factors and Causes*        → Worst sellers, cities, products.
*Conclusion & Insights*     → Key takeaways.

- Data to Upload for Analysis → [link](https://drive.google.com/file/d/1h02g6ObGWiTID990u2pWTw5o3aNEYzSb/view?usp=sharing)

        """
    )

# ──────────────────────────────────────────────────────────────
# 2️⃣  Understanding the Problem
# ──────────────────────────────────────────────────────────────
if page == "Understanding the Problem":
    st.title("Understanding the Problem")

    if df is None:
        st.warning("➡️  Please upload a dataset to view this analysis.")
        st.stop()

    st.markdown("""Focus KPIs: **Delivery Delay**, **Processing Time**, **Freight Value** vs Review Score.""")

    # Delivery Delay vs Review
    fig_delay = px.box(df, x="review_category", y="delivery_delay", template="plotly_white")
    fig_delay.update_traces(marker_color="#1f77b4", quartilemethod="inclusive")
    fig_delay.update_layout(title="Delivery Delay by Review Category", xaxis_title="Review Category", yaxis_title="Delay (days)")
    st.plotly_chart(fig_delay, use_container_width=True)

    # Processing Time vs Review
    fig_proc = px.box(df, x="review_category", y="processing_time", template="plotly_white")
    fig_proc.update_traces(marker_color="#ff7f0e", quartilemethod="inclusive")
    fig_proc.update_layout(title="Processing Time by Review Category", xaxis_title="Review Category", yaxis_title="Processing Time (days)")
    st.plotly_chart(fig_proc, use_container_width=True)

    # Freight Value vs Review
    fig_freight = px.box(df, x="review_category", y="freight_value", template="plotly_white")
    fig_freight.update_traces(marker_color="#2ca02c", quartilemethod="inclusive")
    fig_freight.update_layout(title="Freight Value by Review Category", xaxis_title="Review Category", yaxis_title="Freight (BRL)")
    fig_freight.update_yaxes(tickprefix="R$ ")
    st.plotly_chart(fig_freight, use_container_width=True)

# ──────────────────────────────────────────────────────────────
# 3️⃣  Factors and Causes
# ──────────────────────────────────────────────────────────────
if page == "Factors and Causes":
    st.title("Factors and Causes")

    if df is None:
        st.warning("➡️  Please upload a dataset to view this analysis.")
        st.stop()

    st.markdown("Which sellers, cities, and products are most problematic?")

    # Top 10 sellers (wide to grouped bar — no melt)
    sellers = (
        df.groupby("seller_id")[["delivery_delay", "processing_time", "freight_value"]]
        .mean()
        .sort_values("delivery_delay", ascending=False)
        .head(10)
        .reset_index()
    )
    fig_sellers = px.bar(
        sellers,
        x="seller_id",
        y=["delivery_delay", "processing_time", "freight_value"],
        barmode="group",
        template="plotly_white",
        labels={"value": "Avg Value", "variable": "Metric"},
    )
    fig_sellers.update_traces(texttemplate="%{y:.1f}", textposition="outside")
    fig_sellers.update_layout(title="Top Sellers by Delay / Processing / Freight", xaxis_title="Seller ID", yaxis_title="Avg Value")
    st.plotly_chart(fig_sellers, use_container_width=True)

    # Top 10 cities
    cities = (
        df.groupby("customer_city")[["delivery_delay", "processing_time", "freight_value"]]
        .mean()
        .sort_values("delivery_delay", ascending=False)
        .head(10)
        .reset_index()
    )
    fig_cities = px.bar(
        cities,
        x="customer_city",
        y=["delivery_delay", "processing_time", "freight_value"],
        barmode="group",
        template="plotly_white",
        labels={"value": "Avg Value", "variable": "Metric"},
    )
    fig_cities.update_traces(texttemplate="%{y:.1f}", textposition="outside")
    fig_cities.update_layout(title="Top Cities by Delay / Processing / Freight", xaxis_title="City", yaxis_title="Avg Value")
    st.plotly_chart(fig_cities, use_container_width=True)

    # Top 10 products
    products = (
        df.groupby("product_id")[["delivery_delay", "processing_time", "freight_value"]]
        .mean()
        .sort_values("delivery_delay", ascending=False)
        .head(10)
        .reset_index()
    )
    fig_products = px.bar(
        products,
        x="product_id",
        y=["delivery_delay", "processing_time", "freight_value"],
        barmode="group",
        template="plotly_white",
        labels={"value": "Avg Value", "variable": "Metric"},
    )
    fig_products.update_traces(texttemplate="%{y:.1f}", textposition="outside")
    fig_products.update_layout(title="Top Products by Delay / Processing / Freight", xaxis_title="Product ID", yaxis_title="Avg Value")
    st.plotly_chart(fig_products, use_container_width=True)

# ──────────────────────────────────────────────────────────────
# 4️⃣  Conclusion & Insights
# ──────────────────────────────────────────────────────────────
if page == "Conclusion and Insights":
    st.title("Conclusion & Insights")
    st.markdown(
        """### Key Findings
* **Delivery delays** drive negative reviews.
* **Fast processing** correlates with positive feedback.
* **Freight cost** alone isn’t a deal‑breaker.

### Next Moves
1. Improve ETA accuracy with real‑time tracking.
2. Automate low‑risk order approvals.
3. Target worst sellers/cities/products first.
        """
    )
