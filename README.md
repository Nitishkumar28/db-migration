Create react app:
npm create vite@latest frontend -- --template react

Routes with functionality:
1) Get databases -  http://127.0.0.1:8000/api/databases/postgresql
2) Get tables - http://127.0.0.1:8000/api/tables/postgresql/demo
3) Get Indexes - http://127.0.0.1:8000/api/indexes/postgresql/demo/data
4) Table schema - http://127.0.0.1:8000/api/schema/postgresql/demo/conversion


TODO:

1) check_connection() testing -  Done
2) remove table names from exportRequest and ensure all tables are taken in from the source database - Done
3) Log statement - logging module (backend)
4) Mongo DB + APIs - for storing history, credentials, other details 
5) Websockets for logs
6) Docker file

Errors:

1) Incorrect database name must raise error - Done
2) Datatype adapter always falls back to TEXT only -- Incorrect conversion -  Done
3) Primary key and foreign key -  Done
4) data type equivalents list - check accuracy - Done
5) Error handling - Done 

6) UI - Save details - Endpoints (specific)


Ideas:

1) foreign key disabling and enabling



