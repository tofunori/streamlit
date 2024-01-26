import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

st.set_page_config(
    layout="wide",
    page_icon="🧊",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!",
    }
    )

st.title('Carte intéractive des données')
col1, col2 = st.columns([8.5, 1.5])


# Dropdown for basemap selection
with col2:
    dropdown = st.selectbox("Select a basemap", ["TERRAIN", "HYBRID", "ROADMAP", "SATELLITE"])

# Initialize the map
m = leafmap.Map()

m.add_basemap(dropdown)

default_shapefiles = {
    "500m": "Utilisation du sol 500m",
    "1km": "Utilisation du sol 1km",
    "2km": "Utilisation du sol 2km"
}

# Organize file paths by distance categories
buffers = {
    "500m": {
        "Utilisation du sol 500m": "files/sol_500m.shp",
        "Pente 500m": "files/slope_500m.shp",
        "Couverture forestière 500m": "files/landcover_500m.shp",
        "Rivières 500m": "files/rivieres_buffers_500m.shp",
        "Réseau ferroviaire 500m": "files/railroad_buffers_500m.shp",
        "Routes 500m": "files/roads_buffers_500m.shp",
        
    },
    "1km": {
        "Utilisation du sol 1km": "files/sol_1km.shp",
        "Pente 1km": "files/slope_1km.shp",
        "Couverture forestière 1km": "files/landcover_1km.shp",
        "Rivières 1km": "files/rivieres_buffers_1km.shp",
        "Réseau ferroviaire 1km": "files/railroad_buffers_1km.shp",
        "Routes 1km": "files/roads_buffers_1km.shp",
        
    },
    "2km": {
        "Utilisation du sol 2km": "files/sol_2km.shp",
        "Pente 2km": "files/slope_2km.shp",
        "Couverture forestière 2km": "files/landcover_2km.shp",
        "Rivières 2km": "files/rivieres_buffers_2km.shp",
        "Réseau ferroviaire 2km": "files/railroad_buffers_2km_2.shp",
        "Routes 2km": "files/roads_buffers_2km.shp",
        
    }
}

# Add radio button for buffer selection
selected_buffer = st.sidebar.radio("**Sélection des buffers:**", ["500m", "1km", "2km"])

st.sidebar.markdown("**Sélection des couches:**")

# For each shapefile in the selected buffer, add a toggle switch
selected_shapefiles = []
for shapefile_name in buffers[selected_buffer].keys():
    is_default = shapefile_name == default_shapefiles[selected_buffer]
    is_checked = st.sidebar.checkbox(f"{shapefile_name}", value=is_default, key=f"{selected_buffer}_{shapefile_name}")
    if is_checked:
        selected_shapefiles.append(shapefile_name)
        

# Function to customize and add each shapefile to the map
def add_shapefile_to_map(shapefile_name, gdf):
    if shapefile_name == "Utilisation du sol 500m":
        m.add_data(
            data=gdf,
            column='DESC_CAT',  # Replace 'DESC_CAT' with actual column name
            key_on='feature.properties.DESC_CAT',
            add_legend=False,
            cmap='Set1',
            legend_name='Category'
        )
        
    elif shapefile_name == "Couverture forestière 500m":
        m.add_data(
            data=gdf,
            column='TYPE_COUV',  # Replace 'DESC_CAT' with actual column name
            key_on='feature.properties.TYPE_COUV',
            add_legend=False,
            cmap='Paired',
            legend_name='Category'
        )   
        
    elif shapefile_name == "Pente 500m":
        m.add_data(
            data=gdf,
            column='CL_PENT',  # Replace 'DESC_CAT' with actual column name
            key_on='feature.properties.CL_PENT',
            add_legend=False,
            cmap='Set3',
            legend_name='Category'
        ) 
        
    elif shapefile_name == "Rivières 500m":
        def style(feature):
            return {
                'color': 'green',  # Set your desired line color here
                'weight': 1.5,       # Set the line width
                'opacity': 1
            }
        m.add_gdf(
            gdf=gdf,
            layer_name="Rivières 500m",
            style_function=style,
            zoom_to_layer=True
            # You can add other parameters as needed
        )
    #Railroad   
    elif shapefile_name == "Réseau ferroviaire 500m":
        def route_style(feature):
            return {
                'color': 'red',  # Set your desired line color here
                'weight': 3,       # Set the line width
                'opacity': 1
            }
        m.add_gdf(
            gdf=gdf,
            layer_name="Réseau ferroviaire 500m",
            style_function=route_style,
            zoom_to_layer=True
            # You can add other parameters as needed
        )
              
    elif shapefile_name == "Routes 500m":
        # Define a style function for custom line color
        def route_style(feature):
            return {
                'color': 'black',  # Set your desired line color here
                'weight': 2,       # Set the line width
                'opacity': 1
            }

        m.add_gdf(
            gdf=gdf,
            layer_name="Routes 500m",
            style_function=route_style
            # You can add other parameters as needed
        )
    #1km buffer
    if shapefile_name == "Utilisation du sol 1km":
        m.add_data(
            data=gdf,
            column='DESC_CAT',  # Replace 'DESC_CAT' with actual column name
            key_on='feature.properties.DESC_CAT',
            add_legend=False,
            cmap='Set1',
            legend_name='Category'
        )
        
    elif shapefile_name == "Couverture forestière 1km":
        m.add_data(
            data=gdf,
            column='TYPE_COUV',  # Replace 'DESC_CAT' with actual column name
            key_on='feature.properties.TYPE_COUV',
            add_legend=False,
            cmap='Set1',
            legend_name='Category'
        )   
        
    elif shapefile_name == "Pente 1km":
        m.add_data(
            data=gdf,
            column='CL_PENT',  # Replace 'DESC_CAT' with actual column name
            key_on='feature.properties.CL_PENT',
            add_legend=False,
            cmap='Set3',
            legend_name='Category'
        )            

    elif shapefile_name == "Rivières 1km":
        def route_style(feature):
            return {
                'color': 'blue',  # Set your desired line color here
                'weight': 2,       # Set the line width
                'opacity': 1
            }

        m.add_gdf(
            gdf=gdf,
            layer_name="Rivières 1km",
            style_function=route_style
            # You can add other parameters as needed
        )
       
    elif shapefile_name == "Réseau ferroviaire 1km":
        def style(feature):
            return {
                'color': 'red',  # Set your desired line color here
                'weight': 3,       # Set the line width
                'opacity': 1
            }
        m.add_gdf(
            gdf=gdf,
            layer_name="Réseau ferroviaire 1km",
            style_function=style,
            zoom_to_layer=True
            # You can add other parameters as needed
        )
        
   
    elif shapefile_name == "Routes 1km":
        def style(feature):
            return {
                'color': 'black',  # Set your desired line color here
                'weight': 2,       # Set the line width
                'opacity': 1
            }
        m.add_gdf(  
            gdf=gdf,
            layer_name="Routes 1km",
            style_function=style
            # You can add other parameters as needed
        )
        
    #2km buffer

    if shapefile_name == "Utilisation du sol 2km":
        m.add_data(
            data=gdf,
            column='DESC_CAT',  # Replace 'DESC_CAT' with actual column name
            key_on='feature.properties.DESC_CAT',
            add_legend=False,
            cmap='Set1',
            legend_name='Category'
        )

    elif shapefile_name == "Rivières 2km":
        
        def style(feature):
            return {
                'color': 'blue',  # Set your desired line color here
                'weight': 2,       # Set the line width
                'opacity': 1
            }
        m.add_gdf(
            gdf=gdf,
            layer_name="Rivières 2km",
            style_function=style,
            zoom_to_layer=True
            # You can add other parameters as needed
        )
       
    elif shapefile_name == "Réseau ferroviaire 2km":
        def style(feature):
            return {
                'color': 'red',  # Set your desired line color here
                'weight': 3,       # Set the line width
                'opacity': 1
            }
        m.add_gdf(
            gdf=gdf,
            layer_name="Réseau ferroviaire 2km",
            style_function=style,
            zoom_to_layer=True
        )
        
    elif shapefile_name == "Couverture forestière 2km":
        m.add_data(
            data=gdf,
            column='TYPE_COUV',  # Replace 'DESC_CAT' with actual column name
            key_on='feature.properties.TYPE_COUV',
            add_legend=False,
            cmap='Set1',
            legend_name='Category'
        )   
        
    elif shapefile_name == "Pente 2km":
        m.add_data(
            data=gdf,
            column='CL_PENT',  # Replace 'DESC_CAT' with actual column name
            key_on='feature.properties.CL_PENT',
            add_legend=False,
            cmap='Set3',
            legend_name='Category'
        )       
    elif shapefile_name == "Routes 2km":
        def style(feature):
            return {
                'color': 'black',  # Set your desired line color here
                'weight': 2,       # Set the line width
                'opacity': 1
            }
        m.add_gdf(
            gdf=gdf,
            layer_name="Routes 2km",
            style_function=style
            # You can add other parameters as needed
        )
    
   

# Loop through each selected shapefile and add it to the map
for shapefile_name in selected_shapefiles:
    gdf = gpd.read_file(buffers[selected_buffer][shapefile_name])
    add_shapefile_to_map(shapefile_name, gdf)

# Display the map in Streamlit
with col1:
    m.to_streamlit()

