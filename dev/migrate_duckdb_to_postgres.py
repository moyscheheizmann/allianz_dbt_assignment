"""Migrate tables from DuckDB raw schema to PostgreSQL raw schema."""

import duckdb
import psycopg2
import pandas as pd
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# Configuration
import os

DUCKDB_PATH = "transformation/casestudy.duckdb"
PG_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "postgres"),  # Use env var from devcontainer
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "user": os.getenv("POSTGRES_USER", "dbt_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "dbt_password"),
    "database": os.getenv("POSTGRES_DB", "dbt_dev")
}


def get_raw_tables(duck_conn):
    """Get list of tables in raw schema."""
    query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'raw'
        ORDER BY table_name
    """
    return duck_conn.execute(query).fetchdf()['table_name'].tolist()


def create_schema_if_not_exists(pg_conn):
    """Create raw schema in PostgreSQL if it doesn't exist."""
    with pg_conn.cursor() as cur:
        cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    pg_conn.commit()
    print("✓ Created/verified raw schema in PostgreSQL")


def migrate_table(table_name, duck_conn, pg_conn):
    """Migrate a single table from DuckDB to PostgreSQL."""
    print(f"\nMigrating table: {table_name}")

    # Read data from DuckDB
    query = f'SELECT * FROM raw."{table_name}"'
    df = duck_conn.execute(query).fetchdf()
    print(f"  Read {len(df)} rows from DuckDB")

    if len(df) == 0:
        print(f"  ⚠ Table {table_name} is empty, skipping")
        return

    # Drop table if exists in PostgreSQL
    with pg_conn.cursor() as cur:
        cur.execute(f'DROP TABLE IF EXISTS raw."{table_name}" CASCADE;')
    pg_conn.commit()

    # Create table and insert data using pandas
    from sqlalchemy import create_engine
    engine = create_engine(
        f"postgresql://{PG_CONFIG['user']}:{PG_CONFIG['password']}@"
        f"{PG_CONFIG['host']}:{PG_CONFIG['port']}/{PG_CONFIG['database']}"
    )

    df.to_sql(
        table_name,
        engine,
        schema='raw',
        if_exists='replace',
        index=False,
        method='multi',
        chunksize=1000
    )

    print(f"  ✓ Migrated {len(df)} rows to PostgreSQL")

    # Verify
    with pg_conn.cursor() as cur:
        cur.execute(f'SELECT COUNT(*) FROM raw."{table_name}"')
        count = cur.fetchone()[0]
        print(f"  ✓ Verified {count} rows in PostgreSQL")


def main():
    """Main migration function."""
    print("=" * 80)
    print("DuckDB to PostgreSQL Migration")
    print("=" * 80)

    # Connect to DuckDB
    print("\nConnecting to DuckDB...")
    duck_conn = duckdb.connect(DUCKDB_PATH, read_only=True)
    print("✓ Connected to DuckDB")

    # Connect to PostgreSQL
    print("\nConnecting to PostgreSQL...")
    pg_conn = psycopg2.connect(**PG_CONFIG)
    pg_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    print("✓ Connected to PostgreSQL")

    # Create raw schema
    create_schema_if_not_exists(pg_conn)

    # Get tables from DuckDB
    tables = get_raw_tables(duck_conn)
    print(f"\nFound {len(tables)} tables in raw schema:")
    for table in tables:
        print(f"  - {table}")

    # Migrate each table
    print("\n" + "=" * 80)
    print("Starting Migration")
    print("=" * 80)

    for table in tables:
        try:
            migrate_table(table, duck_conn, pg_conn)
        except Exception as e:
            print(f"  ✗ Error migrating {table}: {e}")
            continue

    # Close connections
    duck_conn.close()
    pg_conn.close()

    print("\n" + "=" * 80)
    print("Migration Complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
