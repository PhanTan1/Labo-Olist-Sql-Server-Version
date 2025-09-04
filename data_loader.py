import pandas as pd
from sqlalchemy import text

def create_table(engine, sql):
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()

def load_csv_to_table(csv_path, table_name, engine):
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, engine, if_exists='append', index=False, method='multi')
