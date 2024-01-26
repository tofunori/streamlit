import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import altair as alt

gpd.read_csv("files/csv/landcover_1km.csv")


alt.Chart(gpd.read_csv("files/csv/landcover_1km.csv")).mark_bar()