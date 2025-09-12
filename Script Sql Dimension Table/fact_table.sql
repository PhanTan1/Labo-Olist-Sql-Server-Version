DROP TABLE IF EXISTS FactOrder;
CREATE TABLE FactOrder (
    order_id UNIQUEIDENTIFIER NOT NULL,
    order_item_id SMALLINT NOT NULL,
    customer_id UNIQUEIDENTIFIER NOT NULL,
    product_id UNIQUEIDENTIFIER NOT NULL,
    seller_id UNIQUEIDENTIFIER NOT NULL,

    order_status NVARCHAR(11) NOT NULL,
    order_purchase_timestamp DATETIME NOT NULL,
    order_delivered_customer_date DATETIME,
    order_estimated_delivery_date DATETIME NOT NULL,

    price DECIMAL(8,2) NOT NULL,
    freight_value DECIMAL(8,2) NOT NULL,

    product_category_name NVARCHAR(60),
    product_name_length NVARCHAR(11),
    product_description_length SMALLINT,
    product_photos_qty SMALLINT,

    payment_type NVARCHAR(11),
    payment_installments INT,
    payment_value DECIMAL(8,2),
);
