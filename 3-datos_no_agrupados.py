import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import random

# === CONFIGURACIÓN ===
st.set_page_config(page_title="Tablas de Frecuencia", page_icon="📊", layout="wide")

# === DATOS GLOBALES ===
ORDEN_SATISFACCION = ['Muy Insatisfecho', 'Insatisfecho', 'Neutral', 'Satisfecho', 'Muy Satisfecho']
COLORES_NOMINAL = ['Rojo', 'Azul', 'Verde', 'Amarillo']
# Se añade el dataset 'Tiempo de Reacción (Continua)' para tener la referencia continua.
DATA_CONTINUA = pd.Series(np.random.normal(loc=40, scale=8, size=200).round(1), name='Tiempo de Reacción (seg)')

@st.cache_data
def load_datasets():
    """Carga y genera datasets para diferentes tipos de variables."""
    datasets = {
        "Color de Productos (Nominal)": {
            "data": pd.Series(np.random.choice(COLORES_NOMINAL, size=100, p=[0.25, 0.35, 0.2, 0.2]), name='Color de Productos'),
            "tipo": "Nominal", "orden": None, "descripcion": "Variable cualitativa cuyas categorías no tienen orden."
        },
        "Hijos por Familia (Discreta)": {
            "data": pd.Series(np.random.randint(0, 5, size=120), name='Hijos por Familia'),
            "tipo": "Discreta", "orden": "ascendente", "descripcion": "Variable cuantitativa que toma valores enteros contables."
        },
        "Nivel de Satisfacción (Ordinal)": {
            "data": pd.Series(np.random.choice(ORDEN_SATISFACCION, size=150, p=[0.10, 0.15, 0.25, 0.35, 0.15]), name='Nivel de Satisfacción'),
            "tipo": "Ordinal", "orden": ORDEN_SATISFACCION, "descripcion": "Variable cualitativa con un orden jerárquico natural."
        },
        "Tiempo de Reacción (Continua NO Agrupada)": {
            "data": DATA_CONTINUA,
            "tipo": "Continua", "orden": "ascendente", "descripcion": "Variable cuantitativa con muchos valores únicos. **No Agrupada** es inadecuada para el análisis."
        },
    }
    return datasets

def generar_tabla_frecuencia(data, order=None):
    """Genera una DataFrame de tabla de frecuencia completa con orden de columnas corregido."""
    if data is None or data.empty:
        return pd.DataFrame()
        
    if isinstance(order, list):
        categories = pd.Categorical(data, categories=order, ordered=True)
        frecuencia_abs = categories.value_counts()
    elif order == 'ascendente':
        frecuencia_abs = data.value_counts().sort_index(ascending=True)
    else:
        frecuencia_abs = data.value_counts().sort_index()
        
    df = pd.DataFrame({'Frecuencia Absoluta': frecuencia_abs})
    N = len(data)

    # 1. Frecuencia Acumulada
    df['Frecuencia Acumulada'] = df['Frecuencia Absoluta'].cumsum()
    # 2. Frecuencia Relativa
    df['Frecuencia Relativa'] = df['Frecuencia Absoluta'] / N
    # 3. Frecuencia Relativa Acumulada
    df['Frecuencia Relativa Acumulada'] = df['Frecuencia Acumulada'] / N
    # 4. Porcentaje
    df['Porcentaje (%)'] = df['Frecuencia Relativa'] * 100
    
    df = df.reset_index()
    df = df.rename(columns={df.columns[0]: 'Clase/Categoría'})
    return df

def generar_figura_pastel(data_dict, title, show_text=True):
    """Genera una figura de Plotly para el cuestionario (controlando si muestra el porcentaje)."""
    labels = list(data_dict.keys())
    values = list(data_dict.values())
    
    # Texto a mostrar: 'percent' si se permite, 'label' para solo la categoría
    text_info = 'percent+label' if show_text else 'label' 

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, 
                                 marker={'colors': px.colors.qualitative.D3[:len(labels)]})])
    fig.update_layout(
        height=250, 
        margin=dict(l=0, r=0, t=30, b=0),
        title=title,
        showlegend=False
    )
    fig.update_traces(textinfo=text_info, textfont_size=14)
    return fig

# === DATOS CUESTIONARIO Y CASOS REALES ===

# Datos para Pregunta 5 (Gráfico) del Cuestionario
GRAFICOS_Q5 = [
    {'Rojo': 40, 'Azul': 40, 'Verde': 20}, # A: Incorrecto
    {'Rojo': 50, 'Azul': 25, 'Verde': 25}, # B: Correcto
    {'Rojo': 33, 'Azul': 33, 'Verde': 34}  # C: Incorrecto
]

# CUESTIONARIO (Ampliado a 10 preguntas)
PREGUNTAS_CUESTIONARIO = [
    # C1: Interpretación de Acumulada (Ordinal/Discreta)
    {
        "q": "Si en la columna $F_r$ (Frecuencia Relativa Acumulada), el valor para la categoría '3 Hijos' es **0.85**, ¿qué significa?",
        "opts": ["El 85% de las familias tiene exactamente 3 hijos.",
                 "El 85% de las familias tiene 3 hijos o menos.",
                 "El 15% de las familias tiene más de 3 hijos.",
                 "El 85% de las familias tiene 4 hijos o más."],
        "resp": "El 85% de las familias tiene 3 hijos o menos.",
        "retro": "La **Frecuencia Relativa Acumulada ($F_r$)** siempre indica la proporción de datos que está en esa categoría **o en una inferior**."
    },
    # C2: Cálculo de Porcentaje de una Frecuencia Absoluta (Nominal/Discreta)
    {
        "q": "En una muestra de $N=150$ datos, la Frecuencia Absoluta ($f_i$) del color 'Verde' es **30**. ¿Cuál es el porcentaje de productos Verdes?",
        "opts": ["$30\%$", "$15\%$", "$20\%$", "$25\%$"],
        "resp": "$20\%$",
        "retro": "El porcentaje se calcula como $(\\frac{f_i}{N}) \\times 100$. Es decir, $(\\frac{30}{150}) \\times 100 = 0.20 \\times 100 = 20\%$."
    },
    # C3: Propiedad de la Moda (Discreta)
    {
        "q": "En un Gráfico de Barras que representa la Frecuencia Absoluta, ¿qué característica identifica la **Moda**?",
        "opts": ["La barra más a la izquierda.",
                 "La barra más alta.",
                 "La suma de todas las barras.",
                 "La barra del centro."],
        "resp": "La barra más alta.",
        "retro": "La **Moda** es el valor que tiene la mayor frecuencia, lo que se traduce en la **barra más alta** del gráfico de frecuencia absoluta."
    },
    # C4: Uso del Gráfico de Pastel (Nominal)
    {
        "q": "¿Cuál es la principal desventaja del Gráfico de Pastel si se tienen **12 categorías** diferentes?",
        "opts": ["La suma de los porcentajes no da 100%.",
                 "Es difícil comparar visualmente el tamaño exacto de las porciones.",
                 "Solo se puede usar para variables Discretas.",
                 "El eje X se vuelve demasiado largo."],
        "resp": "Es difícil comparar visualmente el tamaño exacto de las porciones.",
        "retro": "Con muchas categorías, el Gráfico de Pastel se vuelve ilegible; es **difícil diferenciar** visualmente entre porciones que tienen porcentajes similares (ej. $6\%$ vs $7\%$). El Gráfico de Barras es mejor."
    },
    # C5: Pregunta de Gráfico (Visual, sin porcentajes)
    {
        "q": "Un estudio muestra: **50% Rojo, 25% Azul, 25% Verde**. ¿Cuál gráfico de pastel es **correcto**?",
        "opts": ["Gráfico A", "Gráfico B", "Gráfico C"],
        "resp": "Gráfico B",
        "retro": "El **Gráfico B** es el único donde la categoría 'Rojo' ocupa la mitad del círculo (50%), y las otras dos categorías se reparten la mitad restante equitativamente (25% y 25%).",
        "tipo": "grafico",
        "datos_grafico": GRAFICOS_Q5
    },
     # C6: Propiedad de la Frecuencia Relativa
    {
        "q": "La suma total de la columna **Frecuencia Relativa ($f_r$)** siempre debe ser:",
        "opts": ["Igual a $N$ (Total de datos).",
                 "Igual a 1.0.",
                 "Mayor a 100.",
                 "El valor de la Moda."],
        "resp": "Igual a 1.0.",
        "retro": "La Frecuencia Relativa es una proporción, y la suma de todas las proporciones de las clases debe ser **1.0**."
    },
    # C7: Cuándo usar la Frecuencia Acumulada
    {
        "q": "¿Qué tipo de variable **no permite** una interpretación lógica de la Frecuencia Acumulada?",
        "opts": ["Discreta.",
                 "Ordinal.",
                 "Nominal.",
                 "Continua."],
        "resp": "Nominal.",
        "retro": "La Frecuencia Acumulada requiere un orden ('esta categoría o menos'), y las variables **Nominales** no tienen orden."
    },
    # C8: Conversión de Proporción a Número
    {
        "q": "Si la proporción ($f_r$) de clientes 'Muy Satisfecho' es **0.35** en una muestra de $N=200$, ¿cuántos clientes están en esa categoría?",
        "opts": ["35 clientes.",
                 "70 clientes.",
                 "3.5 clientes.",
                 "130 clientes."],
        "resp": "70 clientes.",
        "retro": "La cantidad se calcula como $\\mathbf{{N \\times f_r}}$. En este caso, $200 \\times 0.35 = 70$ clientes."
    },
    # C9: Interpretación de Ojiva (Curva ascendente)
    {
        "q": "¿Qué representa la curva ascendente de la **Ojiva**?",
        "opts": ["La Frecuencia Absoluta.",
                 "El Porcentaje de la Moda.",
                 "La Frecuencia Acumulada.",
                 "La Frecuencia Relativa."],
        "resp": "La Frecuencia Acumulada.",
        "retro": "La Ojiva es la representación gráfica de la **Frecuencia Relativa Acumulada ($F_r$)** o la Frecuencia Acumulada ($F_i$). Ambas son, por naturaleza, curvas ascendentes."
    },
    # C10: Rango de una frecuencia
    {
        "q": "Si en la columna $F_i$ (Frecuencia Acumulada), el valor para '4 Hijos' es **80** y el valor para '3 Hijos' es **65**, ¿cuántas familias tienen exactamente **4 hijos**?",
        "opts": ["80 familias.",
                 "15 familias.",
                 "145 familias.",
                 "65 familias."],
        "resp": "15 familias.",
        "retro": "La Frecuencia Absoluta ($f_i$) de una clase se encuentra restando la Frecuencia Acumulada ($F_i$) de la clase anterior: $\\mathbf{{f_i = F_i - F_{{i-1}}}}$ . En este caso, $F_i(\\text{{4 Hijos}}) - F_i(\\text{{3 Hijos}}) = 80 - 65 = 15$."
    },
]

# === INICIALIZACIÓN ===
if 'ejercicio_data' not in st.session_state:
    st.session_state['ejercicio_data'] = None
if 'form_counter' not in st.session_state:
    st.session_state['form_counter'] = 0
if 'mostrar_solucion_ej' not in st.session_state:
    st.session_state['mostrar_solucion_ej'] = False

# === SIDEBAR ===
with st.sidebar:
    st.title("🎯 Navegación")
    
    st.markdown("### 📊 Dataset")
    datasets = load_datasets()
    selected_dataset_name = st.selectbox("Elige datos:", list(datasets.keys()), key='sidebar_dataset')
    
    st.markdown("---")
    st.markdown("### 📑 Secciones")
    page = st.radio("", [
        "🏠 Inicio",
        "💯 Porcentajes",
        "💡 Conceptos: Tabla de Frecuencia 📋", 
        "📊 Explorador de Datos",
        "🔄 Comparador de Gráficos",
        "📈 Casos Reales (Análisis Guiado)",
        "🎲 Generador de Ejercicios y Validación",
        "❓ Cuestionario"
    ], label_visibility="collapsed")

selected_data_info = datasets.get(selected_dataset_name, {"data": None, "orden": None, "tipo": None, "descripcion": ""})
data = selected_data_info['data']
data_order = selected_data_info['orden']

st.title("📊 Análisis de Datos No Agrupados")
st.markdown("---")

# ----------------------------------------------------------------------
## 🏠 INICIO
# ----------------------------------------------------------------------
if page == "🏠 Inicio":
    st.header("👋 Bienvenido al Laboratorio de Frecuencias")
    st.markdown("""
    Este espacio interactivo está diseñado para que comprendas de manera práctica cómo se **organizan**, **visualizan** e **interpretan** los datos crudos en la estadística descriptiva. La clave para el análisis es dominar las **Tablas de Frecuencia** y elegir el gráfico correcto para cada tipo de variable.
    
    A través de las diferentes secciones, podrás:
    
    * **Comprender** los componentes esenciales de una tabla ($f_i$, $f_r$, $F_i$, $F_r$).
    * **Explorar** cómo se ve un mismo conjunto de datos (Nominales, Ordinales, Discretos) en distintos gráficos.
    * **Practicar** la construcción de tablas de frecuencia y responder preguntas de análisis de datos.
    
    Utiliza el menú lateral para iniciar tu aprendizaje. ¡Empecemos por los fundamentos!
                
    Si encuentras algun error, por favor comunicate conmigo a mi correo carlosdl@uninorte.edu.co           
    """)
    

# ----------------------------------------------------------------------
## 💯 PORCENTAJES (Ejercicios restaurados)
# ----------------------------------------------------------------------
elif page == "💯 Porcentajes":
    st.header("💯 Fundamentos: Cálculo de Porcentajes")
    
    # Explicaciones conceptuales
    st.markdown("- ### ¿Qué es una Proporción?")
    st.markdown("""
    Una **proporción** es una relación o comparación entre dos cantidades. Nos indica **qué fracción** 
    representa una parte con respecto al total. Se expresa como un número positivo mayor o igual que 0.
    """)
    
    st.markdown("- ### ¿Qué es un Porcentaje?")
    st.markdown("""
    Un **porcentaje** es una forma especial de expresar una proporción, usando como referencia **100 partes**.
    La palabra "porcentaje" significa literalmente "por cada cien".
    
    **¿Por qué usar porcentajes?**
    - Son más fáciles de entender y comparar que las proporciones decimales
    - El símbolo % significa "de cada 100"
    - 75% significa "75 de cada 100" o "75 partes de un total de 100"
    """)
    
    st.markdown("---")
    
    st.markdown("### 📝 Fórmulas Básicas")
    
    # Fórmula general
    st.markdown("#### Fórmula General:")
    col1, col2 = st.columns(2)
    with col1:
        st.latex(r"\text{Proporción} = \frac{\text{Cantidad A}}{\text{Cantidad B}}")
        st.caption("Podemos obtener un numero positivo cualquiera")
    with col2:
        st.latex(r"\text{Porcentaje} = \text{Proporción} \times 100")
        st.caption("Expresa la proporción en base 100")
    
    st.markdown("")
    
    # Caso especial: Parte/Total
    st.markdown("#### Caso Especial - Parte de un Todo:")
    st.info("""
    Cuando queremos saber **qué porción representa una parte del total**, usamos:
    """)
    
    col3, col4 = st.columns(2)
    with col3:
        st.latex(r"\text{Proporción} = \frac{\text{Parte}}{\text{Total}}")
        st.caption("Resultado: siempre entre 0 y 1")
        st.markdown("**Ejemplo:** 45 de 60 → 45/60 = 0.75")
    with col4:
        st.latex(r"\text{Porcentaje} = \frac{\text{Parte}}{\text{Total}} \times 100")
        st.caption("Resultado: siempre entre 0% y 100%")
        st.markdown("**Ejemplo:** 0.75 × 100 = 75%")
    
    st.warning("⚠️ **Importante:** El caso Parte/Total es solo UNA forma de usar proporciones. También podemos comparar cantidades independientes donde el resultado puede ser > 1 o > 100%")
        
    st.markdown("---")
    
    # Ejemplo 1
    with st.expander("**Ejemplo 1: Estudiantes Aprobados (Parte/Total)**", expanded=True):
        st.markdown("**Situación:** De 60 estudiantes, 45 aprobaron.")
        st.info("💡 Este es el caso clásico: comparamos una **parte** (45) con el **total** (60)")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Proporción:**")
            st.latex(r"\frac{45}{60} = 0.75")
            st.caption("0.75 del total aprobó (menor a 1)")
        with col2:
            st.markdown("**Porcentaje:**")
            st.latex(r"0.75 \times 100 = 75\%")
            st.caption("75 de cada 100 aprobaron (menor a 100%)")
        st.success("✅ El 75% aprobó (3 de cada 4 estudiantes)")
        
    # Ejemplo 2
    with st.expander("**Ejemplo 2: Ventas de Productos**"):
        st.markdown("**Situación:** Un almacen vende 80 productos: 20 tipo A, 30 tipo B, 30 tipo C. Cual es el porcentaje de venta de cada uno?")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**A:**")
            st.latex(r"\frac{20}{80} = 25\%")
        with col2:
            st.markdown("**B:**")
            st.latex(r"\frac{30}{80} = 37.5\%")
        with col3:
            st.markdown("**C:**")
            st.latex(r"\frac{30}{80} = 37.5\%")
        st.info("Suma: 25% + 37.5% + 37.5% = 100% ✓")

    # Ejemplo 3 (Restaurado)
    with st.expander("**Ejemplo 3: Encuesta (Acumulación)**"):
        st.markdown("**Situación:** 200 clientes: 70 muy satisfechos, 90 satisfechos, 40 otros")
        st.markdown("**¿Qué % está satisfecho o muy satisfecho?**")
        st.latex(r"\frac{70 + 90}{200} = \frac{160}{200} = 0.80 = 80\%")
        st.success("✅ El 80% está satisfecho o muy satisfecho")
        
    # Ejemplo 4 (Restaurado)
    with st.expander("**Ejemplo 4: Comparación de Proporciones**"):
        st.markdown("**Grupo A:** 30 de 40 aprobaron")
        st.markdown("**Grupo B:** 45 de 50 aprobaron")
        col1, col2 = st.columns(2)
        with col1:
            st.latex(r"\text{A: } \frac{30}{40} = 75\%")
        with col2:
            st.latex(r"\text{B: } \frac{45}{50} = 90\%")
        st.success("✅ Grupo B tiene mejor desempeño (90% vs 75%)")
        
    # Ejemplo 5 (Restaurado)
    with st.expander("**Ejemplo 5: Problema Inverso (Obtener la Parte)**"):
        st.markdown("**Situación:** El 35% de 200 empleados trabaja en ventas")
        st.markdown("**¿Cuántos empleados trabajan en ventas?**")
        st.latex(r"200 \times 0.35 = 70 \text{ empleados}")
        st.success("✅ 70 empleados")

    # Ejemplo 6 (Descuento/Disminución)
    with st.expander("**Ejemplo 6: Descuento (Disminución Porcentual)**"):
        st.markdown("**Situación:** Una tienda ofrece un descuento del **15%** en un artículo de **\$80.000**.")
        st.markdown("**¿Cuál es el valor final a pagar?**")
        
        st.markdown("1. **Método de Disminución Directa (Factor de Cambio):**")
        st.info("Si descuentas el **15%**, el valor final es el **85%** del precio original ($100\% - 15\% = 85\%$ o $1 - 0.15 = 0.85$).")
        st.latex(r"\text{Valor Final} = \text{Precio Original} \times (1 - \text{Tasa de Descuento})")
        st.latex(r"\text{Valor Final} = 80.000 \times (1 - 0.15) = 80.000 \times 0.85 = \mathbf{68.000}")
        st.success("✅ El valor final es **\$68.000**")
        
    # Ejemplo 7 (Aumento/Incremento)
    with st.expander("**Ejemplo 7: Aumento (Incremento Porcentual)**"):
        st.markdown("**Situación:** Una acción tiene un valor de **\$5.000** y su rendimiento **aumentó** en un **20%**.")
        st.markdown("**¿Cuál es el nuevo valor de la acción?**")
        
        st.markdown("1. **Método de Aumento Directo (Factor de Cambio):**")
        st.info("Si aumenta el **20%**, el valor final es el **120%** del precio original ($100\% + 20\% = 120\%$ o $1 + 0.20 = 1.20$).")
        st.latex(r"\text{Valor Final} = \text{Precio Original} \times (1 + \text{Tasa de Aumento})")
        st.latex(r"\text{Valor Final} = 5.000 \times (1 + 0.20) = 5.000 \times 1.20 = \mathbf{6.000}")
        st.success("✅ El nuevo valor de la acción es **\$6.000**")
        
    # Ejemplo 8 (Nuevo: Porcentaje > 100%)
    with st.expander("**Ejemplo 8: Comparación con Porcentaje Mayor a 100%**"):
        st.markdown("**Situación:** Un producto cuesta **\$150** hoy, pero antes costaba **\$100**.")
        st.markdown("**¿Qué porcentaje representa el precio actual respecto al anterior?**")
        st.info("💡 Aquí NO comparamos parte/total, sino **precio nuevo** vs **precio anterior**")
        st.latex(r"\text{Proporción} = \frac{150}{100} = 1.50")
        st.latex(r"\text{Porcentaje} = 1.50 \times 100 = 150\%")
        st.warning("⚠️ El precio actual es el **150%** del anterior (es decir, un 50% más caro)")
        st.success("✅ Interpretación: Por cada \$100 que costaba, ahora cuesta \$150")
        
    # Calculadora
    st.markdown("---")
    st.markdown("### 🧮 Calculadora Interactiva")
    col1, col2 = st.columns(2)
    with col1:
        parte = st.number_input("Parte:", min_value=0.0, value=45.0, key='calc_parte_p')
        total = st.number_input("Total:", min_value=1.0, value=60.0, key='calc_total_p')
    with col2:
        if total > 0:
            prop = parte / total
            porc = prop * 100
            st.metric("Proporción", f"{prop:.4f}")
            st.metric("Porcentaje", f"{porc:.2f}%")
# ----------------------------------------------------------------------
## 💡 CONCEPTOS: TABLA DE FRECUENCIA
# ----------------------------------------------------------------------
elif page == "💡 Conceptos: Tabla de Frecuencia 📋":
    st.header("💡 Conceptos: Estructura de la Tabla de Frecuencia")
    st.markdown("""
    La **Tabla de Frecuencia** es la herramienta fundamental para resumir y organizar cualquier conjunto de datos.
    """)
    
    st.markdown("### 📌 Componentes Esenciales y su Orden Lógico")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Frecuencias de Conteo")
        st.markdown(r"**Frecuencia Absoluta** ($f_i$) [**Conteo**]:")
        st.info("Es el **número de veces** que aparece un valor o categoría específica.")
        st.markdown(r"**Frecuencia Acumulada** ($F_i$):")
        st.info("Es la suma de las frecuencias absolutas hasta la categoría actual. **Solo tiene sentido** para variables con orden (Ordinales, Discretas, Continuas).")
    
    with col2:
        st.subheader("2. Frecuencias Proporcionales")
        st.markdown(r"**Frecuencia Relativa** ($f_r$):")
        st.info(r"Es la **proporción** respecto al total ($N$). Se calcula como $f_r = f_i / N$. Su suma siempre es **1**.")
        st.markdown(r"**Frecuencia Relativa Acumulada** ($F_r$):")
        st.info(r"Es la proporción de datos que está en la categoría actual o inferior. Se calcula como $F_r = F_i / N$. El último valor debe ser **1**.")

    st.markdown("---")
    st.markdown("### 🔎 Ejemplo de Lógica (Variables con Orden)")
    
    st.markdown("Ejemplo usando datos con orden y la estructura corregida:")
    
    ej_data = {'Clase/Categoría': ['Bajo', 'Medio', 'Alto'], 'Frecuencia Absoluta': [10, 20, 10]}
    ej_df = pd.DataFrame(ej_data)
    N_ej = ej_df['Frecuencia Absoluta'].sum()
    ej_df['Frecuencia Acumulada'] = ej_df['Frecuencia Absoluta'].cumsum()
    ej_df['Frecuencia Relativa'] = ej_df['Frecuencia Absoluta'] / N_ej
    ej_df['Frecuencia Relativa Acumulada'] = ej_df['Frecuencia Acumulada'] / N_ej
    ej_df['Porcentaje'] = ej_df['Frecuencia Relativa'] * 100

    
    st.dataframe(ej_df.style.format(
        {'Frecuencia Relativa': '{:.2f}', 'Frecuencia Relativa Acumulada': '{:.2f}', 'Porcentaje': '{:.0f}%'}
    ), hide_index=True, use_container_width=True)

    st.markdown(r"""
    * **Frecuencia Absoluta ($f_i$)** de 'Medio' (20) es la Moda si es el valor más alto.
    * **Frecuencia Acumulada ($F_i$)** de 'Alto' (40) nos da el Total de datos ($N$).
    * **Frecuencia Relativa Acumulada ($F_r$)** de 'Medio' (0.75) indica que el $\mathbf{75\%}$ de los datos son 'Medio o Bajo'.
    """)


# ----------------------------------------------------------------------
## 📊 EXPLORADOR DE DATOS (Diseño corregido)
# ----------------------------------------------------------------------
elif page == "📊 Explorador de Datos":
    st.header("📊 Explorador de Datos")
    
    if data is not None:
        st.success(f"**Dataset:** {selected_dataset_name} (N={len(data)}) | **Tipo:** {selected_data_info['tipo']}")
        st.info(f"**Descripción:** {selected_data_info['descripcion']}")

        tabla = generar_tabla_frecuencia(data, order=data_order)
        
        # 1. Tabla arriba (diseño corregido)
        st.subheader("📋 Tabla de Frecuencia Completa")
        st.dataframe(tabla, hide_index=True, use_container_width=True)
        st.markdown("---")

        # 2. Gráfico abajo (se mantiene en una sola columna)
        st.subheader("📈 Visualización Gráfica")
        chart = st.selectbox("Elige el Tipo de Gráfico:", ['Barras', 'Pastel', 'Ojiva'], key='explorador_chart')
        
        x_axis_config = {'categoryorder': 'array', 'categoryarray': data_order} if isinstance(data_order, list) else {}

        if chart == 'Barras':
            fig = px.bar(tabla, x='Clase/Categoría', y='Frecuencia Absoluta', 
                         title='Gráfico de Barras (Frecuencia Absoluta)')
        elif chart == 'Pastel':
            fig = px.pie(tabla, values='Porcentaje (%)', names='Clase/Categoría', 
                         title='Gráfico de Pastel (Distribución Porcentual)')
        else: # Ojiva
            fig = px.line(tabla, x='Clase/Categoría', y='Frecuencia Relativa Acumulada', 
                         title='Ojiva (Frecuencia Relativa Acumulada)', markers=True)
        
        # Aplicar orden si no es pastel
        if chart != 'Pastel' and data_order is not None:
             fig.update_xaxes(x_axis_config)

        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.info("Selecciona un dataset para empezar a explorar.")

# ----------------------------------------------------------------------
## 🔄 COMPARADOR DE GRÁFICOS (Precauciones y usos mejorados)
# ----------------------------------------------------------------------
elif page == "🔄 Comparador de Gráficos":
    st.header("🔄 Comparador de Gráficos: Elección Correcta")
    
    if data is not None:
        tabla = generar_tabla_frecuencia(data, order=data_order)
        data_type = selected_data_info['tipo']
        
        col1, col2, col3 = st.columns(3)
        x_axis_config = {'categoryorder': 'array', 'categoryarray': data_order} if isinstance(data_order, list) else {}

        # --- GRÁFICO DE BARRAS ---
        with col1:
            st.subheader("Gráfico de Barras")
            fig = px.bar(tabla, x='Clase/Categoría', y='Frecuencia Absoluta')
            if data_order is not None: fig.update_xaxes(x_axis_config)
            st.plotly_chart(fig, use_container_width=True)
            
            # Lógica de Mensajes para Barras
            if data_type in ['Nominal', 'Ordinal', 'Discreta']:
                st.success("✅ **APLICABLE Y RECOMENDADO:** Ideal para **Nominales**, **Ordinales** y **Discretas**. Permite una **comparación directa** de la Frecuencia Absoluta ($f_i$) o Porcentual.")
                st.info("💡 **Consejo:** Excelente para visualizar la **Moda** (la barra más alta).")
            elif data_type == 'Continua':
                st.error("❌ **NO APLICABLE:** Para datos Continuos no agrupados, este gráfico es inútil al mostrar una barra por cada valor. Se debe usar un **Histograma** (datos agrupados en intervalos).")

        # --- GRÁFICO DE PASTEL ---
        with col2:
            st.subheader("Gráfico de Pastel")
            fig = px.pie(tabla, values='Porcentaje (%)', names='Clase/Categoría')
            st.plotly_chart(fig, use_container_width=True)
            
            # Lógica de Mensajes para Pastel
            if data_type == 'Nominal':
                st.success("✅ **APLICABLE:** Muestra la **proporción** de cada parte respecto al $100\%$ total. Es adecuado para variables **Nominales**.")
                if len(tabla) > 1:
                    st.warning("⚠️ **Precaución Clave:** Si hay más de **6 o 7 categorías**, el gráfico pierde utilidad visual y es difícil diferenciar las porciones pequeñas.")
            elif data_type in ['Ordinal', 'Discreta']:
                 st.warning("⚠️ **LIMITACIÓN:** El gráfico de pastel se puede generar, pero **no es el más recomendado**.")
                 st.warning("⚠️ **Precaución Clave:** Si hay más de **6 o 7 categorías**, el gráfico pierde utilidad visual y es difícil diferenciar las porciones pequeñas.")
                 if data_type == 'Ordinal':
                    st.warning("⚠️ **El Problema:** Al ser un círculo, el gráfico **sacrifica la información del orden** jerárquico inherente a la variable Ordinal.")
            elif data_type == 'Continua':
                st.error("❌ **NO APLICABLE:** Si la variable es Continua, generalmente tiene muchos valores, lo que hace el pastel ilegible.")

            
        # --- OJIVA (ACUMULADA) ---
        with col3:
            st.subheader("Ojiva (Frecuencia Acumulada)")
            fig = px.line(tabla, x='Clase/Categoría', y='Frecuencia Relativa Acumulada', markers=True)
            if data_order is not None: fig.update_xaxes(x_axis_config)
            st.plotly_chart(fig, use_container_width=True)
            
            # Lógica de Mensajes para Ojiva
            if data_type in ['Ordinal', 'Discreta', 'Continua']:
                st.success("✅ **APLICABLE Y ESENCIAL:** Muestra qué proporción de la población está por **debajo de un valor** ($F_r$). Es crucial para el análisis acumulado.")
                st.info("💡 **Consejo:** Permite estimar percentiles o cuartiles de manera gráfica muy fácil.")
            elif data_type == 'Nominal':
                st.error("❌ **NO APLICABLE:** La acumulación **carece de significado** en variables Nominales, ya que el orden de las categorías es arbitrario (ej. ¿qué significa 'Rojo o menos'?).")
    else:
        st.info("Selecciona un dataset para iniciar el comparador.")

# ----------------------------------------------------------------------
## 📈 CASOS REALES (Múltiples preguntas)
# ----------------------------------------------------------------------
elif page == "📈 Casos Reales (Análisis Guiado)":
    st.header("📈 Casos Reales: Análisis Guiado de Tablas")
    
    if data is not None:
        st.subheader(f"Dataset: {selected_dataset_name} (N={len(data)})")
        tabla = generar_tabla_frecuencia(data, order=data_order)
        
        with st.expander("Ver tabla de frecuencia completa"):
            st.dataframe(tabla, hide_index=True, use_container_width=True)

        st.markdown("---")
        
        # Generación dinámica de preguntas según el tipo de variable
        
        if selected_data_info['tipo'] == 'Ordinal' and selected_dataset_name == "Nivel de Satisfacción (Ordinal)":
            st.markdown("### Análisis: Nivel de Satisfacción (Ordinal) - Mínimo 5 Preguntas")
            
            # P1: Acumulada (Satisfecho o menos)
            st.markdown("**P1:** ¿Qué **porcentaje** de clientes está **Satisfecho o inferior**?")
            if st.button("Mostrar P1", key="p1_ord"):
                val = tabla[tabla['Clase/Categoría']=='Satisfecho']['Frecuencia Relativa Acumulada'].iloc[0]
                st.success(f"Respuesta: **{val*100:.2f}%**")
                # CORRECCIÓN P1: Usar valor dinámico en la fórmula
                st.info(f"Procedimiento: Se lee la columna $\\mathbf{{F_r}}$ para la categoría 'Satisfecho' y se multiplica por 100. $F_r(\\text{{Satisfecho}}) = {val:.4f}$, entonces $\\text{{Porcentaje}} = {val:.4f} \\times 100 = {val*100:.2f}\\%$.")
                
            # P2: Absoluta Inversa (Superior a)
            st.markdown("**P2:** ¿Cuántos clientes están en un nivel de satisfacción **superior a Neutral**?")
            if st.button("Mostrar P2", key="p2_ord"):
                fa_hasta_neutral = tabla[tabla['Clase/Categoría']=='Neutral']['Frecuencia Acumulada'].iloc[0]
                total = len(data)
                respuesta = total - fa_hasta_neutral
                st.success(f"Respuesta: **{int(respuesta)}** clientes")
                # CORRECCIÓN P2: Usar variables dinámicas y \text{}
                st.info(f"Procedimiento: Clientes superiores = $N - F_i(\\text{{Neutral}}) = {total} - {fa_hasta_neutral} = {int(respuesta)}$.")
                
            # P3: Frecuencia Absoluta de la Moda
            st.markdown("**P3:** ¿Cuál es la **Frecuencia Absoluta** ($f_i$) del nivel de satisfacción **más común** (Moda)?")
            if st.button("Mostrar P3", key="p3_ord"):
                moda_val = data.mode().iloc[0]
                fa = tabla[tabla['Clase/Categoría']==moda_val]['Frecuencia Absoluta'].iloc[0]
                st.success(f"Respuesta: **{int(fa)}** clientes ({moda_val})")
                # CORRECCIÓN P3: Simplificar la explicación con la variable modal
                st.info(f"Procedimiento: La moda es '{moda_val}'. Se lee directamente su valor en la columna $f_i$: $\\mathbf{{f_i(\\text{{{moda_val}}})}} = {int(fa)}$.")

            # P4: Acumulada de rango
            st.markdown("**P4:** ¿Qué proporción de clientes está **Insatisfecho o Muy Insatisfecho**?")
            if st.button("Mostrar P4", key="p4_ord"):
                fr_ins = tabla[tabla['Clase/Categoría']=='Insatisfecho']['Frecuencia Relativa'].iloc[0]
                fr_muyns = tabla[tabla['Clase/Categoría']=='Muy Insatisfecho']['Frecuencia Relativa'].iloc[0]
                proporcion = fr_ins + fr_muyns
                st.success(f"Respuesta: **{proporcion:.4f}**")
                # CORRECCIÓN P4: Usar la suma de fr y valores dinámicos
                st.info(f"Procedimiento: Se suman las $f_r$ de las dos categorías: $f_r(\\text{{Insatisfecho}}) + f_r(\\text{{Muy Insatisfecho}}) = {fr_ins:.4f} + {fr_muyns:.4f} = {proporcion:.4f}$.")
            
            # P5: Porcentaje de Rango Inverso
            st.markdown("**P5:** ¿Qué porcentaje de clientes está **Muy Satisfecho**?")
            if st.button("Mostrar P5", key="p5_ord"):
                porc = tabla[tabla['Clase/Categoría']=='Muy Satisfecho']['Porcentaje (%)'].iloc[0]
                st.success(f"Respuesta: **{porc:.2f}%**")
                # CORRECCIÓN P5: Usar el valor dinámico en la explicación
                st.info(f"Procedimiento: Lectura directa de la columna Porcentaje ($\\%$) para 'Muy Satisfecho': $\\mathbf{{\\%(\\text{{Muy Satisfecho}})}} = {porc:.2f}\\%$.")


        elif selected_data_info['tipo'] == 'Nominal' and selected_dataset_name == "Color de Productos (Nominal)":
            st.markdown("### Análisis: Color de Productos (Nominal) - Mínimo 5 Preguntas")
            
            # P1: Proyección de Frecuencia (Nominal)
            st.markdown("**P1:** Si la producción se escala a $300$ unidades, ¿cuántos productos del color **más popular (Moda)** se esperarían producir?")
            if st.button("Mostrar P1", key="p1_nom"):
                moda_val = tabla.iloc[tabla['Frecuencia Absoluta'].argmax()]['Clase/Categoría']
                fr = tabla[tabla['Clase/Categoría']==moda_val]['Frecuencia Relativa'].iloc[0]
                esperado = int(300 * fr)
                st.success(f"Respuesta: **{esperado}** productos de color '{moda_val}'")
                # CORRECCIÓN P1: Usar valor dinámico en la fórmula
                st.info(f"Procedimiento: Se aplica la Frecuencia Relativa del color modal: $\\mathbf{{300 \\times f_r(\\text{{{moda_val}}})}} = 300 \\times {fr:.4f} \\approx {int(esperado)}$.")
                
            # P2: Frecuencia Absoluta de Múltiples Categorías
            st.markdown("**P2:** ¿Cuántos productos, en total, **NO son 'Rojos' ni 'Azules'**?")
            if st.button("Mostrar P2", key="p2_nom"):
                fa_rojo = tabla[tabla['Clase/Categoría']=='Rojo']['Frecuencia Absoluta'].iloc[0]
                fa_azul = tabla[tabla['Clase/Categoría']=='Azul']['Frecuencia Absoluta'].iloc[0]
                total = len(data)
                respuesta = total - (fa_rojo + fa_azul)
                st.success(f"Respuesta: **{int(respuesta)}** productos")
                # CORRECCIÓN P2: Usar variables dinámicas y \text{}
                st.info(f"Procedimiento: Total $N$ menos la suma de las $f_i$ de 'Rojo' y 'Azul': $\\mathbf{{N - (f_i(\\text{{Rojo}}) + f_i(\\text{{Azul}}))}} = {total} - ({fa_rojo} + {fa_azul}) = {int(respuesta)}$.")
                
            # P3: Porcentaje de Múltiples Categorías
            st.markdown("**P3:** ¿Cuál es el **porcentaje combinado** de productos 'Verdes' y 'Amarillos'?")
            if st.button("Mostrar P3", key="p3_nom"):
                porc_ver = tabla[tabla['Clase/Categoría']=='Verde']['Porcentaje (%)'].iloc[0]
                porc_ama = tabla[tabla['Clase/Categoría']=='Amarillo']['Porcentaje (%)'].iloc[0]
                total_porc = porc_ver + porc_ama
                st.success(f"Respuesta: **{total_porc:.2f}%**")
                # CORRECCIÓN P3: Usar la suma de porcentajes con valores dinámicos
                st.info(f"Procedimiento: Sumar los porcentajes de ambas categorías: $\\mathbf{{\\%(\\text{{Verde}}) + \\%(\\text{{Amarillo}})}} = {porc_ver:.2f}\\% + {porc_ama:.2f}\\% = {total_porc:.2f}\\%$.")
            
            # P4: Porcentaje de la categoría menos común
            st.markdown("**P4:** ¿Cuál es la **proporción** del color **menos frecuente**?")
            if st.button("Mostrar P4", key="p4_nom"):
                min_val = tabla['Frecuencia Absoluta'].min()
                fr = tabla[tabla['Frecuencia Absoluta']==min_val]['Frecuencia Relativa'].iloc[0]
                st.success(f"Respuesta: **{fr:.4f}**")
                # CORRECCIÓN P4: Usar la fórmula de fr con el valor dinámico
                st.info(f"Procedimiento: Se identifica la Frecuencia Absoluta mínima ($f_i = {min_val}$) y se lee su correspondiente $f_r$: $\\mathbf{{f_r}} = {fr:.4f}$.")
                
            # P5: Frecuencia de la categoría más común
            st.markdown("**P5:** ¿Cuántas veces más es la $f_i$ del color más popular comparado con el color menos popular?")
            if st.button("Mostrar P5", key="p5_nom"):
                fa_max = tabla['Frecuencia Absoluta'].max()
                fa_min = tabla['Frecuencia Absoluta'].min()
                ratio = fa_max / fa_min
                st.success(f"Respuesta: **{ratio:.2f} veces**")
                # CORRECCIÓN P5: Usar la división de fi con valores dinámicos
                st.info(f"Procedimiento: Se divide la $f_i$ máxima entre la $f_i$ mínima: $\\mathbf{{\\frac{{f_{{i, max}}}}{{f_{{i, min}}}}}} = \\frac{{{fa_max}}}{{{fa_min}}} = {ratio:.2f} \\text{{ veces}}$.")


        elif selected_data_info['tipo'] == 'Discreta' and selected_dataset_name == "Hijos por Familia (Discreta)":
            st.markdown("### Análisis: Hijos por Familia (Discreta) - Mínimo 5 Preguntas")
            
            # P1: Acumulada
            st.markdown("**P1:** ¿Qué porcentaje de familias tiene **2 hijos o menos**?")
            if st.button("Mostrar P1", key="p1_disc"):
                val = tabla[tabla['Clase/Categoría']==2]['Frecuencia Relativa Acumulada'].iloc[0]
                st.success(f"Respuesta: **{val*100:.2f}%**")
                # CORRECCIÓN P1: Usar valor dinámico en la fórmula
                st.info(f"Procedimiento: Lectura de la $\\mathbf{{F_r}}$ para el valor '2' y multiplicación por 100: $F_r(2) \\times 100 = {val:.4f} \\times 100 = {val*100:.2f}\\%$.")
                
            # P2: Absoluta de rango
            st.markdown("**P2:** ¿Cuántas familias tienen **más de 3 hijos**?")
            if st.button("Mostrar P2", key="p2_disc"):
                fa_hasta_3 = tabla[tabla['Clase/Categoría']==3]['Frecuencia Acumulada'].iloc[0]
                total = len(data)
                respuesta = total - fa_hasta_3
                st.success(f"Respuesta: **{int(respuesta)}** familias")
                # CORRECCIÓN P2: Usar valores dinámicos en la fórmula
                st.info(f"Procedimiento: Familias con más de 3 hijos = $\\mathbf{{N - F_i(3)}} = {total} - {fa_hasta_3} = {int(respuesta)}$.")
                
            # P3: Frecuencia Absoluta de la Moda
            st.markdown("**P3:** ¿Cuál es el número de familias que tiene **el número de hijos más frecuente (Moda)**?")
            if st.button("Mostrar P3", key="p3_disc"):
                moda_val = data.mode().iloc[0]
                val = tabla[tabla['Clase/Categoría']==moda_val]['Frecuencia Absoluta'].iloc[0]
                st.success(f"Respuesta: **{int(val)}** familias con {int(moda_val)} hijos.")
                # CORRECCIÓN P3: Usar valor dinámico en la explicación
                st.info(f"Procedimiento: La moda es **{int(moda_val)}** hijos. Se lee el valor $\\mathbf{{f_i}}$ correspondiente: $f_i(\\text{{Moda}}) = f_i({int(moda_val)}) = {int(val)}$.")
                
            # P4: Porcentaje de la categoría menos común
            st.markdown("**P4:** ¿Qué porcentaje de familias tiene **el número de hijos menos frecuente**?")
            if st.button("Mostrar P4", key="p4_disc"):
                min_fa = tabla['Frecuencia Absoluta'].min()
                porc = tabla[tabla['Frecuencia Absoluta']==min_fa]['Porcentaje (%)'].iloc[0]
                st.success(f"Respuesta: **{porc:.2f}%**")
                # CORRECCIÓN P4: Usar valor dinámico en la explicación
                st.info(f"Procedimiento: Se encuentra la Frecuencia Absoluta mínima ($f_i = {int(min_fa)}$) y se lee su porcentaje asociado: $\\mathbf{{\\%}} = {porc:.2f}\\%$.")
            
            # P5: Proporción de Rango (0, 1 o 2 hijos)
            st.markdown("**P5:** ¿Cuál es la proporción de familias que tiene **2 hijos o menos**?")
            if st.button("Mostrar P5", key="p5_disc"):
                fr_2 = tabla[tabla['Clase/Categoría']==2]['Frecuencia Relativa Acumulada'].iloc[0]
                st.success(f"Respuesta: **{fr_2:.4f}**")
                # CORRECCIÓN P5: Usar valor dinámico en la fórmula
                st.info(f"Procedimiento: Lectura directa de la $\\mathbf{{F_r}}$ para 2 hijos: $F_r(2) = {fr_2:.4f}$.")
                
        elif selected_data_info['tipo'] == 'Continua':
            st.markdown("### Análisis: Tiempo de Reacción (Continua NO Agrupada)")
            
            st.error("🚨 **ADVERTENCIA:** Este dataset es **Continua** y **NO está agrupado** por intervalos.")
            
            st.markdown("**P1:** ¿Por qué la Tabla de Frecuencia generada es inútil para el análisis?")
            if st.button("Mostrar P1", key="p1_cont"):
                # CORRECCIÓN P1: Poner N y filas únicas en LaTeX
                st.info(f"Respuesta: Hay $N={len(data)}$ datos, pero la tabla tiene $\\mathbf{{ {len(tabla)} }}$ filas únicas. Es decir, casi cada valor es distinto.")
                st.warning("Explicación: Para datos Continuos o Discretos con muchos valores, **es obligatorio agruparlos en intervalos (Clases)** para que la tabla y el gráfico (Histograma) sean significativos.")
                
            st.markdown("**P2:** ¿Qué tipo de gráfico debería usarse en su lugar?")
            if st.button("Mostrar P2", key="p2_cont"):
                st.success("Respuesta: Un **Histograma** (para la $f_i$) y una **Ojiva** (para la $F_r$).")
                st.info("Explicación: El Histograma se usa para variables continuas agrupadas, mostrando la densidad de datos por intervalo.")
    
    else:
        st.info("Selecciona un dataset para iniciar el análisis guiado.")


# ----------------------------------------------------------------------
## 🎲 GENERADOR DE EJERCICIOS Y VALIDACIÓN (Error corregido)
# ----------------------------------------------------------------------
elif page == "🎲 Generador de Ejercicios y Validación":
    st.header("🎲 Generador de Ejercicios y Validación de Frecuencias")
    
    # Botón fuera del formulario
    if st.button("Generar Nuevo Ejercicio", key='gen_new_exercise'):
        
        # 70% Nominal/Ordinal, 30% Discreta
        if random.random() < 0.7: 
            tipo = random.choice(['Letras (Nominal)', 'Niveles (Ordinal)'])
        else:
            tipo = 'Números (Discreta)'
            
        N = random.randint(25, 55)
        
        if tipo == 'Letras (Nominal)':
            new_data = pd.Series(np.random.choice(['A','B','C','D','E'], size=N), name='Calificaciones de Encuesta')
        elif tipo == 'Niveles (Ordinal)':
            new_data = pd.Series(np.random.choice(ORDEN_SATISFACCION, size=N, p=[0.1, 0.2, 0.3, 0.3, 0.1]), name='Valoración de Producto')
        else: # Números (Discreta)
            new_data = pd.Series(np.random.randint(0, 6, size=N), name='Veces Compradas')
            
        st.session_state['ejercicio_data'] = new_data
        st.session_state['form_counter'] += 1
        st.session_state['mostrar_solucion_ej'] = False
        st.rerun()
        
    if st.session_state['ejercicio_data'] is not None:
        data_ej = st.session_state['ejercicio_data']
        
        # Determinar el orden correcto para la tabla
        order_ej = ORDEN_SATISFACCION if data_ej.name == 'Valoración de Producto' else 'ascendente'
        if data_ej.name == 'Calificaciones de Encuesta':
            order_ej = None

        tabla_correcta = generar_tabla_frecuencia(data_ej, order=order_ej).set_index('Clase/Categoría')
        
        st.subheader(f"Datos Crudos ({data_ej.name}, N={len(data_ej)}):")
        st.code(', '.join(map(str, data_ej.tolist())))
        
        st.markdown("### Ingresa solo las frecuencias absolutas ($f_i$) de las clases:")
        
        form_key = f"ejercicio_form_{st.session_state['form_counter']}"
        with st.form(form_key):
            user_inputs = {}
            cols = st.columns(len(tabla_correcta))
            
            for i, cat in enumerate(tabla_correcta.index):
                # Asegurar que la clave del input sea string
                cat_str = str(cat) 
                input_key = f"input_{cat_str}_{st.session_state['form_counter']}"
                
                user_inputs[cat_str] = cols[i].number_input(
                    f"Frec. Abs. ({cat_str})", 
                    min_value=0, 
                    step=1,
                    key=input_key
                )
            
            submitted = st.form_submit_button("Validar")
            
            if submitted:
                st.session_state['mostrar_solucion_ej'] = False # Ocultar solución si se valida
                correcto = True
                st.markdown("---")
                for cat in tabla_correcta.index:
                    esperado = tabla_correcta.loc[cat, 'Frecuencia Absoluta']
                    user_val = user_inputs[str(cat)]
                    if user_val == esperado:
                        st.success(f"✅ **{cat}**: Correcto ($f_i = {esperado}$)")
                    else:
                        st.error(f"❌ **{cat}**: Tu $f_i = {user_val}$, Correcta: ${esperado}$")
                        correcto = False
                        
                if correcto:
                    st.balloons()
                    st.success("🎉 ¡Perfecto! La Frecuencia Absoluta es correcta.")
                else:
                    st.warning("Revisa tu conteo e intenta de nuevo.")

        # Botón de solución (FUERA DEL FORMULARIO)
        if st.button("Mostrar Tabla de Solución Completa", key='show_solution_button'):
            st.session_state['mostrar_solucion_ej'] = True
            
        if st.session_state.get('mostrar_solucion_ej', False):
             st.markdown("### Solución del Ejercicio")
             st.dataframe(tabla_correcta.reset_index(), use_container_width=True)

# ----------------------------------------------------------------------
## ❓ CUESTIONARIO (10 preguntas)
# ----------------------------------------------------------------------
elif page == "❓ Cuestionario":
    st.header("❓ Cuestionario Interactivo")
    st.info("Responde las siguientes preguntas. Están orientadas a la **interpretación de valores de frecuencia y la selección de gráficos**.")
    
    # Iterar sobre todas las preguntas
    for i, p in enumerate(PREGUNTAS_CUESTIONARIO, start=1):
        st.markdown(f"---")
        st.markdown(f"**P{i}:** {p['q']}")
        
        # Lógica especial para preguntas con gráfico de pastel (P5)
        if p.get("tipo") == "grafico":
            
            col1, col2, col3 = st.columns(3)
            
            # 1. Crear y mostrar los gráficos SIN TEXTO DE PORCENTAJE (show_text=False)
            with col1:
                st.markdown("**Gráfico A**")
                fig1 = generar_figura_pastel(p['datos_grafico'][0], "Gráfico A", show_text=False)
                st.plotly_chart(fig1, use_container_width=True)
                
            with col2:
                st.markdown("**Gráfico B**")
                fig2 = generar_figura_pastel(p['datos_grafico'][1], "Gráfico B", show_text=False)
                st.plotly_chart(fig2, use_container_width=True)
                
            with col3:
                st.markdown("**Gráfico C**")
                fig3 = generar_figura_pastel(p['datos_grafico'][2], "Gráfico C", show_text=False)
                st.plotly_chart(fig3, use_container_width=True)
            
        # Formulario para la respuesta (se crea un formulario único para cada pregunta)
        with st.form(f"form_p{i}"):
            resp = st.radio("Selecciona la respuesta:", p['opts'], key=f"q{i}_radio_final")
            
            if st.form_submit_button("Comprobar", key=f"check_p{i}_final"):
                if resp == p['resp']:
                    st.success(f"✅ ¡Correcto! {p['retro']}")
                else:
                    st.error(f"❌ Incorrecto. {p['retro']}")

st.markdown("---")

st.markdown("📧 **Contacto:** carlosdl@uninorte.edu.co")












