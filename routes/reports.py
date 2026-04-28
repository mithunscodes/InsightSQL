from flask import Blueprint, render_template, jsonify
from models.sales     import get_monthly_revenue, get_revenue_by_category
from models.products  import get_all_products, get_sales_summary
from models.customers import get_revenue_by_city

bp = Blueprint("reports", __name__)

@bp.route("/reports")
def reports():
    data = {
        "monthly_revenue":  get_monthly_revenue(),
        "category_revenue": get_revenue_by_category(),
        "products":         get_all_products(),
        "city_revenue":     get_revenue_by_city(),
        "sales_summary":    get_sales_summary(),
    }
    return render_template("reports.html", **data)

@bp.route("/api/city-revenue")
def api_city_revenue():
    return jsonify(get_revenue_by_city())

@bp.route("/api/sales-summary")
def api_sales_summary():
    return jsonify(get_sales_summary())
