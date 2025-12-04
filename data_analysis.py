import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from config import url_csv

# --- קריאת הנתונים ---
movies_data = pd.read_csv(url_csv)
movies_data = movies_data.drop_duplicates()
movies_data = movies_data.dropna(subset=["genre", "budget", "score", "year"])

st.title("🎬 Movie Data Explorer")

st.write("## Average Movie Budget, Grouped by Genre")

# --- ממוצע תקציב לפי ז'אנר ---
avg_budget = (
    movies_data
    .groupby('genre', as_index=False)['budget']
    .mean()
    .round()
)

genre = avg_budget['genre']
avg_bud = avg_budget['budget']

# --- Matplotlib Bar Chart ---
fig = plt.figure(figsize=(19, 10))
plt.bar(genre, avg_bud)
plt.xlabel('genre')
plt.ylabel('budget')
plt.title('Average Movie Budget per Genre')
st.pyplot(fig)

# --- Sidebar filters ---
score_list = movies_data['score'].unique().tolist()
genre_list = movies_data['genre'].unique().tolist()
year_list = sorted(movies_data['year'].unique().tolist())

with st.sidebar:
    st.header("Filters")
    
    score_range = st.slider(
        "Choose Score Range:",
        min_value=1.0,
        max_value=10.0,
        value=(3.0, 4.0)
    )
    
    selected_genres = st.multiselect(
        "Choose Genres:",
        genre_list,
        default=['Animation', 'Horror', 'Fantasy', 'Romance']
    )
    
    selected_year = st.selectbox(
        "Choose Year:",
        year_list
    )

# --- פילטר לנתונים ---
filtered_data = movies_data[
    (movies_data['score'].between(*score_range)) &
    (movies_data['genre'].isin(selected_genres)) &
    (movies_data['year'] == selected_year)
]

# --- תצוגה טבלאית של סרטים לפי הפילטרים ---
col1, col2 = st.columns([2, 3])

with col1:
    st.write("#### Movies Filtered by Genre and Year")
    
    dataframe_genre_year = (
        filtered_data
        .groupby(['name', 'genre'])['year']
        .sum()
        .reset_index()
    )
    
    st.dataframe(dataframe_genre_year, width=400)

# --- גרף Plotly שמתחשב בכל הפילטרים ---
with col2:
    st.write("#### Number of Movies per Genre (Based on Filters)")
    
    rating_count_year = (
        filtered_data
        .groupby('genre')['score']
        .count()
        .reset_index()
    )
    
    figpx = px.bar(
        rating_count_year,
        x='genre',
        y='score',
        title=f"Movies by Genre (Score {score_range[0]}–{score_range[1]}, Year {selected_year})"
    )
    
    st.plotly_chart(figpx, use_container_width=True)
