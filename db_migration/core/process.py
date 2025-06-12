
class PostgresToMySQLDataTypeAdapter:
    def convert_data(self, column_object_type) -> str:
        data_class_name = column_object_type.__class__.__name__.upper()

        # 1) UUID -> CHAR(36)
        if isinstance(column_object_type, PostGre_UUID) or data_class_name == "UUID":
            return "CHAR(36)"

        # 2) BIGINT
        if (
            isinstance(column_object_type, PostGre_BIGINT)
            or data_class_name == "BIGINT"
        ):
            return "BIGINT"

        # 3) SMALLINT
        if (
            isinstance(column_object_type, PostGre_SMALLINT)
            or data_class_name == "SMALLINT"
        ):
            return "SMALLINT"

        # 4) INTEGER -> INT
        if (
            isinstance(column_object_type, PostGre_INTEGER)
            or isinstance(column_object_type, Gen_Integer)
            or data_class_name == "INTEGER"
        ):
            return "INT"

        # 5) DOUBLE PRECISION -> DOUBLE
        if (
            isinstance(column_object_type, PostGre_DOUBLE_PRECISION)
            or (
                isinstance(column_object_type, Gen_Float)
                and getattr(column_object_type, "precision", None) == 53
            )
            or data_class_name in ("DOUBLE_PRECISION", "DOUBLE")
        ):
            return "DOUBLE"

        # 6) REAL -> FLOAT
        if (
            isinstance(column_object_type, PostGre_REAL)
            or (
                isinstance(column_object_type, Gen_Float)
                and getattr(column_object_type, "precision", None) == 24
            )
            or data_class_name == "REAL"
            or (
                data_class_name == "FLOAT"
                and getattr(column_object_type, "precision", None) is None
            )
        ):
            return "FLOAT"

        # 7) CHAR(length)
        if isinstance(column_object_type, PostGre_CHAR) or data_class_name.startswith(
            "CHAR"
        ):
            length = getattr(column_object_type, "length", None) or 1
            return f"CHAR({length})"

        # 8) TEXT
        if isinstance(column_object_type, PostGre_TEXT) or data_class_name == "TEXT":
            return "TEXT"

        # 9) VARCHAR(length)
        if (
            isinstance(column_object_type, PostGre_VARCHAR)
            or isinstance(column_object_type, Gen_String)
            or data_class_name.startswith("VARCHAR")
        ):
            length = getattr(column_object_type, "length", None) or 255
            return f"VARCHAR({length})"

        # 10) DATE
        if (
            isinstance(column_object_type, PostGre_DATE)
            or isinstance(column_object_type, Gen_Date)
            or data_class_name == "DATE"
        ):
            return "DATE"

        # 11) TIME
        if (
            isinstance(column_object_type, PostGre_TIME)
            or isinstance(column_object_type, Gen_Time)
            or data_class_name == "TIME"
        ):
            return "TIME"

        # 12) TIMESTAMP (both with & without time zone) -> DATETIME
        if (
            isinstance(column_object_type, PostGre_TIMESTAMP)
            or isinstance(column_object_type, Gen_DateTime)
            or data_class_name == "TIMESTAMP"
        ):
            return "DATETIME"

        # 13) BOOLEAN
        if (
            isinstance(column_object_type, PostGre_BOOLEAN)
            or isinstance(column_object_type, Gen_Boolean)
            or data_class_name == "BOOLEAN"
        ):
            return "BOOLEAN"

        # 14) NUMERIC/DECIMAL -> DECIMAL
        if (
            isinstance(column_object_type, PostGre_NUMERIC)
            or isinstance(column_object_type, Gen_Numeric)
            or data_class_name in ("NUMERIC", "DECIMAL")
        ):
            precision = getattr(column_object_type, "precision", None) or 10
            scale = getattr(column_object_type, "scale", None) or 0
            return f"DECIMAL({precision},{scale})"

        # 15) BYTEA -> BLOB
        if (
            isinstance(column_object_type, PostGre_BYTEA)
            or isinstance(column_object_type, Gen_LargeBinary)
            or data_class_name == "BYTEA"
        ):
            return "BLOB"

        # 16) JSON/JSONB -> JSON
        if (
            isinstance(column_object_type, PostGre_JSON)
            or isinstance(column_object_type, PostGre_JSONB)
            or isinstance(column_object_type, Gen_JSON)
            or data_class_name in ("JSON", "JSONB")
        ):
            return "JSON"

        # 17) Default fallback to TEXT
        return "TEXT"


def generate_mysql_create_table(
    connection,
    database_name: str,
    table_name: str,
    adapter: PostgresToMySQLDataTypeAdapter,
):
    postgre_eng = db_engine("postgres", database_name)
    inspector = inspect(postgre_eng)

    columns = inspector.get_columns(table_name)
    try:
        pk_info = inspector.get_pk_constraint(table_name)
    except Exception:
        pk_info = {}
    pk_columns = pk_info.get("constrained_columns", [])

    ddl_parts = [f"CREATE TABLE `{table_name}` ("]
    col_def = []

    for col in columns:
        name = col["name"]
        col_type_obj = col["type"]
        mysql_type = adapter.convert_data(col_type_obj)
        null_const = "NULL" if col["nullable"] else "" 
        default_val = ""
        col_def.append(f"`{name}` {mysql_type} {null_const} {default_val}".strip()) 
    if pk_columns:
        pk_list = ", ".join(f"`{c}`" for c in pk_columns)
        col_def.append(f"  PRIMARY KEY ({pk_list})")

    ddl_parts.append(",\n".join(col_def))
    ddl_parts.append(");")
    ddl_statement = "\n".join(ddl_parts)

    # Debug print
    print(f"===== DDL FOR TABLE {table_name} =====")
    print(ddl_statement)
    print("=====================================")

    connection.execute(text(f"DROP TABLE IF EXISTS `{table_name}`;"))
    connection.execute(text(ddl_statement))


def generate_mysql_ddl(database_name: str, table_name: str) -> str:  
    engine = db_engine("postgres", database_name)
    inspector = inspect(engine)
    table_columns = inspector.get_columns(table_name)

    table_ddl_create = [f"CREATE TABLE `{table_name}` ("]
    col_defs = []
    adapter = PostgresToMySQLDataTypeAdapter()

    for column in table_columns:
        col_name = column["name"]
        col_type_obj = column["type"]
        sql_type = adapter.convert_data(col_type_obj)
        null_const = "NULL" if column["nullable"] else "NOT NULL"
        default_val = ""
        col_defs.append(f"  `{col_name}` {sql_type} {null_const} {default_val}".strip())

    table_ddl_create.append(",\n".join(col_defs))
    table_ddl_create.append(");")
    return "\n".join(table_ddl_create)

