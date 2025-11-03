# Installation Guide

Complete setup instructions for running the Database Benchmarking project.

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
- [Database Configuration](#database-configuration)
- [Running the Benchmark](#running-the-benchmark)
- [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### Required Software

- **Python 3.8+**
- **MySQL Server 8.0+**
- **MongoDB 5.0+**
- **Neo4j 5.0+** (Community or Enterprise)

### Python Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `mysql-connector-python` - MySQL database driver
- `pymongo` - MongoDB driver
- `neo4j` - Neo4j Bolt driver
- `faker` - Synthetic data generation
- `psutil` - System resource monitoring
- `matplotlib` - Data visualization
- `tqdm` - Progress bars for batch operations

---

## 📥 Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/database-benchmark-network-analytics.git
cd database-benchmark-network-analytics
```

### 2. Install Python Dependencies

**Option 1: Using requirements.txt**
```bash
pip install -r requirements.txt
```

**Option 2: Manual installation**
```bash
pip install mysql-connector-python pymongo neo4j faker psutil matplotlib tqdm
```

### 3. Verify Python Installation

```bash
python --version
# Should show Python 3.8 or higher
```

---

## ⚙️ Database Configuration

### MySQL Setup

**Start MySQL Service:**

**Linux/Mac:**
```bash
sudo service mysql start
```

**Windows:**
```bash
net start MySQL
```

**Default Connection Settings:**
- Host: `localhost`
- Port: `3306`
- User: `root`
- Password: (no password)
- Database: `road_network_db` (auto-created)

**To modify connection settings:**
Edit `scripts/populator.py` and `scripts/queries.py`:
```python
conn = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_password'
)
```

---

### MongoDB Setup

**Start MongoDB Service:**

**Linux/Mac:**
```bash
sudo service mongod start
```

**Windows:**
```bash
net start MongoDB
```

**Default Connection Settings:**
- Connection String: `mongodb://localhost:27017/`
- Database: `road_network_db`
- Collection: `roads`

**To modify connection settings:**
Edit `scripts/populator.py` and `scripts/queries.py`:
```python
client = pymongo.MongoClient("mongodb://localhost:27017/")
```

---

### Neo4j Setup

**Start Neo4j Service:**

**Option 1: Neo4j Desktop (Recommended)**
1. Download from [neo4j.com/download](https://neo4j.com/download/)
2. Create a new project
3. Create a new database
4. Set password to `12345678` (or update in scripts)
5. Click "Start"

**Option 2: Command Line**
```bash
neo4j start
```

**Default Connection Settings:**
- URI: `neo4j://localhost:7687`
- Username: `neo4j`
- Password: `12345678`

**To modify connection settings:**
Edit `scripts/populator.py` and `scripts/queries.py`:
```python
driver = GraphDatabase.driver(
    "neo4j://localhost:7687",
    auth=("neo4j", "your_password")
)
```

---

## 🚀 Running the Benchmark

### Step 1: Generate Dataset

```bash
python scripts/generator.py
```

**What it does:**
- Creates synthetic road network data
- Generates 500 unique cities
- Creates 250,000 road connections
- Saves to `data/final_road_network.csv`

**Expected output:**
```
Generating cities... 100%
Generating roads... 100%
Dataset saved: data/final_road_network.csv (250,000 rows)
```

**Duration:** ~30 seconds

---

### Step 2: Populate Databases

```bash
python scripts/populator.py
```

**What it does:**
1. **MySQL:**
   - Creates `road_network_db` database
   - Creates `roads` table with indexes
   - Batch inserts 250K records

2. **MongoDB:**
   - Creates `road_network_db` database
   - Creates `roads` collection
   - Inserts documents with indexes on source/destination

3. **Neo4j:**
   - Creates City nodes (500 nodes)
   - Creates ROAD relationships (250K relationships)
   - Adds distance properties

**Expected output:**
```
[MySQL] Creating database...
[MySQL] Inserting 250,000 records...
Progress: 100% |████████████████| 250000/250000

[MongoDB] Connecting...
[MongoDB] Inserting records...
Progress: 100% |████████████████| 250000/250000

[Neo4j] Creating nodes...
[Neo4j] Creating relationships...
Progress: 100% |████████████████| 250000/250000

✓ All databases populated successfully!
```

**Duration:** ~5-10 minutes (depending on hardware)

---

### Step 3: Run Benchmarks

```bash
python scripts/queries.py
```

**What it does:**
- Executes 4 queries on each database (12 total)
- Measures execution time, CPU usage, memory consumption
- Generates 15+ visualization charts
- Saves results to `outputs/` directory

**Expected output:**
```
Running MySQL queries...
  Query 1: 0.25s | CPU: 10.5% | Memory: 31 MB
  Query 2: 2.25s | CPU: 0.5% | Memory: 8 MB
  Query 3: 13.5s | CPU: 11.5% | Memory: 462 MB
  Query 4: 11.5s | CPU: 10.8% | Memory: 25 MB

Running MongoDB queries...
  Query 1: 0.60s | CPU: 0.8% | Memory: 42 MB
  ...

Running Neo4j queries...
  Query 1: 2.15s | CPU: 0.8% | Memory: 30 MB
  ...

✓ Benchmarks complete!
✓ Visualizations saved to: outputs/Performace Visualizations/
```

**Duration:** ~3-5 minutes

---

### Step 4: View Results

Charts are automatically saved to:
```
outputs/
├── Performace Visualizations/
│   ├── query_performance_comparison.png
│   ├── execution_time_comparison_line.png
│   ├── cpu_usage_comparison_line.png
│   └── memory_usage_comparison_line.png
```

---

## 🔧 Troubleshooting

### Common Issues

#### **Python Module Not Found**
```bash
# Solution: Install missing package
pip install <package-name>
```

#### **MySQL Connection Refused**
```bash
# Check if MySQL is running
sudo service mysql status

# Start MySQL if not running
sudo service mysql start
```

#### **MongoDB Connection Timeout**
```bash
# Check if MongoDB is running
sudo service mongod status

# Start MongoDB if not running
sudo service mongod start
```

#### **Neo4j Authentication Error**
```bash
# Reset Neo4j password:
# 1. Stop Neo4j
neo4j stop

# 2. Delete auth file (Linux/Mac)
rm data/dbms/auth

# 3. Restart and set new password
neo4j start
```

#### **Permission Denied Errors**
```bash
# Run with appropriate permissions
sudo python scripts/populator.py
```

#### **Out of Memory Errors**
```python
# Reduce batch size in scripts/populator.py
BATCH_SIZE = 1000  # Default: 5000
```

---

## 🔒 Security Notes

### Production Deployment

**Never use default credentials in production!**

Update all passwords and connection strings:

```python
# MySQL
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

# MongoDB
MONGO_URI = os.getenv('MONGO_CONNECTION_STRING')

# Neo4j
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
```

### Network Security

- Enable SSL/TLS for database connections
- Use firewalls to restrict database access
- Implement role-based access control (RBAC)

---

## 📊 System Requirements

### Minimum Requirements
- **CPU:** 2 cores
- **RAM:** 4 GB
- **Storage:** 10 GB free space
- **OS:** Windows 10, macOS 10.14+, Ubuntu 18.04+

### Recommended Requirements
- **CPU:** 4+ cores
- **RAM:** 8+ GB
- **Storage:** 20 GB SSD
- **OS:** Latest stable versions

---

## 🆘 Getting Help

If you encounter issues:

1. **Check database logs:**
   - MySQL: `/var/log/mysql/error.log`
   - MongoDB: `/var/log/mongodb/mongod.log`
   - Neo4j: `logs/neo4j.log`

2. **Verify Python dependencies:**
   ```bash
   pip list
   ```

3. **Test database connections:**
   ```bash
   # MySQL
   mysql -u root -p
   
   # MongoDB
   mongosh
   
   # Neo4j
   # Visit http://localhost:7474
   ```

4. **Open a GitHub issue:**
   - Include error messages
   - Specify database versions
   - Describe steps to reproduce


