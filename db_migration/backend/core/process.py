from sqlalchemy import column

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
    BIT as Postgre_BIT,
    CIDR as Postgre_CIDR,
    INET as Postgre_INET,
    MACADDR as Postgre_MACADDR,
    TSVECTOR as Postgre_TSVEC,
    TSQUERY as Postgre_TSQUR,
    ARRAY as Postgre_ARR,   
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
            PostGre_SMALLINT: lambda col: "SMALLINT",
            PostGre_BIGINT: lambda col: "BIGINT",
            PostGre_INTEGER: lambda col: "INT", 
            Gen_Integer: lambda col: "INT",
            Postgre_BIT: lambda col: "BIT",
            PostGre_BOOLEAN: lambda col: "BOOLEAN",
            Gen_Boolean: lambda col: "BOOLEAN",
            PostGre_REAL: lambda col: "FLOAT",
            PostGre_DOUBLE_PRECISION: lambda col: "DOUBLE",
            PostGre_NUMERIC: self._handle_numeric,
            Gen_Numeric: self._handle_numeric,
            PostGre_CHAR: self._handle_char,
            PostGre_VARCHAR: self._handle_varchar,
            Gen_String: self._handle_varchar,
            PostGre_DATE: lambda col: "DATE",
            Gen_Date: lambda col: "DATE",
            PostGre_TIME: lambda col: "TIME",
            Gen_Time: lambda col: "TIME",
            PostGre_TIMESTAMP: lambda col: "DATETIME",
            Gen_DateTime: lambda col: "DATETIME",
            PostGre_BYTEA: lambda col: "BLOB",
            PostGre_TEXT: lambda col: "LONGTEXT",
            Postgre_CIDR: self._handle_varchar,
            Postgre_INET: self._handle_varchar,
            Postgre_MACADDR: self._handle_varchar,
            PostGre_UUID: lambda col: "VARCHAR(36)",
            Gen_Float: self._handle_float,
            PostGre_JSON: lambda col: "LONGTEXT",
            Postgre_TSVEC: lambda col: "LONGTEXT",
            Postgre_TSQUR: lambda col: "LONGTEXT",
            Postgre_ARR: lambda col: "LONGTEXT",
            Gen_LargeBinary: lambda col: "LONGBLOB",
            PostGre_JSONB: lambda col: "LONGTEXT",
            Gen_JSON: lambda col: "LONGTEXT"
        }

        self.postgre_to_mysql_map_fallback = {
            "SMALLINT": "SMALLINT",
            "BIGINT": "BIGINT",
            "INTEGER": "INT",
            "INT": "INT",
            "SERIAL": "INT AUTO_INCREMENT",
            "SMALLSERIAL": "SMALLINT AUTO_INCREMENT",
            "BIGSERIAL": "BIGINT AUTO_INCREMENT",
            "BIT": "BIT",   
            "BOOLEAN": "TINYINT(1)",
            "REAL": "FLOAT",
            "FLOAT": "FLOAT",
            "DOUBLE PRECISION": "DOUBLE",
            "NUMERIC": "DECIMAL",
            "DECIMAL": "DECIMAL",
            "MONEY": "DECIMAL(19,2)",
            "CHAR": "CHAR",
            "CHARACTER": "CHAR",
            "VARCHAR": "VARCHAR",
            "CHARACTER VARYING": "VARCHAR",
            "DATE": "DATE",
            "TIME": "TIME",
            "TIMESTAMP": "DATETIME",
            "INTERVAL": "TIME",
            "BYTEA": "LONGBLOB",
            "TEXT": "LONGTEXT",
            "CIDR": "VARCHAR(43)",
            "INET": "VARCHAR(43)",
            "MACADDR": "VARCHAR(17)",
            "UUID": "VARCHAR(36)",
            "XML": "LONGTEXT",
            "JSON": "LONGTEXT",
            "TSVECTOR": "LONGTEXT",
            "TSQUERY": "LONGTEXT",
            "ARRAY": "LONGTEXT",
            "POINT": "POINT",
            "LINE": "LINESTRING",
            "LSEG": "LINESTRING",
            "BOX": "POLYGON",
            "PATH": "LINESTRING",
            "POLYGON": "POLYGON",
            "CIRCLE": "POLYGON",
            "TXID_SNAPSHOT": "VARCHAR",
            "JSONB": "LONGTEXT",
            "ENUM": "VARCHAR(255)",
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
