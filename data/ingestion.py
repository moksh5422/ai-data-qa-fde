import io
import re
from pathlib import Path

import duckdb
import pandas as pd


def safe_table_name(name):
    value = re.sub(r"[^a-zA-Z0-9_]+", "_", Path(name).stem).strip("_").lower()
    if not value:
        value = "uploaded_data"
    if value[0].isdigit():
        value = "t_" + value
    return value


def unique_name(base, used):
    candidate = base
    index = 2
    while candidate in used:
        candidate = f"{base}_{index}"
        index += 1
    return candidate


def load_uploaded_files(uploaded_files):
    connection = duckdb.connect(":memory:")
    tables, messages, used = [], [], set()

    for uploaded in uploaded_files:
        suffix = Path(uploaded.name).suffix.lower()
        raw = uploaded.getvalue()

        if suffix == ".csv":
            dataframe = pd.read_csv(io.BytesIO(raw))
            name = unique_name(safe_table_name(uploaded.name), used)
            connection.register(name, dataframe)
            tables.append(name)
            used.add(name)
            messages.append(f"{uploaded.name} → {name} ({len(dataframe):,} rows)")

        elif suffix in {".xlsx", ".xls"}:
            sheets = pd.read_excel(io.BytesIO(raw), sheet_name=None)
            for sheet, dataframe in sheets.items():
                if dataframe.empty:
                    continue
                name = unique_name(
                    safe_table_name(f"{uploaded.name}_{sheet}"), used
                )
                connection.register(name, dataframe)
                tables.append(name)
                used.add(name)
                messages.append(
                    f"{uploaded.name} / {sheet} → {name} ({len(dataframe):,} rows)"
                )
        else:
            raise ValueError(f"Unsupported file type: {suffix}")

    return connection, tables, messages
