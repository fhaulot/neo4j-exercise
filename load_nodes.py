import json

class Neo4jLoader:
    """
    Load movies, people (actors & directors), genres, and relationships into Neo4j.
    """
    def __init__(self, df):
        self.df = df

    def load_nodes(self, conn):
        for _, row in self.df.iterrows():
            # --- Movie ---
            conn.query(
                "MERGE (m:Movie {title: $title}) "
                "SET m.year = $year",
                {"title": row['title'], "year": int(row['year'])}
            )

            # --- Genre ---
            conn.query(
                "MERGE (g:Genre {name: $genre}) "
                "WITH g "
                "MATCH (m:Movie {title: $title}) "
                "MERGE (m)-[:HAS_GENRE]->(g)",
                {"title": row['title'], "genre": row['genre']}
            )

            # --- Director ---
            conn.query(
                "MERGE (p:Person {name: $director}) "
                "WITH p "
                "MATCH (m:Movie {title: $title}) "
                "MERGE (p)-[:DIRECTED]->(m)",
                {"title": row['title'], "director": row['director']}
            )

            # --- Actors ---
            for actor in row['actors']:
                conn.query(
                    "MERGE (a:Person {name: $actor}) "
                    "WITH a "
                    "MATCH (m:Movie {title: $title}) "
                    "MERGE (a)-[:ACTED_IN]->(m)",
                    {"title": row['title'], "actor": actor}
                )
