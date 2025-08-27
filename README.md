# 🎬 Movie Social Graph with Neo4j and Python

This repository contains a **mini-project** to create a Movie Social Graph using **Neo4j** and **Python**.
The goal is to model movies, people, and their relationships, and explore the data using **Cypher queries**.

---

## 📂 Project Structure

```
├── data/                  # CSV datasets
│   ├── tmdb_5000_movies.csv
│   ├── tmdb_5000_credits.csv
│   └── tmdb_cleaned.csv   # optional cleaned dataset
├── cypher_patterns.py     # aggregation and pattern queries
├── db_connection.py       # Neo4j connection utility
├── graph_updates.py       # functions to update the graph (add actors, genres, etc.)
├── load_data.py           # load and clean CSV, create nodes and relationships
├── main.py                # main script to load data into Neo4j
├── queries.py             # example exploratory queries
├── instructions.md        # instructions for setup or running
├── requirements.txt       # Python dependencies
└── readme.md              # this file
```

---

## 🎯 Goal

By the end of this project, you will be able to:

* Model graph data (nodes, relationships, properties)
* Load and clean movie datasets
* Insert nodes and relationships into Neo4j
* Run **Cypher queries** to explore the graph
* Perform aggregations and detect patterns (most frequent collaborators, popular genres, actors with most connections)
* Update and modify the graph (add actors, add missing genres)

---

## 📥 Datasets

* **TMDB Movie Dataset**: `tmdb_5000_movies.csv`
* **TMDB Credits Dataset**: `tmdb_5000_credits.csv`

Both CSVs are stored in the `data/` folder. You can optionally create a cleaned version (`tmdb_cleaned.csv`) after preprocessing.

---

## ⚡ Setup

1. Create a Python virtual environment and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up Neo4j and create a `.env` file in the root directory with your connection credentials:

```
URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password_here
```

4. Start your Neo4j server locally and make sure it is running.

---

## 🚀 Running the Project

1. **Load the data into Neo4j**:

```bash
python main.py
```

* This will read the CSVs, clean the data, and insert nodes and relationships into Neo4j.
* Progress is printed in the terminal. For large datasets, this may take several minutes.

2. **Explore the graph with queries**:

* Use the provided Python functions in `queries.py` or `cypher_patterns.py`
* Or use the **Neo4j Browser** at [http://localhost:7474](http://localhost:7474) to run queries manually.

3. **Update the graph**:

* Add missing genres or actors using `graph_updates.py`.

---

## 🔍 Example Queries

* Get all movies by a director
* Find all actors who co-starred with a given actor
* Find all movies of a specific genre after 2010
* Most frequent actor-director collaborations
* Most popular genres
* Actor with the most co-actor connections

---

## 📝 Notes

* All sensitive credentials are stored in `.env` and **should not be committed** to version control.
* For large datasets, consider testing on a subset to speed up development.

---

## 🛠️ Dependencies

* Python 3.12
* `neo4j` Python driver
* `pandas`
* `python-dotenv`

Install via `pip install -r requirements.txt`.

---

## 📚 References

* [Neo4j Official Documentation](https://neo4j.com/docs/)
* [Cypher Query Language Guide](https://neo4j.com/developer/cypher/)
* [TMDB Dataset on Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
