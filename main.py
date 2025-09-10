from db_config import get_engine
from table_schemas import TABLES
from data_loader import create_table, load_csv_to_table
from post_load_tasks import create_zip_code_reference, add_foreign_keys

engine = get_engine()

for table_name, create_sql in TABLES.items():
    print(f"Creating table: {table_name}")
    create_table(engine, create_sql)
    
    # Skip derived table
    if table_name == 'zip_code_reference':
        continue

    csv_path = f"data/olist_{table_name}_dataset.csv"
    print(f"Loading data from: {csv_path}")
    load_csv_to_table(csv_path, table_name, engine)

# Create derived table and add constraints
create_zip_code_reference(engine)
add_foreign_keys(engine)

print("✅ All tables created and data loaded.")
