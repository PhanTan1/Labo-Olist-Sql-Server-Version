CREATE TABLE FactOrder (
    order_id NVARCHAR(50),
    order_item_id INT,
    customer_id NVARCHAR(50),
    product_id NVARCHAR(50),
    seller_id NVARCHAR(50),
    order_status NVARCHAR(50),
    order_purchase_timestamp DATETIME,
    order_delivered_customer_date DATETIME,
    order_estimated_delivery_date DATETIME,
    delivery_delay_days INT, -- à calculer dans SSIS ou via une vue
    is_delivered_late BIT,   -- idem
    price DECIMAL(10,2),
    freight_value DECIMAL(10,2),
    product_category_name NVARCHAR(100),
    product_name_length INT,
    product_description_length INT,
    product_photos_qty INT,
    payment_type NVARCHAR(50),
    payment_installments INT,
    payment_value DECIMAL(10,2)
);