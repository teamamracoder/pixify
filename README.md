# Pixify

## Clone Repo

    'https://token@github.com/teamamracoder/pixify.git

## Navigate to Directory

    > cd pixify

## Create virtual env

    > python -m venv venv

## Activate Virtual env

    > .\venv\Scripts\activate
    -if Execution Policy Error
        -open windows powershell as Admin and run this command
            > Set-ExecutionPolicy Unrestricted -Force
        - then try the activate command again

## Install packages

    > pip install -r requirements.txt

## Migrate

    > cd pixify
    > python manage.py makemigrations social_network
    - if error in psycopg,
        -step 1: uninstall psycopg
            > pip uninstall psycopg
        -step 2: install psycopg-binanry
            > pip install "psycopg[binary]"
        -step 3: run the migration command again

    > python manage.py migrate

- Run the server
    > python manage.py runserver

## Make Sure to make separate branch and navigate to that branch before commiting any changes
