#%%
"""
@author: Joaquín Hormazabal M.
@date: 2021

"""
import numpy as np
import pylab as pl

carpeta = "pulled_data_terremoto_noto_2024_japon"
ruta = f"{carpeta}/id_coords.txt"

def to_plot(t, data , pred , t_eq = None, t_at = None, name = 'Station', Tau = None):
    ew = data[:,0]
    ns = data[:,1]
    up = data[:,2]
    Pew = pred[:,0]
    Pns = pred[:,1]
    Pup = pred[:,2]
    ##fig1_name="serie1.svg"
    fig1 = pl.figure(1)
    fig1.set_size_inches(11, 10)
    pl.subplot(321)
    pl.plot(t, ew, '.', markersize=3, color = "#00ff00")
    pl.plot(t, Pew, '-r')
    try:
        pl.plot(t_eq, np.ones(len(t_eq))*np.min(ew),'*m', markersize = 8)
    except:
        None
    try:
        pl.plot(t_at, np.ones(len(t_at)) * np.min(ew), 'D', markersize=4)
    except:
        None
    pl.ylabel('EW [mm]')
    if Tau == None:
        pl.title(name)
    else:
        pl.title("{} -- tau = {}".format(name,Tau/0.00273785))


    pl.subplot(322)
    pl.plot(t, ew - Pew, '.k', markersize=3)
    pl.plot(t, np.zeros(t.shape), '-w', markersize=3)
    try:
        pl.plot(t_eq, np.zeros(len(t_eq)),'*m', markersize = 8)
    except:
        None
    try:
        pl.plot(t_at, np.zeros(len(t_at)), 'D', markersize=4)
    except:
        None
    pl.ylabel('NS [mm]')
    pl.title('Residuales')

    pl.subplot(323)
    pl.plot(t, ns, '.', markersize=3, color = "#00ff00")
    pl.plot(t, Pns ,'-r')
    try:
        pl.plot(t_at, np.ones(len(t_at)) * np.min(ns), 'D', markersize=4)
    except:
        None
    try:
        pl.plot(t_eq, np.ones(len(t_eq))*np.min(ns),'*m', markersize = 8)
    except:
        None
    pl.ylabel('NS [mm]')

    pl.subplot(324)
    pl.plot(t, ns - Pns, '.k', markersize=3)
    pl.plot(t, np.zeros(t.shape), '-w', markersize=3)
    try:
        pl.plot(t_eq, np.zeros(len(t_eq)),'*m', markersize = 8)
    except:
        None
    try:
        pl.plot(t_at, np.zeros(len(t_at)), 'D', markersize=4)
    except:
        None
    pl.ylabel('NS [mm]')

    pl.subplot(325)
    pl.plot(t, up, '.', markersize=3, color = "#00ff00")
    pl.plot(t, Pup, '-r')
    try:
        pl.plot(t_eq, np.ones(len(t_eq))*np.min(up),'*m', markersize = 8)
    except:
        None
    try:
        pl.plot(t_at, np.ones(len(t_at)) * np.min(up), 'D', markersize=4)
    except:
        None
    pl.xlabel('Tiempo')
    pl.ylabel('UP [mm]')

    pl.subplot(326)
    pl.plot(t, up - Pup, '.k', markersize=3)
    pl.plot(t, np.zeros(t.shape), '-w', markersize=3)
    try:
        pl.plot(t_eq, np.zeros(len(t_eq)),'*m', markersize = 8)
    except:
        None
    try:
        pl.plot(t_at, np.zeros(len(t_at)), 'D', markersize=4)
    except:
        None
    pl.ylabel('UP [mm]')
    pl.xlabel('Tiempo')
    pl.tight_layout()
    #pl.savefig(fig1_name, dpi = 300)

    
    pl.show()
    return None
# %%
