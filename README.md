# Pixify

## Requirements

1. [Python](https://www.python.org/downloads/)
2. [PostgreSQL](https://www.postgresql.org/download/)
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
