import csv
import itertools
from faker import Faker
import random

# Initialize Faker
faker = Faker()

# Generate unique city names
num_cities = 500
random_cities = [faker.unique.city() for _ in range(num_cities - 12)]

# Add specific cities to the list
specific_cities = [
    "Atlanta", "Richmond", "Paris", "Strasbourg", "Breslau", "Prague",
    "Frankfurt", "Cologne", "Salzburg", "Berlin", "London", "Amman"
]

cities = specific_cities + random_cities

# Generate all possible pairs of cities (allowing for both directions)
all_city_pairs = list(itertools.permutations(cities, 2))

# Shuffle the pairs to randomize them
random.shuffle(all_city_pairs)

# Generate roads with distances
num_roads = 250000
roads = []

# Since we can reuse pairs if needed, iterate with modulo to cycle through pairs if we exceed the list
for i in range(num_roads):
    from_city, to_city = all_city_pairs[i % len(all_city_pairs)]
    distance = faker.random_int(min=50, max=1000)
    roads.append((from_city, to_city, distance))

# Write dataset to CSV file
with open('final_road_network.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['FromCity', 'ToCity', 'Distance'])
    writer.writerows(roads)

print(f"\n\nGenerated {len(roads)} roads between {num_cities} cities (including specific cities) and saved to 'final_road_network.csv'")