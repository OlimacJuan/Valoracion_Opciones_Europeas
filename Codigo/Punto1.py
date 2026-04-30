import numpy as np
import matplotlib.pyplot as plt

def simular_black_scholes(N, delta_t, S_0, mu, sigma):
    """
    Simula el proceso de valor de un modelo de Black-Scholes.
    """
    t = np.zeros(N + 1)
    S = np.zeros(N + 1)
    
    t[0] = 0.0
    S[0] = S_0
    
    for i in range(N):
        t[i+1] = t[i] + delta_t
        Z_i = np.random.randn()
        S[i+1] = S[i] + mu * S[i] * delta_t + sigma * S[i] * np.sqrt(delta_t) * Z_i
        
    return t, S

# Parámetros solicitados
N = 100            # 100 periodos
delta_t = 5.0      # de 5 unidades de tiempo
S_0 = 4.0        # valor inicial
mu = 0.0          # tendencia (drift)
sigma = 0.01       # volatilidad

# Crear una figura con 3 subgráficos (1 fila, 3 columnas)
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Título principal con los parámetros
fig.suptitle(
    f"Simulaciones de Modelo Black-Scholes\n"
    f"Tendencia ($\\mu$): {mu} | Volatilidad ($\\sigma$): {sigma} | Valor Inicial ($S_0$): {S_0} | $\\Delta t$: {delta_t}", 
    fontsize=16
)

# Configuraciones para cada subgráfico: 1, 3 y 10 simulaciones
simulaciones = [1, 3, 10]

for idx, num_sims in enumerate(simulaciones):
    ax = axes[idx]
    
    # Realizar y graficar el número correspondiente de simulaciones
    for _ in range(num_sims):
        t, S = simular_black_scholes(N, delta_t, S_0, mu, sigma)
        ax.plot(t, S, alpha=0.8)
        
    ax.set_title(f"{num_sims} Simulación{'es' if num_sims > 1 else ''}")
    ax.set_xlabel("Tiempo (t)")
    ax.set_ylabel("Proceso de Valor (S_t)")
    ax.grid(True, linestyle='--', alpha=0.7)

# Ajustar el diseño y mostrar la gráfica
plt.tight_layout()
plt.show()
