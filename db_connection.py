
"""
Database connection module for Neo4j.

Provides a simple wrapper class to manage Neo4j database connections and execute Cypher queries.
"""

from neo4j import GraphDatabase

class Neo4jConnection:
    """
    Wrapper for Neo4j database connection and query execution.
    """
    def __init__(self, uri: str, user: str, password: str):
        """
        Initialize the Neo4j connection.

        Args:
            uri (str): The Neo4j URI.
            user (str): The Neo4j username.
            password (str): The Neo4j password.
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self) -> None:
        """
        Close the Neo4j database connection.
        """
        self.driver.close()

    def query(self, query: str, parameters: dict = None):
        """
        Execute a Cypher query and return the results as a list.

        Args:
            query (str): The Cypher query to execute.
            parameters (dict, optional): Query parameters. Defaults to None.

        Returns:
            list: Query results.
        """
        with self.driver.session() as session:
            return list(session.run(query, parameters))
