from data.ingestion import safe_table_name


def test_table_names():
    assert safe_table_name("My Sales File.xlsx") == "my_sales_file"
    assert safe_table_name("2025 Sales.csv") == "t_2025_sales"
