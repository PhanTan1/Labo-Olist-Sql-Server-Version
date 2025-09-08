from db_config import get_engine
from table_schemas_sql_server_version import TABLES
from data_loader import create_table, load_csv_to_table

engine = get_engine()

for table_name, create_sql in TABLES.items():
    print(f"Creating table: {table_name}")
    create_table(engine, create_sql)

    csv_path = f"data/olist_{table_name}_dataset.csv"
    print(f"Loading data from: {csv_path}")
    load_csv_to_table(csv_path, table_name, engine)

print("✅ All tables created and data loaded.")
