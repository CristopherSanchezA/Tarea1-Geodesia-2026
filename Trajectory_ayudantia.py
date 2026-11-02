# %%
"""
Trayectory model. Bevis & Brown (2014)
Joaquín Hormazabal M.
2021

"""
import numpy as np
import pylab as pl
from FG import G_matrix as FG # crea las funciones bases para armar la matriz G
from to_plot import to_plot as pt # para plotear las series de tiempo
from to_plot2 import to_plot2 as pt2 # para el modelo de trayectorias por componente
import time
from MinCuad import MinCuadPesos as mmc # minimos cuadrados con pesos
from datetime import date, datetime, timedelta # ordenar los tiempos
import pickle
import os
from directo import directo as dr

do_euler = True # Aplicar ajuste de euler (true o false)
#parametros polo de euler:
euler = {
    'lon_euler': -75.988219,  # longitud del polo de euler
    'lat_euler': 32.028902,   # latitud del polo de euler
    'omega': 0.294426,  # velocidad angular del polo de euler
}

def toYearFraction(date):
    def sinceEpoch(date):  # returns seconds since epoch
        return time.mktime(date.timetuple())

    s = sinceEpoch

    year = date.year
    startOfThisYear = datetime(year=year, month=1, day=1)
    startOfNextYear = datetime(year=year + 1, month=1, day=1)

    yearElapsed = s(date) - s(startOfThisYear)
    yearDuration = s(startOfNextYear) - s(startOfThisYear)
    fraction = yearElapsed / yearDuration

    return date.year + fraction

def extract_data(ts_file, t_cut = False):
    name = ts_file[-8:-4]
    data = np.loadtxt(ts_file, usecols=(1, 2, 3, 4, 5, 6, 7, 8), dtype=float)
    year = data[:, 0]
    days = data[:, 1]
    dates = [datetime(year=int(yr), month=1, day=1) + timedelta(days=int(days[i])-1)
             for i, yr in enumerate(year)]
    dates = np.array(dates)
    t = np.array([toYearFraction(date_i) for date_i in dates])
    if t_cut != False:
        ind = np.where(t >= t_cut)
    else:
        ind = np.where(t >= t[0])
    ew = data[ind, 2].T.flatten()
    ns = data[ind, 3].T.flatten()
    up = data[ind, 4].T.flatten()
    sigm_ew = data[ind, 5].T.flatten() 
    sigm_ns = data[ind, 6].T.flatten() 
    sigm_up = data[ind, 7].T.flatten() 
    datas = np.vstack((t,ew, ns, up, sigm_ew, sigm_ns, sigm_up)).T

    return {'station' : name , 'data': datas}

def extract_at(name, t_cut = False):
    #PickleFilename = f"./jumps_python/{name}_jump.pickle"
    PickleFilename = f"./jumps_python/{name}_jump.pickle"
    #PickleFilename = f"./jumps_matlab/{name}_jump.pickle"
    try:
        PickleFile = open(PickleFilename, 'rb')
        AT = pickle.load(PickleFile)
        PickleFile.close()
        t_at = AT['t_at']
        if t_cut != False:
            t_at = [x for x in t_at if x >= t_cut]
    except FileNotFoundError:
        t_at = []
    return t_at

def read_coords(ts_file):
    # usecols=(0, 1, 2) fuerza a leer únicamente las primeras 3 columnas
    matriz = np.loadtxt(ts_file, dtype=str, usecols=(0, 1, 2))
    coords = {}

    for ID, lon, lat in matriz:
        coords[ID] = [float(lon), float(lat)]
        
    return coords  # Importante: devolver el diccionario


def Trajectory(ts_file, t_eq = None ,tau = None, t_at = False , new_at = False, Do_plot = False,
               t_cut = False):
    name = ts_file[-8:-4]
    
    ######## Aqui deben construir su código #########

    # 1) El archivo ts_file contiene los datos de la estación geodésica. 
    #    Se cargan usando np.loadtxt, que selecciona las columnas 1 a 8 del archivo.
    #    Ayuda: función usecols selecciona columnas específicas del archivo de datos.

    data = np.loadtxt(ts_file, usecols=(1, 2, 3, 4, 5, 6, 7, 8), dtype=float)
    
    # 2) Extraer años y días:
    #    La columna 0 tiene el año, y la columna 1 tiene los días del año.
    #    Convertir días y años a fechas completas:
    #    La combinación de datetime y timedelta convierte el año y el número de días en una fecha completa.

    year = data[:, 0]
    days = data[:, 1]
    dates = [datetime(year=int(yr), month=1, day=1) + timedelta(days=int(days[i])-1)
                 for i, yr in enumerate(year)]
    dates = np.array(dates)

    # 3) Convertir Fechas a Fracciones de Año usando la función anteriormente creada.
    # toYearFraction es una función que convierte fechas a fracciones de año (por ejemplo, el 1 de julio de 2021 sería aproximadamente 2021.5). 
    # Esto es necesario porque el modelo de trayectoria requiere que las fechas estén en unidades continuas de tiempo.

    t = np.array([toYearFraction(date_i) for date_i in dates])
    
    # 4) Extraer las Componentes de Desplazamiento y sus Errores
    # Cada una de las columnas del archivo de datos contiene una componente de desplazamiento (EW, NS, UP) y su error.
    # Ayuda: Se utilizan índices para seleccionar solo los datos que pasaron el filtro de t_cut y 
    # se transforman en un arreglo plano usando .flatten().

    if t_cut != False:
        ind = np.where(t >= t_cut)
    else:
        ind = np.where(t >= t[0])
    t = t[ind]

    ew = data[ind, 2].T.flatten()
    ns = data[ind, 3].T.flatten()
    up = data[ind, 4].T.flatten()
    sigm_ew = data[ind, 5].T.flatten() 
    sigm_ns = data[ind, 6].T.flatten() 
    sigm_up = data[ind, 7].T.flatten() 
    

    if t_at == True:
        t_at = extract_at(name, t_cut = t_cut)
    else:
        t_at = []

    idx_jump = []
    iteration = 0
    while (idx_jump != None) and (not not idx_jump) or (iteration == 0):
        pl.close()
        NJ = len(idx_jump)
        for i in range(NJ):
            t_at.append(idx_jump[i][0])
# Usamos la función de Green generada antes

        G_all = FG(t,tau = tau, t_eq = t_eq, t_at = t_at)

# definala, ayudese de np.hstack

        G = np.hstack((G_all['g_lineal'], G_all['g_annual'], G_all['g_heavis_at'], G_all['g_heavis_eq'], G_all['g_post']))

# Calule las incertidumbres del modelo
# rellene para la Ins e Iup

        Iew = mmc(G, ew, np.diag(1/(sigm_ew**2)))
        Ins = mmc(G, ns, np.diag(1/(sigm_ns**2)))
        Iup = mmc(G, up, np.diag(1/(sigm_up**2)))
        
 #armamos los coef. ajustados
 
        Mew = Iew['m']
        Mns = Ins['m']
        Mup = Iup['m']

        Pew = G.dot(Mew)
        Pns = G.dot(Mns)
        Pup = G.dot(Mup)

#Plotear, pt recuerda que es la función de to_plot

        if Do_plot == True: #Colocar en True
            datas = np.vstack((ew,ns,up)).T
            pred = np.vstack((Pew,Pns,Pup)).T
            pt2(t, datas, pred,sigm_ew, sigm_ns, sigm_up, Mew, Mns, Mup,G_all['g_lineal'],G_all['g_annual'],G_all['g_heavis_eq'],G_all['g_post'],t_eq=t_eq,t_at=t_at,name=name,Tau=None)
            if new_at == True:
                idx_jump = pl.ginput(20, timeout = 20)
                pl.show()
            else:
                idx_jump = None
                pl.show()       
        else:
            idx_jump = None
        iteration = iteration + 1
    datas = np.vstack((t, ew, ns, up, sigm_ew, sigm_ns, sigm_up)).T

    if iteration > 1:
        PickleFilename = f"./jumps_python/{name}_jump.pickle"
        PickleFile = open(PickleFilename, 'wb')
        data2save = {}
        data2save['t_at'] = t_at
        pickle.dump(data2save, PickleFile, pickle.HIGHEST_PROTOCOL)
        PickleFile.close()

 
# Errores, complete para ns y up
    wrms_e = np.sqrt(sum((Pew - ew)**2 / sigm_ew**2 ) / sum(1/ sigm_ew**2))
    wrms_n = np.sqrt(sum((Pns - ns)**2 / sigm_ns**2 ) / sum(1/ sigm_ns**2))
    wrms_u = np.sqrt(sum((Pup - up)**2 / sigm_up**2 ) / sum(1/ sigm_up**2))

# Inicializar vearibles lon y lat con None
    carpeta = "pulled_data_terremoto_noto_2024_japon"
    ruta = f"{carpeta}/id_coords.txt"
    coords = read_coords(ruta)
    lon = None
    lat = None


# Verificar si la estación está en el diccionario
    if name in coords:
        lon, lat = coords[name]
    else:
        print(f"Estación {name} no encontrada en el archivo de coordenadas.")


# Velocidades ITRF

    v_ew = Mew[1]
    v_ns = Mns[1]

# Formato de velocidades ITRF

    velocidades = np.array([lon, lat, v_ew, v_ns, wrms_e, wrms_n,0], dtype=float)

# Guardar archivo de velocidades ITRF si lon y lat no son None con os.path.join y np.savetxt, con formato de 6 decimales y encabezado con nombre de estación, lon y lat

    carpeta_itrf = "velocidades_itrf"
    velocidades_archivo = os.path.join(carpeta_itrf, "vector_de_velocidades_ITRF.txt")
    
    with open(velocidades_archivo, "a") as f:
        np.savetxt(f, velocidades.reshape(1, -1), fmt="%.6f", delimiter="\t")


    if do_euler: 
        v_euler = dr(lat, lon, euler['lat_euler'], euler['lon_euler'], euler['omega'])
        v_ew_euler = v_ew - v_euler[1]
        v_ns_euler = v_ns - v_euler[0]
        velocidades_euler = np.array([lon, lat, v_ew_euler, v_ns_euler,0,0,0], dtype=float)
        velocidades_archivo_euler = os.path.join(carpeta_itrf, "vector_de_velocidades_ITRF_absoluta.txt")
        
        with open(velocidades_archivo_euler, "a") as f:
            np.savetxt(f, velocidades_euler.reshape(1, -1), fmt="%.6f", delimiter="\t")
    
# Matríz final
    return {'Param_ew' : Iew, 'Param_ns' : Ins, 'Param_up' : Iup, 'fg_all' : G,
             'fg' : G_all, 'new_jumps' : idx_jump, 'data' : datas,
             'wrms_e': wrms_e, 'wrms_u': wrms_u, 'wrms_n': wrms_n, 
             'velocidad_ew': v_ew, 'velocidad_ns': v_ns, 'lon': lon, 'lat': lat }
# agregar variables de velocidades ITRF al return
# %%
