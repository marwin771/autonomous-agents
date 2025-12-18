# src/config/permissions.py

# 1. Mapping User IDs to the database keys they are allowed to access.
USER_DB_PERMISSIONS = {
    "marketing_team": ["chinook"],       # Only music sales data
    "logistics_team": ["northwind"],     # Only inventory/ERP data
    "admin_user": ["sakila", "chinook", "northwind"] # Access to everything
}

# 2. Database Registry (Easy Integration)
# Ensure these filenames match the files in your /data folder exactly.
DB_REGISTRY = {
    "sakila": "data/sakila.db",
    "chinook": "data/chinook.db",
    "northwind": "data/northwind_small.sqlite"
}