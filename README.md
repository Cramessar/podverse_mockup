# Docker Setup & Usage for Podverse Mockup

Prerequisites
Docker and Docker Desktop installed on your machine

Get Docker for Windows, Mac, or Linux
Docker for linux...good luck
#

# Setup Instructions
1. Clone the repository, download as zip, git clone. However you want to grab the repo.

```bash
Copy
git clone https://github.com/Cramessar/podverse_mockup.git
cd podverse_mockup
```
---

2. Build Docker images

If you have Dockerfiles for backend and frontend, the db. Which you should have from the repo.

run:

```bash
Copy
docker compose up --build
```
You should now see the containers running in your docker desktop window.

---

3. Run containers
You can always click on the "play" button in docker desktop to run your containers.

Or if you are a loser and want to use a powershell terminal:

```bash
Copy
docker-compose up
```
This will start all services as defined in the compose file (frontend, backend, database, etc.).

---

# Database Setup & Initialization
If you have SQL scripts for initializing the DB schema and seeding data (e.g., init_database.sql), you can:
READ THE HOW TO DB, located in the podverse_db folder for your convienent viewing. 

Accessing the Application
Frontend: http://localhost:3000

Backend API: http://localhost:5000

Postgres DB: localhost:5432

Stopping & Cleaning Up
To stop running containers:

```bash
docker-compose down
```

Tips:
Use this to view logs:
```
docker logs <container-name>
```

Use this list all containers:
```
docker ps -a
```