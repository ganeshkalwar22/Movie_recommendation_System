import streamlit as st
import pickle
import requests

st.title('Movie Recommender System')
movies=pickle.load(open('movies.pkl','rb'))
similar=pickle.load(open('simi.pkl','rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distance=similar[movie_index]
    movie_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
    recommend_movies=[]
    recommend_poster=[]
  
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_poster.append(fetch_poster(movie_id))
        recommend_movies.append(movies.iloc[i[0]].title)
    return recommend_movies,recommend_poster
    
  

selected_movie_name = st.selectbox(
    "Type or select a movie from the dropdown",
    (movies['title'].values),
)

if st.button('Show Recommendation'):
    recommend_movie_name,recommend_movie_poster=recommend(selected_movie_name)
    cols = st.columns(5)

    for i in range(5):
            with cols[i]:
                    st.text(recommend_movie_name[i])
                    st.image(recommend_movie_poster[i])
    
                

    
        