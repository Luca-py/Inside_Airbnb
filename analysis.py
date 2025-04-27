import pandas as pd
import sqlalchemy as db
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from dotenv import load_dotenv
import os

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

# Print data diagnostics
print("\nData Overview:")
print(f"Total listings: {len(listings)}")
print(f"Room types: {listings['room_type'].unique()}")
print(f"Room type counts:\n{listings['room_type'].value_counts()}")
print(f"Cities: {listings['city'].unique()}")
print(f"City counts:\n{listings['city'].value_counts()}")
print(f"Price statistics:\n{listings['price'].describe()}")

# T-test 1: Room types

# Room Type comparison
private_prices = listings[listings['room_type'] == 'Private Room']['price'].dropna().values
entire_prices = listings[listings['room_type'] == 'Entire Home/Apt']['price'].dropna().values

t_stat, p_value = stats.ttest_ind(private_prices, entire_prices, equal_var=False)
print("\nRoom Type T-Test:")
print(f"T-stat: {t_stat:.4f}, P-value: {p_value:.10f}")

# T-test 2: Downtown vs non-downtown
# Define downtown neighborhood and calculate distance
downtown_berlin = ['Mitte', 'Friedrichshain-Kreuzberg', 'Prenzlauer Berg']
downtown_munich = ['Altstadt-Lehel', 'Ludwigsvorstadt-Isarvorstadt', 'Maxvorstadt']

def is_downtown(neighborhood, city):
    if city == 'Berlin':
        return neighborhood in downtown_berlin
    elif city == 'Munich':
        return neighborhood in downtown_munich

listings['is_downtown'] = listings.apply(lambda row: is_downtown(row['neighbourhood'], row['city']), axis=1)

downtown_prices = listings[listings['is_downtown']]['price'].dropna().values
non_downtown_prices = listings[~listings['is_downtown']]['price'].dropna().values

t_stat, p_value = stats.ttest_ind(downtown_prices, non_downtown_prices, equal_var=False)
print("\nDowntown vs Non-Downtown T-Test:")
print(f"T-stat: {t_stat:.4f}, P-value: {p_value:.10f}")

# T-test 3: Berlin vs Munich
berlin_prices = listings[listings['city'] == 'Berlin']['price'].dropna().values
munich_prices = listings[listings['city'] == 'Munich']['price'].dropna().values

t_stat, p_value = stats.ttest_ind(berlin_prices, munich_prices, equal_var=False)
print("\nBerlin vs Munich T-Test:")
print(f"T-stat: {t_stat:.4f}, P-value: {p_value:.10f}")

# Correlation between price and review count
correlation = listings['price'].corr(listings['number_of_reviews'])
print(f"\nCorrelation between price and review score: {correlation:.4f}")

# Visualizations
plt.figure(figsize=(12, 6))

# Price distribution by room type
plt.subplot(1, 2, 1)
sns.boxplot(x='room_type', y='price', data=listings)
plt.title('Price Distribution by Room Type')
plt.xlabel('Room Type')
plt.ylabel('Price')
plt.ylim(0, listings['price'].quantile(0.95))  # Limit y-axis to 95th percentile for better visibility

# Price distribution by city
plt.subplot(1, 2, 2)
sns.boxplot(x='city', y='price', data=listings)
plt.title('Price Distribution by City')
plt.xlabel('City')
plt.ylabel('Price')
plt.ylim(0, listings['price'].quantile(0.95))  # Limit y-axis to 95th percentile for better visibility

plt.tight_layout()
plt.savefig('price_distribution.png')
plt.close()

# Price distribution by neighborhood
listings['city_neighborhood'] = listings['city'] + " - " + listings['neighbourhood']  # Fix spelling here

neighborhood_stats = listings.groupby('city_neighborhood').agg({
    'price': 'mean',
    'id': 'count'
}).rename(columns={'id': 'listing_count'})

# Only include neighborhoods with enough listings
popular_neighborhoods = neighborhood_stats[neighborhood_stats['listing_count'] > 10]
popular_neighborhoods = popular_neighborhoods.sort_values('price', ascending=False)

# Plot heatmap of prices for top 20 neighborhoods
plt.figure(figsize=(12, 8))
sns.heatmap(popular_neighborhoods.head(20)[['price']].T, annot=True, fmt='.0f', cmap='viridis')
plt.title('Average Price by Neighborhood (Top 20)')
plt.tight_layout()
plt.savefig('neighborhood_price_heatmap.png')
