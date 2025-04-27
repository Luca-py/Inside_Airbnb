from dotenv import load_dotenv
import sqlalchemy as db
import os
import pandas as pd

# Database connection
# Load the .env file
load_dotenv()

# Extract each part of the DB config
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Construct the DB URL manually
db_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the engine
engine = db.create_engine(db_url)

# Create a connection
conn = engine.connect()

# Load data
listings = pd.read_sql_table('listings', conn)
reviews = pd.read_sql_table('reviews', conn)

# Create exports directory if it doesn't exist
os.makedirs('exports', exist_ok=True)

# Export full data
print("Exporting full datasets...")
listings.to_csv('exports/listings_full.csv', index=False)
reviews.to_csv('exports/reviews_full.csv', index=False)

print(f"Export complete! Files saved to 'exports' directory")

conn.close()
