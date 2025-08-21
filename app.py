import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "E-Commerce Dashboard"


def load_data():
    np.random.seed(1)   
    dates = pd.date_range(end=datetime.now(), periods=30)

    sales = pd.DataFrame({
        "date": dates,
        "revenue": np.random.normal(50000, 10000, 30),
        "orders": np.random.normal(200, 50, 30),
        "visitors": np.random.normal(5000, 1000, 30)
    })

    products = pd.DataFrame({
        "product": ["Electronics", "Clothing", "Home", "Sports", "Books", "Toys"],
        "sales": np.random.randint(1000, 10000, 6),
        "profit": np.random.randint(100, 1000, 6),
        "rating": np.random.uniform(3.5, 5.0, 6)
    })

    customers = pd.DataFrame({
        "segment": ["New", "Returning", "VIP", "Inactive"],
        "count": np.random.randint(100, 1000, 4),
        "avg_order_value": np.random.randint(50, 500, 4)
    })

    orders = pd.DataFrame({
        "status": ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"],
        "count": np.random.randint(50, 500, 5)
    })

    return sales, products, customers, orders


sales_df, product_df, customer_df, order_df = load_data()


total_revenue = sales_df["revenue"].sum()
total_orders = sales_df["orders"].sum()
total_visitors = sales_df["visitors"].sum()
conversion_rate = (total_orders / total_visitors) * 100


def kpi(title, value, color="primary"):
    return dbc.Card(
        dbc.CardBody([
            html.H6(title, className="text-muted"),
            html.H3(f"{value:,.0f}", className=f"text-{color}")
        ]), className="mb-3"
    )


def revenue_chart():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sales_df["date"], y=sales_df["revenue"], mode="lines+markers"))
    fig.update_layout(title="Revenue (Last 30 Days)", template="plotly_white", height=350)
    return fig

def product_chart():
    return px.bar(product_df, x="product", y="sales", title="Product Sales", height=350)

def customer_chart():
    return px.pie(customer_df, values="count", names="segment", title="Customer Segments", height=350)

def order_chart():
    return px.bar(order_df, x="status", y="count", title="Order Status", height=350)

app.layout = dbc.Container([
    html.H2("E-Commerce Dashboard", className="text-center my-4"),

    dbc.Row([
        dbc.Col(kpi("Revenue", total_revenue, "success"), md=3),
        dbc.Col(kpi("Orders", total_orders, "info"), md=3),
        dbc.Col(kpi("Visitors", total_visitors, "warning"), md=3),
        dbc.Col(kpi("Conversion %", conversion_rate, "danger"), md=3),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=revenue_chart()), md=8),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Progress", className="mb-3"),
            dbc.Progress(value=70, className="mb-2", color="success"),
            dbc.Progress(value=50, className="mb-2", color="info"),
            dbc.Progress(value=90, className="mb-2", color="warning"),
        ])), md=4),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=product_chart()), md=6),
        dbc.Col(dcc.Graph(figure=customer_chart()), md=6),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=order_chart()), md=12),
    ]),

    html.Footer("© 2024 Demo Dashboard", className="text-center text-muted mt-4")
], fluid=True)


if __name__ == "__main__":
    app.run_server(debug=True, host="127.0.0.1", port=8050)
