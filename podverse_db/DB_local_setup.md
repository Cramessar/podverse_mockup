# Podverse Database Setup Guide

This guide walks you through setting up the Podverse PostgreSQL database locally using **pgAdmin 4** and **PowerShell**. I have removed the Docker setup, so everything here assumes you are working with local PostgreSQL and pgAdmin.

---

## Prerequisites

- PostgreSQL installed locally (version 12 or higher recommended)
- pgAdmin 4 installed
- PowerShell (comes with Windows, linux users good luck...)
- The SQL initialization script located here (as an example):  
```
  `C:\Users\chris\OneDrive\Documents\GitHub\podverse_mockup\podverse_db\init_database.sql`
```

- db script pulled originally from here:
`https://github.com/podverse/podverse-ops/blob/v5-develop/database/combined/init_database.sql`
---

## Step 1: Create the Database

1. Open **pgAdmin 4**.
2. Connect to your local PostgreSQL server.
3. Right-click on `Databases` and select **Create > Database...**.
4. Name the database `podverse`.
5. Click **Save**.

---

## Step 2: Prepare Roles (Users)

The initialization script requires the following roles (users):

- `read` (with password: `your_read_password`)
- `read_write` (with password: `your_read_write_password`)

You can create these roles with the following commands in the **Query Tool** inside pgAdmin:

```sql
CREATE USER read WITH PASSWORD 'your_read_password';
CREATE USER read_write WITH PASSWORD 'your_read_write_password';
GRANT CONNECT ON DATABASE podverse TO read, read_write;
```

## Step 3: Initialize the Database Schema and Data
You can run the SQL initialization script in pgAdmin or via PowerShell.

### Option A: Using pgAdmin Query Tool
Select the podverse database.

Open the Query Tool.

Load the SQL file from:
C:\Users\chris\OneDrive\Documents\GitHub\podverse_mockup\podverse_db\init_database.sql

Execute the script.

---

### Option B: Using PowerShell and psql CLI
Open PowerShell.

Run the following command (adjust paths and user accordingly):

psql -h localhost -U postgres -d podverse -f "C:\Users\chris\OneDrive\Documents\GitHub\podverse_mockup\podverse_db\init_database.sql"

When prompted, enter your postgres user password.

---

## Step 4: Verify the Setup
Connect to the podverse database using pgAdmin or psql.

Run the following command to list tables:
```
\dt
```

You should see a list of tables like account, channel, item, etc.

You can also query sample data to verify:
```
SELECT * FROM account LIMIT 5;
```

---

## Folder Structure Reference
```
C:\Users\chris\OneDrive\Documents\GitHub\podverse_mockup\
├── podverse_db\
│   └── init_database.sql
│
└── [other project files and folders]
```

## Notes
Ensure your PostgreSQL user (postgres) has the right privileges to create roles, schemas, tables, and grants.

Passwords for roles should be securely stored and shared only with trusted team members.

If you face any permissions errors, verify your PostgreSQL user permissions or consult your database admin.

## Troubleshooting
Permission denied errors when running SQL scripts usually mean the current user lacks CREATEROLE or other privileges.

If roles read or read_write already exist, you can alter passwords instead of creating:

`ALTER USER read WITH PASSWORD 'new_password';`
`ALTER USER read_write WITH PASSWORD 'new_password';`

Make sure the SQL file path is correct and accessible when running from PowerShell.

## Summary
This guide helps your team set up the Podverse PostgreSQL database locally without Docker, relying on native PostgreSQL tools and commands. Follow the steps to get your local dev environment ready quickly.

