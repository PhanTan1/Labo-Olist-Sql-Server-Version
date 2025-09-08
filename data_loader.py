# import pandas as pd
# from sqlalchemy import text

# def create_table(engine, sql):
#     with engine.connect() as conn:
#         conn.execute(text(sql))
#         conn.commit()

# def load_csv_to_table(csv_path, table_name, engine):
#     df = pd.read_csv(csv_path)
#     df.to_sql(table_name, engine, if_exists='append', index=False, method='multi')

import pandas as pd
import uuid
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.types import CHAR, String, SmallInteger, Integer, Numeric, DateTime, DECIMAL

def create_table(engine, create_sql):
    with engine.begin() as conn:
        conn.execute(text(create_sql))

def format_guid(value):
    try:
        return str(uuid.UUID(value))
    except (ValueError, TypeError):
        return None

def load_csv_to_table(csv_path, table_name, engine):
    df = pd.read_csv(csv_path)
    df = df.where(pd.notnull(df), None)

    # Format UUIDs based on table
    uuid_columns = {
        'customers': ['customer_id', 'customer_unique_id'],
        'orders': ['order_id', 'customer_id'],
        'order_items': ['order_id', 'product_id', 'seller_id'],
        'order_payments': ['order_id'],
        'order_reviews': ['review_id', 'order_id'],
        'products': ['product_id'],
        'sellers': ['seller_id']
    }

    for col in uuid_columns.get(table_name, []):
        if col in df.columns:
            df[col] = df[col].apply(format_guid)

    # Define dtype mappings
    dtype_map = {
        'customers': {
            'customer_id': CHAR(36),
            'customer_unique_id': CHAR(36),
            'customer_zip_code_prefix': String(5),
            'customer_city': String(32),
            'customer_state': String(2)
        },
        'geolocation': {
            'geolocation_zip_code_prefix': String(5),
            'geolocation_lat': Numeric(15, 10),
            'geolocation_lng': Numeric(15, 10),
            'geolocation_city': String(38),
            'geolocation_state': String(2)
        },
        'orders': {
            'order_id': CHAR(36),
            'customer_id': CHAR(36),
            'order_status': String(11),
            'order_purchase_timestamp': DateTime(),
            'order_approved_at': DateTime(),
            'order_delivered_carrier_date': DateTime(),
            'order_delivered_customer_date': DateTime(),
            'order_estimated_delivery_date': DateTime()
        },
        'order_items': {
            'order_id': CHAR(36),
            'order_item_id': SmallInteger(),
            'product_id': CHAR(36),
            'seller_id': CHAR(36),
            'shipping_limit_date': DateTime(),
            'price': DECIMAL(8, 2),
            'freight_value': DECIMAL(8, 2)
        },
        'order_payments': {
            'order_id': CHAR(36),
            'payment_sequential': SmallInteger(),
            'payment_type': String(11),
            'payment_installments': Integer(),
            'payment_value': DECIMAL(8, 2)
        },
        'order_reviews': {
            'review_id': CHAR(36),
            'order_id': CHAR(36),
            'review_score': Integer(),
            'review_comment_title': String(50),
            'review_comment_message': String(255),
            'review_creation_date': DateTime(),
            'review_answer_timestamp': DateTime()
        },
        'products': {
            'product_id': CHAR(36),
            'product_category_name': String(60),
            'product_name_length': String(11),
            'product_description_length': SmallInteger(),
            'product_photos_qty': SmallInteger(),
            'product_weight_g': Integer(),
            'product_length_cm': SmallInteger(),
            'product_height_cm': SmallInteger(),
            'product_width_cm': SmallInteger()
        },
        'sellers': {
            'seller_id': CHAR(36),
            'seller_zip_code_prefix': String(5),
            'seller_city': String(45),
            'seller_state': String(2)
        },
        'product_category_name_translation': {
            'product_category_name': String(60),
            'product_category_name_english': String(60)
        }
    }

    with engine.begin() as conn:
        for i, row in df.iterrows():
            try:
                pd.DataFrame([row]).to_sql(
                    table_name,
                    conn,
                    if_exists='append',
                    index=False,
                    method='multi',
                    dtype=dtype_map.get(table_name)
                )
            except (IntegrityError, DataError) as e:
                print(f"❌ Error at row {i} in table '{table_name}':")
                print(row.to_dict())
                print(f"Exception: {e.orig}")
