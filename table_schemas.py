customers_table_sql = """
DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    customer_id UUID,
    customer_unique_id UUID NOT NULL,
    customer_zip_code_prefix VARCHAR(5) NOT NULL,
    customer_city VARCHAR(32),
    customer_state VARCHAR(2),

    CONSTRAINT PK__customers PRIMARY KEY (customer_id),
    CONSTRAINT customer_zip_code_prefix_valid CHECK (customer_zip_code_prefix ~ '^\d{4,5}$'),
    CONSTRAINT customer_state_format CHECK (customer_state ~ '^[A-Z]{2}$')
);
"""

geolocation_table_sql = """
DROP TABLE IF EXISTS geolocation;
    CREATE TABLE geolocation (
        geolocation_zip_code_prefix VARCHAR(5),
        geolocation_lat NUMERIC(15,10),
        geolocation_lng NUMERIC(15,10),
        geolocation_city VARCHAR(38),
        geolocation_state VARCHAR(2),
        CONSTRAINT geolocation_zip_code_prefix_valid CHECK (geolocation_zip_code_prefix ~ '^\d{4,5}$'),
        CONSTRAINT geolocation_state_format CHECK (geolocation_state ~ '^[A-Z]{2}$')
    );
"""
orderItems_table_sql ="""
DROP TABLE IF EXISTS orderItems;
CREATE TABLE orderItems (
    order_id UUID,
    order_item_id INT NOT NULL,
    product_id UUID NOT NULL,
    seller_id UUID NOT NULL,
    shipping_limit_date TIMESTAMP NOT NULL,
    price DECIMAL (8,2) NOT NULL,
    freight_value DECIMAL(8,2) NOT NULL,

    CONSTRAINT PK__orderItems PRIMARY KEY (order_id)
);
    """
orderPayments_table_sql = """
    DROP TABLE IF EXISTS orderPayments;

    CREATE TABLE orderPayments (
            order_id UUID,
    payment_sequential INT NOT NULL,
    payment_type VARCHAR(11) NOT NULL,
    payment_installments INT NOT NULL,
    payment_value DECIMAL(8,2) NOT NULL,

    CONSTRAINT PK__orderPayments PRIMARY KEY (order_id)
);
    """
orderReviews_table_sql = """
    DROP TABLE IF EXISTS orderReviews;

    CREATE TABLE orderReviews (
        review_id UUID,
        order_id UUID NOT NULL,
        review_score INT NOT NULL,
        review_comment_title VARCHAR (50),
        review_comment_message VARCHAR (255),
        review_creation_date TIMESTAMP NOT NULL,
        review_answer_timestamp TIMESTAMP NOT NULL,

    CONSTRAINT PK__orderReviews PRIMARY KEY (review_id),
    CONSTRAINT review_score CHECK (review_score BETWEEN 1 AND 5)
);
"""

# Add other table schemas here...
TABLES = {
    'customers': customers_table_sql,
    'geolocation': geolocation_table_sql,
    'order_items': orderItems_table_sql,
    'order_payments': orderPayments_table_sql,
    'order_reviews': orderReviews_table_sql
    # Add other tables here...
}