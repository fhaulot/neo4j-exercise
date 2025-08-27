"""
Movie Social Graph Queries in Neo4j
----------------------------------

This script connects to a Neo4j database using credentials stored in a .env file.
It runs three example queries:

1. Get all movies by a specific director.
2. Get all actors who have co-starred with a given actor.
3. Get all movies of a specific genre released after 2010.

Environment variables:
- URI: Neo4j connection URI (e.g., neo4j://localhost:7687)
- NEO4J_USER: Neo4j username
- NEO4J_PASSWORD: Neo4j password
"""

import os
from dotenv import load_dotenv
from db_connection import Neo4jConnection

# -------------------------------
# Setup connection
# -------------------------------
load_dotenv()
URI = os.getenv("URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

conn = Neo4jConnection(URI, USER, PASSWORD)

# -------------------------------
# Queries
# -------------------------------
def get_movies_by_director(director_name: str):
    """
    Return all movies directed by the given director.
    """
    query = """
    MATCH (d:Person)-[:DIRECTED]->(m:Movie)
    WHERE d.name = $director
    RETURN m.title AS title, m.year AS year
    ORDER BY m.year
    """
    return [record.data() for record in conn.query(query, {"director": director_name})]

def get_coactors(actor_name: str):
    """
    Return all actors who have acted in a movie with the given actor.
    """
    query = """
    MATCH (a:Person)-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(co:Person)
    WHERE a.name = $actor AND a <> co
    RETURN DISTINCT co.name AS coactor, m.title AS movie
    ORDER BY coactor
    """
    return [record.data() for record in conn.query(query, {"actor": actor_name})]

def get_movies_by_genre_after_year(genre_name: str, year: int = 2010):
    """
    Return all movies of a specific genre released after a certain year.
    """
    query = """
    MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre)
    WHERE g.name = $genre AND m.year > $year
    RETURN m.title AS title, m.year AS year
    ORDER BY m.year
    """
    return [record.data() for record in conn.query(query, {"genre": genre_name, "year": year})]

# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    print("Movies by director 'Christopher Nolan':")
    movies = get_movies_by_director("Christopher Nolan")
    for m in movies:
        print(f"{m['title']} ({m['year']})")

    print("\nActors who acted with 'Leonardo DiCaprio':")
    coactors = get_coactors("Leonardo DiCaprio")
    for c in coactors:
        print(f"{c['coactor']} in {c['movie']}")

    print("\nAction movies after 2010:")
    action_movies = get_movies_by_genre_after_year("Action", 2010)
    for m in action_movies:
        print(f"{m['title']} ({m['year']})")

# -------------------------------
# Close connection
# -------------------------------
conn.close()