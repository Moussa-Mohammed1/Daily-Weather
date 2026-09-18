from src.load.connection import engine
from sqlalchemy import text

def test_database_connection():
    with engine.connect() as connection:
      
        result = connection.execute(text("SELECT * FROM cities"))
        print(result.fetchone())