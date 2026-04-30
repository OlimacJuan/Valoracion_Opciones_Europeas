import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ====================================================================
# Parámetros del Contrato
# ====================================================================
N = 252            # Número de pasos de tiempo (252 días de trading)
T = 1.0            # Tiempo de expiración (1 año)
delta_t = T / N    # Incremento de tiempo finito
S_0 = 100.0        # Valor inicial del subyacente
E = 100.0          # Precio Strike

# Sección 1 – Portafolio Replicante (cobertura delta)
E1_h = 90.0        # Límite inferior de la ventana
E2_h = 110.0       # Límite superior de la ventana
mu_h = 0.05        # Tendencia
sigma_h = 0.20     # Volatilidad
r_h = 0.05         # Tasa libre de riesgo

# Sección 2 – Demostración de Seguridad (Covered Window Call)
E1_s = 80.0        # Ventana más amplia
E2_s = 120.0
mu_s = 0.05
sigma_s = 0.05     # Volatilidad baja
r_s = 0.05
N_sims = 25        # Número de simulaciones para la comparación

# ====================================================================
# Funciones Comunes
# ====================================================================
def simular_S(N, delta_t, S_0, mu, sigma):
    """Simula la evolución del activo S (discretización Euler-Maruyama del Punto 1)."""
    t = np.zeros(N + 1)
    S = np.zeros(N + 1)
    t[0] = 0.0
    S[0] = S_0
    for i in range(N):
        t[i+1] = t[i] + delta_t
        S[i+1] = S[i] + mu * S[i] * delta_t + sigma * S[i] * np.sqrt(delta_t) * np.random.randn()
    return t, S

def call_ventana_y_delta(S, t, r, sigma, E, E1, E2, T):
    """Retorna el Precio Teórico (C) y el Delta (∂C/∂S) de la Opción Ventana."""
    S_min = max(E1, E)
    if S_min >= E2 or S <= 1e-8:
        return 0.0, 0.0

    tau = T - t
    if tau <= 1e-8:
        C = max(S - E, 0.0) if E1 <= S <= E2 else 0.0
        Delta = 1.0 if (E1 <= S <= E2 and S > E) else 0.0
        return C, Delta

    d1_Smin = (np.log(S / S_min) + (r + sigma**2 / 2) * tau) / (sigma * np.sqrt(tau))
    d1_E2   = (np.log(S / E2)    + (r + sigma**2 / 2) * tau) / (sigma * np.sqrt(tau))
    d2_Smin = (np.log(S / S_min) + (r - sigma**2 / 2) * tau) / (sigma * np.sqrt(tau))
    d2_E2   = (np.log(S / E2)    + (r - sigma**2 / 2) * tau) / (sigma * np.sqrt(tau))

    C     = S * (norm.cdf(d1_Smin) - norm.cdf(d1_E2)) \
            - E * np.exp(-r * tau) * (norm.cdf(d2_Smin) - norm.cdf(d2_E2))
    Delta = norm.cdf(d1_Smin) - norm.cdf(d1_E2)
    return C, Delta

# ====================================================================
# SECCIÓN 1: Portafolio de Cobertura Delta (una trayectoria)
# ====================================================================
t, S = simular_S(N, delta_t, S_0, mu_h, sigma_h)

C_t   = np.zeros(N + 1)
Delta_t = np.zeros(N + 1)
B_t   = np.zeros(N + 1)
Pi_t  = np.zeros(N + 1)

# Inicialización en t = 0
C_0, Delta_0 = call_ventana_y_delta(S[0], t[0], r_h, sigma_h, E, E1_h, E2_h, T)
C_t[0]   = C_0
Delta_t[0] = Delta_0
B_t[0]   = C_0 - Delta_0 * S[0]          # B = C - Δ·S  (portafolio auto-financiado)
Pi_t[0]  = Delta_t[0] * S[0] + B_t[0]

for i in range(N):
    B_next  = B_t[i] * np.exp(r_h * delta_t)     # banco devenga intereses
    Pi_next = Delta_t[i] * S[i+1] + B_next        # valor portafolio antes de rebalanceo

    c_val, delta_val = call_ventana_y_delta(S[i+1], t[i+1], r_h, sigma_h, E, E1_h, E2_h, T)
    C_t[i+1]   = c_val
    Delta_t[i+1] = delta_val
    Pi_t[i+1]  = Pi_next
    B_t[i+1]   = Pi_next - delta_val * S[i+1]     # rebalanceo: ajustar cuenta bancaria

# ====================================================================
# Demostración de Seguridad (Covered Window Call)
# ====================================================================
t_grid = np.linspace(0, T, N + 1)
C_0_s  = call_ventana_y_delta(S_0, 0.0, r_s, sigma_s, E, E1_s, E2_s, T)[0]
B_t_s  = C_0_s * np.exp(r_s * t_grid)   # prima recibida crece en el banco

trayectorias_S  = []
trayectorias_Pi = []

for _ in range(N_sims):
    t_sim, S_sim = simular_S(N, delta_t, S_0, mu_s, sigma_s)
    trayectorias_S.append(S_sim)

    # Valor de la opción en cada instante
    C_t_s = np.zeros(N + 1)
    for i in range(N):
        C_t_s[i] = call_ventana_y_delta(S_sim[i], t_sim[i], r_s, sigma_s, E, E1_s, E2_s, T)[0]
    S_T = S_sim[-1]
    C_t_s[-1] = max(S_T - E, 0.0) if E1_s <= S_T <= E2_s else 0.0

    # Portafolio Asegurado: Activo − Obligación de la Opción Vendida + Prima en Banco
    trayectorias_Pi.append(S_sim - C_t_s + B_t_s)

# Figura 2 – Comparación de Seguridad
fig2, axes2 = plt.subplots(1, 2, figsize=(16, 7), sharey=True)

for S_tray in trayectorias_S:
    axes2[0].plot(t_grid, S_tray, alpha=0.55, lw=1)
axes2[0].axhline(E1_s, color='red',   linestyle=':', lw=1.5, label='$E_1$ (Límite Inf)')
axes2[0].axhline(E2_s, color='red',   linestyle=':', lw=1.5, label='$E_2$ (Límite Sup)')
axes2[0].set_title('Portafolio No Asegurado\n(Solo Activo Subyacente $S_t$)', fontsize=13)
axes2[0].set_xlabel('Tiempo ($t$)', fontsize=12)
axes2[0].set_ylabel('Valor del Portafolio', fontsize=12)
axes2[0].legend(); axes2[0].grid(True, linestyle='--', alpha=0.6)

for Pi_tray in trayectorias_Pi:
    axes2[1].plot(t_grid, Pi_tray, alpha=0.55, lw=1)
axes2[1].axhline(E + B_t_s[-1], color='green', linestyle='-', lw=2, label='Valor Asegurado ($E + B_T$)')
axes2[1].set_title('Portafolio Asegurado\n(Covered Window Call)', fontsize=13)
axes2[1].set_xlabel('Tiempo ($t$)', fontsize=12)
axes2[1].legend(); axes2[1].grid(True, linestyle='--', alpha=0.6)

fig2.suptitle(
    'Demostración de Seguridad del Portafolio mediante Opción Ventana\n'
    f'$r={r_s}$, $\\sigma={sigma_s}$, Strike $E={E}$, Ventana $[{E1_s}, {E2_s}]$',
    fontsize=15, fontweight='bold'
)
plt.tight_layout()
plt.show()
