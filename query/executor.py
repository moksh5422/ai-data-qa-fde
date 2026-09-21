from config import MAX_RESULT_ROWS


def execute_sql(connection, sql):
    result = connection.execute(sql).fetchdf()
    if len(result) > MAX_RESULT_ROWS:
        raise ValueError(f"Result contains more than {MAX_RESULT_ROWS:,} rows.")
    return result
