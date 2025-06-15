import os

class Config:
    MYSQL_HOST = os.environ.get("DB_HOST", "localhost")
    MYSQL_USER = os.environ.get("DB_USER", "root")
    MYSQL_PASSWORD = os.environ.get("DB_PASSWORD", "")
    MYSQL_DB = os.environ.get("DB_NAME", "nama_database")
