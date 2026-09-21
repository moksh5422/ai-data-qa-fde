import json


def build_catalog(connection, tables):
    sections = []

    for table in tables:
        schema = connection.execute(
            f'DESCRIBE "{table}"'
        ).fetchdf()

        row_count = connection.execute(
            f'SELECT COUNT(*) FROM "{table}"'
        ).fetchone()[0]

        sample = connection.execute(
            f'SELECT * FROM "{table}" LIMIT 3'
        ).fetchdf()

        lines = [
            f"TABLE: {table}",
            f"ROWS: {row_count:,}",
            "COLUMNS:",
        ]

        for _, row in schema.iterrows():
            lines.append(
                f"  - {row['column_name']}: {row['column_type']}"
            )

        lines.append("SAMPLE:")
        lines.append(
            json.dumps(
                sample.to_dict(orient="records"),
                default=str
            )
        )

        sections.append("\n".join(lines))

    return "\n\n".join(sections)
