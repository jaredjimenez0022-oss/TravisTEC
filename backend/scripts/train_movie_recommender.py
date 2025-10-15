"""Train a simple movie recommendation model using collaborative filtering.

Uses the movies.csv and ratings.csv datasets to build a basic recommendation system.
"""
import pandas as pd
from pathlib import Path
from sklearn.neighbors import NearestNeighbors
import joblib

MOVIES_DATA = Path(__file__).parent.parent / 'datasets' / 'movies.csv'
RATINGS_DATA = Path(__file__).parent.parent / 'datasets' / 'ratings.csv'
MODEL_OUT = Path(__file__).parent.parent / 'models' / 'movie_recommender.joblib'

def main():
    if not MOVIES_DATA.exists() or not RATINGS_DATA.exists():
        print(f"Datasets not found. Skipping training.")
        return

    # Load datasets
    movies = pd.read_csv(MOVIES_DATA)
    ratings = pd.read_csv(RATINGS_DATA)
    
    print(f"Loaded {len(movies)} movies and {len(ratings)} ratings")
    
    # Create user-item matrix
    user_item_matrix = ratings.pivot_table(
        index='userId', 
        columns='movieId', 
        values='rating'
    ).fillna(0)
    
    # Train KNN model for collaborative filtering
    model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20)
    model.fit(user_item_matrix.T)
    
    # Save model and metadata
    model_data = {
        'model': model,
        'user_item_matrix': user_item_matrix,
        'movies': movies
    }
    
    MODEL_OUT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model_data, MODEL_OUT)
    print(f'Saved movie recommender model to {MODEL_OUT}')
    print(f'Model can recommend from {len(movies)} movies')

if __name__ == '__main__':
    main()
