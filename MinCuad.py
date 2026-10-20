# %%
from numpy.linalg import lstsq
import numpy as NP
"""
J.Hormazabal & F.Ortega 2021
"""

def MinCuadSimple(G, d): # input: G que es la matriz de diseñp y d que son los datos observados
    """
    Calcula la solución de G*m = d por el método de mínimos cuadrados simples.
    Devuelve un diccionario con m y Cm.
    Para el cálculo de la matriz de covarianza del modelo, se asume que los
    errores del ajuste (i.e., de la diferencia d-Gm) son i.i.d. con media nula
    y varianza unitaria.
    """
    Ndata, Npar = G.shape
    Cm = NP.linalg.lstsq(G.T.dot(G), NP.eye(Npar), rcond=-1)[0]
    m = Cm.dot(G.T.dot(d))
    return {'m': m, 'Cm': Cm} # output: m que son los coef. ajustados al modelo y Cm que es la matriz de covarianza de los parámetros ajustados.


######
def MinCuadPesos(G, d, Wx): # en el input agregamos Wx que es una matriz de pesos
    """
    Calcula la solución de Wx*G*m = Wx*d por el método de mínimos cuadrados (con pesos).
    Devuelve un diccionario con m y Cm.
    Para el cálculo de la matriz de covarianza de los parámetros estimados del modelo,
    se asume que los errores del ajuste (i.e., de la diferencia d-Gm) siguen una
    distribución normal multivariada con media nula y matriz de covarianza Cx.
    donde Cx = inv( Wx.T.dot(Wx) )
    """
    return MinCuadSimple(Wx.dot(G), Wx.dot(d)) # output: m que son los coef. ajustados al modelo y Cm que es la matriz de covarianza de los parámetros ajustados.


######
def MinCuadCov(G, d, Cx): #Resuelve un problema de mínimos cuadrados cuando se conoce la matriz de covarianza de los errores utilizando el método de Cholesky.
    """
    inv(Cx) = Wx.T.dot(Wx)
    Calcula la solución de Wx*G*m = Wx*d por el método de mínimos cuadrados (con pesos).
    Devuelve un diccionario con m y Cm.
    Para el cálculo de la matriz de covarianza de los parámetros estimados del modelo,
    se asume que los errores del ajuste (i.e., de la diferencia d-Gm) siguen una
    distribución normal multivariada con media nula y matriz de covarianza Cx.
    """
    Ndata, Ndata2 = Cx.shape
    inv_Cx = NP.linalg.lstsq(Cx, NP.eye(Ndata))[0]
    Wx = NP.linalg.cholesky(inv_Cx).T  # as python calculates A.dot(A.T) = inv_Cx

    return MinCuadPesos(G, d, Wx)

# %%
