### Database Migration Tool

## Overview:
The database migration tool is designed to support and automate the task of migration across various relational databases. It serves as a simple stop solution, easing out the process of migration by analyzing the intricate details of a database schema and efficiently transferring all the individual elements of a database architecture. The tool supports connectivity with any relational database and exporting them from their respective source to target destinations while handling the load efficiently and at the same time ensuring that the process of migration, ranging from the creation of table schemas to the insertion of data records is handled smoothly. It is also built with a clean and interactive user interface, offering users a concise and focused summary that can be reviewed, ensuring transparency and ease of validation as an outcome of the migration task.


## Technologies/Frameworks:
Backend: Python, FastAPI
Frontend: HTML, CSS, React(JavaScript)
Databases: SQLite


## Features:

# Frontend
1. User Authentication: Providing a secure authentication system that allows both user signup and login. This ensures that only authorized personnel can get access to the platform to perform migration operations and track the relevant summary data.

2. Database Connection Testing: The application allows users to check and validate connections with their source and target before initiating a database migration. It helps in ensuring that the required database is configured correctly on both ends, leading to smooth and easy operations.

3. Export Dashboard: An interactive interface providing users with a graphical representation of their source and target relations database management system, and embedded with an option to initiate the process of migration. The dashboard also presents a concise summary of completed migration cards, including a detailed summary of all the components that were successfully migrated for user validation.


# Backend
1. Table schema and structure migration: Enabling the automatic extraction of source tables and recreating the same table definitions in target including the specifications of columns and constraints guaranteeing the reflection of the same structural consistency across the source and target databases.

2. Data type mapping and conversion: Handling the conversion between the differing data types across the source and target database systems. The implementation of a custom data mapping ensures maintaining the data integrity and compatibility during the process of migration.

3. Table data records transfer: Supporting the transfers of row level data from tables through the process of loading and writing them as dataframes enabling the management of large table records.

4. Index migration: Replicating the index creation from the source to the target database to maintain query performance post the migration task. This includes primary, unique, and composite indexes.

5. Relational integrity preserver: Migrating the primary and foreign key relationships retaining the referential integrity in the target schema and securing all the data dependencies and constraints.

6. Triggers syncing: Identifying and transferring compatible database triggers from the source to the target supporting the system with a consistent and aligned trigger functionality.

