from sqlalchemy import create_engine
import urllib

DB_CONFIG = {
    'dbms': 'mssql+pyodbc',
    'server': 'ict-210-06',
    'database': 'olist',
    'username': 'sa1',
    'password': 'Qwertyui1#',
    'driver': 'ODBC Driver 18 for SQL Server'
}

def get_engine():
    odbc_str = (
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"UID={DB_CONFIG['username']};"
        f"PWD={DB_CONFIG['password']};"
        f"TrustServerCertificate=yes;"
        f"Encrypt=yes"
    )
    connection_url = f"{DB_CONFIG['dbms']}:///?odbc_connect={urllib.parse.quote_plus(odbc_str)}"
    return create_engine(connection_url)
