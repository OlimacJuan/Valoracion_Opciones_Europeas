import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

def call_ventana(S, t, E1, E2, T, r, sigma):
    """
    Calcula el precio de la opción Call Ventana según la fórmula analítica.
    """
    tau = T - t
    # Para evitar división por cero en expiración
    tau = np.maximum(tau, 1e-6)
    
    # d1 terms
    arg1_E2 = (np.log(E2 / S) - (r + 0.5 * sigma**2) * tau) / (sigma * np.sqrt(tau))
    arg1_E1 = (np.log(E1 / S) - (r + 0.5 * sigma**2) * tau) / (sigma * np.sqrt(tau))
    
    # d2 terms
    arg2_E2 = (np.log(E2 / S) + (0.5 * sigma**2 - r) * tau) / (sigma * np.sqrt(tau))
    arg2_E1 = (np.log(E1 / S) + (0.5 * sigma**2 - r) * tau) / (sigma * np.sqrt(tau))
    
    term1 = S * (norm.cdf(arg1_E2) - norm.cdf(arg1_E1))
    term2 = E1 * np.exp(-r * tau) * (norm.cdf(arg2_E2) - norm.cdf(arg2_E1))
    
    return term1 - term2

def generar_superficie_3x3():
    # Parámetros fijos
    E1 = 90
    E2 = 110
    T = 1.0
    
    # Grilla de S y t
    S_vals = np.linspace(10, 150, 60)
    t_vals = np.linspace(0, 0.99, 60)
    S_grid, t_grid = np.meshgrid(S_vals, t_vals)
    
    # Valores para explorar
    r_valores = [0.02, 0.08, 0.20]       # Baja, Media, Alta
    sigma_valores = [0.05, 0.20, 0.40]    # Baja, Media, Alta
    
    r_labels = ['Baja (2%)', 'Media (8%)', 'Alta (20%)']
    sigma_labels = ['Baja (5%)', 'Media (20%)', 'Alta (40%)']
    
    fig = plt.figure(figsize=(18, 14))
    fig.suptitle('Superficie del Valor de la Opción "Call Ventana" $C(S,t)$', fontsize=18, y=0.95)
    
    for i, r in enumerate(r_valores):
        for j, sigma in enumerate(sigma_valores):
            # subplot index is 1-based, 3 cols * i + j + 1
            ax = fig.add_subplot(3, 3, i * 3 + j + 1, projection='3d')
            
            C_grid = call_ventana(S_grid, t_grid, E1, E2, T, r, sigma)
            
            surf = ax.plot_surface(S_grid, t_grid, C_grid, cmap='viridis', edgecolor='none', alpha=0.9)
            
            ax.set_title(f'$r$: {r_labels[i]}, $\sigma$: {sigma_labels[j]}')
            ax.set_xlabel('Precio S')
            ax.set_ylabel('Tiempo t')
            ax.set_zlabel('Valor C')
            
            # Limitar z para consistencia en la visualización, 
            # El valor máximo teórico es E2 - E1 = 20
            ax.set_zlim(0, 25)
            
            # Ángulo de visión para que se vea bien la ventana
            ax.view_init(elev=25, azim=-125)

    plt.tight_layout(rect=[0, 0.03, 1, 0.93])
    
    output_dir = 'Informe'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'superficie_3x3.png')
    plt.savefig(output_path, dpi=300)
    print(f"Gráfico guardado en: {output_path}")

if __name__ == "__main__":
    generar_superficie_3x3()
