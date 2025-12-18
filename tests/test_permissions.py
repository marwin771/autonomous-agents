# tests/test_permissions.py
import pytest
from src.tools.sql_tools import get_db_for_user

def test_unauthorized_access():
    with pytest.raises(PermissionError):
        # User 002 only has 'marketing_leads' access
        get_db_for_user("user_002", "global_sales")

def test_authorized_access():
    # Assuming the file exists in /data/
    db = get_db_for_user("user_001", "global_sales")
    assert db is not None