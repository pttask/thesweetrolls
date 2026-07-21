"""
The Sweet Rolls - Flask e-commerce POV (user-facing) application.
Tugas 11 Praktikum Sistem Multimedia.
"""
import os
import sqlite3
from datetime import datetime

from flask import Flask, g, render_template, request, redirect, url_for, session, flash, jsonify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "sweetrolls.db")
DELIVERY_FEE = 10000

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "sweetrolls-dev-secret-key-change-in-production")

if not os.path.exists(DATABASE):
    from seed import seed_database
    seed_database(DATABASE)
    
# ---------- Database helpers ----------

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_all_products():
    return query_db("SELECT * FROM products ORDER BY sort_order")


def get_product_by_slug(slug):
    return query_db("SELECT * FROM products WHERE slug = ?", (slug,), one=True)


def get_product_by_id(pid):
    return query_db("SELECT * FROM products WHERE id = ?", (pid,), one=True)


# ---------- Cart helpers (session based) ----------

def get_cart():
    return session.setdefault("cart", {})  # {product_id_str: qty}


def cart_details():
    cart = get_cart()
    items = []
    subtotal = 0
    for pid_str, qty in cart.items():
        product = get_product_by_id(int(pid_str))
        if not product:
            continue
        line_total = product["price"] * qty
        subtotal += line_total
        items.append({"product": product, "qty": qty, "line_total": line_total})
    return items, subtotal


def cart_count():
    return sum(get_cart().values())


@app.context_processor
def inject_cart_count():
    return {"cart_count": cart_count()}


# ---------- Routes: main pages ----------

@app.route("/")
def home():
    products = get_all_products()
    return render_template("home.html", products=products, active_page="home")


@app.route("/about")
def about():
    return render_template("about.html", active_page="about")


@app.route("/product")
def product_list():
    products = get_all_products()
    return render_template("product.html", products=products, active_page="product")


@app.route("/product/<slug>")
def product_detail(slug):
    product = get_product_by_slug(slug)
    if not product:
        flash("Produk tidak ditemukan.", "danger")
        return redirect(url_for("product_list"))
    other_products = [p for p in get_all_products() if p["slug"] != slug]
    return render_template(
        "product_detail.html", product=product, active_page="product"
    )


@app.route("/contact")
def contact():
    return render_template("contact.html", active_page="contact")


# ---------- Routes: cart ----------

@app.route("/cart/add", methods=["POST"])
def cart_add():
    product_id = request.form.get("product_id")
    qty = int(request.form.get("qty", 1))
    if not product_id or not get_product_by_id(int(product_id)):
        flash("Produk tidak valid.", "danger")
        return redirect(request.referrer or url_for("product_list"))

    cart = get_cart()
    cart[product_id] = cart.get(product_id, 0) + max(qty, 1)
    session["cart"] = cart
    session.modified = True
    flash("Produk ditambahkan ke keranjang.", "success")
    return redirect(url_for("checkout"))


@app.route("/cart/update", methods=["POST"])
def cart_update():
    product_id = request.form.get("product_id")
    action = request.form.get("action")
    cart = get_cart()

    if product_id in cart:
        if action == "increase":
            cart[product_id] += 1
        elif action == "decrease":
            cart[product_id] -= 1
            if cart[product_id] <= 0:
                del cart[product_id]
        elif action == "remove":
            del cart[product_id]

    session["cart"] = cart
    session.modified = True

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        items, subtotal = cart_details()
        delivery_fee = DELIVERY_FEE if items else 0
        return jsonify({
            "subtotal": subtotal,
            "delivery_fee": delivery_fee,
            "total": subtotal + delivery_fee,
            "cart_count": cart_count(),
            "items": [
                {"product_id": it["product"]["id"], "qty": it["qty"], "line_total": it["line_total"]}
                for it in items
            ],
        })
    return redirect(url_for("checkout"))


# ---------- Routes: checkout ----------

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, subtotal = cart_details()
    delivery_fee = DELIVERY_FEE if items else 0
    errors = {}
    form_data = {}

    if request.method == "POST":
        form_data = {
            "full_name": request.form.get("full_name", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "address": request.form.get("address", "").strip(),
            "city": request.form.get("city", "").strip(),
            "postal_code": request.form.get("postal_code", "").strip(),
            "delivery_method": request.form.get("delivery_method", "delivery"),
            "payment_method": request.form.get("payment_method", "bank_transfer"),
        }

        if not items:
            errors["cart"] = "Keranjang belanja Anda kosong."
        if not form_data["full_name"]:
            errors["full_name"] = "Nama lengkap wajib diisi."
        if not form_data["phone"] or not form_data["phone"].replace("+", "").isdigit():
            errors["phone"] = "Nomor telepon wajib diisi dengan format angka yang valid."
        if not form_data["address"]:
            errors["address"] = "Alamat lengkap wajib diisi."
        if not form_data["city"]:
            errors["city"] = "Kota / Kecamatan wajib dipilih."
        if not form_data["postal_code"] or not form_data["postal_code"].isdigit() or len(form_data["postal_code"]) < 5:
            errors["postal_code"] = "Kode pos wajib diisi (minimal 5 digit angka)."

        actual_delivery_fee = DELIVERY_FEE if form_data["delivery_method"] == "delivery" else 0

        if not errors:
            db = get_db()
            cur = db.execute(
                """
                INSERT INTO orders
                    (full_name, phone, address, city, postal_code, delivery_method,
                     payment_method, promo_code, subtotal, delivery_fee, total, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    form_data["full_name"], form_data["phone"], form_data["address"],
                    form_data["city"], form_data["postal_code"], form_data["delivery_method"],
                    form_data["payment_method"], request.form.get("promo_code", ""),
                    subtotal, actual_delivery_fee, subtotal + actual_delivery_fee,
                    datetime.now().isoformat(timespec="seconds"),
                ),
            )
            order_id = cur.lastrowid
            for it in items:
                db.execute(
                    """
                    INSERT INTO order_items (order_id, product_id, product_name, qty, price)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (order_id, it["product"]["id"], it["product"]["name"], it["qty"], it["product"]["price"]),
                )
            db.commit()
            session["cart"] = {}
            session.modified = True
            return redirect(url_for("order_success", order_id=order_id))

    return render_template(
        "checkout.html",
        items=items,
        subtotal=subtotal,
        delivery_fee=delivery_fee,
        total=subtotal + delivery_fee,
        errors=errors,
        form_data=form_data,
        active_page="checkout",
    )


@app.route("/order/success/<int:order_id>")
def order_success(order_id):
    order = query_db("SELECT * FROM orders WHERE id = ?", (order_id,), one=True)
    if not order:
        return redirect(url_for("home"))
    order_items = query_db("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
    return render_template("order_success.html", order=order, order_items=order_items, active_page="checkout")


if __name__ == "__main__":
    app.run(debug=True)
