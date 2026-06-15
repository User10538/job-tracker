def add_column_if_missing(
    cursor,
    conn,
    column_name
):

    cursor.execute(
        "PRAGMA table_info(jobs)"
    )

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    if column_name not in columns:

        cursor.execute(
            f"""
            ALTER TABLE jobs
            ADD COLUMN {column_name} TEXT
            """
        )

        conn.commit()
