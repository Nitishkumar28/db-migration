import sys
import os
import pathlib

project_root = pathlib.Path(__file__).resolve().parent.parent
os.chdir(project_root)
static_dir = project_root / "static"
static_dir.mkdir(exist_ok=True)
sys.path.insert(0, str(project_root))

import pytest

from sqlalchemy.dialects.postgresql import (
    UUID as PG_UUID,
    VARCHAR as PG_VARCHAR,
    CHAR as PG_CHAR,
    TEXT as PG_TEXT,
    INTEGER as PG_INTEGER,
    SMALLINT as PG_SMALLINT,
    BIGINT as PG_BIGINT,
    NUMERIC as PG_NUMERIC,
    REAL as PG_REAL,
    DOUBLE_PRECISION as PG_DOUBLE_PRECISION,
    BYTEA as PG_BYTEA,
    JSON as PG_JSON,
    JSONB as PG_JSONB,
    TIMESTAMP as PG_TIMESTAMP,
    TIME as PG_TIME,
    DATE as PG_DATE,
    BOOLEAN as PG_BOOLEAN,
)
from sqlalchemy.types import (
    Integer as Generic_Integer,
    String as Generic_String,
    Numeric as Generic_Numeric,
    Date as Generic_Date,
    DateTime as Generic_DateTime,
    Boolean as Generic_Boolean,
    Float as Generic_Float,
    LargeBinary as Generic_LargeBinary,
    JSON as Generic_JSON,
    Time as Generic_Time,
)


from process_api import PostgresToMySQLDataTypeAdapter


@pytest.fixture
def data_adapter():
    return PostgresToMySQLDataTypeAdapter()


def test_UUID_TO_CHAR(data_adapter):
    # PG_UUID() -> CHAR(36)
    uuid_pg = PG_UUID()
    assert data_adapter.convert(uuid_pg) == "CHAR(36)"

    # UUID -> CHAR(36)
    class RelatedUUID:
        pass

    RelatedUUID.__name__ = "UUID"
    assert data_adapter.convert(RelatedUUID()) == "CHAR(36)"


def test_INTEGER_TO_INT(data_adapter):
    # PG_INTEGER() and Generic_Integer() -> INT
    assert data_adapter.convert(PG_INTEGER()) == "INT"
    assert data_adapter.convert(Generic_Integer()) == "INT"

    # INTEGER -> INT
    class RelatedInteger:
        pass

    RelatedInteger.__name__ = "INTEGER"
    assert data_adapter.convert(RelatedInteger()) == "INT"


def test_BIGINT_TO_BIGINT(data_adapter):
    # PG_BIGINT() -> BIGINT
    assert data_adapter.convert(PG_BIGINT()) == "BIGINT"

    # BIGINT -> BIGINT
    class RelatedBigInt:
        pass

    RelatedBigInt.__name__ = "BIGINT"
    assert data_adapter.convert(RelatedBigInt()) == "BIGINT"


def test_SMALLINT_TO_SMALLINT(data_adapter):
    # PG_SMALLINT() -> SMALLINT
    assert data_adapter.convert(PG_SMALLINT()) == "SMALLINT"

    # SMALLINT -> SMALLINT
    class RelatedSmallInt:
        pass

    RelatedSmallInt.__name__ = "SMALLINT"
    assert data_adapter.convert(RelatedSmallInt()) == "SMALLINT"


def test_VARCHAR(data_adapter):
    # PG_VARCHAR(50) -> VARCHAR(50)
    varchar_fifty_pg = PG_VARCHAR(length=50)
    assert data_adapter.convert(varchar_fifty_pg) == "VARCHAR(50)"

    # Generic_String(30) -> VARCHAR(30)
    string_thirty_pg = Generic_String(length=30)
    assert data_adapter.convert(string_thirty_pg) == "VARCHAR(30)"

    # Generic_String(no length) -> VARCHAR(255)
    string_pg = Generic_String()
    assert data_adapter.convert(string_pg) == "VARCHAR(255)"

    # VARCHAR -> VARCHAR(255)
    class RelatedVarchar:
        pass

    RelatedVarchar.__name__ = "VARCHAR71"
    assert data_adapter.convert(RelatedVarchar()) == "VARCHAR(255)"


def test_CHAR(data_adapter):
    # PG_CHAR(10) -> CHAR(10)
    char_ten_pg = PG_CHAR(length=10)
    assert data_adapter.convert(char_ten_pg) == "CHAR(10)"

    # CHAR -> CHAR(1)
    class RelatedChar:
        pass

    RelatedChar.__name__ = "CHAR7"
    assert data_adapter.convert(RelatedChar()) == "CHAR(1)"


def test_TEXT_TO_TEXT(data_adapter):
    # PG_TEXT() → TEXT
    assert data_adapter.convert(PG_TEXT()) == "TEXT"

    # TEXT -> TEXT
    class RelatedText:
        pass

    RelatedText.__name__ = "TEXT"
    assert data_adapter.convert(RelatedText()) == "TEXT"


def test_DATE_TO_DATE(data_adapter):
    # PG_DATE() and Generic_Date() -> DATE
    assert data_adapter.convert(PG_DATE()) == "DATE"
    assert data_adapter.convert(Generic_Date()) == "DATE"

    # DATE -> DATE
    class RelatedDate:
        pass

    RelatedDate.__name__ = "DATE"
    assert data_adapter.convert(RelatedDate()) == "DATE"


def test_TIME_TO_TIME(data_adapter):
    # PG_TIME() and Generic_Time() -> TIME
    assert data_adapter.convert(PG_TIME()) == "TIME"
    assert data_adapter.convert(Generic_Time()) == "TIME"

    # TIME -> TIME
    class RelatedTime:
        pass

    RelatedTime.__name__ = "TIME"
    assert data_adapter.convert(RelatedTime()) == "TIME"


def test_TIMESTAMP_TO_DATETIME(data_adapter):
    # PG_TIMESTAMP() and Generic_DateTime() -> DATETIME
    assert data_adapter.convert(PG_TIMESTAMP()) == "DATETIME"
    assert data_adapter.convert(Generic_DateTime()) == "DATETIME"

    # TIMESTAMP -> DATETIME
    class RelatedTimestamp:
        pass

    RelatedTimestamp.__name__ = "TIMESTAMP"
    assert data_adapter.convert(RelatedTimestamp()) == "DATETIME"


def test_BOOLEAN_TO_BOOLEAN(data_adapter):
    # PG_BOOLEAN() and Generic_Boolean() -> BOOLEAN
    assert data_adapter.convert(PG_BOOLEAN()) == "BOOLEAN"
    assert data_adapter.convert(Generic_Boolean()) == "BOOLEAN"

    # BOOLEAN -> BOOLEAN
    class RelatedBoolean:
        pass

    RelatedBoolean.__name__ = "BOOLEAN"
    assert data_adapter.convert(RelatedBoolean()) == "BOOLEAN"


def test_NUMERIC_AND_DECIMAL_TO_DECIMAL(data_adapter):
    # PG_NUMERIC(8,3) -> DECIMAL(8,3)
    pg_num = PG_NUMERIC(precision=8, scale=3)
    assert data_adapter.convert(pg_num) == "DECIMAL(8,3)"

    # Generic_Numeric(6,2) -> DECIMAL(6,2)
    gen_num = Generic_Numeric(precision=6, scale=2)
    assert data_adapter.convert(gen_num) == "DECIMAL(6,2)"

    # NUMERIC (no precision/scale) -> DECIMAL(10,0)
    class RelatedNumeric:
        pass

    RelatedNumeric.__name__ = "NUMERIC"
    assert data_adapter.convert(RelatedNumeric()) == "DECIMAL(10,0)"

    # DECIMAL (no precision/scale) -> DECIMAL(10,0)
    class RelatedDecimal:
        pass

    RelatedDecimal.__name__ = "DECIMAL"
    assert data_adapter.convert(RelatedDecimal()) == "DECIMAL(10,0)"


def test_REAL_TO_FLOAT(data_adapter):
    # PG_REAL() -> FLOAT
    assert data_adapter.convert(PG_REAL()) == "FLOAT"

    # Generic_Float(precision=24) -> "FLOAT"
    gen_float_24 = Generic_Float(precision=24)
    assert data_adapter.convert(gen_float_24) == "FLOAT"

    # REAL -> FLOAT
    class RelatedReal:
        pass

    RelatedReal.__name__ = "REAL"
    assert data_adapter.convert(RelatedReal()) == "FLOAT"

    # FLOAT -> FLOAT
    class RelatedFloatName:
        pass

    RelatedFloatName.__name__ = "FLOAT"
    assert data_adapter.convert(RelatedFloatName()) == "FLOAT"


def test_DOUBLE_PRECISION_TO_DOUBLE(data_adapter):
    # PG_DOUBLE_PRECISION() -> DOUBLE
    assert data_adapter.convert(PG_DOUBLE_PRECISION()) == "DOUBLE"

    # Generic_Float(precision=53) -> DOUBLE
    gen_float_53 = Generic_Float(precision=53)
    assert data_adapter.convert(gen_float_53) == "DOUBLE"

    # DOUBLE_PRECISION -> DOUBLE
    class RelatedDoublePrec:
        pass

    RelatedDoublePrec.__name__ = "DOUBLE_PRECISION"
    assert data_adapter.convert(RelatedDoublePrec()) == "DOUBLE"

    # DOUBLE -> DOUBLE
    class RelatedDouble:
        pass

    RelatedDouble.__name__ = "DOUBLE"
    assert data_adapter.convert(RelatedDouble()) == "DOUBLE"


def test_BYTEA_TO_BLOB(data_adapter):
    # PG_BYTEA() -> "BLOB"
    assert data_adapter.convert(PG_BYTEA()) == "BLOB"

    # Generic_LargeBinary() -> "BLOB"
    assert data_adapter.convert(Generic_LargeBinary()) == "BLOB"

    # "BYTEA" -> "BLOB"
    class RelatedBytea:
        pass

    RelatedBytea.__name__ = "BYTEA"
    assert data_adapter.convert(RelatedBytea()) == "BLOB"


def test_JSON_AND_JSONB_TO_JSON(data_adapter):
    # PG_JSON() and PG_JSONB() -> "JSON"

    assert data_adapter.convert(PG_JSON()) == "JSON"
    assert data_adapter.convert(PG_JSONB()) == "JSON"

    # Generic_JSON() -> "JSON"
    assert data_adapter.convert(Generic_JSON()) == "JSON"

    # "JSON" -> "JSON"
    class RelatedJSON:
        pass

    RelatedJSON.__name__ = "JSON"
    assert data_adapter.convert(RelatedJSON()) == "JSON"

    # "JSONB" -> "JSON"
    class RelatedJSONB:
        pass

    RelatedJSONB.__name__ = "JSONB"
    assert data_adapter.convert(RelatedJSONB()) == "JSON"


def test_FALLBACK_TO_TEXT(data_adapter):
    # Default to "TEXT" if there is an unknown type or no mapping case was matched
    class SomeUnknownType:
        pass

    SomeUnknownType.__name__ = "SOMETYPE_UNKNOWN"
    assert data_adapter.convert(SomeUnknownType()) == "TEXT"

    class AnotherType:
        pass

    assert data_adapter.convert(AnotherType()) == "TEXT"
