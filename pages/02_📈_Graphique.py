import streamlit as st
import geopandas as gpd
import plotly.express as px
import altair as alt

st.set_page_config(page_icon="📈")

st.write(" Cette page permet de visualiser à l'aide d'un graphique à bar, les différentes variables analysées et l'étendue de leur couverture au sein de chaque zone tampon.")

# Define a list of available shapefiles
shapefiles = [
    "sol_500m.shp", "slope_500m.shp", "landcover_500m.shp",
    "sol_1km.shp", "slope_1km.shp", "landcover_1km.shp",
    "sol_2km.shp", "slope_2km.shp", "landcover_2km.shp",
    "roads_buffers_500m.shp", "rivieres_buffers_500m.shp", "railroad_buffers_500m.shp",
    "roads_buffers_1km.shp", "rivieres_buffers_1km.shp", "railroad_buffers_1km.shp",
    "roads_buffers_2km.shp", "rivieres_buffers_2km.shp", "railroad_buffers_2km_2.shp"
]

# Define a mapping for each shapefile if they have different column names
column_mappings = {
    "sol_500m.shp": {"category_col": "DESC_CAT", "site_col": "Site", "area_col": "area"},
    "sol_1km.shp": {"category_col": "DESC_CAT", "site_col": "Site", "area_col": "area"},
    "sol_2km.shp": {"category_col": "DESC_CAT", "site_col": "Site", "area_col": "area"},
    "slope_500m.shp": {"category_col": "CL_PENT", "site_col": "Site", "area_col": "area"},
    "slope_1km.shp": {"category_col": "CL_PENT", "site_col": "Site", "area_col": "area"},
    "slope_2km.shp": {"category_col": "CL_PENT", "site_col": "Site", "area_col": "area"},
    "landcover_500m.shp": {"category_col": "TYPE_COUV", "site_col": "Site", "area_col": "area"},
    "landcover_1km.shp": {"category_col": "TYPE_COUV", "site_col": "Site", "area_col": "area"},
    "sol_2km.shp": {"category_col": "DESC_CAT", "site_col": "Site", "area_col": "area"},
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

custom_titles = {
'landcover_1km.shp': 'Couverture forestière - 1km Buffer',
'landcover_2km.shp': 'Couverture forestière - 2km Buffer',
 'landcover_500m.shp': 'Couverture forestière - 500m Buffer',
 'railroad_buffers_1km.shp': 'Réseau férroviaire - 1km Buffer',
 'railroad_buffers_2km_2.shp': 'Réseau férroviaire - 2km Buffer',
 'railroad_buffers_500m.shp': 'Réseau férroviaire - 500m Buffer',
 'rivieres_buffers_1km.shp': 'Rivières - 1km Buffer',
 'rivieres_buffers_2km.shp': 'Rivières - 2km Buffer',
 'rivieres_buffers_500m.shp': 'Rivières - 500m Buffer',
 'roads_buffers_1km.shp': 'Routes - 1km Buffer',
 'roads_buffers_2km.shp': 'Routes - 2km Buffer',
 'roads_buffers_500m.shp': 'Routes - 500m Buffer',
 'slope_1km.shp': 'Pente - 1km Buffer',
 'slope_2km.shp': 'Pente - 2km Buffer',
 'slope_500m.shp': 'Pente - 500m Buffer',
 'sol_1km.shp': 'Utilisation du sol - 1km Buffer',
 'sol_2km.shp': 'Utilisation du sol - 2km Buffer',
 'sol_500m.shp': 'Utilisation du sol - 500m Buffer'}
    # ... add custom titles for all shapefiles ...

# Create a select box for file selection with custom titles
selected_title = st.sidebar.selectbox("Sélectionner une couche:", list(custom_titles.values()))

# Find the original shapefile name corresponding to the selected title
selected_shapefile = [key for key, value in custom_titles.items() if value == selected_title][0]

# Load the selected shapefile
shapefile_path = f"files/{selected_shapefile}"
sol_data = gpd.read_file(shapefile_path)

# Get the custom title for the selected shapefile
chart_title = custom_titles.get(selected_shapefile, "Graphique")

# Check if the selected shapefile has 'length' and 'Site' columns
if selected_shapefile in column_mappings.keys() and 'length_col' in column_mappings[selected_shapefile]:
    mapping = column_mappings[selected_shapefile]
    sol_data.rename(columns={mapping["length_col"]: "length", mapping["site_col"]: "Site"}, inplace=True)

    # Convert 'Site' to string
    sol_data['Site'] = sol_data['Site'].astype(str)

    # Grouping by 'Site' and summing 'length'
    grouped_data = sol_data.groupby('Site')['length'].sum().reset_index()

    # Create an Altair bar chart
    chart = alt.Chart(grouped_data).mark_bar().encode(
        x=alt.X('Site:N', axis=alt.Axis(title='Site')),  # Change X-axis label
        y=alt.Y('length:Q', axis=alt.Axis(title='Somme des longueurs en mètre')),
        color='Site:N',
        tooltip=['Site:N', 'length:Q']
    ).properties(
        title=chart_title,  # Use the custom title
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
        title=chart_title,  # Use the custom title
        width=800, 
        height=500
    )

    fig.update_layout(
        xaxis_title="Résultats groupés par catégorie", 
        yaxis_title="Superficie en mètre carré"
    )

    # Display the graph in Streamlit
    st.plotly_chart(fig)