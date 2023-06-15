# Cargando módulos
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("Evaluación de corrosión en el concreto")

# Lectura de datos
## Cargando archivo csv
uploaded_file = st.file_uploader("Cargue el archivo de lecturas en formato .csv")

st.header("Datos de medición")
## Limpiando datos
datos = pd.read_csv(uploaded_file, skiprows = 6)
datos = datos.loc[1:,["Potential","Temperature"]]
datos = datos.astype(float)
st.table(datos)

# Puntos de lectura
st.header("Configuración de gráfico")
col1, col2 = st.columns(2)

#Grilla
with col1:
    x_lines = st.number_input("Número de filas:", min_value=2)
with col2:
    y_lines = st.number_input("Número de columnas:", min_value=2)

if x_lines*y_lines != datos.Potential.shape[0]:
    st.error("El número de puntos en la gráfico configurado no coincide con el número de puntos medidos")
else:
    with col1:
        x_sep = st.number_input("Espaciamiento horizontal (cm):", min_value=1)
    with col2:
        y_sep = st.number_input("Espaciamiento vertical (cm):", min_value=1)
    z_sep = st.number_input("Separación de líneas equipotenciales (mV/CSE):", min_value=5)

    ## Grilla de datos
    potential_points=datos["Potential"].to_numpy().reshape((x_lines,y_lines),order="F")
    x_coord = np.arange(0, x_lines*x_sep, x_sep)
    y_coord = np.arange(0, y_lines*y_sep, y_sep)
    coords = np.meshgrid(x_coord,y_coord)
    datos["Coord X (cm)"] =coords[1].reshape(coords[1].size)
    datos["Coord Y (cm)"] =coords[0].reshape(coords[0].size)

# Gráfica de Mapa de Corrosión
    fig1 = px.scatter(datos,x= "Coord X (cm)",y="Coord Y (cm)",color="Potential",
                      hover_data=["Temperature"],color_continuous_scale=px.colors.sequential.ice)
    fig2 = go.Figure(data=
        go.Contour(
            z=potential_points,
            dx=x_sep,
            x0=0,
            dy=y_sep,
            y0=0,
            contours=dict(start=potential_points.min()//z_sep*z_sep, end=potential_points.max(), size=z_sep,
                #coloring ='heatmap',
                showlabels = True,
                labelfont = dict(size = 12, color='white'))))
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
