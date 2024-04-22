import csv
from faker import Faker

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

# Generate roads with distances
num_roads = 250000
roads = set()

while len(roads) < num_roads:
    from_city, to_city = faker.random_elements(elements=cities, length=2, unique=True)
    distance = faker.random_int(min=50, max=1000)
    roads.add((from_city, to_city, distance))

# Write dataset to CSV file
with open('final_road_network.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['FromCity', 'ToCity', 'Distance'])
    writer.writerows(roads)

print(f"Generated {num_roads} roads between {num_cities} cities (including specific cities) and saved to 'final_road_network.csv'")