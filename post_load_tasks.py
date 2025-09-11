from sqlalchemy import text

def generate_zip_code_reference(engine):
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS zip_code_reference"))

        conn.execute(text("""
            SELECT 
                geolocation_zip_code_prefix,
                AVG(geolocation_lat) AS geolocation_lat,
                AVG(geolocation_lng) AS geolocation_lng
            INTO zip_code_reference
            FROM geolocation
            GROUP BY geolocation_zip_code_prefix
            ORDER BY geolocation_zip_code_prefix;
        """))

        conn.execute(text("""
            ALTER TABLE zip_code_reference
            ADD CONSTRAINT pk_zip_code PRIMARY KEY (geolocation_zip_code_prefix)
        """))

    print("✅ zip_code_reference table created from geolocation.")

def add_foreign_keys(engine):
    with engine.begin() as conn:
        conn.execute(text("""
            ALTER TABLE customers
            ADD CONSTRAINT fk_customers_zip FOREIGN KEY (customer_zip_code_prefix)
            REFERENCES zip_code_reference(geolocation_zip_code_prefix);
        """))
        conn.execute(text("""
            ALTER TABLE sellers
            ADD CONSTRAINT fk_sellers_zip FOREIGN KEY (seller_zip_code_prefix)
            REFERENCES zip_code_reference(geolocation_zip_code_prefix);
        """))
    print("🔗 Foreign keys added to customers and sellers.")
