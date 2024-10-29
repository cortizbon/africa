import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium
from folium.plugins import HeatMap
import geopandas as gpd

st.set_page_config(layout='wide')

st.title("Conflicto en África")

df = pd.read_csv('sum_data_africa.csv')
gdf = gpd.read_file('data_etnias.geojson')


events = df['event_type'].unique().tolist()
years = df['year'].sort_values().unique().tolist()

col1, col2, col3 = st.columns(3)
with col1:
    year = st.select_slider("Seleccione un año: ", years)
with col2:
    event = st.selectbox("Seleccione un evento: ", events)
with col3:
    show_etnias = st.checkbox("Mostrar etnias")
    show_conflict = st.checkbox("Mostrar conflicto")

filtro = df[(df['year'] == year) & (df['event_type'] == event)]

data = filtro[['latitude', 'longitude']].values

m = folium.Map([9.1, 18.2], zoom_start=3.2)
if show_etnias:
    gdf = gdf.to_crs(epsg=3857)

    folium.GeoJson(
        gdf,
        name="geojson",
        style_function=lambda feature: {
            "fillColor": "gray",       # Purple fill color
            "color": "black",           # Light purple outline color
            "weight": 0.6,
            "fillOpacity": 0.2
        }
    ).add_to(m)
if show_conflict:
    HeatMap(data,    gradient={
    '0.0': 'rgb(0, 0, 0)',
    '0.4': 'rgb(24, 53, 103)',
    '0.6': 'rgb(46, 100, 158)',
    '0.8': 'rgb(23, 173, 203)',
    '1.0': 'rgb(0, 250, 250)'
    }).add_to(m)

st_data = st_folium(m, width=1400)

