# 2SDJ5-23231
Code Challenge Submission for Parstasmim .co Interview - Sahar Farahzad

## 1. Clone the Repository

To clone the repository initially:

```bash
git clone https://github.com/CodeWithSahar/2SDJ5-23231.git
cd 2SDJ5-23231
```

If you have already cloned the repository and want to update it, use:

```bash
git pull origin master
```

## 2. System Requirements

You'll need Python 3, python3-pip, python3-venv, and PostgreSQL to be installed on your machine:

## 3. PostgreSQL

If your database is not set up, you'll need to configure it. You can use your favorite PostgreSQL admin tool or the command line interface (CLI):

Windows:
Open Command Prompt or PowerShell as administrator. Navigate to the PostgreSQL bin directory:

```bash
psql -U postgres
```

Linux:
Open the terminal. Switch to the PostgreSQL superuser and open PostgreSQL CLI:

```bash
sudo -u postgres psql
```

After accessing the PostgreSQL command line, use the following SQL commands to create a user, set passwords, configure the database, and manage privileges:

```sql
-- Create the postgres user if it doesn't exist:
CREATE USER postgres WITH PASSWORD 'postgres';

-- Change the password for postgres if you get errors about wrong authentication:
ALTER USER postgres WITH PASSWORD 'postgres';

-- Create the database and give postgres the privileges:
CREATE DATABASE restaurant_db;
GRANT ALL PRIVILEGES ON DATABASE restaurant_db TO postgres;

-- Exit:
\q
```

## 4. Environment Variables Setup

To manage sensitive information like database credentials, create a `.env` file in the root directory of your project and add your database credentials.

**NOTE**: Ensure this file is kept private and not tracked by Git.

## 5. Setup

In this section we explain how you can set up the project with/without Docker.

### 5.1. With Docker

To run the application locally using Docker Compose, make sure both Docker and Docker Compose are installed on your machine.
You can manage the containers with the following commands:

```bash
# Create and run the containers, building the images before starting.
docker compose up --detach --build

# List the running containers.
docker-compose ps

# List all containers, including stopped ones.
docker-compose ps -a

# Read the logs of the running containers.
docker-compose logs

# Stop the containers.
docker-compose stop

# Stop the containers for a single service, e.g., the database.
docker-compose stop db

# Start the containers.
docker-compose start

# Start the containers for a single service, e.g., the database.
docker-compose start db

# Stop and remove the containers, including any named volumes.
# WARNING: This removes the volumes, so important data can be lost. Leave out `--volumes` if needed.
docker-compose down --volumes

# List all images created by Docker Compose.
docker-compose images

# Remove specific images by their image ID. Use -f to force removal.
docker-compose rmi -f <image_id_1> <image_id_2>
```

### 5.2. Without Docker

#### 5.2.1 Python Environment

For a clean development setup, use a virtual environment:

Windows:
```bash
cd 2SDJ5-23231
python -m venv venv
venv\Scripts\activate
```

Linux:
```bash
cd 2SDJ5-23231
python3 -m venv .venv
source .venv/bin/activate
```

**NOTE**: Ensure you add your virtual environment directory to .gitignore to avoid committing unnecessary files to your repository.

To install all requirements for local development, run the following command:

```bash
pip install -r requirements/local.txt
```

#### 5.2.2 Run Server

If you want to run the app locally, you need to execute the `migrate` command to create your database tables. Make sure you have set up your local database as described in the PostgreSQL section:

```bash
python manage.py migrate
```

Then run the following command:

```bash
python manage.py runserver
```

You can see the application in a browser, at [http://localhost:8000](http://localhost:8000).
