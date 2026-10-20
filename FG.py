#%%
"""
Trayectory model. Bevis & Brown (2014)
Joaquín Hormazabal M.
2021
"""

import numpy as np

def Heaviside(t, t0): # t es un vector de tiempos donde queremos evaluar la función Heaviside y t0 es el tiempo específico en el que ocurre el salto
    n = t.shape # nos entrega el tamaño de la dimensión del vector t, lo utilizamos para carear un vector H del mismo tamaño 
    H = np.zeros((n)) # representará el salto, vector creado inicialmente con todos sus valores en 0
    idx = np.where(t >= t0) # localiza los índices del vector t donde el valor el valor dle tiempo es mayor o igual a t0 (se representará con 1)
    H[idx] = 1 #asigna valor 1 en todas las posiciones donde se cumple t=>t0

    return H

def post(t, t_eq, tau): # t es un vector de tiempos donde queremos evaluar la función post_sísmica, t_eq es la fecha del terremoto y tau es el parámetro de tiempo de relaajción (controla la duración del proceso post-sísmico)
    Nx = t.shape[0] #nos asegura que la salida sea del mismo tamaño que t 
    idx = np.where(t >= t_eq) # encunetra el tiempo o fecha donde se presenta el salto en la Matriz G
    log_post = np.zeros((Nx, )) # inicia en ceros y luego se calcula la función log
    log_post[idx] = np.log(1 + ((t[idx] - t_eq )/ (tau/365.25))) # ((t[idx] - t_eq )/ (tau/365.25)) es el tiempo transcurrido desde t al terremoto dividido en la relajación expresada en días para un año

    return log_post

def G_matrix(t, tau = None, t_eq = None, t_at = None):
    t = t.flatten() # flatten() transforma a t en un vector 1D, para poder realizar los cálculos de forma lineal
    # Lineal component
    Nx = t.shape[0]
    g_lineal = np.zeros((Nx, 2))
    g_lineal[:, 0] = 1
    g_lineal[:, 1] = t - t[0]
    # Annual component
    g_annual = np.zeros((Nx, 4))
    g_annual[:, 0] = np.sin(2 * np.pi * t)
    g_annual[:, 1] = np.cos(2 * np.pi * t)
    g_annual[:, 2] = np.sin(4 * np.pi * t)
    g_annual[:, 3] = np.cos(4 * np.pi * t)
    # Heavis eq component
    # en cada columna de g_heavis_eq se captura los saltos bruscos que ocurren en dicho t. Si no se encuentra ninguno, la matriz de salto queda vacía
    if t_eq:
        for i in range(len(t_eq)):
            if (t[0] < t_eq[i]):          
                g_heavis_eq = np.array([], dtype=np.int64).reshape(Nx,0)
            else:
                t_eq = t_eq[i+1:]
        N_eq = len(t_eq)
        g_heavis_eq = np.zeros((Nx, N_eq))
        for i in range(N_eq):
            g_heavis_eq[:,i] = Heaviside(t, t_eq[i])
    else:
        g_heavis_eq = np.array([], dtype=np.int64).reshape(Nx,0)
    # Heavis AT component
    # Se diseña esta variable de saltos para cambios no producidos por terremotos y se almacenan en otra columna, van con un coef distinto.
    try:
        N_at = len(t_at)
        g_heavis_at = np.zeros((Nx, N_at))
        for i in range(N_at):
            g_heavis_at[:,i] = Heaviside(t, t_at[i])
    except:
        g_heavis_at = np.array([], dtype=np.int64).reshape(Nx,0)
    # Postseismic component
    try: #calcula cuántos eventos sísmicos se capturaron en t_eq y se almacenan en N_eq
        N_eq = len(t_eq) #calcula cuántos eventos sísmicos se capturaron en t_eq y se almacenan en N_eq
        g_post = np.zeros((Nx,N_eq)) # se crea la matriz de 0 de tamaño Nx x Neq, siendo el número de puntos en el vector tiempo t y el número de eventos sísmicos localizados 
        try:
            a = tau.shape
        except AttributeError:
            tau = np.ones(20,) # se impone un valor de tau por defecto en caso de que no se ponga como input alguno. Contra más grande sea, más lenta y prolongada la relajación.
        for i in range(N_eq):
            g_post[:,i] = post(t,t_eq[i],tau[i])
    except:
        g_post = np.array([], dtype=np.int64).reshape(Nx,0) # int64 permite trabajar con más cifras de los datos en caso de que sea necesario.

    #G = np.hstack((g_lineal, g_annual, g_heavis_at, g_heavis_eq, g_post))
    return {'g_lineal' : g_lineal, 'g_annual' : g_annual, 'g_heavis_at' : g_heavis_at,
            'g_heavis_eq' : g_heavis_eq, 'g_post' : g_post}

