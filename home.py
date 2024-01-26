import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

st.title('PICOM - Cartographie des données')

st.write("Le lien Github pour le code Python du projet: https://github.com/tofunori/Multi-buffers-data-extraction ")

zip_file_path = "files/picom_data.zip"
# Create two columns
col1, col2 = st.columns([1, 1], gap="small")  # Adjust the ratio as needed

# Put the text in the first column
col1.write("Télécharger les données Shapefile et excel:")

# Put the download button in the second column
with open(zip_file_path, "rb") as file:
    # Create the download button in the second column
    col2.download_button(
        label="data.zip",
        data=file,
        file_name="picom_data.zip",
        mime="application/zip"
    )