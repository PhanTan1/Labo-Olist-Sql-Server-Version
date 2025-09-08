# Customers
customers_table_sql = """
DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    customer_id UNIQUEIDENTIFIER,
    customer_unique_id UNIQUEIDENTIFIER NOT NULL,
    customer_zip_code_prefix VARCHAR(5) NOT NULL,
    customer_city VARCHAR(32),
    customer_state VARCHAR(2),

    CONSTRAINT PK__customers PRIMARY KEY (customer_id),
    CONSTRAINT customer_zip_code_prefix_valid CHECK (customer_zip_code_prefix LIKE '[0-9][0-9][0-9][0-9]%'),
    CONSTRAINT customer_state_format CHECK (customer_state LIKE '[A-Z][A-Z]')
);
"""
#Geolocation
geolocation_table_sql = """
DROP TABLE IF EXISTS geolocation;
CREATE TABLE geolocation (
    geolocation_zip_code_prefix VARCHAR(5),
    geolocation_lat NUMERIC(15,10),
    geolocation_lng NUMERIC(15,10),
    geolocation_city VARCHAR(38),
    geolocation_state VARCHAR(2),

    CONSTRAINT geolocation_zip_code_prefix_valid CHECK (geolocation_zip_code_prefix LIKE '[0-9][0-9][0-9][0-9]%'),
    CONSTRAINT geolocation_state_format CHECK (geolocation_state LIKE '[A-Z][A-Z]')
);
"""
#Orders
orders_table_sql = """
DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    order_id UNIQUEIDENTIFIER,
    customer_id UNIQUEIDENTIFIER NOT NULL,
    order_status VARCHAR(11) NOT NULL,
    order_purchase_timestamp DATETIME NOT NULL,
    order_approved_at DATETIME,
    order_delivered_carrier_date DATETIME,
    order_delivered_customer_date DATETIME,
    order_estimated_delivery_date DATETIME NOT NULL,

    CONSTRAINT PK__orders PRIMARY KEY (order_id),
    CONSTRAINT FK__orders FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
"""
#OrderItems
orderItems_table_sql ="""
DROP TABLE IF EXISTS order_items;
CREATE TABLE order_items (
    order_id UNIQUEIDENTIFIER,
    order_item_id SMALLINT NOT NULL,
    product_id UNIQUEIDENTIFIER NOT NULL,
    seller_id UNIQUEIDENTIFIER NOT NULL,
    shipping_limit_date DATETIME NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    freight_value DECIMAL(8,2) NOT NULL,

    CONSTRAINT PK__order_items PRIMARY KEY (order_item_id, order_id),
    CONSTRAINT FK__order_items_order FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT FK__order_items_product FOREIGN KEY (product_id) REFERENCES products(product_id),
    CONSTRAINT FK__order_items_seller FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);
    """
#OrderPayments
orderPayments_table_sql = """
DROP TABLE IF EXISTS order_payments;
CREATE TABLE order_payments (
    order_id UNIQUEIDENTIFIER NOT NULL,
    payment_sequential SMALLINT NOT NULL,
    payment_type VARCHAR(11) NOT NULL,
    payment_installments INT NOT NULL,
    payment_value DECIMAL(8,2) NOT NULL,

    CONSTRAINT PK__order_payments PRIMARY KEY (order_id, payment_sequential),
    CONSTRAINT FK__order_payments FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
    """
#OrderReviews
orderReviews_table_sql = """
DROP TABLE IF EXISTS order_reviews;
CREATE TABLE order_reviews (
    review_id UNIQUEIDENTIFIER,
    order_id UNIQUEIDENTIFIER NOT NULL,
    review_score INT NOT NULL,
    review_comment_title VARCHAR(50),
    review_comment_message VARCHAR(255),
    review_creation_date DATETIME NOT NULL,
    review_answer_timestamp DATETIME NOT NULL,

    CONSTRAINT PK__order_reviews PRIMARY KEY (review_id),
    CONSTRAINT FK__order_reviews FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT review_score CHECK (review_score BETWEEN 1 AND 5)
);
    """
#Products
products_table_sql = """
DROP TABLE IF EXISTS products;
CREATE TABLE products (
    product_id UNIQUEIDENTIFIER,
    product_category_name VARCHAR(60),
    product_name_length VARCHAR(11),
    product_description_length SMALLINT,
    product_photos_qty SMALLINT,
    product_weight_g INT,
    product_length_cm SMALLINT,
    product_height_cm SMALLINT,
    product_width_cm SMALLINT,

    CONSTRAINT PK__products PRIMARY KEY (product_id),
    CONSTRAINT FK__products FOREIGN KEY (product_category_name) REFERENCES product_category_name_translation(product_category_name)
);
    """
#Sellers
sellers_table_sql = """
DROP TABLE IF EXISTS sellers;
CREATE TABLE sellers (
    seller_id UNIQUEIDENTIFIER,
    seller_zip_code_prefix VARCHAR(5) NOT NULL,
    seller_city VARCHAR(45) NOT NULL,
    seller_state VARCHAR(2) NOT NULL,

    CONSTRAINT PK__sellers PRIMARY KEY (seller_id),
    CONSTRAINT seller_zip_code_prefix_valid CHECK (seller_zip_code_prefix LIKE '[0-9][0-9][0-9][0-9]%'),
    CONSTRAINT seller_state_format CHECK (seller_state LIKE '[A-Z][A-Z]')
);
    """
#Product Category Name Translation
product_category_name_translation_table_sql = """
DROP TABLE IF EXISTS product_category_name_translation;
CREATE TABLE product_category_name_translation (
    product_category_name VARCHAR(60) NOT NULL,
    product_category_name_english VARCHAR(60) NOT NULL,

    CONSTRAINT PK__product_category_name_translation PRIMARY KEY (product_category_name)
);
  """


TABLES = {
    'product_category_name_translation': product_category_name_translation_table_sql,
    'customers': customers_table_sql,
    'orders': orders_table_sql,
    'products': products_table_sql,
    'sellers': sellers_table_sql,
    'order_items': orderItems_table_sql,
    'order_payments': orderPayments_table_sql,
    'order_reviews': orderReviews_table_sql,
    'geolocation': geolocation_table_sql
}