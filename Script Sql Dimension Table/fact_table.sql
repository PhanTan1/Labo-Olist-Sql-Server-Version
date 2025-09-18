CREATE TABLE FactOrder (
    order_id UNIQUEIDENTIFIER NOT NULL,
    order_item_id SMALLINT NOT NULL,
    customer_id UNIQUEIDENTIFIER NOT NULL,
    product_id UNIQUEIDENTIFIER NOT NULL,
    seller_id UNIQUEIDENTIFIER NOT NULL,
    
    order_status_id INT NOT NULL, -- FK vers dim_order_status
    
    order_purchase_timestamp DATETIME NOT NULL,
    order_delivered_customer_date DATETIME NULL,
    order_estimated_delivery_date DATETIME NULL,

    datekey INT NOT NULL, -- FK vers DimDate
    timekey INT NOT NULL, -- FK vers DimTime

    price DECIMAL(10,2) NOT NULL,
    freight_value DECIMAL(10,2) NOT NULL,

    product_category_name NVARCHAR(100) NULL,
    product_name_length SMALLINT NULL,
    product_description_length SMALLINT NULL,
    product_photos_qty SMALLINT NULL,

    -- Clé primaire composite
    CONSTRAINT PK_FactOrder PRIMARY KEY (order_id, order_item_id),

    -- Clés étrangères (à adapter selon ton schéma)
    CONSTRAINT FK_FactOrder_Customer FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
    CONSTRAINT FK_FactOrder_Product FOREIGN KEY (product_id) REFERENCES dim_products(product_id),
    CONSTRAINT FK_FactOrder_Seller FOREIGN KEY (seller_id) REFERENCES dim_sellers(seller_id),
    CONSTRAINT FK_FactOrder_Status FOREIGN KEY (order_status_id) REFERENCES dim_order_status(order_status_id),
    CONSTRAINT FK_FactOrder_Date FOREIGN KEY (datekey) REFERENCES DimDate(datekey),
    CONSTRAINT FK_FactOrder_Time FOREIGN KEY (timekey) REFERENCES DimTime(timekey)
);


DROP TABLE IF EXISTS fact_order_payments;
CREATE TABLE fact_order_payments (
    order_id UNIQUEIDENTIFIER NOT NULL,
    payment_sequential SMALLINT NOT NULL,
    payment_type NVARCHAR(11) NOT NULL,
    payment_installments INT NOT NULL,
    payment_value DECIMAL(8,2) NOT NULL,
    datekey INT NOT NULL,

    CONSTRAINT PK_fact_order_payments PRIMARY KEY (order_id, payment_sequential),
    CONSTRAINT FK_fact_order_payments_date FOREIGN KEY (datekey) REFERENCES DimDate(DateKey)
);


DROP TABLE IF EXISTS fact_review;
CREATE TABLE fact_review (
    review_id UNIQUEIDENTIFIER,
    order_id UNIQUEIDENTIFIER NOT NULL,
    review_score INT NOT NULL,
    review_comment_title NVARCHAR(50),
    review_comment_message NVARCHAR(255),
    review_creation_date DATETIME NOT NULL,
    review_answer_timestamp DATETIME NOT NULL,
    datekey INT NOT NULL,

    CONSTRAINT PK_fact_review PRIMARY KEY (review_id),
    CONSTRAINT FK_fact_review_date FOREIGN KEY (datekey) REFERENCES DimDate(DateKey),
    CONSTRAINT FK_fact_review_score FOREIGN KEY (review_score) REFERENCES dim_review_score(review_score),
    CONSTRAINT review_score CHECK (review_score BETWEEN 1 AND 5)
    
);
