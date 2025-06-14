Create react app:
npm create vite@latest frontend -- --template react

Routes with functionality:
1) Get databases -  http://127.0.0.1:8000/api/databases/postgresql
2) Get tables - http://127.0.0.1:8000/api/tables/postgresql/demo
3) Get Indexes - http://127.0.0.1:8000/api/indexes/postgresql/demo/data
4) Table schema - http://127.0.0.1:8000/api/schema/postgresql/demo/conversion
5) 


Errors:

1) Incorrect database name must raise error
2) Datatype adapter always falls back to TEXT only -- Incorrect conversion
3) Add create database function ()