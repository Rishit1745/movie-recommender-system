import streamlit as st
import pickle as pkl
import pandas as pd
import requests  #for api id

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=ceebd18a53ced04298a9935025224707&language=en-US'.format(movie_id))
    data = response.json()
    #st.write(data)
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movies_id = movies.iloc[i[0]].id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommend_movies_posters.append(fetch_poster(movies_id))
    return recommended_movies, recommend_movies_posters

movie_dict = pkl.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

similarity = pkl.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')
st.markdown("<h1 style='text-align: center; color: #FFA500;'>🎬 Movie Recommender 🎥</h1>", unsafe_allow_html=True)
st.write("Select a movie you like and get top 5 similar recommendations.")

selected_movie_name = st.selectbox(
     "Select a movie",
    movies['title'].values,)


if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])


