# src/tools/sql_tools.py
from langchain_community.utilities import SQLDatabase
from src.config.permissions import USER_DB_PERMISSIONS, DB_REGISTRY

def get_db_for_user(user_id: str, db_key: str):
    """
    Validates permissions and returns a LangChain SQLDatabase object.
    """
    # 1. Check if the database exists in our registry
    if db_key not in DB_REGISTRY:
        raise ValueError(f"Database '{db_key}' not found in registry.")

    # 2. Check if the user has permission for this specific database
    allowed_dbs = USER_DB_PERMISSIONS.get(user_id, [])
    if db_key not in allowed_dbs:
        raise PermissionError(f"User {user_id} does not have access to {db_key}.")

    # 3. Establish a connection (using read-only mode for safety)
    db_path = DB_REGISTRY[db_key]
    # Note: Using 'mode=ro' is a best practice for security
    return SQLDatabase.from_uri(f"sqlite:///{db_path}")