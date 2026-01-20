import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import random

# === CONFIGURACIÓN ===
st.set_page_config(page_title="Análisis Bivariado", page_icon="📈", layout="wide")

# === FUNCIONES AUXILIARES ===
def calcular_regresion(x, y):
    """Calcula regresión lineal y métricas"""
    n = len(x)
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    
    # Pendiente (b1)
    numerador = np.sum((x - x_mean) * (y - y_mean))
    denominador = np.sum((x - x_mean)**2)
    b1 = numerador / denominador
    
    # Intercepto (b0)
    b0 = y_mean - b1 * x_mean
    
    # Correlación
    r = np.corrcoef(x, y)[0, 1]
    
    # R²
    r2 = r**2
    
    # Covarianza
    cov = np.cov(x, y)[0, 1]
    
    return {
        'b0': b0,
        'b1': b1,
        'r': r,
        'r2': r2,
        'cov': cov,
        'y_pred': b0 + b1 * x
    }

def crear_dispersion(x, y, titulo, mostrar_linea=False, x_label="X", y_label="Y"):
    """Crea gráfico de dispersión"""
    fig = go.Figure()
    
    # Puntos
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='markers',
        marker=dict(size=10, color='lightblue', line=dict(width=1, color='darkblue')),
        name='Datos',
        hovertemplate=f'{x_label}: %{{x:.2f}}<br>{y_label}: %{{y:.2f}}<extra></extra>'
    ))
    
    # Línea de regresión
    if mostrar_linea:
        reg = calcular_regresion(x, y)
        fig.add_trace(go.Scatter(
            x=x, y=reg['y_pred'],
            mode='lines',
            line=dict(color='red', width=2),
            name=f'Regresión: y = {reg["b0"]:.2f} + {reg["b1"]:.2f}x'
        ))
    
    fig.update_layout(
        title=titulo,
        xaxis_title=x_label,
        yaxis_title=y_label,
        height=400
    )
    
    return fig

@st.cache_data
def load_datasets_bivariados():
    """Carga datasets bivariados de ejemplo"""
    np.random.seed(42)
    
    datasets = {
        "Estudio vs Calificación (Positiva Fuerte)": {
            "x": np.array([2, 3, 4, 5, 6, 7, 8, 9, 10, 11]),
            "y": np.array([55, 60, 65, 70, 75, 80, 85, 88, 92, 95]) + np.random.normal(0, 3, 10),
            "x_label": "Horas de estudio",
            "y_label": "Calificación",
            "descripcion": "Relación positiva fuerte: A más estudio, mejor calificación"
        },
        "Precio vs Demanda (Negativa Fuerte)": {
            "x": np.array([10, 15, 20, 25, 30, 35, 40, 45, 50, 55]),
            "y": np.array([100, 90, 80, 70, 60, 50, 40, 30, 20, 10]) + np.random.normal(0, 5, 10),
            "x_label": "Precio ($)",
            "y_label": "Demanda (unidades)",
            "descripcion": "Relación negativa fuerte: A mayor precio, menor demanda"
        },
        "Edad vs Flexibilidad (Negativa Moderada)": {
            "x": np.array([20, 25, 30, 35, 40, 45, 50, 55, 60, 65]),
            "y": np.array([90, 85, 80, 75, 70, 65, 60, 55, 50, 45]) + np.random.normal(0, 8, 10),
            "x_label": "Edad (años)",
            "y_label": "Flexibilidad (%)",
            "descripcion": "Relación negativa moderada: Con la edad, disminuye la flexibilidad"
        },
        "Peso vs Altura (Positiva Moderada)": {
            "x": np.array([150, 155, 160, 165, 170, 175, 180, 185, 190, 195]),
            "y": np.array([50, 55, 58, 62, 68, 73, 78, 83, 88, 93]) + np.random.normal(0, 5, 10),
            "x_label": "Altura (cm)",
            "y_label": "Peso (kg)",
            "descripcion": "Relación positiva moderada: A mayor altura, mayor peso (generalmente)"
        },
        "Número de Zapato vs Inteligencia (Sin Relación)": {
            "x": np.array([37, 38, 39, 40, 41, 42, 43, 44, 45, 46]),
            "y": np.random.normal(100, 15, 10),
            "x_label": "Número de zapato",
            "y_label": "IQ",
            "descripcion": "Sin relación: El tamaño del zapato NO determina la inteligencia"
        }
    }
    
    return datasets

# === INICIALIZACIÓN ===
if 'ejercicio_actual' not in st.session_state:
    st.session_state['ejercicio_actual'] = None
if 'quiz_respuestas' not in st.session_state:
    st.session_state['quiz_respuestas'] = {}

# === SIDEBAR ===
with st.sidebar:
    st.title("🎯 Navegación")
    
    st.markdown("### 📊 Datos")
    datasets = load_datasets_bivariados()
    dataset_name = st.selectbox("Elige un dataset:", list(datasets.keys()))
    
    data_info = datasets[dataset_name]
    x_data = data_info['x']
    y_data = data_info['y']
    
    st.info(data_info['descripcion'])
    
    st.markdown("---")
    st.markdown("### 📑 Secciones")
    page = st.radio("", [
        "🏠 Inicio",
        "📊 Gráfico de Dispersión",
        "🔗 Covarianza",
        "📈 Correlación",
        "📉 Regresión Lineal",
        "🤔 Correlación Espuria",
        "🎮 Ejercicios",
        "❓ Cuestionario"
    ], label_visibility="collapsed")

st.title("📊 Análisis Bivariado: Relaciones entre Variables")
st.markdown("---")

# Calcular métricas
reg_actual = calcular_regresion(x_data, y_data)

# === INICIO ===
if page == "🏠 Inicio":
    st.header("👋 Bienvenido al Análisis Bivariado")
    
    st.markdown("""
    ### 🎯 ¿Qué es el Análisis Bivariado?
    
    Hasta ahora has analizado **una variable a la vez** (univariado): 
    la edad de los estudiantes, los salarios, las calificaciones...
    
    Pero, ¿qué pasa cuando quieres saber si **dos variables están relacionadas**?
    
    - ¿A mayor estudio, mejor calificación?
    - ¿A mayor precio, menor demanda?
    - ¿El peso depende de la altura?
    - ¿Consumir café causa cáncer? (¡Spoiler: correlación ≠ causación!)
    
    El **análisis bivariado** estudia la **relación entre DOS variables**.
    
    ### 🔍 Lo que Aprenderás
    
    **1. Visualizar relaciones** usando gráficos de dispersión
    - ¿Hay un patrón visual?
    - ¿Es una relación lineal (recta)?
    
    **2. Medir la fuerza de la relación**
    - Covarianza: ¿Se mueven juntas?
    - Correlación: ¿Qué tan fuerte es la relación? (-1 a +1)
    
    **3. Predecir valores**
    - Regresión lineal: La ecuación de la recta
    - Si estudias 5 horas, ¿qué nota esperas?
    
    **4. Evitar trampas**
    - Correlación espuria: Cuando dos cosas parecen relacionadas pero NO lo están
    - ¡El aumento de pedidos de pizza cerca del pentagono no causa intervenciones de EE.UU. a otros paises!, o si? 🍕💣""")

    
    st.markdown("---")

    st.metric("Dataset Actual", dataset_name.split('(')[0].strip())

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Correlación (r)", f"{reg_actual['r']:.3f}")
    with col2:
        st.metric("R² (Bondad de ajuste)", f"{reg_actual['r2']:.3f}")
    
    fig_preview = crear_dispersion(x_data, y_data, "Vista Previa", True,
                                   data_info['x_label'], data_info['y_label'])
    st.plotly_chart(fig_preview, use_container_width=True)

    st.markdown("---")
    
    st.markdown("""
    ### 🚀 Conceptos Clave
    
    | Concepto | Qué Mide | Rango |
    |----------|----------|-------|
    | **Gráfico de Dispersión** | Muestra visualmente la relación | - |
    | **Covarianza** | Si las variables se mueven juntas | -∞ a +∞ |
    | **Correlación (r)** | Fuerza y dirección de la relación lineal | -1 a +1 |
    | **Regresión Lineal** | La ecuación para predecir Y dado X | y = b₀ + b₁x |
    | **R²** | Qué tan bien la línea representa los datos | 0 a 1 (0% a 100%) |
    """)
    
    st.success("👈 **Usa la barra lateral para explorar cada concepto paso a paso**")

# === GRÁFICO DE DISPERSIÓN ===
elif page == "📊 Gráfico de Dispersión":
    st.header("📊 Gráfico de Dispersión: La Primera Mirada")
    
    st.markdown("""
    El **gráfico de dispersión** (scatter plot) es tu primera herramienta para 
    visualizar si dos variables están relacionadas.
    
    ### 🎯 ¿Cómo se Lee?
    
    - **Eje X (horizontal):** Variable independiente (la que "causa" o predice)
    - **Eje Y (vertical):** Variable dependiente (la que "responde" o es predicha)
    - **Cada punto:** Una observación con sus valores (x, y)
    """)
    
    # Gráfico principal
    fig_main = crear_dispersion(x_data, y_data, 
                                f"Relación: {data_info['x_label']} vs {data_info['y_label']}",
                                False,
                                data_info['x_label'], data_info['y_label'])
    st.plotly_chart(fig_main, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("## 🔍 Tipos de Relaciones que Puedes Identificar")
    
    # Crear ejemplos de diferentes tipos
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### ➡️ Positiva Fuerte")
        x_pos = np.linspace(0, 10, 20)
        y_pos = 2*x_pos + np.random.normal(0, 1, 20)
        fig_pos = crear_dispersion(x_pos, y_pos, "r ≈ +0.9", True, "X", "Y")
        st.plotly_chart(fig_pos, use_container_width=True)
        st.info("""
        **Características:**
        - Puntos forman línea ascendente clara
        - A mayor X → mayor Y
        - Ejemplos: Estudio-Calificación, Altura-Peso
        """)
    
    with col2:
        st.markdown("### ⬅️ Negativa Fuerte")
        x_neg = np.linspace(0, 10, 20)
        y_neg = -2*x_neg + 20 + np.random.normal(0, 1, 20)
        fig_neg = crear_dispersion(x_neg, y_neg, "r ≈ -0.9", True, "X", "Y")
        st.plotly_chart(fig_neg, use_container_width=True)
        st.info("""
        **Características:**
        - Puntos forman línea descendente clara
        - A mayor X → menor Y
        - Ejemplos: Precio-Demanda, Edad-Flexibilidad
        """)
    
    with col3:
        st.markdown("### ⭕ Sin Relación")
        x_sin = np.random.uniform(0, 10, 20)
        y_sin = np.random.uniform(0, 10, 20)
        fig_sin = crear_dispersion(x_sin, y_sin, "r ≈ 0", False, "X", "Y")
        st.plotly_chart(fig_sin, use_container_width=True)
        st.info("""
        **Características:**
        - Puntos dispersos sin patrón
        - No hay tendencia clara
        - X no predice Y
        - Ejemplo: Zapato-IQ
        """)
    
    st.markdown("---")
    
    st.markdown("### 🎓 Interpretación del Dataset Actual")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_analisis = crear_dispersion(x_data, y_data,
                                        f"Análisis: {dataset_name}",
                                        True,
                                        data_info['x_label'], data_info['y_label'])
        st.plotly_chart(fig_analisis, use_container_width=True)
    
    with col2:
        r = reg_actual['r']
        
        if r > 0.7:
            st.success("**✅ Relación Positiva Fuerte**")
            st.write(f"r = {r:.3f}")
            st.write(f"Cuando {data_info['x_label']} aumenta, {data_info['y_label']} tiende a aumentar significativamente.")
        elif r > 0.3:
            st.info("**📊 Relación Positiva Moderada**")
            st.write(f"r = {r:.3f}")
            st.write(f"Hay tendencia positiva, pero con más variabilidad.")
        elif r > -0.3:
            st.warning("**⚠️ Relación Débil o Nula**")
            st.write(f"r = {r:.3f}")
            st.write(f"Poca o ninguna relación lineal aparente.")
        elif r > -0.7:
            st.info("**📉 Relación Negativa Moderada**")
            st.write(f"r = {r:.3f}")
            st.write(f"Tendencia negativa con variabilidad.")
        else:
            st.error("**❌ Relación Negativa Fuerte**")
            st.write(f"r = {r:.3f}")
            st.write(f"Cuando {data_info['x_label']} aumenta, {data_info['y_label']} tiende a disminuir significativamente.")

# === COVARIANZA ===
elif page == "🔗 Covarianza":
    st.header("🔗 Covarianza: ¿Se Mueven Juntas las Variables?")
    
    st.markdown("""
    La **covarianza** mide si dos variables tienden a moverse juntas.
    
    ### 📐 Fórmula
    """)
    
    st.latex(r"Cov(X,Y) = \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{N}")
    
    st.markdown("""
    ### 🤔 ¿Qué Significa?
    
    - **Cov > 0:** Cuando X aumenta, Y tiende a aumentar (relación positiva)
    - **Cov < 0:** Cuando X aumenta, Y tiende a disminuir (relación negativa)
    - **Cov ≈ 0:** No hay relación lineal clara
    
    ### ⚠️ Problema de la Covarianza
    
    **Depende de las unidades de medida.** No podemos comparar covarianzas de diferentes datasets.
    
    Por ejemplo:
    - Cov(estatura_cm, peso_kg) = 800
    - Cov(estatura_m, peso_kg) = 8
    
    ¡Son los mismos datos, solo cambiamos cm a metros!
    
    **Por eso usamos la CORRELACIÓN** (que está estandarizada de -1 a +1)
    """)
    
    st.markdown("---")
    
    st.markdown("### 🧮 Cálculo Paso a Paso")
    
    # Usar primeros 5 datos para mostrar cálculo
    x_sample = x_data[:5]
    y_sample = y_data[:5]
    
    x_mean_sample = np.mean(x_sample)
    y_mean_sample = np.mean(y_sample)
    
    df_cov = pd.DataFrame({
        'xi': x_sample,
        'yi': y_sample,
        'xi - x̄': x_sample - x_mean_sample,
        'yi - ȳ': y_sample - y_mean_sample,
        '(xi - x̄)(yi - ȳ)': (x_sample - x_mean_sample) * (y_sample - y_mean_sample)
    })
    
    st.markdown(f"**Usando los primeros 5 datos como ejemplo:**")
    st.markdown(f"- Media de X: {x_mean_sample:.2f}")
    st.markdown(f"- Media de Y: {y_mean_sample:.2f}")
    
    st.dataframe(df_cov.style.format("{:.2f}"), hide_index=True, use_container_width=True)
    
    suma_productos = np.sum((x_sample - x_mean_sample) * (y_sample - y_mean_sample))
    cov_sample = suma_productos / (len(x_sample))
    
    st.code(f"""
Paso 1: Suma de productos = {suma_productos:.2f}
Paso 2: Covarianza = {suma_productos:.2f} / {len(x_sample)} = {cov_sample:.2f}
    """)
    
    st.markdown("---")
      
    st.markdown("### 📊 Tu Dataset Completo")
    
    col1, col2 = st.columns(2)

    with col1: 
        st.metric("Covarianza", f"{reg_actual['cov']:.2f}")
    
    with col2:
        if reg_actual['cov'] > 0:
            st.success("**Covarianza Positiva:** Las variables se mueven en la misma dirección")
        elif reg_actual['cov'] < 0:
            st.error("**Covarianza Negativa:** Las variables se mueven en direcciones opuestas")
        else:
            st.info("**Covarianza ≈ 0:** No hay relación lineal clara")
    
    fig_cov = crear_dispersion(x_data, y_data, 
                                f"{data_info['x_label']} vs {data_info['y_label']}",
                               data_info['x_label'], data_info['y_label'])
    st.plotly_chart(fig_cov, use_container_width=True)


        
    


# === CORRELACIÓN ===
# === CORRELACIÓN (VERSIÓN MEJORADA Y COMPLETA) ===
elif page == "📈 Correlación":
    st.header("📈 Coeficiente de Correlación: La Medida Estándar")
    
    st.markdown("""
    ### 🎯 ¿Qué es el Coeficiente de Correlación (r)?
    
    El **coeficiente de correlación de Pearson (r)** es la medida más común para cuantificar 
    la **fuerza** y **dirección** de la relación **lineal** entre dos variables.
    
    Piénsalo así: la correlación te dice **qué tan bien los puntos se ajustan a una línea recta**.
    
    ### ✨ Ventaja sobre la Covarianza
    
    Mientras la covarianza depende de las unidades de medida (centímetros, dólares, kilos), 
    la correlación es **adimensional** y siempre está en el mismo rango: **-1 a +1**.
    
    Esto significa que puedes **comparar** correlaciones entre diferentes estudios, 
    independientemente de las unidades usadas.
    
    ### 📐 Fórmula
    """)
    
    st.latex(r"r = \frac{Cov(X,Y)}{s_X \cdot s_Y}")
    
    st.markdown("""
    Donde:
    - $Cov(X,Y)$ = Covarianza entre X e Y
    - $s_X$ = Desviación estándar de X
    - $s_Y$ = Desviación estándar de Y
    
    **En palabras simples:** Es la covarianza "normalizada" o "estandarizada" 
    dividiendo por las desviaciones estándar.
    """)
    
    st.markdown("---")
    
    st.markdown("## 🎯 ¿Qué Significa el Valor de r?")
    
    st.markdown("""
    El coeficiente de correlación **r** te dice DOS cosas simultáneamente:
    
    ### 1️⃣ DIRECCIÓN (Signo de r)
    
    - **r > 0 (Positivo):** Relación directa → Cuando X aumenta, Y tiende a aumentar
    - **r < 0 (Negativo):** Relación inversa → Cuando X aumenta, Y tiende a disminuir
    - **r = 0:** No hay relación lineal → X no predice Y (o la relación no es lineal)
    
    ### 2️⃣ FUERZA (Magnitud de |r|)
    
    Usamos el **valor absoluto** de r para medir la fuerza, ignorando el signo:
    """)
    
    # Tabla de interpretación
    df_interpret = pd.DataFrame({
        'Rango de |r|': ['0.0 - 0.3', '0.3 - 0.7', '0.7 - 1.0'],
        'Interpretación': ['Débil', 'Moderada', 'Fuerte'],
        'Descripción': [
            'Hay poca relación lineal. Los puntos están muy dispersos.',
            'Relación clara pero con variabilidad. Los puntos siguen una tendencia.',
            'Relación muy clara. Los puntos están muy cerca de formar una línea recta.'
        ]
    })
    
    st.dataframe(df_interpret, hide_index=True, use_container_width=True)
    
    st.info("""
    **💡 Ejemplos Prácticos:**
    
    - **|r| = 0.1:** "Sí hay correlación, pero es tan débil que prácticamente no sirve para predecir"
    - **|r| = 0.5:** "Hay relación moderada. Puedo tener una idea, pero con bastante incertidumbre"
    - **|r| = 0.9:** "Relación muy fuerte. Puedo predecir Y conociendo X con bastante precisión"
    """)
    
    st.markdown("---")
    
    st.markdown("## 📊 Escala Visual de Interpretación")
    
    # Escala visual mejorada
    fig_escala = go.Figure()
    
    # Rectángulos de fondo
    fig_escala.add_shape(
        type="rect",
        x0=-1, x1=-0.7, y0=0, y1=1,
        fillcolor="darkred", opacity=0.3, line_width=0
    )
    fig_escala.add_shape(
        type="rect",
        x0=-0.7, x1=-0.3, y0=0, y1=1,
        fillcolor="salmon", opacity=0.3, line_width=0
    )
    fig_escala.add_shape(
        type="rect",
        x0=-0.3, x1=0.3, y0=0, y1=1,
        fillcolor="gray", opacity=0.2, line_width=0
    )
    fig_escala.add_shape(
        type="rect",
        x0=0.3, x1=0.7, y0=0, y1=1,
        fillcolor="lightblue", opacity=0.3, line_width=0
    )
    fig_escala.add_shape(
        type="rect",
        x0=0.7, x1=1, y0=0, y1=1,
        fillcolor="darkblue", opacity=0.3, line_width=0
    )
    
    # Marcador para el valor actual
    fig_escala.add_trace(go.Scatter(
        x=[reg_actual['r']],
        y=[0.5],
        mode='markers+text',
        marker=dict(size=20, color='red', symbol='diamond'),
        text=[f"Tu r: {reg_actual['r']:.3f}"],
        textposition="top center",
        name='Tu correlación',
        showlegend=False
    ))
    
    fig_escala.update_layout(
        title="Escala de Interpretación de r",
        xaxis=dict(range=[-1.1, 1.1], title="Correlación (r)"),
        yaxis=dict(range=[0, 1], showticklabels=False, title=""),
        height=250
    )
    
    # Anotaciones mejoradas
    fig_escala.add_annotation(x=-0.85, y=0.85, text="Negativa<br><b>Fuerte</b>", showarrow=False, font=dict(size=11))
    fig_escala.add_annotation(x=-0.5, y=0.85, text="Negativa<br><b>Moderada</b>", showarrow=False, font=dict(size=11))
    fig_escala.add_annotation(x=0, y=0.85, text="<b>Débil/Nula</b>", showarrow=False, font=dict(size=11))
    fig_escala.add_annotation(x=0.5, y=0.85, text="Positiva<br><b>Moderada</b>", showarrow=False, font=dict(size=11))
    fig_escala.add_annotation(x=0.85, y=0.85, text="Positiva<br><b>Fuerte</b>", showarrow=False, font=dict(size=11))
    
    # Marcadores de límites
    fig_escala.add_annotation(x=-0.7, y=0.1, text="-0.7", showarrow=False, font=dict(size=9, color='gray'))
    fig_escala.add_annotation(x=-0.3, y=0.1, text="-0.3", showarrow=False, font=dict(size=9, color='gray'))
    fig_escala.add_annotation(x=0.3, y=0.1, text="+0.3", showarrow=False, font=dict(size=9, color='gray'))
    fig_escala.add_annotation(x=0.7, y=0.1, text="+0.7", showarrow=False, font=dict(size=9, color='gray'))
    
    st.plotly_chart(fig_escala, use_container_width=True)
    
    st.markdown("---")
    
    # Análisis del dataset actual
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📊 Tu Dataset Actual")
        st.metric("Correlación (r)", f"{reg_actual['r']:.3f}")
        
        # Interpretación dinámica
        r_abs = abs(reg_actual['r'])
        
        if r_abs < 0.3:
            st.warning("**Correlación Débil**")
            st.write("Hay poca relación lineal entre las variables.")
        elif r_abs < 0.7:
            st.info("**Correlación Moderada**")
            st.write("Hay una relación clara pero con variabilidad.")
        else:
            st.success("**Correlación Fuerte**")
            st.write("Hay una relación lineal muy clara.")
        
        # Dirección
        if reg_actual['r'] > 0:
            st.success("**Dirección: Positiva ↗️**")
            st.write(f"Cuando {data_info['x_label']} aumenta, {data_info['y_label']} tiende a aumentar.")
        elif reg_actual['r'] < 0:
            st.error("**Dirección: Negativa ↘️**")
            st.write(f"Cuando {data_info['x_label']} aumenta, {data_info['y_label']} tiende a disminuir.")
        else:
            st.info("**Sin relación clara**")
    
    with col2:
        fig_corr = crear_dispersion(x_data, y_data,
                                    f"Correlación r = {reg_actual['r']:.3f}",
                                    True,
                                    data_info['x_label'], data_info['y_label'])
        st.plotly_chart(fig_corr, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("## 📏 R²: El Coeficiente de Determinación")
    
    st.markdown(f"""
    ### 🎯 ¿Qué es R²?
    
    **R² (R cuadrado)** es simplemente **r elevado al cuadrado**: R² = r²
    
    Para tu dataset: r = {reg_actual['r']:.3f} → R² = {reg_actual['r']:.3f}² = **{reg_actual['r2']:.3f}**
    
    ### 💡 ¿Qué Significa?
    
    R² te dice **qué porcentaje de la variabilidad en Y es "explicada" por X**.
    
    Imagina que tienes datos de calificaciones (Y). Estas calificaciones varían: algunos sacan 60, 
    otros 80, otros 95. Esta variación tiene **causas**:
    - Horas de estudio
    - Calidad del sueño
    - Talento natural
    - Motivación
    - Nutrición
    - Muchos otros factores...
    
    Si tu modelo de regresión con "Horas de estudio" tiene **R² = 0.64**, significa que:
    
    ✅ El **64% de la variación** en las calificaciones se explica por las horas de estudio
    
    ⚠️ El **36% restante** se debe a OTROS factores (sueño, talento, etc.)
    """)
    
    st.metric("R² de tu dataset", f"{reg_actual['r2']:.3f} ({reg_actual['r2']*100:.1f}%)")
    
    st.info(f"""
    **En tu caso:**
    
    {reg_actual['r2']*100:.1f}% de la variación en **{data_info['y_label']}** se explica 
    por **{data_info['x_label']}**.
    
    El {100 - reg_actual['r2']*100:.1f}% restante se debe a otros factores no incluidos en el modelo.
    """)
    
    st.markdown("---")
    
    st.markdown("## 📊 Interpretación de R²: Depende del Contexto")
    
    st.warning("""
    ### ⚠️ IMPORTANTE: No Hay Reglas Universales
    
    La interpretación de R² **depende MUCHO del área de estudio**:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🔬 Ciencias Físicas/Exactas
        
        En física, química, ingeniería, etc., esperamos R² **MUY ALTOS**:
        
        - **R² < 0.6:** Modelo pobre (hay mucho error)
        - **R² 0.6 - 0.8:** Aceptable
        - **R² > 0.8:** Muy bueno
        - **R² > 0.95:** Excelente (esperado)
        
        **¿Por qué?** Porque las leyes físicas son muy precisas y controlables.
        
        **Ejemplos:**
        - Ley de Hooke (fuerza vs elongación): R² > 0.99
        - Ley de Ohm (voltaje vs corriente): R² > 0.98
        - Caída libre (tiempo vs distancia): R² ≈ 1.0
        
        Si tu R² es 0.60 en física, probablemente hay:
        - Error de medición
        - Variables omitidas importantes
        - Modelo incorrecto
        """)
    
    with col2:
        st.markdown("""
        ### 👥 Ciencias Sociales/Humanas
        
        En psicología, sociología, economía, etc., R² **BAJOS son normales**:
        
        - **R² < 0.3:** Débil (pero puede ser aceptable)
        - **R² 0.3 - 0.6:** Moderado/Bueno
        - **R² > 0.6:** Muy bueno (¡raro!)
        - **R² > 0.8:** Excepcional (¡casi nunca!)
        
        **¿Por qué?** Porque el comportamiento humano es **complejo** y tiene 
        **muchas causas** difíciles de medir.
        
        **Ejemplos:**
        - Ingreso vs años de educación: R² ≈ 0.25-0.40 (¡bueno!)
        - Publicidad vs ventas: R² ≈ 0.15-0.30 (aceptable)
        - Felicidad vs salario: R² ≈ 0.10-0.20 (típico)
        
        **¿Por qué tan bajos?** Porque hay MUCHOS factores:
        - Contexto familiar
        - Personalidad
        - Cultura
        - Oportunidades
        - Suerte
        - Relaciones sociales
        - Y mil cosas más...
        """)
    
    st.markdown("---")
    
    st.markdown("### 🎓 Guía General de Interpretación de R²")
    
    df_r2 = pd.DataFrame({
        'R²': ['< 0.3', '0.3 - 0.6', '> 0.6'],
        'Ciencias Exactas': ['Pobre', 'Aceptable', 'Bueno a Excelente'],
        'Ciencias Sociales': ['Débil (común)', 'Moderado/Bueno', 'Muy Bueno (raro)'],
        'Ejemplos Ciencias Exactas': [
            'Modelo con errores',
            'Fenómenos con ruido moderado',
            'Leyes físicas, reacciones químicas'
        ],
        'Ejemplos Ciencias Sociales': [
            'Felicidad vs ingresos',
            'Educación vs salario',
            'Gastos marketing vs ventas (muy bueno)'
        ]
    })
    
    st.dataframe(df_r2, hide_index=True, use_container_width=True)
    
    st.success("""
    ### 💡 La Lección Clave
    
    **NO te desanimes** si tu R² es "bajo". Pregúntate:
    
    1. ¿En qué campo estoy trabajando?
    2. ¿Qué tan predecible es naturalmente este fenómeno?
    3. ¿Es razonable esperar que UNA sola variable explique todo?
    
    En ciencias sociales, **R² = 0.40 puede ser excelente** porque significa que 
    encontraste UN factor que explica el 40% de algo muy complejo.
    
    En física, **R² = 0.40 sería terrible** porque esperamos mayor precisión en 
    fenómenos naturales más simples.
    """)
    
    st.markdown("---")
    
    st.markdown("## 🎯 Análisis de Tu R²")
    
    r2_actual = reg_actual['r2']
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.metric("Tu R²", f"{r2_actual:.3f} ({r2_actual*100:.1f}%)")
        
        if r2_actual < 0.3:
            st.warning(f"""
            **Interpretación:**
            
            - **Ciencias Exactas:** Modelo pobre, necesita mejoras
            - **Ciencias Sociales:** Débil pero común
            
            Solo el {r2_actual*100:.1f}% de la variación se explica. 
            El {(1-r2_actual)*100:.1f}% se debe a otros factores.
            """)
        elif r2_actual < 0.6:
            st.info(f"""
            **Interpretación:**
            
            - **Ciencias Exactas:** Aceptable con margen de mejora
            - **Ciencias Sociales:** Moderado a bueno
            
            El {r2_actual*100:.1f}% de la variación se explica.
            El {(1-r2_actual)*100:.1f}% se debe a otros factores.
            """)
        else:
            st.success(f"""
            **Interpretación:**
            
            - **Ciencias Exactas:** Buen modelo
            - **Ciencias Sociales:** ¡Muy bueno! (poco común)
            
            El {r2_actual*100:.1f}% de la variación se explica.
            Solo el {(1-r2_actual)*100:.1f}% se debe a otros factores.
            """)
    
    with col2:
        # Gráfico de torta mostrando R²
        fig_r2 = go.Figure(data=[go.Pie(
            labels=['Explicado por X', 'Otros factores'],
            values=[r2_actual, 1-r2_actual],
            hole=0.4,
            marker_colors=['#4CAF50', '#FFC107']
        )])
        
        fig_r2.update_layout(
            title=f"Composición de la Varianza en Y",
            height=300,
            annotations=[dict(text=f'R²={r2_actual:.2f}', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        
        st.plotly_chart(fig_r2, use_container_width=True)

    fig_corr = crear_dispersion(x_data, y_data,
                                    f"r = {reg_actual['r']:.3f}, R² = {reg_actual['r2']:.3f}",
                                    True,
                                    data_info['x_label'], data_info['y_label'])
    st.plotly_chart(fig_corr, use_container_width=True)

    st.warning("""
    ### ⚠️ Recordatorio Final
    
    **R² alto NO implica causación.**
    
    Puedes tener R² = 0.95 entre dos variables que NO tienen relación causal 
    (correlación espuria, tercera variable, etc.).
    
    R² solo te dice qué tan bien **se ajusta la línea a los puntos**, 
    NO te dice si la relación es **causal** Veremos más sobre esto en la sección de Correlación Espuria.
    """)
 



    
    

# === REGRESIÓN LINEAL ===
elif page == "📉 Regresión Lineal":
    st.header("📉 Regresión Lineal: La Ecuación para Predecir")
    
    st.markdown("""
    La **regresión lineal** encuentra la "mejor" línea recta que pasa entre los puntos. Con esta línea, puedes **predecir** valores de Y para cualquier valor de X.
    
    ### 📐 La Ecuación
    """)
    
    st.latex(r"\hat{y} = b_0 + b_1 x")
    
    st.markdown("""
    Donde:
    - $\hat{y}$ = Valor predicho de Y
    - $b_0$ = Intercepto (donde la línea cruza el eje Y)
    - $b_1$ = Pendiente (cuánto cambia Y cuando X aumenta en 1)
    - $x$ = Valor de X
    """)
    
    st.markdown("---")
    
    st.markdown("## 🧮 Tu Ecuación de Regresión")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Intercepto (b₀)", f"{reg_actual['b0']:.2f}")
        st.metric("Pendiente (b₁)", f"{reg_actual['b1']:.2f}")
        
        st.markdown(f"""
        ### 📝 Tu Ecuación:
        """)
        
        st.latex(f"\\hat{{y}} = {reg_actual['b0']:.2f} + {reg_actual['b1']:.2f}x")
        
        
        
    with col2:
        fig_regresion = crear_dispersion(x_data, y_data,
                                         f"Regresión: ŷ = {reg_actual['b0']:.2f} + {reg_actual['b1']:.2f}x",
                                         True,
                                         data_info['x_label'], data_info['y_label'])
        st.plotly_chart(fig_regresion, use_container_width=True)
    
    st.markdown("""
    ### 🔍 Interpretación de la Pendiente
    """)
    
    if reg_actual['b1'] > 0:
        st.success(f"""
        **Pendiente Positiva ({reg_actual['b1']:.2f})**
        
        Por cada unidad que aumenta {data_info['x_label']}, 
        {data_info['y_label']} aumenta en **{abs(reg_actual['b1']):.2f}** unidades (en promedio).
        """)
    else:
        st.error(f"""
        **Pendiente Negativa ({reg_actual['b1']:.2f})**
        
        Por cada unidad que aumenta {data_info['x_label']}, 
        {data_info['y_label']} disminuye en **{abs(reg_actual['b1']):.2f}** unidades (en promedio).
        """)

    st.markdown("---")
    
    st.markdown("## 🎯 Calculadora de Predicciones")
    
    st.markdown(f"""
    Usa tu ecuación para predecir valores de **{data_info['y_label']}** 
    dado un valor de **{data_info['x_label']}**.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        x_pred = st.number_input(f"Ingresa un valor de {data_info['x_label']}:",
                                 value=float(np.mean(x_data)),
                                 step=0.5)
    
    with col2:
        y_pred_valor = reg_actual['b0'] + reg_actual['b1'] * x_pred
        st.metric("Predicción (ŷ)", f"{y_pred_valor:.2f}")
    
    with col3:
        st.markdown("**Cálculo:**")
        st.code(f"""
ŷ = {reg_actual['b0']:.2f} + {reg_actual['b1']:.2f} × {x_pred}
ŷ = {reg_actual['b0']:.2f} + {reg_actual['b1'] * x_pred:.2f}
ŷ = {y_pred_valor:.2f}
        """)
    
    st.info(f"""
    **Interpretación:** Si {data_info['x_label']} es {x_pred}, 
    se espera que {data_info['y_label']} sea aproximadamente **{y_pred_valor:.2f}**.
    """)
    
    st.markdown("---")
    
    st.markdown("## 📚 Ejemplo Paso a Paso")
    
    with st.expander("🔍 Ver cálculo completo de b₀ y b₁"):
        st.markdown(f"""
        ### Cálculo de la Pendiente (b₁)
        
        Fórmula:
        """)
        st.latex(r"b_1 = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2}")
        
        x_mean = np.mean(x_data)
        y_mean = np.mean(y_data)
        
        st.markdown(f"""
        - Media de X: {x_mean:.2f}
        - Media de Y: {y_mean:.2f}
        """)
        
        numerador = np.sum((x_data - x_mean) * (y_data - y_mean))
        denominador = np.sum((x_data - x_mean)**2)
        
        st.code(f"""
Numerador = Σ(xi - x̄)(yi - ȳ) = {numerador:.2f}
Denominador = Σ(xi - x̄)² = {denominador:.2f}

b₁ = {numerador:.2f} / {denominador:.2f} = {reg_actual['b1']:.2f}
        """)
        
        st.markdown("### Cálculo del Intercepto (b₀)")
        
        st.latex(r"b_0 = \bar{y} - b_1 \bar{x}")
        
        st.code(f"""
b₀ = {y_mean:.2f} - ({reg_actual['b1']:.2f} × {x_mean:.2f})
b₀ = {y_mean:.2f} - {reg_actual['b1'] * x_mean:.2f}
b₀ = {reg_actual['b0']:.2f}
        """)

# === CORRELACIÓN ESPURIA ===
elif page == "🤔 Correlación Espuria":
    st.header("🤔 Correlación Espuria: Cuando los Números Engañan")
    
    st.markdown("""
    ### ⚠️ El Peligro de Confundir Correlación con Causación
    
    **Correlación espuria** es cuando dos variables están correlacionadas estadísticamente 
    pero **NO tienen una relación causal real**.
    
    Es decir: **se mueven juntas por PURA COINCIDENCIA** o porque ambas son causadas por 
    una **tercera variable oculta**.
    """)
    
    st.error("""
    ### 🚨 Regla de Oro
    
    # **CORRELACIÓN ≠ CAUSACIÓN**
    
    Que dos cosas estén correlacionadas NO significa que una cause la otra.
    """)
    
    st.markdown("---")
    
    st.markdown("## 😂 Ejemplos Ridículos (¡Pero Reales!)")
    
    # Ejemplo 1: Nicolas Cage
    st.markdown("### 🎬 Caso 1: Películas de Nicolas Cage y Ahogamientos")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Datos ficticios pero basados en la correlación real
        years = np.array([1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009])
        cage_movies = np.array([2, 2, 2, 3, 1, 1, 5, 4, 3, 4, 4])
        drownings = np.array([109, 102, 102, 98, 85, 95, 96, 98, 123, 94, 102])
        
        fig_cage = go.Figure()
        
        fig_cage.add_trace(go.Scatter(
            x=years, y=cage_movies,
            name='Películas de Nicolas Cage',
            yaxis='y1',
            marker=dict(size=10, color='red')
        ))
        
        fig_cage.add_trace(go.Scatter(
            x=years, y=drownings,
            name='Ahogamientos en piscinas',
            yaxis='y2',
            marker=dict(size=10, color='blue')
        ))
        
        fig_cage.update_layout(
            title="¡Correlación r = 0.666! 😱",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Películas de Nicolas Cage", side='left'),
            yaxis2=dict(title="Ahogamientos", overlaying='y', side='right'),
            height=400
        )
        
        st.plotly_chart(fig_cage, use_container_width=True)
    
    with col2:
        st.markdown("""
        **Correlación:** r = 0.666
        
        **¿Conclusión lógica?**
        ❌ "Nicolas Cage causa ahogamientos"
        ❌ "Prohibir sus películas salvará vidas"
        
        **¿Realidad?**
        ✅ **Pura coincidencia**
        
        Ambas variables fluctúan pero NO tienen 
        ninguna relación causal.
        
        Es solo **azar** que se muevan juntas 
        en ese período.
        """)
    
    st.markdown("---")
    
    # Ejemplo 2: Queso y sábanas
    st.markdown("### 🧀 Caso 2: Consumo de Queso y Muerte por Enredarse en Sábanas")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        years2 = np.array([2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009])
        cheese = np.array([29.8, 30.1, 30.5, 30.6, 31.3, 31.7, 32.6, 33.1, 32.7, 32.8])
        deaths = np.array([327, 456, 509, 497, 596, 573, 661, 741, 809, 717])
        
        fig_cheese = go.Figure()
        
        fig_cheese.add_trace(go.Scatter(
            x=years2, y=cheese,
            name='Queso per cápita (lb)',
            yaxis='y1',
            marker=dict(size=10, color='orange')
        ))
        
        fig_cheese.add_trace(go.Scatter(
            x=years2, y=deaths,
            name='Muertes por sábanas',
            yaxis='y2',
            marker=dict(size=10, color='purple')
        ))
        
        fig_cheese.update_layout(
            title="¡Correlación r = 0.947! 🤯",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Consumo de queso (lb)", side='left'),
            yaxis2=dict(title="Muertes", overlaying='y', side='right'),
            height=400
        )
        
        st.plotly_chart(fig_cheese, use_container_width=True)
    
    with col2:
        st.markdown("""
        **Correlación:** r = 0.947
        (¡Muy alta!)
        
        **¿Conclusión absurda?**
        ❌ "El queso causa muertes por sábanas"
        ❌ "Dejar de comer queso te salvará"
        
        **¿Realidad?**
        ✅ Ambas variables **aumentan con el tiempo**
        (tendencia de población creciente)
        
        ✅ Coincidencia estadística
        
        **Tercera variable:** Crecimiento poblacional
        """)
    
    st.markdown("---")
    
    # Ejemplo 3: Variables con tendencia temporal
    st.markdown("### 📈 Caso 3: La Trampa de las Tendencias Temporales")
    
    st.markdown("""
    Muchas variables **aumentan con el tiempo** simplemente porque:
    - La población crece
    - La tecnología avanza
    - La economía se expande
    
    Si graficas DOS variables que aumentan con el tiempo, ¡encontrarás correlación!
    """)
    
    # Crear ejemplo de tendencias
    years3 = np.arange(2000, 2020)
    internet = 10 * np.exp(0.15 * (years3 - 2000)) + np.random.normal(0, 5, len(years3))
    obesity = 20 + 0.5 * (years3 - 2000) + np.random.normal(0, 2, len(years3))
    
    fig_trend = go.Figure()
    
    fig_trend.add_trace(go.Scatter(
        x=years3, y=internet,
        name='Usuarios de Internet (%)',
        yaxis='y1',
        marker=dict(size=8, color='green')
    ))
    
    fig_trend.add_trace(go.Scatter(
        x=years3, y=obesity,
        name='Obesidad (%)',
        yaxis='y2',
        marker=dict(size=8, color='red')
    ))
    
    fig_trend.update_layout(
        title=f"Correlación r = {np.corrcoef(internet, obesity)[0,1]:.3f}",
        xaxis=dict(title="Año"),
        yaxis=dict(title="Usuarios Internet (%)", side='left'),
        yaxis2=dict(title="Obesidad (%)", overlaying='y', side='right'),
        height=400
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    st.warning("""
    **⚠️ ¿Internet causa obesidad?**
    
    Quizás hay una relación indirecta (sedentarismo), pero la alta correlación se debe 
    principalmente a que **ambas variables tienen una tendencia creciente en el tiempo**.
    
    No podemos concluir causación solo por la correlación.
    """)
    
    st.markdown("---")
    
    st.markdown("## 🎓 ¿Cómo Identificar Correlación Espuria?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ✅ Preguntas que Debes Hacerte:
        
        1. **¿Tiene sentido lógico?**
           - ¿Hay un mecanismo causal plausible?
           
        2. **¿Hay una tercera variable?**
           - ¿Ambas son causadas por algo más?
           
        3. **¿Es solo tendencia temporal?**
           - ¿Ambas aumentan solo porque pasa el tiempo?
           
        4. **¿Es casualidad?**
           - Con suficientes variables, encontrarás correlaciones por azar
           
        5. **¿Hay evidencia experimental?**
           - ¿Se ha probado en experimentos controlados?
        """)
    
    with col2:
        st.markdown("""
        ### 🔍 Ejemplos de Relaciones REALES:
        
        ✅ **Fumar → Cáncer de pulmón**
        - Hay mecanismo biológico
        - Experimentos en laboratorio
        - Evidencia robusta
        
        ✅ **Educación → Ingresos**
        - Mecanismo lógico (habilidades)
        - Estudios longitudinales
        - Control de otras variables
        
        ✅ **Ejercicio → Salud cardiovascular**
        - Mecanismo fisiológico conocido
        - Estudios clínicos controlados
        - Consenso científico
        """)
    
    st.markdown("---")
    
    st.success("""
    ## 🌐 ¿Quieres Ver Más Correlaciones Ridículas?
    
    Visita esta página increíble con CIENTOS de correlaciones espurias que su querido profesor encuentra graciososas:
    
    **👉 [Spurious Correlations - Tyler Vigen](https://tylervigen.com/spurious/view-all-correlations)**
    
    Encontrarás joyitas como:
    - Consumo de margarina vs. Tasa de divorcios en un estado de USA
    - Gasto en ciencia espacial vs. Suicidios por ahorcamiento
    - Número de divorcios en U.K. 💂‍♂️ vs. Películas de Disney🐀
    """)

# === EJERCICIOS ===
elif page == "🎮 Ejercicios":
    st.header("🎮 Ejercicios Prácticos")
    
    st.markdown("""
    Practica tus habilidades con estos ejercicios interactivos.
    """)
    
    ejercicios = [
        {
            "tipo": "interpretacion",
            "titulo": "📊 Ejercicio 1: Interpretación de Correlación",
            "contexto": "Un estudio encontró r = -0.85 entre 'Horas de TV al día' y 'Calificación promedio'.",
            "pregunta": "¿Qué significa esta correlación?",
            "opciones": [
                "A mayor TV, mejor calificación",
                "A mayor TV, menor calificación (relación fuerte)",
                "No hay relación entre TV y calificación",
                "El 85% de los estudiantes ve TV"
            ],
            "respuesta": "A mayor TV, menor calificación (relación fuerte)",
            "explicacion": "r = -0.85 indica una correlación negativa fuerte. Cuando una variable aumenta, la otra tiende a disminuir significativamente."
        },
        {
            "tipo": "calculo",
            "titulo": "🧮 Ejercicio 2: Predicción con Regresión",
            "contexto": "La ecuación de regresión entre 'Horas de estudio (x)' y 'Calificación (y)' es:\n\nŷ = 50 + 4x",
            "pregunta": "Si un estudiante estudia 8 horas, ¿qué calificación se espera?",
            "opciones": ["58", "68", "78", "82"],
            "respuesta": "82",
            "explicacion": "ŷ = 50 + 4(8) = 50 + 32 = 82 puntos"
        },
        {
            "tipo": "interpretacion",
            "titulo": "📈 Ejercicio 3: R² (Coeficiente de Determinación)",
            "contexto": "Un modelo de regresión tiene R² = 0.64",
            "pregunta": "¿Qué significa este valor?",
            "opciones": [
                "El 64% de los datos son correctos",
                "El 64% de la variación en Y se explica por X",
                "La correlación es 0.64",
                "Hay 64% de error en el modelo"
            ],
            "respuesta": "El 64% de la variación en Y se explica por X",
            "explicacion": "R² indica el porcentaje de variabilidad de Y que es explicada por el modelo de regresión con X."
        },
        {
            "tipo": "espuria",
            "titulo": "🤔 Ejercicio 4: Detectando Correlación Espuria",
            "contexto": "Se encontró r = 0.92 entre 'Ventas de helado' y 'Ataques de tiburón'.",
            "pregunta": "¿Es una relación causal?",
            "opciones": [
                "Sí, comer helado atrae tiburones",
                "Sí, los tiburones hacen que la gente coma helado",
                "No, probablemente ambas aumentan en verano (tercera variable)",
                "Sí, porque r > 0.9"
            ],
            "respuesta": "No, probablemente ambas aumentan en verano (tercera variable)",
            "explicacion": "Correlación espuria. Ambas variables aumentan en verano: más gente va a la playa (helado + tiburones). La tercera variable es la TEMPORADA."
        },
        {
            "tipo": "signo",
            "titulo": "➕➖ Ejercicio 5: Signo de la Pendiente",
            "contexto": "La ecuación es: ŷ = 100 - 2.5x\n\nDonde x = 'Precio' ; y = 'Demanda'",
            "pregunta": "¿Qué pasa con la demanda si el precio aumenta en $10?",
            "opciones": [
                "Aumenta en 25 unidades",
                "Disminuye en 25 unidades",
                "Aumenta en 2.5 unidades",
                "No cambia"
            ],
            "respuesta": "Disminuye en 25 unidades",
            "explicacion": "La pendiente es -2.5 (negativa). Si x aumenta en 10: Δy = -2.5 × 10 = -25 (disminuye 25 unidades)"
        },
        {
            "tipo": "visual",
            "titulo": "👁️ Ejercicio 6: Lectura de Gráfico",
            "pregunta": "Observa el gráfico de dispersión. ¿Cuál es la correlación aproximada?",
            "data_x": np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
            "data_y": np.array([10, 12, 14, 16, 18, 20, 22, 24, 26, 28]) + np.random.normal(0, 1, 10),
            "opciones": ["r ≈ -0.9", "r ≈ 0", "r ≈ +0.5", "r ≈ +0.95"],
            "respuesta": "r ≈ +0.95",
            "explicacion": "Los puntos forman una línea casi perfecta ascendente, indicando correlación positiva muy fuerte (cercana a +1)"
        }
    ]
    
    for i, ej in enumerate(ejercicios, 1):
        st.markdown(f"### {ej['titulo']}")
        
        if 'contexto' in ej:
            st.info(f"**Contexto:** {ej['contexto']}")
        
        # Si es ejercicio visual, mostrar gráfico
        if ej['tipo'] == 'visual':
            fig_ej = crear_dispersion(ej['data_x'], ej['data_y'], 
                                      "Observa el patrón", True, "X", "Y")
            st.plotly_chart(fig_ej, use_container_width=True)
        
        st.markdown(f"**{ej['pregunta']}**")
        
        with st.form(f"ejercicio_{i}"):
            resp_user = st.radio("Tu respuesta:", ej['opciones'], key=f"ej_{i}")
            submitted = st.form_submit_button("✅ Verificar")
            
            if submitted:
                if resp_user == ej['respuesta']:
                    st.success("🎉 ¡Correcto!")
                else:
                    st.error(f"❌ Incorrecto. La respuesta correcta es: **{ej['respuesta']}**")
                
                st.info(f"**💡 Explicación:** {ej['explicacion']}")
        
        st.markdown("---")

# === CUESTIONARIO ===
elif page == "❓ Cuestionario":
    st.header("❓ Cuestionario Final")
    
    st.markdown("Evalúa tu comprensión del análisis bivariado.")
    
    preguntas = [
        {
            "q": "¿Cuál es el rango posible del coeficiente de correlación (r)?",
            "opts": ["0 a 100", "-1 a 1", "0 a 1", "-∞ a +∞"],
            "resp": "-1 a 1",
            "expl": "r siempre está entre -1 (correlación negativa perfecta) y +1 (correlación positiva perfecta)"
        },
        {
            "q": "Si r = 0, ¿qué significa?",
            "opts": [
                "Hay relación positiva fuerte",
                "No hay relación lineal",
                "Hay relación negativa",
                "Los datos son iguales"
            ],
            "resp": "No hay relación lineal",
            "expl": "r = 0 indica ausencia de relación lineal entre las variables"
        },
        {
            "q": "En la ecuación ŷ = 20 + 3x, ¿qué es 3?",
            "opts": ["El intercepto", "La correlación", "La pendiente", "El error"],
            "resp": "La pendiente",
            "expl": "3 es la pendiente (b₁), indica cuánto cambia y cuando x aumenta en 1 unidad"
        },
        {
            "q": "Si R² = 0.81, ¿qué porcentaje de Y es explicado por X?",
            "opts": ["19%", "81%", "0.81%", "90%"],
            "resp": "81%",
            "expl": "R² se interpreta directamente como porcentaje: 0.81 = 81% de variación explicada"
        },
        {
            "q": "¿Cuál afirmación es CORRECTA?",
            "opts": [
                "Correlación implica causación",
                "Correlación fuerte siempre significa que X causa Y",
                "Correlación puede existir sin causación",
                "R² > 0.9 prueba causación"
            ],
            "resp": "Correlación puede existir sin causación",
            "expl": "Correlación ≠ Causación. Pueden estar correlacionadas por coincidencia o tercera variable"
        },
        {
            "q": "Si la pendiente es negativa (-5), ¿qué pasa cuando X aumenta?",
            "opts": [
                "Y aumenta",
                "Y disminuye",
                "Y no cambia",
                "Depende del intercepto"
            ],
            "resp": "Y disminuye",
            "expl": "Pendiente negativa significa relación inversa: cuando X sube, Y baja"
        },
        {
            "q": "¿Qué mide la covarianza?",
            "opts": [
                "Si las variables se mueven juntas",
                "La fuerza exacta de la relación",
                "La causa de la relación",
                "El error del modelo"
            ],
            "resp": "Si las variables se mueven juntas",
            "expl": "La covarianza mide si las variables varían conjuntamente (mismo sentido o sentido opuesto)"
        },
        {
            "q": "En un gráfico de dispersión, ¿qué indica que los puntos formen una línea recta ascendente?",
            "opts": [
                "Correlación negativa",
                "Sin correlación",
                "Correlación positiva fuerte",
                "Correlación espuria"
            ],
            "resp": "Correlación positiva fuerte",
            "expl": "Línea ascendente clara = correlación positiva fuerte (r cercano a +1)"
        },
        {
            "q": "¿Cuál es una limitación de la regresión lineal?",
            "opts": [
                "Solo funciona con datos perfectos",
                "Solo captura relaciones lineales",
                "Siempre da resultados incorrectos",
                "No se puede calcular"
            ],
            "resp": "Solo captura relaciones lineales",
            "expl": "La regresión lineal asume relación recta. Si la relación es curva, no será bien modelada"
        },
        {
            "q": "Dos variables tienen r = 0.95. ¿Podemos concluir que X causa Y?",
            "opts": [
                "Sí, porque r > 0.9",
                "Sí, porque la correlación es muy alta",
                "No, necesitamos más evidencia",
                "Sí, si R² > 0.8"
            ],
            "resp": "No, necesitamos más evidencia",
            "expl": "Alta correlación NO prueba causación. Se necesitan experimentos, teoría, y descartar terceras variables"
        }
    ]
    
    puntaje = 0
    
    for i, p in enumerate(preguntas, 1):
        st.markdown(f"### Pregunta {i}")
        st.markdown(f"**{p['q']}**")
        
        with st.form(f"quiz_{i}"):
            resp = st.radio("", p['opts'], key=f"q{i}")
            submitted = st.form_submit_button("Verificar")
            
            if submitted:
                if resp == p['resp']:
                    st.success("✅ Correcto!")
                    puntaje += 1
                else:
                    st.error(f"❌ Incorrecto. Respuesta: **{p['resp']}**")
                
                st.info(f"💡 {p['expl']}")
        
        st.markdown("---")

# === FOOTER ===
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
📧 <strong>Contacto:</strong> carlosdl@uninorte.edu.co<br>
💙 Desarrollado para estudiantes de Uninorte
</div>
""", unsafe_allow_html=True)

