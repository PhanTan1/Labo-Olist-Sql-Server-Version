import pandas as pd
import uuid
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.types import CHAR, String
from db_config import get_engine

# Connect to SQL Server
engine = get_engine()

# Step 1: Drop and recreate the customers table
with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS customers;"))
    conn.execute(text("""
        CREATE TABLE customers (
            customer_id UNIQUEIDENTIFIER,
            customer_unique_id UNIQUEIDENTIFIER NOT NULL,
            customer_zip_code_prefix NVARCHAR(5) NOT NULL,
            customer_city NVARCHAR(32),
            customer_state NVARCHAR(2),
            CONSTRAINT PK__customers PRIMARY KEY (customer_id),
            CONSTRAINT customer_zip_code_prefix_valid CHECK (customer_zip_code_prefix LIKE '[0-9][0-9][0-9][0-9]%'),
            CONSTRAINT customer_state_format CHECK (customer_state LIKE '[A-Z][A-Z]')
        );
    """))

# Step 2: Load and clean the CSV data
df = pd.read_csv('data/olist_customers_dataset.csv')
df = df.where(pd.notnull(df), None)

# Step 3: Format UUIDs safely
def format_guid(value):
    try:
        return str(uuid.UUID(value))
    except (ValueError, TypeError):
        return None

df = df[df['customer_id'].apply(lambda x: format_guid(x) is not None)]
df['customer_id'] = df['customer_id'].apply(format_guid)
df['customer_unique_id'] = df['customer_unique_id'].apply(format_guid)

# Step 4: Bulk insert with error handling
uuid_type = CHAR(36)

try:
    df.to_sql(
        'customers',
        con=engine,
        if_exists='append',
        index=False,
        chunksize=1000,
        dtype={
            'customer_id': uuid_type,
            'customer_unique_id': uuid_type,
            'customer_zip_code_prefix': String(5),
            'customer_city': String(32),
            'customer_state': String(2)
        }
    )
    print(f"✅ Successfully loaded {len(df)} rows into 'customers'.")
except (IntegrityError, DataError) as e:
    print("❌ Bulk insert failed:")
    print(f"Exception: {e.orig}")
