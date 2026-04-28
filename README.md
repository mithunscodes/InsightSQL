# InsightSQL — Sales Analytics Dashboard

A full-stack sales analytics dashboard built with **Python, Flask, and MySQL**. Designed to showcase relational database design, complex SQL querying, and live data visualisation.

## Live Demo
> Deployed on Render · Database hosted on Railway

## Features

- **Multi-table JOINs** — revenue, customer, and product queries across 4 normalised tables
- **Aggregations** — monthly revenue trends, category breakdowns, top performers
- **MySQL VIEW** — `sales_summary` used across reports
- **Stored Procedures** — parameterised top-N product queries
- **Indexes** — optimised lookups on `order_date`, `customer_id`, `product_id`
- **Live SQL Log** — every query that fires on a page request is shown with execution time
- **Interactive Charts** — Chart.js powered revenue trend and category breakdown
- **Filtering & Drill-down** — filter customers by city, products by category, click through to individual customer history

## Tech Stack

| Layer     | Technology                  |
|-----------|-----------------------------|
| Backend   | Python, Flask               |
| Database  | MySQL (Railway)             |
| Frontend  | HTML, CSS, Chart.js         |
| Deploy    | Render (app), Railway (DB)  |

## Schema

```
customers ──< orders ──< order_items >── products
```

4 tables · 1 view · 3 indexes · 3 stored procedures · 60 seed records

## Local Setup

```bash
git clone https://github.com/YOUR_USERNAME/InsightSQL.git
cd InsightSQL
pip install -r requirements.txt
cp .env.example .env   # fill in your DB credentials
py app.py
```

## Project Structure

```
├── app.py                  # Flask entry point
├── db.py                   # DB connection + query logger
├── config.py               # Environment config
├── models/                 # SQL query functions
│   ├── sales.py
│   ├── products.py
│   └── customers.py
├── routes/                 # Flask blueprints
│   ├── dashboard.py
│   ├── reports.py
│   └── filters.py
├── templates/              # Jinja2 HTML templates
├── static/                 # CSS + Chart.js
└── database/
    ├── schema.sql          # Tables, indexes, view
    ├── seed.sql            # Sample data
    ├── queries.sql         # Reference queries
    └── procedures.sql      # Stored procedures
```
