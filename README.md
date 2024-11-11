# Pixify

## Requirements

1. [Python](https://www.python.org/downloads/)
2. [PostgreSQL](https://www.postgresql.org/download/), just set username(deafult) = postgres ,password = 2023 ,in all places during installation
3. [Postman](https://www.postman.com/downloads/)

## Step 1: Clone Repository and Switch to new Branch

    > git clone https://token@github.com/teamamracoder/pixify.git
    > cd pixify
    > git checkout -b writeYourNewBanchName
    > code .

## Step 2: Create virtual env

    > python -m venv venv

## Step 3: Activate Virtual env

    > .\venv\Scripts\activate
    -if Execution Policy Error
        -open windows powershell as Admin and run this command
            > Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
        - retry Step 3

## Step 4: Install packages

    > pip install -r requirements.txt

## Step 5: Database Setup

    - Open pgAdmin4
    - if you have a database named 'pixify', then delete
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

## Step 6: Migrate

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

## Step 7: Run the server

    > python manage.py runserver
