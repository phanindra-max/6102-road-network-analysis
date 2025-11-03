# Benchmarking Database Architectures for Network Analytics

A comprehensive performance comparison of MySQL, MongoDB, and Neo4j for large-scale graph and network data operations. This project evaluates three different database paradigms—relational, document-oriented, and graph—using a synthetic road network dataset with 500 cities and 250,000 connections.

![Performance Comparison](outputs/Performace%20Visualizations/execution_time_comparison_line.png)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Results Summary](#results-summary)
- [Quick Start](#quick-start)
- [Query Descriptions](#query-descriptions)
- [Performance Metrics](#performance-metrics)
- [Key Findings](#key-findings)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Authors](#authors)
- [License](#license)

---

## 🎯 Overview

This project implements a rigorous benchmarking framework to compare database performance across different architectural paradigms. Using identical datasets and semantically equivalent queries, we measure:

- **Execution Time** - Query response latency
- **CPU Usage** - Processor utilization during query execution  
- **Memory Consumption** - RAM usage patterns

The benchmark focuses on common network analytics operations: filtering, aggregation, multi-hop traversal, and shortest path algorithms.

---

## ✨ Key Features

- **Automated Data Generation**: Synthetic road network with 500 cities and 250,000 directed edges
- **Multi-Database Population**: Batch insertion optimized for each database type
- **Unified Query Suite**: 4 equivalent queries implemented across all platforms
- **Real-Time Metrics**: CPU, memory, and execution time monitoring using `psutil`
- **Comprehensive Visualizations**: 15+ comparative performance charts
- **Production-Ready Code**: Error handling, batch processing, and connection management

---

## 📊 Results Summary

| Query Type | Best Performer | Performance Gain |
|------------|----------------|------------------|
| **Simple Filtering** | MySQL | 8.6x faster than Neo4j |
| **Aggregations** | MongoDB | 2.6x faster than Neo4j |
| **Multi-Hop Traversal** | MySQL | 5.4x faster than MongoDB |
| **Shortest Path** | Neo4j | **19.2x faster than MongoDB** |

### Quick Takeaways:
- ✅ **MySQL**: Best all-rounder with consistent performance
- ✅ **MongoDB**: Dominant for aggregations, poor for graph queries
- ✅ **Neo4j**: Specialized for pathfinding and deep graph traversals

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate dataset
python scripts/generator.py

# 3. Populate databases
python scripts/populator.py

# 4. Run benchmarks
python scripts/queries.py
```

**📖 For detailed installation instructions, database configuration, and troubleshooting, see [INSTALLATION.md](INSTALLATION.md)**

---

## 📁 Project Structure

```
.
├── data/
│   └── final_road_network.csv      # Generated dataset (500 cities, 250K roads)
│
├── docs/
│   ├── 6102 Group project paper-- jup.docx
│   ├── 6102 Queries Ideas.docx
│   └── GROUP 4 PROJECT PROPOSAL.docx
│
├── outputs/
│   ├── Code Outputs/               # Query execution screenshots
│   └── Performace Visualizations/  # Performance comparison charts
│
├── scripts/
│   ├── generator.py                # Synthetic data generation
│   ├── populator.py                # Multi-database population script
│   ├── queries.py                  # Unified benchmark queries with metrics
│   └── hybrid_challenges.py        # Additional database challenge queries
│
├── database_queries.txt            # Query reference documentation
├── INSTALLATION.md                 # Detailed setup guide
├── LICENSE                         # MIT License
├── README.md                       # Project overview and findings
└── requirements.txt                # Python dependencies
```

---

## 🔍 Query Descriptions

### Query 1: Point-to-Point Filtering
**Purpose**: Find roads from Richmond to Atlanta with distance ≥ 500 miles

**Use Case**: Direct route lookup with conditions

---

### Query 2: Top-K Aggregation
**Purpose**: Calculate top 5 city pairs by average distance

**Use Case**: Statistical analysis of network connectivity

---

### Query 3: Multi-Hop Traversal
**Purpose**: Find all cities reachable within 2 hops from Richmond

**Use Case**: Neighborhood discovery, reachability analysis

**Implementation**:
- **MySQL**: Recursive CTE
- **MongoDB**: `$lookup` aggregation pipeline
- **Neo4j**: Variable-length pattern matching `[:ROAD*..2]`

---

### Query 4: Shortest Path Algorithm
**Purpose**: Find shortest route from Richmond to Amman (max 2 hops)

**Use Case**: Navigation, route optimization

**Implementation**:
- **MySQL**: Recursive CTE with path tracking
- **MongoDB**: Custom BFS algorithm in Python
- **Neo4j**: Native `shortestPath()` function

---

## 📈 Performance Metrics

### Execution Time (seconds)

| Query | MySQL | MongoDB | Neo4j | Winner |
|-------|-------|---------|-------|--------|
| Q1 | 0.25 | 0.60 | 2.15 | MySQL |
| Q2 | 2.25 | 1.50 | 3.90 | MongoDB |
| Q3 | 13.5 | 73.0 | 25.5 | MySQL |
| Q4 | 11.5 | 48.0 | 2.5 | **Neo4j** |

### CPU Usage (%)

| Query | MySQL | MongoDB | Neo4j |
|-------|-------|---------|-------|
| Q1 | 10.5 | 0.8 | 0.8 |
| Q2 | 0.5 | 10.0 | 5.5 |
| Q3 | 11.5 | 11.7 | 9.3 |
| Q4 | 10.8 | 10.5 | 8.1 |

### Memory Usage (MB)

| Query | MySQL | MongoDB | Neo4j |
|-------|-------|---------|-------|
| Q1 | 31 | 42 | 30 |
| Q2 | 8 | 9 | 135 |
| Q3 | 462 | 15 | 185 |
| Q4 | 25 | 456 | 28 |

---

## 🔑 Key Findings

### 1. **Query Type Matters More Than Database Type**
Different queries favor different architectures. No single database wins across all categories.

### 2. **Graph Databases Excel at Their Specialty**
Neo4j's 19x advantage in shortest path queries demonstrates the value of specialized databases for specific workloads.

### 3. **MongoDB Struggles with Relationships**
Document stores require custom application logic for graph operations, resulting in 5-73 second penalties.

### 4. **MySQL Recursive CTEs Are Powerful**
Modern SQL databases can handle graph queries competently, making them viable for moderate graph workloads.

### 5. **Aggregation Pipeline Optimization**
MongoDB's aggregation framework outperforms traditional SQL GROUP BY operations.

### 6. **Memory vs. Speed Trade-offs**
MySQL uses significantly more memory for complex traversals (462 MB) but delivers faster results than MongoDB's memory-efficient approach.

### 7. **Specialized Tools for Specialized Jobs**
The 19.2x performance gain of Neo4j for shortest path algorithms justifies specialized databases for graph-heavy workloads.

---

## 🛠️ Technologies Used

**Databases:**
- **MySQL 8.0** - Relational database with InnoDB engine and recursive CTEs
- **MongoDB 5.0** - Document-oriented NoSQL with aggregation pipeline
- **Neo4j 5.0** - Native graph database with Cypher query language

**Tech Stack:**
- **Python 3.8+** with drivers for MySQL, MongoDB, and Neo4j
- **Faker** - Realistic synthetic data generation
- **psutil** - Real-time system resource monitoring
- **matplotlib** - Performance visualization charts

---

## 🤝 Contributing

Contributions welcome! Potential improvements:
- Additional query types (3+ hop traversals, weighted shortest paths)
- More databases (PostgreSQL, ArangoDB, Redis Graph)
- Advanced optimizations (indexing strategies, query tuning)
- Extended metrics (network I/O, disk usage)

Please open an issue or submit a pull request.

---

## 👥 Authors

**Group 4 - Section 10**  
Data Warehousing (6102)  
The George Washington University, 2025

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 📚 References

- [MySQL Recursive CTEs Documentation](https://dev.mysql.com/doc/refman/8.0/en/with.html)
- [MongoDB Aggregation Pipeline](https://docs.mongodb.com/manual/aggregation/)
- [Neo4j Cypher Query Language](https://neo4j.com/docs/cypher-manual/current/)
- [Graph Database Performance Patterns](https://neo4j.com/developer/guide-performance-tuning/)

---

**⭐ If you find this project helpful, please star the repository!**

