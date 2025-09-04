from sqlalchemy import create_engine

DB_CONFIG = {
    'username': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': '5432',
    'database': 'olist'
}

def get_engine():
    url = f"postgresql://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    return create_engine(url)
