import sys
import os
import pathlib

project_root = pathlib.Path(__file__).resolve().parent.parent
os.chdir(project_root)
static_dir = project_root / "static"
static_dir.mkdir(exist_ok=True)
sys.path.insert(0, str(project_root))

import pytest

# Better Type Detection
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
    INTERVAL as PostGre_INTERVAL,
    ENUM as PostGre_ENUM,
    MONEY as PostGre_MONEY,
    OID as PostGre_OID,
    BIT as PostGre_BIT,
    ARRAY as PostGre_ARRAY,
    INT4RANGE as PostGre_INT4RANGE,
    INT4MULTIRANGE as PostGre_INT4MULTIRANGE,
    INT8RANGE as PostGre_INT8RANGE,
    INT8MULTIRANGE as PostGre_INT8MULTIRANGE,
    TSRANGE as PostGre_TSRANGE,
    TSTZRANGE as PostGre_TSTZRANGE,
    TSTZMULTIRANGE as PostGre_TSTZMULTIRANGE,
    DATERANGE as PostGre_DATERANGE,
    TSVECTOR as PostGre_TSVECTOR,
    TSQUERY as PostGre_TSQUERY,
    INET as PostGre_INET,
    CIDR as PostGre_CIDR,
    MACADDR as PostGre_MACADDR,
    MACADDR8 as PostGre_MACADDR8,
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


from process_api import PostgresToMySQLDataTypeAdapter


@pytest.fixture
def data_adapter():
    return PostgresToMySQLDataTypeAdapter()


def test_UUID_TO_CHAR(data_adapter):
    # PG_UUID() -> CHAR(36)
    uuid_pg = PostGre_UUID()
    assert data_adapter.convert_data(uuid_pg) == "CHAR(36)"

    # UUID -> CHAR(36)
    class RelatedUUID:
        pass

    RelatedUUID.__name__ = "UUID"
    assert data_adapter.convert_data(RelatedUUID()) == "CHAR(36)"


def test_INTEGER_TO_INT(data_adapter):
    # PG_INTEGER() and Generic_Integer() -> INT
    assert data_adapter.convert_data(PostGre_INTEGER()) == "INT"
    assert data_adapter.convert_data(Gen_Integer()) == "INT"

    # INTEGER -> INT
    class RelatedInteger:
        pass

    RelatedInteger.__name__ = "INTEGER"
    assert data_adapter.convert_data(RelatedInteger()) == "INT"


def test_BIGINT_TO_BIGINT(data_adapter):
    # PG_BIGINT() -> BIGINT
    assert data_adapter.convert_data(PostGre_BIGINT()) == "BIGINT"

    # BIGINT -> BIGINT
    class RelatedBigInt:
        pass

    RelatedBigInt.__name__ = "BIGINT"
    assert data_adapter.convert_data(RelatedBigInt()) == "BIGINT"


def test_SMALLINT_TO_SMALLINT(data_adapter):
    # PG_SMALLINT() -> SMALLINT
    assert data_adapter.convert_data(PostGre_SMALLINT()) == "SMALLINT"

    # SMALLINT -> SMALLINT
    class RelatedSmallInt:
        pass

    RelatedSmallInt.__name__ = "SMALLINT"
    assert data_adapter.convert_data(RelatedSmallInt()) == "SMALLINT"


def test_VARCHAR(data_adapter):
    # PG_VARCHAR(50) -> VARCHAR(50)
    varchar_fifty_pg = PostGre_VARCHAR(length=50)
    assert data_adapter.convert_data(varchar_fifty_pg) == "VARCHAR(50)"

    # Generic_String(30) -> VARCHAR(30)
    string_thirty_pg = Gen_String(length=30)
    assert data_adapter.convert_data(string_thirty_pg) == "VARCHAR(30)"

    # Generic_String(no length) -> VARCHAR(255)
    string_pg = Gen_String()
    assert data_adapter.convert_data(string_pg) == "VARCHAR(255)"

    # VARCHAR -> VARCHAR(255)
    class RelatedVarchar:
        pass

    RelatedVarchar.__name__ = "VARCHAR71"
    assert data_adapter.convert_data(RelatedVarchar()) == "VARCHAR(255)"


def test_CHAR(data_adapter):
    # PG_CHAR(10) -> CHAR(10)
    char_ten_pg = PostGre_CHAR(length=10)
    assert data_adapter.convert_data(char_ten_pg) == "CHAR(10)"

    # CHAR -> CHAR(1)
    class RelatedChar:
        pass

    RelatedChar.__name__ = "CHAR7"
    assert data_adapter.convert_data(RelatedChar()) == "CHAR(1)"


def test_TEXT_TO_TEXT(data_adapter):
    # PG_TEXT() → TEXT
    assert data_adapter.convert_data(PostGre_TEXT()) == "TEXT"

    # TEXT -> TEXT
    class RelatedText:
        pass

    RelatedText.__name__ = "TEXT"
    assert data_adapter.convert_data(RelatedText()) == "TEXT"


def test_DATE_TO_DATE(data_adapter):
    # PG_DATE() and Generic_Date() -> DATE
    assert data_adapter.convert_data(PostGre_DATE()) == "DATE"
    assert data_adapter.convert_data(Gen_Date()) == "DATE"

    # DATE -> DATE
    class RelatedDate:
        pass

    RelatedDate.__name__ = "DATE"
    assert data_adapter.convert_data(RelatedDate()) == "DATE"


def test_TIME_TO_TIME(data_adapter):
    # PG_TIME() and Generic_Time() -> TIME
    assert data_adapter.convert_data(PostGre_TIME()) == "TIME"
    assert data_adapter.convert_data(Gen_Time()) == "TIME"

    # TIME -> TIME
    class RelatedTime:
        pass

    RelatedTime.__name__ = "TIME"
    assert data_adapter.convert_data(RelatedTime()) == "TIME"


def test_TIMESTAMP_TO_DATETIME(data_adapter):
    # PG_TIMESTAMP() and Generic_DateTime() -> DATETIME
    assert data_adapter.convert_data(PostGre_TIMESTAMP()) == "DATETIME"
    assert data_adapter.convert_data(Gen_DateTime()) == "DATETIME"

    # TIMESTAMP -> DATETIME
    class RelatedTimestamp:
        pass

    RelatedTimestamp.__name__ = "TIMESTAMP"
    assert data_adapter.convert_data(RelatedTimestamp()) == "DATETIME"


def test_BOOLEAN_TO_BOOLEAN(data_adapter):
    # PG_BOOLEAN() and Generic_Boolean() -> BOOLEAN
    assert data_adapter.convert_data(PostGre_BOOLEAN()) == "BOOLEAN"
    assert data_adapter.convert_data(Gen_Boolean()) == "BOOLEAN"

    # BOOLEAN -> BOOLEAN
    class RelatedBoolean:
        pass

    RelatedBoolean.__name__ = "BOOLEAN"
    assert data_adapter.convert_data(RelatedBoolean()) == "BOOLEAN"


def test_NUMERIC_AND_DECIMAL_TO_DECIMAL(data_adapter):
    # PG_NUMERIC(8,3) -> DECIMAL(8,3)
    pg_num = PostGre_NUMERIC(precision=8, scale=3)
    assert data_adapter.convert_data(pg_num) == "DECIMAL(8,3)"

    # Generic_Numeric(6,2) -> DECIMAL(6,2)
    gen_num = Gen_Numeric(precision=6, scale=2)
    assert data_adapter.convert_data(gen_num) == "DECIMAL(6,2)"

    # NUMERIC (no precision/scale) -> DECIMAL(10,0)
    class RelatedNumeric:
        pass

    RelatedNumeric.__name__ = "NUMERIC"
    assert data_adapter.convert_data(RelatedNumeric()) == "DECIMAL(10,0)"

    # DECIMAL (no precision/scale) -> DECIMAL(10,0)
    class RelatedDecimal:
        pass

    RelatedDecimal.__name__ = "DECIMAL"
    assert data_adapter.convert_data(RelatedDecimal()) == "DECIMAL(10,0)"


def test_REAL_TO_FLOAT(data_adapter):
    # PG_REAL() -> FLOAT
    assert data_adapter.convert_data(PostGre_REAL()) == "FLOAT"

    # Generic_Float(precision=24) -> "FLOAT"
    gen_float_24 = Gen_Float(precision=24)
    assert data_adapter.convert_data(gen_float_24) == "FLOAT"

    # REAL -> FLOAT
    class RelatedReal:
        pass

    RelatedReal.__name__ = "REAL"
    assert data_adapter.convert_data(RelatedReal()) == "FLOAT"

    # FLOAT -> FLOAT
    class RelatedFloatName:
        pass

    RelatedFloatName.__name__ = "FLOAT"
    assert data_adapter.convert_data(RelatedFloatName()) == "FLOAT"


def test_DOUBLE_PRECISION_TO_DOUBLE(data_adapter):
    # PG_DOUBLE_PRECISION() -> DOUBLE
    assert data_adapter.convert_data(PostGre_DOUBLE_PRECISION()) == "DOUBLE"

    # Generic_Float(precision=53) -> DOUBLE
    gen_float_53 = Gen_Float(precision=53)
    assert data_adapter.convert_data(gen_float_53) == "DOUBLE"

    # DOUBLE_PRECISION -> DOUBLE
    class RelatedDoublePrec:
        pass

    RelatedDoublePrec.__name__ = "DOUBLE_PRECISION"
    assert data_adapter.convert_data(RelatedDoublePrec()) == "DOUBLE"

    # DOUBLE -> DOUBLE
    class RelatedDouble:
        pass

    RelatedDouble.__name__ = "DOUBLE"
    assert data_adapter.convert_data(RelatedDouble()) == "DOUBLE"


def test_BYTEA_TO_BLOB(data_adapter):
    # PG_BYTEA() -> "BLOB"
    assert data_adapter.convert_data(PostGre_BYTEA()) == "BLOB"

    # Generic_LargeBinary() -> "BLOB"
    assert data_adapter.convert_data(Gen_LargeBinary()) == "BLOB"

    # "BYTEA" -> "BLOB"
    class RelatedBytea:
        pass

    RelatedBytea.__name__ = "BYTEA"
    assert data_adapter.convert_data(RelatedBytea()) == "BLOB"


def test_JSON_AND_JSONB_TO_JSON(data_adapter):
    # PG_JSON() and PG_JSONB() -> "JSON"

    assert data_adapter.convert_data(PostGre_JSON()) == "JSON"
    assert data_adapter.convert_data(PostGre_JSONB()) == "JSON"

    # Generic_JSON() -> "JSON"
    assert data_adapter.convert_data(Gen_JSON()) == "JSON"

    # "JSON" -> "JSON"
    class RelatedJSON:
        pass

    RelatedJSON.__name__ = "JSON"
    assert data_adapter.convert_data(RelatedJSON()) == "JSON"

    # "JSONB" -> "JSON"
    class RelatedJSONB:
        pass

    RelatedJSONB.__name__ = "JSONB"
    assert data_adapter.convert_data(RelatedJSONB()) == "JSON"


def test_ARRAY_TO_JSON(data_adapter):
    # ARRAY -> JSON
    assert data_adapter.convert_data(PostGre_ARRAY(PostGre_INTEGER())) == "JSON"

    class RelatedArr:
        pass

    RelatedArr.__name__ = "ARRAY"
    assert data_adapter.convert_data(RelatedArr()) == "JSON"


def test_RANGE_TO_JSON(data_adapter):
    # INT4RANGE/INT8RANGE/TSRANGE/TSTZRANGE/DATERANGE -> JSON
    for each_type in (PostGre_INT4RANGE(), PostGre_INT8RANGE(), PostGre_TSRANGE(), PostGre_TSTZRANGE(), PostGre_DATERANGE()):
        assert data_adapter.convert_data(each_type) == "JSON"

    class RelatedRange: 
        pass

    RelatedRange.__name__ = "TSRANGE"
    assert data_adapter.convert_data(RelatedRange()) == "JSON"


def test_MULTIRANGE_TO_JSON(data_adapter):
    # INT4MULTIRANGE/INT8MULTIRANGE/TSTZMULTIRANGE -> JSON
    for each_type in (PostGre_INT4MULTIRANGE(), PostGre_INT8MULTIRANGE(), PostGre_TSTZMULTIRANGE()):
        assert data_adapter.convert_data(each_type) == "JSON"

    class RelatedMR: 
        pass

    RelatedMR.__name__ = "INT8MULTIRANGE"
    assert data_adapter.convert_data(RelatedMR()) == "JSON"


def test_NETWORK_TO_VARCHAR(data_adapter):
    # INET / CIDR -> VARCHAR(45)
    assert data_adapter.convert_data(PostGre_INET()) == "VARCHAR(45)"
    assert data_adapter.convert_data(PostGre_CIDR()) == "VARCHAR(45)"

    class RelatedNet:
        pass

    RelatedNet.__name__ = "INET"
    assert data_adapter.convert_data(RelatedNet()) == "VARCHAR(45)"


def test_MACADDR_TO_VARBINARY(data_adapter):
    # MACADDR/MACADDR8 -> VARBINARY(6)
    assert data_adapter.convert_data(PostGre_MACADDR()) == "VARBINARY(6)"
    assert data_adapter.convert_data(PostGre_MACADDR8()) == "VARBINARY(6)"

    class RelatedMac: 
        pass

    RelatedMac.__name__ = "MACADDR"
    assert data_adapter.convert_data(RelatedMac()) == "VARBINARY(6)"


def test_FULLTEXT_TO_TEXT(data_adapter):
    # TSVECTOR/TSQUERY -> TEXT
    assert data_adapter.convert_data(PostGre_TSVECTOR()) == "TEXT"
    assert data_adapter.convert_data(PostGre_TSQUERY()) == "TEXT"

    class RelatedFullText: 
        pass

    RelatedFullText.__name__ = "TSVECTOR"
    assert data_adapter.convert_data(RelatedFullText()) == "TEXT"


def test_BIT_TO_BIT(data_adapter):
    # BIT(n) -> BIT(n)
    assert data_adapter.convert_data(PostGre_BIT(8)) == "BIT(8)"
    assert data_adapter.convert_data(PostGre_BIT()) == "BIT(1)"

    class RelatedBit: 
        pass

    RelatedBit.__name__ = "BIT"
    assert data_adapter.convert_data(RelatedBit()) == "BIT(1)"


def test_ENUM_TO_VARCHAR(data_adapter):
    # ENUM -> VARCHAR(255)
    assert data_adapter.convert_data(PostGre_ENUM("a","b")) == "VARCHAR(255)"

    class RelatedEnum:
        pass

    RelatedEnum.__name__ = "ENUM"
    assert data_adapter.convert_data(RelatedEnum()) == "VARCHAR(255)"


def test_INTERVAL_TO_TIME(data_adapter):
    # INTERVAL -> TIME 
    assert data_adapter.convert_data(PostGre_INTERVAL()) == "TIME"

    class RelatedInt: 
        pass

    RelatedInt.__name__ = "INTERVAL"
    assert data_adapter.convert_data(RelatedInt()) == "TIME"


def test_MONEY_TO_DECIMAL(data_adapter):
    # MONEY -> DECIMAL(19,4)
    assert data_adapter.convert_data(PostGre_MONEY()) == "DECIMAL(19,4)"

    class RelatedMoney: 
        pass

    RelatedMoney.__name__ = "MONEY"
    assert data_adapter.convert_data(RelatedMoney()) == "DECIMAL(19,4)"


def test_OID_TO_INT_UNSIGNED(data_adapter):
    # OID -> INT UNSIGNED
    assert data_adapter.convert_data(PostGre_OID()) == "INT UNSIGNED"

    class RelatedOID: 
        pass

    RelatedOID.__name__ = "OID"
    assert data_adapter.convert_data(RelatedOID()) == "INT UNSIGNED"


def test_FALLBACK_TO_TEXT(data_adapter):
    # Default to "TEXT" if there is an unknown type or no mapping case was matched
    class SomeUnknownType:
        pass

    SomeUnknownType.__name__ = "SOMETYPE_UNKNOWN"
    assert data_adapter.convert_data(SomeUnknownType()) == "TEXT"

    class AnotherType:
        pass

    assert data_adapter.convert_data(AnotherType()) == "TEXT"
    