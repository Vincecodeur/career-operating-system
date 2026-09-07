from sqlalchemy import text
from app.core.database import engine

query = """SELECT setting_key, setting_value FROM application_settings ORDER BY setting_key"""

with engine.connect() as connection:
    result = connection.execute(text(query))
    for row in result:
        print(row[0], "=", row[1])
