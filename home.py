import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

st.title('PICOM - Cartographie des données')

# Path to the existing ZIP file
zip_file_path = 'files/picom_data.zip'  # Replace with your ZIP file path


# Create two columns
col1, col2 = st.columns([3, 1])  # Adjust the ratio as needed

# Put the text in the first column
col1.write("Télécharger les données Shapefile et excel:")

# Put the download button in the second column
with open(zip_file_path, "rb") as file:
    # Create the download button in the second column
    col2.download_button(
        label="Données Shapefile",
        data=file,
        file_name="data.zip",
        mime="application/zip"
    )