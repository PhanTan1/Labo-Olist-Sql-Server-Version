UPDATE FactOrder
SET 
    customer_id = ?,
    product_id = ?,
    seller_id = ?,

    order_status_id = ?,
    order_purchase_timestamp = ?,
    order_delivered_customer_date = ?,
    order_estimated_delivery_date = ?,

    datekey = ?,
    timekey = ?,

    price = ?,
    freight_value = ?,

    product_category_name = ?,
    product_name_length = ?,
    product_description_length = ?,
    product_photos_qty = ?,

    payment_type = ?,
    payment_installments = ?,
    payment_value = ?
WHERE 
    order_id = ? AND 
    order_item_id = ?;