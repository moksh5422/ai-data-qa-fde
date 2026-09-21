import re

FORBIDDEN = (
    "insert", "update", "delete", "drop", "alter", "create",
    "copy", "attach", "install", "load", "pragma", "call",
    "set", "use", "vacuum", "truncate", "export"
)


def clean_sql(sql):
    sql = sql.strip()
    sql = re.sub(r"^```(?:sql)?", "", sql, flags=re.IGNORECASE).strip()
    sql = re.sub(r"```$", "", sql).strip()
    return sql.rstrip(";").strip()


def validate_sql(sql):
    sql = clean_sql(sql)
    if not sql:
        raise ValueError("Empty SQL query.")
    if ";" in sql:
        raise ValueError("Multiple SQL statements are not allowed.")
    normalized = re.sub(r"\s+", " ", sql.lower()).strip()
    if not (normalized.startswith("select ") or normalized.startswith("with ")):
        raise ValueError("Only SELECT/WITH queries are allowed.")
    for keyword in FORBIDDEN:
        if re.search(rf"\b{re.escape(keyword)}\b", normalized):
            raise ValueError(f"Forbidden SQL operation: {keyword}")
    return sql
