import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Simulate listings
n = 500  # number of listings

locations = ['Dubai Marina', 'Jumeirah Village Circle', 'Business Bay', 'Downtown Dubai', 'Jumeirah Lake Towers', 'Palm Jumeirah']
property_types = ['Apartment', 'Villa', 'Studio', 'Townhouse']
furnish_options = ['Yes', 'No']
statuses = ['Available', 'Sold', 'Rented']
agent_ids = [f"AGT{100+i}" for i in range(1, 21)]  # 20 agents

# Generate data
data = {
    'property_id': range(1001, 1001 + n),
    'property_type': np.random.choice(property_types, n),
    'location': np.random.choice(locations, n),
    'bedrooms': np.random.randint(1, 6, size=n),
    'bathrooms': np.random.randint(1, 5, size=n),
    'sqft': np.random.randint(400, 5000, size=n),
    'furnished': np.random.choice(furnish_options, n),
    'agent_id': np.random.choice(agent_ids, n),
    'status': np.random.choice(statuses, n),
    'date_listed': [datetime.today() - timedelta(days=random.randint(0, 180)) for _ in range(n)]
}


# Create base DataFrame
df = pd.DataFrame(data)

# Add price based on size, location, and type
def estimate_price(row):
    base = 800 * row['sqft']
    if row['location'] == 'Palm Jumeirah':
        base *= 1.5
    elif row['location'] in ['Downtown Dubai', 'Dubai Marina']:
        base *= 1.3
    elif row['location'] == 'Business Bay':
        base *= 1.1
    return int(base + np.random.randint(-100000, 100000))

df['price'] = df.apply(estimate_price, axis=1)

# Final touch
df = df[['property_id', 'property_type', 'price', 'location', 'bedrooms', 'bathrooms', 'sqft', 'furnished', 'date_listed']]

# EDA
df.describe()
df['location'].value_counts()
df['property_type'].value_counts()

import seaborn as sns
import matplotlib.pyplot as plt

# Average price by location
plt.figure(figsize=(10,6))
sns.barplot(data=df, x='location', y='price', estimator=np.mean)
plt.title('Average Property Price by Location')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Price vs. Sqft
plt.figure(figsize=(10,6))
sns.scatterplot(data=df, x='sqft', y='price', hue='location')
plt.title('Price vs Square Footage')
plt.show()

# Bedrooms vs Price (Boxplot)
plt.figure(figsize=(10,6))
sns.boxplot(data=df, x='bedrooms', y='price')
plt.title('Distribution of Price by Number of Bedrooms')
plt.show()

# Listing trends over time
df['week'] = df['date_listed'].dt.to_period('W').astype(str)

plt.figure(figsize=(12,6))
sns.countplot(data=df.sort_values('date_listed'), x='week')
plt.title('Listings Over Time (by Week)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Top 10 most expensive properties
df.sort_values('price', ascending=False).head(10)

# Price per sqft analysis
df['price_per_sqft'] = df['price'] / df['sqft']
df.groupby('location')['price_per_sqft'].mean().sort_values(ascending=False)

# Furnishing impact
plt.figure(figsize=(8,6))
sns.boxplot(data=df, x='furnished', y='price')
plt.title('Price Distribution by Furnishing Status')
plt.show()

# Exporting for Power BI analysis
df.to_csv(r'C:\Users\Basil\OneDrive\Desktop\simulated_real_estate_dataset.csv', index=False)
