import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    # User provided credentials
    config = {"user": "postgres", "password": "juanesgc1", "host": "localhost", "port": "5432"}
    target_db = "gestionacademica"

    print(f"Connecting to PostgreSQL as {config['user']} to create '{target_db}'...")
    
    try:
        # Connect to default 'postgres' db to create the new one
        conn = psycopg2.connect(
            user=config["user"],
            password=config["password"],
            host=config["host"],
            port=config["port"],
            dbname="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        cur = conn.cursor()
        
        # Check if db exists
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{target_db}'")
        exists = cur.fetchone()
        
        if not exists:
            print(f"Database '{target_db}' does not exist. Creating...")
            cur.execute(f"CREATE DATABASE {target_db}")
            print(f"Database '{target_db}' created successfully.")
        else:
            print(f"Database '{target_db}' already exists.")
        
        cur.close()
        conn.close()
        return True

    except psycopg2.Error as e:
        print(f"Failed to create database: {e}")
        return False

if __name__ == "__main__":
    create_database()
