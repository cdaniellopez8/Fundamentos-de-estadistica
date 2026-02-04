import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import math
import plotly.graph_objects as go


# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="Estadística: Datos Agrupados")

# --- FUNCIONES DE AGRUPACIÓN ---

def sturges_rule(n):
    """Calcula el número de intervalos sugerido por la Regla de Sturges."""
    if n <= 1:
        return 1
    return int(1 + 3.322 * math.log10(n))

def calculate_amplitude(min_val, max_val, k):
    """Calcula la amplitud de clase."""
    if k <= 0:
        return 1.0
    return (max_val - min_val) / k

def generar_tabla_agrupada(data, k=None, amplitud=None):
    """
    Genera la tabla de frecuencia para datos agrupados.
    
    Ajusta ligeramente los límites para asegurar que el mínimo y el máximo caigan
    dentro de un intervalo cerrado/abierto de manera estándar.
    """
    n = len(data)
    
    if k is None:
        k = sturges_rule(n)
    
    data_min = data.min()
    data_max = data.max()
    
    # Asegurar que el límite inferior sea un poco menor que el mínimo
    # y el superior un poco mayor que el máximo, para incluir todos los datos
    # y evitar problemas de límites exactos.
    rango = data_max - data_min
    
    if amplitud is None:
        amplitud = calculate_amplitude(data_min, data_max, k)
        # Redondear la amplitud a una cifra conveniente (ej: 1 decimal más que el dato)
        if rango > 0:
            decimal_places = max(0, -int(math.floor(math.log10(amplitud)))) + 1
            amplitud = round(amplitud, decimal_places)
            
    # Calcular límites de los bins
    # Ajustar el punto de inicio para ser ligeramente menor al mínimo
    start_point = data_min - (data_min % amplitud) if data_min % amplitud != 0 else data_min
    if start_point + amplitud * k < data_max:
         k += 1 # Ajuste si no cubrimos el máximo con la amplitud calculada
         
    bins = np.arange(data_min, data_max + amplitud, amplitud)
    
    # Corregir la definición de los bins si es necesario
    if bins[-1] < data_max:
        bins = np.append(bins, bins[-1] + amplitud)
    
    # Asegurar que los bins son únicos y ordenados
    bins = np.unique(bins)
    k = len(bins) - 1 # Número real de intervalos

    # Generar intervalos (bins)
    # Por convención, (a, b] o [a, b)
    # Usaremos [a, b) para todos menos el último para evitar errores comunes
    # Se ajusta el límite derecho del último intervalo para ser cerrado
    
    intervals = pd.cut(data, bins=bins, include_lowest=True, right=False)
    
    # Contar frecuencias
    freq_abs = intervals.value_counts().sort_index()
    
    # Crear DataFrame de la tabla
    tabla = pd.DataFrame({
        'Clase/Intervalo': freq_abs.index.astype(str),
        'Frecuencia Absoluta': freq_abs.values
    }).reset_index(drop=True)
    
    # Calcular Marca de Clase ($x_i$)
    # Para la visualización: punto medio del intervalo
    tabla['Límite Inferior'] = [i.left for i in freq_abs.index]
    tabla['Límite Superior'] = [i.right for i in freq_abs.index]
    tabla['Marca de Clase ($x_i$)'] = (tabla['Límite Inferior'] + tabla['Límite Superior']) / 2
    
    # Calcular Frecuencias Relativas y Porcentajes
    tabla['Frecuencia Relativa'] = tabla['Frecuencia Absoluta'] / n
    tabla['Porcentaje (%)'] = tabla['Frecuencia Relativa'] * 100
    
    # Calcular Frecuencias Acumuladas
    tabla['Frecuencia Acumulada'] = tabla['Frecuencia Absoluta'].cumsum()
    tabla['Frecuencia Relativa Acumulada'] = tabla['Frecuencia Relativa'].cumsum()
    
    # Formato de los nombres de columnas
    tabla.columns = ['Clase/Intervalo', 'Frecuencia Absoluta', 'Límite Inferior', 'Límite Superior', 'Marca de Clase ($x_i$)',
                     'Frecuencia Relativa', 'Porcentaje (%)', 'Frecuencia Acumulada', 'Frecuencia Relativa Acumulada']
    
    # Redondeo final para la tabla
    format_mapping = {
        'Frecuencia Relativa': '{:.4f}',
        'Porcentaje (%)': '{:.2f}',
        'Frecuencia Relativa Acumulada': '{:.4f}'
    }
    
    # Aplicar formato a una copia para evitar SettingWithCopyWarning
    tabla_display = tabla.copy()
    for col, fmt in format_mapping.items():
        if col in tabla_display.columns:
            tabla_display[col] = tabla_display[col].apply(lambda x: fmt.format(x))
            
    # Asegurar que el total de f_r y % sea 1.0000 y 100.00
    if 'Frecuencia Relativa' in tabla_display.columns:
        tabla_display.loc['Total'] = ['TOTAL', tabla['Frecuencia Absoluta'].sum(), '', '', '', 
                                       1.0, 100.0, '', '']

    return tabla, tabla_display, amplitud, k

# --- SIMULACIÓN DE DATASETS ---

@st.cache_data
def load_datasets():
    """Genera datasets simulados para datos agrupados."""
    np.random.seed(42)
    
    # 1. Estaturas (Continuo)
    estaturas = np.random.normal(loc=1.70, scale=0.10, size=150)
    estaturas = pd.Series(np.round(estaturas, 2), name='Estatura (m)')

    # 2. Edades de Empleados (Discreto con muchos valores)
    edades = np.random.randint(low=22, high=68, size=200)
    edades = pd.Series(edades, name='Edad (años)')
    
    # 3. Tiempos de Reacción (Continuo)
    tiempos = np.random.exponential(scale=30, size=120)
    tiempos = pd.Series(np.round(tiempos, 1), name='Tiempo de Reacción (ms)')
    
    # 4. Calificaciones (Discreto con muchos valores)
    calificaciones = np.random.randint(low=30, high=101, size=180)
    calificaciones = pd.Series(calificaciones, name='Calificación (0-100)')
    
    # Datos NO agrupados (para sección de comparación)
    color = pd.Series(np.random.choice(['Rojo', 'Azul', 'Verde', 'Amarillo'], size=100), name='Color Favorito')
    hermanos = pd.Series(np.random.randint(0, 5, size=100), name='Número de Hermanos')
    
    return {
        "Estaturas de Estudiantes (Continuo)": estaturas,
        "Edades de Empleados (Discreto Alto)": edades,
        "Tiempos de Reacción (Continuo)": tiempos,
        "Calificaciones de Examen (Discreto Alto)": calificaciones,
        "Color Favorito (Nominal Bajo)": color,
        "Número de Hermanos (Discreto Bajo)": hermanos
    }

# --- BARRA LATERAL (CONTROL DE PÁGINAS) ---

datasets = load_datasets()
dataset_keys = list(datasets.keys())

st.sidebar.title("📚 Menú de Contenido")
page = st.sidebar.radio("Navegar a:", [
    "1. Inicio",
    "2. Comparación: ¿Agrupar o No?",
    "3. Conceptos Fundamentales",
    "4. Constructor de Tablas", 
    "5. Explorador de Datos Agrupados",
    "6. Comparador de Gráficos",
    "7. Casos Reales - Análisis Guiado",
    "8. Cuestionario Final",
    "9. Ventajas y Desventajas",
], index=0)

# --- EJECUCIÓN DEL MÓDULO SELECCIONADO ---


if page == "1. Inicio":
    st.title("📊 Análisis Estadístico para Datos Agrupados")
    
    ## ¿Qué son Datos Agrupados y por qué existen?
    
    st.markdown("""
    Imagina que mides la **estatura de 200 personas** y obtienes valores continuos (1.65, 1.67, 1.68...).
    
    Si intentaras hacer una tabla de frecuencia para **cada valor único**, la tabla sería excesivamente larga (podría tener hasta más de 150 filas) y **demasiado complicada de interpretar**.
    
    La solución es la **Agrupación en Intervalos** (o **Clases**):
    """)
    
    st.info("En lugar de una fila por valor, creamos rangos (ejemplo: **[1.60 - 1.65)**). Ahora, todos los datos que caen en ese rango se cuentan en una sola fila, resumiendo la información de manera efectiva.")

    st.markdown("---")
    
    ## Diferencia Clave con Datos No Agrupados

    st.markdown("""
    * **Datos No Agrupados:** Cada valor único tiene su propia fila. (Ideal para datos **Nominales, Ordinales** o **Discretos con pocos valores únicos**).
    * **Datos Agrupados:** Los valores se organizan en **intervalos/clases**. (Necesario para datos **Continuos** o **Discretos/Ordinales con muchísimos valores**).
    """)

    st.markdown("### 🔍 ¿Cuándo DEBO Agrupar?")

    data_agrupar = pd.DataFrame({
        "Tipo de Dato": ["Nominal", "Ordinal (Baja)", "Discreta (Baja)", "Discreta (Alta)", "Continua"],
        "Ejemplo": ["Género (M/F)", "Satisfacción (1-5)", "Hijos (0-4)", "Edad (18-65)", "Estatura (m)"],
        "Valores Únicos": ["2", "5", "5", "47+", "Infinitos"],
        "¿Agrupar?": ["❌ NO", "❌ NO", "❌ NO", "✅ SÍ", "✅ SÍ"],
        "Razón": ["Pocas categorías", "Pocas categorías. Se mantiene el orden.", "Pocos valores únicos", "Muchos valores (poca repetición)", "Siempre continuo"],
    })
    st.table(data_agrupar.set_index('Tipo de Dato'))

    st.markdown("""
    **Debes agrupar cuando:**
    1.  Trabajas con **Variables Continuas** (peso, estatura, tiempo, temperatura).
    2.  Trabajas con **Variables Discretas u Ordinales con muchos valores únicos** (ej. calificaciones de 0 a 100, donde la tabla no agrupada es inútil).
    """)
    
elif page == "3. Conceptos Fundamentales":
    st.title("📚 Conceptos Fundamentales de Datos Agrupados")
    
    st.markdown("""
    La terminología es específica. Aquí tienes los nuevos conceptos clave que debes dominar:
    """)
    
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Términos del Intervalo")
        
        st.markdown("* **Clase o Intervalo:** El rango de valores que agrupa los datos. Ejemplo: **$[1.65 - 1.70)$**.")
        st.markdown("* **Límite Inferior ($L_i$):** El valor mínimo del intervalo. (1.65)")
        st.markdown("* **Límite Superior ($L_s$):** El valor máximo del intervalo. (1.70)")
        st.markdown("""
        > **Convención Importante (Inclusión de Datos):** > * Un **corchete** `[` o `]` indica que el límite es **inclusivo** (el valor sí se cuenta en esa clase).
        > * Un **paréntesis** `(` o `)` indica que el límite es **exclusivo** (el valor no se cuenta, se cuenta en la clase siguiente).
        
        Por lo general, los intervalos son **cerrados por la izquierda** y **abiertos por la derecha**  $[L_i, L_s)$, lo que significa que, para este ejemplo el dato $1.65$ se incluye, pero el dato $1.70$ **no se incluye** (se incluye en el siguiente intervalo).
        """)
        
    with col_b:
        st.subheader("Términos de Medida")
        
        st.markdown("* **Amplitud de Clase ($A$):** La diferencia entre los límites. $\\mathbf{{A = L_s - L_i}}$. Ejemplo: $1.70 - 1.65 = 0.05$.")
        st.markdown("* **Marca de Clase ($x_i$):** El **punto medio** del intervalo. Es el valor que representa a toda la clase para cálculos posteriores (como la media). $\\mathbf{{x_i = \\frac{{L_i + L_s}}{{2}}}}$. Ejemplo: $\\frac{{1.65 + 1.70}}{{2}} = 1.675$.")
        st.markdown("* **Frecuencia de Clase ($f_i$):** La cantidad de datos que caen dentro de ese intervalo.")
        
    st.markdown("---")
    
    st.subheader("Reglas de Oro para la Agrupación")
    st.markdown("""
    * ❌ Los intervalos **NO se solapan**. Un dato no puede caer en dos clases diferentes.
    * ✅ Todos los intervalos deben tener la **misma amplitud** ($A$). (Esto es lo ideal para evitar sesgos).
    * ✅ Se deben incluir **TODOS** los datos del conjunto.
    """)


elif page == "4. Constructor de Tablas":

    st.title("🔨 Constructor de Tablas Agrupadas (Paso a Paso)")
    st.markdown("Aprende la metodología estadística para construir una tabla de frecuencias agrupada de manera formal.")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Datos de Ejemplo")
    # Usar un dataset de ejemplo para el constructor
    data_constructor = datasets["Estaturas de Estudiantes (Continuo)"]
    n_data_inicial = len(data_constructor) # Valor inicial de N
    min_data = data_constructor.min()
    max_data = data_constructor.max()
    rango_data = max_data - min_data

    st.markdown(f"**Dataset de Muestra:** Estaturas de Estudiantes ($N={n_data_inicial}$)")
    st.markdown(f"Valor Mínimo: **{min_data}** | Valor Máximo: **{max_data}** | Rango ($\mathbf{{R}}$): $\\mathbf{{= Máximo - Mínimo}} = {rango_data:.2f}$")
    st.markdown("---")

    # ----------------------------------------------------
    # --- PASO 1: Número de Intervalos (k) ---
    # ----------------------------------------------------
    st.subheader("Paso 1: ¿Cuántos Intervalos ($k$) necesito?")
    
    # Cálculo de la referencia de Sturges para el dataset inicial
    k_sturges_referencia = 1 + 3.322 * math.log10(n_data_inicial)
    
    st.markdown("""
    La primera pregunta que nos hacemos es... si debo agrupar por intervalos, entonces ¿Cuántos Intervalos (los cuales llamaremos $k$) necesito?
                
    La **Regla de Sturges** nos da una **sugerencia** basada en el tamaño de la muestra ($N$). La formula es la siguiente:
                
    $$ 
    k = 1 + 3.322 \\times \\log_{10}(N)
    $$
    """)
    
    # Mostrar el resultado CON decimales para que sea claro
    st.info(f"Para $N={n_data_inicial}$ datos, la regla sugiere: $\\mathbf{{k_{{Sturges}} \\approx {k_sturges_referencia:.4f}}}$ intervalos.")
    
    st.markdown("---")
    
    ### ✍️ Decisión de k (Del decimal al entero impar)
    
    st.markdown("""
    ### 🤔 ¿Cómo interpretar este resultado?
    
    La fórmula de Sturges nos da un numero de intervalos a utilizar, sin embargo este va a ser muy probablemente un **número decimal**, pero necesitamos un **número entero** de intervalos. Por este motivo debemos redondear.
    Además, por convención estadística, buscamos que este número sea **impar** para mantener la simetría en la distribución.
    """)
    
    st.info("📌 **Nota importante:** Si podemos tener un número de intervalos par (No es obligatorio que sea impar), sin embargo, se busca que sea impar por convención para favorecer la simetría.")            
    
    st.markdown("""
    **El proceso es simple:**
    """)

        
    k_entero_crudo = math.floor(k_sturges_referencia) # Obtener el entero previo
    
    st.markdown(f"""
    **Paso 1:** Identificar el entero inferior  
    De $k_{{Sturges}} \\approx {k_sturges_referencia:.4f}$, tomamos la parte entera: **{k_entero_crudo}**
    """)
    
    # CORRECCIÓN: Aplicar la regla correcta
    # Si el entero previo es IMPAR → redondear HACIA ABAJO (mantener)
    # Si el entero previo es PAR → redondear HACIA ARRIBA (sumar 1)
    if k_entero_crudo % 2 == 0:
        # Si es PAR, se redondea HACIA ARRIBA para obtener el impar siguiente
        k_final_sugerido = k_entero_crudo + 1
        razon_redondeo = f"""
**Paso 2:** Verificar si es impar  
El número **{k_entero_crudo}** es **PAR** ❌

**Paso 3:** Aplicar la regla de redondeo  
Como es PAR, redondeamos **HACIA ARRIBA** al siguiente impar: $\\mathbf{{{k_final_sugerido}}}$ ✓
"""
    else:
        # Si es IMPAR, se redondea HACIA ABAJO (mantener el mismo valor)
        k_final_sugerido = k_entero_crudo
        razon_redondeo = f"""
**Paso 2:** Verificar si es impar  
El número **{k_entero_crudo}** es **IMPAR** ✓

**Paso 3:** Aplicar la regla de redondeo  
Como ya es IMPAR, lo mantenemos (redondeamos HACIA ABAJO): $\\mathbf{{{k_final_sugerido}}}$ ✓
"""
    
    st.markdown(razon_redondeo)
    
    st.markdown("---")
    st.markdown("### 📚 La Regla General de Redondeo de Sturges")
    
    # EXPLICACIÓN CON EJEMPLO 
    st.markdown("""
    Esta convención busca que el número final de intervalos sea **siempre impar**:
    
    - Si el entero es **IMPAR** → Redondear **HACIA ABAJO** (mantener ese valor)
    - Si el entero es **PAR** → Redondear **HACIA ARRIBA** (sumar 1)
    """)
    
    # Ejemplo con caja destacada
    st.success("""
**Ejemplos para entender la regla:**

**Ejemplo A:** Si $k_{Sturges} = 7.82$
- Entero inferior: $7$ (impar)
- **Decisión:** Como ya es impar, redondeamos hacia abajo → $k = 7$ ✓

**Ejemplo B:** Si $k_{Sturges} = 8.45$  
- Entero inferior: $8$ (par)
- **Decisión:** Como es par, redondeamos hacia arriba → $k = 9$ ✓
    """)
    
    st.markdown("---")
    st.markdown("---")
    
    ### 🧮 Calculadora Interactiva de Sturges
    st.markdown("### 🧮 Calculadora Interactiva")
    st.markdown("Experimenta con diferentes tamaños de muestra y observa cómo cambia la recomendación:")
    
    # Slider para N
    n_calculadora = st.slider(
        "Tamaño de muestra (N):",
        min_value=10,
        max_value=1000,
        value=n_data_inicial,
        step=1,
        key="n_calculadora_slider"
    )
    
    # Calcular k de Sturges para el N del slider
    k_sturges_calc = 1 + 3.322 * math.log10(n_calculadora)
    k_entero_calc = math.floor(k_sturges_calc)
    
    # Aplicar regla de redondeo
    if k_entero_calc % 2 == 0:
        k_sugerido_calc = k_entero_calc + 1
        tipo_calc = "PAR"
        accion_calc = "se redondea HACIA ARRIBA"
    else:
        k_sugerido_calc = k_entero_calc
        tipo_calc = "IMPAR"
        accion_calc = "se mantiene (redondeo HACIA ABAJO)"
    
    # Mostrar resultados en columnas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("N (Tamaño muestra)", f"{n_calculadora}")
    
    with col2:
        st.metric("k de Sturges", f"{k_sturges_calc:.4f}")
    
    with col3:
        st.metric("k Sugerido (impar)", f"{k_sugerido_calc}", delta=f"{tipo_calc}")
    
    st.info(f"📌 El entero inferior es **{k_entero_calc}** ({tipo_calc}), por lo tanto {accion_calc} → **k = {k_sugerido_calc}**")
    
    st.markdown("---")
    
    # Ahora mostrar el resumen para LOS DATOS REALES
    st.markdown(f"""
    ### ✅ Aplicando esta regla a nuestros datos:
    
    Nuestro dataset tiene $N = {n_data_inicial}$ observaciones, por lo tanto:
    - $k_{{Sturges}} \\approx {k_sturges_referencia:.4f}$
    - Número sugerido de intervalos: **$\\mathbf{{k = {k_final_sugerido}}}$**
    """)
    
    k_final = st.number_input("Usar $k$ (Intervalos) Final:", min_value=1, max_value=15, 
                               value=k_final_sugerido, 
                               step=1, key="k_final_input",
                               help="Puedes ajustar manualmente si lo deseas, pero se recomienda usar el valor sugerido.")

    st.markdown("---") 

    # ----------------------------------------------------
    # --- PASO 2: Amplitud de Clase (A) ---
    # ----------------------------------------------------
    st.subheader("Paso 2: ¿Qué Amplitud ($A$) deben tener?")
    
    st.markdown("""
    Ya tenemos cuantos intervalos vamos a utilizar, ahora necesitamos saber que tan grandes son estos invervalos, a este tamaño del intervalo le llamaremos **Amplitud**. La Amplitud es el ancho de cada intervalo. Se calcula dividiendo el Rango entre el número de intervalos elegido:
    $$ \\mathbf{A = \\frac{Rango (R)}{k}} $$
    """)
    
    col_k, col_a = st.columns(2)
    with col_k:
        st.markdown(f"**k Seleccionado (Paso 1):** $\\mathbf{{{k_final}}}$")
    
    # Recalculamos la amplitud CRUDA con el k_final seleccionado.
    amplitud_raw_calculada = calculate_amplitude(min_data, max_data, k_final)
    
    with col_a:
        st.markdown(f"**Amplitud Cruda Calculada (A):**")
        st.info(f"$$ \\mathbf{{A}} = \\frac{{{max_data:.2f} - {min_data:.2f}}}{{{k_final}}} \\approx {amplitud_raw_calculada:.6f} $$") 

    
    st.markdown("---")
    st.subheader("Redondeo de la Amplitud (Decisión Crítica) 📏")
    
    # Función auxiliar para redondear un número hacia arriba (por exceso).
    def round_up(n, decimals=0):
        multiplier = 10 ** decimals
        return math.ceil(n * multiplier) / multiplier

    # Lógica de sugerencia de redondeo para A
    decimales_datos = 2 # Asumimos 2 decimales para las estaturas
    a_sugerida_conveniente = round_up(amplitud_raw_calculada, decimales_datos)
    
    # Lógica simplificada para la sugerencia final, asegurando exceso
    if amplitud_raw_calculada < 0.1:
        a_sugerida_final = max(a_sugerida_conveniente, 0.05)
    elif amplitud_raw_calculada > 5:
        a_sugerida_final = math.ceil(amplitud_raw_calculada)
    else:
        a_sugerida_final = a_sugerida_conveniente
        
    # Última verificación de seguridad: debe cubrir el rango
    if a_sugerida_final < amplitud_raw_calculada:
        a_sugerida_final = round_up(amplitud_raw_calculada, decimales_datos) + 0.01

    st.markdown(f"""
    * 🛑 **Regla de Oro:** La amplitud **SIEMPRE se debe redondear HACIA ARRIBA (por exceso)** al número conveniente más cercano para garantizar que el **Valor Máximo** de los datos quede cubierto por el último intervalo.
    * **Ejemplo Explícito 1 (Decimales):** Si $\\mathbf{{A}} \\approx 0.0462$, se debe escoger $\\mathbf{{A=0.05}}$.
    * **Ejemplo Explícito 2 (Enteros):** Si $\\mathbf{{A}} \\approx 9.5651$ y queremos enteros, se escoge $\\mathbf{{A=10}}$ (el entero superior).
    
    **Conclusión para este caso:**
    """)
    
    st.success(f"Dado que $\\mathbf{{A}} \\approx {amplitud_raw_calculada:.6f}$, se recomienda redondear hacia arriba y escoger $\\mathbf{{A = {a_sugerida_final:.2f}}}$.")

    amplitud_final = st.number_input("Amplitud ($A$) Final (Redondeada):", min_value=0.01, max_value=1.0, 
                                     value=a_sugerida_final, 
                                     step=0.01, key="amplitud_final_input",
                                     help="Elige un valor redondeado conveniente. Debe ser mayor o igual al valor crudo calculado.")
    
    st.info(f"Rango cubierto con $k={k_final}$ y $A={amplitud_final}$: $\\text{{Desde }} {min_data:.2f} \\text{{ hasta }} {min_data + k_final * amplitud_final:.2f}$.")
    
    # ----------------------------------------------------
    # --- PASO 3-6: Construir la Tabla y Completar ---
    # ----------------------------------------------------
    st.markdown("### 📐 Paso 3: Construir los Intervalos")
    st.markdown(f"""
    Ahora vamos a **construir los k={k_final} intervalos** que dividirán nuestros datos:

    **¿Cómo se hace?**

    1. **Comenzamos con el valor mínimo:** ${min_data:.2f}$

    2. **Le sumamos la amplitud** para obtener el siguiente límite: ${min_data:.2f} + {amplitud_final:.2f} = {min_data + amplitud_final:.2f}$

    3. **Perfecto! ya tenemos nuestro primer intervalo. Repetimos este proceso** hasta completar los $k={k_final}$ intervalos

    **⚠️ Importante sobre los límites:**
    - El **Límite Inferior (Lᵢ)** es **CERRADO** → incluye el valor exacto
    - El **Límite Superior (Ls)** es **ABIERTO** → NO incluye el valor exacto
    - Notación: **[Lᵢ, Ls)** significa "desde Lᵢ (incluido) hasta Ls (no incluido)"

    **Ejemplo:** Si tenemos el intervalo [1.50, 1.55), esto significa que:
    - ✅ 1.50 (sí está incluido)
    - ✅ 1.52 (sí está incluido)
    - ✅ 1.5499... (sí está incluido)
    - ❌ 1.55 (NO está incluido, pertenece al siguiente intervalo)
    """)

    st.markdown("---")

    st.markdown("### 🎯 Paso 4: Calcular la Marca de Clase ($x_i$)")
    st.markdown(f"""
    La **Marca de Clase** es el **punto medio** de cada intervalo. Representa el valor "típico" o "representativo" de todos los datos que caen dentro de ese intervalo.

    **¿Para qué sirve?**
    - Es el valor que usamos para **representar** a todos los datos del intervalo en cálculos posteriores
    - Nos ayuda a estimar la **media**, **mediana** y otros estadísticos cuando trabajamos con datos agrupados

    **¿Cómo se calcula?**

    $$ x_i = \\frac{{L_i + L_s}}{{2}} $$

    Es decir, **sumamos el Límite Inferior con el Límite Superior y dividimos entre 2**.

    **Ejemplo:** Para el intervalo [1.50, 1.55):

    $$ x_i = \\frac{{1.50 + 1.55}}{{2}} = \\frac{{3.05}}{{2}} = 1.525 $$
    """)

    st.markdown("---")

    st.markdown("### 📊 Paso 5: Contar Frecuencias")
    st.markdown("""
    Ahora viene la parte más importante: **¿Cuántos datos caen dentro de cada intervalo?**

    **El proceso:**
    1. Para cada intervalo **[Lᵢ, Ls)**, revisamos todos los datos de nuestra muestra
    2. **Contamos** cuántos valores entran dentro de nuestro intervalo
    3. Ese conteo es la **Frecuencia Absoluta ($f_i$)** del intervalo

    **Ejemplo:** 
    - Si el intervalo es [1.60, 1.65) y tenemos los datos: 1.61, 1.62, 1.63, 1.65, 1.67
    - Contamos: 1.61 ✅, 1.62 ✅, 1.63 ✅, 1.65 ❌ (no incluido), 1.67 ❌
    - Resultado: $f_i = 3$ datos en este intervalo
    """)

    st.markdown("---")

    st.markdown("### 📋 Paso 6: Completar la Tabla con Todas las Frecuencias")
    st.markdown("""
    Finalmente, calculamos las **frecuencias derivadas** que nos ayudan a interpretar mejor los datos:

    **Frecuencias que calcularemos:**

    #### 1. **Frecuencia Relativa ($f_r$):** 
    - Es la **fracción** o **pedacito** que representa cada intervalo del total
    - **¿Cómo se calcula?** Dividimos la frecuencia del intervalo entre el total de datos
    - **Ejemplo sencillo:** 
        - Tengo 150 estudiantes en total
        - 30 estudiantes están en el intervalo [1.60, 1.65)
        - Entonces: $30 ÷ 150 = 0.20$
        - **Significado:** Este intervalo tiene 0.20 (o sea, 1/5) del total de datos

    #### 2. **Porcentaje (%):**
    - Es lo mismo que la frecuencia relativa, pero **en porcentaje** (más fácil de entender)
    - **¿Cómo se calcula?** Multiplicamos la frecuencia relativa por 100
    - **Ejemplo sencillo:**
        - Si $f_r = 0.20$
        - Entonces: $0.20 × 100 = 20\\%$
        - **Significado:** El 20% de los estudiantes están en este intervalo

    #### 3. **Frecuencia Acumulada ($F_i$):**
    - Es **ir sumando** las frecuencias de todos los intervalos anteriores
    - **¿Cómo se calcula?** Sumamos la frecuencia del intervalo actual + todas las anteriores
    - **Ejemplo paso a paso:**
        - Intervalo 1: tiene 25 datos → $F_1 = f_1 = 25$
        - Intervalo 2: tiene 30 datos → $F_2 = F_1 + f_2 = 25 + 30 = 55$ (Es decir, a los 25 que tengo en el intervalo 1 le sumo los que tengo en el intervalo 2)
        - Intervalo 3: tiene 40 datos → $F_3 = F_2 + f_3= 55 + 40 = 95$ (Es decir, a los acumulados **hasta el intervalo 2** (55) le sumo los que tengo en el intervalo 2)
        - **Significado:** Hasta el 3er intervalo, ya llevamos 95 datos contados

    #### 4. **Frecuencia Relativa Acumulada ($F_r$):**
    - Es la frecuencia acumulada pero **expresada como fracción** del total
    - **¿Cómo se calcula?** Dividimos la frecuencia acumulada entre el total de datos
    - **Ejemplo sencillo:**
        - Si $F_3 = 95$ (datos acumulados hasta el tercer intervalo)
        - Y tenemos $N = 150$ datos en total
        - Entonces: $95 ÷ 150 = 0.6333$
        - **Significado:** Hasta el tercer intervalo ya hemos contado el 63.33% de todos los datos
    """)

    st.success("✅ ¡Ahora sí! Con todo esto claro, construyamos la tabla completa:")

    # Generar la tabla con la k y amplitud elegidas
    tabla_raw, tabla_display, A_calc, k_calc = generar_tabla_agrupada(data_constructor, k=k_final, amplitud=amplitud_final)

    st.markdown(f"**Tabla generada con {k_calc} Intervalos y Amplitud $A \\approx {A_calc:.4f}$:**")

    col_t, col_e = st.columns([2, 1])
    with col_t:
        st.dataframe(tabla_display, use_container_width=True, height=500)
    with col_e:
        st.markdown("**Recordatorio de Fórmulas:**")
        st.info("""
        **Marca de Clase:**
        $$ x_i = \\frac{L_i + L_s}{2} $$
        
        **Frecuencias:**
        - $f_r = f_i / N$
        - $\\% = f_r \\times 100$
        - $F_i = \\sum f_i$ 
        - $F_r = F_i / N$
        """)
    
    # ----------------------------------------------------
    # --- HISTOGRAMA FINAL ---
    # ----------------------------------------------------
    st.subheader("📊 Visualización Final: Histograma")
    st.markdown("Así se ve la distribución de tus datos con la tabla construida:")
    
 
    limites_inf = tabla_raw['Límite Inferior'].tolist()
    limites_sup = tabla_raw['Límite Superior'].tolist()
    frecuencias = tabla_raw['Frecuencia Absoluta'].tolist()

    # Crear listas para el gráfico de barras
    x_centers = tabla_raw['Marca de Clase ($x_i$)'].tolist()
    widths = [sup - inf for inf, sup in zip(limites_inf, limites_sup)]

    # Crear el gráfico usando barras en lugar de histograma
    fig_final = go.Figure()

    # Agregar barras con el ancho correcto de cada intervalo
    fig_final.add_trace(go.Bar(
        x=x_centers,
        y=frecuencias,
        width=widths,
        marker=dict(
            color='steelblue',
            line=dict(color='black', width=1.5)
        ),
        opacity=0.7,
        name='Frecuencia',
        hovertemplate='Intervalo: [%{customdata[0]:.2f}, %{customdata[1]:.2f})<br>Frecuencia: %{y}<extra></extra>',
        customdata=[[inf, sup] for inf, sup in zip(limites_inf, limites_sup)]
    ))

    # Agregar líneas verticales en cada límite de clase
    todos_limites = [limites_inf[0]] + limites_sup
    for limite in todos_limites:
        fig_final.add_vline(
            x=limite, 
            line_dash="dash", 
            line_color="red", 
            opacity=0.5,
            line_width=1.5
        )

    # Configurar el layout
    fig_final.update_layout(
        title=dict(
            text=f'Histograma de Frecuencias | N={len(data_constructor)} | k={k_calc} intervalos | A≈{A_calc:.4f}',
            font=dict(size=16, family='Arial Black')
        ),
        xaxis=dict(
            title='Valores',
            title_font=dict(size=14, family='Arial Black'),
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title='Frecuencia Absoluta (fᵢ)',
            title_font=dict(size=14, family='Arial Black'),
            gridcolor='lightgray'
        ),
        plot_bgcolor='white',
        showlegend=False,
        hovermode='closest',
        height=600,
        bargap=0  # Sin espacio entre barras
    )

    st.plotly_chart(fig_final, use_container_width=True)

    st.success("✅ ¡Tabla de frecuencias agrupada construida exitosamente!")

elif page == "2. Comparación: ¿Agrupar o No?":
    st.title("💯 Comparación: ¿Debo Agrupar?")
    st.markdown("Pon a prueba tu conocimiento sobre cuándo es estadísticamente necesario agrupar datos.")
    
    comparacion_datasets = [
        ("Color Favorito (Nominal Bajo)", datasets["Color Favorito (Nominal Bajo)"], "No", "Nominal con 4 categorías. Siempre se usa tabla no agrupada."),
        ("Número de Hermanos (Discreto Bajo)", datasets["Número de Hermanos (Discreto Bajo)"], "No", "Discreta con 5 valores únicos (0-4). Se usa tabla no agrupada."),
        ("Calificaciones de Examen (Discreto Alto)", datasets["Calificaciones de Examen (Discreto Alto)"], "Sí", "Discreta con muchos valores únicos (30-100). La repetición es baja, es mejor agrupar para ver la distribución."),
        ("Estaturas de Estudiantes (Continuo)", datasets["Estaturas de Estudiantes (Continuo)"], "Sí", "Variable Continua. Es obligatorio agrupar."),
        ("Edades de Empleados (Discreto Alto)", datasets["Edades de Empleados (Discreto Alto)"], "Sí", "Discreta con más de 45 valores únicos. La tabla no agrupada sería muy larga."),
    ]
    
    for i, (name, data, answer, reason) in enumerate(comparacion_datasets):
        st.markdown(f"---")
        st.subheader(f"Dataset {i+1}: {name}")
        st.markdown(f"**Tamaño ($N$):** {len(data)}")
        st.markdown(f"**Valores Únicos:** {len(data.unique())}")
        st.code(f"Muestra: {data.head(10).tolist()}...")
        
        col_q, col_r = st.columns(2)
        with col_q:
            choice = st.radio("¿Se debe agrupar?", ["Sí", "No"], key=f"q_agrupar_{i}")
        
        with col_r:
            if st.button("Ver Solución", key=f"btn_sol_{i}"):
                if choice == answer:
                    st.success(f"✅ ¡Correcto! La respuesta es **{answer}**.")
                else:
                    st.error(f"❌ Incorrecto. La respuesta correcta es **{answer}**.")
                st.info(f"**Razón:** {reason}")

elif page == "5. Explorador de Datos Agrupados":
    st.title("📊 Explorador de Datos Agrupados")
    st.markdown("Visualiza cómo la elección del número de intervalos afecta la tabla de frecuencia y el histograma.")

    selected_data_key = st.selectbox("Selecciona un Dataset Agrupable:", dataset_keys[:4], index=0)
    data_explore = datasets[selected_data_key]
    n_explore = len(data_explore)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Control de Intervalos")

    k_suggested = sturges_rule(n_explore)
    k_explore = st.sidebar.slider("Número de Intervalos ($k$):", min_value=2, max_value=15, value=k_suggested, step=1)
    
    st.sidebar.info(f"Regla de Sturges sugiere: $k \\approx {k_suggested}$")

    # Generar tabla con k seleccionado
    tabla_raw_exp, tabla_display_exp, A_calc_exp, k_calc_exp = generar_tabla_agrupada(data_explore, k=k_explore)
    
    st.markdown(f"**Dataset:** {selected_data_key} ($N={n_explore}$)")
    st.markdown(f"**Intervalos Usados ($k$):** {k_calc_exp} | **Amplitud ($A$):** {A_calc_exp:.4f}")

    col_t, col_g = st.columns(2)
    
    with col_t:
        st.subheader("Tabla de Frecuencia Agrupada")
        st.dataframe(tabla_display_exp, use_container_width=True, hide_index=True)
    
    with col_g:
        st.subheader("Histograma de Frecuencia")
        
        # Extraer datos DIRECTAMENTE de la tabla para que coincidan
        limites_inf = tabla_raw_exp['Límite Inferior'].tolist()
        limites_sup = tabla_raw_exp['Límite Superior'].tolist()
        frecuencias = tabla_raw_exp['Frecuencia Absoluta'].tolist()
        x_centers = tabla_raw_exp['Marca de Clase ($x_i$)'].tolist()
        widths = [sup - inf for inf, sup in zip(limites_inf, limites_sup)]
        
        # Crear el gráfico usando barras con los datos de la tabla
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=x_centers,
            y=frecuencias,
            width=widths,
            marker=dict(
                color='steelblue',
                line=dict(color='black', width=1)
            ),
            opacity=0.7,
            hovertemplate='[%{customdata[0]:.2f}, %{customdata[1]:.2f})<br>Frecuencia: %{y}<extra></extra>',
            customdata=[[inf, sup] for inf, sup in zip(limites_inf, limites_sup)]
        ))
        
        # Agregar líneas verticales en cada límite
        todos_limites = [limites_inf[0]] + limites_sup
        for limite in todos_limites:
            fig.add_vline(x=limite, line_dash="dash", line_color="red", opacity=0.4, line_width=1)
        
        fig.update_layout(
            title=f"Histograma ({k_calc_exp} Clases, A={A_calc_exp:.4f})",
            xaxis_title="Valores",
            yaxis_title="Frecuencia Absoluta",
            showlegend=False,
            bargap=0,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)


elif page == "6. Comparador de Gráficos":
    st.title("🔄 Comparador de Gráficos para Datos Agrupados")
    st.markdown("Comprende qué gráficos son apropiados y por qué no deben usarse los gráficos de datos no agrupados.")
    
    data_grafico = datasets["Estaturas de Estudiantes (Continuo)"]
    k_grafico = sturges_rule(len(data_grafico))
    
    tabla_raw_g, tabla_display_g, A_calc_g, k_calc_g = generar_tabla_agrupada(data_grafico, k=k_grafico)
    
    st.markdown(f"**Dataset de Ejemplo:** Estaturas de Estudiantes ($N={len(data_grafico)}$) agrupado en $k={k_calc_g}$ clases.")
    st.markdown("---")
    
    col_h, col_b, col_p, col_o = st.columns(4)

    # --- HISTOGRAMA (CORRECTO) ---
    with col_h:
        st.subheader("1. Histograma $(f_i)$ ✅")
        
        # Generar bins para Plotly
        data_min = data_grafico.min()
        amplitud = A_calc_g
        bins_plotly = np.arange(data_min, data_grafico.max() + amplitud, amplitud)
        
        fig = px.histogram(data_grafico, x=data_grafico.name, 
                           nbins=k_grafico, histfunc='count')
        fig.update_traces(marker_line_width=0, marker_color='#4682B4')
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("✅ **APLICABLE:** Gráfico **obligatorio** para datos continuos agrupados. Las barras representan la frecuencia ($f_i$) y el **área** representa la cantidad de datos.")
        st.info("💡 **Clave:** Las barras **NO** tienen espacios, indicando la continuidad de la variable.")
    
    # --- GRÁFICO DE BARRAS (INCORRECTO) ---
    with col_b:
        st.subheader("2. Barras (Clases) ❌")
        # Gráfico de barras usando las clases como categorías
        fig = px.bar(tabla_raw_g, x='Clase/Intervalo', y='Frecuencia Absoluta')
        fig.update_traces(marker_color='#FF5733')
        st.plotly_chart(fig, use_container_width=True)
        
        st.error("❌ **NO APLICABLE:** Inadecuado. Muestra **espacios** entre las clases, lo cual es incorrecto para una variable continua. Viola el principio de continuidad.")
        st.info("⚠️ **Error Común:** El gráfico de barras se usa para variables discretas o nominales/ordinales, no para la visualización de datos agrupados.")

    # --- POLÍGONO DE FRECUENCIAS (CORRECTO) ---
    with col_p:
        st.subheader("3. Polígono $(f_i)$ ✅")
        # El polígono usa la Marca de Clase (xi)
        fig = px.line(tabla_raw_g, x='Marca de Clase ($x_i$)', y='Frecuencia Absoluta', markers=True)
        fig.update_traces(line=dict(color='#008000'))
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("✅ **APLICABLE:** Gráfico que une los **puntos medios** (Marca de Clase) de la parte superior de cada barra del Histograma. Muestra la forma de la distribución.")
        st.info("💡 **Clave:** Es la representación de la distribución de frecuencias usando la Marca de Clase ($x_i$).")

    # --- OJIVA (CORRECTO) ---
    with col_o:
        st.subheader("4. Ojiva $(F_r)$ ✅")
        # La ojiva usa la Frecuencia Acumulada (F_r)
        fig = px.line(tabla_raw_g, x='Límite Superior', y='Frecuencia Relativa Acumulada', markers=True)
        fig.update_traces(line=dict(color='#8A2BE2'))
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("✅ **APLICABLE:** Muestra la **Frecuencia Acumulada**. Es esencial para calcular **percentiles** o cuartiles de manera gráfica.")
        st.info("💡 **Clave:** Siempre va ascendiendo, mostrando la proporción de datos **menores o iguales** al límite superior de cada clase.")


elif page == "7. Casos Reales - Análisis Guiado":
    st.title("📈 Casos Reales: Análisis Guiado de Tablas Agrupadas")
    st.markdown("Aplica la interpretación de las frecuencias, marcas de clase y límites a preguntas prácticas.")
    
    selected_data_key = st.selectbox("Selecciona un Dataset para Analizar:", dataset_keys[:4], index=0, key="analisis_data_sel")
    data_analisis = datasets[selected_data_key]
    n_analisis = len(data_analisis)
    
    # Usar Sturges para k
    k_analisis = sturges_rule(n_analisis)
    tabla_raw_an, tabla_display_an, A_calc_an, k_calc_an = generar_tabla_agrupada(data_analisis, k=k_analisis)
    
    st.subheader(f"Dataset: {selected_data_key} (k={k_calc_an})")
    
    with st.expander("Ver Tabla de Frecuencia Completa"):
        st.dataframe(tabla_display_an, hide_index=True, use_container_width=True)

    # --- FUNCIÓN AUXILIAR PARA CREAR HISTOGRAMA ---
    def crear_histograma_resaltado(tabla_raw, data, intervalos_resaltados=None, titulo="Histograma", mostrar_valores=None):
        """
        Crea un histograma con intervalos específicos resaltados
        intervalos_resaltados: lista de índices de intervalos a resaltar (base 0)
        mostrar_valores: dict con índices y valores a mostrar, ej: {0: "fᵢ=25", 1: "xᵢ=1.65"}
        """
        import plotly.graph_objects as go
        
        limites_inf = tabla_raw['Límite Inferior'].tolist()
        limites_sup = tabla_raw['Límite Superior'].tolist()
        frecuencias = tabla_raw['Frecuencia Absoluta'].tolist()
        x_centers = tabla_raw['Marca de Clase ($x_i$)'].tolist()
        widths = [sup - inf for inf, sup in zip(limites_inf, limites_sup)]
        
        # Crear colores: resaltar intervalos específicos
        colors = []
        for i in range(len(frecuencias)):
            if intervalos_resaltados and i in intervalos_resaltados:
                colors.append('orange')  # Color de resaltado
            else:
                colors.append('steelblue')  # Color normal
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=x_centers,
            y=frecuencias,
            width=widths,
            marker=dict(
                color=colors,
                line=dict(color='black', width=1.5)
            ),
            opacity=0.7,
            hovertemplate='[%{customdata[0]:.2f}, %{customdata[1]:.2f})<br>Frecuencia: %{y}<extra></extra>',
            customdata=[[inf, sup] for inf, sup in zip(limites_inf, limites_sup)]
        ))
        
        # Agregar anotaciones de texto sobre las barras resaltadas
        if mostrar_valores:
            for idx, texto in mostrar_valores.items():
                fig.add_annotation(
                    x=x_centers[idx],
                    y=frecuencias[idx],
                    text=f"<b>{texto}</b>",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor="orange",
                    ax=0,
                    ay=-40,
                    font=dict(size=14, color="black"),
                    bgcolor="yellow",
                    opacity=0.8,
                    bordercolor="orange",
                    borderwidth=2
                )
        
        # Líneas verticales
        todos_limites = [limites_inf[0]] + limites_sup
        for limite in todos_limites:
            fig.add_vline(x=limite, line_dash="dash", line_color="red", opacity=0.4, line_width=1)
        
        fig.update_layout(
            title=titulo,
            xaxis_title="Valores",
            yaxis_title="Frecuencia Absoluta",
            showlegend=False,
            bargap=0,
            height=400
        )
        
        return fig

    st.markdown("---")
    
    # --- PREGUNTAS CLAVE ---

    st.markdown("### Preguntas de Interpretación")
    
    # P1: Intervalo con Mayor Frecuencia (Moda)
    st.markdown("**P1:** ¿En qué **intervalo** (Clase Modal) se encuentra la mayor concentración de datos?")
    if st.button("Mostrar P1", key="p1_an"):
        fa_max = tabla_raw_an['Frecuencia Absoluta'].max()
        # Encontrar TODOS los intervalos con la frecuencia máxima
        indices_modales = tabla_raw_an[tabla_raw_an['Frecuencia Absoluta'] == fa_max].index.tolist()
        clases_modales = tabla_raw_an[tabla_raw_an['Frecuencia Absoluta'] == fa_max]['Clase/Intervalo'].tolist()
        
        if len(clases_modales) == 1:
            st.success(f"Respuesta: El intervalo con mayor frecuencia es **{clases_modales[0]}** (con $f_i = {fa_max}$).")
            st.info("Procedimiento: Lectura directa de la columna $f_i$. El intervalo con el valor más alto es la Clase Modal.")
        else:
            clases_str = ", ".join([f"**{clase}**" for clase in clases_modales])
            st.success(f"Respuesta: Hay **{len(clases_modales)} clases modales** con la misma frecuencia máxima: {clases_str} (con $f_i = {fa_max}$).")
            st.info("Procedimiento: Se identificaron múltiples intervalos con la frecuencia máxima. Esta es una distribución **multimodal**.")
        
        # Crear diccionario con valores a mostrar
        valores_p1 = {idx: f"fᵢ = {int(fa_max)}" for idx in indices_modales}
        
        # Histograma con clase(s) modal(es) resaltada(s)
        fig_p1 = crear_histograma_resaltado(tabla_raw_an, data_analisis, 
                                            intervalos_resaltados=indices_modales,
                                            mostrar_valores=valores_p1,
                                            titulo="Clase Modal Resaltada (Naranja)")
        st.plotly_chart(fig_p1, use_container_width=True)
        
    # P2: Marca de Clase del Intervalo Modal
    st.markdown("**P2:** ¿Cuál es la **Marca de Clase ($x_i$)** de ese intervalo modal? (En caso de haber más de uno tome cualquiera)")
    if st.button("Mostrar P2", key="p2_an"):
        idx_moda = tabla_raw_an['Frecuencia Absoluta'].argmax()
        moda_intervalo = tabla_raw_an.iloc[idx_moda]['Clase/Intervalo']
        xi_moda = tabla_raw_an.iloc[idx_moda]['Marca de Clase ($x_i$)']
        st.success(f"Respuesta: La Marca de Clase ($x_i$) para **{moda_intervalo}** es **{xi_moda:.4f}**.")
        st.info("Procedimiento: Se calcula el punto medio: $\\mathbf{{x_i = \\frac{{L_i + L_s}}{{2}}}}$.")
        
        # Mostrar marca de clase sobre la barra
        valores_p2 = {idx_moda: f"x̄ᵢ = {xi_moda:.4f}"}
        
        # Histograma con intervalo modal resaltado
        fig_p2 = crear_histograma_resaltado(tabla_raw_an, data_analisis, 
                                            intervalos_resaltados=[idx_moda],
                                            mostrar_valores=valores_p2,
                                            titulo=f"Intervalo Modal con Marca de Clase")
        st.plotly_chart(fig_p2, use_container_width=True)
        
    # P3: Porcentaje acumulado
    st.markdown("**P3:** ¿Qué **porcentaje** de la muestra se encuentra **por debajo del Límite Superior del 3er Intervalo**?")
    if st.button("Mostrar P3", key="p3_an"):
        if k_calc_an >= 3:
            limite_superior_3 = tabla_raw_an.iloc[2]['Límite Superior']
            fr_acum_3 = tabla_raw_an.iloc[2]['Frecuencia Relativa Acumulada']
            porc_acum_3 = fr_acum_3 * 100
            st.success(f"Respuesta: **{porc_acum_3:.2f}%**")
            st.info(f"Procedimiento: Lectura directa de la columna **Frecuencia Relativa Acumulada ($F_r$)**. Se busca la fila del 3er intervalo (índice 2): $\\mathbf{{F_r(3) \\times 100}} = {fr_acum_3:.4f} \\times 100 = {porc_acum_3:.2f}\\%$.")
            
            # Mostrar porcentaje acumulado
            valores_p3 = {2: f"{porc_acum_3:.2f}%"}
            
            # Histograma resaltando los primeros 3 intervalos
            fig_p3 = crear_histograma_resaltado(tabla_raw_an, data_analisis, 
                                                intervalos_resaltados=[0, 1, 2],
                                                mostrar_valores=valores_p3,
                                                titulo=f"Primeros 3 intervalos ({porc_acum_3:.2f}% de los datos)")
            st.plotly_chart(fig_p3, use_container_width=True)
        else:
            st.warning("Este dataset tiene menos de 3 intervalos. Ajusta el número de intervalos en el 'Explorador'.")
             
    # P4: Frecuencia Absoluta de Rango
    st.markdown("**P4:** ¿Cuántos datos se encuentran en los **primeros dos intervalos**?")
    if st.button("Mostrar P4", key="p4_an"):
        if k_calc_an >= 2:
            fa_acum_2 = tabla_raw_an.iloc[1]['Frecuencia Acumulada']
            st.success(f"Respuesta: **{int(fa_acum_2)}** datos.")
            st.info("Procedimiento: Lectura directa de la $\\mathbf{{F_i}}$ (Frecuencia Acumulada) del segundo intervalo.")
            
            # Mostrar frecuencia acumulada
            valores_p4 = {1: f"Fᵢ = {int(fa_acum_2)}"}
            
            # Histograma resaltando los primeros 2 intervalos
            fig_p4 = crear_histograma_resaltado(tabla_raw_an, data_analisis, 
                                                intervalos_resaltados=[0, 1],
                                                mostrar_valores=valores_p4,
                                                titulo=f"Primeros 2 intervalos ({int(fa_acum_2)} datos)")
            st.plotly_chart(fig_p4, use_container_width=True)
        else:
            st.warning("Este dataset tiene menos de 2 intervalos.")
             
    # P5: Proporción de Rango Superior
    st.markdown("**P5:** ¿Cuál es la **proporción ($f_r$ Acumulada Inversa)** de datos que están **por encima** del Límite Superior del 4to Intervalo?")
    if st.button("Mostrar P5", key="p5_an"):
        if k_calc_an >= 5:
            fr_acum_4 = tabla_raw_an.iloc[3]['Frecuencia Relativa Acumulada']
            proporcion_sup = 1.0 - fr_acum_4
            st.success(f"Respuesta: **{proporcion_sup:.4f}**")
            st.info(f"Procedimiento: Se usa la $F_r$ Acumulada Inversa: $\\mathbf{{1 - F_r(\\text{{4to Intervalo}})}} = 1 - {fr_acum_4:.4f} = {proporcion_sup:.4f}$.")
            
            # Mostrar proporción sobre el primer intervalo superior
            valores_p5 = {4: f"Fr = {proporcion_sup:.4f}"} if k_calc_an > 4 else {}
            
            # Histograma resaltando intervalos superiores al 4to
            intervalos_superiores = list(range(4, k_calc_an))
            fig_p5 = crear_histograma_resaltado(tabla_raw_an, data_analisis, 
                                                intervalos_resaltados=intervalos_superiores,
                                                mostrar_valores=valores_p5,
                                                titulo=f"Datos por encima del 4to intervalo ({proporcion_sup:.4f})")
            st.plotly_chart(fig_p5, use_container_width=True)
        else:
            st.warning("Este dataset tiene menos de 5 intervalos. No se puede calcular el valor superior al 4to intervalo.")


elif page == "8. Cuestionario Final":
    st.title("❓ Cuestionario Final: Evaluación de Conceptos")
    st.markdown("Evalúa tu comprensión sobre la agrupación de datos, sus conceptos y gráficos.")
    
    questions = [
        # Conceptuales
        {"q": "¿Cuál es el valor que representa un intervalo o clase en los cálculos de medidas de tendencia central?",
         "opts": ["Límite Superior ($L_s$)", "Amplitud ($A$)", "Marca de Clase ($x_i$)", "Frecuencia Absoluta ($f_i$)"],
         "resp": "Marca de Clase ($x_i$)",
         "retro": "La **Marca de Clase ($x_i$)** es el punto medio del intervalo y se usa como el valor representativo de toda la clase."},
         
        {"q": "¿Cuál es la principal razón por la que un Histograma NO debe tener espacios entre sus barras?",
         "opts": ["Para ahorrar espacio en el gráfico.", "Para indicar la continuidad de la variable.", "Porque los datos son nominales.", "Solo los gráficos de pastel tienen espacios."],
         "resp": "Para indicar la continuidad de la variable.",
         "retro": "El espacio entre barras en un gráfico indica discontinuidad. El histograma, al ser para datos continuos, debe mostrar la conexión entre clases."},
         
        {"q": "Según la Regla de Sturges, si $N=100$ datos, ¿cuántos intervalos ($k$) se sugieren?",
         "opts": ["5", "7", "10", "12"],
         "resp": "7",
         "retro": f"Para $N=100$, $k = 1 + 3.322 \\times \\log_{{10}}(100) = 1 + 3.322 \\times 2 \\approx 7.644$. Se redondea a **7** u **8**."},
         
        # Cálculo / Interpretación
        {"q": "Si un intervalo es $[50 - 60)$ y su $f_i$ es 12, ¿cuál es su Marca de Clase ($x_i$)?",
         "opts": ["10", "50", "60", "55"],
         "resp": "55",
         "retro": "La Marca de Clase se calcula como $\\mathbf{{\\frac{{L_i + L_s}}{{2}}}}: \\frac{{50 + 60}}{{2}} = 55$."},
         
        {"q": "En una Ojiva, el último punto siempre se encuentra en una Frecuencia Relativa Acumulada ($F_r$) de:",
         "opts": ["El valor de $N$", "50%", "1.0 o 100%", "La Amplitud"],
         "resp": "1.0 o 100%",
         "retro": "La Ojiva es un gráfico acumulado. El último punto debe sumar el **100%** o **1.0** de los datos."},
         
        {"q": "Un dato con valor $20$ cae en el intervalo:",
         "opts": ["[10 - 20)", "[20 - 30)", "(15 - 20)", "Solo en ninguno de los anteriores"],
         "resp": "[20 - 30)",
         "retro": "Por convención $(L_i, L_s]$, el dato $20$ no se incluye en $[10 - 20)$, pero sí en el siguiente intervalo $[20 - 30)$, ya que el límite inferior es inclusivo (corchete)."},

        # Decisión
        {"q": "¿Qué se **pierde** al agrupar un conjunto de datos en intervalos?",
         "opts": ["La Amplitud de Clase.", "La posibilidad de calcular la Marca de Clase.", "La exactitud de los valores individuales.", "La frecuencia absoluta."],
         "resp": "La exactitud de los valores individuales.",
         "retro": "La principal desventaja es la **pérdida de la exactitud**; ahora solo sabemos que el dato cayó en ese rango, no su valor exacto."},
         
        {"q": "¿Cuál es la fórmula correcta para calcular la Amplitud ($A$) de clase?",
         "opts": ["$L_i + L_s$", "$L_s - L_i$", "$N / k$", "Máximo / Mínimo"],
         "resp": "$L_s - L_i$",
         "retro": "La Amplitud se calcula como la diferencia entre el $\\mathbf{{L\\acute{i}mite\\ Superior\\ (L_s)}}$ y el $\\mathbf{{L\\acute{i}mite\\ Inferior\\ (L_i)}}$ de la clase."},
         
        {"q": "Si la $F_i$ (Frecuencia Acumulada) del intervalo [30-40) es 50 y la $F_i$ del intervalo [20-30) es 30, ¿cuál es la $f_i$ del intervalo [30-40)?",
         "opts": ["80", "20", "50", "30"],
         "resp": "20",
         "retro": "La Frecuencia Absoluta ($f_i$) de una clase se encuentra restando la $F_i$ de la clase anterior: $\\mathbf{{f_i = F_i - F_{{i-1}}}}$. En este caso, $F_i(\\text{{[30-40)}}) - F_i(\\text{{[20-30)}}) = 50 - 30 = 20$."},
         
        {"q": "¿Cuál de estos datasets **NO** necesita ser agrupado?",
         "opts": ["Tiempos de entrega (Continuo)", "Salario de 500 empleados", "Calificación de 0 a 5 estrellas", "Edad de jubilación (60 a 70 años)"],
         "resp": "Calificación de 0 a 5 estrellas",
         "retro": "La calificación de 0 a 5 estrellas es una variable ordinal/discreta con muy pocos valores únicos, por lo que es mejor usar una tabla no agrupada."},
    ]
    
    if 'quiz_agrupados_index' not in st.session_state:
        st.session_state.quiz_agrupados_index = 0
        st.session_state.quiz_agrupados_answers = {}
        st.session_state.quiz_agrupados_submitted = False
        
    def next_question():
        if st.session_state.quiz_agrupados_index < len(questions) - 1:
            st.session_state.quiz_agrupados_index += 1
        else:
            st.session_state.quiz_agrupados_submitted = True

    def prev_question():
        if st.session_state.quiz_agrupados_index > 0:
            st.session_state.quiz_agrupados_index -= 1

    if not st.session_state.quiz_agrupados_submitted:
        q_data = questions[st.session_state.quiz_agrupados_index]
        st.subheader(f"Pregunta {st.session_state.quiz_agrupados_index + 1}/{len(questions)}")
        st.markdown(f"**{q_data['q']}**")

        user_answer = st.radio("Selecciona una opción:", q_data['opts'], 
                               key=f"q_{st.session_state.quiz_agrupados_index}", 
                               index=q_data['opts'].index(st.session_state.quiz_agrupados_answers.get(st.session_state.quiz_agrupados_index, q_data['opts'][0])))
        
        st.session_state.quiz_agrupados_answers[st.session_state.quiz_agrupados_index] = user_answer
        
        col_prev, col_next = st.columns([1, 1])
        with col_prev:
            if st.session_state.quiz_agrupados_index > 0:
                st.button("⬅️ Anterior", on_click=prev_question)
        with col_next:
            if st.session_state.quiz_agrupados_index < len(questions) - 1:
                st.button("Siguiente ➡️", on_click=next_question)
            else:
                st.button("Finalizar y Revisar 🏁", on_click=next_question)
    else:
        st.subheader("🏁 Resultados del Cuestionario")
        correct_count = 0
        for i, q_data in enumerate(questions):
            user_answer = st.session_state.quiz_agrupados_answers.get(i)
            is_correct = user_answer == q_data['resp']
            
            if is_correct:
                correct_count += 1
                st.markdown(f"**✅ Pregunta {i+1}:** {q_data['q']}")
            else:
                st.markdown(f"**❌ Pregunta {i+1}:** {q_data['q']}")
            
            st.markdown(f"Tu Respuesta: **{user_answer}**")
            st.markdown(f"Respuesta Correcta: **{q_data['resp']}**")
            st.info(f"Retroalimentación: {q_data['retro']}")
            st.markdown("---")
            
        st.metric("Puntuación Final", f"{correct_count}/{len(questions)}", delta=f"{correct_count / len(questions) * 100:.1f}% de aciertos")
        if st.button("Reiniciar Cuestionario"):
            st.session_state.quiz_agrupados_index = 0
            st.session_state.quiz_agrupados_answers = {}
            st.session_state.quiz_agrupados_submitted = False
            st.rerun()

elif page == "9. Ventajas y Desventajas":
    st.title("🎯 Ventajas y Desventajas de la Agrupación")
    st.markdown("Comprende la compensación clave al agrupar datos: la manejabilidad frente a la pérdida de detalle.")
    
    col_v, col_d = st.columns(2)
    
    with col_v:
        st.subheader("👍 Ventajas de Agrupar")
        st.success("""
        * **Manejo:** Convierte grandes volúmenes de datos continuos o dispersos en tablas compactas y manejables.
        * **Patrones:** Permite visualizar fácilmente la forma y distribución de los datos (simetría, sesgo, moda).
        * **Gráficos:** Hace posible la creación de gráficos esenciales como el Histograma, que de otra manera serían inútiles.
        * **Resumen:** Facilita la interpretación global para la toma de decisiones.
        """)
        
    with col_d:
        st.subheader("👎 Desventajas de Agrupar")
        st.error("""
        * **Pérdida de Información:** Se pierde el valor exacto de cada dato individual.
        * **Interpretación Sesgada:** La elección arbitraria de $k$ (número de intervalos) o $A$ (amplitud) puede alterar visualmente la distribución.
        """)
        
    st.markdown("---")
    st.subheader("Mismo Dataset: Agrupado vs No Agrupado")
    
    # Usamos el dataset de calificaciones (Discreto Alto)
    data_no_agrupado = datasets["Calificaciones de Examen (Discreto Alto)"]
    st.markdown(f"Dataset: Calificaciones de Examen ($N={len(data_no_agrupado)}$)")
    
    col_na, col_a = st.columns(2)
    
    with col_na:
        st.markdown("**Tabla NO Agrupada (Inútil para este caso):**")
        tabla_no_agrup = data_no_agrupado.value_counts().reset_index()
        tabla_no_agrup.columns = ['Calificación', 'Frecuencia Absoluta']
        tabla_no_agrup_sorted = tabla_no_agrup.sort_values('Calificación')
        st.dataframe(tabla_no_agrup_sorted, hide_index=True, height=300)
        st.warning(f"La tabla tiene {len(tabla_no_agrup)} filas. Es demasiado dispersa.")
        
    with col_a:
        st.markdown("**Tabla Agrupada (Manejable):**")
        k_final = sturges_rule(len(data_no_agrupado))
        tabla_raw_a, tabla_display_a, A_calc_a, k_calc_a = generar_tabla_agrupada(data_no_agrupado, k=k_final)
        st.dataframe(tabla_display_a.drop(columns=['Límite Inferior', 'Límite Superior', 'Marca de Clase ($x_i$)']).head(10), hide_index=True, height=300)
        st.success(f"La tabla tiene **{k_calc_a}** filas. Es mucho más fácil ver dónde se concentran las calificaciones.")
    
    st.markdown("---")
    st.subheader("Comparación Visual")
    
    col_graf_na, col_graf_a = st.columns(2)
    
    with col_graf_na:
        st.markdown("**Gráfico de Barras (Datos NO Agrupados)**")
        
       
        fig_barras = go.Figure()
        
        fig_barras.add_trace(go.Bar(
            x=tabla_no_agrup_sorted['Calificación'],
            y=tabla_no_agrup_sorted['Frecuencia Absoluta'],
            marker=dict(
                color='lightcoral',
                line=dict(color='darkred', width=1)
            ),
            opacity=0.8
        ))
        
        fig_barras.update_layout(
            title="Datos Individuales (Disperso)",
            xaxis_title="Calificación",
            yaxis_title="Frecuencia Absoluta",
            showlegend=False,
            height=400,
            xaxis=dict(tickmode='linear', tick0=tabla_no_agrup_sorted['Calificación'].min(), dtick=5)
        )
        
        st.plotly_chart(fig_barras, use_container_width=True)
        st.info("⚠️ Demasiadas barras individuales dificultan ver el patrón general.")
        
    with col_graf_a:
        st.markdown("**Histograma (Datos Agrupados)**")
        
        # Crear histograma usando los datos de la tabla agrupada
        limites_inf = tabla_raw_a['Límite Inferior'].tolist()
        limites_sup = tabla_raw_a['Límite Superior'].tolist()
        frecuencias = tabla_raw_a['Frecuencia Absoluta'].tolist()
        x_centers = tabla_raw_a['Marca de Clase ($x_i$)'].tolist()
        widths = [sup - inf for inf, sup in zip(limites_inf, limites_sup)]
        
        fig_hist = go.Figure()
        
        fig_hist.add_trace(go.Bar(
            x=x_centers,
            y=frecuencias,
            width=widths,
            marker=dict(
                color='steelblue',
                line=dict(color='black', width=1.5)
            ),
            opacity=0.7
        ))
        
        # Líneas verticales en los límites
        todos_limites = [limites_inf[0]] + limites_sup
        for limite in todos_limites:
            fig_hist.add_vline(x=limite, line_dash="dash", line_color="red", opacity=0.4, line_width=1)
        
        fig_hist.update_layout(
            title=f"Datos Agrupados (k={k_calc_a}, A≈{A_calc_a:.2f})",
            xaxis_title="Calificación",
            yaxis_title="Frecuencia Absoluta",
            showlegend=False,
            bargap=0,
            height=400
        )
        
        st.plotly_chart(fig_hist, use_container_width=True)
        st.success("✅ El histograma revela claramente la distribución y concentración de datos.")

# === FOOTER ===
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
📧 <strong>Contacto:</strong> carlosdl@uninorte.edu.co<br>
Desarrollado con 💙 para estudiantes de Uninorte 
</div>
""", unsafe_allow_html=True)

