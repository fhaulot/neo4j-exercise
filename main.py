import os
from dotenv import load_dotenv
import pandas as pd
from db_connection import Neo4jConnection
from load_data import TMDBDataLoader
from load_nodes import Neo4jLoader

"""
Main script to load, clean, and import TMDB data into a Neo4j database.

This script:
1. Loads environment variables from a .env file for Neo4j connection.
2. Loads and cleans TMDB movie and credits data using TMDBDataLoader.
3. Connects to the Neo4j database.
4. Loads nodes and relationships into Neo4j.
"""

# -------------------------------
# Load environment variables from .env file
# -------------------------------
load_dotenv()
URI = os.getenv("URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# -------------------------------
# Test Neo4j connection
# -------------------------------
def test_neo4j_connection(uri, user, password):
    conn = Neo4jConnection(uri, user, password)
    with conn.driver.session() as session:
        result = session.run("RETURN 'Connexion OK' AS message")
        print(result.single()["message"])
    conn.close()

test_neo4j_connection(URI, USER, PASSWORD)

# -------------------------------
# Load, clean, and upload data
# -------------------------------
def main():
    # Load CSVs
    movies_df = pd.read_csv("data/tmdb_5000_movies.csv")
    credits_df = pd.read_csv("data/tmdb_5000_credits.csv")

    # Clean and merge
    loader = TMDBDataLoader(movies_df, credits_df)
    loader.merge_and_clean_data()

    # Load into Neo4j
    neo4j_loader = Neo4jLoader(loader.df)
    conn = Neo4jConnection(URI, USER, PASSWORD)
    neo4j_loader.load_nodes(conn)
    conn.close()
    print("Data loaded into Neo4j successfully.")

if __name__ == "__main__":
    main()
