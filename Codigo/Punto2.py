import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def call_ventana(S, t, r, sigma, E, E1, E2, T):
    """
    Calcula el precio de una opción Call Ventana Europea basado en la EDP de Black-Scholes.
    
    Parámetros:
    S     : Precio actual del activo subyacente
    t     : Tiempo actual
    r     : Tasa de interés libre de riesgo (equivalente a la tendencia mu en un mundo neutral al riesgo)
    sigma : Volatilidad del activo
    E     : Precio de ejercicio (Strike)
    E1    : Límite inferior de la ventana
    E2    : Límite superior de la ventana
    T     : Tiempo de expiración del contrato
    """
    # Determinamos S_min según la deducción teórica
    S_min = max(E1, E)
    
    # Si la barrera inferior combinada supera la barrera superior, la opción nunca tendrá valor
    if S_min >= E2:
        return 0.0
        
    tau = T - t
    
    # Manejar el valor asintótico al vencimiento (tau -> 0)
    if tau <= 1e-8:
        if E1 <= S <= E2:
            return max(S - E, 0.0)
        else:
            return 0.0
            
    # Manejar si el precio subyacente cae a cero (límite absorbente)
    if S <= 1e-8:
        return 0.0
        
    # Calcular los argumentos d1 y d2
    d1_Smin = (np.log(S / S_min) + (r + sigma**2 / 2) * tau) / (sigma * np.sqrt(tau))
    d1_E2 = (np.log(S / E2) + (r + sigma**2 / 2) * tau) / (sigma * np.sqrt(tau))
    
    d2_Smin = (np.log(S / S_min) + (r - sigma**2 / 2) * tau) / (sigma * np.sqrt(tau))
    d2_E2 = (np.log(S / E2) + (r - sigma**2 / 2) * tau) / (sigma * np.sqrt(tau))
    
    # Evaluar los términos de la fórmula deducida
    term1 = S * (norm.cdf(d1_Smin) - norm.cdf(d1_E2))
    term2 = E * np.exp(-r * tau) * (norm.cdf(d2_Smin) - norm.cdf(d2_E2))
    
    return term1 - term2

# Vectorizar la función para aplicarla sobre la malla (meshgrid)
call_ventana_vec = np.vectorize(call_ventana)

# ----------------- PARÁMETROS DEL CONTRATO -----------------
# (Se asumen valores representativos ya que no se especificaron)
E = 100.0   # Precio strike
E1 = 90.0   # Límite inferior de la ventana
E2 = 110.0  # Límite superior de la ventana
T = 1.0     # Tiempo de madurez (1 año)

# Malla de valores espaciales (Precio S) y temporales (Tiempo t)
S_vals = np.linspace(60, 140, 100) # Precios de 60 a 140
t_vals = np.linspace(0, T, 100)    # Tiempos de t=0 hasta t=T

S_mesh, t_mesh = np.meshgrid(S_vals, t_vals)

# ----------------- CASOS A GRAFICAR -----------------
# Caso 1: r (mu) = 0.002, sigma = 0.01
r1 = 0.002
sigma1 = 0.01
C_mesh1 = call_ventana_vec(S_mesh, t_mesh, r1, sigma1, E, E1, E2, T)

# Caso 2: r (mu) = 0.0, sigma = 0.01
r2 = 0.0
sigma2 = 0.01
C_mesh2 = call_ventana_vec(S_mesh, t_mesh, r2, sigma2, E, E1, E2, T)


# ----------------- CREACIÓN DE LAS SUPERFICIES -----------------
fig = plt.figure(figsize=(16, 7))

# Superficie 1
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
surf1 = ax1.plot_surface(S_mesh, t_mesh, C_mesh1, cmap='viridis', edgecolor='none', alpha=0.9)
ax1.set_title(f'Caso 1: Tasa (r) = {r1}, Volatilidad ($\\sigma$) = {sigma1}')
ax1.set_xlabel('Precio del Subyacente ($S$)')
ax1.set_ylabel('Tiempo ($t$)')
ax1.set_zlabel('Valor de la Opción ($C$)')
fig.colorbar(surf1, ax=ax1, shrink=0.5, aspect=10, pad=0.1)

# Superficie 2
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
surf2 = ax2.plot_surface(S_mesh, t_mesh, C_mesh2, cmap='plasma', edgecolor='none', alpha=0.9)
ax2.set_title(f'Caso 2: Tasa (r) = {r2}, Volatilidad ($\\sigma$) = {sigma2}')
ax2.set_xlabel('Precio del Subyacente ($S$)')
ax2.set_ylabel('Tiempo ($t$)')
ax2.set_zlabel('Valor de la Opción ($C$)')
fig.colorbar(surf2, ax=ax2, shrink=0.5, aspect=10, pad=0.1)

plt.suptitle(
    f"Superficies de Valor para Opción Call Ventana\n"
    f"$E = {E}$, $E_1 = {E1}$, $E_2 = {E2}$, $T = {T}$",
    fontsize=16, fontweight='bold'
)
plt.tight_layout()
plt.show()
