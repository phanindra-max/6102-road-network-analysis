#%%
import time
import mysql.connector
import psutil

# connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="final_road_network"
)
print("Connected to MySQL successfully!")
cursor = connection.cursor()

# Query 1: To get roads from Richmond to Atlanta with distance > 500
query = """
SELECT fromCity, toCity, distance
FROM roads
WHERE fromCity = 'Richmond' AND toCity = 'Atlanta' AND distance >= 500;
"""
start_time = time.time()
start_cpu = psutil.cpu_percent()
start_memory = psutil.virtual_memory().used
cursor.execute(query)
results = cursor.fetchall()
for row in results:
    print(f"From: {row[0]}, To: {row[1]}, Distance: {row[2]}")
query1_sql_time = time.time() - start_time
query1_sql_cpu = psutil.cpu_percent() - start_cpu
query1_sql_memory = psutil.virtual_memory().used - start_memory
print(f'\n\nMySQL Query 1 executed successfully in {query1_sql_time} seconds!')
print(f'CPU Usage: {query1_sql_cpu}%')
print(f'Memory Usage: {query1_sql_memory/1024} KB', end="\n\n")

#%%
# Query 2: To calculate the top 5 average distance per city pairs
query = """
    SELECT fromCity, toCity, AVG(distance) AS avg_distance
    FROM roads
    GROUP BY fromCity, toCity
    ORDER BY avg_distance DESC
    LIMIT 5;
"""
start_time = time.time()
start_cpu = psutil.cpu_percent()
start_memory = psutil.virtual_memory().used
cursor.execute(query)
results = cursor.fetchall()
print("Top 5 Average distance per city pairs:")
for row in results:
    print(f"From: {row[0]}, To: {row[1]}, Average Distance: {row[2]}")
query2_sql_time = time.time() - start_time
query2_sql_cpu = psutil.cpu_percent() - start_cpu
query2_sql_memory = psutil.virtual_memory().used - start_memory
print(f'\n\nMySQL Query 2 executed successfully in {query2_sql_time} seconds!')
print(f'CPU Usage: {query2_sql_cpu}%')
print(f'Memory Usage: {query2_sql_memory/1024} KB', end="\n\n")

#%%
# Query 3: To find cities within 2 hops from Richmond
query = """
    WITH RECURSIVE city_distances(fromCity, toCity, distance, hops) AS (
    SELECT fromCity, toCity, distance, 1 AS hops
    FROM roads
    WHERE fromCity = 'Richmond'
    UNION ALL
    SELECT cd.fromCity, r.toCity, cd.distance + r.distance, cd.hops + 1
    FROM city_distances cd
    JOIN roads r ON cd.toCity = r.fromCity
    WHERE cd.hops < 2
)
SELECT DISTINCT toCity AS city, MIN(distance) AS distance
FROM city_distances
GROUP BY toCity;
"""
start_time = time.time()
start_cpu = psutil.cpu_percent()
start_memory = psutil.virtual_memory().used
cursor.execute(query)
results = cursor.fetchall()
print("Cities within 2 hop from Richmond (MySQL):")
for row in results:
    print(f"City: {row[0]}, Distance: {row[1]} miles")
query3_sql_time = time.time() - start_time
query3_sql_cpu = psutil.cpu_percent() - start_cpu
query3_sql_memory = psutil.virtual_memory().used - start_memory
print(f'\n\nMySQL Query 3 executed successfully in {query3_sql_time} seconds!')
print(f'CPU Usage: {query3_sql_cpu}%')
print(f'Memory Usage: {query3_sql_memory/1024} KB', end="\n\n")

#%%
# Query 4: To find the shortest path between Richmond and Amman with at most 2 hops
query = """
    WITH RECURSIVE paths (fromCity, toCity, distance, path, hops) AS (
        SELECT fromCity, toCity, distance, CONCAT(fromCity, ' -> ', toCity), 1
        FROM roads
        WHERE fromCity = 'Richmond'
        UNION ALL
        SELECT p.fromCity, r.toCity, p.distance + r.distance,
               CONCAT(p.path, ' -> ', r.toCity), p.hops + 1
        FROM paths p
        JOIN roads r ON p.toCity = r.fromCity
        WHERE p.hops < 2 AND r.toCity != 'Amman'
    )
    SELECT path, distance
    FROM paths
    WHERE toCity = 'Amman'
    ORDER BY distance
    LIMIT 1;
"""

start_time = time.time()
start_cpu = psutil.cpu_percent()
start_memory = psutil.virtual_memory().used
cursor.execute(query)
result = cursor.fetchone()
if result:
    print(f"Shortest Path: {result[0]}")
    print(f"Distance: {result[1]}")
else:
    print("No path found between Richmond and Amman with at most 2 hops.")
query4_sql_time = time.time() - start_time
query4_sql_cpu = psutil.cpu_percent() - start_cpu
query4_sql_memory = psutil.virtual_memory().used - start_memory
print(f"\n\nMySQL Query 4 executed successfully in {query4_sql_time} seconds!")
print(f'CPU Usage: {query4_sql_cpu}%')
print(f'Memory Usage: {query4_sql_memory/1024} KB', end="\n\n")
# Close the cursor and connection
cursor.close()
connection.close()

#%%
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
print("Connected to MongoDB successfully!")
db = client['final_road_network']
collection = db['roads']

# Query 1: To get roads from Richmond to Atlanta with distance > 500
query = {
    "fromCity": "Richmond",
    "toCity": "Atlanta",
    "distance": {"$gte": 500}
}
start_time = time.time()
start_cpu = psutil.cpu_percent()
start_memory = psutil.virtual_memory().used
results = collection.find(query, {"_id": 0})
for row in results:
    print(f"From: {row['fromCity']}, To: {row['toCity']}, Distance: {row['distance']}")
query1_mongo_time = time.time() - start_time
query1_mongo_cpu = psutil.cpu_percent() - start_cpu
query1_mongo_memory = psutil.virtual_memory().used - start_memory
print(f'\n\nMongo Query 1 executed successfully in {query1_mongo_time} seconds!')
print(f'CPU Usage: {query1_mongo_cpu}%')
print(f'Memory Usage: {query1_mongo_memory/1024} KB', end="\n\n")

#%%
# Query 2: To calculate the top 5 average distance per city pairs
pipeline = [
    {
        "$group": {
            "_id": {"fromCity": "$fromCity", "toCity": "$toCity"},
            "avg_distance": {"$avg": "$distance"}
        }
    },
    {
        "$project": {
            "_id": 0,
            "fromCity": "$_id.fromCity",
            "toCity": "$_id.toCity",
            "avg_distance": 1
        }
    },
    {
        "$sort": {"avg_distance": -1}
    },
    {
        "$limit": 5
    }
]
start_time = time.time()
start_cpu = psutil.cpu_percent()
start_memory = psutil.virtual_memory().used
results = collection.aggregate(pipeline)
print("Top 5 Average distance per city pairs:")
for row in results:
    print(f"From: {row['fromCity']}, To: {row['toCity']}, Average Distance: {row['avg_distance']}")
query2_mongo_time = time.time() - start_time
query2_mongo_cpu = psutil.cpu_percent() - start_cpu
query2_mongo_memory = psutil.virtual_memory().used - start_memory
print(f'\n\nMongo Query 2 executed successfully in {query2_mongo_time} seconds!')
print(f'CPU Usage: {query2_mongo_cpu}%')
print(f'Memory Usage: {query2_mongo_memory/1024} KB', end="\n\n")

#%%
# Query 3: To find cities within 2 hops from Richmond
def find_cities_within_hops(start_city):
    pipeline = [
        {
            "$match": {
                "fromCity": start_city
            }
        },
        {
            "$lookup": {
                "from": "roads",
                "localField": "toCity",
                "foreignField": "fromCity",
                "as": "connections"
            }
        },
        {
            "$unwind": "$connections"
        },
        {
            "$project": {
                "_id": 0,
                "city": "$connections.toCity",
                "distance": {
                    "$sum": ["$distance", "$connections.distance"]
                }
            }
        },
        {
            "$group": {
                "_id": "$city",
                "minDistance": {
                    "$min": "$distance"
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "city": "$_id",
                "distance": "$minDistance"
            }
        }
    ]

    try:
        results = collection.aggregate(pipeline)
        return list(results)
    except Exception as e:
        print(f"Error: {str(e)}")
        return []

print("Cities within 2 hops from Richmond:")
start_time = time.time()
start_cpu = psutil.cpu_percent()
start_memory = psutil.virtual_memory().used
results = find_cities_within_hops("Richmond")
for row in results:
    print(f"City: {row['city']}, Distance: {row['distance']}")

query3_mongo_time = time.time() - start_time
query3_mongo_cpu = psutil.cpu_percent() - start_cpu
query3_mongo_memory = psutil.virtual_memory().used - start_memory
print(f'\n\nMongo Query 3 executed successfully in {query3_mongo_time} seconds!')
print(f'CPU Usage: {query3_mongo_cpu}%')
print(f'Memory Usage: {query3_mongo_memory/1024} KB', end="\n\n")

#%%
# Query 4: To find the shortest path between Richmond and Amman with at most 2 hops
from collections import deque

def find_shortest_path_bfs(start_city, end_city, max_hops):
    # Create a queue to store the paths
    queue = deque([(start_city, [start_city], 0)])
    
    # Set to store visited cities
    visited = set()
    
    while queue:
        current_city, path, distance = queue.popleft()
        
        # Check if the current city is the end city
        if current_city == end_city:
            return path, distance
        
        # Check if the current city has been visited before
        if current_city in visited:
            continue
        
        # Mark the current city as visited
        visited.add(current_city)
        
        # Find the neighboring cities
        neighbors = collection.find({"fromCity": current_city}, {"toCity": 1, "distance": 1})
        
        for neighbor in neighbors:
            city = neighbor["toCity"]
            dist = neighbor["distance"]
            
            # Check if the city has been visited and if the number of hops is within the limit
            if city not in visited and len(path) <= max_hops:
                queue.append((city, path + [city], distance + dist))
    
    # If no path is found within the hop limit
    return None, None

# Find the shortest path between Richmond and Amman with at most 2 hops
start_city = "Richmond"
end_city = "Amman"
max_hops = 2

start_time = time.time()
start_cpu = psutil.cpu_percent()
start_memory = psutil.virtual_memory().used
path, distance = find_shortest_path_bfs(start_city, end_city, max_hops)
if path:
    print(f"Shortest Path: {' -> '.join(path)}")
    print(f"Distance: {distance}")
else:
    print(f"No path found between {start_city} and {end_city} within {max_hops} hops.")
query4_mongo_time = time.time() - start_time
query4_mongo_cpu = psutil.cpu_percent() - start_cpu
query4_mongo_memory = psutil.virtual_memory().used - start_memory
print(f'\n\nMongo Query 4 executed successfully in {query4_mongo_time} seconds!')
print(f'CPU Usage: {query4_mongo_cpu}%')
print(f'Memory Usage: {query4_mongo_memory/1024} KB', end="\n\n")

# Close the MongoDB connection
client.close()

#%%
from neo4j import GraphDatabase
from tqdm import tqdm 

# Connect to Neo4j
uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "12345678"))
driver.verify_connectivity()
print("Connected to Neo4j successfully!")

# Query 1: To get roads from Richmond to Atlanta with distance > 500
def find_routes(tx, from_city, to_city, min_distance):
    query = """
        MATCH (from:City {name: $from_city})-[road:ROAD]->(to:City {name: $to_city})
        WHERE road.distance >= $min_distance
        RETURN from.name AS fromCity, to.name AS toCity, road.distance AS distance
    """
    results = tx.run(query, from_city=from_city, to_city=to_city, min_distance=min_distance)
    return [(row["fromCity"], row["toCity"], row["distance"]) for row in results]

start_time = time.time()
start_cpu = psutil.cpu_percent()
start_memory = psutil.virtual_memory().used
# Execute the Cypher query within a transaction
with driver.session() as session:
    results = session.execute_read(find_routes, "Richmond", "Atlanta", 500)

# Print the results
for row in results:
    print(f"From: {row[0]}, To: {row[1]}, Distance: {row[2]}")

query1_neo_time = time.time() - start_time
query1_neo_cpu = psutil.cpu_percent() - start_cpu
query1_neo_memory = psutil.virtual_memory().used - start_memory
print(f'\n\nNeo4j Query 1 executed successfully in {query1_neo_time} seconds!')
print(f'CPU Usage: {query1_neo_cpu}%')
print(f'Memory Usage: {query1_neo_memory/1024} KB', end="\n\n")


# %%
# Query 2: To calculate the top 5 average distance per city pairs
def calculate_avg_distance(tx):
    query = """
        MATCH (from:City)-[road:ROAD]->(to:City)
        RETURN from.name AS fromCity, to.name AS toCity, AVG(road.distance) AS avg_distance
        ORDER BY avg_distance DESC
        LIMIT 5
    """
    results = tx.run(query)
    return [(row["fromCity"], row["toCity"], row["avg_distance"]) for row in results]

start_time = time.time()
start_cpu = psutil.cpu_percent()
start_memory = psutil.virtual_memory().used
with driver.session() as session:
    results = session.execute_read(calculate_avg_distance)
print("Top 5 Average distance per city pairs:")
for row in results:
    print(f"From: {row[0]}, To: {row[1]}, Average Distance: {row[2]}")
query2_neo_time = time.time() - start_time
query2_neo_cpu = psutil.cpu_percent() - start_cpu
query2_neo_memory = psutil.virtual_memory().used - start_memory
print(f'\n\nNeo4j Query 2 executed successfully in {query2_neo_time} seconds!')
print(f'CPU Usage: {query2_neo_cpu}%')
print(f'Memory Usage: {query2_neo_memory/1024} KB', end="\n\n")

# %%
# Query 3: To find cities within 2 hops from Richmond
def find_cities_within_hops(tx, start_city, max_hops):
    query = """
        MATCH (start:City {name: $start_city})-[r:ROAD*..2]->(dest:City)
        RETURN dest.name AS city, min(reduce(distance = 0, road IN r | distance + road.distance)) AS distance
    """
    results = tx.run(query, start_city=start_city, max_hops=max_hops)
    return [(row["city"], row["distance"]) for row in results]

print("Cities within 2 hops from Richmond using Neo4j:")
start_time = time.time()
start_cpu = psutil.cpu_percent()
start_memory = psutil.virtual_memory().used
with driver.session() as session:
    results = session.execute_read(find_cities_within_hops, "Richmond", 2)
for row in results:
    print(f"City: {row[0]}, Distance: {row[1]}")
query3_neo_time = time.time() - start_time
query3_neo_cpu = psutil.cpu_percent() - start_cpu
query3_neo_memory = psutil.virtual_memory().used - start_memory
print(f'\n\nNeo4j Query 3 executed successfully in {query3_neo_time} seconds!')
print(f'CPU Usage: {query3_neo_cpu}%')
print(f'Memory Usage: {query3_neo_memory/1024} KB', end="\n\n")

# driver.close()
# %%
# Query 4: To find the shortest path between Richmond and Amman with at most 2 hops
def find_shortest_path(tx, start_city, end_city, max_hops):
    query = f"""
        MATCH path = shortestPath((start:City {{name: $start_city}})-[:ROAD*..{max_hops}]->(end:City {{name: $end_city}}))
        RETURN nodes(path) AS cities, reduce(distance = 0, road IN relationships(path) | distance + road.distance) AS total_distance
        ORDER BY total_distance
        LIMIT 1
    """
    results = tx.run(query, start_city=start_city, end_city=end_city)
    return results.single()

print("Shortest path between Richmond and Amman with at most 2 hops (Neo4j):")
start_time = time.time()
start_cpu = psutil.cpu_percent()
start_memory = psutil.virtual_memory().used
with driver.session() as session:
    result = session.execute_read(find_shortest_path, "Richmond", "Amman", 2)
if result:
    print(f"Shortest Path: {' -> '.join([record['name'] for record in result['cities']])}")
    print(f"Distance: {result['total_distance']}")
else:
    print("No path found between Richmond and Amman with at most 2 hops.")
query4_neo_time = time.time() - start_time
query4_neo_cpu = psutil.cpu_percent() - start_cpu
query4_neo_memory = psutil.virtual_memory().used - start_memory
print(f'\n\nNeo4j Query 4 executed successfully in {query4_neo_time} seconds!')
print(f'CPU Usage: {query4_neo_cpu}%')
print(f'Memory Usage: {query4_neo_memory/1024} KB', end="\n\n")

# %%
import matplotlib.pyplot as plt

# Create lists to store the values for each database
databases = ['MySQL', 'MongoDB', 'Neo4j']
query_times = [query1_sql_time, query1_mongo_time, query1_neo_time]
query_cpu = [query1_sql_cpu, query1_mongo_cpu, query1_neo_cpu]
query_memory = [query1_sql_memory, query1_mongo_memory, query1_neo_memory]

# Create a figure with subplots for bar plots
fig_bar, (ax1_bar, ax2_bar, ax3_bar) = plt.subplots(1, 3, figsize=(15, 5))

# Plot execution time (bar plot)
ax1_bar.bar(databases, query_times)
ax1_bar.set_ylabel('Execution Time (seconds)')
ax1_bar.set_title('Query Execution Time (Bar Plot)')

# Plot CPU usage (bar plot)
ax2_bar.bar(databases, query_cpu)
ax2_bar.set_ylabel('CPU Usage (%)')
ax2_bar.set_title('Query CPU Usage (Bar Plot)')

# Plot memory usage (bar plot)
ax3_bar.bar(databases, query_memory)
ax3_bar.set_ylabel('Memory Usage (bytes)')
ax3_bar.set_title('Query Memory Usage (Bar Plot)')

# Adjust spacing between subplots
plt.tight_layout()

# Save the bar plot figure
plt.savefig('query_performance_bar_plot.png')

# Create a figure with subplots for line plots
fig_line, (ax1_line, ax2_line, ax3_line) = plt.subplots(1, 3, figsize=(15, 5))

# Plot execution time (line plot)
ax1_line.plot(databases, query_times, marker='o')
ax1_line.set_ylabel('Execution Time (seconds)')
ax1_line.set_title('Query Execution Time (Line Plot)')

# Plot CPU usage (line plot)
ax2_line.plot(databases, query_cpu, marker='o')
ax2_line.set_ylabel('CPU Usage (%)')
ax2_line.set_title('Query CPU Usage (Line Plot)')

# Plot memory usage (line plot)
ax3_line.plot(databases, query_memory, marker='o')
ax3_line.set_ylabel('Memory Usage (bytes)')
ax3_line.set_title('Query Memory Usage (Line Plot)')

# Adjust spacing between subplots
plt.tight_layout()

# Save the line plot figure
plt.savefig('query_performance_line_plot.png')

# Display the plots
plt.show()