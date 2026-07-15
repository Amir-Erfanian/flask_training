import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

print("=== Testing Configuration ===")
print(f"SECRET_KEY: {os.environ.get('SECRET_KEY')}")
print(f"DATABASE_URL: {os.environ.get('DATABASE_URL')}")
print()

connection_string = os.environ.get('DATABASE_URL')

try:
    engine = create_engine(connection_string)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT @@VERSION"))
        version = result.fetchone()[0]
        print("✅ CONNECTION SUCCESSFUL!")
        print(f"SQL Server: {version[:50]}...")
        
        result = conn.execute(text("SELECT DB_NAME()"))
        db_name = result.fetchone()[0]
        print(f"Database: {db_name}")
        
except Exception as e:
    print(f"❌ Connection failed: {e}")