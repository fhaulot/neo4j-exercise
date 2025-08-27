import json
import pandas as pd

class TMDBDataLoader:
    """
    Class to load, clean, and preprocess TMDB movies and credits data.
    """
    def __init__(self, movies_df: pd.DataFrame, credits_df: pd.DataFrame):
        self.movies_df = movies_df
        self.credits_df = credits_df
        self.df = None  # Will hold cleaned merged data

    def merge_and_clean_data(self):
        """
        Merge movies and credits, keep essential columns, parse JSON, extract top info.
        """
        # Merge
        df = self.movies_df.merge(self.credits_df, left_on='id', right_on='movie_id')

        # Garder uniquement title_x (de movies) et ignorer title_y
        df = df.rename(columns={"title_x": "title"})
        if "title_y" in df.columns:
            df = df.drop(columns=["title_y"])

        # Keep only relevant columns
        df = df[['title', 'release_date', 'genres', 'cast', 'crew']]

        # Parse JSON columns
        for col in ['genres', 'cast', 'crew']:
            df[col] = df[col].apply(lambda x: json.loads(x) if pd.notnull(x) else [])

        # Extract year
        df['year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year

        # Extract first genre, director, top 5 actors
        df['genre'] = df['genres'].apply(lambda g: g[0]['name'] if g else None)
        df['director'] = df['crew'].apply(lambda c: next((m['name'] for m in c if m.get('job')=='Director'), None))
        df['actors'] = df['cast'].apply(lambda c: [a['name'] for a in sorted(c, key=lambda x: x.get('order',100))[:5]])

        # Drop rows without essential info
        df = df.dropna(subset=['title', 'year', 'director', 'genre'])
        df = df[df['actors'].map(len) > 0]

        self.df = df
