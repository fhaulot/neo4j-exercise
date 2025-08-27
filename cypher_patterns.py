
"""
Cypher Pattern Queries for Neo4j Movie Social Graph
--------------------------------------------------

This script connects to a Neo4j database using credentials from a .env file.
It provides example aggregation and pattern-matching queries, such as:
    - Most frequent actor-director collaborations
    - Most popular genres
    - Actor(s) with the most co-actor connections

Environment variables required:
    - URI: Neo4j connection URI (e.g., bolt://localhost:7687)
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
# Aggregation & Pattern Queries
# -------------------------------
def most_frequent_collaborators(limit: int = 5):
    """
    Return the top actor-director pairs who worked together most frequently.
    """
    query = """
    MATCH (a:Person)-[:ACTED_IN]->(m:Movie)<-[:DIRECTED]-(d:Person)
    RETURN a.name AS actor, d.name AS director, count(m) AS collaborations
    ORDER BY collaborations DESC
    LIMIT $limit
    """
    return [record.data() for record in conn.query(query, {"limit": limit})]


def most_popular_genres(limit: int = 5):
    """
    Return the genres with the most movies.
    """
    query = """
    MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre)
    RETURN g.name AS genre, count(m) AS movie_count
    ORDER BY movie_count DESC
    LIMIT $limit
    """
    return [record.data() for record in conn.query(query, {"limit": limit})]


def actor_with_most_connections(limit: int = 1):
    """
    Return the actor(s) with the most co-actor connections.
    """
    query = """
    MATCH (a:Person)-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(co:Person)
    WHERE a <> co
    RETURN a.name AS actor, count(DISTINCT co) AS connections
    ORDER BY connections DESC
    LIMIT $limit
    """
    return [record.data() for record in conn.query(query, {"limit": limit})]

# -------------------------------
# Example usage for Cypher patterns
# -------------------------------
if __name__ == "__main__":
    # Most frequent actor-director pairs
    print("\nTop 5 actor-director collaborations:")
    for rec in most_frequent_collaborators():
        print(f"{rec['actor']} & {rec['director']} - {rec['collaborations']} movies")

    # Most popular genres
    print("\nTop 5 genres by number of movies:")
    for rec in most_popular_genres():
        print(f"{rec['genre']} - {rec['movie_count']} movies")

    # Actor with most connections
    print("\nActor with the most co-actor connections:")
    for rec in actor_with_most_connections():
        print(f"{rec['actor']} - {rec['connections']} co-actors")

    conn.close()