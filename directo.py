#%%
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 22:19:50 2022

@author: Mila
Modified by: Javi
Last update by Feña, 2025
"""
import numpy as np
def directo(lat,lon,latp,lonp,omega):

# function to compute local plate velocity vector at a point (lat, lon) caused by the rigid rotation of the plate 
# given the Euler pole position and angular velocity

# INPUT:
 
# lat,lon - position of the point where you want velocity
# latp,lonp,omegae - Euler pole position and velocity

# latitudes and longitudes are in degrees
# omega is in degrees per million years3

# OUTPUT:

# v1=[vn,ve,vd]' velocity in north easat, and down directions 
#(referred to point p) in mm/yr.

    RT = 6370*10**(6) #Radio de la tierra en milimetros
    #convertir de grados a radianes
    latr=np.deg2rad(lat)
    lonr=np.deg2rad(lon)
    latpr=np.deg2rad(latp)
    lonpr=np.deg2rad(lonp)
    
    omega = omega*10**(-6)*(np.pi/180) # convertir a radians por año
    
    #convertir a coordenadas cartesianas
    P=np.array([np.cos(latr)*np.cos(lonr), np.cos(latr)*np.sin(lonr), np.sin(latr)]).T # es el vector unitario desde el centro de la Tierra hacia el punto (lat,lon) en coordenadas cartesianas 
    EP=np.array([np.cos(latpr)*np.cos(lonpr), np.cos(latpr)*np.sin(lonpr), np.sin(latpr)]).T*omega # es el vector unitario del Polo de Euler (dirección del eje de rotación) ,multiplicado por omega
    
    VC=RT*np.cross(EP,P) # velocidad cartesiana por producto cruzado 
    
    #rotate to local coordinate system
    #Queremos pasar de la velocidad en ejes globales a ejes locales geodésicos en el punto Norte, Este, Up
    T=np.zeros((3,3));
    T[0,0]=-np.sin(latr)*np.cos(lonr); T[1,0]=-np.sin(lonr); T[2,0]=-np.cos(latr)*np.cos(lonr); # Norte
    T[0,1]=-np.sin(latr)*np.sin(lonr); T[1,1]=np.cos(lonr);  T[2,1]=-np.cos(latr)*np.sin(lonr); # Este
    T[0,2]=np.cos(latr);            T[1,2]=0;          T[2,2]=-np.sin(latr); # Up
     
    v1=T.dot(VC) # Multiplica la velocidad global Vc por T para obtener v1
    return v1

#Ejemplo de como ejecutar la función directo 
if __name__ == "__main__": # con esto solo corre si ejecuto directo.py directamente y no si llamo a la función 
    v = directo(-20.219, -70.153, -18.72, -134.22, 0.117)
    print(v)

# %%
