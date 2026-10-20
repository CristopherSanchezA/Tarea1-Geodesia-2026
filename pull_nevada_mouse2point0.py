#!/usr/bin/env python3
#% SCRIPT TO PULL DATA FROM THE NEVADA WEBPAGE.
# % The script pulls both the metadata (latitude, longitude) and the data
# % (East, North, Up)
# % Note, that the data are in IGS14 format.

# % Last updated 12th July 2016, Potsdam.
# % This update was a slight upgrade of the script to allow choosing a range
# % of stations from a global map.
# % Author: Jonathan Bedford, jonrbedford@gmhthttps://www.dropbox.com/s/m9zhh7acrfof7s7/Test%201%20Geodesia%2002.docx?dl=0tps://www.dropbox.com/s/m9zhh7acrfof7s7/Test%201%20Geodesia%2002.docx?dl=0ail.com // jbed@gfz-potsdam.de

# Updated python file, 24/10/2025 Marcelo Cardenas.
# last update by Fernanda Castro Araya - Fernanda Bonilla Contreras 08/10/2026.
 
# Librerías

import os
import requests
import pandas as pd
import matplotlib
matplotlib.use("TkAgg") #OCUPO ESTO PARA PODER VISUALIZAR 
import matplotlib.pyplot as plt
from matplotlib.widgets import PolygonSelector
from matplotlib.path import Path
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import datetime
import numpy as np

# Se define la zona de la cual descargar las estaciones
zona = "terremoto"

# Crear la carpeta 'pulled_data' si no existe
def create_folder():
    if not os.path.exists(f'./pulled_data_{zona}'):
        os.makedirs(f'./pulled_data_{zona}')
    else:
        # Limpiar la carpeta antes de empezar
        for f in os.listdir(f'./pulled_data_{zona}'):
            os.remove(os.path.join(f'./pulled_data_{zona}', f))

# Función para descargar el contenido URL GNSS
def download_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Error al descargar desde {url}. Código de estado: {response.status_code}")

# Función para descargar y procesar los datos ENU de la estación
def download_and_save_data(station_id):
    print(f"Descargando datos para la estación: {station_id}")
    
    # Descargar los datos ENU
    datapath = f"https://geodesy.unr.edu/gps_timeseries/IGS20/tenv3/IGS20/{station_id}.tenv3"
    try:
        enu_data = download_file(datapath)
    except Exception as e:
        print(f"Error al descargar los datos de la estación {station_id}: {e}")
        return
    
    # Guardar temporalmente los datos descargados
    with open('data_temp.txt', 'w') as f:
        f.write(enu_data)
    
    # Leer los datos y extraer fechas y valores ENU
    with open('data_temp.txt', 'r') as f:
        lines = f.readlines()
    
    # Procesar las líneas y obtener los datos ENU
    data = [line.split() for line in lines[1:]]  # Omitir la primera línea (encabezado)

    if len(data) == 0:                                         
        print(f"La estación {station_id} no tiene datos, se omite.") 
        return                                                      
    
    # Extraer las fechas y las columnas ENU
    # DESAFIO 1
    
    datestring = [line[1] for line in data]  # Segundo elemento de cada línea es la fecha
    enu = np.array([[float(line[8]), float(line[10]), float(line[12])] for line in data])  # Columnas ENU
    sig_enu = np.array([[float(line[14]), float(line[15]), float(line[16])] for line in data])  # Columnas de error
    
    # Normalizar ENU restando el primer valor
    enu -= enu[0, :]
    
    # Convertir las fechas de formato YYMMDD a YYYY, MM, DD
    yyyy = []
    mm = []
    dd = []
    for date in datestring:
        year = int(date[:2])
        yyyy.append(1900 + year if year > 80 else 2000 + year)  # Asume años mayores a 80 como 1900
        dd.append(int(date[5:7]))  # Día
        month_str = date[2:5]  # Mes en formato 'JAN', 'FEB', etc.
        mm.append(datetime.datetime.strptime(month_str, '%b').month)  # Convertir el mes a número
    
    # Convertir las fechas a DOY (día del año)
    doy = [datetime.datetime(y, m, d).timetuple().tm_yday for y, m, d in zip(yyyy, mm, dd)]
    
    # Guardar los resultados en un archivo dentro de la carpeta 'pulled_data'
    save_path = f'./pulled_data_{zona}/{station_id}.txt'
    with open(save_path, 'w') as f_out:
        for i in range(len(yyyy)):
            f_out.write(f"{station_id} {yyyy[i]} {doy[i]} {enu[i,0]*1000:.4f} {enu[i,1]*1000:.4f} {enu[i,2]*1000:.4f} "
                        f"{sig_enu[i,0]*1000:.4f} {sig_enu[i,1]*1000:.4f} {sig_enu[i,2]*1000:.4f}\n")
    
    print(f"Datos de {station_id} guardados en {save_path}")


# Función para normalizar las coordenadas de longitud
def normalize_longitude(lon):
    while lon > 180:
        lon -= 360
    while lon < -180:
        lon += 360
    return lon

# Archivo de coordenadas de todas las estaciones NGL
ARCHIVO_COORDS = './Coords_Nevada/id_coords_all_NEVADA.txt'
ACTUALIZAR_COORDS = True   # True: descarga la lista actual de NGL cada vez que se corre
                           # False: usa el .txt guardado (si no existe, lo descarga igual)

# Descarga DataHoldings.txt de NGL y guarda un .txt con columnas sta lon lat
def actualizar_coords(archivo=ARCHIVO_COORDS):
    url = "https://geodesy.unr.edu/NGLStationPages/DataHoldings.txt"
    print("Descargando lista de estaciones desde NGL...")
    df = pd.read_csv(url, sep=r"\s+", usecols=[0, 1, 2],
                     names=["sta", "lat", "lon"], skiprows=1)
    os.makedirs(os.path.dirname(archivo), exist_ok=True)
    df[["sta", "lon", "lat"]].to_csv(archivo, sep=" ", index=False)
    print(f"{len(df)} estaciones guardadas en {archivo}")

if ACTUALIZAR_COORDS or not os.path.exists(ARCHIVO_COORDS):
    try:
        actualizar_coords()
    except Exception as e:
        if os.path.exists(ARCHIVO_COORDS):
            print(f"No se pudo descargar la lista ({e}). Se usa el archivo guardado.")
        else:
            raise

# Cargar los datos (el archivo tiene encabezado 'sta lon lat', por eso header=0)
data = pd.read_csv(ARCHIVO_COORDS, sep=r"\s+", header=0, names=['ID', 'Longitude', 'Latitude'])
data_original = data.copy()
data['Longitude'] = data['Longitude'].apply(normalize_longitude)


# Función para añadir la visualización de coordenadas en el mapa
def format_coord(x, y):
    return f'Longitude: {x:.2f}, Latitude: {y:.2f}'

def plot_map(lon1=-180, lon2=180, lat1=-90, lat2=90, title=''):
    fig, ax = plt.subplots(figsize=(15, 10), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([lon1, lon2, lat1, lat2], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAND, edgecolor='black')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
    
    # Añadir las líneas de paralelos y meridianos con etiquetas de coordenadas
    gl = ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
    gl.top_labels = False
    gl.right_labels = False
    
    # Dibujar las estaciones
    x = data['Longitude'].values
    y = data['Latitude'].values
    ax.scatter(x, y, marker='v', facecolor='k', edgecolor='r', s=8, zorder=5, transform=ccrs.PlateCarree())

    # Formato para mostrar las coordenadas en los ejes
    ax.format_coord = format_coord
    
    plt.title(title)
    return fig, ax, x, y

class SelectFromPolygon:
    def __init__(self, ax, x, y):
        self.ax = ax
        self.x = x
        self.y = y
        self.selected_stations_data = pd.DataFrame()
        self.poly = PolygonSelector(ax, self.onselect, useblit=True)
        plt.title('SELECTING STATIONS WITHIN POLYGON')

    def onselect(self, verts):
        path = Path(verts)
        selected_points = path.contains_points(list(zip(self.x, self.y)))
        self.selected_stations_data = data[selected_points]
        poly = plt.Polygon(verts, edgecolor='c', facecolor='none', transform=ccrs.PlateCarree())
        self.ax.add_patch(poly)
        plt.draw()
        plt.close()

    def get_selected_data(self):
        return self.selected_stations_data

def main():
    create_folder()  # Crear la carpeta pulled_data
    
    # Mostrar el mapa completo para seleccionar la región de zoom
    fig, ax, x, y = plot_map(title='CLICK twice to select a zoom region')
    selector = SelectFromPolygon(ax, x, y)
    plt.show(block=True)
 
    selected_stations_data = selector.get_selected_data()
 
    if not selected_stations_data.empty:
        # Determinar el rango de la región seleccionada para hacer zoom
        lon_min, lat_min = selected_stations_data[['Longitude', 'Latitude']].min()
        lon_max, lat_max = selected_stations_data[['Longitude', 'Latitude']].max()
 
        # Hacer zoom en la región seleccionada
        fig, ax, x, y = plot_map(lon_min, lon_max, lat_min, lat_max, title='SELECTING STATIONS WITHIN POLYGON')
        
        # Asegurarse de que las coordenadas se muestren en el mapa de zoom
        ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
        
        selector = SelectFromPolygon(ax, x, y)
        plt.show(block=True)
 
        selected_stations_data = selector.get_selected_data()
 
        # Cambiar las longitudes a sus valores originales para la salida
        selected_stations_data = selected_stations_data.copy()
        selected_stations_data.loc[:, 'Longitude'] = data_original.loc[selected_stations_data.index, 'Longitude']

        # Listas para almacenar longitudes y latitudes
        longitudes = []
        latitudes = []
 
        # Descargar los datos de cada estación seleccionada
        for station_id in selected_stations_data['ID']:
            download_and_save_data(station_id)
            # Recuperar la latitud y longitud de la estación
            longitude = selected_stations_data.loc[selected_stations_data['ID'] == station_id, 'Longitude'].values[0]
            latitude = selected_stations_data.loc[selected_stations_data['ID'] == station_id, 'Latitude'].values[0]
            longitudes.append(longitude)
            latitudes.append(latitude)
            
 
        # Guardar las estaciones y sus coordenadas en 'id_coords.txt'
        save_path = f'./pulled_data_{zona}/id_coords.txt'
        with open(save_path, 'w') as f: #se sobreescribira la información cada vez que corra el código
            for station_id, lon, lat in zip(selected_stations_data['ID'], longitudes, latitudes):
                f.write(f"{station_id} {lon:.2f} {lat:.2f}\n")
 
        print("Descarga completada.")
    else:
        print("No se seleccionaron estaciones.")
 
if __name__ == '__main__':
    main()