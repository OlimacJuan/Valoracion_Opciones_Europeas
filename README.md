# Valoración de Opciones Europeas y Gestión de Riesgo (Call Ventana)

Este repositorio contiene el desarrollo integral del **Proyecto 2**, enfocado en la modelación estocástica, valoración de derivados exóticos y composición de portafolios de inversión seguros utilizando Python y LaTeX.

## Descripción General
El proyecto se divide en tres ejes fundamentales:
1. **Modelación Estocástica:** Simulación de trayectorias de precios de activos financieros utilizando el Movimiento Browniano Geométrico y la discretización de Euler-Maruyama.
2. **Valoración Analítica:** Deducción de las condiciones de frontera, resolución de la ecuación de Black-Scholes y graficación de la superficie teórica para una opción exótica tipo **"Call Ventana"**.
3. **Gestión de Portafolio:** Construcción y simulación de Monte Carlo de una estrategia *Covered Call Ventana* para demostrar matemáticamente la amortiguación del riesgo ante escenarios adversos sin sacrificar las ganancias extremas del mercado.

## Estructura del Repositorio

- `Informe/`
  - `informe_proyecto.tex`: Código fuente en LaTeX que contiene el documento final formal con todo el marco teórico, algoritmos, deducciones analíticas, resultados y conclusiones.
  - `simulacion_3x3.png`: Análisis gráfico de sensibilidad del precio del activo frente a diversas tasas y volatilidades.
  - `superficie_3x3.png`: Superficies tridimensionales de valoración teórica $C(S,t)$ de la Call Ventana.
  - `portafolio_seguro.png`: Gráficos de evolución y perfiles de riesgo que validan la seguridad del portafolio estructurado.

- **Scripts de Python:**
  - `simulacion_wiener.py`: Implementa el generador de trayectorias del Proceso de Wiener y genera la figura 3x3 de caminos aleatorios.
  - `superficie_ventana.py`: Ejecuta el algoritmo analítico (CDF de la distribución normal) para calcular y proyectar las superficies tridimensionales de la opción ventana.
  - `simulacion_portafolio.py`: Módulo de Monte Carlo que evalúa el desempeño temporal y el perfil de pago final de un portafolio asegurado (*Covered Call Ventana*) frente a un activo sin cobertura.

- `Valoracion de Opciones Europeas/`: Directorio que contiene todo el material bibliográfico y las notas teóricas originales proporcionadas para el curso (Archivos Markdown sobre Cálculo Estocástico, Lemas de Ito, y la Ecuación de Difusión).
- `Enunciado Proyecto 2.md`: Documento con los requerimientos originales del proyecto.

## Uso
Para replicar los resultados numéricos, ejecute cualquiera de los tres scripts de Python desde la raíz del proyecto. Las imágenes resultantes se exportarán automáticamente y se sobrescribirán en la carpeta `Informe/`, listas para ser compiladas en el documento de LaTeX.