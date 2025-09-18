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
CREATE VIEW vw_fact_order AS
SELECT 
    o.order_id,
    CAST(oi.order_item_id AS SMALLINT) AS order_item_id,
    o.customer_id,
    oi.product_id,
    oi.seller_id,

    -- Encodage du statut
    CAST(
        CASE 
            WHEN o.order_status = 'delivered' THEN 1
            WHEN o.order_status = 'shipped' THEN 2
            WHEN o.order_status = 'processing' THEN 3
            WHEN o.order_status = 'canceled' THEN 4
            WHEN o.order_status = 'approved' THEN 5
            WHEN o.order_status = 'invoiced' THEN 6
            WHEN o.order_status = 'created' THEN 7
            WHEN o.order_status = 'unavailable' THEN 8
            ELSE 0
        END
    AS INT) AS order_status_id,

    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,

    -- DateKey et TimeKey
    CAST(CONVERT(VARCHAR(8), o.order_purchase_timestamp, 112) AS INT) AS datekey,
    CAST(DATEPART(HOUR, o.order_purchase_timestamp) * 10000 +
         DATEPART(MINUTE, o.order_purchase_timestamp) * 100 +
         DATEPART(SECOND, o.order_purchase_timestamp) AS INT) AS timekey,

    CAST(oi.price AS DECIMAL(10,2)) AS price,
    CAST(oi.freight_value AS DECIMAL(10,2)) AS freight_value,

    p.product_category_name,
    p.product_name_length,
    p.product_description_length,
    p.product_photos_qty

FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;
GO

CREATE VIEW vw_fact_order_payments AS
SELECT 
    op.order_id,
    op.payment_sequential,
    op.payment_type,
    op.payment_installments,
    op.payment_value,
    CAST(FORMAT(o.order_purchase_timestamp, 'yyyyMMdd') AS INT) AS datekey
FROM order_payments op
JOIN orders o ON op.order_id = o.order_id;
GO

CREATE VIEW vw_fact_review AS
SELECT 
    r.review_id,
    r.order_id,
    r.review_score,
    r.review_comment_title,
    r.review_comment_message,
    r.review_creation_date,
    r.review_answer_timestamp,
    CAST(FORMAT(r.review_creation_date, 'yyyyMMdd') AS INT) AS datekey
FROM order_reviews r;
