import streamlit as st
import altair as alt
import geopandas as gpd

# Load the data
landcover = gpd.read_file("files/roads_buffers_1km.shp")

# Convert to a Pandas DataFrame and assume 'landcover_type' is an attribute to plot
landcover_df = landcover.drop(columns='geometry')
landcover_counts = landcover_df.groupby('Site')['length'].sum().reset_index()
landcover_counts.columns = ['Site', 'length']

# Create an Altair bar chart
chart = alt.Chart(landcover_counts).mark_bar().encode(
    x='Site',
    y='length'
)

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)

