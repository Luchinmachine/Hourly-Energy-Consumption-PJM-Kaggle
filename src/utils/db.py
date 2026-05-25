from sqlalchemy import create_engine
from src.config import DB_CONFIG

def get_engine():
    connection_string = (
        f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['name']}"
    )
    return create_engine(connection_string)