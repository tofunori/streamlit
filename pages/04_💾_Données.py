import streamlit as st
import pandas as pd
import openpyxl

st.set_page_config(page_icon="💾")

st.title("**Données disponibles**")
st.write(" ")
st.write("  ")

st.write("Pour télécharger les shapefiles de l'ensemble des couches spatiales du projet ainsi que les données:")

# Path to the existing ZIP file
zip_file_path = 'files/picom_data.zip'  # Replace with your ZIP file path


# Put the download button in the second column
with open(zip_file_path, "rb") as file:
    # Create the download button in the second column
    st.download_button(
        label="données_picom2024.zip",
        data=file,
        file_name="données_picom2024.zip",
        mime="application/zip"
    )
    st.write(" ")
    st.write("  ")
    st.write("Le code source des analyses réalisées sous Python est disponible sur GitHub: https://github.com/tofunori/Multi-buffers-data-extraction")
    st.write(" ")
    st.write("  ")
    st.markdown("### Les résultats des analyses sont disponibles dans le fichier Excel suivant:")
    st.write(" ")
    df = pd.read_excel('files/Resultats_Analyses.xlsx')
    
    st.dataframe(df)
    
    