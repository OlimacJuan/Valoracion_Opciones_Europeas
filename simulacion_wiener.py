import numpy as np
import matplotlib.pyplot as plt
import os

def simular_camino_aleatorio(S0, mu, sigma, T, N, n_simulaciones):
    """
    Simula el camino aleatorio de un activo usando el modelo de Black-Scholes.
    """
    dt = T / N
    t = np.linspace(0, T, N + 1)
    
    # Matriz para almacenar las simulaciones (N+1 filas, n_simulaciones columnas)
    S = np.zeros((N + 1, n_simulaciones))
    S[0] = S0
    
    for i in range(N):
        # Generar variables aleatorias con distribución normal estándar
        Z = np.random.normal(0, 1, n_simulaciones)
        
        # Fórmula recursiva: S_{i+1} = S_i + mu * S_i * dt + sigma * S_i * sqrt(dt) * Z_i
        S[i+1] = S[i] + mu * S[i] * dt + sigma * S[i] * np.sqrt(dt) * Z
        
    return t, S

def generar_grafico_3x3():
    # Parámetros base
    S0 = 100      # Precio inicial
    T = 1.0       # Tiempo a simular (ej. 1 año)
    N = 252       # Pasos de tiempo (ej. días de trading en un año)
    n_simulaciones = 10  # Caminos a simular por cada gráfico para ver la varianza
    
    # Valores para explorar
    mu_valores = [0.02, 0.08, 0.20]       # Baja, Media, Alta
    sigma_valores = [0.05, 0.20, 0.40]    # Baja, Media, Alta
    
    mu_labels = ['Baja (2%)', 'Media (8%)', 'Alta (20%)']
    sigma_labels = ['Baja (5%)', 'Media (20%)', 'Alta (40%)']
    
    fig, axes = plt.subplots(3, 3, figsize=(15, 12), sharex=True, sharey=True)
    fig.suptitle('Simulación del Precio del Activo: $dS = \mu S dt + \sigma S dW$', fontsize=16)
    
    np.random.seed(42) # Para reproducibilidad
    
    for i, mu in enumerate(mu_valores):
        for j, sigma in enumerate(sigma_valores):
            ax = axes[i, j]
            t, S = simular_camino_aleatorio(S0, mu, sigma, T, N, n_simulaciones)
            
            ax.plot(t, S, lw=1, alpha=0.8)
            ax.set_title(f'$\mu$: {mu_labels[i]}, $\sigma$: {sigma_labels[j]}')
            ax.grid(True, alpha=0.3)
            
            # Línea base para ver si subió o bajó
            ax.axhline(S0, color='black', linestyle='--', alpha=0.5)
            
            if i == 2:
                ax.set_xlabel('Tiempo ($t$)')
            if j == 0:
                ax.set_ylabel('Precio ($S$)')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Asegurar que el directorio existe y guardar
    output_dir = 'Informe'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'simulacion_3x3.png')
    plt.savefig(output_path, dpi=300)
    print(f"Gráfico guardado en: {output_path}")

if __name__ == "__main__":
    generar_grafico_3x3()
