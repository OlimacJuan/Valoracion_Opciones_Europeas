# Valoración de Opciones Europeas Call Ventana

Proyecto académico de Métodos Matemáticos en Gestión Financiera (MMGF) que implementa la valoración analítica y simulación numérica de **opciones Call Ventana** (Window Call Options) sobre un activo subyacente modelado mediante el proceso de Black-Scholes.

## Descripción

Una opción **Call Ventana** es un derivado financiero europeo cuyo derecho de ejercicio está condicionado a que el precio del activo subyacente al vencimiento se encuentre dentro de un intervalo predefinido $[E_1, E_2]$. Si el precio queda fuera de esta "ventana", la opción expira sin valor, independientemente de si el activo subió o bajó.

Este proyecto cubre:
1. **Simulación del proceso de valor** del activo subyacente (Movimiento Browniano Geométrico).
2. **Derivación analítica** de la EDP de Black-Scholes y su solución cerrada para la opción ventana, vía la ecuación del calor.
3. **Construcción de un portafolio de cobertura** (delta-neutral) y demostración de la utilidad de la opción ventana como instrumento de aseguramiento.

---

## Estructura del Proyecto

```
Valoracion_Opciones_Europeas/
│
├── Codigo/
│   ├── Punto1.py     # Simulación del subyacente S(t) - MBG (Euler-Maruyama)
│   ├── Punto2.py     # Superficies 3D del valor C(S,t) para dos escenarios
│   └── Punto3.py     # Portafolio replicante y estrategia Covered Window Call
│
├── Figuras/
│   ├── Punto1_Figura1.png   # Simulaciones del proceso S(t) con tendencia
│   ├── Punto1_Figura2.png   # Simulaciones del proceso S(t) sin tendencia
│   ├── Punto2_Figura1.png   # Superficies C(S,t) para r=0.002 y r=0.0
│   └── Punto3_Figura1.png   # Comparación portafolio asegurado vs no asegurado
│
└── Informe/
    └── Documento.tex         # Informe técnico completo en LaTeX
```

---

## Scripts

### `Codigo/Punto1.py` — Simulación del Proceso de Valor
Implementa el algoritmo de discretización de Euler-Maruyama para el Movimiento Browniano Geométrico:

$$S_{i+1} = S_i + \mu S_i \Delta t + \sigma S_i \sqrt{\Delta t}\, Z_i, \quad Z_i \sim \mathcal{N}(0,1)$$

Genera una figura con tres subgráficas comparando **1, 3 y 10 trayectorias** simultáneas del proceso, para 100 periodos de 5 unidades de tiempo.

**Parámetros principales:**
| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `N` | 100 | Número de pasos de tiempo |
| `delta_t` | 5.0 | Incremento temporal |
| `S_0` | 4.0 | Valor inicial del activo |
| `mu` | 0.0 | Tendencia (drift) |
| `sigma` | 0.01 | Volatilidad |

---

### `Codigo/Punto2.py` — Superficies de Valoración C(S, t)
Calcula y grafica en 3D el precio justo de la opción ventana mediante la fórmula cerrada derivada de la transformación de la EDP de Black-Scholes a la ecuación del calor:

$$C(S,t) = S\bigl[F_Z(d_1(S,S_{\min})) - F_Z(d_1(S,E_2))\bigr] - Ee^{-r(T-t)}\bigl[F_Z(d_2(S,S_{\min})) - F_Z(d_2(S,E_2))\bigr]$$

Genera superficies para dos escenarios de parámetros:
- **Caso 1:** $r = 0.002$, $\sigma = 0.01$
- **Caso 2:** $r = 0.0$, $\sigma = 0.01$

**Parámetros del contrato:**
| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `E` | 100 | Precio Strike |
| `E1` | 90 | Límite inferior de la ventana |
| `E2` | 110 | Límite superior de la ventana |
| `T` | 1.0 | Tiempo al vencimiento (años) |

---

### `Codigo/Punto3.py` — Portafolio de Cobertura y Aseguramiento
Contiene dos secciones:

**Sección 1 – Portafolio Replicante (Delta Hedging):**
Construye un portafolio auto-financiado $\Pi_t = \Delta_t S_t + B_t$ que replica exactamente el valor de la opción ventana en cada instante, con rebalanceo continuo a lo largo de 252 pasos.

**Sección 2 – Covered Window Call (Demostración de Seguridad):**
Simula 25 trayectorias bajo la estrategia de aseguramiento:

$$\Pi_t^{\text{seg}} = S_t - C_t + B_t, \quad B_t = C_0 e^{rt}$$

Compara visualmente la dispersión del portafolio **sin cobertura** (solo $S_t$) frente al portafolio **asegurado** (Covered Window Call), demostrando la reducción de varianza que aporta la opción ventana.

---

## Requisitos

```bash
pip install numpy matplotlib scipy
```

**Python:** 3.8+

---

## Ejecución

```bash
# Simular y graficar el proceso de valor
python Codigo/Punto1.py

# Generar superficies de valoración C(S,t)
python Codigo/Punto2.py

# Simular el portafolio de cobertura y demostrar seguridad
python Codigo/Punto3.py
```

---

## Fundamento Matemático

El proyecto se basa en la **EDP de Black-Scholes** derivada por el argumento de portafolio libre de riesgo (no arbitraje):

$$\frac{\partial C}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 C}{\partial S^2} + rS\frac{\partial C}{\partial S} - rC = 0$$

La solución analítica se obtiene mediante la transformación de variables $x = \ln(S/E)$, $\tau = \frac{\sigma^2}{2}(T-t)$, $C = Ev(x,\tau)$, reduciendo el problema a la **ecuación del calor** $\frac{\partial u}{\partial \tau} = \frac{\partial^2 u}{\partial x^2}$, cuya solución integral vía el núcleo gaussiano conduce a la fórmula cerrada final.

---

## Informe

El informe técnico completo con la derivación matemática detallada, la documentación de los algoritmos y el análisis de resultados se encuentra en `Informe/Documento.tex` (compilable con LaTeX/pdflatex).
