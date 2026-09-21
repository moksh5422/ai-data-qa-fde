import pytest
from query.validator import validate_sql


def test_select_allowed():
    assert validate_sql("SELECT SUM(revenue) FROM orders").startswith("SELECT")


def test_with_allowed():
    assert validate_sql("WITH x AS (SELECT revenue FROM orders) SELECT SUM(revenue) FROM x").startswith("WITH")


@pytest.mark.parametrize("sql", [
    "DROP TABLE orders",
    "DELETE FROM orders",
    "UPDATE orders SET revenue = 0",
    "INSERT INTO orders VALUES (1)",
    "CREATE TABLE x AS SELECT 1",
])
def test_write_operations_rejected(sql):
    with pytest.raises(ValueError):
        validate_sql(sql)


def test_multiple_statements_rejected():
    with pytest.raises(ValueError):
        validate_sql("SELECT 1; DROP TABLE orders")
