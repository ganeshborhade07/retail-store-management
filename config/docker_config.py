

class Dockerconfig:
    PORT = 8000
    HOST = "localhost"
    SERVER_TYPE = 'default'
    DEBUG = True
    SERVER_WORKERS = 0
    DATABASE_URL = "sqlite:///retail_db.db"
    TEST_DATABASE_URL = "sqlite:///retail_test.db"