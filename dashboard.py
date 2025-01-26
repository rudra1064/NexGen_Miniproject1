import streamlit as st
import matplotlib.pyplot as plt
from collections import defaultdict

# File paths
users_file_path = r"C:\Users\kamle\Desktop\ml-1m\users.dat"
ratings_file_path = r"C:\Users\kamle\Desktop\ml-1m\ratings.dat"
movies_file_path = r"C:\Users\kamle\Desktop\ml-1m\movies.dat"

# Load users data
def load_users(file_path):
    users_data = {}
    with open(file_path, 'r') as file:
        for line in file:
            user_id, gender, age, occupation, _ = line.strip().split('::')
            users_data[int(user_id)] = {'gender': gender, 'age': int(age), 'occupation': occupation}
    return users_data

# Load movies data
def load_movies(file_path):
    movies_data = {}
    with open(file_path, 'r') as file:
        for line in file:
            movie_id, title, genres = line.strip().split('::')
            movies_data[int(movie_id)] = {'title': title, 'genres': genres.split('|')}
    return movies_data

# Load ratings data
def load_ratings(file_path):
    ratings_data = defaultdict(list)
    with open(file_path, 'r') as file:
        for line in file:
            user_id, movie_id, rating, _ = map(int, line.strip().split('::'))
            ratings_data[movie_id].append(rating)
    return ratings_data

# Compute average ratings for movies
def calculate_average_ratings(ratings_data):
    avg_ratings = {}
    for movie_id, ratings in ratings_data.items():
        avg_ratings[movie_id] = sum(ratings) / len(ratings)
    return avg_ratings

# Data loading
st.title("MovieLens Dashboard")
st.sidebar.header("Dataset Overview")
st.sidebar.write("Using MovieLens dataset (users, ratings, movies).")

users = load_users(users_file_path)
movies = load_movies(movies_file_path)
ratings = load_ratings(ratings_file_path)
avg_ratings = calculate_average_ratings(ratings)

# Top-rated movies
st.header("Top-Rated Movies")
min_ratings = st.slider("Minimum number of ratings", min_value=1, max_value=100, value=10)
top_movies = [
    (movies[movie_id]['title'], avg_rating, len(ratings[movie_id]))
    for movie_id, avg_rating in avg_ratings.items()
    if len(ratings[movie_id]) >= min_ratings
]
top_movies = sorted(top_movies, key=lambda x: x[1], reverse=True)[:10]

st.table({"Title": [x[0] for x in top_movies], "Average Rating": [x[1] for x in top_movies], "Number of Ratings": [x[2] for x in top_movies]})

# Genre popularity
st.header("Genre Popularity")
genre_popularity = defaultdict(int)
for movie_id, movie in movies.items():
    for genre in movie['genres']:
        genre_popularity[genre] += len(ratings[movie_id])

genres, counts = zip(*sorted(genre_popularity.items(), key=lambda x: x[1], reverse=True))
fig, ax = plt.subplots()
ax.bar(genres, counts, color='skyblue')
ax.set_xlabel("Genres")
ax.set_ylabel("Number of Ratings")
ax.set_title("Most Popular Genres")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Gender-based analysis
st.header("Gender-Based Rating Patterns")
gender_ratings = {'M': defaultdict(list), 'F': defaultdict(list)}
for user_id, user in users.items():
    gender = user['gender']
    for movie_id, rating in ratings.items():
        if user_id in ratings:
            for rate in ratings[movie_id]:
                gender_ratings[gender][movie_id].append(rate)

gender_avg_ratings = {
    gender: {movie_id: sum(rates) / len(rates) for movie_id, rates in movie_ratings.items()}
    for gender, movie_ratings in gender_ratings.items()
}

male_ratings = list(gender_avg_ratings['M'].values())
female_ratings = list(gender_avg_ratings['F'].values())

fig, ax = plt.subplots()
ax.boxplot([male_ratings, female_ratings], labels=["Male", "Female"], patch_artist=True, boxprops=dict(facecolor="skyblue"))
ax.set_title("Gender-Based Average Ratings")
ax.set_ylabel("Average Ratings")
st.pyplot(fig)

st.write("Dashboard built with MovieLens dataset and Streamlit.")
