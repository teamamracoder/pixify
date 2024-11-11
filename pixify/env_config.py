import environ

# Initialize environment
env = environ.Env(
    # DEBUG
    DEBUG=(bool, False),

    # SECRET KEY
    SECRET_KEY=(str, ''),

    # DB
    DATABASE_NAME=(str, ''),
    DATABASE_USER=(str, ''),
    DATABASE_PASSWORD=(str, ''),
    DATABASE_HOST=(str, ''),
    DATABASE_PORT=(str, ''),
)

env.read_env()