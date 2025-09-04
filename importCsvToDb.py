from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError, DataError
import pandas as pd

# Database credentials
username = 'postgres'
password = 'password'
host = 'localhost'
port = '5432'
database = 'olist'

# Create SQLAlchemy engine
engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}', echo=True)

# Step 1: Create the table
with engine.begin() as conn:
    create_table_sql = """
    DROP TABLE IF EXISTS product_category_name_translation;

    CREATE TABLE product_category_name_translation (
        product_category_name VARCHAR (50) NOT NULL,
        product_category_name_english VARCHAR (50) NOT NULL,
        UNIQUE(product_category_name),
        UNIQUE(product_category_name_english)
);
    """
    conn.execute(text(create_table_sql))

# Step 2: Load CSV data
df = pd.read_csv('data/olist_product_category_name_translation_dataset.csv')
df = df.where(pd.notnull(df), None)

# Step 3: Insert row-by-row to catch errors
with engine.begin() as conn:
    for i, row in df.iterrows():
        try:
            pd.DataFrame([row]).to_sql('product_category_name_translation', conn, if_exists='append', index=False, method='multi')
        except (IntegrityError, DataError) as e:
            print(f"❌ Error at row {i}:")
            print(row.to_dict())
            print(f"Exception: {e.orig}")