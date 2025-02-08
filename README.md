# 2SDJ5-23231
Code Challenge Submission for Parstasmim .co Interview - Sahar Farahzad

## 1. Project Description
This project implements a booking system for a restaurant using Django and PostgreSQL. The system allows users to book tables and cancel reservations. Authentication is required for these actions. The booking logic ensures the best price for users based on seat or table availability.

### Business Logic
1. The restaurant has **10 tables**, each with a minimum of **4 seats** and a maximum of **10 seats**.
2. Users specify the number of people for the reservation, and the system allocates seats/tables at the cheapest price.
3. If a user requests an odd number of seats (e.g., 3), the system automatically books 4 seats and calculates the cost for 4 seats.
4. Each seat costs **X** amount, while booking an entire table costs **(M - 1) * X** amount.
5. Users must be authenticated to perform the following actions:
    - **Action 1**: `/book` API returns reservation details (cost, table ID, and number of seats).
    - **Action 2**: `/cancel` API cancels a reservation.

## 2. Clone the Repository

To clone the repository initially:

```bash
git clone https://github.com/CodeWithSahar/2SDJ5-23231.git
cd 2SDJ5-23231
```

If you have already cloned the repository and want to update it, use:

```bash
git pull origin master
```

## 3. System Requirements
- Python 3
- python3-pip
- python3-venv
- PostgreSQL
- Docker (optional)

## 4. PostgreSQL

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

## 5. Environment Variables Setup

To manage sensitive information like database credentials, create a `.env` file in the root directory of your project and add your database credentials.

**NOTE**: Ensure this file is kept private and not tracked by Git.

## 6. Setup

In this section we explain how you can set up the project with/without Docker.

### 6.1. With Docker

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

### 6.2. Without Docker

#### 6.2.1 Python Environment

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

#### 6.2.2 Run Server

If you want to run the app locally, you need to execute the `migrate` command to create your database tables. Make sure you have set up your local database as described in the PostgreSQL section:

```bash
python manage.py migrate
```

Then run the following command:

```bash
python manage.py runserver
```

You can see the application in a browser, at [http://localhost:8000](http://localhost:8000).

## 7. API Documentation 

The API documentation is available at `/api/schema/swagger-ui/`. You can use Swagger UI to explore and test all available endpoints.

### Authentication in Swagger UI

After registering a new user and logging in, you will receive an `access` token in the response. To test protected endpoints:
1. Copy the `access` token from the response.
2. Click on the `Authorize` button in the top-right corner of Swagger UI.
3. Paste the token.
4. Click `Authorize` to authenticate and access the protected APIs.

### Email Verification  

After registering a new user, a confirmation email will be printed in the terminal. This email will contain a verification link. Copy the code after `/dj-rest-auth/registration/account-confirm-email/` from the link and use it in the `/dj-rest-auth/registration/verify-email/` endpoint as the key to complete the email verification process.

## 8. Running Tests

To run all tests, make sure you have your environment set up and run the following command:
```bash
pytest 
```
