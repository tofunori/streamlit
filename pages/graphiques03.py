import streamlit as st
import geopandas as gpd
import plotly.express as px

# Define a list of available shapefiles
shapefiles = ["sol_500m.shp", "slope_500m.shp", "landcover_500m.shp", "sol_1km.shp", "slope_1km.shp", "landcover_1km.shp", "sol_2km.shp", "slope_2km.shp", "landcover_2km.shp", "roads_buffers_500m.shp"]

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
    "roads_buffers_500m.shp": {"category_col": "Site", "site_col": "Site", "area_col": "length"},
}

# Create a select box for file selection
selected_shapefile = st.sidebar.selectbox("Select a Shapefile", shapefiles)

# Load the selected shapefile
shapefile_path = f"files/{selected_shapefile}"
sol_data = gpd.read_file(shapefile_path)

# Apply the column mapping for the selected shapefile
mapping = column_mappings[selected_shapefile]
sol_data.rename(columns={mapping["category_col"]: "DESC_CAT", mapping["site_col"]: "Site", mapping["area_col"]: "area"}, inplace=True)
sol_data['area'] = sol_data['area'].round(1)

# Grouping by 'Site' and 'DESC_CAT' and summing 'area'
grouped_data = sol_data.groupby(['DESC_CAT', 'Site'])['area'].sum().reset_index()

# Create a Plotly bar graph
fig = px.bar(grouped_data, x='DESC_CAT', y='area', color='Site', barmode='group', title='Graphique', width=800, height=500)

# Update the axis labels
fig.update_layout(
    xaxis_title="Utilisation du sol par site",
    yaxis_title="Superficie en mètre carré"
)

# Display the graph in Streamlit
st.plotly_chart(fig)
