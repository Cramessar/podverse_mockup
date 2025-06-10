How to Connect to Your Docker PostgreSQL Database and Verify Data
1. Connect to Your Backend Docker Container
Open your terminal and run:

bash
Copy
docker exec -it podverse_backend sh
This opens an interactive shell inside the backend container.

Make sure your backend container is running. If not, start it with:

bash
Copy
docker-compose up -d
2. Login to the PostgreSQL Database Inside the Container
Once inside the container shell, use the psql command-line tool to connect to the database:

bash
Copy
psql -h database -U podverse_admin -d podverse_db
-h database points to the hostname of your PostgreSQL service in Docker Compose.

-U podverse_admin specifies the PostgreSQL username.

-d podverse_db specifies the database name.

You will be prompted for the password. Enter the password you configured in your .env or Docker Compose file (e.g., testest).

If you see this prompt:

makefile
Copy
podverse_db=#
You’re connected successfully!

3. Run SQL Queries to Check Your Data
Check how many rows are in a table (e.g., account):
sql
Copy
SELECT COUNT(*) FROM account;
Example output:

markdown
Copy
 count
-------
   200
(1 row)
View sample data from the table:
sql
Copy
SELECT * FROM account LIMIT 5;
This shows the first 5 rows of the account table.

4. Exit the PostgreSQL Console and Docker Container
To exit the PostgreSQL prompt, type:

sql
Copy
\q
To exit the Docker container shell, type:

bash
Copy
exit
Summary
Connect to Docker backend container with docker exec.

Login to PostgreSQL inside container with psql.

Run SQL queries to verify tables and data.

Exit cleanly when done.