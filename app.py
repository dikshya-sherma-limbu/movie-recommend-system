import streamlit as st
import pickle
import pandas as pd
import requests


# de-serialize the movies_dict
movies_dict =pickle.load(open('movies_dict.pkl','rb'))
#re-create the dataframe of this dictionary
movies = pd.DataFrame(movies_dict)

#de-serialize
similarity = pickle.load(open('similarity.pkl','rb'))


def  fetch_poster(movie_id):
   headers= {
      "accept": "application/json",
      "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxOGM3MDBkZjNhZTE2NzhkMzRmOThjZWNjN2IyMDM0OCIsIm5iZiI6MTczNjEwNzM2MS45MTYsInN1YiI6IjY3N2FlNTYxMWEyZGY1OWFkMzc1MDYxNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.BRqUznndQMHwIavH52GSzTII3e2OTOrx43U4E84OdTI"
   }
   url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
   response = requests.get(url, headers=headers)
   response.raise_for_status()  # Raise an error for bad responses

   data =  response.json()
   return 'https://image.tmdb.org/t/p/w500/' +data['poster_path']

#get the list of 5 similar movies
def recommend(movie):
   # get the index position of the movie
   movie_index = movies[movies['title'] == movie].index[0]

   # get the 4806 similarity distances with the given movie
   distances = similarity[movie_index]
   # list and enumarate - to keep the index position of the distance:
   # meaning to keep which distance is of which movie so later to the movie title
   # sort and store
   movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
   recommended_movies =[]
   recommended_movies_posters=[]
   for i in movies_list:
      movie_id = movies.iloc[i[0]].movie_id
      recommended_movies.append(movies.iloc[i[0]].title)

      # fetch poster from API'

      recommended_movies_posters.append(fetch_poster(movie_id))
   return  recommended_movies, recommended_movies_posters

# Custom CSS for wider text

st.title('Movie Recommender System')

with st.form("my_form"):
   st.write("Choose the movie")
   selected_movie_name = st.selectbox('Pick a Movie', movies['title'].values)
   if st.form_submit_button('Recommend'):
     names,posters= recommend(selected_movie_name)

     col1, col2, col3,col4,col5 = st.columns(5, gap="small")

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





