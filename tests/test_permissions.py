# tests/test_permissions.py
import pytest
from src.tools.sql_tools import get_db_for_user

def test_unauthorized_access():
    with pytest.raises(PermissionError):
        get_db_for_user("logistics_team", "sakila")

def test_authorized_access():
    db = get_db_for_user("marketing_team", "chinook")
    assert db is not None