DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    tagline TEXT NOT NULL,
    price INTEGER NOT NULL,
    description TEXT NOT NULL,
    feature1 TEXT NOT NULL,
    feature2 TEXT NOT NULL,
    feature3 TEXT NOT NULL,
    image TEXT NOT NULL,
    hero_bg TEXT NOT NULL,
    accent TEXT NOT NULL,
    sort_order INTEGER NOT NULL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    postal_code TEXT NOT NULL,
    delivery_method TEXT NOT NULL,
    payment_method TEXT NOT NULL,
    promo_code TEXT,
    subtotal INTEGER NOT NULL,
    delivery_fee INTEGER NOT NULL,
    total INTEGER NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    qty INTEGER NOT NULL,
    price INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);
