import streamlit as st
import geopandas as gpd
import altair as alt

# Dictionary of buffers with available columns for each shapefile
buffers = {
    "500m": {
        "Utilisation du sol 500m": ("files/sol_500m.shp", ['DESC_CAT', 'Site']),
        "Pente 500m": ("files/slope_500m.shp", ['CL_PENT', 'Site']),	
        "Couverture forestière 500m": ("files/landcover_500m.shp", ["TYPE_COUV"]),
        "Rivières 500m": ("files/rivieres_buffers_500m.shp", ['length']),
        "Réseau ferroviaire 500m": ("files/railroad_buffers_500m.shp", ['length']),
        "Routes 500m": ("files/roads_buffers_500m.shp", ['length', 'Site'])	
        
    },
    "1km": {
        "Utilisation du sol 1km": ("files/sol_1km.shp", ['DESC_CAT']),
        "Pente 1km": ("files/slope_1km.shp", ['CL_PENT']),
        "Couverture forestière 1km": ("files/landcover_1km.shp", ["TYPE_COUV"]),
        "Rivières 1km": ("files/rivieres_buffers_1km.shp", ['length']),
        "Réseau ferroviaire 1km": ("files/railroad_buffers_1km.shp", ['length']),
        "Routes 1km": ("files/roads_buffers_1km.shp", ['length']),
        
    },
    "2km": {
        "Utilisation du sol 2km": ("files/sol_2km.shp", ['DESC_CAT']),
        "Pente 2km": ("files/slope_2km.shp", ['CL_PENT']),
        "Couverture forestière 2km": ("files/landcover_2km.shp", ["TYPE_COUV"]),
        "Rivières 2km": ("files/rivieres_buffers_2km.shp", ['length']),
        "Réseau ferroviaire 2km": ("files/railroad_buffers_2km_2.shp", ['length']),
        "Routes 2km": ("files/roads_buffers_2km.shp", ['length']),
        
    }
}

# Flatten the buffer dictionary to a list of tuples (buffer_name, file_path, columns)
shapefile_options = [(key + ' - ' + k, v[0], v[1]) for key, buffer in buffers.items() for k, v in buffer.items()]

# Sidebar select box for choosing the shapefile
selected_option = st.sidebar.selectbox('Select a shapefile', shapefile_options, format_func=lambda x: x[0])
selected_shapefile_name, selected_shapefile_path, available_columns = selected_option

# Load the selected data
df_chart = gpd.read_file(selected_shapefile_path)

# Main area select box for choosing the column to plot
if df_chart.empty:
    st.write("No data available for the selected shapefile.")
else:
    selected_column = st.selectbox('Select a column to plot', available_columns)

    # Check for 'Area' or 'Length' column and perform aggregation
    value_column = 'area' if 'area' in df_chart.columns else 'length' if 'length' in df_chart.columns else None
    if value_column and 'Site' in df_chart.columns and selected_column in df_chart.columns:
        # Create a new column combining 'Site' and the selected column
        df_chart['combined'] = df_chart['Site'] + ' - ' + df_chart[selected_column].astype(str)

        # Aggregate data: Sum of 'value_column' for each combined category
        df_chart_sum = df_chart.groupby(['Site', 'combined'])[value_column].sum().reset_index()

        # Create an Altair bar chart with color encoding
        chart = alt.Chart(df_chart_sum).mark_bar().encode(
            x=alt.X('combined', type='nominal', title="Site"),
            y=alt.Y(value_column),
            color=alt.Color('Site', type='nominal')  # Color encoding by 'Site'
        )

        # Display the chart in Streamlit
        st.altair_chart(chart, use_container_width=True)
    else:
        st.write("The required columns are not available in the selected shapefile.")