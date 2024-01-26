import streamlit as st
import geopandas as gpd
import plotly.express as px
import altair as alt

# Define a list of available shapefiles
shapefiles = ["sol_500m.shp", "slope_500m.shp", "landcover_500m.shp", "sol_1km.shp", "slope_1km.shp", "landcover_1km.shp", "sol_2km.shp", "slope_2km.shp", "landcover_2km.shp", "roads_buffers_500m.shp", "rivieres_buffers_500m.shp", "railroad_buffers_500m.shp", "roads_buffers_1km.shp", "rivieres_buffers_1km.shp", "railroad_buffers_1km.shp", "roads_buffers_2km.shp", "rivieres_buffers_2km.shp", "railroad_buffers_2km_2.shp"]

# Define a mapping for each shapefile if they have different column names
column_mappings = {
    "sol_500m.shp": {"category_col": "DESC_CAT", "site_col": "Site", "area_col": "area"},
    "slope_500m.shp": {"category_col": "CL_PENT", "site_col": "Site", "area_col": "area"},
    "landcover_500m.shp": {"category_col": "TYPE_COUV", "site_col": "Site", "area_col": "area"},
    "sol_1km.shp": {"category_col": "DESC_CAT", "site_col": "Site", "area_col": "area"},
    "slope_1km.shp": {"category_col": "CL_PENT", "site_col": "Site", "area_col": "area"},
    "landcover_1km.shp": {"category_col": "TYPE_COUV", "site_col": "Site", "area_col": "area"},
    "sol_2km.shp": {"category_col": "DESC_CAT", "site_col": "Site", "area_col": "area"},
    "slope_2km.shp": {"category_col": "CL_PENT", "site_col": "Site", "area_col": "area"},
    "landcover_2km.shp": {"category_col": "TYPE_COUV", "site_col": "Site", "area_col": "area"},
    "roads_buffers_500m.shp": {"length_col": "length", "site_col": "Site"},
    "rivieres_buffers_500m.shp": {"length_col": "length", "site_col": "Site"},
    "railroad_buffers_500m.shp": {"length_col": "length", "site_col": "Site"},
    "roads_buffers_1km.shp": {"length_col": "length", "site_col": "Site"},
    "rivieres_buffers_1km.shp": {"length_col": "length", "site_col": "Site"},
    "railroad_buffers_1km.shp": {"length_col": "length", "site_col": "Site"},
    "roads_buffers_2km.shp": {"length_col": "length", "site_col": "Site"},
    "rivieres_buffers_2km.shp": {"length_col": "length", "site_col": "Site"},
    "railroad_buffers_2km_2.shp": {"length_col": "length", "site_col": "Site"},
}


# Create a select box for file selection
selected_shapefile = st.sidebar.selectbox("Select a Shapefile", shapefiles)

# Load the selected shapefile
shapefile_path = f"files/{selected_shapefile}"
sol_data = gpd.read_file(shapefile_path)

if selected_shapefile in ["roads_buffers_500m.shp", "rivieres_buffers_500m.shp", "railroad_buffers_500m.shp", "roads_buffers_1km.shp", "rivieres_buffers_1km.shp", "railroad_buffers_1km.shp", "roads_buffers_2km.shp", "rivieres_buffers_2km.shp", "railroad_buffers_2km.shp"]:
    mapping = column_mappings[selected_shapefile]
    sol_data.rename(columns={mapping["length_col"]: "length", mapping["site_col"]: "Site"}, inplace=True)

    # Convert 'Site' to string
    sol_data['Site'] = sol_data['Site'].astype(str)

    # Grouping by 'Site' and summing 'length'
    grouped_data = sol_data.groupby('Site')['length'].sum().reset_index()

    # Create an Altair bar chart
    chart = alt.Chart(grouped_data).mark_bar().encode(
        x='Site:N',  # The ':N' tells Altair that the column is nominal (categorical)
        y='length:Q',  # The ':Q' tells Altair that the column is quantitative
        color='Site:N',
        tooltip=['Site:N', 'length:Q']
    ).properties(
        title='Total Length by Site',
        width=800,
        height=500
    )

    # Display the chart in Streamlit
    st.altair_chart(chart)
    
else:
    # Apply the column mapping for other shapefiles
    mapping = column_mappings[selected_shapefile]
    sol_data.rename(columns={mapping["category_col"]: "DESC_CAT", mapping["site_col"]: "Site", mapping["area_col"]: "area"}, inplace=True)
    sol_data['area'] = sol_data['area'].astype(float).round(1)

    # Grouping by 'Site' and 'DESC_CAT' and summing 'area'
    grouped_data = sol_data.groupby(['DESC_CAT', 'Site'])['area'].sum().reset_index()

    # Create a Plotly bar graph for area data
    fig = px.bar(
        grouped_data, 
        x='DESC_CAT', 
        y='area', 
        color='Site', 
        barmode='group', 
        title='Graphique', 
        width=800, 
        height=500
    )

    fig.update_layout(
        xaxis_title="Utilisation du sol par site", 
        yaxis_title="Superficie en mètre carré"
    )

    # Display the graph in Streamlit
    st.plotly_chart(fig)