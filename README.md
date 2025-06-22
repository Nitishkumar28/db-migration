Create react app:
npm create vite@latest frontend -- --template react

Routes with functionality:
1) Get databases -  http://127.0.0.1:8000/api/databases/postgresql
2) Get tables - http://127.0.0.1:8000/api/tables/postgresql/demo
3) Get Indexes - http://127.0.0.1:8000/api/indexes/postgresql/demo/data
4) Table schema - http://127.0.0.1:8000/api/schema/postgresql/demo/conversion

1) Export Features - http://127.0.0.1:8000/api/export
2) get-history-brief - http://127.0.0.1:8000/api/migration-history-brief - list of history object in brief
3) get-history-for-job-id - http://127.0.0.1:8000/api/migration-history/{job_id} - full history object for the given jobid
4) create history object after export is clicked - http://127.0.0.1:8000/api/migration-history/create - post request_body
    - create jobid
    - source and target info
    - create a new record with these details as an initialization
5) update history object after export - http://127.0.0.1:8000/api/migration-history/{job_id} - patch request_body
    - total_time_taken
    - status of export
6) get stats - http://127.0.0.1:8000/api/get-stats - post includes request_body(source & target info) - retrieves stats and creates migration items in DB

http://127.0.0.1:8000/api/export
http://127.0.0.1:8000/api/migration-history-brief
http://127.0.0.1:8000/api/migration-history/{job_id} 
http://127.0.0.1:8000/api/migration-history/create
http://127.0.0.1:8000/api/migration-history/{job_id}
http://127.0.0.1:8000/api/get-stats

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
2) Separate the stats for source and target and eventually merge them during display

Summary table

1) Export - export_feature()
-  Request body:     {
        "source": {
            "db_type": "postgresql",
            "db_name": "demo"
        },
        "target": {
            "db_type": "mysql",
            "db_name": "demo"
        }
    }

- Returns :

return {
            "message": "Tables and triggers exported successfully.",
            "exported_tables": list(exported),
            "exported_triggers": result.get("exported", [])
            "timing": Each table timing
        }



Todos:
- Merge export return body and stats endpoint result for table execution time
- Single History page - DONE
- APIs detailing - InProgress
- API connections (expected)
- Mongo vs relational
- APIs to store and manage history 

```js

// CONNECTIONS
connections = [
    {
        "db_type": "",
        "host_name": "",
        "username": "",
        "password": "",
        "port": "",
        "db_name": "",
        "status": "idle | success | failed",
        "last_checked": "",
        "last_status_message": "",
        "tags": []
    },
    ...
]

// filter specific one from list of all connections
single_connection = {
        "db_type": "",
        "host_name": "",
        "username": "",
        "password": "",
        "port": "",
        "db_name": "",
        "status": "idle | success | failed",
        "last_checked": "",
        "last_status_message": "",
        "tags": []
    }

// EXPORT


// HISTORY CARDS
history_cards = [
    {
        "jobid": "",
        "source_db_type": "",
        "target_db_type": "",
        "source_db_name": "",
        "target_db_name": "",
        "created_at": "",
        "started_by": "",
        "status": "completed | failed | running",
    }
]

// FULL HISTORY BODY
const full_history = [
  {
    job_id: "job_001",
    source_db_type: "mysql",
    target_db_type: "postgresql",
    source_db_name: "demo",
    target_db_name: "demo",
    status: "completed",
    created_at: "2024-06-17T10:00:00Z",
    completed_at: "2024-06-17T10:10:00Z",
    total_migration_time: "10m",
    started_by: "ram",
    description: "Initial user and trigger migration",
    tags: ["user", "phase1"],
    items: [
      {
        item_id: 1,
        type: "table",
        name: "users",
        source_total_rows: 1200,
        target_total_rows: 1200,
        index_validation: "2/2",
        primary_key_validation: "1/1",
        foreign_key_validation: "1/1",
        status: "completed",
        duration: "6m",
        timestamp: "2024-06-17T10:01:00Z"
      },
    ]
  }
];

const full_history_initial = [
Add comment
More actions


  {
    job_id: "",
    source_db_type: "",
    target_db_type: "",
    source_db_name: "",
    target_db_name: "",
    status: "running",
    created_at: "",
    completed_at: "",
    started_by: "",
    description: "",
    tags: [],
    total_migration_time: "",
    items: []
  }


];





const new_job_id = "1241241" // random 6-digit number generator





// Request body


source_db_type: "postgresql",


target_db_type: "mysql",


source_db_name: "demo",


target_db_name: "demo",





// Save to DB


object.job_id = new_job_id


object.source_db_type = "postgresql"


object.target_db_type = "mysql"


...


object.save()

// AFTER create-jobid endpoint -> sample card is created -> results: true
const new_job_id = "1241241" // random 6-digit number generator
const full_history = [
  {
    job_id: new_job_id,
    source_db_type: "postgresql",
    target_db_type: "mysql",
    source_db_name: "demo",
    target_db_name: "demo",
    status: "running",
    created_at: "2024-06-17T10:00:00Z",
    completed_at: "2024-06-17T10:10:00Z",
    started_by: "",
    description: "",
    tags: [],
    total_migration_time: "",
    items: []
  }
];

// Save to DB -> app specific(Postgresql)

// EXPORT TABLES -> results: true
total_migration_time: "", // End of the export tables

// STATS -> results: true
items: []


// VALIDATION -> results: true


// Final

```

> selected source, selected target

> sourceConnectionStatus, targetConnectionStatus

> isExport = selected source + target ? true : false

> After export is clicked: 3 separate APIs
    > create-job API -> to initialize the process
    > export-features API -> to export and update complete_status
    > get-stats API -> for the current source and target

> history for jobid


[
    {
        "jobid": "job_001",
        "source_db_type": "mysql",
        "target_db_type": "postgresql",
        "source_db_name": "user_service",
        "target_db_name": "user_service_pg",
        "created_at": "2024-06-17T10:24:00Z",
        "started_by": "admin",
        "status": "completed",
    },
    ...
]

[
    {
    job_id: `job_00${i + 1}`,
    source_db_type: "mysql",
    target_db_type: "postgresql",
    source_db_name: `app_db_${i}`,
    target_db_name: `app_pg_${i}`,
    status: i % 2 === 0 ? "completed" : "failed",
    created_at: `2024-06-17T10:0${i}:00Z`,
    completed_at: `2024-06-17T10:1${i}:00Z`,
    total_migration_time: `${10 + i}m`,
    started_by: "preetham",
    description: `Migration job ${i + 1}`,
    tags: ["batch", `job_${i + 1}`],
    items: [
        {
        item_id: 1,
        type: "table",
        name: `table_${i}`,
        source_total_rows: 500 + i * 10,
        target_total_rows: 500 + i * 10,
        index_validation: "2/2",
        primary_key_validation: "1/1",
        foreign_key_validation: "1/1",
        status: "completed",
        duration: `${5 + i}m`,
        timestamp: `2024-06-17T10:0${i}:30Z`
        },
    },
    ...
  ]