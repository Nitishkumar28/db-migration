Create react app:
npm create vite@latest frontend -- --template react

Routes with functionality:
1) Get databases -  http://127.0.0.1:8000/api/databases/postgresql
2) Get tables - http://127.0.0.1:8000/api/tables/postgresql/demo
3) Get Indexes - http://127.0.0.1:8000/api/indexes/postgresql/demo/data
4) Table schema - http://127.0.0.1:8000/api/schema/postgresql/demo/conversion


Errors:

1) Incorrect database name must raise error - Done
2) Datatype adapter always falls back to TEXT only -- Incorrect conversion -  Done
3) Primary key and foreign key -  Done
4) data type equivalents list - check accuracy - Done
5) Error handling 

6) UI - Save details - Endpoints (specific)


Ideas:

1) foreign key disabling and enabling


Data types not available within the library:

1) MONEY
2) SMALLSERIAL
3) SERIAL
4) POINT
5) LINE
6) LSEG
7) BOX
8) PATH
9) POLYGON
10) CIRCLE
11) TXID_SNAPSHOT

