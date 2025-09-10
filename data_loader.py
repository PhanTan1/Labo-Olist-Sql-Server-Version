import pandas as pd
import uuid
import logging
from sqlalchemy import text, event
from sqlalchemy.exc import DataError

# Setup logging for dropped duplicates or load errors
logging.basicConfig(
    filename='duplicate_key_drops.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# Mapping of each table to its primary-key columns
PK_COLUMNS = {
    'customers': ['customer_id'],
    'orders': ['order_id'],
    'order_items': ['order_item_id', 'order_id'],
    'order_payments': ['order_id', 'payment_sequential'],
    'order_reviews': ['review_id'],
    'products': ['product_id'],
    'sellers': ['seller_id'],
}

# Tables that have no PK or for which we don’t need deduplication
FAST_LOAD_TABLES = ['geolocation', 'product_category_name_translation']

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

    # Apply UUID formatting
    uuid_cols = {
        'customers': ['customer_id', 'customer_unique_id'],
        'orders': ['order_id', 'customer_id'],
        'order_items': ['order_id', 'product_id', 'seller_id'],
        'order_payments': ['order_id'],
        'order_reviews': ['review_id', 'order_id'],
        'products': ['product_id'],
        'sellers': ['seller_id']
    }
    for col in uuid_cols.get(table_name, []):
        if col in df.columns:
            df[col] = df[col].apply(format_guid)

    # Fast-load tables without deduplication
    if table_name in FAST_LOAD_TABLES:
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"🚀 Fast-loaded {table_name} ({len(df)} rows).")
        return

    # Drop duplicate keys in the DataFrame before inserting
    pk = PK_COLUMNS.get(table_name)
    if pk:
        dupes = df[df.duplicated(subset=pk, keep='first')]
        if not dupes.empty:
            for _, row in dupes.iterrows():
                logging.info(
                    f"Dropped duplicate from '{table_name}': {row.to_dict()}\n"
                    f"Exception: duplicate key value violates unique constraint \"pk__{table_name}\"\n"
                    f"DETAIL: Key ({', '.join([f'{k}={row[k]}' for k in pk])}) already exists.\n"
                )
        df = df.drop_duplicates(subset=pk, keep='first')

    # Enable fast_executemany for pyodbc bulk insert optimization
    @event.listens_for(engine, "before_cursor_execute")
    def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        if executemany:
            cursor.fast_executemany = True

    # Bulk insert the cleaned DataFrame
    try:
        df.to_sql(
            table_name,
            engine,
            if_exists='append',
            index=False,
            chunksize=1000  # Removed method='multi' for SQL Server compatibility
        )
        print(f"✅ Loaded {table_name} ({len(df)} rows).")
    except DataError as err:
        logging.error(f"DataError loading '{table_name}': {err}")
        raise
