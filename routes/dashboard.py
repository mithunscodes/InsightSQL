from flask import Blueprint, render_template, jsonify
from models.sales    import get_monthly_revenue, get_revenue_by_category, get_total_revenue, get_total_orders, get_recent_orders
from models.products import get_top_products, get_low_stock
from models.customers import get_top_customers

bp = Blueprint("dashboard", __name__)

@bp.route("/")
def index():
    stats = {
        "total_revenue": get_total_revenue(),
        "total_orders":  get_total_orders(),
        "top_products":  get_top_products(5),
        "top_customers": get_top_customers(5),
        "recent_orders": get_recent_orders(8),
        "low_stock":     get_low_stock(50),
    }
    return render_template("index.html", **stats)

@bp.route("/api/monthly-revenue")
def api_monthly_revenue():
    return jsonify(get_monthly_revenue())

@bp.route("/api/category-revenue")
def api_category_revenue():
    return jsonify(get_revenue_by_category())

@bp.route("/api/top-products")
def api_top_products():
    return jsonify(get_top_products(10))
