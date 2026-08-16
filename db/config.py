import os

from dotenv import load_dotenv

load_dotenv()

# Legacy PostgreSQL configuration.
# Productized builds should not require a separately managed database server.
# Keep credentials in the local environment only; never commit them.
DB_CONFIG = {
    "dbname": os.environ.get("INVENTORY_DB_NAME", "inventory_db"),
    "user": os.environ.get("INVENTORY_DB_USER", "postgres"),
    "password": os.environ.get("INVENTORY_DB_PASSWORD", ""),
    "host": os.environ.get("INVENTORY_DB_HOST", "localhost"),
    "port": os.environ.get("INVENTORY_DB_PORT", "5432"),
}
