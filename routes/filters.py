from flask import Blueprint, render_template, request, jsonify
from models.customers import get_all_customers, get_customer_detail
from models.products  import get_all_products
from db import get_db

bp = Blueprint("filters", __name__)

@bp.route("/customers")
def customers():
    city   = request.args.get("city", "")
    search = request.args.get("q", "")
    all_customers = get_all_customers()

    if city:
        all_customers = [c for c in all_customers if c["city"] == city]
    if search:
        all_customers = [c for c in all_customers if search.lower() in c["name"].lower()]

    cities = sorted({c["city"] for c in get_all_customers()})
    return render_template("details.html", customers=all_customers, cities=cities,
                           selected_city=city, search=search, view="customers")

@bp.route("/customers/<int:customer_id>")
def customer_detail(customer_id):
    rows = get_customer_detail(customer_id)
    return render_template("details.html", rows=rows, view="customer_detail",
                           customer_id=customer_id)

@bp.route("/products")
def products():
    category = request.args.get("category", "")
    all_products = get_all_products()

    if category:
        all_products = [p for p in all_products if p["category"] == category]

    categories = sorted({p["category"] for p in get_all_products()})
    return render_template("details.html", products=all_products, categories=categories,
                           selected_category=category, view="products")

@bp.route("/api/search-customers")
def search_customers():
    q = request.args.get("q", "")
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT customer_id, name, city, email
        FROM customers
        WHERE name LIKE %s OR city LIKE %s
        LIMIT 20
    """, (f"%{q}%", f"%{q}%"))
    return jsonify(cursor.fetchall())
