#%%
"""
@author: Joaquín Hormazabal M.
@date: 2021

"""
import numpy as np
import pylab as pl

output_path= "\\pulled_data_terremoto_noto_2024_japon"

def to_plot2(t, data , pred, sigm_ew, sigm_ns, sigm_up, Mew, Mns, Mup, g_lineal, g_annual, g_heavis_eq, g_post, t_eq = None, t_at = None, name = 'Station', Tau = None, save=False):
    ew = data[:,0]
    ns = data[:,1]
    up = data[:,2]
    Pew = pred[:,0]
    Pns = pred[:,1]
    Pup = pred[:,2]
    [_, tr] = g_lineal.shape 
    [_, s] = g_annual.shape
    [_, sa] = g_heavis_eq.shape
    [_, p] = g_post.shape
    

    fig1 = pl.figure(1)
    fig1.set_size_inches(11, 10)
    pl.subplot(321)
    pl.plot(t, ew, '.', markersize=3, color = "black", label='Datos E-W')
    pl.plot(t, Pew, '-r', label='Predicción E-W')
    try:
        pl.plot(t_eq, np.ones(len(t_eq))*np.min(ew),'*m', markersize = 8, label='Terremotos')
    except:
        None
    try:
        pl.plot(t_at, np.ones(len(t_at)) * np.min(ew), 'D', markersize=4)
    except:
        None
    pl.ylabel('EW [mm]')
    if Tau == None:
        pl.title(f'{name} -- EW component')
    else:
        pl.title("{} -- tau = {}".format(name,Tau/0.00273785))
    pl.grid(True)
    pl.legend()


    pl.subplot(322)
    pl.plot(t, ew - Pew, '.k', markersize=3, label='Residuales E-W')
    pl.plot(t, np.zeros(t.shape), '-w', markersize=3)
    try:
        pl.plot(t_eq, np.zeros(len(t_eq)),'*m', markersize = 8, label='Terremotos')
    except:
        None
    try:
        pl.plot(t_at, np.zeros(len(t_at)), 'D', markersize=4)
    except:
        None
    pl.ylabel('Residuales [mm]')
    pl.title(f'Residuales - {name} -- EW component')
    pl.grid(True)
    pl.legend()

    pl.subplot(323)
    pl.plot(t, ns, '.', markersize=3, color = "black", label='Datos N-S')
    pl.plot(t, Pns ,'-r', label='Predicción N-S')
    try:
        pl.plot(t_at, np.ones(len(t_at)) * np.min(ns), 'D', markersize=4)
    except:
        None
    try:
        pl.plot(t_eq, np.ones(len(t_eq))*np.min(ns),'*m', markersize = 8, label ='Terremotos')
    except:
        None
    pl.ylabel('NS [mm]')
    pl.title(f'{name} -- NS component')
    pl.grid(True)
    pl.legend()

    pl.subplot(324)
    pl.plot(t, ns - Pns, '.k', markersize=3, label='Residuales N-S')
    pl.plot(t, np.zeros(t.shape), '-w', markersize=3)
    try:
        pl.plot(t_eq, np.zeros(len(t_eq)),'*m', markersize = 8, label='Terremotos')
    except:
        None
    try:
        pl.plot(t_at, np.zeros(len(t_at)), 'D', markersize=4)
    except:
        None
    pl.ylabel('NS [mm]')
    pl.title(f'Residuales - {name} -- NS component')
    pl.grid(True)
    pl.legend()

    pl.subplot(325)
    pl.plot(t, up, '.', markersize=3, color = "black", label='Datos Up')
    pl.plot(t, Pup, '-r', label='Predicción Up')
    try:
        pl.plot(t_eq, np.ones(len(t_eq))*np.min(up),'*m', markersize = 8, label='Terremotos')
    except:
        None
    try:
        pl.plot(t_at, np.ones(len(t_at)) * np.min(up), 'D', markersize=4)
    except:
        None
    pl.xlabel('Tiempo')
    pl.ylabel('UP [mm]')
    pl.title(f'{name} -- Up component')
    pl.grid(True)
    pl.legend()

    pl.subplot(326)
    pl.plot(t, up - Pup, '.k', markersize=3, label='Residuales Up')
    pl.plot(t, np.zeros(t.shape), '-w', markersize=3)
    try:
        pl.plot(t_eq, np.zeros(len(t_eq)),'*m', markersize = 8, label='Terremotos')
    except:
        None
    try:
        pl.plot(t_at, np.zeros(len(t_at)), 'D', markersize=4)
    except:
        None
    pl.ylabel('UP [mm]')
    pl.xlabel('Tiempo')
    pl.title(f'Residuales - {name} -- Up component')
    pl.tight_layout()
    pl.grid(True)
    pl.legend()
    fig1.savefig(f'{output_path}{name}_timeseries.png',dpi=300)
    pl.show()

    fig2 = pl.figure(2)
    fig2.set_size_inches(11,10)
    pl.subplot(311) # Componente EW
    pl.plot(t, g_lineal @Mew[:tr], 'g', linewidth=2, label='Lineal')
    pl.plot(t, g_annual @Mew[tr:tr + s], 'r', linewidth=2, label='Estacional')
    pl.plot(t, g_heavis_eq @Mew[tr + s + sa:tr + s + sa + p], 'k', linewidth=2, label='Saltos')
    pl.plot(t, g_post @Mew[tr + s + sa:tr + s + sa + p], 'b', linewidth=2, label='Post-sísmico')
    pl.title(f'{name} -- E-W Component')
    pl.ylabel('E-W [mm]')
    pl.legend()
    pl.grid()
    
    pl.subplot(312)
    pl.plot(t, g_lineal @Mns[:tr], 'g', linewidth=2, label='Lineal')
    pl.plot(t, g_annual @Mns[tr:tr + s], 'r', linewidth=2, label='Estacional')
    pl.plot(t, g_heavis_eq @Mns[tr + s + sa:tr + s + sa + p], 'k', linewidth=2, label='Saltos')
    pl.plot(t, g_post @Mns[tr + s + sa:tr + s + sa + p], 'b', linewidth=2, label='Post-sísmico')
    pl.title(f'{name} -- N-S Component')
    pl.ylabel('N-S [mm]')
    pl.legend()
    pl.grid()
    
    pl.subplot(313)
    pl.plot(t, g_lineal @Mup[:tr], 'g', linewidth=2, label='Lineal')
    pl.plot(t, g_annual @Mup[tr:tr + s], 'r', linewidth=2, label='Estacional')
    pl.plot(t, g_heavis_eq @Mup[tr + s + sa:tr + s + sa + p], 'k', linewidth=2, label='Saltos')
    pl.plot(t, g_post @Mup[tr + s + sa:tr + s + sa + p], 'b', linewidth=2, label='Post-sísmico')
    pl.title(f'{name} -- UP Component')
    pl.ylabel('UP [mm]')
    pl.legend()
    pl.grid()
    fig2.savefig(f'{output_path}{name}_component.png',dpi=300)
    return None

# %%
