from db_config import get_engine
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy import text
import pandas as pd
import uuid
from sqlalchemy.types import CHAR, String

# Connect to SQL Server
engine = get_engine()

# Step 1: Create the table
with engine.begin() as conn:
    create_table_sql = """
    DROP TABLE IF EXISTS customers;
    CREATE TABLE customers (
        customer_id UNIQUEIDENTIFIER,
        customer_unique_id UNIQUEIDENTIFIER NOT NULL,
        customer_zip_code_prefix VARCHAR(5) NOT NULL,
        customer_city VARCHAR(32),
        customer_state VARCHAR(2),

        CONSTRAINT PK__customers PRIMARY KEY (customer_id),
        CONSTRAINT customer_zip_code_prefix_valid CHECK (customer_zip_code_prefix LIKE '[0-9][0-9][0-9][0-9]%'),
        CONSTRAINT customer_state_format CHECK (customer_state LIKE '[A-Z][A-Z]')
    );
    """
    conn.execute(text(create_table_sql))

# Step 2: Load CSV data
df = pd.read_csv('data/olist_customers_dataset.csv')
df = df.where(pd.notnull(df), None)

# Step 3: Format UUIDs
def format_guid(value):
    try:
        return str(uuid.UUID(value))
    except (ValueError, TypeError):
        return None  # Skip invalid UUIDs

df['customer_id'] = df['customer_id'].apply(format_guid)
df['customer_unique_id'] = df['customer_unique_id'].apply(format_guid)

# Step 4: Insert row-by-row to catch errors


uuid_type = CHAR(36)  # SQL Server expects 36-character GUID strings

with engine.begin() as conn:
    for i, row in df.iterrows():
        try:
            pd.DataFrame([row]).to_sql(
                'customers',
                conn,
                if_exists='append',
                index=False,
                method='multi',
                dtype={
                    'customer_id': uuid_type,
                    'customer_unique_id': uuid_type,
                    'customer_zip_code_prefix': String(5),
                    'customer_city': String(32),
                    'customer_state': String(2)
                }
            )
        except (IntegrityError, DataError) as e:
            print(f"❌ Error at row {i}:")
            print(row.to_dict())
            print(f"Exception: {e.orig}")
