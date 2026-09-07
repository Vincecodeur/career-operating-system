from sqlalchemy import text
from app.core.database import engine

query = """SELECT table_name FROM information_schema.tables WHERE table_name IN ('user_settings', 'saved_searches', 'application_settings')"""

with engine.connect() as connection:
    result = connection.execute(text(query))
    for row in result:
        print(row[0])
