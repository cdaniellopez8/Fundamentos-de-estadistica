import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import random

# === CONFIGURACIÓN ===
st.set_page_config(page_title="Medidas Descriptivas", page_icon="📊", layout="wide")

# === FUNCIONES AUXILIARES ===
def calcular_medidas(data):
    """Calcula todas las medidas descriptivas"""
    if len(data) == 0:
        return None
    return {
        'media': np.mean(data),
        'mediana': np.median(data),
        'moda': stats.mode(data, keepdims=True)[0][0] if len(stats.mode(data, keepdims=True)[0]) > 0 else None,
        'rango': np.max(data) - np.min(data),
        'varianza': np.var(data, ddof=1),
        'desv_std': np.std(data, ddof=1),
        'cv': (np.std(data, ddof=1) / np.mean(data) * 100) if np.mean(data) != 0 else 0,
        'q1': np.percentile(data, 25),
        'q2': np.percentile(data, 50),
        'q3': np.percentile(data, 75),
        'iqr': np.percentile(data, 75) - np.percentile(data, 25),
        'asimetria': stats.skew(data),
        'curtosis': stats.kurtosis(data),
        'minimo': np.min(data),
        'maximo': np.max(data),
        'n': len(data)
    }

def crear_boxplot(data, title="Diagrama de Cajas"):
    """Crea un boxplot con Plotly"""
    fig = go.Figure()
    fig.add_trace(go.Box(y=data, name="Datos", boxmean='sd', marker_color='lightblue'))
    fig.update_layout(
        title=title,
        yaxis_title="Valores",
        height=400,
        showlegend=False
    )
    return fig

def crear_histograma_con_medidas(data, medidas):
    """Crea histograma con líneas de tendencia central"""
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=data,
        name="Frecuencia",
        opacity=0.7,
        marker_color='lightblue',
        nbinsx=20
    ))
    
    fig.add_vline(x=medidas['media'], line_dash="dash", line_color="red", 
                  annotation_text=f"Media: {medidas['media']:.2f}", annotation_position="top left")
    fig.add_vline(x=medidas['mediana'], line_dash="dash", line_color="blue",
                  annotation_text=f"Mediana: {medidas['mediana']:.2f}", annotation_position="top")
    
    fig.update_layout(
        title="Distribución con Medidas de Tendencia Central",
        xaxis_title="Valores",
        yaxis_title="Frecuencia",
        height=400
    )
    return fig

@st.cache_data
def load_datasets():
    """Carga datasets de ejemplo"""
    np.random.seed(42)
    
    datasets = {
        "Notas de Examen (Simétrico)": {
            "data": np.random.normal(75, 10, 100).clip(0, 100),
            "descripcion": "Distribución aproximadamente normal de calificaciones",
            "tipo": "Simétrico"
        },
        "Salarios (Asimétrico Derecha)": {
            "data": np.concatenate([np.random.normal(3000, 500, 90), np.array([15000, 18000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 60000])]),
            "descripcion": "Distribución de salarios con cola larga hacia valores altos",
            "tipo": "Asimétrico Positivo"
        },
        "Tiempos de Respuesta (seg)": {
            "data": np.random.exponential(5, 100),
            "descripcion": "Tiempos de respuesta en segundos",
            "tipo": "Asimétrico Positivo"
        },
        "Estaturas (cm)": {
            "data": np.random.normal(170, 8, 100),
            "descripcion": "Estaturas de personas adultas",
            "tipo": "Simétrico"
        },
        "Edad de Jubilación": {
            "data": np.random.normal(65, 3, 100).clip(55, 75),
            "descripcion": "Edad de jubilación (concentrada)",
            "tipo": "Simétrico"
        }
    }
    return datasets

# === INICIALIZACIÓN ===
if 'ejercicio_actual' not in st.session_state:
    st.session_state['ejercicio_actual'] = None

# === SIDEBAR ===
with st.sidebar:
    st.title("🎯 Navegación")
    
    st.markdown("### 📊 Datos")
    tipo_datos = st.radio("Fuente:", ["Datasets Precargados", "Datos Personalizados"])
    
    if tipo_datos == "Datasets Precargados":
        datasets = load_datasets()
        dataset_name = st.selectbox("Elige dataset:", list(datasets.keys()))
        data = datasets[dataset_name]['data']
        st.info(datasets[dataset_name]['descripcion'])
    else:
        st.markdown("**Ingresa datos (separados por comas):**")
        datos_input = st.text_area("Datos:", "12, 15, 18, 20, 22, 25, 28, 30, 35, 40, 45, 50")
        try:
            data = np.array([float(x.strip()) for x in datos_input.split(',')])
            st.success(f"✅ {len(data)} datos cargados")
        except:
            st.error("❌ Error en formato")
            data = np.array([12, 15, 18, 20, 22, 25, 28, 30, 35, 40])
    
    st.markdown("---")
    st.markdown("### 📑 Secciones")
    page = st.radio("", [
        "🏠 Inicio",
        "📍 Tendencia Central",
        "📏 Dispersión",
        "📊 Posición",
        "🎭 Forma",
        "📦 Boxplot",
        "🎮 Laboratorio",
        "📈 Casos Reales",
        "❓ Cuestionario"
    ], label_visibility="collapsed")

st.title("📊 Medidas Descriptivas: El Arte de Resumir Datos")
st.markdown("---")

# Calcular medidas
medidas = calcular_medidas(data)

# === INICIO ===
if page == "🏠 Inicio":
    st.header("👋 Bienvenido al Mundo de las Medidas Descriptivas")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 La Historia de Netflix
        
        Imagina que eres científico de datos en **Netflix** con información de 10,000 usuarios 
        sobre cuántas horas ven contenido al día. Tu jefe pregunta: *"¿Cuánto ve la gente en promedio?"*
        
        No puedes mostrar una lista de 10,000 números. Necesitas **RESUMIR** en unos pocos números 
        clave que cuenten la historia completa. Eso es lo que hacen las **medidas descriptivas**.
        """)
    
    with col2:
        st.metric("📊 Tus Datos", f"{len(data)} valores")
        st.metric("📍 Media", f"{medidas['media']:.2f}")
        st.metric("📏 Desv. Est.", f"{medidas['desv_std']:.2f}")
    
    st.markdown("### 🎨 Los 4 Pilares")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info("**📍 Tendencia Central**\n\n¿Dónde está el centro?\n\nMedia • Mediana • Moda")
    with col2:
        st.warning("**📏 Dispersión**\n\n¿Qué tan separados?\n\nRango • Varianza • Desv.Est")
    with col3:
        st.success("**📊 Posición**\n\n¿Dónde se ubica?\n\nPercentiles • Cuartiles")
    with col4:
        st.error("**🎭 Forma**\n\n¿Cómo se ve?\n\nAsimetría • Curtosis")
    
    st.markdown("---")
    st.markdown("### 🎪 Metáfora: La Fiesta")
    st.markdown("""
    Si los datos fueran personas en una fiesta:
    - 📍 **Tendencia Central** → ¿Dónde está el centro de la pista?
    - 📏 **Dispersión** → ¿Bailan juntos o dispersos?
    - 📊 **Posición** → ¿Dónde estás TÚ?
    - 🎭 **Forma** → ¿Distribuidos simétricamente?
    """)
    
    st.markdown("---")
    st.markdown("### 👀 Vista Previa de Tus Datos")
    fig = crear_histograma_con_medidas(data, medidas)
    st.plotly_chart(fig, use_container_width=True)

# === TENDENCIA CENTRAL ===
elif page == "📍 Tendencia Central":
    st.header("📍 Medidas de Tendencia Central")

    st.markdown("""
    Las **medidas de tendencia central** buscan responder a una pregunta fundamental:

    > **¿Cuál es el valor más representativo de un conjunto de datos?**

    Dependiendo del contexto, este conjunto puede ser:
    - **Población**: todos los individuos de interés
    - **Muestra**: una parte de la población usada para estimar sus características
    """)

    st.info("""
    **Ejemplo Corto y sencillo**  
    Datos: 5, 5, 6, 6, 7, 100  

    - Media = 21.5  
    - Mediana = 6  
    - Moda = 5 y 6  

    👉 Cada medida responde a una idea distinta de "valor típico".
    """)

    tabs = st.tabs(["📊 Media", "🎯 Mediana", "⭐ Moda", "🔄 Comparador"])

    # ===================== MEDIA =====================
    with tabs[0]:
        st.markdown("### 📊 La Media Aritmética")

        st.markdown("""
        La **media** representa el **punto de equilibrio** de los datos.
        Es el valor que tendrían todos los datos si se redistribuyeran de forma equitativa. Para calcularla, sumamos todos los datos y a ese resultado lo dividimos entre el numero de datos.
        """)

        st.latex(r"\text{Media poblacional: } \mu = \frac{1}{N}\sum_{i=1}^{N} x_i")
        st.latex(r"\text{Media muestral: } \bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i")

        st.info("""
        📌 **Interpretación**
        - **μ**: parámetro real de la población (generalmente desconocido)
        - **x̄**: estimador de μ calculado a partir de una muestra
                
        **Nota:** Cuando usamos letras griegas nos referimos a calculos en la poblacion, y cuando son letras latinas a calculos hechos en la muestra. 
        """)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Media muestral (x̄)", f"{medidas['media']:.2f}")
            st.code(
                f"Suma de datos = {np.sum(data):.2f}\n"
                f"Tamaño de la muestra (n) = {len(data)}\n"
                f"Media = {medidas['media']:.2f}"
            )

        with col2:
            salarios = np.array([2000, 2100, 2200, 2300, 10000])
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=['E1', 'E2', 'E3', 'E4', 'E5'],
                y=salarios
            ))
            fig.add_hline(
                y=np.mean(salarios),
                line_dash="dash",
                line_color="red",
                annotation_text=f"Media: ${np.mean(salarios):.0f}"
            )
            fig.update_layout(
                title="Ejemplo: la media en salarios",
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)

        st.warning("""
        ⚠️ **Limitación importante**
        La media es **sensible a valores extremos**.
        En el ejemplo, 4 de 5 personas ganan menos que la media.
        """)

        st.success("""
        ✅ **Usar la media cuando:**
        - Datos simétricos
        - Variables cuantitativas continuas
        - Sin valores extremos relevantes
        """)

    # ===================== MEDIANA =====================
    with tabs[1]:
        st.markdown("### 🎯 La Mediana")

        st.markdown("""
        La **mediana** es el valor que **divide los datos ordenados en dos partes iguales**:

        - 50% de los datos por debajo
        - 50% de los datos por encima
        """)

        st.info("""
        📌 La mediana **no depende de la magnitud** de los valores extremos,
        solo del orden de los datos.
        """)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Mediana", f"{medidas['mediana']:.2f}")

            datos_ord = np.sort(data)
            n = len(data)

            if n % 2 == 1:
                st.code(
                    f"n = {n} (impar)\n"
                    f"Posición central: {n//2 + 1}\n"
                    f"Mediana = {datos_ord[n//2]:.2f}"
                )
            else:
                st.code(
                    f"n = {n} (par)\n"
                    f"Promedio de posiciones {n//2} y {n//2 + 1}\n"
                    f"Mediana = {medidas['mediana']:.2f}"
                )

        with col2:
            salarios = np.array([2000, 2100, 2200, 2300, 10000])
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=['E1', 'E2', 'E3', 'E4', 'E5'],
                y=salarios,
                marker_color='lightgreen'
            ))
            fig.add_hline(
                y=np.median(salarios),
                line_dash="dash",
                line_color="blue",
                annotation_text=f"Mediana: ${np.median(salarios):.0f}"
            )
            fig.update_layout(
                title="Mediana en salarios",
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)

        st.success("""
        ✅ **Ventaja clave**
        La mediana es más representativa cuando los datos son **asimétricos**
        o contienen **outliers**.
        """)

    # ===================== MODA =====================
    with tabs[2]:
        st.markdown("### ⭐ La Moda")

        st.markdown("""
        La **moda** es el valor que aparece con **mayor frecuencia** en los datos.

        📌 No siempre existe una moda única:
        - Puede ser unimodal, bimodal, multimodal o no existir
        """)

        unique, counts = np.unique(data, return_counts=True)
        max_count = np.max(counts)
        modas = unique[counts == max_count]

        col1, col2 = st.columns(2)

        with col1:
            if len(modas) == 1:
                st.success(f"Moda: {modas[0]:.2f}")
                st.info(f"Aparece {max_count} veces")
            elif len(modas) == 2:
                st.warning(f"Moda bimodal: {modas[0]:.2f} y {modas[1]:.2f}")
            elif len(modas) == len(unique):
                st.info("No hay una moda definida")
            else:
                st.warning(f"Distribución multimodal ({len(modas)} modas)")

        with col2:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=unique,
                y=counts,
                marker_color='lightcoral'
            ))
            fig.update_layout(
                title="Frecuencias de los valores",
                xaxis_title="Valor",
                yaxis_title="Frecuencia",
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)

        st.info("""
        📌 La moda es especialmente útil en:
        - Variables categóricas
        - Preferencias, respuestas nominales
        """)

    # ===================== COMPARADOR =====================
    with tabs[3]:
        st.markdown("### 🔄 Comparación e Interpretación")

        col1, col2, col3 = st.columns(3)
        col1.metric("📊 Media", f"{medidas['media']:.2f}")
        col2.metric("🎯 Mediana", f"{medidas['mediana']:.2f}")
        col3.metric("⭐ Moda", f"{medidas['moda']:.2f}" if medidas['moda'] else "N/A")

        fig = crear_histograma_con_medidas(data, medidas)
        st.plotly_chart(fig, use_container_width=True)

        diff = abs(medidas['media'] - medidas['mediana'])

        if diff < medidas['desv_std'] * 0.1:
            st.success("Distribución aproximadamente **simétrica** (media ≈ mediana)")
        elif medidas['media'] > medidas['mediana']:
            st.warning("Distribución **asimétrica a la derecha** (usa mediana)")
        else:
            st.warning("Distribución **asimétrica a la izquierda**")

# === DISPERSIÓN ===
elif page == "📏 Dispersión":
    st.header("📏 Medidas de Dispersión")

    st.markdown("""
    Las **medidas de dispersión** indican **qué tan separados están los datos entre sí**.

    Dos conjuntos pueden tener la **misma media**, pero comportamientos muy distintos.
    """)

    st.info("""
    **Ejemplo Breve**  
    Dos ciudades tienen temperatura promedio de 20°C:

    - **Ciudad A:** siempre 20°C  
    - **Ciudad B:** 6 meses 0°C y 6 meses 40°C  

    👉 Misma media, pero **climas completamente distintos**  
    La diferencia está en la **dispersión**.
    """)

    tabs = st.tabs(["📐 Rango", "📊 Varianza", "📏 Desv. Estándar", "📈 Coef. Variación"])

    # ===================== RANGO =====================
    with tabs[0]:
        st.markdown("### 📐 Rango")

        st.markdown("""
        El **rango** mide la dispersión usando **solo los valores extremos**.
        Indica la amplitud total de los datos.
        """)

        st.latex(r"R = x_{\max} - x_{\min}")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Rango", f"{medidas['rango']:.2f}")
            st.code(
                f"Valor máximo = {medidas['maximo']:.2f}\n"
                f"Valor mínimo = {medidas['minimo']:.2f}\n"
                f"Rango = {medidas['rango']:.2f}"
            )

        with col2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(range(len(data))),
                y=data,
                mode='markers'
            ))
            fig.add_hline(y=medidas['minimo'], line_color="green", annotation_text="Mínimo")
            fig.add_hline(y=medidas['maximo'], line_color="red", annotation_text="Máximo")
            fig.update_layout(title="Rango visual", height=300)
            st.plotly_chart(fig, use_container_width=True)

        st.warning("""
        ⚠️ **Limitación**
        - Extremadamente sensible a outliers  
        - Ignora completamente cómo se distribuyen los datos intermedios
        """)

    # ===================== VARIANZA =====================
    with tabs[1]:
        st.markdown("### 📊 Varianza")

        st.markdown("""
        La **varianza** mide qué tan dispersos están los datos **con respecto a la media**.
        Para entenderla bien, veámosla **paso a paso con pocos datos**.
        """)

        st.latex(r"s^2 =    \frac{\sum (x-\bar{x})^2}{n-1} \quad \rightarrow \text{Varianza Muestral}")
        st.latex(r"\sigma = \frac{\sum (x-\mu)^2}{N} \quad \rightarrow \text{Varianza Poblacional}")

        # === DATOS DE EJEMPLO ===
        ejemplo = np.array([2, 4, 6, 8, 10])
        media_ej = ejemplo.mean()

        

        st.markdown("### 📌 Paso 1: Datos originales")

        st.markdown(f"""
        Tenemos una **MUESTRA** con los siguientes datos:
        """)

        st.latex(r"Datos = \{ 2, 4, 6, 8, 10 \}")

        st.markdown(f"""
        **Calculamos Media muestral (x̄)**  
        La media es el promedio de los datos:
        """)

        st.latex(r"\bar{x} = \frac{2+ 4+ 6+ 8+ 10}{5} = \frac{30}{5} = 6.00")


        # === DESVIACIONES ===
        desviaciones = ejemplo - media_ej
        cuadrados = desviaciones ** 2

        df_calc = pd.DataFrame({
            "xᵢ": ejemplo,
            "xᵢ − x̄": desviaciones,
            "(xᵢ − x̄)²": cuadrados
        })

        st.markdown("### 📌 Paso 2: Distancia de cada dato a la media")
        st.markdown("""
        Restamos la media a cada dato para ver **qué tan lejos está** de ella, a ese valor lo elevamos al cuadrado y los sumamos todos
        """)

        st.dataframe(df_calc.style.format("{:.2f}"), hide_index=True)

        # === VARIANZA ===
        varianza_muestral = cuadrados.sum() / (len(ejemplo) - 1)

        st.markdown("### 📌 Paso 3: Calcular la varianza")
        st.markdown(f"""
        Sumamos las distancias al cuadrado y dividimos entre *(n − 1)* si estamos calculando la varianza de una muestra o sobre *N* si estamos calculando la varianza de una poblacion:
        """)

        st.latex(r"s^2 = \frac{\sum(x-\bar{x})^2}{n-1} = \frac{16 + 4+ 0+ 4+ 16}{n-1} = \frac{40}{4} = 10.00")

        st.info("""
        📌 **Interpretación**
        - La varianza muestral para los datos del ejemplo es de 10.00. En el denominador usamos *n-1* ya que estamos calculando la varianza de una **MUESTRA**
        - Si la varianza es **grande**, los datos están **muy dispersos**.
        - Si la varianza es **pequeña**, los datos están **más concentrados cerca de la media**.
        """)

        st.warning("""
        ⚠️ La varianza queda en **unidades al cuadrado** y no tiene interpretacion logica por si sola, por eso suele usarse
        la **desviación estándar**, que usa las unidades originales.
        """)

    # ===================== DESVIACIÓN ESTÁNDAR =====================
    with tabs[2]:
        st.markdown("### 📏 Desviación Estándar")

        st.markdown("""
        La **desviación estándar** es la raíz cuadrada de la varianza.
        Indica, en promedio, **cuánto se alejan los datos de la media**.
        """)

        st.latex(r"s = \sqrt{s^2} \quad \rightarrow \text{Desviacion Estandar Muestral}")
        st.latex(r"\sigma = \sqrt{\sigma^2} \quad \rightarrow \text{Desviacion Estandar Poblacional}")

        st.markdown("""
        Para el ejemplo anterior, nuestra varianza muestral dio $s^2 = 10$, entonces nuestra desviacion estandar muestral $s$ sera: $s = \sqrt{s^2}= \sqrt{10} = 3.162$
        """)


        st.markdown("### 📊 Ejemplo Grafico")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Desviación estándar (s)", f"{medidas['desv_std']:.2f}")
            st.info("""          
            📌 **Cómo leer este gráfico**

            - La **línea central** es la **media**
            - Cada línea roja marca una **desviación estándar (σ)** desde la media
            - **σ no es un porcentaje**, es una **distancia típica**
            - Cuantas más líneas necesites para cubrir los datos, **más dispersos están**
            """)

        with col2:
            fig = go.Figure()

            # Eje horizontal centrado en la media
            x_range = np.linspace(
                medidas['media'] - 4 * medidas['desv_std'],
                medidas['media'] + 4 * medidas['desv_std'],
                200
            )

            # Curva solo como forma visual (no probabilística)
            y = stats.norm.pdf(x_range, medidas['media'], medidas['desv_std'])
            fig.add_trace(
                go.Scatter(
                    x=x_range,
                    y=y,
                    fill='tozeroy',
                    name="Distribución de los datos",
                    opacity=0.6
                )
            )

            # Media
            fig.add_vline(
                x=medidas['media'],
                line_color="black",
                line_width=3,
                annotation_text="Media",
                annotation_position="top"
            )

            # Líneas de desviación estándar
            for i in range(1, 4):
                fig.add_vline(
                    x=medidas['media'] + i * medidas['desv_std'],
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"+{i}σ",
                    annotation_position="top"
                )
                fig.add_vline(
                    x=medidas['media'] - i * medidas['desv_std'],
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"-{i}σ",
                    annotation_position="top"
                )

            fig.update_layout(
                title="Distancia típica de los datos respecto a la media",
                xaxis_title="Valores de la variable",
                yaxis_title="Frecuencia (forma visual)",
                height=300,
                showlegend=False
            )

            st.plotly_chart(fig, use_container_width=True)

        st.write("""
                    📌 **Ventaja clave: Se manejan las mismas unidades que los datos**

                    La desviación estándar se expresa en las **mismas unidades** que la variable original.
                    Esto hace que su interpretación sea **directa e intuitiva**.

                    **Ejemplos:**
                    - Si los datos son **temperaturas (°C)** → la desviación estándar está en **°C**
                    - Si los datos son **salarios (USD)** → la desviación estándar está en **USD**
                    - Si los datos son **tiempos (minutos)** → la desviación estándar está en **minutos**

                    **Interpretación práctica:**
                    Decir que la desviación estándar es **5** significa que,
                    en promedio, los datos se alejan **5 unidades reales** de la media.

                    **Conclusion:** A diferencia de la varianza (que queda en unidades al cuadrado),
                    la desviación estándar **sí se puede interpretar en el mundo real**.
                    """)
                

    # ===================== COEFICIENTE DE VARIACIÓN =====================
    with tabs[3]:
        st.markdown("### 📈 Coeficiente de Variación")

        st.markdown("""
        El **coeficiente de variación (CV)** mide la dispersión **en relación con la media**.
        Permite comparar variabilidad entre variables con distintas unidades.
        """)

        st.latex(r"CV_{Muestral} = \frac{s}{\bar{x}} \times 100\%")
        st.latex(r"CV_{Poblacional} = \frac{\sigma}{\mu} \times 100\%")

        st.metric("CV", f"{medidas['cv']:.2f}%", help="Dispersión relativa")

        st.info("""
        **Interpretación general:**
        - CV < 15% → Baja variabilidad
        - 15% ≤ CV < 30% → Variabilidad moderada
        - CV ≥ 30% → Alta variabilidad
        """)

        st.markdown("**Ejemplo comparativo:**")

        col1, col2 = st.columns(2)

        with col1:
            st.write("📏 **Estaturas**")
            st.write("μ = 170 cm, σ = 10 cm")
            st.metric("CV", f"{10/170*100:.2f}%")

        with col2:
            st.write("💰 **Salarios**")
            st.write("μ = $3000, σ = $500")
            st.metric("CV", f"{500/3000*100:.2f}%")

        st.success("""
        👉 Aunque las unidades son distintas, el CV permite comparar
        **qué variable es relativamente más variable, en este caso, los salarios son mas variables que las estaturas.**.
        """)

# === POSICIÓN ===
elif page == "📊 Posición":
    st.header("📊 Medidas de Posición")

    # =========================================================
    # CONTEXTO GENERAL
    # =========================================================
    st.info("""
    📌 **Idea clave**

    Las medidas de posición sirven para responder preguntas como:
    - ¿Estoy por encima o por debajo del resto?
    - ¿En qué parte del grupo me encuentro?

    👉 No miden dispersión  
    👉 No miden forma  
    👉 Miden **UBICACIÓN dentro del conjunto**
    """)

    # =========================================================
    # DATOS DE EJEMPLO FIJOS
    # =========================================================
    st.markdown("## 📋 Datos de ejemplo (ordenados)")

    data_ej = np.array([40, 45, 50, 55, 60, 65, 70, 75, 80, 85])
    n = len(data_ej)

    st.latex(r"\{40,\;45,\;50,\;55,\;60,\;65,\;70,\;75,\;80,\;85\}")
    st.latex(rf"n = {n}")

    tabs = st.tabs(["📍 Percentiles", "📦 Cuartiles", "📏 IQR", "🔁 Equivalencias"])

    # =========================================================
    # TAB 1 — PERCENTILES
    # =========================================================
    with tabs[0]:
        st.markdown("## 📍 Percentiles")

        st.markdown("""
        Un **percentil Pₖ** es el valor que deja **k% de los datos por debajo**
        cuando los datos están **ordenados**.
        """)

        st.markdown("### 🎯 Ejemplo: calcular el percentil 55 (P₅₅)")

        # Paso 1
        st.markdown("### 1️⃣ Contar los datos")
        st.latex(r"n = 10")

        # Paso 2
        st.markdown("### 2️⃣ Calcular la posición del percentil")
        st.markdown("Usamos la siguiente fórmula:")

        st.latex(r"\text{Posición} = \frac{k}{100}(n + 1)")
        st.latex(r"\text{Posición} = \frac{55}{100}(10 + 1) = 6.05")

        # Paso 3
        st.markdown("### 3️⃣ Ubicar los valores vecinos")
        st.markdown("""
        La posición **6.05** está:
        - después del dato 6
        - antes del dato 7
        """)

        st.latex(r"x_6 = 65 \qquad x_7 = 70")

        # Paso 4
        st.markdown("### 4️⃣ Interpolación (¿qué hacemos cuando la posición NO es entera?)")

        st.markdown("""
        La posición obtenida fue **6.05**. Esto significa que el percentil **NO cae exactamente sobre un dato**, sino **entre el dato 6 y el dato 7**.

        👉 Por eso debemos **interpolar**.
        """)

        st.markdown("#### ¿Qué es interpolar?")
        st.markdown("""
        Interpolar significa **calcular un valor intermedio**, asumiendo que el cambio
        entre dos datos consecutivos es **progresivo y uniforme**.
        """)

        st.markdown("#### 📍 Paso a paso de la interpolación")

        st.markdown("""
        1. **Identificamos los dos valores entre los que cae el percentil**
        """)
        st.latex(r"x_6 = 65 \qquad x_7 = 70")

        st.markdown("""
        2. **Tomamos la parte decimal de la posición**
        """)
        st.latex(r"6.05 \rightarrow \text{Parte Decimal = 0.05}")

        st.markdown("""
        Esto indica que el percentil está **al 5% del camino**
        entre el dato 6 y el dato 7.
        """)

        st.markdown("""
        3. **Calculamos la distancia entre los dos datos**
        """)
        st.latex(r"70 - 65 = 5")

        st.markdown("""
        4. **Calculamos cuánto avanzamos desde el dato inferior**
        """)
        st.latex(r"0.05 \times 5 = 0.25")

        st.markdown("""
        5. **Sumamos ese avance al valor inferior**
        """)
        st.latex(r"P_{55} = 65 + 0.25 = 65.25")

        st.markdown("""
        6. **Profe, quiero la formula y ya!** ok estimado si quieres interpolar rapidamente, la formula seria asi:
        """)
        st.latex(r"Interpolacion = \text{Valor menor} + (\text{Valor mayor} - \text{Valor menor})* \text{Parte Decimal}")

        st.success("""
        ✅ **Conclusión**

        El percentil 55 es **65.25**.

        Esto significa que el **55% de los datos es menor o igual a 65.25**.
        """)

        st.warning("""
        ⚠️ Si la posición hubiera sido un número entero,
        el percentil sería exactamente ese dato (sin interpolar).
        """)

    # =========================================================
    # TAB 2 — CUARTILES
    # =========================================================
    with tabs[1]:
        st.markdown("## 📦 Cuartiles")

        st.markdown("""
        Los **cuartiles** dividen los datos ordenados en **4 partes iguales**.
        Cada parte contiene el **25% de los datos**.
        """)

        # Q1
        st.markdown("### 📌 Primer cuartil (Q₁)")

        st.latex(r"\text{Posición} = \frac{25}{100}(n+1)")
        st.latex(r"\text{Posición} = \frac{25}{100}(11) = 2.75")
        st.latex(r"x_2 = 45 \qquad x_3 = 50")
        st.latex(r"Q_1 = 45 + 0.75(50 - 45) = 48.75")

        # Q2
        st.markdown("### 📌 Segundo cuartil (Q₂ = Mediana)")

        st.latex(r"\text{Posición} = \frac{50}{100}(11) = 5.5")
        st.latex(r"x_5 = 60 \qquad x_6 = 65")
        st.latex(r"Q_2 = 60 + 0.5(65 - 60) = 62.5")

        # Q3
        st.markdown("### 📌 Tercer cuartil (Q₃)")

        st.latex(r"\text{Posición} = \frac{75}{100}(11) = 8.25")
        st.latex(r"x_8 = 75 \qquad x_9 = 80")
        st.latex(r"Q_3 = 75 + 0.25(80 - 75) = 76.25")

        st.success("""
        👉 Los cuartiles permiten saber:
        - dónde empieza el 25% inferior
        - dónde está la mitad
        - dónde empieza el 25% superior
        """)

    # =========================================================
    # TAB 3 — IQR
    # =========================================================
    with tabs[2]:
        st.markdown("## 📏 Rango Intercuartílico (IQR)")

        st.markdown("""
        El **IQR** mide la amplitud del **50% central de los datos**.
        Ignora los valores extremos.
        """)

        st.latex(r"IQR = Q_3 - Q_1")
        st.latex(r"IQR = 76.25 - 48.75 = 27.5")

        st.success("""
        ✅ **Interpretación**

        El 50% central de los datos se concentra en un rango de **27.5 unidades**.
        """)

        st.info("""
        📌 El IQR es muy usado porque:
        - No se ve afectado por outliers
        - Describe el “corazón” de la distribución
        """)

    # =========================================================
    # TAB 4 — EQUIVALENCIAS
    # =========================================================
    with tabs[3]:
        st.markdown("## 🔁 Equivalencias importantes")

        st.markdown("""
        Los cuartiles **NO son distintos a los percentiles**.
        Son simplemente percentiles con nombre especial.
        """)

        st.latex(r"Q_1 = P_{25}")
        st.latex(r"Q_2 = P_{50} \quad (\text{Mediana})")
        st.latex(r"Q_3 = P_{75}")

        st.success("""
        🧠 **Idea final**

        - Percentiles → cualquier porcentaje
        - Cuartiles → percentiles clave
        - Todo se basa en **ordenar datos y buscar posiciones**
        """)

# === FORMA (VERSIÓN PEDAGÓGICA COMPLETA) ===
elif page == "🎭 Forma":
    st.header("🎭 Medidas de Forma: ¿Cómo Se Ve Tu Distribución?")
    
    st.markdown("""
    Imagina que tienes un montón de datos y quieres describir "la forma" que tienen cuando los graficas.
    ¿Son simétricos como una montaña perfecta? ¿O están inclinados hacia un lado?
    
    Las **medidas de forma** nos ayudan a responder estas preguntas de manera numérica.
    """)
    
    tabs = st.tabs(["📐 Asimetría (Skewness)", "📊 Curtosis (Apuntamiento)"])
    
    with tabs[0]:
        st.markdown("## 📐 Asimetría: ¿Está Balanceado o Inclinado?")
        
        st.markdown("""
        La **asimetría** mide si tu distribución tiene una "cola larga" hacia un lado.
        Es como preguntarse: ¿Los datos están balanceados alrededor del centro, o hay más datos
        acumulados en un extremo?
        
        ### 🎯 Tu Dataset Actual
        """)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric("Coeficiente de Asimetría", f"{medidas['asimetria']:.3f}")
            
            if abs(medidas['asimetria']) < 0.5:
                st.success("**✅ Aproximadamente Simétrica**")
            elif medidas['asimetria'] > 0:
                st.warning("**➡️ Asimétrica a la Derecha (Positiva)**")
            else:
                st.warning("**⬅️ Asimétrica a la Izquierda (Negativa)**")
            
            st.markdown("**Tus medidas de centro:**")
            st.write(f"• Media: {medidas['media']:.2f}")
            st.write(f"• Mediana: {medidas['mediana']:.2f}")
            if medidas['moda']:
                st.write(f"• Moda: {medidas['moda']:.2f}")
        
        with col2:
            fig_tu_dist = crear_histograma_con_medidas(data, medidas)
            st.plotly_chart(fig_tu_dist, use_container_width=True)
        
        st.markdown("---")
        st.markdown("## 📚 Los 3 Tipos de Asimetría Explicados")
        
        # TIPO 1: SIMÉTRICA
        st.markdown("### 1️⃣ Distribución Simétrica (Asimetría ≈ 0)")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Crear distribución simétrica
            np.random.seed(42)
            datos_simetricos = np.random.normal(50, 10, 1000)
            
            fig_sim = go.Figure()
            fig_sim.add_trace(go.Histogram(
                x=datos_simetricos,
                nbinsx=30,
                name="Frecuencia",
                marker_color='lightblue',
                opacity=0.7
            ))
            
            media_sim = np.mean(datos_simetricos)
            mediana_sim = np.median(datos_simetricos)
            
            fig_sim.add_vline(x=media_sim, line_dash="dash", line_color="red", 
                             annotation_text=f"Media: {media_sim:.1f}")
            fig_sim.add_vline(x=mediana_sim, line_dash="dash", line_color="blue",
                             annotation_text=f"Mediana: {mediana_sim:.1f}")
            
            fig_sim.update_layout(
                title="Distribución Simétrica - Ejemplo: Estaturas",
                xaxis_title="Valores",
                yaxis_title="Frecuencia",
                height=350
            )
            st.plotly_chart(fig_sim, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Características:")
            st.success("**Media ≈ Mediana ≈ Moda**")
            
            st.markdown("""
            **🔍 ¿Qué significa?**
            
            Los datos están **balanceados** alrededor del centro. 
            Si divides la distribución por la mitad, ambas mitades 
            son casi idénticas (como un espejo).
            
            **🌍 Ejemplos reales:**
            - Estaturas de personas adultas
            - Notas en un examen bien diseñado
            - Errores de medición
            - Temperatura en un mes
            
            **💡 Implicación:**
            Cualquiera de las tres medidas de centro 
            (media, mediana, moda) representa bien 
            el "valor típico".
            """)
        
        st.markdown("---")
        
        # TIPO 2: ASIMÉTRICA DERECHA
        st.markdown("### 2️⃣ Distribución Asimétrica a la Derecha (Asimetría > 0)")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Crear distribución asimétrica derecha
            datos_derecha = np.random.gamma(2, 2, 1000) * 1000 + 2000
            
            fig_der = go.Figure()
            fig_der.add_trace(go.Histogram(
                x=datos_derecha,
                nbinsx=30,
                name="Frecuencia",
                marker_color='lightsalmon',
                opacity=0.7
            ))
            
            media_der = np.mean(datos_derecha)
            mediana_der = np.median(datos_derecha)
            moda_der = float(stats.mode(datos_derecha.round(-2), keepdims=True)[0][0])
            
            fig_der.add_vline(x=moda_der, line_dash="dash", line_color="green",
                             annotation_text=f"Moda: ${moda_der:.0f}", annotation_position="top left")
            fig_der.add_vline(x=mediana_der, line_dash="dash", line_color="blue",
                             annotation_text=f"Mediana: ${mediana_der:.0f}", annotation_position="top")
            fig_der.add_vline(x=media_der, line_dash="dash", line_color="red", 
                             annotation_text=f"Media: ${media_der:.0f}", annotation_position="top right")
            
            # Agregar flecha mostrando la "cola"
            fig_der.add_annotation(
                x=media_der + 1000, y=50,
                text="← Cola larga hacia la derecha",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="red"
            )
            
            fig_der.update_layout(
                title="Distribución Asimétrica Derecha - Ejemplo: Salarios",
                xaxis_title="Salario ($)",
                yaxis_title="Frecuencia",
                height=350
            )
            st.plotly_chart(fig_der, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Características:")
            st.warning("**Media > Mediana > Moda**")
            
            st.markdown("""
            **🔍 ¿Qué significa?**
            
            La mayoría de los datos se concentran en valores 
            **BAJOS**, pero hay algunos valores **MUY ALTOS** 
            que "jalan" la media hacia la derecha.
            
            Es como una cola larga que se extiende hacia 
            valores altos →→→
            
            **🌍 Ejemplos reales:**
            - **Salarios**: La mayoría gana poco o moderado, 
              pero algunos ejecutivos ganan millones
            - **Precio de viviendas**: Muchas baratas, 
              pocas mansiones carísimas
            - **Edad al morir**: La mayoría vive 70-90 años,
              pocos llegan a 100+
            - **Tiempo para completar una tarea**: 
              La mayoría rápido, algunos muy lentos
            
            **💡 Implicación CLAVE:**
            
            ⚠️ **La MEDIA está inflada** por los valores altos.
            
            ✅ **Usa la MEDIANA** para representar el valor típico.
            
            Por ejemplo: Si la media salarial es $5,000 
            pero la mediana es $3,000, significa que 
            **la mayoría gana menos de $5,000**. 
            Los salarios altos distorsionan el promedio.
            """)
        
        st.info("""
        **🎯 Ejemplo Visual:** Imagina una clase donde la mayoría sacó 60-70 puntos, 
        pero un genio sacó 100. La media se va hacia arriba por ese valor alto, 
        pero la mediana (el del medio) sigue cerca de 65, representando mejor al grupo.
        """)
        
        st.markdown("---")
        
        # TIPO 3: ASIMÉTRICA IZQUIERDA
        st.markdown("### 3️⃣ Distribución Asimétrica a la Izquierda (Asimetría < 0)")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Crear distribución asimétrica izquierda
            datos_izq = 100 - np.random.gamma(2, 2, 1000) * 5
            datos_izq = datos_izq[datos_izq > 0]  # Eliminar negativos
            
            fig_izq = go.Figure()
            fig_izq.add_trace(go.Histogram(
                x=datos_izq,
                nbinsx=30,
                name="Frecuencia",
                marker_color='lightgreen',
                opacity=0.7
            ))
            
            media_izq = np.mean(datos_izq)
            mediana_izq = np.median(datos_izq)
            moda_izq = float(stats.mode(datos_izq.round(0), keepdims=True)[0][0])
            
            fig_izq.add_vline(x=media_izq, line_dash="dash", line_color="red",
                             annotation_text=f"Media: {media_izq:.1f}", annotation_position="top left")
            fig_izq.add_vline(x=mediana_izq, line_dash="dash", line_color="blue",
                             annotation_text=f"Mediana: {mediana_izq:.1f}", annotation_position="top")
            fig_izq.add_vline(x=moda_izq, line_dash="dash", line_color="green", 
                             annotation_text=f"Moda: {moda_izq:.0f}", annotation_position="top right")
            
            # Agregar flecha mostrando la "cola"
            fig_izq.add_annotation(
                x=media_izq - 10, y=50,
                text="Cola larga hacia la izquierda →",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="red"
            )
            
            fig_izq.update_layout(
                title="Distribución Asimétrica Izquierda - Ejemplo: Examen Fácil",
                xaxis_title="Calificación",
                yaxis_title="Frecuencia",
                height=350
            )
            st.plotly_chart(fig_izq, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Características:")
            st.warning("**Moda > Mediana > Media**")
            
            st.markdown("""
            **🔍 ¿Qué significa?**
            
            La mayoría de los datos se concentran en valores 
            **ALTOS**, pero hay algunos valores **MUY BAJOS** 
            que "jalan" la media hacia la izquierda.
            
            Es como una cola larga que se extiende hacia 
            valores bajos ←←←
            
            **🌍 Ejemplos reales:**
            - **Examen muy fácil**: La mayoría saca 90-100,
              pocos reprueban con 20-40
            - **Edad de jubilación**: La mayoría se jubila 
              cerca de 65, pocos antes por enfermedad
            - **Tiempo de vida de bombillas**: La mayoría 
              dura 900-1000 horas, pocas fallan temprano
            - **Satisfacción del cliente**: La mayoría muy 
              satisfecha, pocos muy insatisfechos
            
            **💡 Implicación CLAVE:**
            
            ⚠️ **La MEDIA está reducida** por los valores bajos.
            
            ✅ **Usa la MEDIANA o MODA** como mejor representación.
            
            Por ejemplo: En un examen fácil, la media puede 
            ser 85 por algunos reprobados, pero la mediana 
            es 92, mostrando que **la mayoría sacó muy buena nota**.
            """)
        
        st.info("""
        **🎯 Ejemplo Visual:** Imagina que mides cuánto tarda la gente en llegar al trabajo. 
        La mayoría tarda 20-25 minutos (tráfico normal), pero algunos días con accidente tardan 
        60 minutos. Esos días raros bajan el promedio, pero la mediana de 22 minutos representa 
        mejor el tiempo "típico".
        """)
        
        st.markdown("---")
        
        # TABLA RESUMEN
        st.markdown("## 📋 Tabla Resumen: ¿Cuál Usar?")
        
        df_resumen_asim = pd.DataFrame({
            'Tipo': ['Simétrica', 'Asimétrica Derecha', 'Asimétrica Izquierda'],
            'Coeficiente': ['≈ 0', '> 0 (positivo)', '< 0 (negativo)'],
            'Relación': ['Media ≈ Mediana ≈ Moda', 'Media > Mediana > Moda', 'Moda > Mediana > Media'],
            'Cola Larga': ['Ninguna (balanceada)', 'Hacia la derecha →', 'Hacia la izquierda ←'],
            'Medida Recomendada': ['Media o Mediana', '⚠️ MEDIANA', '⚠️ MEDIANA o MODA'],
            'Ejemplo': ['Estaturas', 'Salarios', 'Examen fácil']
        })
        
        st.dataframe(df_resumen_asim, use_container_width=True, hide_index=True)
        
        st.success("""
        **🎓 Regla de Oro:**
        
        Si tu distribución es **asimétrica** (tiene cola larga), **NO uses la media** como medida de centro.
        La media será engañosa porque está "jalada" por los valores extremos.
        
        **Usa la MEDIANA** en su lugar, que es resistente a valores extremos.
        """)
    
    with tabs[1]:
        st.markdown("## 📊 Curtosis: ¿Qué Tan Puntiaguda Es Tu Distribución?")
        
        st.markdown("""
        La **curtosis** mide qué tan "concentrados" o "dispersos" están los datos alrededor del centro.
        
        Piénsalo así: imagina dos montañas con la misma altura (media) y la misma desviación estándar:
        - Una es **alta y puntiaguda** (como el Everest) → Leptocúrtica
        - Otra es **baja y achatada** (como una colina) → Platicúrtica
        - Una intermedia **como campana** → Mesocúrtica
        
        ### 🎯 Tu Dataset Actual
        """)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric("Coeficiente de Curtosis", f"{medidas['curtosis']:.3f}")
            
            if medidas['curtosis'] > 1:
                st.warning("**⛰️ Leptocúrtica (Puntiaguda)**")
            elif medidas['curtosis'] < -1:
                st.info("**🏔️ Platicúrtica (Achatada)**")
            else:
                st.success("**🔔 Mesocúrtica (Normal)**")
        
        with col2:
            fig_tu_dist2 = crear_histograma_con_medidas(data, medidas)
            st.plotly_chart(fig_tu_dist2, use_container_width=True, key="tab1_fig")
        
        st.markdown("---")
        st.markdown("## 📚 Los 3 Tipos de Curtosis Explicados")
        
        # TIPO 1: MESOCÚRTICA
        st.markdown("### 1️⃣ Mesocúrtica (Curtosis ≈ 0): La \"Normal\"")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Crear distribución normal (mesocúrtica)
            np.random.seed(42)
            x_normal = np.linspace(-4, 4, 300)
            y_normal = stats.norm.pdf(x_normal, 0, 1)
            
            fig_meso = go.Figure()
            fig_meso.add_trace(go.Scatter(
                x=x_normal,
                y=y_normal,
                fill='tozeroy',
                name='Mesocúrtica',
                line=dict(color='blue', width=3),
                fillcolor='rgba(0, 100, 255, 0.3)'
            ))
            
            fig_meso.update_layout(
                title="Distribución Mesocúrtica - La Campana de Gauss Clásica",
                xaxis_title="Desviaciones estándar (σ)",
                yaxis_title="Densidad",
                height=350,
                showlegend=False
            )
            
            # Añadir líneas en ±1σ, ±2σ, ±3σ
            for i in [1, 2, 3]:
                fig_meso.add_vline(x=i, line_dash="dot", line_color="gray", opacity=0.5)
                fig_meso.add_vline(x=-i, line_dash="dot", line_color="gray", opacity=0.5)
            
            st.plotly_chart(fig_meso, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Características:")
            st.success("**Curtosis ≈ 0**")
            
            st.markdown("""
            **🔍 ¿Qué significa?**
            
            Es la distribución "**estándar**" o "**referencia**".
            Tiene la forma de campana clásica que ves en 
            todos los libros de estadística.
            
            **Ni muy puntiaguda, ni muy achatada.**
            
            **🔔 Propiedades:**
            - 68% de datos dentro de ±1σ
            - 95% dentro de ±2σ
            - 99.7% dentro de ±3σ
            
            **🌍 Ejemplos reales:**
            - Estaturas humanas
            - Coeficiente intelectual (IQ)
            - Errores de medición
            - Muchos fenómenos naturales
            
            **💡 Implicación:**
            Los datos se comportan "como se espera".
            No hay concentración extrema ni dispersión inusual.
            Es la distribución más común en la naturaleza.
            """)
        
        st.info("""
        **🎯 Piénsalo así:** Es como una montaña "normal". No llama la atención 
        por ser ni demasiado empinada ni demasiado plana. Es el estándar.
        """)
        
        st.markdown("---")
        
        # TIPO 2: LEPTOCÚRTICA
        st.markdown("### 2️⃣ Leptocúrtica (Curtosis > 0): La Puntiaguda")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Crear distribuciones para comparar
            x_comp = np.linspace(-4, 4, 300)
            y_normal_comp = stats.norm.pdf(x_comp, 0, 1)
            y_lepto = stats.norm.pdf(x_comp, 0, 0.5)  # Más concentrada
            
            fig_lepto = go.Figure()
            
            # Normal de referencia (transparente)
            fig_lepto.add_trace(go.Scatter(
                x=x_comp,
                y=y_normal_comp,
                name='Mesocúrtica (referencia)',
                line=dict(color='gray', width=2, dash='dash'),
                opacity=0.4
            ))
            
            # Leptocúrtica
            fig_lepto.add_trace(go.Scatter(
                x=x_comp,
                y=y_lepto,
                fill='tozeroy',
                name='Leptocúrtica',
                line=dict(color='red', width=3),
                fillcolor='rgba(255, 0, 0, 0.3)'
            ))
            
            # Anotaciones
            fig_lepto.add_annotation(
                x=0, y=0.85,
                text="← MÁS ALTA Y PUNTIAGUDA",
                showarrow=True,
                arrowhead=2,
                arrowcolor="red",
                font=dict(color="red", size=12, family="Arial Black")
            )
            
            fig_lepto.add_annotation(
                x=2.5, y=0.02,
                text="Colas más pesadas →<br>(más outliers potenciales)",
                showarrow=False,
                font=dict(color="darkred", size=10)
            )
            
            fig_lepto.update_layout(
                title="Distribución Leptocúrtica - Datos MUY Concentrados",
                xaxis_title="Valores",
                yaxis_title="Densidad",
                height=350
            )
            
            st.plotly_chart(fig_lepto, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Características:")
            st.warning("**Curtosis > 0 (positiva)**")
            
            st.markdown("""
            **🔍 ¿Qué significa?**
            
            Los datos están **MUY CONCENTRADOS** alrededor 
            de la media. El pico es más alto y puntiagudo.
            
            ⛰️ **Como el Monte Everest**: Alto y empinado
            
            **⚠️ Característica importante:**
            Aunque están concentrados, tiene **colas más pesadas**.
            Esto significa que cuando hay outliers, 
            pueden ser MUY extremos.
            
            **🌍 Ejemplos reales:**
            - **Retornos financieros**: La mayoría de días 
              el mercado cambia poco (±1%), pero algunos días 
              hay caídas o subidas enormes (±10%)
            - **Tiempo de respuesta de servidores**: 
              Casi siempre responden en 100ms, pero ocasionalmente 
              tardan 10 segundos (fallas)
            - **Control de calidad**: Productos muy consistentes,
              pero los defectuosos son MUY defectuosos
            
            **💡 Implicación CLAVE:**
            
            ✅ **Alta consistencia**: La mayoría de datos 
            son muy similares (predecibles)
            
            ⚠️ **PERO**: Cuando aparecen valores raros,
            son EXTREMADAMENTE raros (riesgo de cola)
            
            **🎯 En contexto de inversiones:**
            Es el famoso "**Riesgo de Cola**" (tail risk):
            9 de cada 10 días todo normal, pero el día 10 
            puede ser catastrófico.
            """)
        
        st.warning("""
        **⚠️ Advertencia Práctica:**
        
        Una distribución leptocúrtica puede **parecer segura** porque está muy concentrada,
        pero los outliers (cuando ocurren) son **muy peligrosos**. Es como vivir al pie de 
        un volcán: 99% del tiempo todo tranquilo, pero cuando erupciona...
        """)
        
        st.markdown("---")
        
        # TIPO 3: PLATICÚRTICA
        st.markdown("### 3️⃣ Platicúrtica (Curtosis < 0): La Achatada")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Crear distribuciones para comparar
            y_normal_comp2 = stats.norm.pdf(x_comp, 0, 1)
            y_plati = stats.norm.pdf(x_comp, 0, 1.8)  # Más dispersa
            
            fig_plati = go.Figure()
            
            # Normal de referencia (transparente)
            fig_plati.add_trace(go.Scatter(
                x=x_comp,
                y=y_normal_comp2,
                name='Mesocúrtica (referencia)',
                line=dict(color='gray', width=2, dash='dash'),
                opacity=0.4
            ))
            
            # Platicúrtica
            fig_plati.add_trace(go.Scatter(
                x=x_comp,
                y=y_plati,
                fill='tozeroy',
                name='Platicúrtica',
                line=dict(color='green', width=3),
                fillcolor='rgba(0, 255, 0, 0.3)'
            ))
            
            # Anotaciones
            fig_plati.add_annotation(
                x=0, y=0.22,
                text="← MÁS BAJA Y ACHATADA",
                showarrow=True,
                arrowhead=2,
                arrowcolor="green",
                font=dict(color="green", size=12, family="Arial Black")
            )
            
            fig_plati.add_annotation(
                x=2.5, y=0.15,
                text="Datos más dispersos →<br>(menos outliers extremos)",
                showarrow=False,
                font=dict(color="darkgreen", size=10)
            )
            
            fig_plati.update_layout(
                title="Distribución Platicúrtica - Datos Más Dispersos",
                xaxis_title="Valores",
                yaxis_title="Densidad",
                height=350
            )
            
            st.plotly_chart(fig_plati, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Características:")
            st.info("**Curtosis < 0 (negativa)**")
            
            st.markdown("""
            **🔍 ¿Qué significa?**
            
            Los datos están **MÁS DISPERSOS** alrededor 
            de la media. El pico es más bajo y achatado.
            
            🏔️ **Como una colina suave**: Baja y extendida
            
            **Característica clave:**
            Los datos están más "**esparcidos uniformemente**".
            Menos concentración en el centro, más distribución
            en los extremos.
            
            **🌍 Ejemplos reales:**
            - **Distribución uniforme**: Como lanzar un dado,
              todos los resultados (1-6) son igual de probables
            - **Edad de empleados en startup**: Desde 22 hasta 
              45 años, sin concentración clara
            - **Calificaciones en examen mal diseñado**: 
              Algunos sacan 100, otros 50, otros 75, sin patrón claro
            - **Temperatura en zona de transición climática**:
              Varía mucho sin un "centro" claro
            
            **💡 Implicación CLAVE:**
            
            ⚠️ **Baja consistencia**: Los datos son muy variables
            (impredecibles)
            
            ✅ **PERO**: Los outliers no son tan extremos
            como en leptocúrtica. La variabilidad es más "normal"
            
            **🎯 En contexto práctico:**
            Es más difícil predecir valores futuros porque 
            no hay una tendencia central fuerte. Los datos 
            están "por todos lados".
            """)
        
        st.info("""
        **🎯 Piénsalo así:**
        
        **Leptocúrtica** = Todos llegan a trabajar entre 8:55-9:05am (muy predecible),
        pero un día alguien llega a las 11am (extremo).
        
        **Platicúrtica** = La gente llega entre 8:30-9:30am (variable),
        pero nadie llega súper tarde. Menos predecible, pero sin sorpresas extremas.
        """)
        
        st.markdown("---")
        

# === BOXPLOT (VERSIÓN PEDAGÓGICA COMPLETA) ===
elif page == "📦 Boxplot":
    st.header("📦 Diagrama de Cajas y Bigotes: El Resumen Visual Perfecto")
    
    st.markdown("""
    El **boxplot** (o diagrama de caja y bigotes) es uno de los gráficos más poderosos en estadística.
    En un solo vistazo, te dice:
    
    - 📍 ¿Dónde está el centro de los datos?
    - 📏 ¿Qué tan dispersos están?
    - 🎯 ¿Hay valores extremos (outliers)?
    - ⚖️ ¿La distribución es simétrica o asimétrica?
    
    **Todo esto en una sola imagen.**
    """)
    
    # Sección de tabs
    tabs = st.tabs([
        "📚 Los 5 Números",
        "🔨 Construcción Paso a Paso", 
        "🎨 Anatomía Completa",
        "⚠️ Outliers"
    ])
    
    # ==========================================
    # TAB 1: LOS 5 NÚMEROS
    # ==========================================
    with tabs[0]:
        st.markdown("## 📚 Los 5 Números Clave del Boxplot")
        
        st.markdown("""
        El boxplot se basa en **5 números fundamentales** que resumen completamente tu distribución.
        Estos se llaman el **resumen de 5 números** (Five-Number Summary).
        """)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### 🔢 Tus 5 Números:")
            st.metric("1️⃣ Mínimo", f"{medidas['minimo']:.2f}", help="El valor más pequeño")
            st.metric("2️⃣ Q1 (Primer Cuartil)", f"{medidas['q1']:.2f}", help="25% de datos por debajo")
            st.metric("3️⃣ Mediana (Q2)", f"{medidas['q2']:.2f}", help="50% de datos por debajo")
            st.metric("4️⃣ Q3 (Tercer Cuartil)", f"{medidas['q3']:.2f}", help="75% de datos por debajo")
            st.metric("5️⃣ Máximo", f"{medidas['maximo']:.2f}", help="El valor más grande")
            
            st.markdown("---")
            st.metric("📏 Rango Intercuartílico (IQR)", f"{medidas['iqr']:.2f}", 
                     help="Q3 - Q1: Rango del 50% central")
        
        with col2:
            st.markdown("### 📊 Visualización de los 5 Números")
            
            # Crear visualización de los datos ordenados
            datos_ordenados = np.sort(data)
            n = len(datos_ordenados)
            
            fig_5num = go.Figure()
            
            # Todos los puntos
            fig_5num.add_trace(go.Scatter(
                x=list(range(n)),
                y=datos_ordenados,
                mode='markers',
                marker=dict(size=6, color='lightblue', line=dict(width=1, color='darkblue')),
                name='Todos los datos',
                hovertemplate='Posición: %{x}<br>Valor: %{y:.2f}<extra></extra>'
            ))
            
            # Líneas horizontales para los 5 números
            fig_5num.add_hline(y=medidas['minimo'], line_dash="dash", line_color="green",
                              annotation_text="Mínimo", annotation_position="right")
            fig_5num.add_hline(y=medidas['q1'], line_dash="dash", line_color="orange",
                              annotation_text="Q1 (25%)", annotation_position="right")
            fig_5num.add_hline(y=medidas['q2'], line_dash="solid", line_color="red", line_width=3,
                              annotation_text="Mediana (50%)", annotation_position="right")
            fig_5num.add_hline(y=medidas['q3'], line_dash="dash", line_color="orange",
                              annotation_text="Q3 (75%)", annotation_position="right")
            fig_5num.add_hline(y=medidas['maximo'], line_dash="dash", line_color="green",
                              annotation_text="Máximo", annotation_position="right")
            
            fig_5num.update_layout(
                title="Datos Ordenados con los 5 Números Marcados",
                xaxis_title="Posición en el ordenamiento",
                yaxis_title="Valor",
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig_5num, use_container_width=True)
        
        st.markdown("---")
        
        st.info("""
        ### 🎯 ¿Qué Significa Cada Uno?
        
        **1️⃣ Mínimo:** El estudiante que sacó la nota más baja, el empleado que gana menos, 
        la temperatura más fría del mes.
        
        **2️⃣ Q1 (Primer Cuartil - Percentil 25):** El valor que deja el **25% de los datos por debajo**. 
        Si estás en Q1, superaste al 25% pero el 75% está por encima de ti.
        
        **3️⃣ Mediana (Q2 - Percentil 50):** El valor **del medio**. Exactamente la mitad de los datos 
        está por debajo y la otra mitad por encima. Es el "centro" de tu distribución.
        
        **4️⃣ Q3 (Tercer Cuartil - Percentil 75):** El valor que deja el **75% de los datos por debajo**. 
        Si estás en Q3, estás en el **top 25%** (cuarto superior).
        
        **5️⃣ Máximo:** El estudiante con la mejor nota, el empleado mejor pagado, la temperatura más alta.
        
        **📏 IQR (Rango Intercuartílico):** La "amplitud" del **50% central** de tus datos. 
        Es Q3 - Q1. Mide qué tan disperso está el "corazón" de tu distribución.
        """)
    
    # ==========================================
    # TAB 2: CONSTRUCCIÓN PASO A PASO
    # ==========================================
    with tabs[1]:
        st.markdown("## 🔨 Construcción del Boxplot: Paso a Paso")
        
        st.markdown("""
        Vamos a construir un boxplot desde cero, paso por paso, para que entiendas 
        exactamente qué representa cada elemento.
        """)
        
        # Usar una muestra pequeña para mejor visualización
        datos_normales = [
            31.9, 38.2, 41.7, 44.1, 45.9,
            47.3, 48.9, 49.5, 50.0, 50.4,
            51.2, 52.0, 52.8, 53.6, 54.3,
            55.1, 56.0, 57.4, 58.6, 59.8,
            42.9, 46.5, 48.1, 51.8, 53.2,
            55.7, 60.4, 69.7, 35.9, 39.6
        ]        
        outliers = np.array([80.4])
        datos_demo = np.concatenate([datos_normales, outliers])
        datos_demo_sorted = np.sort(datos_demo)
        med_demo = calcular_medidas(datos_demo_sorted)
        
        st.markdown("### 📊 Nuestros Datos de Ejemplo")
        st.write(f"**{len(datos_demo)} valores:** {datos_demo_sorted[:10]}... (mostrando primeros 10)")
        
        # Paso 1
        st.markdown("---")
        st.markdown("### Paso 1️⃣: Ordenar los Datos")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            **¿Por qué?** Porque necesitamos encontrar la **mediana** (el del medio) 
            y los **cuartiles** (que dividen en cuartos).
            
            Ordenamos de menor a mayor:
            """)
            st.code(f"{datos_demo_sorted}")
        
        with col2:
            fig_paso1 = go.Figure()
            fig_paso1.add_trace(go.Scatter(
                x=list(range(len(datos_demo_sorted))),
                y=datos_demo_sorted,
                mode='markers+lines',
                marker=dict(size=8, color='lightblue'),
                line=dict(color='lightgray', width=1)
            ))
            fig_paso1.update_layout(title="Datos Ordenados", height=300,
                                   xaxis_title="Posición", yaxis_title="Valor")
            st.plotly_chart(fig_paso1, use_container_width=True)
        
        # Paso 2
        st.markdown("---")
        st.markdown("### Paso 2️⃣: Encontrar la Mediana (Q2)")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"""
            La **mediana** es el valor del medio. Con {len(datos_demo)} datos:
            
            - Posición central: {len(datos_demo)//2 + 1}
            - **Mediana = {med_demo['mediana']:.2f}**
            
            Esto divide los datos en **dos mitades iguales**: 
            {len(datos_demo)//2} datos a la izquierda, {len(datos_demo)//2} a la derecha.
            """)
        
        with col2:
            fig_paso2 = go.Figure()
            fig_paso2.add_trace(go.Scatter(
                x=list(range(len(datos_demo_sorted))),
                y=datos_demo_sorted,
                mode='markers',
                marker=dict(size=8, color='lightblue')
            ))
            fig_paso2.add_hline(y=med_demo['mediana'], line_color="red", line_width=3,
                               annotation_text="MEDIANA")
            fig_paso2.update_layout(title="Ubicación de la Mediana", height=300)
            st.plotly_chart(fig_paso2, use_container_width=True)
        
        # Paso 3
        st.markdown("---")
        st.markdown("### Paso 3️⃣: Encontrar Q1 y Q3")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"""
            Ahora dividimos **cada mitad** en dos partes más:
            
            **Q1 (Primer Cuartil):**
            - Mediana de la **mitad inferior**
            - **Q1 = {med_demo['q1']:.1f}**
            - Deja el 25% de datos por debajo
            
            **Q3 (Tercer Cuartil):**
            - Mediana de la **mitad superior**
            - **Q3 = {med_demo['q3']:.1f}**
            - Deja el 75% de datos por debajo
            
            **IQR = Q3 - Q1 = {med_demo['iqr']:.1f}**
            """)
        
        with col2:
            fig_paso3 = go.Figure()
            fig_paso3.add_trace(go.Scatter(
                x=list(range(len(datos_demo_sorted))),
                y=datos_demo_sorted,
                mode='markers',
                marker=dict(size=8, color='lightblue')
            ))
            fig_paso3.add_hline(y=med_demo['q1'], line_color="orange", line_dash="dash",
                               annotation_text="Q1 (25%)")
            fig_paso3.add_hline(y=med_demo['mediana'], line_color="red", line_width=3,
                               annotation_text="Mediana (50%)")
            fig_paso3.add_hline(y=med_demo['q3'], line_color="orange", line_dash="dash",
                               annotation_text="Q3 (75%)")
            
            # Sombrear el IQR
            fig_paso3.add_hrect(y0=med_demo['q1'], y1=med_demo['q3'],
                               fillcolor="yellow", opacity=0.2,
                               annotation_text="IQR (50% central)", annotation_position="top left")
            
            fig_paso3.update_layout(title="Cuartiles: Q1, Q2, Q3", height=300)
            st.plotly_chart(fig_paso3, use_container_width=True)
        
        st.info("""
        **🎯 Interpretación:**
        
        Ahora sabemos que:
        - 25% de los datos están por debajo de Q1
        - 25% están entre Q1 y la mediana
        - 25% están entre la mediana y Q3
        - 25% están por encima de Q3
        
        ¡Los cuartiles dividen los datos en **4 partes iguales**!
        """)
        
        # Paso 4
        st.markdown("---")
        st.markdown("### Paso 4️⃣: Dibujar la Caja (Box)")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            La **caja** es un rectángulo que va:
            - **Desde Q1 (abajo)**
            - **Hasta Q3 (arriba)**
            
            Dentro de la caja dibujamos una **línea** en la mediana.
            
            **La caja contiene el 50% central de los datos.**
            
            Si la caja es:
            - **Pequeña** → Datos concentrados (poca dispersión)
            - **Grande** → Datos dispersos (mucha variabilidad)
            """)
        
        with col2:
            fig_paso4 = go.Figure()
            
            # La caja
            fig_paso4.add_trace(go.Box(
                y=datos_demo_sorted,
                name='',
                boxmean=False,
                marker_color='lightblue',
                line=dict(color='darkblue', width=2)
            ))
            
            fig_paso4.update_layout(
                title="La Caja (Box)",
                yaxis_title="Valores",
                height=400,
                showlegend=False
            )
            
            # Anotaciones
            fig_paso4.add_annotation(x=0.35, y=med_demo['q3'], text="← Q3 (borde superior)",
                                    showarrow=False, font=dict(size=12, color="darkblue"))
            fig_paso4.add_annotation(x=0.35, y=med_demo['mediana'], text="← Mediana (línea central)",
                                    showarrow=False, font=dict(size=12, color="red"))
            fig_paso4.add_annotation(x=0.35, y=med_demo['q1'], text="← Q1 (borde inferior)",
                                    showarrow=False, font=dict(size=12, color="darkblue"))
            
            st.plotly_chart(fig_paso4, use_container_width=True)
        
        # Paso 5
        st.markdown("---")
        st.markdown("### Paso 5️⃣: Agregar los Bigotes (Whiskers)")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"""
            Los **bigotes** son líneas que se extienden desde la caja hacia los extremos.
            
            **Regla estándar:**
            - **Bigote inferior:** Hasta el dato más pequeño que esté dentro de 
              `Q1 - 1.5 × IQR`
            - **Bigote superior:** Hasta el dato más grande que esté dentro de 
              `Q3 + 1.5 × IQR`
            
            **Para nuestros datos:**
            - Límite inferior: Q1 - (1.5 × IQR) = {med_demo['q1']:.2f} - (1.5 × {med_demo['iqr']:.2f}) = {med_demo['q1'] - 1.5*med_demo['iqr']:.2f}
            - Límite superior: Q3 + (1.5 × IQR) = {med_demo['q3']:.2f} + (1.5 × {med_demo['iqr']:.2f}) = {med_demo['q3'] + 1.5*med_demo['iqr']:.2f}
            
            Los bigotes muestran el **rango "normal"** de los datos.
            """)
        
        with col2:
            fig_paso5 = go.Figure()
            
            fig_paso5.add_trace(go.Box(
                y=datos_demo_sorted,
                name='',
                boxmean=False,
                marker_color='lightblue',
                line=dict(color='darkblue', width=2)
            ))
            
            # Calcular límites
            lim_inf = med_demo['q1'] - 1.5 * med_demo['iqr']
            lim_sup = med_demo['q3'] + 1.5 * med_demo['iqr']
            
            fig_paso5.add_annotation(x=0.3, y=lim_sup, text="← Límite superior (Q3 + 1.5×IQR)",
                                    showarrow=False, font=dict(size=10, color="green"))
            fig_paso5.add_annotation(x=0.3, y=lim_inf, text="← Límite inferior (Q1 - 1.5×IQR)",
                                    showarrow=False, font=dict(size=10, color="green"))
            
            fig_paso5.update_layout(
                title="Caja con Bigotes",
                yaxis_title="Valores",
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig_paso5, use_container_width=True)
        
        # Paso 6
        st.markdown("---")
        st.markdown("### Paso 6️⃣: Marcar los Outliers (Valores Atípicos)")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            lim_inf = med_demo['q1'] - 1.5 * med_demo['iqr']
            lim_sup = med_demo['q3'] + 1.5 * med_demo['iqr']
            outliers_demo = datos_demo[(datos_demo < lim_inf) | (datos_demo > lim_sup)]
            
            st.markdown(f"""
            Cualquier dato **fuera de los bigotes** se considera un **outlier** 
            (valor atípico o extremo).
            
            **Outliers detectados:** {1}
            
            {f"**Valores:** {80.4}" if len(outliers_demo) > 0 else "**No hay outliers en este dataset**"}
            
            Los outliers se marcan como **puntos individuales** más allá de los bigotes.
            
            **⚠️ Importante:** Un outlier no es necesariamente un "error". 
            Puede ser un dato real pero inusual (por ejemplo, un empleado que gana 
            mucho más que los demás, o un día con clima extremo).
            """)
        
        with col2:
            fig_paso6 = crear_boxplot(datos_demo, "Boxplot Completo con Outliers")
            st.plotly_chart(fig_paso6, use_container_width=True)
        
        st.success("""
        ### 🎉 ¡Boxplot Completo!
        
        Ahora tienes un gráfico que resume:
        - **Tendencia central:** Mediana (línea en la caja)
        - **Dispersión:** Tamaño de la caja (IQR) y bigotes
        - **Forma:** Simetría de la caja y bigotes
        - **Valores extremos:** Outliers (puntos individuales)
        
        **Todo en una sola imagen.**
        """)
    
    # ==========================================
    # TAB 3: ANATOMÍA COMPLETA
    # ==========================================
    with tabs[2]:
        st.markdown("## 🎨 Anatomía Completa del Boxplot")
        
        st.markdown("""
        Ahora que sabes cómo se construye, veamos **en detalle** cada componente 
        y qué te dice sobre tus datos.
        """)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig_anatomia = crear_boxplot(data, "Anatomía del Boxplot")
            st.plotly_chart(fig_anatomia, use_container_width=True)
        
        with col2:
            st.markdown("### 🔍 Elementos:")
            
            st.markdown(f"""
            **🟦 LA CAJA (Box):**
            - Va de Q1 a Q3
            - Contiene el 50% central
            - Altura = IQR = {medidas['iqr']:.2f}
            
            **LÍNEA Central (dentro):**
            - Es la **mediana**
            - Valor: {medidas['mediana']:.2f}
            
            **📏 BIGOTES (Whiskers):**
            - Extienden hasta ±1.5×IQR
            - Muestran rango "normal"
            
            **PUNTOS (si hay):**
            - Son **outliers**
            - Fuera del rango "normal"
            """)
        
        st.markdown("---")
        
        st.markdown("### 📖 Guía de Interpretación Visual")
        
        # Crear ejemplos visuales de diferentes situaciones
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🎯 Mediana Centrada")
            
            # Simétrico
            datos_sim_ej = np.random.normal(50, 10, 100)
            fig_sim_ej = crear_boxplot(datos_sim_ej, "Simétrico")
            st.plotly_chart(fig_sim_ej, use_container_width=True)
            
            st.info("""
            **Mediana en el centro de la caja**
            
            ✅ Distribución **simétrica**
            
            Los datos están balanceados:
            - 25% entre Q1 y mediana
            - 25% entre mediana y Q3
            
            Ambas mitades son iguales.
            """)
        
        with col2:
            st.markdown("#### ➡️ Mediana Abajo")
            
            # Asimétrica derecha
            datos_der_ej = np.random.gamma(2, 10, 100)
            fig_der_ej = crear_boxplot(datos_der_ej, "Asimétrica Derecha")
            st.plotly_chart(fig_der_ej, use_container_width=True)
            
            st.warning("""
            **Mediana cerca de Q1**
            
            ⚠️ **Asimétrica a la derecha**
            
            Más datos concentrados abajo, 
            pocos valores muy altos.
            
            La parte superior de la caja 
            es más grande que la inferior.
            
            Ejemplo: Salarios
            """)
        
        with col3:
            st.markdown("#### ⬅️ Mediana Arriba")
            
            # Asimétrica izquierda
            datos_izq_ej = 100 - np.random.gamma(2, 5, 100)
            datos_izq_ej = datos_izq_ej[datos_izq_ej > 0]
            fig_izq_ej = crear_boxplot(datos_izq_ej, "Asimétrica Izquierda")
            st.plotly_chart(fig_izq_ej, use_container_width=True)
            
            st.warning("""
            **Mediana cerca de Q3**
            
            ⚠️ **Asimétrica a la izquierda**
            
            Más datos concentrados arriba,
            pocos valores muy bajos.
            
            La parte inferior de la caja
            es más grande que la superior.
            
            Ejemplo: Examen fácil
            """)
        
        st.markdown("---")
        
        st.markdown("### 🎓 Preguntas que Responde el Boxplot")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 1️⃣ ¿Dónde está el centro?
            → **Mira la mediana** (línea roja)
            
            #### 2️⃣ ¿Qué tan dispersos están los datos?
            → **Mira el tamaño de la caja** (IQR) y los bigotes
            - Caja pequeña = Datos concentrados
            - Caja grande = Datos dispersos
            
            #### 3️⃣ ¿Hay valores extremos?
            → **Mira si hay puntos** fuera de los bigotes
            - Sin puntos = No hay outliers
            - Con puntos = Hay valores atípicos
            """)
        
        with col2:
            st.markdown("""
            #### 4️⃣ ¿Es simétrica la distribución?
            → **Compara las mitades de la caja**
            - Mediana centrada + bigotes iguales = Simétrica
            - Mediana descentrada = Asimétrica
            
            #### 5️⃣ ¿Dónde está la mayoría de los datos?
            → **Dentro de la caja** (50% central)
            
            #### 6️⃣ ¿En qué rango "normal" están?
            → **Entre los extremos de los bigotes** (aprox. 95%)
            """)
    
    # ==========================================
    # TAB 4: OUTLIERS
    # ==========================================
    with tabs[3]:
        st.markdown("## ⚠️ Valores Atípicos (Outliers): Todo lo que Necesitas Saber")
        
        st.markdown("""
        Los **outliers** son valores que están "muy lejos" del resto de los datos.
        El boxplot los identifica automáticamente usando una regla matemática.
        """)
        
        # Calcular outliers del dataset actual
        limite_inferior = medidas['q1'] - 1.5 * medidas['iqr']
        limite_superior = medidas['q3'] + 1.5 * medidas['iqr']
        outliers_actuales = data[(data < limite_inferior) | (data > limite_superior)]
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 🔍 Detección de Outliers")
            
            st.markdown(f"""
            **Regla del Boxplot:**
            
            Un dato es outlier si está:
            - **Por debajo de:** Q1 - 1.5 × IQR
            - **Por encima de:** Q3 + 1.5 × IQR
            
            **Para tus datos:**
            - Q1 = {medidas['q1']:.2f}
            - Q3 = {medidas['q3']:.2f}
            - IQR = {medidas['iqr']:.2f}
            
            **Límites:**
            - Inferior: {medidas['q1']:.2f} - 1.5×{medidas['iqr']:.2f} = **{limite_inferior:.2f}**
            - Superior: {medidas['q3']:.2f} + 1.5×{medidas['iqr']:.2f} = **{limite_superior:.2f}**
            """)
            
            st.markdown("---")
            
            if len(outliers_actuales) > 0:
                st.warning(f"""
                **⚠️ Outliers Detectados: {len(outliers_actuales)}**
                
                Valores: {np.round(outliers_actuales.tolist(),2)}
                
                Estos datos están fuera del rango "normal" de [{limite_inferior:.2f}, {limite_superior:.2f}]
                """)
            else:
                st.success("""
                **✅ No hay outliers detectados**
                
                Todos los datos están dentro del rango "normal".
                """)
        
        with col2:
            fig_outliers = crear_boxplot(data, "Outliers Marcados")
            st.plotly_chart(fig_outliers, use_container_width=True)
        
        st.markdown("---")
        
        st.markdown("### 🤔 ¿Por Qué 1.5 × IQR?")
        
        st.info("""
        La regla de **1.5 × IQR** es una convención estadística establecida por John Tukey.
        
        **Razones:**
        1. **Balance:** No es ni muy estricta (pocos outliers) ni muy laxa (muchos outliers)
        2. **Estadística:** En una distribución normal, aproximadamente el **99.3%** de los datos 
           cae dentro de este rango
        3. **Práctica:** Funciona bien para detectar valores "genuinamente" raros en la mayoría de situaciones
        
        **Si cambiaras la regla:**
        - **1 × IQR:** Demasiados outliers (demasiado estricto)
        - **2 × IQR:** Muy pocos outliers (demasiado laxo)
        - **1.5 × IQR:** ✅ Punto dulce (el estándar)
        """)
        


# === LABORATORIO ===
elif page == "🎮 Laboratorio":
    st.header("🎮 Laboratorio Interactivo")
    
    st.markdown("### 🔬 Experimenta con tus Datos")
    
    tab1, tab2, tab3 = st.tabs(["📊 Resumen Completo", "🎲 Simulador", "⚖️ Comparador"])
    
    with tab1:
        st.markdown("### 📊 Resumen Estadístico Completo")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**📍 Tendencia Central**")
            st.metric("Media", f"{medidas['media']:.2f}")
            st.metric("Mediana", f"{medidas['mediana']:.2f}")
            st.metric("Moda", f"{medidas['moda']:.2f}" if medidas['moda'] else "N/A")
        
        with col2:
            st.markdown("**📏 Dispersión**")
            st.metric("Rango", f"{medidas['rango']:.2f}")
            st.metric("Desv. Est.", f"{medidas['desv_std']:.2f}")
            st.metric("CV", f"{medidas['cv']:.2f}%")
        
        with col3:
            st.markdown("**📊 Posición y Forma**")
            st.metric("IQR", f"{medidas['iqr']:.2f}")
            st.metric("Asimetría", f"{medidas['asimetria']:.3f}")
            st.metric("Curtosis", f"{medidas['curtosis']:.3f}")
        
        st.markdown("---")
        
        # Tabla completa
        df_resumen = pd.DataFrame({
            'Medida': ['N', 'Media', 'Mediana', 'Moda', 'Desv.Est', 'Varianza', 
                      'Mínimo', 'Q1', 'Q2', 'Q3', 'Máximo', 'Rango', 'IQR', 
                      'CV (%)', 'Asimetría', 'Curtosis'],
            'Valor': [
                medidas['n'], medidas['media'], medidas['mediana'], 
                medidas['moda'] if medidas['moda'] else np.nan,
                medidas['desv_std'], medidas['varianza'], medidas['minimo'],
                medidas['q1'], medidas['q2'], medidas['q3'], medidas['maximo'],
                medidas['rango'], medidas['iqr'], medidas['cv'],
                medidas['asimetria'], medidas['curtosis']
            ]
        })
        
               
        # Visualizaciones
        col1, col2 = st.columns(2)
        
        with col1:
            fig_hist = crear_histograma_con_medidas(data, medidas)
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            fig_box = crear_boxplot(data)
            st.plotly_chart(fig_box, use_container_width=True)

        st.dataframe(df_resumen.style.format({'Valor': '{:.2f}'}, na_rep='N/A'), 
                    use_container_width=True, hide_index=True)
    
    with tab2:
        st.markdown("### 🎲 Simulador de Distribuciones")

        n_datos = st.slider("Cantidad de datos:", 50, 500, 100)
        media_sim = st.slider("Media:", 0, 100, 50)
        std_sim = st.slider("Desv. Est.:", 1, 30, 10)

        datos_sim = np.random.normal(media_sim, std_sim, n_datos)

        medidas_sim = calcular_medidas(datos_sim)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Media", f"{medidas_sim['media']:.2f}")
        col2.metric("Mediana", f"{medidas_sim['mediana']:.2f}")
        col3.metric("Desv. Est.", f"{medidas_sim['desv_std']:.2f}")
        col4.metric("Asimetría", f"{medidas_sim['asimetria']:.3f}")

        fig_sim = crear_histograma_con_medidas(datos_sim, medidas_sim)

        # 🔒 FIJAR EJES PARA COMPARAR CAMBIOS
        fig_sim.update_layout(
            xaxis=dict(range=[0, 100]),        # ajusta si lo deseas
            yaxis=dict(range=[0, 120]),    # escala estable
            bargap=0.05
        )

        st.plotly_chart(fig_sim, use_container_width=True)
    
    with tab3:
        st.markdown("### ⚖️ Comparador de Datasets")
        
        datasets = load_datasets()
        
        col1, col2 = st.columns(2)
        
        with col1:
            dataset1 = st.selectbox("Dataset 1:", list(datasets.keys()), index=0)
            data1 = datasets[dataset1]['data']
            med1 = calcular_medidas(data1)
            
            st.metric("Media", f"{med1['media']:.2f}")
            st.metric("Desv.Est", f"{med1['desv_std']:.2f}")
            st.metric("CV", f"{med1['cv']:.2f}%")
        
        with col2:
            dataset2 = st.selectbox("Dataset 2:", list(datasets.keys()), index=1)
            data2 = datasets[dataset2]['data']
            med2 = calcular_medidas(data2)
            
            st.metric("Media", f"{med2['media']:.2f}")
            st.metric("Desv.Est", f"{med2['desv_std']:.2f}")
            st.metric("CV", f"{med2['cv']:.2f}%")
        
        # Comparación visual
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Box(y=data1, name=dataset1.split('(')[0]))
        fig_comp.add_trace(go.Box(y=data2, name=dataset2.split('(')[0]))
        fig_comp.update_layout(title="Comparación", height=400)
        st.plotly_chart(fig_comp, use_container_width=True)
        
        # Análisis
        st.markdown("### 📊 Análisis Comparativo")
        
        if med1['cv'] > med2['cv']:
            st.info(f"{dataset1} tiene **mayor variabilidad relativa** ({med1['cv']:.1f}% vs {med2['cv']:.1f}%)")
        else:
            st.info(f"{dataset2} tiene **mayor variabilidad relativa** ({med2['cv']:.1f}% vs {med1['cv']:.1f}%)")

# === REEMPLAZO PARA CASOS REALES Y CUESTIONARIO ===
# Reemplaza estas secciones en la Parte 2

# === CASOS REALES (VERSIÓN MEJORADA) ===
elif page == "📈 Casos Reales":
    st.header("📈 Casos de Estudio: Piensa Como un Estadístico")
    
    casos = {
        "🏀 Caso 1: ¿Soy más alto que el promedio?": {
            "contexto": """
            La estatura promedio mundial de adultos es **170 cm** con una desviación estándar de **10 cm**.
            La distribución es aproximadamente normal.
            
            Tu mides **175 cm**.
            """,
            "preguntas": [
                {
                    "q": "¿Estás por encima del promedio mundial?",
                    "opts": ["Sí", "No", "Estoy en el promedio exacto"],
                    "resp": "Sí",
                    "expl": "175 cm > 170 cm (media), por lo tanto estás por encima del promedio."
                },
                {
                    "q": "¿A cuántas desviaciones estándar de la media estás?",
                    "opts": ["0.5σ", "1σ", "1.5σ", "2σ"],
                    "resp": "0.5σ",
                    "expl": "Z = (175-170)/10 = 0.5. Estás medio σ por encima de la media."
                },
                {
                    "q": "Si una persona mide 150 cm, ¿cuántas desviaciones estándar está de la media?",
                    "opts": ["-1σ", "-2σ", "-1.5σ", "-0.5σ"],
                    "resp": "-2σ",
                    "expl": "Z = (150-170)/10 = -2. Está 2 desviaciones por debajo (percentil ~2.5)."
                }
            ]
        },
        
        "💰 Caso 2: El Dilema de los Salarios": {
            "contexto": """
            Una startup tecnológica tiene 20 empleados:
            - 15 empleados junior: $2,000/mes cada uno
            - 4 empleados senior: $5,000/mes cada uno
            - 1 CEO: $30,000/mes
            
            La empresa va a contratar y publica: "Salario promedio: $4,000/mes"
            """,
            "preguntas": [
                {
                    "q": "Calcula la media real de los salarios. ¿Es correcta la publicidad?",
                    "opts": ["Sí, es exactamente $4,000", "No, es mayor a $4,000", "No, es menor a $4,000"],
                    "resp": "Sí, es exactamente $4,000",
                    "expl": "Media = (15×2000 + 4×5000 + 1×30000)/20 = 80000/20 = $4,000. ¡Es correcta! Pero no refleja la realidad de los trabajadores comunes"
                },
                {
                    "q": "¿Cuál es la mediana de los salarios?",
                    "opts": ["$2,000", "$3,500", "$4,000", "$5,000"],
                    "resp": "$2,000",
                    "expl": "Al calcular la mediana, el resultado obtenido es de 2.000"
                },
                {
                    "q": "Si eres un nuevo empleado junior, ¿cuál medida representa mejor tu salario esperado?",
                    "opts": ["Media ($4,000)", "Mediana ($2,000)", "Moda ($2,000)", "CEO ($30,000)"],
                    "resp": "Mediana ($2,000)",
                    "expl": "La mediana (2,000) o moda (2,000) representan mejor lo que ganaría la mayoría. La media está inflada por el CEO."
                },
                {
                    "q": "¿Qué porcentaje de empleados gana MENOS que el 'salario promedio' de $4,000?",
                    "opts": ["25%", "50%", "75%", "95%"],
                    "resp": "75%",
                    "expl": "15 de 20 empleados (75%) ganan 2,000, que es menos que la media de 4,000."
                },
                {
                    "q": "Esta distribución de salarios es:",
                    "opts": ["Simétrica", "Asimétrica a la derecha", "Asimétrica a la izquierda", "Uniforme"],
                    "resp": "Asimétrica a la derecha",
                    "expl": "Media (4,000) > Mediana (2,000), indicando asimetría positiva (cola larga hacia valores altos)."
                }
            ]
        },
        
        "🎓 Caso 3: El Examen Imposible": {
            "contexto": """
            Un profesor aplicó un examen. Los resultados fueron:
            - Media: 45 puntos (sobre 100)
            - Mediana: 42 puntos
            - Desviación estándar: 15 puntos
            - Q1: 35 puntos
            - Q3: 55 puntos
            
            Tú sacaste 70 puntos.
            """,
            "preguntas": [
                {
                    "q": "¿Reprobaste o aprobaste según la distribución del grupo?",
                    "opts": ["Reprobé", "Aprobé, pero estoy abajo del promedio", "Aprobé y estoy sobre el promedio", "No se puede determinar"],
                    "resp": "Aprobé y estoy sobre el promedio",
                    "expl": "70 > 45 (media). Estás significativamente por encima del grupo. Nota: el examen fue muy difícil para todos."
                },
                {
                    "q": "Aproximadamente, ¿en qué percentil es mas probable que te encuentres?",
                    "opts": ["P50", "P75", "P90", "P25"],
                    "resp": "P90",
                    "expl": "Por descarte, es imposible que te encuentres en los percentiles 25, 50 o 75 dada la informacion suministrada"
                },
                {
                    "q": "¿Qué porcentaje de estudiantes sacó entre 35 y 55 puntos?",
                    "opts": ["25%", "50%", "75%", "100%"],
                    "resp": "50%",
                    "expl": "Entre Q1 y Q3 siempre está el 50% central de los datos (definición del IQR)."
                },
                {
                    "q": "Si el profesor decide 'curvar' sumando 20 puntos a todos, ¿qué pasa con la desviación estándar?",
                    "opts": ["Aumenta a 35", "Se mantiene en 15", "Disminuye", "Se duplica"],
                    "resp": "Se mantiene en 15",
                    "expl": "Sumar una constante cambia la media pero NO cambia la dispersión (desviación estándar)."
                },
                {
                    "q": "¿Cuál es el IQR del examen?",
                    "opts": ["15", "20", "35", "55"],
                    "resp": "20",
                    "expl": "IQR = Q3 - Q1 = 55 - 35 = 20 puntos."
                }
            ]
        },
        
        "🏃 Caso 4: Maratón vs Sprint": {
            "contexto": """
            Tiempos en una carrera de 100m (en segundos):
            **Grupo A (velocistas):** 10.5, 10.8, 11.0, 11.2, 11.5, 12.0
            **Grupo B (aficionados):** 14.0, 15.5, 16.0, 17.0, 18.5, 25.0
            """,
            "preguntas": [
                {
                    "q": "¿Qué grupo tiene menor tiempo promedio?",
                    "opts": ["Grupo A", "Grupo B", "Iguales"],
                    "resp": "Grupo A",
                    "expl": "Media A ≈ 11.17s, Media B ≈ 17.67s. Grupo A es más rápido."
                },
                {
                    "q": "¿Qué grupo es más consistente (menos variabilidad)?",
                    "opts": ["Grupo A", "Grupo B", "Igual variabilidad"],
                    "resp": "Grupo A",
                    "expl": "Rango A = 1.5s, Rango B = 11s. La desviación estándar de A es mucho menor. Grupo A es más homogéneo."
                },
                {
                    "q": "En el Grupo B, el tiempo de 25s es probablemente:",
                    "opts": ["Normal", "Un outlier", "La mediana", "El Q1"],
                    "resp": "Un outlier",
                    "expl": "25s está muy alejado del resto (14-18.5s). Es un valor atípico que aumenta la media y dispersión."
                },
                {
                    "q": "Si comparas usando Coeficiente de Variación, ¿qué esperas?",
                    "opts": ["CV(A) > CV(B)", "CV(A) < CV(B)", "CV(A) = CV(B)"],
                    "resp": "CV(A) < CV(B)",
                    "expl": "Aunque ambos tienen poca dispersión absoluta, B tiene mayor variabilidad relativa por el outlier de 25s."
                },
                {
                    "q": "Si quieres representar el 'tiempo típico' del Grupo B, ¿qué usas?",
                    "opts": ["Media", "Mediana", "Moda", "Máximo"],
                    "resp": "Mediana",
                    "expl": "Por el outlier de 25s, la mediana (16s aprox) representa mejor el centro sin ser afectada por valores extremos."
                }
            ]
        },
        
        "👁️ Caso 5: ¿Cuántos ojos tengo?": {
            "contexto": """
            La mayoría de las personas tienen **2 ojos**.
            Algunas personas (muy pocas) han perdido un ojo por accidentes o condiciones médicas.
            Prácticamente nadie tiene más de 2 ojos.
            
            Considerando la población mundial de 8 mil millones de personas.
            """,
            "preguntas": [
                {
                    "q": "¿Cuál es la MODA del número de ojos?",
                    "opts": ["0", "1", "2", "No hay moda"],
                    "resp": "2",
                    "expl": "La gran mayoría (>99.9%) tiene 2 ojos. Es el valor más frecuente."
                },
                {
                    "q": "¿Cuál es aproximadamente la MEDIA del número de ojos en la población mundial?",
                    "opts": ["Exactamente 2", "Ligeramente menor que 2", "Ligeramente mayor que 2", "1"],
                    "resp": "Ligeramente menor que 2",
                    "expl": "Aunque casi todos tienen 2, existen personas con 1 o 0 ojos (accidentes, condiciones médicas). Esto baja ligeramente la media, quizás a 1.999..."
                },
                {
                    "q": "¿Es correcto decir que 'tienes más ojos que el promedio mundial'?",
                    "opts": ["No, imposible", "Sí, si tienes 2 ojos", "Solo si tienes 3 ojos", "Depende de tu país"],
                    "resp": "Sí, si tienes 2 ojos",
                    "expl": "¡Sí! Como la media es ligeramente menor que 2 (por casos con <2 ojos), tener 2 ojos te pone por encima del promedio. Paradoja estadística interesante."
                },
                {
                    "q": "Esta distribución es:",
                    "opts": ["Simétrica", "Asimétrica a la izquierda", "Asimétrica a la derecha", "Uniforme"],
                    "resp": "Asimétrica a la izquierda",
                    "expl": "Concentrada en 2, con cola hacia valores bajos (1, 0). Media < Moda, indicando asimetría negativa."
                },
                {
                    "q": "¿Qué medida de tendencia central es MÁS representativa en este caso?",
                    "opts": ["Media", "Moda", "Todas por igual"],
                    "resp": "Moda",
                    "expl": "La moda (2) representa lo que realmente tiene la gran mayoría. La mediana tambien era una posible respuesta correcta, La media está sesgada por casos raros."
                }
            ]
        },
        
        "📱 Caso 6: Adicción al Celular": {
            "contexto": """
            Se midió el tiempo diario de uso de celular (en horas) de 100 estudiantes universitarios:
            - Media: 6.5 horas
            - Mediana: 5.5 horas
            - Q1: 4 horas
            - Q3: 7 horas
            - Máximo: 16 horas
            - Desviación estándar: 2.8 horas
            
            Tú usas tu celular 9 horas al día.
            """,
            "preguntas": [
                {
                    "q": "¿Usas el celular más que el 'estudiante promedio'?",
                    "opts": ["Sí", "No", "Estoy en el promedio"],
                    "resp": "Sí",
                    "expl": "9 horas > 6.5 horas (media). Usas más que el promedio."
                },
                {
                    "q": "¿En qué cuartil aproximadamente te encuentras?",
                    "opts": ["Entre Q1 y Q2", "Entre Q2 y Q3", "Por encima de Q3", "Por debajo de Q1"],
                    "resp": "Por encima de Q3",
                    "expl": "9 horas > 7 horas (Q3). Estás en el 25% superior de uso."
                },
                {
                    "q": "¿A cuántas desviaciones estándar de la media estás?",
                    "opts": ["Menos de 1σ", "Entre 1σ y 2σ", "Más de 2σ", "Exactamente 1σ"],
                    "resp": "Menos de 1σ",
                    "expl": "Z = (9-6.5)/2.8 ≈ 0.89σ. Estás dentro del rango 'normal' según la regla 68-95-99.7."
                },
                {
                    "q": "La persona que usa 16 horas al día es probablemente:",
                    "opts": ["Normal", "Un outlier extremo", "Está en el Q3", "Representa la moda"],
                    "resp": "Un outlier extremo",
                    "expl": "16 horas está a (16-6.5)/2.8 ≈ 3.4σ de la media. Es un valor extremadamente atípico (>99.9% usa menos)."
                },
                {
                    "q": "¿Qué porcentaje aproximado de estudiantes usa el celular menos que tú (9 horas)?",
                    "opts": ["50%", "60%", "75%", "85%"],
                    "resp": "85%",
                    "expl": "Es la unica posible respuesta dado que el tercer cuartil (7 Horas) es menor a 9 horas."
                }
            ]
        }
    }
    
    caso_elegido = st.selectbox("🎯 Elige un caso desafiante:", list(casos.keys()))
    caso = casos[caso_elegido]
    
    st.markdown(f"""
    <div style="background-color: #fff3cd; padding: 20px; border-radius: 10px; border-left: 5px solid #ffc107;">
    <h3>📖 Contexto del Caso</h3>
    {caso["contexto"]}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    puntaje_caso = 0
    
    for i, preg in enumerate(caso["preguntas"], 1):
        st.markdown(f"### 🤔 Pregunta {i}")
        st.markdown(f"**{preg['q']}**")
        
        with st.form(f"caso_{caso_elegido}_{i}"):
            resp_usuario = st.radio("Selecciona tu respuesta:", preg['opts'], key=f"radio_{caso_elegido}_{i}")
            submitted = st.form_submit_button("✅ Verificar Respuesta")
            
            if submitted:
                if resp_usuario == preg['resp']:
                    st.success(f"🎉 ¡Correcto! +1 punto")
                    puntaje_caso += 1
                else:
                    st.error(f"❌ Incorrecto. La respuesta correcta era: **{preg['resp']}**")
                
                st.info(f"**💡 Explicación:** {preg['expl']}")
        
        st.markdown("---")
    

# === CUESTIONARIO (VERSIÓN MEJORADA) ===
elif page == "❓ Cuestionario":
    st.header("❓ Cuestionario Integral: Pon a Prueba tu Comprensión")
    
    st.markdown("""
    Este cuestionario contiene preguntas que requieren **pensamiento crítico** y **aplicación práctica** 
    de los conceptos. No son de memorización, sino de **comprensión profunda**.
    """)
    
    preguntas = [
        {
            "nivel": "🟢 Aplicación",
            "q": "Una empresa reporta que el 'salario promedio' es 5,000 pero la 'mediana salarial' es 3,000. ¿Qué puedes concluir?",
            "opts": [
                "La empresa está mintiendo en sus estadísticas",
                "Hay pocos empleados con salarios muy altos que inflan la media",
                "La mayoría gana más de $5,000",
                "Los datos están mal calculados"
            ],
            "resp": "Hay pocos empleados con salarios muy altos que inflan la media",
            "expl": "Media > Mediana indica asimetría positiva: pocos valores altos (ejecutivos) jalan la media hacia arriba, mientras que la mediana ($3,000) representa mejor lo que gana la mayoría."
        },
        {
            "nivel": "🟡 Análisis",
            "q": "Dos ciudades tienen temperatura media anual de 20°C. Ciudad A tiene σ=2°C, Ciudad B tiene σ=15°C. ¿Qué significa?",
            "opts": [
                "Son idénticas en clima",
                "Ciudad B tiene mejor clima",
                "La media no es confiable",
                "Ciudad A tiene clima más estable/predecible"
            ],
            "resp": "Ciudad A tiene clima más estable/predecible",
            "expl": "Mayor desviación estándar (Ciudad B) significa mayor variabilidad. Ciudad A tiene temperaturas más consistentes cerca de 20°C, mientras B tiene cambios drásticos."
        },
        {
            "nivel": "🔴 Pensamiento Crítico",
            "q": "Un estudiante dice: 'Saqué 70 en el examen, estoy reprobado'. Pero resulta que está en el percentil 85. ¿Qué pasó?",
            "opts": [
                "El estudiante está mal informado, 70 siempre es aprobar",
                "El percentil está mal calculado",
                "El examen fue muy difícil para todos, 70 es un buen puntaje relativo",
                "70 es automáticamente un mal puntaje"
            ],
            "resp": "El examen fue muy difícil para todos, 70 es un buen puntaje relativo",
            "expl": "Estar en P85 significa que superó al 85% del grupo. El puntaje absoluto (70) no importa tanto como la posición relativa. El examen fue difícil para todos."
        },
        {
            "nivel": "🟢 Aplicación",
            "q": "Tienes dos opciones de inversión: A (retorno medio 8%, σ=2%) y B (retorno medio 12%, σ=8%). ¿Cuál es menos riesgosa?",
            "opts": [
                "A, porque tiene menor desviación estándar",
                "B, porque tiene mayor retorno",
                "Son igual de riesgosas",
                "No se puede determinar sin más datos"
            ],
            "resp": "A, porque tiene menor desviación estándar",
            "expl": "La desviación estándar mide riesgo/volatilidad. A tiene σ=2% (muy estable), B tiene σ=8% (muy volátil). A es menos riesgosa aunque tenga menor retorno."
        },
        {
            "nivel": "🟡 Análisis",
            "q": "En un boxplot, la 'caja' es muy pequeña pero los bigotes son muy largos. ¿Qué significa?",
            "opts": [
                "Datos muy concentrados en el centro con algunos extremos",
                "Distribución uniforme",
                "Error en los datos",
                "Todos los datos son iguales"
            ],
            "resp": "Datos muy concentrados en el centro con algunos extremos",
            "expl": "Caja pequeña = IQR pequeño = 50% central muy junto. Bigotes largos = hay valores extremos alejados del centro."
        },
        {
            "nivel": "🔴 Pensamiento Crítico",
            "q": "Un político dice: 'El ingreso promedio aumentó 10%'. Un economista responde: 'Pero la mediana solo aumentó 2%'. ¿Qué implica?",
            "opts": [
                "El político miente",
                "El aumento benefició principalmente a los más ricos",
                "El economista está equivocado",
                "Ambos dicen lo mismo"
            ],
            "resp": "El aumento benefició principalmente a los más ricos",
            "expl": "Si media sube mucho (10%) pero mediana poco (2%), significa que los incrementos fueron principalmente en la cola superior (ricos), no en la mayoría de la población."
        },
        {
            "nivel": "🟢 Aplicación",
            "q": "Quieres comparar la variabilidad de estaturas (cm) vs pesos (kg). ¿Qué medida usas?",
            "opts": [
                "Desviación estándar",
                "Varianza",
                "Coeficiente de variación",
                "Rango"
            ],
            "resp": "Coeficiente de variación",
            "expl": "El CV es adimensional (porcentaje), permite comparar variabilidad entre variables con diferentes unidades o escalas."
        },
        {
            "nivel": "🟡 Análisis",
            "q": "Un dataset tiene Media=50, Mediana=50, Moda=50. ¿Qué forma tiene probablemente la distribución?",
            "opts": [
                "Asimétrica a la derecha",
                "Asimétrica a la izquierda",
                "Aproximadamente simétrica",
                "Imposible determinar"
            ],
            "resp": "Aproximadamente simétrica",
            "expl": "Cuando las tres medidas de tendencia central coinciden, indica simetría. La distribución está balanceada alrededor del centro."
        },
        {
            "nivel": "🔴 Pensamiento Crítico",
            "q": "Una app de ejercicio dice: 'Quemaste 500 calorías, más que el 90% de usuarios'. Pero la media es 300 calorías con σ=200. ¿Es creíble?",
            "opts": [
                "Sí, 500 está claramente por encima",
                "No, 500 calorías solo está a una desviacion estandar de la media, no es coherente",
                "La app definitivamente miente",
                "Faltan datos para verificar"
            ],
            "resp": "No, 500 calorías solo está a una desviacion estandar de la media, no es coherente",
            "expl": "Si el valor (500) esta a solo una desviacion estandar de la media, no es posible que este por encima del 90% del resto de usuarios"
        },
        {
            "nivel": "🟢 Aplicación",
            "q": "¿En cuál situación NO deberías usar la media como medida de centro?",
            "opts": [
                "Estaturas de estudiantes universitarios",
                "Ingresos de una población nacional",
                "Temperaturas diarias de un mes",
                "Edad de empleados en una oficina"
            ],
            "resp": "Ingresos de una población nacional",
            "expl": "Los ingresos tienen distribución muy asimétrica con outliers (millonarios). La mediana es más representativa del 'ingreso típico'."
        },
        {
            "nivel": "🟡 Análisis",
            "q": "Tienes dos grupos: A (n=10) con σ=5, y B (n=100) con σ=5. ¿Cuál representa mejor el comportamiento general de los datos?",
            "opts": [
                "A, porque es más fácil de analizar",
                "B, porque tiene más datos y es más representativo",
                "Son igual de confiables porque σ es igual",
                "No se puede determinar"
            ],
            "resp": "B, porque tiene más datos y es más representativo",
            "expl": "Con más datos (n=100 vs n=10), el grupo B captura mejor la variabilidad real y los patrones de la población. Una muestra más grande reduce el efecto de valores atípicos individuales y da una imagen más completa del comportamiento de los datos."
        },
        {
            "nivel": "🔴 Pensamiento Crítico",
            "q": "Una encuesta reporta: 'La satisfacción promedio es 4.2/5'. Pero el boxplot muestra muchos outliers en 1 y 2. ¿Problema?",
            "opts": [
                "No hay problema, 4.2 es alto",
                "Sí, la media está ocultando clientes muy insatisfechos",
                "Los outliers no importan",
                "El boxplot está mal hecho"
            ],
            "resp": "Sí, la media está ocultando clientes muy insatisfechos",
            "expl": "Los outliers bajos (1-2) indican clientes muy insatisfechos. La media de 4.2 puede ser engañosa si hay dos grupos: muchos muy satisfechos y algunos muy insatisfechos (bimodal)."
        },
        {
            "nivel": "🟢 Aplicación",
            "q": "Dos cursos tienen la misma media de notas. ¿Qué medida te permite saber en cuál las notas están más dispersas?",
            "opts": [
                "Media",
                "Moda",
                "Desviación estándar",
                "Mediana"
            ],
            "resp": "Desviación estándar",
            "expl": "La desviación estándar mide qué tan separados están los datos respecto a la media, permitiendo comparar la dispersión entre grupos."
        },
        {
            "nivel": "🟡 Análisis",
            "q": "Un dataset tiene IQR=10 y Rango=100. ¿Qué sugiere?",
            "opts": [ "Distribución muy concentrada",
                "Presencia significativa de outliers",
                "Datos uniformes",
                "Error en el cálculo"
            ],
            "resp": "Presencia significativa de outliers",
            "expl": "IQR pequeño (10) vs Rango grande (100) indica que el 50% central está muy junto, pero hay valores extremos muy alejados (outliers)."
        },
        {
            "nivel": "🔴 Pensamiento Crítico",
            "q": "Dos profesores: A curva sumando 10 puntos a todos. B multiplica todas las notas por 1.2. ¿Cuál aumenta más la desviación estándar?",
            "opts": [
                "A aumenta más σ",
                "B aumenta más σ",
                "Ambos aumentan σ igual",
                "Ninguno cambia σ"
            ],
            "resp": "B aumenta más σ",
            "expl": "Sumar constante NO cambia σ. Multiplicar por constante SÍ: nueva σ = 1.2 × σ original. Solo B aumenta la dispersión."
        },
        {
            "nivel": "🟢 Aplicación",
            "q": "Estás en P75 de ingresos. Si tu ingreso aumenta 50%, ¿necesariamente subes de percentil?",
            "opts": [
                "Sí, definitivamente",
                "No, depende de qué le pase a los demás",
                "Solo si nadie más sube",
                "Los percentiles no cambian"
            ],
            "resp": "No, depende de qué le pase a los demás",
            "expl": "Los percentiles son RELATIVOS. Si todos aumentan 50%, tu percentil se mantiene. Solo subes si aumentas MÁS que los que están arriba de ti."
        }
    ]
    
    # Organizar por nivel
    st.markdown("### 📊 Distribución de Preguntas")
    col1, col2, col3 = st.columns(3)
    col1.metric("🟢 Aplicación", len([p for p in preguntas if "🟢" in p["nivel"]]))
    col2.metric("🟡 Análisis", len([p for p in preguntas if "🟡" in p["nivel"]]))
    col3.metric("🔴 Pensamiento", len([p for p in preguntas if "🔴" in p["nivel"]]))
    
    st.markdown("---")
    
    if 'quiz_respuestas' not in st.session_state:
        st.session_state['quiz_respuestas'] = {}
    
    for i, p in enumerate(preguntas, 1):
        st.markdown(f"### {p['nivel']} - Pregunta {i}")
        st.markdown(f"**{p['q']}**")
        
        with st.form(f"quiz_final_{i}"):
            resp = st.radio("Tu respuesta:", p['opts'], key=f"qf_{i}")
            submitted = st.form_submit_button("✅ Verificar")
            
            if submitted:
                st.session_state['quiz_respuestas'][i] = (resp == p['resp'])
                
                if resp == p['resp']:
                    st.success("🎉 ¡Correcto!")
                else:
                    st.error(f"❌ Incorrecto. Respuesta: **{p['resp']}**")
                
                st.info(f"**💡 Explicación:** {p['expl']}")
        
        st.markdown("---")
    
    # Resumen final
    if len(st.session_state['quiz_respuestas']) > 0:
        st.markdown("## 📈 Tu Desempeño")
        
        correctas = sum(st.session_state['quiz_respuestas'].values())
        total = len(st.session_state['quiz_respuestas'])
        porcentaje = (correctas / total) * 100
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Correctas", f"{correctas}/{total}")
        col2.metric("Porcentaje", f"{porcentaje:.1f}%")
        
        if porcentaje >= 90:
            col3.success("🏆 Excelente")
            st.balloons()
        elif porcentaje >= 70:
            col3.info("👍 Bien")
        elif porcentaje >= 50:
            col3.warning("📚 Regular")
        else:
            col3.error("🔄 Repasa")
        
        if st.button("🔄 Reiniciar Cuestionario"):
            st.session_state['quiz_respuestas'] = {}
            st.rerun()

# === FOOTER ===
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
📧 <strong>Contacto:</strong> carlosdl@uninorte.edu.co<br>
Desarrollado con 💙 para estudiantes de Uninorte 
</div>
""", unsafe_allow_html=True)