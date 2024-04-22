#%%
# MySQL Connection & Population
import csv
import mysql.connector
from pymongo import MongoClient
from neo4j import GraphDatabase
from tqdm import tqdm

#%%
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    database = "final_road_network",
)
print("Connected to MySQL successfully!")

connection.autocommit = False # for improving performance
cursor = connection.cursor()

# Create database in SQL if not exists
# CREATE DATABASE IF NOT EXISTS final_road_network

create_table_query = """
CREATE TABLE IF NOT EXISTS roads (
    fromCity VARCHAR(255),
    toCity VARCHAR(255),
    distance INT
)
"""
cursor.execute(create_table_query)
print("Using 'roads' table in 'final_road_network' database")

# Read data from CSV and insert into MySQL
with open('final_road_network.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader) # skip header row

    batch_size = 25000
    batch_data = []
    
    for row in csv_reader:
        batch_data.append(row)
        
        if len(batch_data) >= batch_size:
            cursor.executemany("INSERT INTO roads (fromCity, toCity, distance) VALUES (%s, %s, %s)", batch_data)
            batch_data = []
    
    if batch_data:
        cursor.executemany("INSERT INTO roads (fromCity, toCity, distance) VALUES (%s, %s, %s)", batch_data)
        

print("250,000 rows Data populated into MySQL successfully!")
connection.commit()
cursor.close()

#%%
# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
print("Connected to MongoDB successfully!")
db = client['final_road_network']
collection = db['roads']

# Read data from CSV and insert into MongoDB
with open('final_road_network.csv', 'r') as file:
    reader = csv.DictReader(file)
    roads = []
    for row in reader:
        road = {
            'fromCity': row['FromCity'],
            'toCity': row['ToCity'],
            'distance': int(row['Distance'])
        }
        roads.append(road)
    
    collection.insert_many(roads)

print("250,000 documents Data populated into MongoDB successfully!")

#%%
# Connect to Neo4j
uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "12345678"))
driver.verify_connectivity()
print("Connected to Neo4j successfully!")

def populate_neo4j(tx, roads):
    tx.run("UNWIND $roads AS road "
           "MERGE (from:City {name: road.fromCity}) "
           "MERGE (to:City {name: road.toCity}) "
           "MERGE (from)-[:ROAD {distance: road.distance}]->(to)",
           roads=roads)

# Read data from CSV and populate Neo4j in batches
batch_size = 10000
roads = []

with open('final_road_network.csv', 'r') as file:
    reader = csv.DictReader(file)
    with driver.session() as session:
        for row in tqdm(reader):
            road = {
                'fromCity': row['FromCity'],
                'toCity': row['ToCity'],
                'distance': int(row['Distance'])
            }
            roads.append(road)
            
            if len(roads) >= batch_size:
                session.execute_write(populate_neo4j, roads)
                roads = []
        
        if roads:
            session.execute_write(populate_neo4j, roads)

driver.close()
print("Data populated into Neo4j successfully!")

# %%
