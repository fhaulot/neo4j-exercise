# -------------------------------
# Graph Updates
# -------------------------------
def add_actor_to_movie(actor_name: str, movie_title: str):
    """
    Create an ACTED_IN relationship between an actor and a movie.
    If the actor or movie does not exist, the function creates the nodes.
    """
    query = """
    MERGE (a:Person {name: $actor})
    MERGE (m:Movie {title: $movie})
    MERGE (a)-[:ACTED_IN]->(m)
    RETURN a.name AS actor, m.title AS movie
    """
    with driver.session() as session:
        result = session.run(query, {"actor": actor_name, "movie": movie_title})
        return result.single().data()

def add_missing_genre_to_movie(movie_title: str, genre_name: str):
    """
    Create a HAS_GENRE relationship between a movie and a genre.
    If the movie or genre does not exist, the function creates the nodes.
    """
    query = """
    MERGE (m:Movie {title: $movie})
    MERGE (g:Genre {name: $genre})
    MERGE (m)-[:HAS_GENRE]->(g)
    RETURN m.title AS movie, g.name AS genre
    """
    with driver.session() as session:
        result = session.run(query, {"movie": movie_title, "genre": genre_name})
        return result.single().data()

# -------------------------------
# Example usage for Step 5
# -------------------------------
if __name__ == "__main__":
    # Add a new actor to a movie
    print("\nAdding actor 'Tom Hanks' to movie 'Forrest Gump':")
    res = add_actor_to_movie("Tom Hanks", "Forrest Gump")
    print(res)

    # Add a missing genre to a movie
    print("\nAdding genre 'Adventure' to movie 'Inception':")
    res = add_missing_genre_to_movie("Inception", "Adventure")
    print(res)
