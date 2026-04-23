# Movie Recommender System - Model Training Guide

## How the Models Were Built (Simple Steps)

This project builds a movie recommender system using machine learning. Here's a simple breakdown of how the models were created:

### 1. Data Preparation
- Loaded movie data from `tmdb_5000_movies.csv` and credits from `tmdb_5000_credits.csv`
- Merged the datasets on the 'title' column
- Kept only important columns: movie_id, title, overview, genres, keywords, cast, crew
- Removed any rows with missing data

### 2. Feature Extraction
- **Genres**: Extracted genre names from JSON-like text
- **Keywords**: Pulled out key movie keywords
- **Cast**: Took the top 3 actors from the cast list
- **Crew**: Got the director's name
- **Overview**: Split the movie description into words

### 3. Data Cleaning
- Removed spaces from names (e.g., "Sam Worthington" → "SamWorthington") to avoid confusion between first/last names
- Combined all features (overview, genres, keywords, cast, crew) into a single "tags" column for each movie

### 4. Vectorization
- Used CountVectorizer to convert the text "tags" into numbers (vectors)
- Limited to 5000 most common words, ignoring common English stop words
- This creates a matrix where each movie is a vector of word counts

### 5. Similarity Calculation
- Computed cosine similarity between all movie vectors
- Cosine similarity measures how similar two movies are based on their content
- Higher similarity score means more similar movies

### 6. Model Saving
- Saved the processed movie list as `movie_list.pkl`
- Saved the similarity matrix as `similarity.pkl`
- These files are used by the app to make recommendations

### How to Train/Recreate the Model
1. Run the `model_building.ipynb` notebook in Jupyter
2. Make sure you have the CSV files in the same folder
3. Install required packages: pandas, numpy, scikit-learn
4. Execute all cells in order
5. The pickle files will be created automatically

### What the Model Does
- Takes a movie title as input
- Finds the most similar movies using the similarity scores
- Returns top 5 recommendations

For more details, check the `model_building.ipynb` notebook.

model dataset is in the archive.zip file 