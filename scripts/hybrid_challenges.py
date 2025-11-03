#%%
# SQL CHALLENGES

import mysql.connector
import json

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="final_road_network"
)
print("Connected to MySQL successfully!")
cursor = connection.cursor()

#%%
# Dynamic JSON Construction:
query = """ 
SELECT 
    fromCity,
    CONCAT('[', GROUP_CONCAT(DISTINCT JSON_OBJECT ORDER BY JSON_OBJECT SEPARATOR ','), ']') AS Connections
FROM (
    SELECT 
        r1.fromCity,
        CONCAT(
            '{',
            '"ToCity":"', r1.toCity, '",',
            '"Distance":', r1.distance, ',',
            '"SecondLevelConnections": [', COALESCE((
                SELECT GROUP_CONCAT(
                    DISTINCT CONCAT(
                        '{',
                        '"ToCity":"', r2.toCity, '",',
                        '"Distance":', r2.distance,
                        '}'
                    ) SEPARATOR ','
                )
                FROM roads AS r2
                WHERE r2.fromCity = r1.toCity
            ), ''), ']'
        ) AS JSON_OBJECT
    FROM roads AS r1
) AS subquery
GROUP BY fromCity;


"""
cursor.execute(query)
results = cursor.fetchall()

for row in results:
    from_city, connections = row
    connections_json = json.loads(connections)  # This converts the JSON string to a Python dictionary
    print(f"From City: {from_city}, Connections: {connections_json}")


cursor.close()
# %%
# Recursive Path Finding:

query = """
WITH RECURSIVE RouteFinder (fromCity, toCity, distance, path, hops) AS (
    -- Anchor member
    SELECT 
        fromCity, 
        toCity, 
        distance, 
        CAST(fromCity AS CHAR(255)) AS path, 
        1 AS hops
    FROM 
        roads
    WHERE 
        fromCity = 'StartingCity' -- Replace with your actual starting city
    UNION ALL
    -- Recursive member
    SELECT 
        rf.fromCity, 
        r.toCity, 
        rf.distance + r.distance, 
        CONCAT(rf.path, '->', r.toCity), 
        rf.hops + 1
    FROM 
        roads AS r
    INNER JOIN RouteFinder AS rf ON rf.toCity = r.fromCity
    WHERE 
        rf.hops < 5 AND 
        r.toCity NOT IN (SELECT fromCity FROM RouteFinder)
)
SELECT * FROM RouteFinder
WHERE toCity = 'DestinationCity'; -- Replace with your actual destination city
"""
cursor.execute(query)
routes = cursor.fetchall()

for route in routes:
    print(f"From City: {route[0]}, To City: {route[1]}, Distance: {route[2]}, Path: {route[3]}, Hops: {route[4]}")


#%%
# Aggregate Network Analysis
query= """
SELECT 
    fromCity, 
    SUM(distance) AS totalDistance
FROM 
    roads
GROUP BY 
    fromCity
ORDER BY 
    totalDistance ASC
LIMIT 1;
"""

cursor.execute(query)
most_central_city = cursor.fetchone()

if most_central_city:
    print(f"The most central city is: {most_central_city[0]} with a total travel distance of: {most_central_city[1]}")
else:
    print("No central city was found.")
    
cursor.close()


#%%
# MONGODB CHALLENGES
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
print("Connected to MongoDB successfully!")
db = client['final_road_network']
collection = db['roads']

# %%
# Multi-Level Document Embedding
pipeline = [
    {'$lookup': {
        'from': 'roads',
        'localField': 'toCity',
        'foreignField': 'fromCity',
        'as': 'directConnections'
        }},
    {'$unwind': '$directConnections'},
    {'$lookup': {
        'from': 'roads',
        'localField': 'directConnections.toCity',
        'foreignField': 'fromCity',
        'as': 'directConnections.secondLevelConnections'
        }},
    {'$group': {
        '_id': '$fromCity',
        'connections': {'$push': {
                    'toCity': '$toCity',
                    'distance': '$distance',
                    'secondLevelConnections': '$directConnections.secondLevelConnections'
                }}}},
    {'$project': {
        '_id': 0,
        'fromCity': '$_id',
        'connections': 1
        }}
]


embedded_docs = collection.aggregate(pipeline)

for doc in embedded_docs:
    print(doc)

# %%
# Aggregation of Connection Degrees
pipeline = [
    {'$group': {
            '_id': '$fromCity',
            'numberOfConnections': {'$sum': 1}}},
    {'$sort': {'numberOfConnections': -1}}
]

city_degrees = collection.aggregate(pipeline)

for city in city_degrees:
    print(f"City: {city['_id']}, Number of Direct Connections: {city['numberOfConnections']}")


client.close()

# %%
# NEO4J CHALLENGES
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "123456789"))
driver.verify_connectivity()
print("Connected to Neo4j successfully!")

    #%%
# Complex Path Analysis
def find_paths(tx):
    result = tx.run(
        "MATCH path=(from:City)-[:ROAD*1..3]->(to:City) "
        "WHERE from.name <> to.name "
        "RETURN path"
    )
    return [record["path"] for record in result]

with driver.session() as session:
    paths = session.read_transaction(find_paths)
    for path in paths:
        print(path)


# %%
# Centrality Calculation 
def compute_centrality(tx):
    # Make sure to match the correct graph name and configuration to your setup
    query = (
        "CALL gds.closeness.stream({ "
        "  nodeProjection: 'City', "
        "  relationshipProjection: { "
        "    ROAD: { "
        "      type: 'ROAD', "
        "      orientation: 'UNDIRECTED' "
        "    } "
        "  } "
        "}) "
        "YIELD nodeId, centrality "
        "RETURN gds.util.asNode(nodeId).name AS city, centrality "
        "ORDER BY centrality DESC"
    )
    results = tx.run(query)
    return [(record["city"], record["centrality"]) for record in results]

with driver.session() as session:
    centrality_results = session.read_transaction(compute_centrality)
    for result in centrality_results:
        print(f"City: {result['city']}, Centrality: {result['centrality']}")

# %%
# Advanced Relationship Querying:
def find_triangular_routes(tx, max_distance):
    query = (
        "MATCH (c1:City)-[r1:ROAD]->(c2:City)-[r2:ROAD]->(c3:City)-[r3:ROAD]->(c1:City) "
        "WHERE r1.distance <= $maxDistance AND r2.distance <= $maxDistance AND r3.distance <= $maxDistance "
        "RETURN c1.name AS City1, c2.name AS City2, c3.name AS City3, "
        "       r1.distance AS Leg1, r2.distance AS Leg2, r3.distance AS Leg3"
    )
    results = tx.run(query, maxDistance=max_distance)
    return [(record["City1"], record["City2"], record["City3"], 
             record["Leg1"], record["Leg2"], record["Leg3"]) for record in results]

max_distance = 100  # Replace with your specified maximum distance

# Execute the query
with driver.session() as session:
    routes = session.read_transaction(find_triangular_routes, max_distance)
    for route in routes:
        print(f"Triangle Route: {route[0]} -> {route[1]} -> {route[2]} -> {route[0]} "
              f"with distances {route[3]}, {route[4]}, {route[5]}")

driver.close()
# %%
