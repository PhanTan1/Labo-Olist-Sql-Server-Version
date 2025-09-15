CREATE VIEW vw_dim_product AS
SELECT
    product_id,
    product_category_name,
    product_name_length,
    product_description_length,
    product_photos_qty,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm
FROM products;
GO
CREATE VIEW vw_dim_customer AS
SELECT
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
FROM customers;
GO
CREATE VIEW vw_dim_seller AS
SELECT
    seller_id,
    seller_zip_code_prefix,
    seller_city,
    seller_state
FROM sellers;
GO
CREATE VIEW vw_dim_payment AS
SELECT
    ROW_NUMBER() OVER (ORDER BY payment_type) AS payment_type_id,
    payment_type
FROM (
    SELECT DISTINCT payment_type FROM order_payments
) AS distinct_payments;
GO
CREATE VIEW vw_dim_order_status AS
SELECT
    ROW_NUMBER() OVER (ORDER BY order_status) AS order_status_id,
    order_status
FROM (
    SELECT DISTINCT order_status FROM orders
) AS distinct_status;
GO
CREATE VIEW vw_dim_geolocation AS
SELECT
    geolocation_zip_code_prefix,
    geolocation_lat,
    geolocation_lng
FROM zip_code_reference;
GO
