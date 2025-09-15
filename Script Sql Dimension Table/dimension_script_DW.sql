DROP TABLE IF EXISTS dim_customers;
CREATE TABLE dim_customers (
    customer_id UNIQUEIDENTIFIER,
    customer_unique_id UNIQUEIDENTIFIER NOT NULL,
    customer_zip_code_prefix NVARCHAR(5) NOT NULL,
    customer_city NVARCHAR(32),
    customer_state NVARCHAR(2),

    CONSTRAINT PK__dim_customers PRIMARY KEY (customer_id),
    CONSTRAINT CHK_customer_zip_code_prefix_valid CHECK (customer_zip_code_prefix LIKE '[0-9][0-9][0-9][0-9]%'),
    CONSTRAINT CHK_customer_state_format CHECK (customer_state LIKE '[A-Z][A-Z]')
);


DROP TABLE IF EXISTS dim_sellers;
CREATE TABLE dim_sellers (
    seller_id UNIQUEIDENTIFIER,
    seller_zip_code_prefix NVARCHAR(5) NOT NULL,
    seller_city NVARCHAR(45) NOT NULL,
    seller_state NVARCHAR(2) NOT NULL,

    CONSTRAINT PK__dim_sellers PRIMARY KEY (seller_id),
    CONSTRAINT seller_zip_code_prefix_valid CHECK (seller_zip_code_prefix LIKE '[0-9][0-9][0-9][0-9]%'),
    CONSTRAINT seller_state_format CHECK (seller_state LIKE '[A-Z][A-Z]')
);

DROP TABLE IF EXISTS dim_products;
CREATE TABLE dim_products (
    product_id UNIQUEIDENTIFIER,
    product_category_name NVARCHAR(60),
    product_name_length SMALLINT,
    product_description_length SMALLINT,
    product_photos_qty SMALLINT,
    product_weight_g INT,
    product_length_cm SMALLINT,
    product_height_cm SMALLINT,
    product_width_cm SMALLINT,

    CONSTRAINT PK__dim_products PRIMARY KEY (product_id)
    );

DROP TABLE IF EXISTS dim_order_status;
CREATE TABLE dim_order_status (
    order_status_id INT PRIMARY KEY,
    order_status NVARCHAR(11) NOT NULL
);

DROP TABLE IF EXISTS dim_geolocation;
CREATE TABLE dim_geolocation (
    geolocation_zip_code_prefix NVARCHAR(5) NOT NULL,
    geolocation_lat NUMERIC(15,10),
    geolocation_lng NUMERIC(15,10),

    CONSTRAINT PK__dim_geolocation PRIMARY KEY (geolocation_zip_code_prefix),
    CONSTRAINT dim_geolocation_zip_code_prefix_valid CHECK (geolocation_zip_code_prefix LIKE '[0-9][0-9][0-9][0-9]%')
);


DROP TABLE IF EXISTS dim_payment_type;
CREATE TABLE dim_payment_type (
    payment_type_id INT PRIMARY KEY,
    payment_type NVARCHAR(20) NOT NULL,

    CONSTRAINT CHK_payment_type_format CHECK (payment_type NOT LIKE '%[^a-zA-Z_]%')
);


DROP TABLE IF EXISTS dim_review_score;
CREATE TABLE dim_review_score (
    review_score INT PRIMARY KEY,
    review_label NVARCHAR(20) NOT NULL,
    is_positive BIT NOT NULL,
    is_neutral BIT NOT NULL,
    is_negative BIT NOT NULL,

    CONSTRAINT CHK_review_score_range CHECK (review_score BETWEEN 1 AND 5)
);

