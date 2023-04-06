import pathlib
import os

PROJECT_PATH = pathlib.Path(__file__).parent.parent
ENVIRONMENT = os.getenv('ENV') or "dev"

DB_URI = {
    'drivername': 'mysql+pymysql',
    'username': os.getenv('RDS_USERNAME') or 'root',
    'password': os.getenv('RDS_PASSWORD') or 'root',
    'host': os.getenv('RDS_HOSTNAME') or 'localhost',
    'port': os.getenv('RDS_PORT') or 3306,
    'database': 'highlite',
}
