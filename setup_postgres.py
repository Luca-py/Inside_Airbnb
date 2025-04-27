import pandas as pd
import sqlalchemy as db
import os
from dotenv import load_dotenv

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

# Test the connection
print("Connection successful")

metadata = db.MetaData()

# Create a table for the listings
listings_table = db.Table("listings", metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("name", db.String(200)),
    db.Column("host_id", db.Integer),
    db.Column("host_name", db.String(100)),
    db.Column("neighbourhood_group", db.String(100)),
    db.Column("neighbourhood", db.String(100)),
    db.Column("latitude", db.Float),
    db.Column("longitude", db.Float),
    db.Column("room_type", db.String(50)),
    db.Column("price", db.Float),
    db.Column("minimum_nights", db.Integer),
    db.Column("number_of_reviews", db.Integer),
    db.Column("last_review", db.DateTime),
    db.Column("reviews_per_month", db.Float),
    db.Column("calculated_host_listings_count", db.Integer),
    db.Column("availability_365", db.Integer),
    db.Column("number_of_reviews_ltm", db.Integer),
    db.Column("license", db.String(500)),
    db.Column("city", db.String(50))
)

reviews_table = db.Table("reviews", metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("listing_id", db.Integer, db.ForeignKey("listings.id")),
    db.Column("city", db.String(50)),
    db.Column("date", db.DateTime)
)

print("Tables created")

# Add data to the database

# Read the listings data
listings_berlin = pd.read_csv("CSVs/listings_berlin.csv")
listings_munich = pd.read_csv("CSVs/listings_munich.csv")

# Merge both listings dataframes
listings_berlin['city'] = 'Berlin'
listings_munich['city'] = 'Munich'

listings_all = pd.concat([listings_berlin, listings_munich], ignore_index=True)

# Read the reviews data
reviews_berlin = pd.read_csv("CSVs/reviews_berlin.csv")
reviews_munich = pd.read_csv("CSVs/reviews_munich.csv")

# Merge both reviews dataframes

reviews_berlin['city'] = 'Berlin'
reviews_munich['city'] = 'Munich'

reviews_all = pd.concat([reviews_berlin, reviews_munich], ignore_index=True)

# Clean up the reviews dataframe
def clean_listings(df):
    df = df.copy()
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['number_of_reviews'] = df['number_of_reviews'].fillna(0).astype(int)
    df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')
    df['room_type'] = df['room_type'].str.strip().str.title()
    return df

def clean_reviews(df):
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

reviews_all = clean_reviews(reviews_all)
listings_all = clean_listings(listings_all)

# Add data to the database
reviews_all.to_sql("reviews", conn, if_exists="replace", index=False)
listings_all.to_sql("listings", conn, if_exists="replace", index=False)
print("Data added to the database")

# Close the connection
conn.close()
print("Connection closed")