# Pixify

## Requirements

1. [Python](https://www.python.org/downloads/)
2. [PostgreSQL](https://www.postgresql.org/download/), just set username(deafult) = postgres ,password = 2023 ,in all places during installation
3. [Postman](https://www.postman.com/downloads/)

## Step 1: Clone Repository and Switch to new Branch

    > git clone https://token@github.com/teamamracoder/pixify.git
    > git checkout -b writeYourNewBanchName

## Step 2: Navigate to Directory

    > cd pixify

## Step 3: Create virtual env

    > python -m venv venv

## Step 4: Activate Virtual env

    > .\venv\Scripts\activate
    -if Execution Policy Error
        -open windows powershell as Admin and run this command
            > Set-ExecutionPolicy Unrestricted -Force
        - retry Step 4

## Step 5: Install packages

    > pip install -r requirements.txt

## Step 6: Database Setup

    - Open pgAdmin4
    - create database 'pixify'
    - make sure you have set password = 2023 ,for default user 'postgres' while installing and setting up postgresSQL database
        - if not then open query tool on the database 'pixify' and run below commands
            - if username is correct and password is wrong 
                > ALTER USER postgres WITH PASSWORD '2023';
            - if username is no correct
                > CREATE USER postgres WITH PASSWORD '2023';
                > GRANT ALL PRIVILEGES ON DATABASE pixify TO postgres;
                > ALTER DATABASE pixify OWNER TO postgres;
                > REVOKE ALL PRIVILEGES ON DATABASE pixify FROM postgres;

## Step 7: Migrate

    > cd pixify
    > python manage.py makemigrations social_network
    - if error reagarding psycopg,
        -step 6.1: uninstall psycopg
            > pip uninstall psycopg
        -step 6.2: install psycopg-binanry
            > pip install "psycopg[binary]"
        -step 6.3: run the migration command again
            > python manage.py makemigrations social_network

    > python manage.py migrate

## Step 8: Run the server

    > python manage.py runserver
