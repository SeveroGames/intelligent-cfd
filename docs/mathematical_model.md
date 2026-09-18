# Formulación Matemática y Discretización (Lid-Driven Cavity)

## 1. El Problema Físico y el Dominio
Vamos a simular un flujo 2D, incompresible y transitorio dentro de una cavidad cuadrada donde la pared superior se mueve a una velocidad constante.

* **Dominio espacial:** $\Omega = [0, L_x] \times [0, L_y]$
* **Variables primitivas:** Velocidad horizontal $u(x,y,t)$, velocidad vertical $v(x,y,t)$ y presión $p(x,y,t)$.
* **Propiedades constantes:** Densidad ($\rho$) y viscosidad dinámica ($\mu$).

## 2. Ecuaciones Gobernantes (2D)
Para un fluido incompresible, las ecuaciones de Navier-Stokes en dos dimensiones se expresan como:

**1. Ecuación de Continuidad (Conservación de masa):**
$$ \frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} = 0 $$

**2. Conservación de Momento en X:**
$$ \frac{\partial u}{\partial t} + u \frac{\partial u}{\partial x} + v \frac{\partial u}{\partial y} = -\frac{1}{\rho} \frac{\partial p}{\partial x} + \nu \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right) $$

**3. Conservación de Momento en Y:**
$$ \frac{\partial v}{\partial t} + u \frac{\partial v}{\partial x} + v \frac{\partial v}{\partial y} = -\frac{1}{\rho} \frac{\partial p}{\partial y} + \nu \left( \frac{\partial^2 v}{\partial x^2} + \frac{\partial^2 v}{\partial y^2} \right) $$

*(Donde $\nu = \mu / \rho$ es la viscosidad cinemática).*

## 3. Condiciones de Frontera e Iniciales
Para el problema de la cavidad con tapa móvil (Lid-Driven Cavity):

* **Condición Inicial (t = 0):** El fluido está en reposo. $u = 0, v = 0, p = 0$ en todo el dominio.
* **Pared Superior (Tapa):** $u = U_{tapa}, v = 0$ (Dirichlet).
* **Paredes Izquierda, Derecha e Inferior:** $u = 0, v = 0$ (Condición de no-deslizamiento o *no-slip*).
* **Presión:** Se fija un nodo de referencia $p(x,y) = 0$ para evitar infinitas soluciones, y gradiente nulo en las paredes ($\partial p / \partial n = 0$).

## 4. Discretización (Diferencias Finitas)
Las computadoras no pueden resolver derivadas continuas. Usaremos el método de **Diferencias Finitas** discretizando el dominio en una malla de $nx \times ny$ nodos, con distancias $\Delta x$ y $\Delta y$. El tiempo avanzará en pasos $\Delta t$.

Usaremos un esquema **FTCS (Forward in Time, Central in Space)** modificado con diferencias hacia atrás (backward) para los términos convectivos (upwind):

* **Derivada temporal (Forward):** 
  $$ \frac{\partial u}{\partial t} \approx \frac{u^{n+1}_{i,j} - u^n_{i,j}}{\Delta t} $$
* **Derivada espacial de primer orden (Central):** 
  $$ \frac{\partial u}{\partial x} \approx \frac{u^n_{i+1,j} - u^n_{i-1,j}}{2\Delta x} $$
* **Derivada espacial de segundo orden (Central):** 
  $$ \frac{\partial^2 u}{\partial x^2} \approx \frac{u^n_{i+1,j} - 2u^n_{i,j} + u^n_{i-1,j}}{\Delta x^2} $$

## 5. Método de Proyección (Chorin)
Para acoplar la velocidad y la presión (el gran desafío en flujos incompresibles), usaremos un método de pasos fraccionados:
1. **Paso predictor:** Calculamos una velocidad intermedia ($u^*, v^*$) ignorando el gradiente de presión.
2. **Ecuación de Poisson para la presión:** Usamos $u^*$ y $v^*$ para calcular el campo de presión $p^{n+1}$ que garantice que se cumpla la continuidad.
   $$ \nabla^2 p = \frac{\rho}{\Delta t} \nabla \cdot \vec{u}^* $$
3. **Paso corrector:** Actualizamos las velocidades finales $u^{n+1}, v^{n+1}$ usando los gradientes de la nueva presión.

## 6. Estabilidad Numérica (Condición CFL)
Para evitar que la simulación "explote" (inestabilidad numérica), el paso de tiempo $\Delta t$ no puede ser arbitrario. Debe cumplir la condición de Courant-Friedrichs-Lewy (CFL):

$$ \Delta t < \frac{\Delta x}{c} $$

En nuestro código exigiremos que la información no viaje más de una celda por iteración, limitando $\Delta t$ en función de la viscosidad y las velocidades máximas.