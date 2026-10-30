#%%
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 22:19:50 2022

@author: Mila
Modified by: Javi
"""
#Polo de Euler en un punto con respecto al sistema de referencia ITRF
import numpy as np
from MinCuad import MinCuadPesos as mcp

#Se carga el archivo de velocidades con las que construiremos el polo de Euler
#'Lon','lat', 've','vn'
#filename="estacionaria_velo.txt"    

def polo_euler(filename):
    data = np.loadtxt(filename, usecols=(0,1, 2, 3, 4, 5), dtype=float)
    #Se separa cada columna y se aplana a vectores 1D
    lon= data[:,0].T.flatten()
    lat=data[:,1].T.flatten()
    ve=data[:,2]*0.001 #convertimos a (m)
    ve=ve.T.flatten()
    vn=data[:,3]*0.001 #pasamos de mm/año a m/año
    vn=vn.T.flatten()
    sigme=data[:,4]*0.001
    sigme=sigme.T.flatten()
    sigmn=data[:,5]*0.001
    sigmn=sigmn.T.flatten()
    
    r1=6378137 # radio ecuatorial (m)
    r2=6356752 #eje polar del geoide (m)
    
    #Se convierten las coordenadas de grados a radianes
    lon=np.deg2rad(lon) 
    lat=np.deg2rad(lat)
    
    X=r1*np.cos(lat) 
    Y=r2*np.sin(lat)
    
    r=np.sqrt(X**2 + Y**2) #Radio desde el centro del elipsoide a la superficie
    
    # Matriz de Diseño G y velocidades (D)
    #Sn = sigmn**2
    #Se = sigme**2
    G=np.zeros((2*len(ve),3)) # ¿Qué es G?
    D = np.zeros((2*len(ve),1)) #¿Qué representa D?
    S=np.zeros((2*len(ve),1)) # guardará las incertidumbres asociadas a cada ecuación 
                 
    #eq. 11 de Goundarzi et al. 2014
    for i in range(0, len(ve)): # estructura de G forma cinemática
        G[2*i,:]=r[i]*np.array([np.sin(lon[i]), -np.cos(lon[i]), 0]) #componente N
        G[2*i+1,:]=r[i]*np.array([-np.sin(lat[i])*np.cos(lon[i]), -np.sin(lat[i])*np.sin(lon[i]), np.cos(lat[i])]); # componente E
        #Velocidades
        D[2*i,:]=vn[i]
        D[2*i+1,:]=ve[i]      
        S[2*i]=sigme[i]
        S[2*i+1]=sigmn[i]

   
    # w = inv(G' * inv(S) * G) * G' * inv(S) * d
    #with W'* W = inv(S), or, simplified: S = s^2

    S=S.T.flatten() # aplanamos S a 1D y construyes la matriz de pesos
    Wd = np.diag(1/(S**2))
    w = mcp(G,D,Wd) #llamamos a nuestra función de mínimos cuadrados que resuelve w 
    w=w['m']
    
    # Parametros del Polo de Euler w_uni=(wx,wy,wz)
    wx=w[0]; wy=w[1]; wz=w[2]
    # parametros del Polo de Euler (lat,lon,Magnitude grados/Ma)
    latp = np.rad2deg(np.arctan2(wz,np.sqrt(wx**2 +wy**2)))
    lonp = np.rad2deg(np.arctan2(wy,wx))
    omega = np.rad2deg(np.sqrt(w.T.dot(w)))*10**6;
    
    # modeled velocities = model predictions
    pred = G.dot(w)
    pred_n = np.zeros(len(ve))
    pred_e = np.zeros(len(ve))

    for i in range(0, len(ve)):
        pred_n[i]=pred[2*i]
        pred_e[i]=pred[2*i+1]
        
    euler_pole=np.zeros(3)
    euler_pole[0]=lonp
    euler_pole[1]=latp
    euler_pole[2]=omega
    
    return [euler_pole, pred_n, pred_e]


#Ahora debemos ejecutar la función del polo de euler y lo hacemos de la siguiente manera
#CASO EJEMPLO, para cada caso deben hacerlo según el evento que hayan escogido 

#[polo,vn_pred, ve_pred] = polo_euler('zona_estable.txt') Aquí ejecutamos la inversión para el archivo zona_estable.txt

# data = np.loadtxt('zona_estable.txt') cargamos datos, luego separamos columnas de lon y lat 
# lon=data[:,0]
# lat=data[:,1]
# vel = np.column_stack((lon, lat, ve_pred*1000, vn_pred*1000, np.zeros(len(lon)), np.zeros(len(lon)), np.zeros(len(lon)))) Armamos una matriz vel con lon, lat, ve_pred y vn_pred convertidos a mm/año y trez columnas de ceros 
# output_polo = f'Polo_Euler.txt' guardamos en un archivo llamado polo_euler.txt 
# np.savetxt(output_polo, polo, fmt='%.6f', delimiter='\t') el polo de Euler estimado en lon, lat y omega con 6 decimales
# vel_rot_ze = f'pred_zonaestable.txt'  creamos un archivo para guardar la velocidades predichas
# np.savetxt(vel_rot_ze, vel, fmt='%.6f', delimiter='\t') guardamos las velocidades predichas por el modelo (en mm/año) junto con lon/lat y columnas extras en cero

# %%
