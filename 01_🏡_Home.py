import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

st.set_page_config(
    layout="wide",
    page_icon="🏡",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "Cette application a été développée par Thierry Laurent St-Pierre, étudiant au Baccalauréat en Géographie environnementale à l'Université du Québec à Trois-Rivières."
    }
)

st.title("**PICOM Corridors écologiques**")
st.write(" ")
# Title for the sidebar
st.sidebar.title("Menu")
st.image('files/images/forest.jpg', caption='Photo: Fanny Bec')

st.write("""

Ce projet d’intervention dans la communauté se concentre sur la connectivité écologique et les corridors de conservation en Mauricie. L'objectif principal est de développer un plan de conservation pour le sud-ouest de la Mauricie, visant à faciliter le déplacement des espèces fauniques.

Les axes majeurs du projet incluent:

1. La validation des corridors écologiques.
2. L'identification des contraintes humaines ou physiques impactant ces corridors.
3. La confirmation de l’utilisation de ces corridors par la faune.

Cette application offre une visualisation de l'espace concerné par le projet, ainsi que les différentes couches de variables prises en compte dans nos analyses. Quinze sites ont été sélectionnés pour l'installation de caméras et d’audiomoths. Autour de chacun de ces sites, des zones tampons de 500 mètres, 1 kilomètre et 2 kilomètres ont été établies.

L'application permet également de visualiser les différentes variables analysées et l'étendue de leur couverture au sein de chaque zone tampon. Les variables analysées comprennent les routes, les cours d'eau, les voies ferrées, les dépôts de surface, le type de couverture végétale, et le type d’occupation du territoire.
""")
st.write("- Les données sont disponibles sous forme de fichiers Shapefile et de fichiers Excel:")

# Path to the existing ZIP file
zip_file_path = 'files/picom_data.zip'  # Replace with your ZIP file path


# Put the download button in the second column
with open(zip_file_path, "rb") as file:
    # Create the download button in the second column
    st.download_button(
        label="Données",
        data=file,
        file_name="data.zip",
        mime="application/zip"
    )
    
    st.write("- Le code source des analyses est disponible sur [GitHub](https://github.com/tofunori/Multi-buffers-data-extraction")