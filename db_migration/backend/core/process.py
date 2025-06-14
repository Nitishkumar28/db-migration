from sqlalchemy.dialects.postgresql import (
    UUID as PostGre_UUID,
    VARCHAR as PostGre_VARCHAR,
    CHAR as PostGre_CHAR,
    TEXT as PostGre_TEXT,
    INTEGER as PostGre_INTEGER,
    SMALLINT as PostGre_SMALLINT,
    BIGINT as PostGre_BIGINT,
    NUMERIC as PostGre_NUMERIC,
    REAL as PostGre_REAL,
    DOUBLE_PRECISION as PostGre_DOUBLE_PRECISION,
    BYTEA as PostGre_BYTEA,
    JSON as PostGre_JSON,
    JSONB as PostGre_JSONB,
    TIMESTAMP as PostGre_TIMESTAMP,
    TIME as PostGre_TIME,
    DATE as PostGre_DATE,
    BOOLEAN as PostGre_BOOLEAN,
)


from sqlalchemy.types import (
    Integer as Gen_Integer,
    String as Gen_String,
    Numeric as Gen_Numeric,
    Date as Gen_Date,
    DateTime as Gen_DateTime,
    Boolean as Gen_Boolean,
    Float as Gen_Float,
    LargeBinary as Gen_LargeBinary,
    JSON as Gen_JSON,
    Time as Gen_Time,
)


class PostgresToMySQLDataTypeAdapter:
    def __init__(self):
        
        self.postgre_to_mysql_map = {
            PostGre_UUID: lambda col: "CHAR(36)",
            PostGre_BIGINT: lambda col: "BIGINT",
            PostGre_SMALLINT: lambda col: "SMALLINT",
            PostGre_INTEGER: lambda col: "INT",
            Gen_Integer: lambda col: "INT",
            PostGre_DOUBLE_PRECISION: lambda col: "DOUBLE",
            PostGre_REAL: lambda col: "FLOAT",
            Gen_Float: self._handle_float,
            PostGre_CHAR: self._handle_char,
            PostGre_TEXT: lambda col: "TEXT",
            PostGre_VARCHAR: self._handle_varchar,
            Gen_String: self._handle_varchar,
            PostGre_DATE: lambda col: "DATE",
            Gen_Date: lambda col: "DATE",
            PostGre_TIME: lambda col: "TIME",
            Gen_Time: lambda col: "TIME",
            PostGre_TIMESTAMP: lambda col: "DATETIME",
            Gen_DateTime: lambda col: "DATETIME",
            PostGre_BOOLEAN: lambda col: "BOOLEAN",
            Gen_Boolean: lambda col: "BOOLEAN",
            PostGre_NUMERIC: self._handle_numeric,
            Gen_Numeric: self._handle_numeric,
            PostGre_BYTEA: lambda col: "BLOB",
            Gen_LargeBinary: lambda col: "BLOB",
            PostGre_JSON: lambda col: "JSON",
            PostGre_JSONB: lambda col: "JSON",
            Gen_JSON: lambda col: "JSON",
        }

        self.postgre_to_mysql_map_fallback = {
            "UUID": "CHAR(36)",
            "BIGINT": "BIGINT",
            "SMALLINT": "SMALLINT",
            "INTEGER": "INT",
            "INT": "INT",
            "SERIAL": "INT AUTO_INCREMENT",
            "BIGSERIAL": "BIGINT AUTO_INCREMENT",
            "REAL": "FLOAT",
            "DOUBLE": "DOUBLE",
            "DOUBLE PRECISION": "DOUBLE",
            "FLOAT": "FLOAT",
            "DECIMAL": "DECIMAL",
            "NUMERIC": "DECIMAL",
            "BOOLEAN": "BOOLEAN",
            "CHAR": "CHAR",
            "CHARACTER": "CHAR",
            "VARCHAR": "VARCHAR",
            "CHARACTER VARYING": "VARCHAR",
            "TEXT": "TEXT",
            "DATE": "DATE",
            "TIME": "TIME",
            "TIMESTAMP": "DATETIME",
            "TIMESTAMPTZ": "DATETIME",
            "BYTEA": "BLOB",
            "JSON": "JSON",
            "JSONB": "JSON",
            "INET": "VARCHAR(45)",
            "CIDR": "VARCHAR(43)",
            "MACADDR": "VARCHAR(17)",
            "XML": "TEXT",
            "ENUM": "VARCHAR(255)",
            "ARRAY": "TEXT",
            "TSVECTOR": "TEXT",
        }

    def convert_data(self, column_object_type) -> str:
        for data_type, handler in self.postgre_to_mysql_map.items():
            if isinstance(column_object_type, data_type):
                return handler(column_object_type)

        data_type_upper_class = column_object_type.__class__.__name__.upper()
        return self.postgre_to_mysql_map_fallback.get(data_type_upper_class, "TEXT")

    def _handle_float(self, col) -> str:
        precision = getattr(col, "precision", None)
        if precision == 53:
            return "DOUBLE"
        return "FLOAT"

    def _handle_char(self, col) -> str:
        length = getattr(col, "length", None) or 1
        return f"CHAR({length})"

    def _handle_varchar(self, col) -> str:
        length = getattr(col, "length", None) or 255
        return f"VARCHAR({length})"

    def _handle_numeric(self, col) -> str:
        precision = getattr(col, "precision", None) or 10
        scale = getattr(col, "scale", None) or 0
        return f"DECIMAL({precision},{scale})"
