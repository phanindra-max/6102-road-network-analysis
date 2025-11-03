# Benchmarking Database Architectures for Network Analytics

A comprehensive performance comparison of MySQL, MongoDB, and Neo4j for large-scale graph and network data operations. This project evaluates three different database paradigms—relational, document-oriented, and graph—using a synthetic road network dataset with 500 cities and 250,000 connections.

![Performance Comparison](Output%20Images/Performace%20Visualizations/execution_time_comparison_line.png)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Results Summary](#results-summary)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Query Descriptions](#query-descriptions)
- [Performance Metrics](#performance-metrics)
- [Technologies Used](#technologies-used)
- [Key Findings](#key-findings)
- [Contributing](#contributing)
- [License](#license)
- [Authors](#authors)

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

## 🔧 Prerequisites

### Required Software:
- Python 3.8+
- MySQL Server 8.0+
- MongoDB 5.0+
- Neo4j 5.0+ (Community or Enterprise)

### Python Dependencies:
```bash
pip install -r requirements.txt
```

Required packages:
- `mysql-connector-python`
- `pymongo`
- `neo4j`
- `faker`
- `psutil`
- `matplotlib`
- `tqdm`

---

## 📥 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/database-benchmark-network-analytics.git
cd database-benchmark-network-analytics
```

### 2. Install Python Dependencies
```bash
pip install mysql-connector-python pymongo neo4j faker psutil matplotlib tqdm
```

Or use requirements file:
```bash
pip install -r requirements.txt
```

### 3. Configure Database Connections

**MySQL:**
```python
# Default: localhost, user='root', no password
# Modify in populator.py and queries.py if needed
```

**MongoDB:**
```python
# Default: mongodb://localhost:27017/
# Modify connection string in populator.py and queries.py if needed
```

**Neo4j:**
```python
# Default: neo4j://localhost:7687
# Username: neo4j
# Password: 12345678 (change in populator.py and queries.py)
```

### 4. Start Database Services

**MySQL:**
```bash
# Linux/Mac
sudo service mysql start

# Windows
net start MySQL
```

**MongoDB:**
```bash
# Linux/Mac
sudo service mongod start

# Windows
net start MongoDB
```

**Neo4j:**
```bash
# Using Neo4j Desktop (recommended) or:
neo4j start
```

---

## 🚀 Usage

### Step 1: Generate Dataset
```bash
python generator.py
```
**Output**: `final_road_network.csv` (250,000 rows)

### Step 2: Populate Databases
```bash
python populator.py
```
**Duration**: ~5-10 minutes depending on hardware

This script will:
- Create MySQL database and table
- Populate MongoDB collection
- Build Neo4j graph (nodes + relationships)

### Step 3: Run Benchmarks
```bash
python queries.py
```
**Duration**: ~3-5 minutes

This will:
- Execute 12 queries (4 per database)
- Collect performance metrics
- Generate visualization charts
- Save results to `Output Images/` directory

### View Results
Charts are saved in:
- `Output Images/Performace Visualizations/`
- `query_performance_comparison.png`
- Individual metric line charts

---

## 📁 Project Structure

```
.
├── generator.py                    # Synthetic data generation
├── populator.py                    # Multi-database population script
├── queries.py                      # Unified benchmark queries
├── final_road_network.csv          # Generated dataset (250K rows)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── Output Images/
│   ├── Code Outputs/
│   │   ├── Unified Queries/        # Query execution screenshots
│   │   └── Data Generation and Population.png
│   │
│   └── Performace Visualizations/  # Performance charts
│       ├── query_performance_comparison.png
│       ├── execution_time_comparison_line.png
│       ├── cpu_usage_comparison_line.png
│       └── memory_usage_comparison_line.png
│
└── Documentation/
    ├── 6102 Queries Ideas.docx
    └── GROUP 4 PROJECT PROPOSAL.docx
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

## 🛠️ Technologies Used

### Databases
- **MySQL 8.0** - Relational database with InnoDB engine
- **MongoDB 5.0** - Document-oriented NoSQL database
- **Neo4j 5.0** - Native graph database

### Programming & Libraries
- **Python 3.8+** - Primary language
- **Faker** - Synthetic data generation
- **psutil** - System resource monitoring
- **matplotlib** - Data visualization
- **tqdm** - Progress bars
- **mysql-connector-python** - MySQL driver
- **pymongo** - MongoDB driver
- **neo4j-python-driver** - Neo4j Bolt driver

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

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Issues
- Use GitHub Issues to report bugs
- Include database versions and error messages
- Provide steps to reproduce

### Feature Requests
- Query additions (3+ hop traversals, weighted paths)
- Additional databases (PostgreSQL, Redis, ArangoDB)
- Performance optimizations
- Visualization improvements

### Pull Requests
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025 [Your Name/Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👥 Authors

**Group 4 - Section 10**
- [Your Name](https://github.com/yourusername)
- [Team Member 2]
- [Team Member 3]
- [Team Member 4]

**Course**: Data Warehousing (6102)  
**Institution**: The George Washington University  
**Year**: 2025

---

## 📧 Contact

For questions or collaboration:
- GitHub Issues: [Project Issues](https://github.com/yourusername/database-benchmark-network-analytics/issues)
- Email: your.email@university.edu

---

## 🙏 Acknowledgments

- Faker library for realistic test data generation
- Database communities (MySQL, MongoDB, Neo4j) for excellent documentation
- The George Washington University Data Warehousing course

---

## 📚 Further Reading

- [MySQL Recursive CTEs Documentation](https://dev.mysql.com/doc/refman/8.0/en/with.html)
- [MongoDB Aggregation Pipeline](https://docs.mongodb.com/manual/aggregation/)
- [Neo4j Cypher Query Language](https://neo4j.com/docs/cypher-manual/current/)
- [Graph Database Performance Patterns](https://neo4j.com/developer/guide-performance-tuning/)

---

**⭐ If you find this project helpful, please star the repository!**

