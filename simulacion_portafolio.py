import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

def call_ventana(S, t, E1, E2, T, r, sigma):
    tau = T - t
    tau = np.maximum(tau, 1e-6)
    
    arg1_E2 = (np.log(E2 / S) - (r + 0.5 * sigma**2) * tau) / (sigma * np.sqrt(tau))
    arg1_E1 = (np.log(E1 / S) - (r + 0.5 * sigma**2) * tau) / (sigma * np.sqrt(tau))
    arg2_E2 = (np.log(E2 / S) + (0.5 * sigma**2 - r) * tau) / (sigma * np.sqrt(tau))
    arg2_E1 = (np.log(E1 / S) + (0.5 * sigma**2 - r) * tau) / (sigma * np.sqrt(tau))
    
    term1 = S * (norm.cdf(arg1_E2) - norm.cdf(arg1_E1))
    term2 = E1 * np.exp(-r * tau) * (norm.cdf(arg2_E2) - norm.cdf(arg2_E1))
    
    return term1 - term2

def simular_paths(S0, mu, sigma, T, N, M):
    dt = T / N
    t = np.linspace(0, T, N + 1)
    S = np.zeros((N + 1, M))
    S[0] = S0
    for i in range(N):
        Z = np.random.normal(0, 1, M)
        S[i+1] = S[i] + mu * S[i] * dt + sigma * S[i] * np.sqrt(dt) * Z
    return t, S

def evaluar_portafolio(t_arr, S_paths, E1, E2, T, r, sigma):
    N, M = S_paths.shape
    C0 = call_ventana(S_paths[0,0], 0, E1, E2, T, r, sigma)
    Pi = np.zeros_like(S_paths)
    
    for i in range(N):
        t = t_arr[i]
        Bt = C0 * np.exp(r * t)
        if i == N - 1 or t >= T - 1e-5:
            # Payoff exacto en madurez
            C_t = np.zeros(M)
            mask = (S_paths[i] >= E1) & (S_paths[i] <= E2)
            C_t[mask] = S_paths[i, mask] - E1
        else:
            C_t = call_ventana(S_paths[i], t, E1, E2, T, r, sigma)
        
        Pi[i] = S_paths[i] - C_t + Bt
    return Pi, C0

def plot_analysis():
    S0 = 100
    E1 = 90
    E2 = 110
    T = 1.0
    N = 252
    
    # Dos escenarios a contrastar
    scenarios = [
        {'mu': 0.08, 'r': 0.05, 'sigma': 0.10, 'title': 'Baja Volatilidad (10%), r=5%'},
        {'mu': 0.08, 'r': 0.05, 'sigma': 0.30, 'title': 'Alta Volatilidad (30%), r=5%'}
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Análisis de Seguridad del Portafolio "Covered Call Ventana"', fontsize=18)
    
    np.random.seed(42)
    
    for col, sc in enumerate(scenarios):
        # Evolución de 5 caminos aleatorios
        t, S_evol = simular_paths(S0, sc['mu'], sc['sigma'], T, N, 5)
        Pi_evol, C0 = evaluar_portafolio(t, S_evol, E1, E2, T, sc['r'], sc['sigma'])
        
        ax1 = axes[0, col]
        for m in range(5):
            ax1.plot(t, S_evol[:, m], color='red', alpha=0.3, linestyle='--', label='Activo $S_t$' if m==0 else "")
            ax1.plot(t, Pi_evol[:, m], color='blue', alpha=0.7, label='Portafolio $\Pi_t$' if m==0 else "")
        ax1.set_title(f"Evolución en el Tiempo\n{sc['title']}")
        ax1.set_xlabel('Tiempo $t$')
        ax1.set_ylabel('Valor')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Simulación de Monte Carlo con 1000 trayectorias para ver la distribución final
        _, S_dist = simular_paths(S0, sc['mu'], sc['sigma'], T, N, 1000)
        Pi_dist, _ = evaluar_portafolio(t, S_dist, E1, E2, T, sc['r'], sc['sigma'])
        
        S_T = S_dist[-1, :]
        Pi_T = Pi_dist[-1, :]
        
        ax2 = axes[1, col]
        # Dibujar perfil teórico de pagos
        S_range = np.linspace(40, 180, 400)
        C_T_teo = np.where((S_range >= E1) & (S_range <= E2), S_range - E1, 0)
        Pi_T_teo = S_range - C_T_teo + C0 * np.exp(sc['r'] * T)
        
        ax2.plot(S_range, Pi_T_teo, color='black', lw=2, label='Perfil Portafolio $\Pi_T$')
        ax2.plot(S_range, S_range, color='gray', linestyle='--', label='Activo Sin Cobertura')
        
        # Scatter de la nube de puntos simulada
        ax2.scatter(S_T, Pi_T, color='blue', alpha=0.1, label='Simulaciones M=1000')
        
        # Histograma de la distribución del subyacente
        ax2_hist = ax2.twinx()
        ax2_hist.hist(S_T, bins=40, color='red', alpha=0.15, label='Distribución $S_T$')
        ax2_hist.set_yticks([])
        
        ax2.set_title(f"Valor Final en Madurez ($t=T$)\n{sc['title']}")
        ax2.set_xlabel('Precio Final del Activo $S_T$')
        ax2.set_ylabel('Valor del Portafolio $\Pi_T$')
        
        lines, labels = ax2.get_legend_handles_labels()
        lines2, labels2 = ax2_hist.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='upper left')
        ax2.grid(True, alpha=0.3)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    output_dir = 'Informe'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'portafolio_seguro.png')
    plt.savefig(output_path, dpi=300)
    print(f"Gráfico guardado en: {output_path}")

if __name__ == "__main__":
    plot_analysis()
