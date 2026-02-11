import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
from matplotlib import pyplot as plt
from matplotlib_venn import venn2, venn3
import io

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="Introducción a la Probabilidad", page_icon="🎲")

# --- FUNCIONES AUXILIARES ---

def calcular_probabilidad(favorables, totales):
    """Calcula probabilidad simple."""
    if totales == 0:
        return 0
    return favorables / totales

def generar_espacio_muestral_dado(num_dados=1):
    """Genera espacio muestral para dados."""
    if num_dados == 1:
        return list(range(1, 7))
    elif num_dados == 2:
        return [(i, j) for i in range(1, 7) for j in range(1, 7)]
    return []

def generar_espacio_muestral_moneda(num_monedas=1):
    """Genera espacio muestral para monedas."""
    if num_monedas == 1:
        return ['Cara', 'Sello']
    elif num_monedas == 2:
        return [('C', 'C'), ('C', 'S'), ('S', 'C'), ('S', 'S')]
    elif num_monedas == 3:
        return [('C', 'C', 'C'), ('C', 'C', 'S'), ('C', 'S', 'C'), ('C', 'S', 'S'),
                ('S', 'C', 'C'), ('S', 'C', 'S'), ('S', 'S', 'C'), ('S', 'S', 'S')]
    return []

def simular_lanzamientos(tipo, num_elementos, num_lanzamientos):
    """Simula lanzamientos de monedas o dados."""
    resultados = []
    if tipo == "Moneda":
        for _ in range(num_lanzamientos):
            if num_elementos == 1:
                resultados.append(random.choice(['Cara', 'Sello']))
            else:
                resultados.append(tuple(random.choice(['C', 'S']) for _ in range(num_elementos)))
    elif tipo == "Dado":
        for _ in range(num_lanzamientos):
            if num_elementos == 1:
                resultados.append(random.randint(1, 6))
            else:
                resultados.append(tuple(random.randint(1, 6) for _ in range(num_elementos)))
    return resultados

def crear_diagrama_venn_2(set_a, set_b, label_a="A", label_b="B", highlight=None):
    """Crea un diagrama de Venn para 2 conjuntos usando matplotlib."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Crear el diagrama
    v = venn2([set_a, set_b], set_labels=(label_a, label_b), ax=ax)
    
    # Colorear según lo que queremos resaltar
    if highlight == "union":
        if v.get_patch_by_id('10'):
            v.get_patch_by_id('10').set_color('lightblue')
            v.get_patch_by_id('10').set_alpha(0.7)
        if v.get_patch_by_id('01'):
            v.get_patch_by_id('01').set_color('lightblue')
            v.get_patch_by_id('01').set_alpha(0.7)
        if v.get_patch_by_id('11'):
            v.get_patch_by_id('11').set_color('lightblue')
            v.get_patch_by_id('11').set_alpha(0.7)
    elif highlight == "intersection":
        if v.get_patch_by_id('11'):
            v.get_patch_by_id('11').set_color('orange')
            v.get_patch_by_id('11').set_alpha(0.7)
    elif highlight == "A":
        if v.get_patch_by_id('10'):
            v.get_patch_by_id('10').set_color('lightgreen')
            v.get_patch_by_id('10').set_alpha(0.7)
        if v.get_patch_by_id('11'):
            v.get_patch_by_id('11').set_color('lightgreen')
            v.get_patch_by_id('11').set_alpha(0.7)
    elif highlight == "B":
        if v.get_patch_by_id('01'):
            v.get_patch_by_id('01').set_color('lightcoral')
            v.get_patch_by_id('01').set_alpha(0.7)
        if v.get_patch_by_id('11'):
            v.get_patch_by_id('11').set_color('lightcoral')
            v.get_patch_by_id('11').set_alpha(0.7)
    elif highlight == "A-B":
        if v.get_patch_by_id('10'):
            v.get_patch_by_id('10').set_color('purple')
            v.get_patch_by_id('10').set_alpha(0.7)
    
    return fig

# --- BARRA LATERAL ---
st.sidebar.title("🎲 Menú de Contenido")
st.sidebar.markdown("### Navegación")

page = st.sidebar.radio("Ir a:", [
    "1. 🏠 Inicio",
    "2. 🎯 Conceptos Fundamentales",
    "3. 🔵 Diagramas de Venn",
    "4. 📊 Probabilidad Simple",
    "5. 📐 Axiomas de Kolmogorov",
    "6. 🎮 Simulador de Experimentos",
    "7. 🏥 Casos por Carrera",
    "8. 🧮 Calculadora de Probabilidades",
    "9. 🎯 Ejercicios Interactivos",
    "10. ❓ Cuestionario Final",
    "11. 📖 Resumen y Fórmulas"
], index=0)

# --- PÁGINAS ---

if page == "1. 🏠 Inicio":
    st.title("🎲 Introducción a la Probabilidad")
    st.markdown("### Bienvenido al mundo de la incertidumbre medible")
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## ¿Qué es la Probabilidad?
        
        La **probabilidad** es una medida numérica de la **incertidumbre** de que ocurra un evento. 
        Es una herramienta fundamental que nos permite:
        
        - 🎯 **Cuantificar la incertidumbre** (de 0 a 1, o de 0% a 100%)
        - 📊 **Tomar decisiones informadas** basadas en datos
        - 🔮 **Predecir resultados** en situaciones aleatorias
        - 🧪 **Analizar experimentos** y fenómenos del mundo real
        
        ### La Escala de Probabilidad
        
        """)
        
        # Visualización de la escala
        fig_escala = go.Figure()
        
        fig_escala.add_trace(go.Bar(
            x=[0, 0.25, 0.5, 0.75, 1.0],
            y=[1, 1, 1, 1, 1],
            marker=dict(
                color=['red', 'orange', 'yellow', 'lightgreen', 'green'],
                line=dict(color='black', width=2)
            ),
            text=['Imposible<br>0', 'Poco Probable<br>0.25', 'Equiprobable<br>0.5', 'Muy Probable<br>0.75', 'Seguro<br>1.0'],
            textposition='outside',
            orientation='h',
            showlegend=False
        ))
        
        fig_escala.update_layout(
            title="Escala de Probabilidad: De lo Imposible a lo Seguro",
            xaxis=dict(title="Probabilidad", range=[0, 1.1]),
            yaxis=dict(visible=False),
            height=300,
            showlegend=False
        )
        
        st.plotly_chart(fig_escala, use_container_width=True)
        
    with col2:
        st.markdown("### 💡 Datos Curiosos")
        st.info("""
        **¿Sabías que...?**
        
        🎲 La probabilidad de obtener un 6 al lanzar un dado es $\\frac{1}{6} \\approx 0.167$
        
        🃏 La probabilidad de sacar un As de una baraja es $\\frac{4}{52} \\approx 0.077$
        
        ☂️ Si hay 70% de probabilidad de lluvia, significa que en 10 días similares, lloverá aproximadamente 7 veces
        """)
    
    st.markdown("---")
    
    st.markdown("## 🌍 La Probabilidad en Diferentes Carreras")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏥 Medicina", "⚙️ Ingeniería", "💼 Negocios", "⚖️ Derecho"])
    
    with tab1:
        st.markdown("""
        ### Medicina y Salud
        
        **Ejemplos de aplicación:**
        - 🦠 **Epidemiología**: Probabilidad de contagio de enfermedades
        - 💉 **Efectividad de vacunas**: ¿Qué tan probable es que una vacuna proteja?
        - 🧬 **Genética**: Probabilidad de heredar ciertas características
        - 🔬 **Diagnóstico**: Probabilidad de que un test sea correcto
        
        **Ejemplo práctico:**
        > Si una enfermedad afecta al 2% de la población, la probabilidad de que una persona seleccionada al azar la tenga es $P(\\text{Enfermedad}) = 0.02$
        """)
        
    with tab2:
        st.markdown("""
        ### Ingeniería
        
        **Ejemplos de aplicación:**
        - 🔧 **Control de calidad**: Probabilidad de productos defectuosos
        - 🏗️ **Confiabilidad de sistemas**: Probabilidad de fallo de componentes
        - 🌉 **Análisis de riesgos**: Probabilidad de desastres estructurales
        - 📡 **Telecomunicaciones**: Probabilidad de pérdida de señal
        
        **Ejemplo práctico:**
        > Si una máquina produce 5% de piezas defectuosas, la probabilidad de que una pieza aleatoria sea defectuosa es $P(\\text{Defectuosa}) = 0.05$
        """)
        
    with tab3:
        st.markdown("""
        ### Negocios y Finanzas
        
        **Ejemplos de aplicación:**
        - 📈 **Inversiones**: Probabilidad de ganancia o pérdida
        - 🎯 **Marketing**: Probabilidad de conversión de clientes
        - 📊 **Gestión de riesgos**: Probabilidad de incumplimiento de pagos
        - 🛒 **Comportamiento del consumidor**: Probabilidad de compra
        
        **Ejemplo práctico:**
        > Si históricamente 15% de los leads se convierten en clientes, la probabilidad de conversión es $P(\\text{Conversión}) = 0.15$
        """)
        
    with tab4:
        st.markdown("""
        ### Derecho y Ciencias Sociales
        
        **Ejemplos de aplicación:**
        - ⚖️ **Juicios**: Probabilidad de culpabilidad basada en evidencia
        - 📋 **Encuestas**: Probabilidad de que una muestra represente a la población
        - 🗳️ **Elecciones**: Probabilidad de victoria de candidatos
        - 🔍 **Criminología**: Probabilidad de reincidencia
        
        **Ejemplo práctico:**
        > Si 60% de los votantes favorecen a un candidato en una encuesta, la probabilidad de que un votante aleatorio lo favorezca es $P(\\text{Favor}) = 0.60$
        """)
    
    st.markdown("---")
    
    st.success("""
    ### 🎯 Objetivos de esta App
    
    Al finalizar este recorrido, serás capaz de:
    
    1. ✅ Identificar experimentos aleatorios y sus espacios muestrales
    2. ✅ Interpretar y construir diagramas de Venn
    3. ✅ Calcular probabilidades simples y compuestas
    4. ✅ Comprender y aplicar los axiomas de Kolmogorov
    5. ✅ Resolver problemas de probabilidad en contextos reales
    """)

elif page == "2. 🎯 Conceptos Fundamentales":
    st.title("🎯 Conceptos Fundamentales de Probabilidad")
    st.markdown("### Los bloques de construcción del pensamiento probabilístico")
    
    st.markdown("---")
    
    # --- EXPERIMENTO ALEATORIO ---
    st.header("1️⃣ Experimento Aleatorio")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### ¿Qué es un Experimento Aleatorio?
        
        Es un **proceso u observación** que cumple con dos características esenciales:
        
        1. 🔄 **Se puede repetir** bajo las mismas condiciones
        2. 🎲 **El resultado NO se puede predecir** con certeza antes de realizarlo
        
        #### Ejemplos:
        """)
        
        ejemplos_exp = pd.DataFrame({
            'Experimento': [
                '🎲 Lanzar un dado',
                '🪙 Lanzar una moneda',
                '🃏 Sacar una carta',
                '🌡️ Medir la temperatura',
                '👶 Nacimiento de un bebé',
                '🎯 Lanzar un dardo'
            ],
            '¿Es Aleatorio?': [
                '✅ SÍ',
                '✅ SÍ',
                '✅ SÍ',
                '✅ SÍ',
                '✅ SÍ',
                '✅ SÍ'
            ],
            'Razón': [
                'No sabemos qué número saldrá',
                'No sabemos si será cara o sello',
                'Depende del azar del mazo',
                'Varía según condiciones climáticas',
                'No sabemos el género con certeza',
                'Depende de múltiples factores'
            ]
        })
        
        st.dataframe(ejemplos_exp, use_container_width=True, hide_index=True)
        
    with col2:
        st.info("""
        ### ⚠️ NO es Aleatorio:
        
        - 🔢 Sumar 2 + 2
        - 🌍 La salida del sol
        - 💧 El agua hierve a 100°C
        - 📐 Área de un círculo
        
        Estos tienen **resultados determinísticos** (predecibles).
        """)
    
    st.markdown("---")
    
    # --- ESPACIO MUESTRAL ---
    st.header("2️⃣ Espacio Muestral (S)")
    
    st.markdown("""
    ### Definición
    
    El **Espacio Muestral** (denotado como $S$ o $\\Omega$) es el conjunto de **TODOS** los resultados posibles de un experimento aleatorio.
    
    ### Características:
    - 📦 Contiene **todos** los resultados posibles
    - 🎯 Cada resultado es **único** (no se repite)
    - ✅ Es **exhaustivo** (no falta ningún resultado)
    """)
    
    st.markdown("#### 🧮 Ejemplos Interactivos:")
    
    col_e1, col_e2, col_e3 = st.columns(3)
    
    with col_e1:
        st.markdown("##### 🎲 Un Dado")
        st.code("S = {1, 2, 3, 4, 5, 6}")
        st.metric("Tamaño de S", "|S| = 6")
        
        # Visualización
        fig1 = go.Figure(data=[go.Bar(
            x=[1, 2, 3, 4, 5, 6],
            y=[1, 1, 1, 1, 1, 1],
            marker_color='lightblue',
            text=[1, 2, 3, 4, 5, 6],
            textposition='inside'
        )])
        fig1.update_layout(
            title="Espacio Muestral: Un Dado",
            xaxis_title="Resultado",
            yaxis_visible=False,
            height=250,
            showlegend=False
        )
        st.plotly_chart(fig1, use_container_width=True)
        
    with col_e2:
        st.markdown("##### 🪙 Una Moneda")
        st.code("S = {Cara, Sello}")
        st.metric("Tamaño de S", "|S| = 2")
        
        # Visualización
        fig2 = go.Figure(data=[go.Bar(
            x=['Cara', 'Sello'],
            y=[1, 1],
            marker_color='lightgreen',
            text=['Cara', 'Sello'],
            textposition='inside'
        )])
        fig2.update_layout(
            title="Espacio Muestral: Una Moneda",
            xaxis_title="Resultado",
            yaxis_visible=False,
            height=250,
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)
        
    with col_e3:
        st.markdown("##### 🃏 Color de Carta")
        st.code("S = {♠, ♥, ♦, ♣}")
        st.metric("Tamaño de S", "|S| = 4")
        
        # Visualización
        fig3 = go.Figure(data=[go.Bar(
            x=['♠ Picas', '♥ Corazones', '♦ Diamantes', '♣ Tréboles'],
            y=[1, 1, 1, 1],
            marker_color=['black', 'red', 'red', 'black'],
            text=['♠', '♥', '♦', '♣'],
            textposition='inside',
            textfont=dict(size=20)
        )])
        fig3.update_layout(
            title="Espacio Muestral: Palo de Carta",
            xaxis_title="Resultado",
            yaxis_visible=False,
            height=250,
            showlegend=False
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown("---")
    
    # --- Constructor de Espacio Muestral ---
    st.subheader("🛠️ Constructor Interactivo de Espacios Muestrales")
    
    tipo_exp = st.selectbox("Selecciona un experimento:", [
        "🎲 Lanzar Dados",
        "🪙 Lanzar Monedas",
        "🃏 Baraja de Cartas",
        "👶 Género de Bebés"
    ])
    
    if tipo_exp == "🎲 Lanzar Dados":
        num_dados = st.slider("Número de dados:", 1, 2, 1)
        
        if num_dados == 1:
            S = generar_espacio_muestral_dado(1)
            st.success(f"**Espacio Muestral:** $S = \\{{{', '.join(map(str, S))}\\}}$")
            st.info(f"**Tamaño:** $|S| = {len(S)}$ resultados posibles")
            
        elif num_dados == 2:
            S = generar_espacio_muestral_dado(2)
            st.success(f"**Tamaño del Espacio Muestral:** $|S| = {len(S)}$ resultados posibles")
            
            # Mostrar en tabla
            df_dados = pd.DataFrame(S, columns=['Dado 1', 'Dado 2'])
            df_dados['Suma'] = df_dados['Dado 1'] + df_dados['Dado 2']
            
            col_tab, col_graf = st.columns(2)
            
            with col_tab:
                st.markdown("**Primeros 10 resultados:**")
                st.dataframe(df_dados.head(10), hide_index=True)
                
            with col_graf:
                # Gráfico de distribución de sumas
                sumas = df_dados['Suma'].value_counts().sort_index()
                fig_sumas = go.Figure(data=[go.Bar(
                    x=sumas.index,
                    y=sumas.values,
                    marker_color='steelblue',
                    text=sumas.values,
                    textposition='outside'
                )])
                fig_sumas.update_layout(
                    title="Frecuencia de Sumas (2 dados)",
                    xaxis_title="Suma",
                    yaxis_title="Frecuencia",
                    height=300
                )
                st.plotly_chart(fig_sumas, use_container_width=True)
                
    elif tipo_exp == "🪙 Lanzar Monedas":
        num_monedas = st.slider("Número de monedas:", 1, 3, 1)
        S = generar_espacio_muestral_moneda(num_monedas)
        
        if num_monedas == 1:
            st.success(f"**Espacio Muestral:** $S = \\{{{', '.join(S)}\\}}$")
        else:
            st.success(f"**Tamaño del Espacio Muestral:** $|S| = {len(S)}$ resultados posibles")
            st.code('\n'.join([str(resultado) for resultado in S]))
        
        st.info(f"**Tamaño:** $|S| = 2^{{{num_monedas}}} = {len(S)}$ resultados posibles")
        
    elif tipo_exp == "🃏 Baraja de Cartas":
        tipo_carta = st.radio("¿Qué quieres sacar?", [
            "Una carta cualquiera",
            "Solo el palo",
            "Solo el número/figura"
        ])
        
        if tipo_carta == "Una carta cualquiera":
            st.success("**Espacio Muestral:** 52 cartas en total")
            st.info("$|S| = 52$ (13 cartas × 4 palos)")
            
            palos = ['♠ Picas', '♥ Corazones', '♦ Diamantes', '♣ Tréboles']
            valores = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
            
            st.markdown("**Ejemplo de algunas cartas:**")
            ejemplos = [f"{val} de {palo}" for palo in palos[:2] for val in valores[:3]]
            st.code(', '.join(ejemplos) + ", ...")
            
        elif tipo_carta == "Solo el palo":
            st.success("**Espacio Muestral:** $S = \\{♠, ♥, ♦, ♣\\}$")
            st.info("$|S| = 4$ palos posibles")
            
        else:
            st.success("**Espacio Muestral:** $S = \\{A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K\\}$")
            st.info("$|S| = 13$ valores posibles")
            
    else:  # Género de Bebés
        num_bebes = st.slider("Número de bebés:", 1, 3, 1)
        
        if num_bebes == 1:
            st.success("**Espacio Muestral:** $S = \\{\\text{Masculino}, \\text{Femenino}\\}$")
            st.info("$|S| = 2$ géneros posibles")
        else:
            # Generar combinaciones
            S_bebes = []
            for i in range(2**num_bebes):
                combinacion = []
                for j in range(num_bebes):
                    if (i >> j) & 1:
                        combinacion.append('M')
                    else:
                        combinacion.append('F')
                S_bebes.append(tuple(combinacion))
            
            st.success(f"**Tamaño del Espacio Muestral:** $|S| = 2^{{{num_bebes}}} = {len(S_bebes)}$")
            st.code('\n'.join([str(resultado) for resultado in S_bebes]))
    
    st.markdown("---")
    
    # --- EVENTO ---
    st.header("3️⃣ Evento (A, B, C, ...)")
    
    st.markdown("""
    ### Definición
    
    Un **Evento** es un **subconjunto del espacio muestral** $S$. Es decir, es una colección de uno o más resultados posibles.
    
    ### Tipos de Eventos:
    """)
    
    col_tipos1, col_tipos2 = st.columns(2)
    
    with col_tipos1:
        st.markdown("""
        #### 🎯 Evento Simple
        Contiene **un solo resultado**.
        
        **Ejemplos:**
        - $A = \\{\\text{Obtener un 6 en el dado}\\} = \\{6\\}$
        - $B = \\{\\text{Sacar el As de ♠}\\}$
        """)
        
        st.markdown("""
        #### 📦 Evento Compuesto
        Contiene **dos o más resultados**.
        
        **Ejemplos:**
        - $C = \\{\\text{Número par en el dado}\\} = \\{2, 4, 6\\}$
        - $D = \\{\\text{Figura en cartas}\\} = \\{J, Q, K\\}$
        """)
        
    with col_tipos2:
        st.markdown("""
        #### ✅ Evento Seguro
        Es **igual al espacio muestral** $S$.
        
        **Ejemplo:**
        - $S = \\{\\text{Obtener cualquier número del 1 al 6}\\}$
        - $P(S) = 1$ (100% de probabilidad)
        """)
        
        st.markdown("""
        #### ❌ Evento Imposible
        Es el **conjunto vacío** $\\emptyset$ o $\\{\\}$.
        
        **Ejemplo:**
        - $\\emptyset = \\{\\text{Obtener un 7 en un dado de 6 caras}\\}$
        - $P(\\emptyset) = 0$ (0% de probabilidad)
        """)
    
    st.markdown("---")
    
    # --- VISUALIZACIÓN DE EVENTOS ---
    st.subheader("🎨 Visualización de Eventos")
    
    st.markdown("**Experimento:** Lanzar un dado de 6 caras")
    st.markdown("**Espacio Muestral:** $S = \\{1, 2, 3, 4, 5, 6\\}$")
    
    evento_sel = st.selectbox("Selecciona un evento para visualizar:", [
        "A = {Número par}",
        "B = {Número mayor que 4}",
        "C = {Número primo}",
        "D = {Múltiplo de 3}"
    ])
    
    S_dado = set(range(1, 7))
    
    if evento_sel == "A = {Número par}":
        evento = {2, 4, 6}
        descripcion = "Números pares: 2, 4, 6"
    elif evento_sel == "B = {Número mayor que 4}":
        evento = {5, 6}
        descripcion = "Números mayores que 4: 5, 6"
    elif evento_sel == "C = {Número primo}":
        evento = {2, 3, 5}
        descripcion = "Números primos: 2, 3, 5"
    else:
        evento = {3, 6}
        descripcion = "Múltiplos de 3: 3, 6"
    
    # Visualizar
    colores = ['lightgreen' if x in evento else 'lightgray' for x in S_dado]
    
    fig_evento = go.Figure(data=[go.Bar(
        x=list(S_dado),
        y=[1]*6,
        marker_color=colores,
        text=list(S_dado),
        textposition='inside',
        textfont=dict(size=20)
    )])
    
    fig_evento.update_layout(
        title=f"Evento: {evento_sel}",
        xaxis_title="Resultado del Dado",
        yaxis_visible=False,
        height=300,
        showlegend=False
    )
    
    st.plotly_chart(fig_evento, use_container_width=True)
    st.success(f"**{descripcion}**")
    st.info(f"**Tamaño del evento:** $|A| = {len(evento)}$")
    st.info(f"**Probabilidad:** $P(A) = \\frac{{{len(evento)}}}{{{len(S_dado)}}} = {len(evento)/len(S_dado):.3f}$")

elif page == "3. 🔵 Diagramas de Venn":
    st.title("🔵 Diagramas de Venn Interactivos")
    st.markdown("### Visualiza las operaciones entre eventos de manera intuitiva")
    
    st.markdown("---")
    
    # --- INTRODUCCIÓN ---
    st.markdown("""
    ## ¿Qué son los Diagramas de Venn?
    
    Los **Diagramas de Venn** son representaciones visuales que muestran las relaciones entre diferentes conjuntos (eventos).
    Son fundamentales para entender operaciones entre eventos en probabilidad.
    
    ### 🎯 Componentes Básicos:
    - 🟦 **Rectángulo externo**: Representa el Espacio Muestral ($S$)
    - 🔵 **Círculos**: Representan eventos individuales ($A$, $B$, $C$, ...)
    - 🎨 **Áreas sombreadas**: Muestran el resultado de operaciones
    """)
    
    st.markdown("---")
    
    # --- OPERACIONES BÁSICAS ---
    st.header("📐 Operaciones entre Eventos")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔵 Evento A",
        "🟠 Unión (A ∪ B)",
        "🟢 Intersección (A ∩ B)",
        "🟣 Diferencia (A - B)",
        "⚪ Complemento (A')"
    ])
    
    with tab1:
        st.markdown("""
        ### Evento Individual A
        
        Es simplemente el evento $A$ por sí solo, que contiene todos los resultados que pertenecen a $A$.
        
        **Notación:** $A$
        
        **Ejemplo:** En una baraja de cartas:
        - $A = \\{\\text{Sacar una carta roja}\\}$
        """)
        
        # Crear ejemplo
        S_ejemplo = set(range(1, 11))  # Espacio muestral {1,2,3,...,10}
        A_ejemplo = {2, 4, 6, 8}  # Números pares
        
        st.code(f"S = {S_ejemplo}\nA = {A_ejemplo}")
        
        try:
            fig_A = crear_diagrama_venn_2(A_ejemplo, set(), label_a="A", label_b="", highlight="A")
            st.pyplot(fig_A)
        except:
            st.info("Visualización del evento A (números pares del 1 al 10)")
        
        st.success(f"**Cardinalidad:** $|A| = {len(A_ejemplo)}$ elementos")
        
    with tab2:
        st.markdown("""
        ### Unión de Eventos (A ∪ B)
        
        La **unión** de dos eventos $A$ y $B$ es el evento que ocurre cuando **al menos uno** de los dos eventos sucede.
        
        **Notación:** $A \\cup B$ (se lee "A unión B")
        
        **Definición formal:** $A \\cup B = \\{x : x \\in A \\text{ o } x \\in B\\}$
        
        **Palabra clave:** **"O"** (inclusivo)
        
        ### Ejemplos por Carrera:
        """)
        
        col_med, col_ing = st.columns(2)
        
        with col_med:
            st.markdown("""
            **🏥 Medicina:**
            - $A = \\{\\text{Paciente con fiebre}\\}$
            - $B = \\{\\text{Paciente con tos}\\}$
            - $A \\cup B = \\{\\text{Paciente con fiebre O tos (o ambas)}\\}$
            """)
            
        with col_ing:
            st.markdown("""
            **⚙️ Ingeniería:**
            - $A = \\{\\text{Pieza con defecto tipo 1}\\}$
            - $B = \\{\\text{Pieza con defecto tipo 2}\\}$
            - $A \\cup B = \\{\\text{Pieza con al menos un defecto}\\}$
            """)
        
        # Ejemplo numérico
        st.markdown("#### 🧮 Ejemplo Numérico:")
        A_union = {1, 2, 3, 4}
        B_union = {3, 4, 5, 6}
        
        st.code(f"A = {A_union}\nB = {B_union}\nA ∪ B = {A_union.union(B_union)}")
        
        try:
            fig_union = crear_diagrama_venn_2(A_union, B_union, label_a="A", label_b="B", highlight="union")
            st.pyplot(fig_union)
        except:
            st.info("La unión incluye todos los elementos que están en A, en B, o en ambos")
        
        st.success(f"**Resultado:** $A \\cup B = {A_union.union(B_union)}$")
        st.info(f"**Tamaño:** $|A \\cup B| = {len(A_union.union(B_union))}$ elementos")
        
    with tab3:
        st.markdown("""
        ### Intersección de Eventos (A ∩ B)
        
        La **intersección** de dos eventos $A$ y $B$ es el evento que ocurre cuando **ambos eventos suceden simultáneamente**.
        
        **Notación:** $A \\cap B$ (se lee "A intersección B")
        
        **Definición formal:** $A \\cap B = \\{x : x \\in A \\text{ y } x \\in B\\}$
        
        **Palabra clave:** **"Y"** (ambos a la vez)
        
        ### Ejemplos por Carrera:
        """)
        
        col_neg, col_der = st.columns(2)
        
        with col_neg:
            st.markdown("""
            **💼 Negocios:**
            - $A = \\{\\text{Cliente satisfecho}\\}$
            - $B = \\{\\text{Cliente que recomienda}\\}$
            - $A \\cap B = \\{\\text{Cliente satisfecho Y que recomienda}\\}$
            """)
            
        with col_der:
            st.markdown("""
            **⚖️ Derecho:**
            - $A = \\{\\text{Evidencia tipo A presente}\\}$
            - $B = \\{\\text{Evidencia tipo B presente}\\}$
            - $A \\cap B = \\{\\text{Ambas evidencias presentes}\\}$
            """)
        
        # Ejemplo numérico
        st.markdown("#### 🧮 Ejemplo Numérico:")
        A_inter = {1, 2, 3, 4, 5}
        B_inter = {3, 4, 5, 6, 7}
        
        st.code(f"A = {A_inter}\nB = {B_inter}\nA ∩ B = {A_inter.intersection(B_inter)}")
        
        try:
            fig_inter = crear_diagrama_venn_2(A_inter, B_inter, label_a="A", label_b="B", highlight="intersection")
            st.pyplot(fig_inter)
        except:
            st.info("La intersección incluye solo los elementos que están en AMBOS conjuntos")
        
        st.success(f"**Resultado:** $A \\cap B = {A_inter.intersection(B_inter)}$")
        st.info(f"**Tamaño:** $|A \\cap B| = {len(A_inter.intersection(B_inter))}$ elementos")
        
        st.markdown("---")
        st.markdown("### 🚫 Eventos Mutuamente Excluyentes")
        st.warning("""
        Dos eventos son **mutuamente excluyentes** (o disjuntos) si **NO pueden ocurrir simultáneamente**.
        
        **Formalmente:** $A \\cap B = \\emptyset$ (la intersección es vacía)
        
        **Ejemplo:** Al lanzar un dado:
        - $A = \\{\\text{Obtener número par}\\} = \\{2, 4, 6\\}$
        - $B = \\{\\text{Obtener número impar}\\} = \\{1, 3, 5\\}$
        - $A \\cap B = \\emptyset$ ✅ Son mutuamente excluyentes
        """)
        
    with tab4:
        st.markdown("""
        ### Diferencia de Eventos (A - B)
        
        La **diferencia** entre $A$ y $B$ es el evento que contiene los elementos que están en $A$ pero **NO** están en $B$.
        
        **Notación:** $A - B$ o $A \\setminus B$ (se lee "A menos B")
        
        **Definición formal:** $A - B = \\{x : x \\in A \\text{ y } x \\notin B\\}$
        
        **Palabra clave:** "En A pero NO en B"
        
        ### Ejemplos por Carrera:
        """)
        
        col_med2, col_ing2 = st.columns(2)
        
        with col_med2:
            st.markdown("""
            **🏥 Medicina:**
            - $A = \\{\\text{Pacientes con síntomas}\\}$
            - $B = \\{\\text{Pacientes diagnosticados}\\}$
            - $A - B = \\{\\text{Pacientes con síntomas pero sin diagnóstico}\\}$
            """)
            
        with col_ing2:
            st.markdown("""
            **⚙️ Ingeniería:**
            - $A = \\{\\text{Piezas producidas}\\}$
            - $B = \\{\\text{Piezas defectuosas}\\}$
            - $A - B = \\{\\text{Piezas producidas sin defectos}\\}$
            """)
        
        # Ejemplo numérico
        st.markdown("#### 🧮 Ejemplo Numérico:")
        A_dif = {1, 2, 3, 4, 5}
        B_dif = {3, 4, 5, 6, 7}
        
        st.code(f"A = {A_dif}\nB = {B_dif}\nA - B = {A_dif.difference(B_dif)}")
        
        try:
            fig_dif = crear_diagrama_venn_2(A_dif, B_dif, label_a="A", label_b="B", highlight="A-B")
            st.pyplot(fig_dif)
        except:
            st.info("La diferencia A - B incluye solo los elementos exclusivos de A")
        
        st.success(f"**Resultado:** $A - B = {A_dif.difference(B_dif)}$")
        st.info(f"**Tamaño:** $|A - B| = {len(A_dif.difference(B_dif))}$ elementos")
        
        st.warning("""
        ⚠️ **Nota Importante:** 
        
        $A - B \\neq B - A$ (la diferencia NO es conmutativa)
        
        En este ejemplo: $B - A = \\{6, 7\\}$ (elementos en B pero no en A)
        """)
        
    with tab5:
        st.markdown("""
        ### Complemento de un Evento (A')
        
        El **complemento** de un evento $A$ es el evento que contiene **todos** los resultados del espacio muestral que **NO** están en $A$.
        
        **Notación:** $A'$, $A^c$, o $\\overline{A}$ (se lee "A complemento")
        
        **Definición formal:** $A' = \\{x : x \\in S \\text{ y } x \\notin A\\} = S - A$
        
        **Palabra clave:** "TODO lo que NO es A"
        
        ### Propiedades Importantes:
        """)
        
        col_prop1, col_prop2 = st.columns(2)
        
        with col_prop1:
            st.info("""
            **Propiedad 1:**
            
            $A \\cup A' = S$
            
            (A junto con su complemento cubren todo el espacio muestral)
            """)
            
        with col_prop2:
            st.info("""
            **Propiedad 2:**
            
            $A \\cap A' = \\emptyset$
            
            (A y su complemento son mutuamente excluyentes)
            """)
        
        st.success("""
        **Propiedad Probabilística:**
        
        $P(A') = 1 - P(A)$
        
        Esta es una de las fórmulas más útiles en probabilidad.
        """)
        
        # Ejemplo numérico
        st.markdown("#### 🧮 Ejemplo Numérico:")
        st.markdown("**Experimento:** Lanzar un dado de 6 caras")
        
        S_comp = {1, 2, 3, 4, 5, 6}
        A_comp = {2, 4, 6}  # Números pares
        A_comp_complemento = S_comp.difference(A_comp)
        
        st.code(f"S = {S_comp}\nA = {A_comp} (números pares)\nA' = {A_comp_complemento} (números impares)")
        
        # Visualización con barras
        resultados = list(S_comp)
        colores = ['lightcoral' if x in A_comp_complemento else 'lightblue' for x in resultados]
        
        fig_comp = go.Figure(data=[go.Bar(
            x=resultados,
            y=[1]*6,
            marker_color=colores,
            text=resultados,
            textposition='inside',
            textfont=dict(size=20)
        )])
        
        fig_comp.update_layout(
            title="Evento A (azul) y su Complemento A' (rojo)",
            xaxis_title="Resultado del Dado",
            yaxis_visible=False,
            height=300,
            showlegend=False
        )
        
        st.plotly_chart(fig_comp, use_container_width=True)
        
        st.success(f"**Resultado:** $A' = {A_comp_complemento}$")
        st.info(f"**Verificación:** $|A| + |A'| = {len(A_comp)} + {len(A_comp_complemento)} = {len(S_comp)} = |S|$ ✓")
        
        # Ejemplos por carrera
        st.markdown("### Ejemplos por Carrera:")
        
        ejemplos_comp = pd.DataFrame({
            'Carrera': ['🏥 Medicina', '⚙️ Ingeniería', '💼 Negocios', '⚖️ Derecho'],
            'Evento A': [
                'Paciente sano',
                'Pieza aprobada',
                'Cliente compra',
                'Veredicto culpable'
            ],
            'Complemento A\'': [
                'Paciente enfermo',
                'Pieza rechazada',
                'Cliente NO compra',
                'Veredicto NO culpable'
            ]
        })
        
        st.table(ejemplos_comp.set_index('Carrera'))
    
    st.markdown("---")
    
    # --- CONSTRUCTOR INTERACTIVO ---
    st.header("🛠️ Constructor Interactivo de Diagramas de Venn")
    
    st.markdown("### Define tus propios conjuntos y visualiza las operaciones")
    
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        st.markdown("#### Conjunto A")
        input_A = st.text_input(
            "Elementos de A (separados por comas):",
            value="1, 2, 3, 4, 5",
            key="input_A"
        )
        
    with col_input2:
        st.markdown("#### Conjunto B")
        input_B = st.text_input(
            "Elementos de B (separados por comas):",
            value="3, 4, 5, 6, 7",
            key="input_B"
        )
    
    try:
        # Procesar inputs
        A_custom = set([int(x.strip()) for x in input_A.split(',')])
        B_custom = set([int(x.strip()) for x in input_B.split(',')])
        
        st.markdown("### Tus Conjuntos:")
        col_show1, col_show2 = st.columns(2)
        
        with col_show1:
            st.code(f"A = {sorted(A_custom)}")
            st.metric("Cardinalidad |A|", len(A_custom))
            
        with col_show2:
            st.code(f"B = {sorted(B_custom)}")
            st.metric("Cardinalidad |B|", len(B_custom))
        
        # Operación a visualizar
        operacion = st.selectbox(
            "Selecciona la operación a visualizar:",
            [
                "A ∪ B (Unión)",
                "A ∩ B (Intersección)",
                "A - B (Diferencia)",
                "B - A (Diferencia inversa)",
                "Solo A",
                "Solo B"
            ]
        )
        
        # Calcular resultado
        if operacion == "A ∪ B (Unión)":
            resultado = A_custom.union(B_custom)
            highlight_type = "union"
            formula = "$A \\cup B$"
        elif operacion == "A ∩ B (Intersección)":
            resultado = A_custom.intersection(B_custom)
            highlight_type = "intersection"
            formula = "$A \\cap B$"
        elif operacion == "A - B (Diferencia)":
            resultado = A_custom.difference(B_custom)
            highlight_type = "A-B"
            formula = "$A - B$"
        elif operacion == "B - A (Diferencia inversa)":
            resultado = B_custom.difference(A_custom)
            highlight_type = "B-A"
            formula = "$B - A$"
        elif operacion == "Solo A":
            resultado = A_custom
            highlight_type = "A"
            formula = "$A$"
        else:
            resultado = B_custom
            highlight_type = "B"
            formula = "$B$"
        
        # Mostrar resultado
        st.success(f"**Resultado de {formula}:** {sorted(resultado)}")
        st.info(f"**Cardinalidad:** $|\\text{{Resultado}}| = {len(resultado)}$")
        
        # Diagrama de Venn
        try:
            if highlight_type in ["A-B", "B-A"]:
                # Para diferencias, ajustar el highlight
                if highlight_type == "A-B":
                    fig_custom = crear_diagrama_venn_2(A_custom, B_custom, label_a="A", label_b="B", highlight="A-B")
                else:
                    # Para B-A, invertir los conjuntos y usar el highlight A-B
                    fig_custom = crear_diagrama_venn_2(B_custom, A_custom, label_a="B", label_b="A", highlight="A-B")
            else:
                fig_custom = crear_diagrama_venn_2(A_custom, B_custom, label_a="A", label_b="B", highlight=highlight_type)
            
            st.pyplot(fig_custom)
        except Exception as e:
            st.warning("No se pudo generar el diagrama de Venn para estos conjuntos. Verifica que haya intersección o diferencias.")
        
    except Exception as e:
        st.error("⚠️ Error: Asegúrate de ingresar números enteros separados por comas.")
    
    st.markdown("---")
    
    # --- LEYES DE DE MORGAN ---
    st.header("🎓 Leyes de De Morgan")
    
    st.markdown("""
    Las **Leyes de De Morgan** son dos reglas fundamentales que relacionan las operaciones de unión, intersección y complemento:
    """)
    
    col_ley1, col_ley2 = st.columns(2)
    
    with col_ley1:
        st.info("""
        ### Primera Ley:
        
        $(A \\cup B)' = A' \\cap B'$
        
        "El complemento de la unión es igual a la intersección de los complementos"
        
        **En palabras:** Los elementos que NO están en A ni en B son los mismos que están fuera de A Y fuera de B.
        """)
        
    with col_ley2:
        st.info("""
        ### Segunda Ley:
        
        $(A \\cap B)' = A' \\cup B'$
        
        "El complemento de la intersección es igual a la unión de los complementos"
        
        **En palabras:** Los elementos que NO están en ambos (A y B) son los que están fuera de A O fuera de B.
        """)
    
    # Ejemplo verificable
    st.markdown("#### 🧪 Verificación con Ejemplo:")
    
    S_morgan = {1, 2, 3, 4, 5, 6, 7, 8}
    A_morgan = {1, 2, 3, 4}
    B_morgan = {3, 4, 5, 6}
    
    st.code(f"S = {S_morgan}\nA = {A_morgan}\nB = {B_morgan}")
    
    # Primera ley
    union_AB = A_morgan.union(B_morgan)
    comp_union = S_morgan.difference(union_AB)
    
    comp_A = S_morgan.difference(A_morgan)
    comp_B = S_morgan.difference(B_morgan)
    inter_comp = comp_A.intersection(comp_B)
    
    st.markdown("**Verificando Primera Ley:**")
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        st.code(f"(A ∪ B)' = {sorted(comp_union)}")
    with col_v2:
        st.code(f"A' ∩ B' = {sorted(inter_comp)}")
    
    if comp_union == inter_comp:
        st.success("✅ ¡Primera Ley verificada!")
    
    # Segunda ley
    inter_AB = A_morgan.intersection(B_morgan)
    comp_inter = S_morgan.difference(inter_AB)
    
    union_comp = comp_A.union(comp_B)
    
    st.markdown("**Verificando Segunda Ley:**")
    col_v3, col_v4 = st.columns(2)
    
    with col_v3:
        st.code(f"(A ∩ B)' = {sorted(comp_inter)}")
    with col_v4:
        st.code(f"A' ∪ B' = {sorted(union_comp)}")
    
    if comp_inter == union_comp:
        st.success("✅ ¡Segunda Ley verificada!")

elif page == "4. 📊 Probabilidad Simple":
    st.title("📊 Probabilidad Simple")
    st.markdown("### La fórmula fundamental de la probabilidad")
    
    st.markdown("---")
    
    # --- DEFINICIÓN ---
    st.header("📐 Definición Clásica de Probabilidad")
    
    st.markdown("""
    La **probabilidad** de un evento $A$ se calcula como:
    """)
    
    st.latex(r"P(A) = \frac{\text{Número de casos favorables a } A}{\text{Número total de casos posibles}} = \frac{|A|}{|S|}")
    
    col_def1, col_def2 = st.columns([2, 1])
    
    with col_def1:
        st.markdown("""
        ### Condiciones para usar esta fórmula:
        
        1. ✅ Todos los resultados en $S$ deben ser **igualmente probables**
        2. ✅ El espacio muestral $S$ debe ser **finito**
        3. ✅ Los casos favorables deben estar **bien definidos**
        
        ### Propiedades de la Probabilidad:
        
        - 📏 **Rango:** $0 \\leq P(A) \\leq 1$ (siempre entre 0 y 1)
        - ❌ **Evento imposible:** $P(\\emptyset) = 0$
        - ✅ **Evento seguro:** $P(S) = 1$
        - 📊 **En porcentaje:** Multiplica por 100 para obtener el %
        """)
        
    with col_def2:
        st.info("""
        ### 💡 Interpretación:
        
        Si $P(A) = 0.25$:
        
        - En **4 repeticiones** esperamos que ocurra **1 vez**
        
        - Es un **25%** de probabilidad
        
        - Equivale a **1 de cada 4** veces        """)
    
    st.markdown("---")
    
    # --- EJEMPLOS BÁSICOS ---
    st.header("🎲 Ejemplos Básicos Paso a Paso")
    
    ejemplo_basico = st.selectbox(
        "Selecciona un ejemplo:",
        [
            "🎲 Dado de 6 caras",
            "🪙 Moneda",
            "🃏 Baraja de 52 cartas",
            "🎱 Urna con bolas"
        ]
    )
    
    if ejemplo_basico == "🎲 Dado de 6 caras":
        st.markdown("### Experimento: Lanzar un dado de 6 caras")
        
        col_e1, col_e2 = st.columns(2)
        
        with col_e1:
            st.markdown("**Espacio Muestral:**")
            st.code("S = {1, 2, 3, 4, 5, 6}")
            st.metric("Tamaño de S", "|S| = 6")
            
        with col_e2:
            evento_dado = st.selectbox(
                "Evento a calcular:",
                [
                    "Obtener un 4",
                    "Obtener un número par",
                    "Obtener un número mayor que 4",
                    "Obtener un número primo"
                ]
            )
        
        S_dado = {1, 2, 3, 4, 5, 6}
        
        if evento_dado == "Obtener un 4":
            A = {4}
            descripcion = "Solo el número 4"
        elif evento_dado == "Obtener un número par":
            A = {2, 4, 6}
            descripcion = "Números pares: 2, 4, 6"
        elif evento_dado == "Obtener un número mayor que 4":
            A = {5, 6}
            descripcion = "Números mayores que 4: 5 y 6"
        else:
            A = {2, 3, 5}
            descripcion = "Números primos: 2, 3, 5"
        
        st.markdown(f"**Evento A:** {descripcion}")
        st.code(f"A = {sorted(A)}")
        
        # Cálculo
        prob = len(A) / len(S_dado)
        
        st.markdown("### 📝 Cálculo Paso a Paso:")
        st.latex(f"P(A) = \\frac{{|A|}}{{|S|}} = \\frac{{{len(A)}}}{{{len(S_dado)}}} = {prob:.4f}")
        
        st.success(f"### ✅ Respuesta: $P(A) = {prob:.4f}$ o **{prob*100:.2f}%**")
        
        # Visualización
        colores = ['lightgreen' if x in A else 'lightgray' for x in S_dado]
        
        fig_dado_prob = go.Figure(data=[go.Bar(
            x=list(S_dado),
            y=[1]*6,
            marker_color=colores,
            text=list(S_dado),
            textposition='inside',
            textfont=dict(size=20)
        )])
        
        fig_dado_prob.update_layout(
            title=f"Evento: {evento_dado}",
            xaxis_title="Resultado del Dado",
            yaxis_visible=False,
            height=300
        )
        
        st.plotly_chart(fig_dado_prob, use_container_width=True)
        
        st.info(f"""
        **Interpretación:** Si lanzamos el dado muchas veces, esperamos que este evento ocurra 
        aproximadamente **{prob*100:.2f}%** de las veces.
        """)
        
    elif ejemplo_basico == "🪙 Moneda":
        st.markdown("### Experimento: Lanzar una moneda")
        
        num_monedas = st.radio("Número de monedas:", [1, 2, 3], horizontal=True)
        
        if num_monedas == 1:
            S_moneda = {'Cara', 'Sello'}
            st.code("S = {Cara, Sello}")
            st.metric("Tamaño de S", "|S| = 2")
            
            evento_moneda = st.radio("Evento:", ["Obtener Cara", "Obtener Sello"])
            
            if evento_moneda == "Obtener Cara":
                A = {'Cara'}
            else:
                A = {'Sello'}
            
            prob = 1/2
            
            st.latex(f"P(\\text{{{evento_moneda}}}) = \\frac{{1}}{{2}} = 0.5 = 50\\%")
            st.success(f"### ✅ Probabilidad: **50%** (equiprobable)")
            
        elif num_monedas == 2:
            S_moneda = {('C', 'C'), ('C', 'S'), ('S', 'C'), ('S', 'S')}
            st.code("S = {(C,C), (C,S), (S,C), (S,S)}")
            st.metric("Tamaño de S", "|S| = 4")
            
            evento_moneda = st.selectbox(
                "Evento:",
                [
                    "Exactamente 2 caras",
                    "Al menos 1 cara",
                    "Exactamente 1 cara",
                    "Ninguna cara (2 sellos)"
                ]
            )
            
            if evento_moneda == "Exactamente 2 caras":
                A = {('C', 'C')}
            elif evento_moneda == "Al menos 1 cara":
                A = {('C', 'C'), ('C', 'S'), ('S', 'C')}
            elif evento_moneda == "Exactamente 1 cara":
                A = {('C', 'S'), ('S', 'C')}
            else:
                A = {('S', 'S')}
            
            prob = len(A) / 4
            
            st.code(f"A = {A}")
            st.latex(f"P(A) = \\frac{{{len(A)}}}{{4}} = {prob:.4f} = {prob*100:.1f}\\%")
            st.success(f"### ✅ Probabilidad: **{prob*100:.1f}%**")
            
        else:  # 3 monedas
            S_moneda = generar_espacio_muestral_moneda(3)
            st.code(f"S tiene {len(S_moneda)} elementos")
            st.metric("Tamaño de S", f"|S| = {len(S_moneda)}")
            
            evento_moneda = st.selectbox(
                "Evento:",
                [
                    "Exactamente 3 caras",
                    "Al menos 2 caras",
                    "Exactamente 2 caras"
                ]
            )
            
            if evento_moneda == "Exactamente 3 caras":
                A = {('C', 'C', 'C')}
            elif evento_moneda == "Al menos 2 caras":
                A = {('C', 'C', 'C'), ('C', 'C', 'S'), ('C', 'S', 'C'), ('S', 'C', 'C')}
            else:
                A = {('C', 'C', 'S'), ('C', 'S', 'C'), ('S', 'C', 'C')}
            
            prob = len(A) / len(S_moneda)
            
            st.code(f"|A| = {len(A)}")
            st.latex(f"P(A) = \\frac{{{len(A)}}}{{{len(S_moneda)}}} = {prob:.4f} = {prob*100:.2f}\\%")
            st.success(f"### ✅ Probabilidad: **{prob*100:.2f}%**")
    
    elif ejemplo_basico == "🃏 Baraja de 52 cartas":
        st.markdown("### Experimento: Sacar una carta de una baraja estándar")
        
        st.info("""
        **Composición de la baraja:**
        - 52 cartas en total
        - 4 palos: ♠ Picas, ♥ Corazones, ♦ Diamantes, ♣ Tréboles
        - 13 valores por palo: A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K
        - 26 cartas rojas (♥ y ♦)
        - 26 cartas negras (♠ y ♣)
        """)
        
        evento_carta = st.selectbox(
            "Calcular probabilidad de:",
            [
                "Sacar un As",
                "Sacar una carta roja",
                "Sacar una figura (J, Q, K)",
                "Sacar el As de ♠",
                "Sacar un corazón (♥)",
                "Sacar un número par (2,4,6,8,10)"
            ]
        )
        
        S_cartas = 52
        
        if evento_carta == "Sacar un As":
            favorables = 4
            explicacion = "Hay 4 Ases (uno por palo)"
        elif evento_carta == "Sacar una carta roja":
            favorables = 26
            explicacion = "Hay 26 cartas rojas (13 ♥ + 13 ♦)"
        elif evento_carta == "Sacar una figura (J, Q, K)":
            favorables = 12
            explicacion = "Hay 3 figuras × 4 palos = 12 figuras"
        elif evento_carta == "Sacar el As de ♠":
            favorables = 1
            explicacion = "Solo hay 1 As de Picas"
        elif evento_carta == "Sacar un corazón (♥)":
            favorables = 13
            explicacion = "Hay 13 cartas de corazones"
        else:
            favorables = 20
            explicacion = "Hay 5 números pares × 4 palos = 20 cartas"
        
        prob = favorables / S_cartas
        
        st.markdown(f"**Explicación:** {explicacion}")
        
        st.latex(f"P(A) = \\frac{{{favorables}}}{{{S_cartas}}} = {prob:.4f} = {prob*100:.2f}\\%")
        
        st.success(f"### ✅ Probabilidad: **{prob:.4f}** ({prob*100:.2f}%)")
        
        # Visualización con pie chart
        fig_carta = go.Figure(data=[go.Pie(
            labels=['Casos Favorables', 'Casos No Favorables'],
            values=[favorables, S_cartas - favorables],
            marker=dict(colors=['lightgreen', 'lightcoral']),
            hole=0.3
        )])
        
        fig_carta.update_layout(
            title=f"Proporción: {evento_carta}",
            height=400
        )
        
        st.plotly_chart(fig_carta, use_container_width=True)
        
    else:  # Urna con bolas
        st.markdown("### Experimento: Sacar una bola de una urna")
        
        col_urna1, col_urna2, col_urna3 = st.columns(3)
        
        with col_urna1:
            bolas_rojas = st.number_input("Bolas rojas 🔴:", min_value=0, max_value=50, value=5)
        with col_urna2:
            bolas_azules = st.number_input("Bolas azules 🔵:", min_value=0, max_value=50, value=3)
        with col_urna3:
            bolas_verdes = st.number_input("Bolas verdes 🟢:", min_value=0, max_value=50, value=2)
        
        total_bolas = bolas_rojas + bolas_azules + bolas_verdes
        
        if total_bolas > 0:
            st.metric("Total de bolas en la urna", total_bolas)
            
            color_sacar = st.radio(
                "¿Qué color quieres sacar?",
                ["🔴 Roja", "🔵 Azul", "🟢 Verde"],
                horizontal=True
            )
            
            if color_sacar == "🔴 Roja":
                favorables = bolas_rojas
            elif color_sacar == "🔵 Azul":
                favorables = bolas_azules
            else:
                favorables = bolas_verdes
            
            prob = favorables / total_bolas if total_bolas > 0 else 0
            
            st.latex(f"P(\\text{{{color_sacar}}}) = \\frac{{{favorables}}}{{{total_bolas}}} = {prob:.4f} = {prob*100:.2f}\\%")
            
            st.success(f"### ✅ Probabilidad de sacar {color_sacar}: **{prob:.4f}** ({prob*100:.2f}%)")
            
            # Gráfico de barras
            fig_urna = go.Figure(data=[go.Bar(
                x=['Rojas 🔴', 'Azules 🔵', 'Verdes 🟢'],
                y=[bolas_rojas, bolas_azules, bolas_verdes],
                marker_color=['red', 'blue', 'green'],
                text=[bolas_rojas, bolas_azules, bolas_verdes],
                textposition='outside'
            )])
            
            fig_urna.update_layout(
                title="Composición de la Urna",
                yaxis_title="Cantidad de Bolas",
                height=400
            )
            
            st.plotly_chart(fig_urna, use_container_width=True)
        else:
            st.warning("⚠️ Agrega al menos una bola a la urna")
    
    st.markdown("---")
    
    # --- CASOS POR CARRERA ---
    st.header("🎓 Ejemplos por Carrera")
    
    carrera_prob = st.selectbox(
        "Selecciona una carrera:",
        ["🏥 Medicina", "⚙️ Ingeniería", "💼 Negocios", "⚖️ Derecho"]
    )
    
    if carrera_prob == "🏥 Medicina":
        st.markdown("### Caso Médico: Diagnóstico de Enfermedad")
        
        st.markdown("""
        **Contexto:** Un hospital tiene registros de 1000 pacientes que se hicieron una prueba.
        Los resultados son:
        """)
        
        col_med1, col_med2 = st.columns(2)
        
        with col_med1:
            enfermos = st.number_input("Pacientes enfermos:", min_value=0, max_value=1000, value=50)
        with col_med2:
            sanos = 1000 - enfermos
            st.metric("Pacientes sanos", sanos)
        
        st.markdown("**Preguntas:**")
        
        # Pregunta 1
        st.markdown("**1. ¿Cuál es la probabilidad de que un paciente aleatorio esté enfermo?**")
        
        prob_enfermo = enfermos / 1000
        
        st.latex(f"P(\\text{{Enfermo}}) = \\frac{{{enfermos}}}{{1000}} = {prob_enfermo:.4f} = {prob_enfermo*100:.2f}\\%")
        
        st.success(f"✅ **Respuesta:** {prob_enfermo:.4f} o {prob_enfermo*100:.2f}%")
        
        # Pregunta 2
        st.markdown("**2. ¿Cuál es la probabilidad de que esté sano? (usando complemento)**")
        
        prob_sano = 1 - prob_enfermo
        
        st.latex(f"P(\\text{{Sano}}) = 1 - P(\\text{{Enfermo}}) = 1 - {prob_enfermo:.4f} = {prob_sano:.4f}")
        
        st.success(f"✅ **Respuesta:** {prob_sano:.4f} o {prob_sano*100:.2f}%")
        
        # Visualización
        fig_med = go.Figure(data=[go.Pie(
            labels=['Enfermos', 'Sanos'],
            values=[enfermos, sanos],
            marker=dict(colors=['#ff6b6b', '#51cf66']),
            textinfo='label+percent',
            hole=0.4
        )])
        
        fig_med.update_layout(
            title="Distribución de Pacientes",
            height=400
        )
        
        st.plotly_chart(fig_med, use_container_width=True)
        
    elif carrera_prob == "⚙️ Ingeniería":
        st.markdown("### Caso Ingeniería: Control de Calidad")
        
        st.markdown("""
        **Contexto:** Una fábrica produce piezas mecánicas. En un lote de producción se inspeccionan 500 piezas.
        """)
        
        col_ing1, col_ing2 = st.columns(2)
        
        with col_ing1:
            defectuosas = st.number_input("Piezas defectuosas:", min_value=0, max_value=500, value=15)
        with col_ing2:
            aprobadas = 500 - defectuosas
            st.metric("Piezas aprobadas", aprobadas)
        
        st.markdown("**Preguntas:**")
        
        # Pregunta 1
        st.markdown("**1. ¿Cuál es la probabilidad de que una pieza seleccionada al azar sea defectuosa?**")
        
        prob_defect = defectuosas / 500
        
        st.latex(f"P(\\text{{Defectuosa}}) = \\frac{{{defectuosas}}}{{500}} = {prob_defect:.4f} = {prob_defect*100:.2f}\\%")
        
        st.success(f"✅ **Respuesta:** {prob_defect:.4f} ({prob_defect*100:.2f}%)")
        
        if prob_defect <= 0.05:
            st.info("✅ La tasa de defectos está dentro del estándar aceptable (≤5%)")
        else:
            st.warning("⚠️ La tasa de defectos excede el estándar aceptable (>5%). Se requiere revisar el proceso.")
        
        # Pregunta 2
        st.markdown("**2. ¿Cuál es la probabilidad de que una pieza sea aprobada?**")
        
        prob_aprobada = 1 - prob_defect
        
        st.latex(f"P(\\text{{Aprobada}}) = 1 - P(\\text{{Defectuosa}}) = {prob_aprobada:.4f} = {prob_aprobada*100:.2f}\\%")
        
        st.success(f"✅ **Respuesta:** {prob_aprobada:.4f} ({prob_aprobada*100:.2f}%)")
        
        # Visualización
        fig_ing = go.Figure(data=[go.Bar(
            x=['Aprobadas', 'Defectuosas'],
            y=[aprobadas, defectuosas],
            marker_color=['#51cf66', '#ff6b6b'],
            text=[aprobadas, defectuosas],
            textposition='outside'
        )])
        
        fig_ing.update_layout(
            title="Control de Calidad del Lote",
            yaxis_title="Cantidad de Piezas",
            height=400
        )
        
        st.plotly_chart(fig_ing, use_container_width=True)
        
    elif carrera_prob == "💼 Negocios":
        st.markdown("### Caso Negocios: Conversión de Ventas")
        
        st.markdown("""
        **Contexto:** Una empresa de e-commerce registró las visitas a su sitio web durante el último mes.
        """)
        
        col_neg1, col_neg2, col_neg3 = st.columns(3)
        
        with col_neg1:
            visitantes = st.number_input("Total de visitantes:", min_value=1, max_value=100000, value=5000)
        with col_neg2:
            compraron = st.number_input("Visitantes que compraron:", min_value=0, max_value=visitantes, value=150)
        with col_neg3:
            no_compraron = visitantes - compraron
            st.metric("No compraron", no_compraron)
        
        st.markdown("**Análisis:**")
        
        # Tasa de conversión
        st.markdown("**1. ¿Cuál es la tasa de conversión (probabilidad de compra)?**")
        
        prob_compra = compraron / visitantes if visitantes > 0 else 0
        
        st.latex(f"P(\\text{{Compra}}) = \\frac{{{compraron}}}{{{visitantes}}} = {prob_compra:.4f} = {prob_compra*100:.2f}\\%")
        
        st.success(f"✅ **Tasa de Conversión:** {prob_compra*100:.2f}%")
        
        # Interpretación
        if prob_compra >= 0.05:
            st.info("✅ Excelente tasa de conversión (≥5%)")
        elif prob_compra >= 0.02:
            st.info("🟡 Tasa de conversión promedio (2-5%)")
        else:
            st.warning("⚠️ Tasa de conversión baja (<2%). Considera optimizar el embudo de ventas.")
        
        # Pregunta 2
        st.markdown("**2. Si llegan 1000 nuevos visitantes, ¿cuántos se espera que compren?**")
        
        esperados = int(1000 * prob_compra)
        
        st.success(f"✅ **Respuesta:** Se esperan aproximadamente **{esperados} compras**")
        
        st.latex(f"\\text{{Compras esperadas}} = 1000 \\times {prob_compra:.4f} \\approx {esperados}")
        
        # Visualización
        fig_neg = go.Figure()
        
        fig_neg.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=prob_compra * 100,
            title={'text': "Tasa de Conversión (%)"},
            delta={'reference': 3, 'suffix': '%'},
            gauge={
                'axis': {'range': [0, 10]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 2], 'color': "lightcoral"},
                    {'range': [2, 5], 'color': "lightyellow"},
                    {'range': [5, 10], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 5
                }
            }
        ))
        
        fig_neg.update_layout(height=400)
        
        st.plotly_chart(fig_neg, use_container_width=True)
        
    else:  # Derecho
        st.markdown("### Caso Derecho: Análisis de Evidencias")
        
        st.markdown("""
        **Contexto:** Un bufete de abogados analiza 200 casos similares del pasado para estimar probabilidades.
        """)
        
        col_der1, col_der2 = st.columns(2)
        
        with col_der1:
            casos_ganados = st.number_input("Casos ganados:", min_value=0, max_value=200, value=140)
        with col_der2:
            casos_perdidos = 200 - casos_ganados
            st.metric("Casos perdidos", casos_perdidos)
        
        st.markdown("**Análisis:**")
        
        # Pregunta 1
        st.markdown("**1. ¿Cuál es la probabilidad histórica de ganar un caso similar?**")
        
        prob_ganar = casos_ganados / 200
        
        st.latex(f"P(\\text{{Ganar}}) = \\frac{{{casos_ganados}}}{{200}} = {prob_ganar:.4f} = {prob_ganar*100:.2f}\\%")
        
        st.success(f"✅ **Probabilidad de victoria:** {prob_ganar:.4f} ({prob_ganar*100:.2f}%)")
        
        # Pregunta 2
        st.markdown("**2. ¿Cuál es la probabilidad de perder?**")
        
        prob_perder = 1 - prob_ganar
        
        st.latex(f"P(\\text{{Perder}}) = 1 - {prob_ganar:.4f} = {prob_perder:.4f} = {prob_perder*100:.2f}\\%")
        
        st.success(f"✅ **Probabilidad de pérdida:** {prob_perder:.4f} ({prob_perder*100:.2f}%)")
        
        # Visualización
        fig_der = go.Figure(data=[go.Bar(
            x=['Ganados', 'Perdidos'],
            y=[casos_ganados, casos_perdidos],
            marker_color=['#4CAF50', '#F44336'],
            text=[f"{casos_ganados}<br>({prob_ganar*100:.1f}%)", 
                  f"{casos_perdidos}<br>({prob_perder*100:.1f}%)"],
            textposition='outside'
        )])
        
        fig_der.update_layout(
            title="Historial de Casos",
            yaxis_title="Número de Casos",
            height=400
        )
        
        st.plotly_chart(fig_der, use_container_width=True)
    
    st.markdown("---")
    
    # --- CALCULADORA PERSONALIZADA ---
    st.header("🧮 Calculadora de Probabilidad Personalizada")
    
    st.markdown("### Calcula la probabilidad de tu propio problema")
    
    col_calc1, col_calc2 = st.columns(2)
    
    with col_calc1:
        casos_favorables = st.number_input(
            "Número de casos favorables:",
            min_value=0,
            max_value=1000000,
            value=5,
            key="fav_custom"
        )
    
    with col_calc2:
        casos_totales = st.number_input(
            "Número total de casos posibles:",
            min_value=1,
            max_value=1000000,
            value=20,
            key="total_custom"
        )
    
    if casos_favorables <= casos_totales:
        prob_custom = casos_favorables / casos_totales
        
        st.markdown("### 📊 Resultado:")
        
        col_r1, col_r2, col_r3 = st.columns(3)
        
        with col_r1:
            st.metric("Probabilidad (decimal)", f"{prob_custom:.6f}")
        with col_r2:
            st.metric("Probabilidad (%)", f"{prob_custom*100:.4f}%")
        with col_r3:
            if prob_custom > 0:
                odds = f"1 en {int(1/prob_custom)}"
            else:
                odds = "Imposible"
            st.metric("Expresión", odds)
        
        # Fórmula
        st.latex(f"P(A) = \\frac{{{casos_favorables}}}{{{casos_totales}}} = {prob_custom:.6f}")
        
        # Gráfico visual
        fig_custom = go.Figure(data=[go.Pie(
            labels=['Casos Favorables', 'Casos No Favorables'],
            values=[casos_favorables, casos_totales - casos_favorables],
            marker=dict(colors=['#4CAF50', '#E0E0E0']),
            hole=0.5,
            textinfo='label+value'
        )])
        
        fig_custom.update_layout(
            title=f"Proporción de Casos (P = {prob_custom:.4f})",
            height=400
        )
        
        st.plotly_chart(fig_custom, use_container_width=True)
        
        # Interpretaciones
        st.markdown("### 💡 Interpretaciones:")
        
        st.info(f"""
        - **En decimal:** {prob_custom:.6f}
        - **En porcentaje:** {prob_custom*100:.4f}%
        - **En fracción:** {casos_favorables}/{casos_totales}
        - **Interpretación:** De cada {casos_totales} veces que se realiza el experimento, 
          esperamos que el evento ocurra aproximadamente {casos_favorables} veces.
        """)
        
    else:
        st.error("⚠️ Error: Los casos favorables no pueden ser mayores que los casos totales.")

elif page == "5. 📐 Axiomas de Kolmogorov":
    st.title("📐 Los Tres Axiomas de Kolmogorov")
    st.markdown("### Los fundamentos matemáticos de la probabilidad")
    
    st.markdown("---")
    
    # --- INTRODUCCIÓN ---
    st.markdown("""
    ## ¿Qué son los Axiomas de Kolmogorov?
    
    Son las **tres reglas fundamentales** propuestas por el matemático ruso **Andrey Kolmogorov** en 1933 
    que establecen las bases matemáticas de la teoría moderna de probabilidad.
    
    Estos axiomas son como las "reglas del juego" que toda función de probabilidad debe cumplir.
    
    ### 🎯 ¿Por qué son importantes?
    
    - ✅ Dan una **base rigurosa** a la probabilidad
    - ✅ Todas las propiedades de probabilidad **se derivan** de estos axiomas
    - ✅ Permiten trabajar con probabilidades de manera **consistente**
    - ✅ Son **universalmente aceptados** en matemáticas y estadística
    """)
    
    st.markdown("---")
    
    # --- AXIOMAS ---
    tab_ax1, tab_ax2, tab_ax3, tab_propiedades = st.tabs([
        "📏 Axioma 1: No Negatividad",
        "✅ Axioma 2: Certeza",
        "➕ Axioma 3: Aditividad",
        "🎓 Propiedades Derivadas"
    ])
    
    with tab_ax1:
        st.header("Axioma 1: No Negatividad")
        
        st.latex(r"P(A) \geq 0 \quad \text{para todo evento } A")
        
        st.markdown("""
        ### 📖 Significado:
        
        La probabilidad de cualquier evento es **siempre un número no negativo** (mayor o igual a cero).
        
        ### 🤔 ¿Por qué tiene sentido?
        
        No tiene sentido hablar de una probabilidad negativa. ¿Qué significaría decir que algo tiene 
        "-30% de probabilidad"? ¡No tiene interpretación lógica!
        
        ### ✅ Ejemplos Válidos:
        """)
        
        ejemplos_ax1_validos = pd.DataFrame({
            'Evento': [
                'Obtener 6 en un dado',
                'Sacar una carta roja',
                'Que llueva mañana',
                'Evento imposible'
            ],
            'Probabilidad': [
                '1/6 ≈ 0.167',
                '26/52 = 0.5',
                '0.3 (30%)',
                '0'
            ],
            '¿Cumple Axioma 1?': [
                '✅ SÍ (0.167 ≥ 0)',
                '✅ SÍ (0.5 ≥ 0)',
                '✅ SÍ (0.3 ≥ 0)',
                '✅ SÍ (0 ≥ 0)'
            ]
        })
        
        st.table(ejemplos_ax1_validos.set_index('Evento'))
        
        st.markdown("### ❌ Ejemplos Inválidos (violan el axioma):")
        
        ejemplos_ax1_invalidos = pd.DataFrame({
            'Probabilidad': ['-0.5', '-1', '-0.001'],
            'Por qué es inválida': [
                'Negativa',
                'Negativa',
                'Negativa'
            ]
        })
        
        st.table(ejemplos_ax1_invalidos.set_index('Probabilidad'))
        
        st.markdown("---")
        
        # Visualización interactiva
        st.subheader("🎨 Visualización Interactiva")
        
        st.markdown("**Experimento:** Lanzar un dado de 6 caras")
        
        # Mostrar todas las probabilidades
        resultados_dado = list(range(1, 7))
        probs_dado = [1/6] * 6
        
        fig_ax1 = go.Figure(data=[go.Bar(
            x=resultados_dado,
            y=probs_dado,
            marker_color='lightblue',
            text=[f"{p:.3f}" for p in probs_dado],
            textposition='outside'
        )])
        
        # Añadir línea en y=0
        fig_ax1.add_hline(y=0, line_dash="dash", line_color="red", 
                          annotation_text="Límite inferior: P ≥ 0")
        
        fig_ax1.update_layout(
            title="Todas las probabilidades son ≥ 0 ✅",
            xaxis_title="Resultado del Dado",
            yaxis_title="Probabilidad",
            yaxis=dict(range=[-0.1, 0.3]),
            height=400
        )
        
        st.plotly_chart(fig_ax1, use_container_width=True)
        
        st.success("✅ Todas las probabilidades mostradas cumplen el **Axioma 1** (son ≥ 0)")
        
    with tab_ax2:
        st.header("Axioma 2: Certeza (Normalización)")
        
        st.latex(r"P(S) = 1")
        
        st.markdown("""
        ### 📖 Significado:
        
        La probabilidad del **espacio muestral completo** $S$ (es decir, que ocurra ALGÚN resultado posible) es igual a **1** (100%).
        
        ### 🤔 ¿Por qué tiene sentido?
        
        Cuando realizamos un experimento aleatorio, **algo tiene que pasar**. Es seguro que ocurrirá 
        uno de los resultados posibles. Por eso la probabilidad de "cualquier resultado" es 1.
        
        ### 📚 Ejemplos:
        """)
        
        col_ej1, col_ej2 = st.columns(2)
        
        with col_ej1:
            st.markdown("""
            **🎲 Dado:**
            - $S = \\{1, 2, 3, 4, 5, 6\\}$
            - $P(S) = P(\\text{salir 1, 2, 3, 4, 5 o 6})$
            - $P(S) = \\frac{6}{6} = 1$ ✅
            """)
            
        with col_ej2:
            st.markdown("""
            **🪙 Moneda:**
            - $S = \\{\\text{Cara, Sello}\\}$
            - $P(S) = P(\\text{Cara o Sello})$
            - $P(S) = \\frac{2}{2} = 1$ ✅
            """)
        
        st.markdown("---")
        
        # Verificación interactiva
        st.subheader("🧪 Verificación Interactiva")
        
        st.markdown("**Vamos a verificar que las probabilidades suman 1:**")
        
        experimento_ax2 = st.selectbox(
            "Selecciona un experimento:",
            ["🎲 Un dado", "🪙 Una moneda", "🃏 Palo de carta"]
        )
        
        if experimento_ax2 == "🎲 Un dado":
            eventos = [1, 2, 3, 4, 5, 6]
            probs = [1/6] * 6
            descripcion = "cada número del dado"
            
        elif experimento_ax2 == "🪙 Una moneda":
            eventos = ['Cara', 'Sello']
            probs = [0.5, 0.5]
            descripcion = "Cara o Sello"
            
        else:
            eventos = ['♠', '♥', '♦', '♣']
            probs = [0.25] * 4
            descripcion = "cada palo"
        
        # Crear DataFrame
        df_ax2 = pd.DataFrame({
            'Evento': eventos,
            'Probabilidad': probs
        })
        
        col_tab, col_graf = st.columns([1, 2])
        
        with col_tab:
            st.dataframe(df_ax2, hide_index=True)
            suma_total = sum(probs)
            st.metric("Suma Total", f"{suma_total:.6f}")
            
        with col_graf:
            fig_ax2 = go.Figure(data=[go.Bar(
                x=[str(e) for e in eventos],
                y=probs,
                marker_color='lightgreen',
                text=[f"{p:.4f}" for p in probs],
                textposition='outside'
            )])
            
            fig_ax2.update_layout(
                title=f"Probabilidades de {descripcion}",
                xaxis_title="Evento",
                yaxis_title="Probabilidad",
                height=400
            )
            
            st.plotly_chart(fig_ax2, use_container_width=True)
        
        st.latex(f"\\sum P(\\text{{evento}}) = {' + '.join([f'{p:.4f}' for p in probs])} = {suma_total:.6f}")
        
        if abs(suma_total - 1.0) < 0.0001:
            st.success(f"✅ La suma es **{suma_total:.6f} ≈ 1**, cumpliendo el **Axioma 2**")
        else:
            st.error(f"❌ La suma es {suma_total:.6f}, NO cumple el Axioma 2")
        
        st.markdown("---")
        
        # Ejemplos por carrera
        st.subheader("🎓 Aplicación en Diferentes Carreras")
        
        st.markdown("""
        **🏥 Medicina:** Si diagnosticamos a un paciente, debe tener **alguna** condición (aunque sea "sano").
        Todas las posibilidades juntas suman 100%.
        
        **⚙️ Ingeniería:** Una pieza inspeccionada debe ser "aprobada" o "rechazada". 
        No hay tercera opción. $P(\\text{Aprobada}) + P(\\text{Rechazada}) = 1$
        
        **💼 Negocios:** Un cliente debe "comprar" o "no comprar". 
        $P(\\text{Compra}) + P(\\text{No Compra}) = 1$
        
        **⚖️ Derecho:** El veredicto debe ser "culpable" o "no culpable". 
        Ambas probabilidades suman 1.
        """)
        
    with tab_ax3:
        st.header("Axioma 3: Aditividad (Eventos Mutuamente Excluyentes)")
        
        st.latex(r"Si \; A \cap B = \emptyset, \; entonces \; P(A \cup B) = P(A) + P(B)")
        
        st.markdown("""
        ### 📖 Significado:
        
        Si dos eventos **A** y **B** son **mutuamente excluyentes** (no pueden ocurrir al mismo tiempo), 
        entonces la probabilidad de que ocurra **A o B** es la **suma** de sus probabilidades individuales.
        
        ### 🔑 Condición CLAVE:
        
        Este axioma solo aplica cuando $A \\cap B = \\emptyset$ (la intersección es vacía).
        
        Es decir, **A y B NO pueden ocurrir simultáneamente**.
        
        ### 🤔 ¿Por qué tiene sentido?
        
        Si dos eventos no se solapan, la probabilidad de que ocurra uno u otro es simplemente 
        la suma de sus probabilidades. No hay "doble conteo".
        """)
        
        st.markdown("---")
        
        # Ejemplo visual
        st.subheader("🎨 Ejemplo Visual: Lanzar un Dado")
        
        st.markdown("""
        **Eventos:**
        - $A = \\{\\text{Obtener un 2}\\} = \\{2\\}$
        - $B = \\{\\text{Obtener un 5}\\} = \\{5\\}$
        
        **¿Son mutuamente excluyentes?**
        
        Sí, porque no podemos obtener 2 y 5 al mismo tiempo en un solo lanzamiento.
        
        Por lo tanto: $A \\cap B = \\emptyset$ ✅
        """)
        
        # Visualización
        S_ax3 = {1, 2, 3, 4, 5, 6}
        A_ax3 = {2}
        B_ax3 = {5}
        
        colores_ax3 = []
        for x in S_ax3:
            if x in A_ax3:
                colores_ax3.append('lightblue')
            elif x in B_ax3:
                colores_ax3.append('lightcoral')
            else:
                colores_ax3.append('lightgray')
        
        fig_ax3_visual = go.Figure(data=[go.Bar(
            x=list(S_ax3),
            y=[1]*6,
            marker_color=colores_ax3,
            text=list(S_ax3),
            textposition='inside',
            textfont=dict(size=20)
        )])
        
        fig_ax3_visual.update_layout(
            title="A (azul) y B (rojo) son mutuamente excluyentes",
            xaxis_title="Resultado del Dado",
            yaxis_visible=False,
            height=300
        )
        
        st.plotly_chart(fig_ax3_visual, use_container_width=True)
        
        # Cálculos
        col_calc1, col_calc2, col_calc3 = st.columns(3)
        
        with col_calc1:
            st.markdown("**Calcular P(A):**")
            st.latex(r"P(A) = \frac{1}{6} \approx 0.167")
            
        with col_calc2:
            st.markdown("**Calcular P(B):**")
            st.latex(r"P(B) = \frac{1}{6} \approx 0.167")
            
        with col_calc3:
            st.markdown("**Calcular P(A ∪ B):**")
            st.latex(r"P(A \cup B) = \frac{2}{6} = 0.333")
        
        st.markdown("### ✅ Verificación del Axioma 3:")
        
        st.latex(r"P(A \cup B) = P(A) + P(B) = \frac{1}{6} + \frac{1}{6} = \frac{2}{6} = 0.333 \; \checkmark")
        
        st.success("✅ El Axioma 3 se cumple: La suma de probabilidades individuales da la probabilidad de la unión")
        
        st.markdown("---")
        
        # Ejemplo INCORRECTO
        st.subheader("⚠️ Caso Donde NO Aplica el Axioma 3")
        
        st.markdown("""
        **Eventos:**
        - $C = \\{\\text{Número par}\\} = \\{2, 4, 6\\}$
        - $D = \\{\\text{Número mayor que 3}\\} = \\{4, 5, 6\\}$
        
        **¿Son mutuamente excluyentes?**
        
        ❌ NO, porque tienen intersección: $C \\cap D = \\{4, 6\\}$ (no es vacía)
        """)
        
        C_ax3 = {2, 4, 6}
        D_ax3 = {4, 5, 6}
        
        colores_ax3_2 = []
        for x in S_ax3:
            if x in C_ax3 and x in D_ax3:
                colores_ax3_2.append('purple')  # Intersección
            elif x in C_ax3:
                colores_ax3_2.append('lightblue')
            elif x in D_ax3:
                colores_ax3_2.append('lightcoral')
            else:
                colores_ax3_2.append('lightgray')
        
        fig_ax3_no = go.Figure(data=[go.Bar(
            x=list(S_ax3),
            y=[1]*6,
            marker_color=colores_ax3_2,
            text=list(S_ax3),
            textposition='inside',
            textfont=dict(size=20)
        )])
        
        fig_ax3_no.update_layout(
            title="C (azul), D (rojo), Intersección (morado) - NO son mutuamente excluyentes",
            xaxis_title="Resultado del Dado",
            yaxis_visible=False,
            height=300
        )
        
        st.plotly_chart(fig_ax3_no, use_container_width=True)
        
        st.markdown("**Si usamos la fórmula simple del Axioma 3:**")
        
        P_C = len(C_ax3) / 6
        P_D = len(D_ax3) / 6
        suma_incorrecta = P_C + P_D
        
        st.latex(f"P(C) + P(D) = \\frac{{3}}{{6}} + \\frac{{3}}{{6}} = {suma_incorrecta:.3f}")
        
        st.markdown("**Pero la probabilidad real de C ∪ D es:**")
        
        union_CD = C_ax3.union(D_ax3)
        P_union_real = len(union_CD) / 6
        
        st.latex(f"P(C \\cup D) = \\frac{{{len(union_CD)}}}{{6}} = {P_union_real:.3f}")
        
        st.error(f"❌ {suma_incorrecta:.3f} ≠ {P_union_real:.3f} - El Axioma 3 NO aplica aquí porque los eventos NO son mutuamente excluyentes")
        
        st.warning("""
        **Conclusión:** Para eventos que SÍ tienen intersección, debemos usar la fórmula general:
        
        $P(C \\cup D) = P(C) + P(D) - P(C \\cap D)$
        
        (Esta fórmula se deriva de los axiomas y la veremos en la siguiente sección)
        """)
        
        st.markdown("---")
        
        # Ejemplos por carrera
        st.subheader("🎓 Ejemplos por Carrera")
        
        st.markdown("""
        ### 🏥 Medicina:
        
        **Eventos mutuamente excluyentes:**
        - $A = \\{\\text{Tipo de sangre A}\\}$
        - $B = \\{\\text{Tipo de sangre B}\\}$
        
        No se puede tener ambos tipos simultáneamente (sin considerar AB).
        
        $P(\\text{A o B}) = P(A) + P(B)$ ✅
        
        ---
        
        ### ⚙️ Ingeniería:
        
        **Eventos mutuamente excluyentes:**
        - $A = \\{\\text{Pieza con defecto tipo 1}\\}$
        - $B = \\{\\text{Pieza sin defectos}\\}$
        
        Una pieza no puede tener defecto y no tenerlo al mismo tiempo.
        
        $P(\\text{Defecto tipo 1 o sin defectos}) = P(A) + P(B)$ ✅
        
        ---
        
        ### 💼 Negocios:
        
        **Eventos mutuamente excluyentes:**
        - $A = \\{\\text{Cliente compra producto X}\\}$
        - $B = \\{\\text{Cliente compra producto Y}\\}$
        
        (Asumiendo que solo puede comprar uno)
        
        $P(\\text{Compra X o Y}) = P(A) + P(B)$ ✅
        
        ---
        
        ### ⚖️ Derecho:
        
        **Eventos mutuamente excluyentes:**
        - $A = \\{\\text{Veredicto: Culpable}\\}$
        - $B = \\{\\text{Veredicto: No Culpable}\\}$
        
        Solo puede haber un veredicto.
        
        $P(\\text{Culpable o No Culpable}) = P(A) + P(B) = 1$ ✅
        """)
        
    with tab_propiedades:
        st.header("🎓 Propiedades Derivadas de los Axiomas")
        
        st.markdown("""
        A partir de los tres axiomas fundamentales, podemos **derivar** muchas otras propiedades útiles 
        de la probabilidad. Aquí están las más importantes:
        """)
        
        st.markdown("---")
        
        # Propiedad 1
        st.subheader("1️⃣ Probabilidad del Evento Imposible")
        
        st.latex(r"P(\emptyset) = 0")
        
        st.markdown("""
        **Demostración:**
        
        Sabemos que $S \\cap \\emptyset = \\emptyset$ (son mutuamente excluyentes).
        
        Por el Axioma 3: $P(S \\cup \\emptyset) = P(S) + P(\\emptyset)$
        
        Pero $S \\cup \\emptyset = S$, entonces: $P(S) = P(S) + P(\\emptyset)$
        
        Por el Axioma 2: $1 = 1 + P(\\emptyset)$
        
        Por lo tanto: $P(\\emptyset) = 0$ ✅
        """)
        
        st.info("**Interpretación:** Un evento imposible tiene probabilidad 0 (nunca ocurre).")
        
        st.markdown("---")
        
        # Propiedad 2
        st.subheader("2️⃣ Probabilidad del Complemento")
        
        st.latex(r"P(A') = 1 - P(A)")
        
        st.markdown("""
        **Demostración:**
        
        Sabemos que $A$ y $A'$ son mutuamente excluyentes: $A \\cap A' = \\emptyset$
        
        También sabemos que cubren todo el espacio: $A \\cup A' = S$
        
        Por el Axioma 3: $P(A \\cup A') = P(A) + P(A')$
        
        Por el Axioma 2: $P(S) = 1$
        
        Entonces: $1 = P(A) + P(A')$
        
        Por lo tanto: $P(A') = 1 - P(A)$ ✅
        """)
        
        st.success("**Esta es una de las fórmulas más útiles en probabilidad!**")
        
        # Ejemplo interactivo
        st.markdown("#### 🧮 Calculadora de Complementos")
        
        prob_evento = st.slider(
            "Selecciona P(A):",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.01
        )
        
        prob_complemento = 1 - prob_evento
        
        col_comp1, col_comp2 = st.columns(2)
        
        with col_comp1:
            st.metric("P(A)", f"{prob_evento:.2f}")
        with col_comp2:
            st.metric("P(A')", f"{prob_complemento:.2f}")
        
        # Visualización
        fig_comp = go.Figure(data=[go.Pie(
            labels=['P(A)', "P(A')"],
            values=[prob_evento, prob_complemento],
            marker=dict(colors=['#4CAF50', '#FF5722']),
            textinfo='label+percent',
            hole=0.4
        )])
        
        fig_comp.update_layout(
            title=f"P(A) = {prob_evento:.2f} y P(A') = {prob_complemento:.2f}",
            height=400
        )
        
        st.plotly_chart(fig_comp, use_container_width=True)
        
        st.latex(f"P(A') = 1 - P(A) = 1 - {prob_evento:.2f} = {prob_complemento:.2f}")
        
        st.markdown("---")
        
        # Propiedad 3
        st.subheader("3️⃣ Probabilidad Acotada")
        
        st.latex(r"0 \leq P(A) \leq 1 \quad \text{para todo evento } A")
        
        st.markdown("""
        **Demostración:**
        
        Del Axioma 1: $P(A) \\geq 0$
        
        Del complemento: $P(A') = 1 - P(A) \\geq 0$ (también por Axioma 1)
        
        Entonces: $1 - P(A) \\geq 0$, lo que implica $P(A) \\leq 1$
        
        Por lo tanto: $0 \\leq P(A) \\leq 1$ ✅
        """)
        
        st.info("**Interpretación:** Toda probabilidad está entre 0 y 1 (o entre 0% y 100%).")
        
        st.markdown("---")
        
        # Propiedad 4
        st.subheader("4️⃣ Probabilidad de la Unión (Fórmula General)")
        
        st.latex(r"P(A \cup B) = P(A) + P(B) - P(A \cap B)")
        
        st.markdown("""
        **¿Por qué restamos la intersección?**
        
        Porque al sumar $P(A) + P(B)$, estamos contando dos veces los elementos que están en $A \\cap B$.
        Para corregir este "doble conteo", debemos restar $P(A \\cap B)$ una vez.
        
        **Nota:** Si $A \\cap B = \\emptyset$, entonces $P(A \\cap B) = 0$, y recuperamos el Axioma 3.
        """)
        
        # Ejemplo interactivo
        st.markdown("#### 🧮 Calculadora de Unión")
        
        col_u1, col_u2, col_u3 = st.columns(3)
        
        with col_u1:
            P_A_union = st.slider("P(A):", 0.0, 1.0, 0.4, 0.01, key="P_A_union")
        with col_u2:
            P_B_union = st.slider("P(B):", 0.0, 1.0, 0.5, 0.01, key="P_B_union")
        with col_u3:
            max_inter = min(P_A_union, P_B_union)
            P_AB_union = st.slider("P(A ∩ B):", 0.0, max_inter, min(0.2, max_inter), 0.01, key="P_AB_union")
        
        P_union_resultado = P_A_union + P_B_union - P_AB_union
        
        st.markdown("### 📊 Resultado:")
        
        if P_union_resultado <= 1.0:
            st.latex(f"P(A \\cup B) = P(A) + P(B) - P(A \\cap B)")
            st.latex(f"P(A \\cup B) = {P_A_union:.2f} + {P_B_union:.2f} - {P_AB_union:.2f} = {P_union_resultado:.2f}")
            
            st.success(f"✅ **P(A ∪ B) = {P_union_resultado:.2f}**")
            
            # Diagrama visual
            fig_union_prop = go.Figure()
            
            # Crear un diagrama de barras apiladas
            fig_union_prop.add_trace(go.Bar(
                name='Solo A',
                x=['Componentes'],
                y=[P_A_union - P_AB_union],
                marker_color='lightblue'
            ))
            
            fig_union_prop.add_trace(go.Bar(
                name='Intersección A ∩ B',
                x=['Componentes'],
                y=[P_AB_union],
                marker_color='purple'
            ))
            
            fig_union_prop.add_trace(go.Bar(
                name='Solo B',
                x=['Componentes'],
                y=[P_B_union - P_AB_union],
                marker_color='lightcoral'
            ))
            
            fig_union_prop.update_layout(
                barmode='stack',
                title=f'Composición de P(A ∪ B) = {P_union_resultado:.2f}',
                yaxis_title='Probabilidad',
                height=400
            )
            
            st.plotly_chart(fig_union_prop, use_container_width=True)
            
        else:
            st.error("⚠️ Error: Los valores ingresados no son consistentes (P(A ∪ B) > 1)")
        
        st.markdown("---")
        
        # Propiedad 5
        st.subheader("5️⃣ Si A ⊆ B, entonces P(A) ≤ P(B)")
        
        st.latex(r"A \subseteq B \implies P(A) \leq P(B)")
        
        st.markdown("""
        **Interpretación:**
        
        Si el evento $A$ está contenido en el evento $B$, entonces la probabilidad de $A$ 
        no puede ser mayor que la de $B$.
        
        **Ejemplo:**
        - $A = \\{\\text{Obtener un 6}\\} = \\{6\\}$
        - $B = \\{\\text{Obtener número par}\\} = \\{2, 4, 6\\}$
        
        Como $A \\subseteq B$ (todo elemento de A está en B):
        
        $P(A) = \\frac{1}{6} \\leq \\frac{3}{6} = P(B)$ ✅
        """)
        
        st.markdown("---")
        
        # Tabla resumen
        st.subheader("📋 Tabla Resumen de Propiedades")
        
        propiedades_tabla = pd.DataFrame({
            'Propiedad': [
                'Evento Imposible',
                'Complemento',
                'Acotamiento',
                'Unión General',
                'Monotonía',
                'Diferencia'
            ],
            'Fórmula': [
                'P(∅) = 0',
                "P(A') = 1 - P(A)",
                '0 ≤ P(A) ≤ 1',
                'P(A ∪ B) = P(A) + P(B) - P(A ∩ B)',
                'A ⊆ B ⟹ P(A) ≤ P(B)',
                'P(A - B) = P(A) - P(A ∩ B)'
            ],
            'Derivada de': [
                'Axiomas 2 y 3',
                'Axiomas 2 y 3',
                'Axiomas 1 y complemento',
                'Axioma 3 generalizado',
                'Axioma 1 y aditividad',
                'Propiedades de conjuntos'
            ]
        })
        
        st.table(propiedades_tabla.set_index('Propiedad'))
        
        st.success("""
        ### 🎯 Conclusión:
        
        Los **3 Axiomas de Kolmogorov** son simples, pero de ellos se derivan **TODAS** 
        las propiedades y fórmulas que usamos en probabilidad. Son la base matemática 
        rigurosa de esta disciplina.
        """)

elif page == "6. 🎮 Simulador de Experimentos":
    st.title("🎮 Simulador de Experimentos Aleatorios")
    st.markdown("### Observa cómo la frecuencia relativa converge a la probabilidad teórica")
    
    st.markdown("---")
    
    # Introducción
    st.markdown("""
    ## 🎯 La Ley de los Grandes Números
    
    Esta ley estadística establece que cuando **repetimos un experimento muchas veces**, 
    la **frecuencia relativa** (proporción observada) se aproxima a la **probabilidad teórica**.
    
    ### Fórmula:
    """)
    
    st.latex(r"\text{Frecuencia Relativa} = \frac{\text{Número de veces que ocurrió el evento}}{\text{Total de experimentos}}")
    
    st.info("""
    **En términos simples:**
    - Con **pocos** experimentos → Los resultados pueden variar mucho (azar)
    - Con **muchos** experimentos → Los resultados se estabilizan cerca de la probabilidad real
    """)
    
    st.markdown("---")
    
    # Selección de experimento
    tipo_experimento = st.selectbox(
        "Selecciona el tipo de experimento:",
        ["🪙 Lanzar Moneda(s)", "🎲 Lanzar Dado(s)", "🎯 Rueda de la Fortuna"]
    )
    
    if tipo_experimento == "🪙 Lanzar Moneda(s)":
        st.subheader("🪙 Simulador de Lanzamiento de Monedas")
        
        col_config1, col_config2 = st.columns(2)
        
        with col_config1:
            num_monedas = st.radio("Número de monedas:", [1, 2], horizontal=True)
        
        with col_config2:
            num_lanzamientos = st.select_slider(
                "Número de lanzamientos:",
                options=[10, 50, 100, 500, 1000, 5000, 10000],
                value=100
            )
        
        if num_monedas == 1:
            st.markdown("**Probabilidades Teóricas:**")
            st.markdown("- P(Cara) = 0.5 (50%)")
            st.markdown("- P(Sello) = 0.5 (50%)")
            
            evento_moneda = st.radio(
                "Evento a rastrear:",
                ["Cara", "Sello"],
                horizontal=True
            )
            
            prob_teorica = 0.5
            
        else:  # 2 monedas
            st.markdown("**Probabilidades Teóricas:**")
            st.markdown("- P(2 Caras) = 0.25 (25%)")
            st.markdown("- P(1 Cara, 1 Sello) = 0.50 (50%)")
            st.markdown("- P(2 Sellos) = 0.25 (25%)")
            
            evento_moneda = st.selectbox(
                "Evento a rastrear:",
                ["2 Caras", "1 Cara y 1 Sello", "2 Sellos"]
            )
            
            if evento_moneda == "2 Caras":
                prob_teorica = 0.25
            elif evento_moneda == "1 Cara y 1 Sello":
                prob_teorica = 0.50
            else:
                prob_teorica = 0.25
        
        if st.button("🎲 Realizar Simulación", key="sim_moneda"):
            with st.spinner("Simulando lanzamientos..."):
                # Realizar simulación
                resultados = simular_lanzamientos("Moneda", num_monedas, num_lanzamientos)
                
                # Calcular frecuencias acumuladas
                frecuencias_acumuladas = []
                count = 0
                
                for i, resultado in enumerate(resultados, 1):
                    if num_monedas == 1:
                        if resultado == evento_moneda:
                            count += 1
                    else:
                        if evento_moneda == "2 Caras" and resultado == ('C', 'C'):
                            count += 1
                        elif evento_moneda == "2 Sellos" and resultado == ('S', 'S'):
                            count += 1
                        elif evento_moneda == "1 Cara y 1 Sello" and resultado in [('C', 'S'), ('S', 'C')]:
                            count += 1
                    
                    frecuencias_acumuladas.append(count / i)
                
                # Crear gráfico de convergencia
                fig_convergencia = go.Figure()
                
                fig_convergencia.add_trace(go.Scatter(
                    x=list(range(1, num_lanzamientos + 1)),
                    y=frecuencias_acumuladas,
                    mode='lines',
                    name='Frecuencia Relativa Observada',
                    line=dict(color='blue', width=2)
                ))
                
                fig_convergencia.add_hline(
                    y=prob_teorica,
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"Probabilidad Teórica = {prob_teorica}",
                    annotation_position="right"
                )
                
                fig_convergencia.update_layout(
                    title=f"Convergencia a la Probabilidad Teórica - {evento_moneda}",
                    xaxis_title="Número de Lanzamientos",
                    yaxis_title="Frecuencia Relativa",
                    yaxis=dict(range=[0, 1]),
                    height=500,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_convergencia, use_container_width=True)
                
                # Resultados finales
                frecuencia_final = frecuencias_acumuladas[-1]
                diferencia = abs(frecuencia_final - prob_teorica)
                
                col_res1, col_res2, col_res3 = st.columns(3)
                
                with col_res1:
                    st.metric("Probabilidad Teórica", f"{prob_teorica:.4f}")
                with col_res2:
                    st.metric("Frecuencia Observada", f"{frecuencia_final:.4f}")
                with col_res3:
                    st.metric("Diferencia", f"{diferencia:.4f}")
                
                if diferencia < 0.05:
                    st.success(f"✅ ¡Excelente! La frecuencia observada está muy cerca de la probabilidad teórica (diferencia < 5%)")
                elif diferencia < 0.10:
                    st.info(f"✓ Buena aproximación. La frecuencia observada está razonablemente cerca (diferencia < 10%)")
                else:
                    st.warning(f"⚠️ La diferencia es notable. Intenta con más lanzamientos para mejor convergencia.")
                
                # Distribución de resultados
                st.markdown("### 📊 Distribución de Resultados")
                
                if num_monedas == 1:
                    conteo = pd.Series(resultados).value_counts()
                else:
                    # Convertir tuplas a strings para contar
                    resultados_str = [str(r) for r in resultados]
                    conteo = pd.Series(resultados_str).value_counts()
                
                fig_dist = go.Figure(data=[go.Bar(
                    x=conteo.index,
                    y=conteo.values,
                    marker_color='lightblue',
                    text=conteo.values,
                    textposition='outside'
                )])
                
                fig_dist.update_layout(
                    title="Frecuencia Absoluta de Resultados",
                    xaxis_title="Resultado",
                    yaxis_title="Frecuencia",
                    height=400
                )
                
                st.plotly_chart(fig_dist, use_container_width=True)
    
    elif tipo_experimento == "🎲 Lanzar Dado(s)":
        st.subheader("🎲 Simulador de Lanzamiento de Dados")
        
        col_config1, col_config2 = st.columns(2)
        
        with col_config1:
            num_dados = st.radio("Número de dados:", [1, 2], horizontal=True)
        
        with col_config2:
            num_lanzamientos = st.select_slider(
                "Número de lanzamientos:",
                options=[10, 50, 100, 500, 1000, 5000, 10000],
                value=100
            )
        
        if num_dados == 1:
            st.markdown("**Probabilidades Teóricas:**")
            st.markdown("- P(cualquier número) = 1/6 ≈ 0.1667 (16.67%)")
            
            evento_dado = st.selectbox(
                "Evento a rastrear:",
                ["Obtener un 1", "Obtener un 2", "Obtener un 3", 
                 "Obtener un 4", "Obtener un 5", "Obtener un 6",
                 "Número par (2,4,6)", "Número impar (1,3,5)"]
            )
            
            if "par" in evento_dado:
                prob_teorica = 0.5
                valores_evento = {2, 4, 6}
            elif "impar" in evento_dado:
                prob_teorica = 0.5
                valores_evento = {1, 3, 5}
            else:
                prob_teorica = 1/6
                valores_evento = {int(evento_dado.split()[-1])}
            
        else:  # 2 dados
            st.markdown("**Probabilidad teórica depende de la suma:**")
            st.markdown("- P(suma = 7) = 6/36 ≈ 0.1667 (la más probable)")
            st.markdown("- P(suma = 2 o 12) = 1/36 ≈ 0.0278 (las menos probables)")
            
            suma_objetivo = st.slider("Suma objetivo:", 2, 12, 7)
            
            # Calcular probabilidad teórica
            probabilidades_sumas = {
                2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36, 6: 5/36, 7: 6/36,
                8: 5/36, 9: 4/36, 10: 3/36, 11: 2/36, 12: 1/36
            }
            
            prob_teorica = probabilidades_sumas[suma_objetivo]
        
        if st.button("🎲 Realizar Simulación", key="sim_dado"):
            with st.spinner("Simulando lanzamientos..."):
                # Realizar simulación
                resultados = simular_lanzamientos("Dado", num_dados, num_lanzamientos)
                
                # Calcular frecuencias acumuladas
                frecuencias_acumuladas = []
                count = 0
                
                for i, resultado in enumerate(resultados, 1):
                    if num_dados == 1:
                        if resultado in valores_evento:
                            count += 1
                    else:
                        if sum(resultado) == suma_objetivo:
                            count += 1
                    
                    frecuencias_acumuladas.append(count / i)
                
                # Crear gráfico de convergencia
                fig_convergencia_dado = go.Figure()
                
                fig_convergencia_dado.add_trace(go.Scatter(
                    x=list(range(1, num_lanzamientos + 1)),
                    y=frecuencias_acumuladas,
                    mode='lines',
                    name='Frecuencia Relativa Observada',
                    line=dict(color='green', width=2)
                ))
                
                fig_convergencia_dado.add_hline(
                    y=prob_teorica,
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"Probabilidad Teórica = {prob_teorica:.4f}",
                    annotation_position="right"
                )
                
                titulo = f"Suma = {suma_objetivo}" if num_dados == 2 else evento_dado
                
                fig_convergencia_dado.update_layout(
                    title=f"Convergencia a la Probabilidad Teórica - {titulo}",
                    xaxis_title="Número de Lanzamientos",
                    yaxis_title="Frecuencia Relativa",
                    yaxis=dict(range=[0, max(1, max(frecuencias_acumuladas) + 0.1)]),
                    height=500,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_convergencia_dado, use_container_width=True)
                
                # Resultados finales
                frecuencia_final = frecuencias_acumuladas[-1]
                diferencia = abs(frecuencia_final - prob_teorica)
                
                col_res1, col_res2, col_res3 = st.columns(3)
                
                with col_res1:
                    st.metric("Probabilidad Teórica", f"{prob_teorica:.4f}")
                with col_res2:
                    st.metric("Frecuencia Observada", f"{frecuencia_final:.4f}")
                with col_res3:
                    st.metric("Diferencia", f"{diferencia:.4f}")
                
                if diferencia < 0.05:
                    st.success(f"✅ ¡Excelente! La frecuencia observada está muy cerca de la probabilidad teórica")
                elif diferencia < 0.10:
                    st.info(f"✓ Buena aproximación. La diferencia es aceptable")
                else:
                    st.warning(f"⚠️ Considera aumentar el número de lanzamientos para mejor convergencia")
                
                # Distribución de resultados
                st.markdown("### 📊 Distribución de Todos los Resultados")
                
                if num_dados == 1:
                    conteo = pd.Series(resultados).value_counts().sort_index()
                else:
                    # Para 2 dados, mostrar distribución de sumas
                    sumas = [sum(r) for r in resultados]
                    conteo = pd.Series(sumas).value_counts().sort_index()
                
                fig_dist_dado = go.Figure()
                
                # Barras observadas
                fig_dist_dado.add_trace(go.Bar(
                    x=conteo.index,
                    y=conteo.values / num_lanzamientos,
                    name='Frecuencia Relativa Observada',
                    marker_color='lightblue',
                    text=[f"{v/num_lanzamientos:.3f}" for v in conteo.values],
                    textposition='outside'
                ))
                
                # Línea teórica
                if num_dados == 1:
                    x_teorico = list(range(1, 7))
                    if "par" in evento_dado or "impar" in evento_dado:
                        y_teorico = [1/6] * 6
                    else:
                        y_teorico = [1/6] * 6
                else:
                    x_teorico = list(range(2, 13))
                    y_teorico = [probabilidades_sumas[i] for i in x_teorico]
                
                fig_dist_dado.add_trace(go.Scatter(
                    x=x_teorico,
                    y=y_teorico,
                    name='Probabilidad Teórica',
                    mode='lines+markers',
                    line=dict(color='red', width=2, dash='dash'),
                    marker=dict(size=8)
                ))
                
                titulo_dist = "Resultado del Dado" if num_dados == 1 else "Suma de los Dados"
                
                fig_dist_dado.update_layout(
                    title=f"Distribución: {titulo_dist}",
                    xaxis_title=titulo_dist,
                    yaxis_title="Frecuencia Relativa",
                    height=400,
                    showlegend=True
                )
                
                st.plotly_chart(fig_dist_dado, use_container_width=True)
    
    else:  # Rueda de la Fortuna
        st.subheader("🎯 Rueda de la Fortuna Personalizada")
        
        st.markdown("Define tu propia rueda con diferentes probabilidades")
        
        # Configuración de la rueda
        num_sectores = st.slider("Número de sectores:", 2, 8, 4)
        
        st.markdown("### Configura cada sector:")
        
        sectores = []
        probabilidades = []
        colores_sectores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2']
        
        cols = st.columns(min(num_sectores, 4))
        
        for i in range(num_sectores):
            with cols[i % 4]:
                nombre = st.text_input(f"Sector {i+1}:", value=f"Opción {i+1}", key=f"sector_{i}")
                prob = st.number_input(f"Proporción:", min_value=1, max_value=100, value=10, key=f"prob_{i}")
                sectores.append(nombre)
                probabilidades.append(prob)
        
        # Normalizar probabilidades
        suma_probs = sum(probabilidades)
        probabilidades_norm = [p / suma_probs for p in probabilidades]
        
        st.markdown("### 📊 Probabilidades Normalizadas:")
        
        df_rueda = pd.DataFrame({
            'Sector': sectores,
            'Proporción': probabilidades,
            'Probabilidad': probabilidades_norm,
            'Porcentaje': [f"{p*100:.2f}%" for p in probabilidades_norm]
        })
        
        st.dataframe(df_rueda, hide_index=True)
        
        # Visualizar la rueda
        fig_rueda = go.Figure(data=[go.Pie(
            labels=sectores,
            values=probabilidades,
            marker=dict(colors=colores_sectores[:num_sectores]),
            textinfo='label+percent',
            hovertemplate='%{label}<br>Probabilidad: %{percent}<extra></extra>'
        )])
        
        fig_rueda.update_layout(
            title="Tu Rueda de la Fortuna",
            height=400
        )
        
        st.plotly_chart(fig_rueda, use_container_width=True)
        
        # Simulación
        num_giros = st.select_slider(
            "Número de giros:",
            options=[10, 50, 100, 500, 1000, 5000, 10000],
            value=100
        )
        
        sector_rastrear = st.selectbox("Sector a rastrear:", sectores)
        prob_teorica_rueda = probabilidades_norm[sectores.index(sector_rastrear)]
        
        if st.button("🎯 Girar la Rueda", key="sim_rueda"):
            with st.spinner("Girando la rueda..."):
                # Realizar simulación
                resultados_rueda = np.random.choice(sectores, size=num_giros, p=probabilidades_norm)
                
                # Calcular frecuencias acumuladas
                frecuencias_acumuladas_rueda = []
                count = 0
                
                for i, resultado in enumerate(resultados_rueda, 1):
                    if resultado == sector_rastrear:
                        count += 1
                    frecuencias_acumuladas_rueda.append(count / i)
                
                # Gráfico de convergencia
                fig_conv_rueda = go.Figure()
                
                fig_conv_rueda.add_trace(go.Scatter(
                    x=list(range(1, num_giros + 1)),
                    y=frecuencias_acumuladas_rueda,
                    mode='lines',
                    name='Frecuencia Relativa Observada',
                    line=dict(color='purple', width=2)
                ))
                
                fig_conv_rueda.add_hline(
                    y=prob_teorica_rueda,
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"Probabilidad Teórica = {prob_teorica_rueda:.4f}",
                    annotation_position="right"
                )
                
                fig_conv_rueda.update_layout(
                    title=f"Convergencia - Sector: {sector_rastrear}",
                    xaxis_title="Número de Giros",
                    yaxis_title="Frecuencia Relativa",
                    yaxis=dict(range=[0, 1]),
                    height=500
                )
                
                st.plotly_chart(fig_conv_rueda, use_container_width=True)
                
                # Resultados
                frecuencia_final = frecuencias_acumuladas_rueda[-1]
                diferencia = abs(frecuencia_final - prob_teorica_rueda)
                
                col_r1, col_r2, col_r3 = st.columns(3)
                
                with col_r1:
                    st.metric("Probabilidad Teórica", f"{prob_teorica_rueda:.4f}")
                with col_r2:
                    st.metric("Frecuencia Observada", f"{frecuencia_final:.4f}")
                with col_r3:
                    st.metric("Diferencia", f"{diferencia:.4f}")
                
                # Distribución de todos los sectores
                st.markdown("### 📊 Distribución de Todos los Sectores")
                
                conteo_rueda = pd.Series(resultados_rueda).value_counts()
                
                fig_dist_rueda = go.Figure()
                
                # Frecuencias observadas
                fig_dist_rueda.add_trace(go.Bar(
                    x=conteo_rueda.index,
                    y=conteo_rueda.values / num_giros,
                    name='Frecuencia Observada',
                    marker_color='lightgreen',
                    text=[f"{v/num_giros:.3f}" for v in conteo_rueda.values],
                    textposition='outside'
                ))
                
                # Probabilidades teóricas
                fig_dist_rueda.add_trace(go.Scatter(
                    x=sectores,
                    y=probabilidades_norm,
                    name='Probabilidad Teórica',
                    mode='lines+markers',
                    line=dict(color='red', width=2, dash='dash'),
                    marker=dict(size=10)
                ))
                
                fig_dist_rueda.update_layout(
                    title="Comparación: Observado vs Teórico",
                    xaxis_title="Sector",
                    yaxis_title="Frecuencia Relativa / Probabilidad",
                    height=400,
                    showlegend=True
                )
                
                st.plotly_chart(fig_dist_rueda, use_container_width=True)
    
    st.markdown("---")
    
    # Explicación final
    st.info("""
    ### 💡 Conclusión sobre la Ley de los Grandes Números:
    
    - **Con pocos experimentos** (10-100): La frecuencia observada puede diferir bastante de la probabilidad teórica
    - **Con experimentos moderados** (100-1000): La convergencia es notable
    - **Con muchos experimentos** (1000+): La frecuencia observada se acerca mucho a la probabilidad teórica
    
    **Esto demuestra que la probabilidad teórica predice el comportamiento a largo plazo de experimentos aleatorios.**
    """)

elif page == "7. 🏥 Casos por Carrera":
    st.title("🏥 Casos Prácticos por Carrera")
    st.markdown("### Aplicaciones reales de probabilidad en diferentes disciplinas")
    
    st.markdown("---")
    
    carrera_select = st.selectbox(
        "Selecciona tu área de interés:",
        ["🏥 Medicina y Salud", "⚙️ Ingeniería", "💼 Negocios y Marketing", "⚖️ Derecho y Ciencias Sociales"]
    )
    
    if carrera_select == "🏥 Medicina y Salud":
        st.header("🏥 Medicina y Salud")
        
        caso_med = st.radio(
            "Selecciona un caso:",
            [
                "Caso 1: Efectividad de una Vacuna",
                "Caso 2: Diagnóstico de Enfermedad",
                "Caso 3: Tipo de Sangre en Donantes"
            ]
        )
        
        if caso_med == "Caso 1: Efectividad de una Vacuna":
            st.subheader("💉 Caso 1: Efectividad de una Vacuna")
            
            st.markdown("""
            **Contexto:**
            
            Un laboratorio desarrolló una nueva vacuna contra una enfermedad. 
            En ensayos clínicos con 1,000 personas vacunadas:
            - 950 personas NO contrajeron la enfermedad al ser expuestas
            - 50 personas SÍ contrajeron la enfermedad a pesar de estar vacunadas
            """)
            
            # Datos
            total_vacunados = 1000
            protegidos = 950
            contagiados = 50
            
            # Visualización
            fig_vacuna = go.Figure(data=[go.Pie(
                labels=['Protegidos', 'Contagiados'],
                values=[protegidos, contagiados],
                marker=dict(colors=['#4CAF50', '#F44336']),
                hole=0.4,
                textinfo='label+value+percent'
            )])
            
            fig_vacuna.update_layout(
                title="Resultados del Ensayo Clínico",
                height=400
            )
            
            st.plotly_chart(fig_vacuna, use_container_width=True)
            
            # Preguntas
            st.markdown("### 📋 Preguntas:")
            
            with st.expander("**Pregunta 1:** ¿Cuál es la efectividad de la vacuna (probabilidad de protección)?"):
                st.markdown("**Solución:**")
                
                prob_proteccion = protegidos / total_vacunados
                
                st.latex(r"P(\text{Protección}) = \frac{\text{Protegidos}}{\text{Total vacunados}} = \frac{950}{1000} = 0.95")
                
                st.success(f"✅ **Respuesta:** La efectividad de la vacuna es del **95%** o **0.95**")
                
                st.info("""
                **Interpretación:** De cada 100 personas vacunadas, esperamos que aproximadamente 95 estén protegidas contra la enfermedad.
                """)
            
            with st.expander("**Pregunta 2:** Si se vacunan 5,000 personas más, ¿cuántas se espera que estén protegidas?"):
                st.markdown("**Solución:**")
                
                nuevos_vacunados = 5000
                esperados_protegidos = int(nuevos_vacunados * prob_proteccion)
                
                st.latex(f"\\text{{Protegidos esperados}} = 5000 \\times 0.95 = {esperados_protegidos}")
                
                st.success(f"✅ **Respuesta:** Se espera que aproximadamente **{esperados_protegidos} personas** estén protegidas")
            
            with st.expander("**Pregunta 3:** ¿Cuál es la probabilidad de que la vacuna NO funcione?"):
                st.markdown("**Solución (usando complemento):**")
                
                prob_fallo = 1 - prob_proteccion
                
                st.latex(r"P(\text{Fallo}) = 1 - P(\text{Protección}) = 1 - 0.95 = 0.05")
                
                st.success(f"✅ **Respuesta:** La probabilidad de fallo es del **5%** o **0.05**")
        
        elif caso_med == "Caso 2: Diagnóstico de Enfermedad":
            st.subheader("🔬 Caso 2: Diagnóstico de Enfermedad")
            
            st.markdown("""
            **Contexto:**
            
            En una clínica se realizan pruebas de detección de una enfermedad rara.
            Los registros históricos muestran:
            - La enfermedad afecta al 2% de la población
            - El 98% de la población está sana
            """)
            
            # Configuración interactiva
            poblacion = st.number_input("Tamaño de la población estudiada:", min_value=100, max_value=100000, value=10000, step=100)
            
            prevalencia = 0.02
            enfermos = int(poblacion * prevalencia)
            sanos = poblacion - enfermos
            
            col_m1, col_m2 = st.columns(2)
            
            with col_m1:
                st.metric("Personas enfermas", enfermos)
            with col_m2:
                st.metric("Personas sanas", sanos)
            
            # Visualización
            fig_enfermedad = go.Figure(data=[go.Bar(
                x=['Enfermos', 'Sanos'],
                y=[enfermos, sanos],
                marker_color=['#E74C3C', '#2ECC71'],
                text=[f"{enfermos}<br>({prevalencia*100:.1f}%)", f"{sanos}<br>({(1-prevalencia)*100:.1f}%)"],
                textposition='outside'
            )])
            
            fig_enfermedad.update_layout(
                title=f"Distribución de la Enfermedad (N={poblacion})",
                yaxis_title="Número de Personas",
                height=400
            )
            
            st.plotly_chart(fig_enfermedad, use_container_width=True)
            
            # Preguntas
            st.markdown("### 📋 Preguntas:")
            
            with st.expander("**Pregunta 1:** Si seleccionamos una persona al azar, ¿cuál es la probabilidad de que esté enferma?"):
                st.latex(r"P(\text{Enfermo}) = 0.02 = 2\%")
                st.success("✅ **Respuesta:** 0.02 o 2%")
            
            with st.expander("**Pregunta 2:** ¿Cuál es la probabilidad de que esté sana?"):
                st.latex(r"P(\text{Sano}) = 1 - P(\text{Enfermo}) = 1 - 0.02 = 0.98 = 98\%")
                st.success("✅ **Respuesta:** 0.98 o 98%")
            
            with st.expander("**Pregunta 3:** De 500 personas seleccionadas al azar, ¿cuántas esperamos que estén enfermas?"):
                esperadas_enfermas = int(500 * prevalencia)
                st.latex(f"\\text{{Esperadas}} = 500 \\times 0.02 = {esperadas_enfermas}")
                st.success(f"✅ **Respuesta:** Aproximadamente **{esperadas_enfermas} personas**")
        
        else:  # Caso 3
            st.subheader("🩸 Caso 3: Tipo de Sangre en Donantes")
            
            st.markdown("""
            **Contexto:**
            
            Un banco de sangre registra los tipos de sangre de sus donantes.
            La distribución es la siguiente:
            """)
            
            # Datos de tipos de sangre (basados en estadísticas reales)
            tipos_sangre = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
            porcentajes = [38, 7, 34, 6, 9, 2, 3, 1]  # Porcentajes aproximados
            
            total_donantes = st.number_input("Total de donantes registrados:", min_value=100, max_value=10000, value=1000, step=100)
            
            # Calcular cantidades
            cantidades = [int(total_donantes * p / 100) for p in porcentajes]
            
            # Crear DataFrame
            df_sangre = pd.DataFrame({
                'Tipo de Sangre': tipos_sangre,
                'Porcentaje': [f"{p}%" for p in porcentajes],
                'Probabilidad': [p/100 for p in porcentajes],
                'Cantidad': cantidades
            })
            
            st.dataframe(df_sangre, hide_index=True, use_container_width=True)
            
            # Visualización
            fig_sangre = go.Figure(data=[go.Bar(
                x=tipos_sangre,
                y=cantidades,
                marker_color=['#E74C3C', '#C0392B', '#3498DB', '#2980B9', '#F39C12', '#D68910', '#9B59B6', '#8E44AD'],
                text=cantidades,
                textposition='outside'
            )])
            
            fig_sangre.update_layout(
                title=f"Distribución de Tipos de Sangre (N={total_donantes})",
                xaxis_title="Tipo de Sangre",
                yaxis_title="Número de Donantes",
                height=400
            )
            
            st.plotly_chart(fig_sangre, use_container_width=True)
            
            # Preguntas
            st.markdown("### 📋 Preguntas:")
            
            with st.expander("**Pregunta 1:** ¿Cuál es la probabilidad de que un donante aleatorio tenga sangre tipo O+ (donante universal)?"):
                prob_O_pos = 0.38
                st.latex(r"P(\text{O+}) = \frac{38}{100} = 0.38 = 38\%")
                st.success("✅ **Respuesta:** 0.38 o 38%")
            
            with st.expander("**Pregunta 2:** ¿Cuál es la probabilidad de tener tipo O (positivo o negativo)?"):
                st.markdown("**Solución:** Usamos el Axioma 3 (eventos mutuamente excluyentes)")
                
                prob_O = 0.38 + 0.07
                
                st.latex(r"P(\text{O+ o O-}) = P(\text{O+}) + P(\text{O-}) = 0.38 + 0.07 = 0.45")
                
                st.success("✅ **Respuesta:** 0.45 o 45%")
                
                st.info("Los eventos son mutuamente excluyentes porque una persona no puede tener dos tipos de sangre simultáneamente.")
            
            with st.expander("**Pregunta 3:** ¿Cuál es la probabilidad de que un donante NO tenga sangre tipo AB-?"):
                st.markdown("**Solución:** Usamos el complemento")
                
                prob_AB_neg = 0.01
                prob_no_AB_neg = 1 - prob_AB_neg
                
                st.latex(r"P(\text{NO AB-}) = 1 - P(\text{AB-}) = 1 - 0.01 = 0.99")
                
                st.success("✅ **Respuesta:** 0.99 o 99%")
            
            with st.expander("**Pregunta 4:** Si llegan 500 nuevos donantes, ¿cuántos se espera que tengan sangre tipo A+ o A-?"):
                st.markdown("**Solución:**")
                
                prob_A_total = 0.34 + 0.06
                esperados_A = int(500 * prob_A_total)
                
                st.latex(r"P(\text{A+ o A-}) = 0.34 + 0.06 = 0.40")
                st.latex(f"\\text{{Esperados}} = 500 \\times 0.40 = {esperados_A}")
                
                st.success(f"✅ **Respuesta:** Aproximadamente **{esperados_A} donantes**")
    
    elif carrera_select == "⚙️ Ingeniería":
        st.header("⚙️ Ingeniería")
        
        caso_ing = st.radio(
            "Selecciona un caso:",
            [
                "Caso 1: Control de Calidad en Producción",
                "Caso 2: Confiabilidad de Sistemas",
                "Caso 3: Pruebas de Componentes Electrónicos"
            ]
        )
        
        if caso_ing == "Caso 1: Control de Calidad en Producción":
            st.subheader("🔧 Caso 1: Control de Calidad en Producción")
            
            st.markdown("""
            **Contexto:**
            
            Una fábrica de componentes mecánicos produce piezas en tres máquinas diferentes.
            Los datos de producción del último mes son:
            """)
            
            col_maq1, col_maq2, col_maq3 = st.columns(3)
            
            with col_maq1:
                prod_M1 = st.number_input("Producción Máquina 1:", min_value=0, value=5000, step=100, key="M1")
                defect_M1 = st.number_input("Defectuosas Máquina 1:", min_value=0, value=100, step=10, key="D1")
            
            with col_maq2:
                prod_M2 = st.number_input("Producción Máquina 2:", min_value=0, value=3000, step=100, key="M2")
                defect_M2 = st.number_input("Defectuosas Máquina 2:", min_value=0, value=90, step=10, key="D2")
            
            with col_maq3:
                prod_M3 = st.number_input("Producción Máquina 3:", min_value=0, value=2000, step=100, key="M3")
                defect_M3 = st.number_input("Defectuosas Máquina 3:", min_value=0, value=40, step=10, key="D3")
            
            total_produccion = prod_M1 + prod_M2 + prod_M3
            total_defectuosas = defect_M1 + defect_M2 + defect_M3
            
            # DataFrame resumen
            df_produccion = pd.DataFrame({
                'Máquina': ['M1', 'M2', 'M3', 'TOTAL'],
                'Producción': [prod_M1, prod_M2, prod_M3, total_produccion],
                'Defectuosas': [defect_M1, defect_M2, defect_M3, total_defectuosas],
                'Tasa Defectos': [
                    f"{defect_M1/prod_M1*100:.2f}%" if prod_M1 > 0 else "0%",
                    f"{defect_M2/prod_M2*100:.2f}%" if prod_M2 > 0 else "0%",
                    f"{defect_M3/prod_M3*100:.2f}%" if prod_M3 > 0 else "0%",
                    f"{total_defectuosas/total_produccion*100:.2f}%" if total_produccion > 0 else "0%"
                ]
            })
            
            st.dataframe(df_produccion, hide_index=True, use_container_width=True)
            
            # Visualización
            fig_produccion = go.Figure()
            
            fig_produccion.add_trace(go.Bar(
                name='Producción Total',
                x=['M1', 'M2', 'M3'],
                y=[prod_M1, prod_M2, prod_M3],
                marker_color='lightblue'
            ))
            
            fig_produccion.add_trace(go.Bar(
                name='Defectuosas',
                x=['M1', 'M2', 'M3'],
                y=[defect_M1, defect_M2, defect_M3],
                marker_color='red'
            ))
            
            fig_produccion.update_layout(
                title="Producción por Máquina",
                xaxis_title="Máquina",
                yaxis_title="Número de Piezas",
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig_produccion, use_container_width=True)
            
            # Preguntas
            st.markdown("### 📋 Preguntas:")
            
            with st.expander("**Pregunta 1:** Si se selecciona una pieza al azar de toda la producción, ¿cuál es la probabilidad de que sea defectuosa?"):
                if total_produccion > 0:
                    prob_defectuosa = total_defectuosas / total_produccion
                    
                    st.latex(f"P(\\text{{Defectuosa}}) = \\frac{{{total_defectuosas}}}{{{total_produccion}}} = {prob_defectuosa:.4f}")
                    
                    st.success(f"✅ **Respuesta:** {prob_defectuosa:.4f} o {prob_defectuosa*100:.2f}%")
                    
                    if prob_defectuosa <= 0.05:
                        st.info("✅ La tasa de defectos está dentro del estándar aceptable (≤5%)")
                    else:
                        st.warning("⚠️ La tasa de defectos supera el estándar aceptable. Se requiere acción correctiva.")
            
            with st.expander("**Pregunta 2:** ¿Cuál máquina tiene la mayor tasa de defectos?"):
                if prod_M1 > 0 and prod_M2 > 0 and prod_M3 > 0:
                    tasa_M1 = defect_M1 / prod_M1
                    tasa_M2 = defect_M2 / prod_M2
                    tasa_M3 = defect_M3 / prod_M3
                    
                    tasas = [('M1', tasa_M1), ('M2', tasa_M2), ('M3', tasa_M3)]
                    tasas_sorted = sorted(tasas, key=lambda x: x[1], reverse=True)
                    
                    st.markdown("**Tasas de defectos por máquina:**")
                    for maq, tasa in tasas_sorted:
                        st.markdown(f"- {maq}: {tasa:.4f} ({tasa*100:.2f}%)")
                    
                    st.success(f"✅ **Respuesta:** {tasas_sorted[0][0]} tiene la mayor tasa con {tasas_sorted[0][1]*100:.2f}%")
            
            with st.expander("**Pregunta 3:** Si se producen 10,000 piezas más con la misma tasa de defectos, ¿cuántas se espera que sean defectuosas?"):
                if total_produccion > 0:
                    prob_defectuosa = total_defectuosas / total_produccion
                    esperadas_defectuosas = int(10000 * prob_defectuosa)
                    
                    st.latex(f"\\text{{Defectuosas esperadas}} = 10000 \\times {prob_defectuosa:.4f} = {esperadas_defectuosas}")
                    
                    st.success(f"✅ **Respuesta:** Aproximadamente **{esperadas_defectuosas} piezas defectuosas**")
        
        elif caso_ing == "Caso 2: Confiabilidad de Sistemas":
            st.subheader("🔌 Caso 2: Confiabilidad de Sistemas")
            
            st.markdown("""
            **Contexto:**
            
            Un sistema electrónico tiene dos componentes críticos (A y B) que funcionan de manera independiente.
            """)
            
            col_comp1, col_comp2 = st.columns(2)
            
            with col_comp1:
                st.markdown("**Componente A:**")
                conf_A = st.slider("Confiabilidad de A:", 0.0, 1.0, 0.95, 0.01, key="conf_A")
                st.metric("P(A funciona)", f"{conf_A:.2f}")
                st.metric("P(A falla)", f"{1-conf_A:.2f}")
            
            with col_comp2:
                st.markdown("**Componente B:**")
                conf_B = st.slider("Confiabilidad de B:", 0.0, 1.0, 0.90, 0.01, key="conf_B")
                st.metric("P(B funciona)", f"{conf_B:.2f}")
                st.metric("P(B falla)", f"{1-conf_B:.2f}")
            
            # Preguntas
            st.markdown("### 📋 Preguntas:")
            
            with st.expander("**Pregunta 1:** Si el sistema falla cuando CUALQUIERA de los dos componentes falla, ¿cuál es la probabilidad de que el sistema funcione?"):
                st.markdown("**Solución:** El sistema funciona solo si AMBOS componentes funcionan")
                
                prob_sistema_funciona = conf_A * conf_B
                
                st.latex(r"P(\text{Sistema funciona}) = P(A \cap B) = P(A) \times P(B)")
                st.latex(f"P(\\text{{Sistema funciona}}) = {conf_A:.2f} \\times {conf_B:.2f} = {prob_sistema_funciona:.4f}")
                
                st.success(f"✅ **Respuesta:** {prob_sistema_funciona:.4f} o {prob_sistema_funciona*100:.2f}%")
                
                st.info("Nota: Esta fórmula asume independencia entre componentes.")
            
            with st.expander("**Pregunta 2:** ¿Cuál es la probabilidad de que el sistema falle?"):
                st.markdown("**Solución:** Usar el complemento")
                
                prob_sistema_falla = 1 - prob_sistema_funciona
                
                st.latex(f"P(\\text{{Sistema falla}}) = 1 - P(\\text{{Sistema funciona}}) = 1 - {prob_sistema_funciona:.4f} = {prob_sistema_falla:.4f}")
                
                st.success(f"✅ **Respuesta:** {prob_sistema_falla:.4f} o {prob_sistema_falla*100:.2f}%")
            
            with st.expander("**Pregunta 3:** Si tenemos un sistema redundante donde solo necesitamos que AL MENOS UNO funcione, ¿cuál es la confiabilidad?"):
                st.markdown("**Solución:** Es más fácil calcular la probabilidad de que AMBOS fallen")
                
                prob_ambos_fallan = (1 - conf_A) * (1 - conf_B)
                prob_al_menos_uno = 1 - prob_ambos_fallan
                
                st.latex(r"P(\text{Ambos fallan}) = P(A') \times P(B')")
                st.latex(f"P(\\text{{Ambos fallan}}) = {1-conf_A:.2f} \\times {1-conf_B:.2f} = {prob_ambos_fallan:.4f}")
                st.latex(f"P(\\text{{Al menos uno funciona}}) = 1 - {prob_ambos_fallan:.4f} = {prob_al_menos_uno:.4f}")
                
                st.success(f"✅ **Respuesta:** {prob_al_menos_uno:.4f} o {prob_al_menos_uno*100:.2f}%")
                
                st.info("💡 La redundancia aumenta significativamente la confiabilidad del sistema.")
        
        else:  # Caso 3
            st.subheader("⚡ Caso 3: Pruebas de Componentes Electrónicos")
            
            st.markdown("""
            **Contexto:**
            
            Una empresa prueba resistencias electrónicas. Las clasifica según su tolerancia:
            - **Alta precisión:** ±1% (más costosas)
            - **Precisión estándar:** ±5%
            - **Baja precisión:** ±10% (más económicas)
            """)
            
            total_resistencias = st.number_input("Total de resistencias probadas:", min_value=100, value=1000, step=100)
            
            col_r1, col_r2, col_r3 = st.columns(3)
            
            with col_r1:
                alta = st.number_input("Alta precisión:", min_value=0, max_value=total_resistencias, value=200)
            with col_r2:
                estandar = st.number_input("Precisión estándar:", min_value=0, max_value=total_resistencias, value=600)
            with col_r3:
                baja = total_resistencias - alta - estandar
                st.metric("Baja precisión", baja)
            
            if alta + estandar <= total_resistencias:
                # Visualización
                fig_resistencias = go.Figure(data=[go.Pie(
                    labels=['Alta Precisión (±1%)', 'Estándar (±5%)', 'Baja (±10%)'],
                    values=[alta, estandar, baja],
                    marker=dict(colors=['#27AE60', '#F39C12', '#E74C3C']),
                    textinfo='label+value+percent'
                )])
                
                fig_resistencias.update_layout(
                    title=f"Distribución de Resistencias (N={total_resistencias})",
                    height=400
                )
                
                st.plotly_chart(fig_resistencias, use_container_width=True)
                
                # Preguntas
                st.markdown("### 📋 Preguntas:")
                
                with  st.expander("**Pregunta 1:** ¿Cuál es la probabilidad de seleccionar una resistencia de alta precisión?"):
                    prob_alta = alta / total_resistencias
                    
                    st.latex(f"P(\\text{{Alta precisión}}) = \\frac{{{alta}}}{{{total_resistencias}}} = {prob_alta:.4f}")
                    
                    st.success(f"✅ **Respuesta:** {prob_alta:.4f} o {prob_alta*100:.2f}%")
                
                with st.expander("**Pregunta 2:** ¿Cuál es la probabilidad de seleccionar una resistencia que NO sea de baja precisión?"):
                    st.markdown("**Solución:** Usar el complemento")
                    
                    prob_baja = baja / total_resistencias
                    prob_no_baja = 1 - prob_baja
                    
                    st.latex(f"P(\\text{{NO baja}}) = 1 - P(\\text{{Baja}}) = 1 - \\frac{{{baja}}}{{{total_resistencias}}} = {prob_no_baja:.4f}")
                    
                    st.success(f"✅ **Respuesta:** {prob_no_baja:.4f} o {prob_no_baja*100:.2f}%")
                    
                    st.info("Alternativamente: P(Alta) + P(Estándar) = P(NO Baja)")
                
                with st.expander("**Pregunta 3:** Si un proyecto requiere al menos precisión estándar (±5% o mejor), ¿cuál es la probabilidad de que una resistencia aleatoria cumpla?"):
                    st.markdown("**Solución:** Necesitamos alta o estándar (eventos mutuamente excluyentes)")
                    
                    prob_cumple = (alta + estandar) / total_resistencias
                    
                    st.latex(r"P(\text{Cumple}) = P(\text{Alta} \cup \text{Estándar}) = P(\text{Alta}) + P(\text{Estándar})")
                    st.latex(f"P(\\text{{Cumple}}) = \\frac{{{alta} + {estandar}}}{{{total_resistencias}}} = {prob_cumple:.4f}")
                    
                    st.success(f"✅ **Respuesta:** {prob_cumple:.4f} o {prob_cumple*100:.2f}%")
                
                with st.expander("**Pregunta 4:** Si se necesitan 500 resistencias de alta precisión, ¿de cuántas se debe partir?"):
                    st.markdown("**Solución:**")
                    
                    necesarias_totales = int(500 / prob_alta) if prob_alta > 0 else 0
                    
                    st.latex(f"\\text{{Total necesario}} = \\frac{{500}}{{{prob_alta:.4f}}} \\approx {necesarias_totales}")
                    
                    st.success(f"✅ **Respuesta:** Se deben probar aproximadamente **{necesarias_totales} resistencias**")
            else:
                st.error("⚠️ Error: La suma de alta y estándar no puede superar el total")
    
    elif carrera_select == "💼 Negocios y Marketing":
        st.header("💼 Negocios y Marketing")
        
        caso_neg = st.radio(
            "Selecciona un caso:",
            [
                "Caso 1: Análisis de Conversión de Clientes",
                "Caso 2: Segmentación de Mercado",
                "Caso 3: Análisis de Abandono (Churn)"
            ]
        )
        
        if caso_neg == "Caso 1: Análisis de Conversión de Clientes":
            st.subheader("💰 Caso 1: Análisis de Conversión de Clientes")
            
            st.markdown("""
            **Contexto:**
            
            Una tienda online analiza el comportamiento de sus visitantes en el último mes.
            El embudo de ventas muestra:
            """)
            
            visitantes = st.number_input("Visitantes totales:", min_value=1, value=10000, step=100)
            
            col_n1, col_n2, col_n3 = st.columns(3)
            
            with col_n1:
                vieron_producto = st.number_input("Vieron un producto:", min_value=0, max_value=visitantes, value=5000)
            with col_n2:
                agregaron_carrito = st.number_input("Agregaron al carrito:", min_value=0, max_value=vieron_producto, value=1500)
            with col_n3:
                compraron = st.number_input("Completaron la compra:", min_value=0, max_value=agregaron_carrito, value=450)
            
            # Visualización del embudo
            fig_embudo = go.Figure(go.Funnel(
                y=['Visitantes', 'Vieron Producto', 'Carrito', 'Compra'],
                x=[visitantes, vieron_producto, agregaron_carrito, compraron],
                textinfo="value+percent initial",
                marker=dict(color=['#3498DB', '#2ECC71', '#F39C12', '#E74C3C'])
            ))
            
            fig_embudo.update_layout(
                title="Embudo de Conversión",
                height=500
            )
            
            st.plotly_chart(fig_embudo, use_container_width=True)
            
            # Preguntas
            st.markdown("### 📋 Preguntas:")
            
            with st.expander("**Pregunta 1:** ¿Cuál es la tasa de conversión final (visitante → comprador)?"):
                tasa_conversion = compraron / visitantes if visitantes > 0 else 0
                
                st.latex(f"P(\\text{{Conversión}}) = \\frac{{\\text{{Compraron}}}}{{\\text{{Visitantes}}}} = \\frac{{{compraron}}}{{{visitantes}}} = {tasa_conversion:.4f}")
                
                st.success(f"✅ **Respuesta:** {tasa_conversion:.4f} o {tasa_conversion*100:.2f}%")
                
                if tasa_conversion >= 0.05:
                    st.info("✅ Excelente tasa de conversión (≥5%)")
                elif tasa_conversion >= 0.02:
                    st.info("🟡 Tasa de conversión promedio (2-5%)")
                else:
                    st.warning("⚠️ Tasa de conversión baja (<2%)")
            
            with st.expander("**Pregunta 2:** De los que vieron un producto, ¿qué probabilidad hay de que lo agreguen al carrito?"):
                prob_carrito = agregaron_carrito / vieron_producto if vieron_producto > 0 else 0
                
                st.latex(f"P(\\text{{Carrito | Vio producto}}) = \\frac{{{agregaron_carrito}}}{{{vieron_producto}}} = {prob_carrito:.4f}")
                
                st.success(f"✅ **Respuesta:** {prob_carrito:.4f} o {prob_carrito*100:.2f}%")
            
            with st.expander("**Pregunta 3:** De los que agregaron al carrito, ¿qué probabilidad hay de que completen la compra?"):
                prob_compra = compraron / agregaron_carrito if agregaron_carrito > 0 else 0
                
                st.latex(f"P(\\text{{Compra | Carrito}}) = \\frac{{{compraron}}}{{{agregaron_carrito}}} = {prob_compra:.4f}")
                
                st.success(f"✅ **Respuesta:** {prob_compra:.4f} o {prob_compra*100:.2f}%")
                
                if prob_compra < 0.5:
                    st.warning("⚠️ Alta tasa de abandono del carrito. Considera: mejorar el proceso de pago, ofrecer envío gratis, o reducir costos ocultos.")
            
            with st.expander("**Pregunta 4:** Si llegan 50,000 visitantes el próximo mes, ¿cuántas ventas se esperan?"):
                ventas_esperadas = int(50000 * tasa_conversion) if tasa_conversion > 0 else 0
                
                st.latex(f"\\text{{Ventas esperadas}} = 50000 \\times {tasa_conversion:.4f} = {ventas_esperadas}")
                
                st.success(f"✅ **Respuesta:** Aproximadamente **{ventas_esperadas} ventas**")
        
        elif caso_neg == "Caso 2: Segmentación de Mercado":
            st.subheader("📊 Caso 2: Segmentación de Mercado")
            
            st.markdown("""
            **Contexto:**
            
            Una empresa segmenta su base de clientes según el valor de sus compras:
            - **VIP:** Compras > $1000
            - **Premium:** Compras $500-$1000
            - **Regular:** Compras $100-$500
            - **Ocasional:** Compras < $100
            """)
            
            total_clientes = st.number_input("Total de clientes:", min_value=100, value=5000, step=100)
            
            col_s1, col_s2, col_s3, col_s4 = st.columns(4)
            
            with col_s1:
                vip = st.number_input("VIP:", min_value=0, value=250, key="vip")
            with col_s2:
                premium = st.number_input("Premium:", min_value=0, value=750, key="premium")
            with col_s3:
                regular = st.number_input("Regular:", min_value=0, value=2000, key="regular")
            with col_s4:
                ocasional = total_clientes - vip - premium - regular
                st.metric("Ocasional", ocasional)
            
            if vip + premium + regular <= total_clientes:
                # Visualización
                fig_segmentos = go.Figure(data=[go.Pie(
                    labels=['VIP', 'Premium', 'Regular', 'Ocasional'],
                    values=[vip, premium, regular, ocasional],
                    marker=dict(colors=['#9B59B6', '#3498DB', '#2ECC71', '#95A5A6']),
                    textinfo='label+percent',
                    hole=0.3
                )])
                
                fig_segmentos.update_layout(
                    title=f"Segmentación de Clientes (N={total_clientes})",
                    height=400
                )
                
                st.plotly_chart(fig_segmentos, use_container_width=True)
                
                # Tabla resumen
                df_segmentos = pd.DataFrame({
                    'Segmento': ['VIP', 'Premium', 'Regular', 'Ocasional'],
                    'Cantidad': [vip, premium, regular, ocasional],
                    'Probabilidad': [
                        f"{vip/total_clientes:.4f}",
                        f"{premium/total_clientes:.4f}",
                        f"{regular/total_clientes:.4f}",
                        f"{ocasional/total_clientes:.4f}"
                    ],
                    'Porcentaje': [
                        f"{vip/total_clientes*100:.2f}%",
                        f"{premium/total_clientes*100:.2f}%",
                        f"{regular/total_clientes*100:.2f}%",
                        f"{ocasional/total_clientes*100:.2f}%"
                    ]
                })
                
                st.dataframe(df_segmentos, hide_index=True, use_container_width=True)
                
                # Preguntas
                st.markdown("### 📋 Preguntas:")
                
                with st.expander("**Pregunta 1:** Si se selecciona un cliente al azar, ¿cuál es la probabilidad de que sea VIP o Premium?"):
                    prob_vip_premium = (vip + premium) / total_clientes
                    
                    st.markdown("**Solución:** Eventos mutuamente excluyentes")
                    st.latex(r"P(\text{VIP} \cup \text{Premium}) = P(\text{VIP}) + P(\text{Premium})")
                    st.latex(f"P(\\text{{VIP o Premium}}) = \\frac{{{vip} + {premium}}}{{{total_clientes}}} = {prob_vip_premium:.4f}")
                    
                    st.success(f"✅ **Respuesta:** {prob_vip_premium:.4f} o {prob_vip_premium*100:.2f}%")
                
                with st.expander("**Pregunta 2:** ¿Cuál es la probabilidad de que un cliente NO sea ocasional?"):
                    prob_no_ocasional = 1 - (ocasional / total_clientes)
                    
                    st.markdown("**Solución:** Usar el complemento")
                    st.latex(f"P(\\text{{NO Ocasional}}) = 1 - P(\\text{{Ocasional}}) = 1 - \\frac{{{ocasional}}}{{{total_clientes}}} = {prob_no_ocasional:.4f}")
                    
                    st.success(f"✅ **Respuesta:** {prob_no_ocasional:.4f} o {prob_no_ocasional*100:.2f}%")
                
                with st.expander("**Pregunta 3:** Para una campaña exclusiva dirigida a clientes de alto valor (VIP + Premium), ¿a cuántos clientes se debe enviar?"):
                    clientes_alto_valor = vip + premium
                    
                    st.success(f"✅ **Respuesta:** Se debe enviar a **{clientes_alto_valor} clientes** ({clientes_alto_valor/total_clientes*100:.2f}% del total)")
                
                with st.expander("**Pregunta 4:** Si la empresa crece a 20,000 clientes manteniendo las mismas proporciones, ¿cuántos VIP habrá?"):
                    prop_vip = vip / total_clientes
                    vip_proyectados = int(20000 * prop_vip)
                    
                    st.latex(f"\\text{{VIP proyectados}} = 20000 \\times {prop_vip:.4f} = {vip_proyectados}")
                    
                    st.success(f"✅ **Respuesta:** Aproximadamente **{vip_proyectados} clientes VIP**")
            else:
                st.error("⚠️ Error: La suma de segmentos no puede superar el total")
        
        else:  # Caso 3
            st.subheader("📉 Caso 3: Análisis de Abandono (Churn)")
            
            st.markdown("""
            **Contexto:**
            
            Una empresa de suscripciones analiza la retención de clientes en el último año.
            """)
            
            clientes_inicio = st.number_input("Clientes al inicio del año:", min_value=100, value=1000, step=50)
            clientes_abandonaron = st.number_input("Clientes que cancelaron:", min_value=0, max_value=clientes_inicio, value=150)
            clientes_fin = clientes_inicio - clientes_abandonaron
            
            col_churn1, col_churn2 = st.columns(2)
            
            with col_churn1:
                st.metric("Clientes que permanecieron", clientes_fin)
            with col_churn2:
                tasa_abandono = clientes_abandonaron / clientes_inicio if clientes_inicio > 0 else 0
                st.metric("Tasa de Abandono (Churn)", f"{tasa_abandono*100:.2f}%")
            
            # Visualización
            fig_churn = go.Figure(data=[go.Pie(
                labels=['Permanecieron', 'Abandonaron'],
                values=[clientes_fin, clientes_abandonaron],
                marker=dict(colors=['#2ECC71', '#E74C3C']),
                hole=0.4,
                textinfo='label+value+percent'
            )])
            
            fig_churn.update_layout(
                title=f"Retención vs Abandono (N={clientes_inicio})",
                height=400
            )
            
            st.plotly_chart(fig_churn, use_container_width=True)
            
            # Preguntas
            st.markdown("### 📋 Preguntas:")
            
            with st.expander("**Pregunta 1:** ¿Cuál es la probabilidad de que un cliente abandone en un año?"):
                st.latex(f"P(\\text{{Abandono}}) = \\frac{{{clientes_abandonaron}}}{{{clientes_inicio}}} = {tasa_abandono:.4f}")
                
                st.success(f"✅ **Respuesta:** {tasa_abandono:.4f} o {tasa_abandono*100:.2f}%")
                
                if tasa_abandono <= 0.05:
                    st.info("✅ Excelente tasa de retención (abandono ≤5%)")
                elif tasa_abandono <= 0.15:
                    st.info("🟡 Tasa de abandono moderada (5-15%)")
                else:
                    st.warning("⚠️ Alta tasa de abandono (>15%). Requiere estrategias de retención.")
            
            with st.expander("**Pregunta 2:** ¿Cuál es la tasa de retención?"):
                tasa_retencion = 1 - tasa_abandono
                
                st.markdown("**Solución:** Usar el complemento")
                st.latex(f"P(\\text{{Retención}}) = 1 - P(\\text{{Abandono}}) = 1 - {tasa_abandono:.4f} = {tasa_retencion:.4f}")
                
                st.success(f"✅ **Respuesta:** {tasa_retencion:.4f} o {tasa_retencion*100:.2f}%")
            
            with st.expander("**Pregunta 3:** Si se adquieren 500 nuevos clientes, ¿cuántos se espera que permanezcan después de un año?"):
                esperados_permanecen = int(500 * tasa_retencion)
                
                st.latex(f"\\text{{Clientes que permanecen}} = 500 \\times {tasa_retencion:.4f} = {esperados_permanecen}")
                
                st.success(f"✅  **Respuesta:** Aproximadamente **{esperados_permanecen} clientes** permanecerán")
            
            with st.expander("**Pregunta 4:** Si queremos tener 2000 clientes activos al final del año, ¿cuántos debemos tener al inicio?"):
                st.markdown("**Solución:**")
                
                if tasa_retencion > 0:
                    necesarios_inicio = int(2000 / tasa_retencion)
                    
                    st.latex(f"\\text{{Clientes necesarios}} = \\frac{{2000}}{{{tasa_retencion:.4f}}} \\approx {necesarios_inicio}")
                    
                    st.success(f"✅ **Respuesta:** Se necesitan aproximadamente **{necesarios_inicio} clientes** al inicio del año")
                else:
                    st.error("No se puede calcular con tasa de retención 0")
    
    else:  # Derecho y Ciencias Sociales
        st.header("⚖️ Derecho y Ciencias Sociales")
        
        caso_der = st.radio(
            "Selecciona un caso:",
            [
                "Caso 1: Análisis de Evidencias en Juicio",
                "Caso 2: Encuestas y Muestreo",
                "Caso 3: Análisis de Sentencias"
            ]
        )
        
        if caso_der == "Caso 1: Análisis de Evidencias en Juicio":
            st.subheader("⚖️ Caso 1: Análisis de Evidencias en Juicio")
            
            st.markdown("""
            **Contexto:**
            
            En un caso judicial, se analizan diferentes tipos de evidencias presentadas.
            Un bufete revisa 200 casos históricos similares para estimar probabilidades.
            """)
            
            total_casos = st.number_input("Total de casos revisados:", min_value=50, value=200, step=10)
            
            col_e1, col_e2 = st.columns(2)
            
            with col_e1:
                evidencia_A = st.number_input("Casos con Evidencia Tipo A:", min_value=0, max_value=total_casos, value=120)
                evidencia_B = st.number_input("Casos con Evidencia Tipo B:", min_value=0, max_value=total_casos, value=80)
            
            with col_e2:
                ambas_evidencias = st.number_input("Casos con AMBAS evidencias:", min_value=0, max_value=min(evidencia_A, evidencia_B), value=40)
                casos_ganados_con_ambas = st.number_input("Ganados teniendo ambas:", min_value=0, max_value=ambas_evidencias, value=35)
            
            # Visualización con Diagrama de Venn (simulado)
            st.markdown("### 📊 Distribución de Evidencias")
            
            solo_A = evidencia_A - ambas_evidencias
            solo_B = evidencia_B - ambas_evidencias
            ninguna = total_casos - solo_A - solo_B - ambas_evidencias
            
            df_evidencias = pd.DataFrame({
                'Categoría': ['Solo A', 'Solo B', 'Ambas (A ∩ B)', 'Ninguna'],
                'Cantidad': [solo_A, solo_B, ambas_evidencias, ninguna],
                'Probabilidad': [
                    f"{solo_A/total_casos:.3f}",
                    f"{solo_B/total_casos:.3f}",
                    f"{ambas_evidencias/total_casos:.3f}",
                    f"{ninguna/total_casos:.3f}"
                ]
            })
            
            st.dataframe(df_evidencias, hide_index=True, use_container_width=True)
            
            fig_evidencias = go.Figure(data=[go.Bar(
                x=['Solo A', 'Solo B', 'Ambas (A ∩ B)', 'Ninguna'],
                y=[solo_A, solo_B, ambas_evidencias, ninguna],
                marker_color=['lightblue', 'lightcoral', 'purple', 'lightgray'],
                text=[solo_A, solo_B, ambas_evidencias, ninguna],
                textposition='outside'
            )])
            
            fig_evidencias.update_layout(
                title="Distribución de Evidencias en Casos",
                yaxis_title="Número de Casos",
                height=400
            )
            
            st.plotly_chart(fig_evidencias, use_container_width=True)
            
            # Preguntas
            st.markdown("### 📋 Preguntas:")
            
            with st.expander("**Pregunta 1:** ¿Cuál es la probabilidad de que un caso tenga Evidencia A?"):
                prob_A = evidencia_A / total_casos
                
                st.latex(f"P(A) = \\frac{{{evidencia_A}}}{{{total_casos}}} = {prob_A:.4f}")
                
                st.success(f"✅ **Respuesta:** {prob_A:.4f} o {prob_A*100:.2f}%")
            
            with st.expander("**Pregunta 2:** ¿Cuál es la probabilidad de que tenga al menos una de las dos evidencias (A ∪ B)?"):
                st.markdown("**Solución:** Usar la fórmula de la unión")
                
                prob_B = evidencia_B / total_casos
                prob_AB = ambas_evidencias / total_casos
                prob_union = prob_A + prob_B - prob_AB
                
                st.latex(r"P(A \cup B) = P(A) + P(B) - P(A \cap B)")
                st.latex(f"P(A \\cup B) = {prob_A:.3f} + {prob_B:.3f} - {prob_AB:.3f} = {prob_union:.4f}")
                
                st.success(f"✅ **Respuesta:** {prob_union:.4f} o {prob_union*100:.2f}%")
                
                # Verificación
                casos_al_menos_una = solo_A + solo_B + ambas_evidencias
                prob_verificacion = casos_al_menos_una / total_casos
                
                st.info(f"✓ Verificación: {casos_al_menos_una}/{total_casos} = {prob_verificacion:.4f}")
            
            with st.expander("**Pregunta 3:** ¿Cuál es la probabilidad de que tenga ambas evidencias (A ∩ B)?"):
                st.latex(f"P(A \\cap B) = \\frac{{{ambas_evidencias}}}{{{total_casos}}} = {prob_AB:.4f}")
                
                st.success(f"✅ **Respuesta:** {prob_AB:.4f} o {prob_AB*100:.2f}%")
            
            with st.expander("**Pregunta 4:** Si un caso tiene ambas evidencias, ¿cuál es la probabilidad histórica de ganarlo?"):
                if ambas_evidencias > 0:
                    prob_ganar_con_ambas = casos_ganados_con_ambas / ambas_evidencias
                    
                    st.latex(f"P(\\text{{Ganar | Ambas evidencias}}) = \\frac{{{casos_ganados_con_ambas}}}{{{ambas_evidencias}}} = {prob_ganar_con_ambas:.4f}")
                    
                    st.success(f"✅ **Respuesta:** {prob_ganar_con_ambas:.4f} o {prob_ganar_con_ambas*100:.2f}%")
                    
                    if prob_ganar_con_ambas >= 0.8:
                        st.info("✅ Tener ambas evidencias da una probabilidad muy alta de éxito")
                else:
                    st.warning("No hay casos con ambas evidencias para calcular")
        
        elif caso_der == "Caso 2: Encuestas y Muestreo":
            st.subheader("📋 Caso 2: Encuestas y Muestreo")
            
            st.markdown("""
            **Contexto:**
            
            Una organización realiza una encuesta sobre opinión pública respecto a una nueva ley.
            Se encuestaron personas de diferentes grupos etarios.
            """)
            
            total_encuestados = st.number_input("Total de encuestados:", min_value=100, value=1000, step=50)
            
            col_edad1, col_edad2, col_edad3 = st.columns(3)
            
            with col_edad1:
                jovenes = st.number_input("Jóvenes (18-35):", min_value=0, value=400, key="jovenes")
                favor_jovenes = st.number_input("A favor (jóvenes):", min_value=0, max_value=jovenes, value=280)
            
            with col_edad2:
                adultos = st.number_input("Adultos (36-55):", min_value=0, value=400, key="adultos")
                favor_adultos = st.number_input("A favor (adultos):", min_value=0, max_value=adultos, value=200)
            
            with col_edad3:
                mayores = total_encuestados - jovenes - adultos
                st.metric("Mayores (56+)", mayores)
                favor_mayores = st.number_input("A favor (mayores):", min_value=0, max_value=mayores, value=80)
            
            if jovenes + adultos <= total_encuestados:
                # Calcular totales
                total_favor = favor_jovenes + favor_adultos + favor_mayores
                total_contra = total_encuestados - total_favor
                
                # Visualización
                fig_encuesta = make_subplots(
                    rows=1, cols=2,
                    subplot_titles=('Por Grupo Etario', 'Total General'),
                    specs=[[{'type': 'bar'}, {'type': 'pie'}]]
                )
                
                # Gráfico de barras
                fig_encuesta.add_trace(
                    go.Bar(
                        name='A favor',
                        x=['Jóvenes', 'Adultos', 'Mayores'],
                        y=[favor_jovenes, favor_adultos, favor_mayores],
                        marker_color='lightgreen'
                    ),
                    row=1, col=1
                )
                
                fig_encuesta.add_trace(
                    go.Bar(
                        name='En contra',
                        x=['Jóvenes', 'Adultos', 'Mayores'],
                        y=[jovenes - favor_jovenes, adultos - favor_adultos, mayores - favor_mayores],
                        marker_color='lightcoral'
                    ),
                    row=1, col=1
                )
                
                # Gráfico de pastel
                fig_encuesta.add_trace(
                    go.Pie(
                        labels=['A favor', 'En contra'],
                        values=[total_favor, total_contra],
                        marker=dict(colors=['#2ECC71', '#E74C3C'])
                    ),
                    row=1, col=2
                )
                
                fig_encuesta.update_layout(
                    height=400,
                    showlegend=True,
                    barmode='stack'
                )
                
                st.plotly_chart(fig_encuesta, use_container_width=True)
                
                # Tabla resumen
                df_encuesta = pd.DataFrame({
                    'Grupo': ['Jóvenes', 'Adultos', 'Mayores', 'TOTAL'],
                    'Total': [jovenes, adultos, mayores, total_encuestados],
                    'A favor': [favor_jovenes, favor_adultos, favor_mayores, total_favor],
                    '% A favor': [
                        f"{favor_jovenes/jovenes*100:.1f}%" if jovenes > 0 else "0%",
                        f"{favor_adultos/adultos*100:.1f}%" if adultos > 0 else "0%",
                        f"{favor_mayores/mayores*100:.1f}%" if mayores > 0 else "0%",
                        f"{total_favor/total_encuestados*100:.1f}%"
                    ]
                })
                
                st.dataframe(df_encuesta, hide_index=True, use_container_width=True)
                
                # Preguntas
                st.markdown("### 📋 Preguntas:")
                
                with st.expander("**Pregunta 1:** Si se selecciona una persona al azar, ¿cuál es la probabilidad de que esté a favor?"):
                    prob_favor = total_favor / total_encuestados
                    
                    st.latex(f"P(\\text{{A favor}}) = \\frac{{{total_favor}}}{{{total_encuestados}}} = {prob_favor:.4f}")
                    
                    st.success(f"✅ **Respuesta:** {prob_favor:.4f} o {prob_favor*100:.2f}%")
                
                with st.expander("**Pregunta 2:** ¿Cuál es la probabilidad de que sea joven Y esté a favor?"):
                    prob_joven_favor = favor_jovenes / total_encuestados
                    
                    st.latex(f"P(\\text{{Joven}} \\cap \\text{{A favor}}) = \\frac{{{favor_jovenes}}}{{{total_encuestados}}} = {prob_joven_favor:.4f}")
                    
                    st.success(f"✅ **Respuesta:** {prob_joven_favor:.4f} o {prob_joven_favor*100:.2f}%")
                
                with st.expander("**Pregunta 3:** ¿Qué grupo etario tiene mayor apoyo (proporcionalmente)?"):
                    if jovenes > 0 and adultos > 0 and mayores > 0:
                        prop_jovenes = favor_jovenes / jovenes
                        prop_adultos = favor_adultos / adultos
                        prop_mayores = favor_mayores / mayores
                        
                        grupos = [
                            ('Jóvenes', prop_jovenes),
                            ('Adultos', prop_adultos),
                            ('Mayores', prop_mayores)
                        ]
                        
                        grupos_sorted = sorted(grupos, key=lambda x: x[1], reverse=True)
                        
                        st.markdown("**Proporciones de apoyo:**")
                        for grupo, prop in grupos_sorted:
                            st.markdown(f"- {grupo}: {prop:.4f} ({prop*100:.2f}%)")
                        
                        st.success(f"✅ **Respuesta:** {grupos_sorted[0][0]} con {grupos_sorted[0][1]*100:.2f}%")
                
                with st.expander("**Pregunta 4:** Si la población total es 100,000 personas con la misma distribución, ¿cuántas estarían a favor?"):
                    proyeccion_favor = int(100000 * prob_favor)
                    
                    st.latex(f"\\text{{A favor (proyección)}} = 100000 \\times {prob_favor:.4f} = {proyeccion_favor}")
                    
                    st.success(f"✅ **Respuesta:** Aproximadamente **{proyeccion_favor:,} personas**")
            else:
                st.error("⚠️ Error: La suma de jóvenes y adultos no puede superar el total")
        
        else:  # Caso 3
            st.subheader("⚖️ Caso 3: Análisis de Sentencias")
            
            st.markdown("""
            **Contexto:**
            
            Un estudio analiza 500 sentencias judiciales en casos de un tipo específico,
            clasificándolas por gravedad y resultado.
            """)
            
            total_sentencias = 500
            
            st.markdown("**Distribución de casos:**")
            
            col_grav1, col_grav2, col_grav3 = st.columns(3)
            
            with col_grav1:
                leves = st.number_input("Casos leves:", min_value=0, value=200, key="leves")
                condena_leves = st.number_input("Condenas (leves):", min_value=0, max_value=leves, value=80)
            
            with col_grav2:
                moderados = st.number_input("Casos moderados:", min_value=0, value=200, key="moderados")
                condena_moderados = st.number_input("Condenas (moderados):", min_value=0, max_value=moderados, value=140)
            
            with col_grav3:
                graves = st.number_input("Casos graves:", min_value=0, value=100, key="graves")
                condena_graves = st.number_input("Condenas (graves):", min_value=0, max_value=graves, value=85)
            
            # Verificar que suma 500
            suma_verificacion = leves + moderados + graves
            
            if suma_verificacion == total_sentencias:
                # Calcular totales
                total_condenas = condena_leves + condena_moderados + condena_graves
                total_absoluciones = total_sentencias - total_condenas
                
                # Visualización
                fig_sentencias = make_subplots(
                    rows=1, cols=2,
                    subplot_titles=('Por Gravedad', 'Resultado Total'),
                    specs=[[{'type': 'bar'}, {'type': 'pie'}]]
                )
                
                # Barras apiladas
                fig_sentencias.add_trace(
                    go.Bar(
                        name='Condenas',
                        x=['Leves', 'Moderados', 'Graves'],
                        y=[condena_leves, condena_moderados, condena_graves],
                        marker_color='#E74C3C'
                    ),
                    row=1, col=1
                )
                
                fig_sentencias.add_trace(
                    go.Bar(
                        name='Absoluciones',
                        x=['Leves', 'Moderados', 'Graves'],
                        y=[leves - condena_leves, moderados - condena_moderados, graves - condena_graves],
                        marker_color='#2ECC71'
                    ),
                    row=1, col=1
                )
                
                # Pastel total
                fig_sentencias.add_trace(
                    go.Pie(
                        labels=['Condenas', 'Absoluciones'],
                        values=[total_condenas, total_absoluciones],
                        marker=dict(colors=['#E74C3C', '#2ECC71'])
                    ),
                    row=1, col=2
                )
                
                fig_sentencias.update_layout(
                    height=400,
                    showlegend=True,
                    barmode='stack'
                )
                
                st.plotly_chart(fig_sentencias, use_container_width=True)
                
                # Tabla resumen
                df_sentencias = pd.DataFrame({
                    'Gravedad': ['Leves', 'Moderados', 'Graves', 'TOTAL'],
                    'Total': [leves, moderados, graves, total_sentencias],
                    'Condenas': [condena_leves, condena_moderados, condena_graves, total_condenas],
                    'Tasa Condena': [
                        f"{condena_leves/leves*100:.1f}%" if leves > 0 else "0%",
                        f"{condena_moderados/moderados*100:.1f}%" if moderados > 0 else "0%",
                        f"{condena_graves/graves*100:.1f}%" if graves > 0 else "0%",
                        f"{total_condenas/total_sentencias*100:.1f}%"
                    ]
                })
                
                st.dataframe(df_sentencias, hide_index=True, use_container_width=True)
                
                # Preguntas
                st.markdown("### 📋 Preguntas:")
                
                with st.expander("**Pregunta 1:** ¿Cuál es la probabilidad de que una sentencia resulte en condena?"):
                    prob_condena = total_condenas / total_sentencias
                    
                    st.latex(f"P(\\text{{Condena}}) = \\frac{{{total_condenas}}}{{{total_sentencias}}} = {prob_condena:.4f}")
                    
                    st.success(f"✅ **Respuesta:** {prob_condena:.4f} o {prob_condena*100:.2f}%")
                
                with st.expander("**Pregunta 2:** En casos graves, ¿cuál es la probabilidad de condena?"):
                    if graves > 0:
                        prob_condena_graves = condena_graves / graves
                        
                        st.latex(f"P(\\text{{Condena | Grave}}) = \\frac{{{condena_graves}}}{{{graves}}} = {prob_condena_graves:.4f}")
                        
                        st.success(f"✅ **Respuesta:** {prob_condena_graves:.4f} o {prob_condena_graves*100:.2f}%")
                
                with st.expander("**Pregunta 3:** ¿Cuál es la probabilidad de absolución?"):
                    prob_absolucion = 1 - prob_condena
                    
                    st.markdown("**Solución:** Usar el complemento")
                    st.latex(f"P(\\text{{Absolución}}) = 1 - P(\\text{{Condena}}) = 1 - {prob_condena:.4f} = {prob_absolucion:.4f}")
                    
                    st.success(f"✅ **Respuesta:** {prob_absolucion:.4f} o {prob_absolucion*100:.2f}%")
                
                with st.expander("**Pregunta 4:** ¿Qué tipo de caso tiene mayor probabilidad de absolución?"):
                    if leves > 0 and moderados > 0 and graves > 0:
                        abs_leves = (leves - condena_leves) / leves
                        abs_moderados = (moderados - condena_moderados) / moderados
                        abs_graves = (graves - condena_graves) / graves
                        
                        tipos = [
                            ('Leves', abs_leves),
                            ('Moderados', abs_moderados),
                            ('Graves', abs_graves)
                        ]
                        
                        tipos_sorted = sorted(tipos, key=lambda x: x[1], reverse=True)
                        
                        st.markdown("**Probabilidades de absolución:**")
                        for tipo, prob in tipos_sorted:
                            st.markdown(f"- {tipo}: {prob:.4f} ({prob*100:.2f}%)")
                        
                        st.success(f"✅ **Respuesta:** Casos {tipos_sorted[0][0]} con {tipos_sorted[0][1]*100:.2f}%")
            else:
                st.error(f"⚠️ Error: La suma debe ser exactamente 500 (actualmente: {suma_verificacion})")

elif page == "8. 🧮 Calculadora de Probabilidades":
    st.title("🧮 Calculadora de Probabilidades Compuestas")
    st.markdown("### Calcula probabilidades de unión, intersección y complemento")
    
    st.markdown("---")
    
    # Tipo de cálculo
    tipo_calculo = st.selectbox(
        "¿Qué deseas calcular?",
        [
            "P(A ∪ B) - Unión de eventos",
            "P(A ∩ B) - Intersección de eventos",
            "P(A') - Complemento de un evento",
            "P(A - B) - Diferencia de eventos",
            "Verificar Axiomas de Kolmogorov"
        ]
    )
    
    if tipo_calculo == "P(A ∪ B) - Unión de eventos":
        st.subheader("🔵 Cálculo de P(A ∪ B)")
        
        st.markdown("""
        ### Fórmula General:
        """)
        
        st.latex(r"P(A \cup B) = P(A) + P(B) - P(A \cap B)")
        
        st.info("""
        **Cuándo usar:**
        - Cuando quieres saber la probabilidad de que ocurra **A o B (o ambos)**
        - Se resta la intersección para evitar el doble conteo
        """)
        
        col_u1, col_u2, col_u3 = st.columns(3)
        
        with col_u1:
            P_A = st.number_input("P(A):", min_value=0.0, max_value=1.0, value=0.4, step=0.01, key="calc_PA")
        with col_u2:
            P_B = st.number_input("P(B):", min_value=0.0, max_value=1.0, value=0.5, step=0.01, key="calc_PB")
        with col_u3:
            max_interseccion = min(P_A, P_B)
            P_AB = st.number_input("P(A ∩ B):", min_value=0.0, max_value=max_interseccion, value=min(0.2, max_interseccion), step=0.01, key="calc_PAB")
        
        # Calcular
        P_union = P_A + P_B - P_AB
        
        if P_union <= 1.0:
            st.markdown("### 📊 Resultado:")
            
            st.latex(f"P(A \\cup B) = {P_A:.3f} + {P_B:.3f} - {P_AB:.3f} = {P_union:.4f}")
            
            st.success(f"### ✅ P(A ∪ B) = {P_union:.4f} ({P_union*100:.2f}%)")
            
            # Visualización con diagrama de Venn conceptual
            fig_union_calc = go.Figure()
            
            # Barras para visualizar componentes
            categorias = ['Solo A', 'A ∩ B', 'Solo B']
            valores = [P_A - P_AB, P_AB, P_B - P_AB]
            colores = ['lightblue', 'purple', 'lightcoral']
            
            fig_union_calc.add_trace(go.Bar(
                x=categorias,
                y=valores,
                marker_color=colores,
                text=[f"{v:.3f}" for v in valores],
                textposition='outside'
            ))
            
            fig_union_calc.update_layout(
                title=f"Componentes de P(A ∪ B) = {P_union:.4f}",
                yaxis_title="Probabilidad",
                yaxis=dict(range=[0, max(valores) + 0.1]),
                height=400
            )
            
            st.plotly_chart(fig_union_calc, use_container_width=True)
            
            # Caso especial: eventos mutuamente excluyentes
            if P_AB == 0:
                st.warning("""
                ⚠️ **Caso Especial Detectado:** P(A ∩ B) = 0
                
                Los eventos A y B son **mutuamente excluyentes** (no pueden ocurrir simultáneamente).
                
                En este caso, la fórmula se simplifica:
                
                $P(A \\cup B) = P(A) + P(B)$ (Axioma 3 de Kolmogorov)
                """)
        else:
            st.error(f"⚠️ Error: P(A ∪ B) = {P_union:.4f} > 1.0 (imposible). Verifica los valores ingresados.")
    
    elif tipo_calculo == "P(A ∩ B) - Intersección de eventos":
        st.subheader("🟢 Cálculo de P(A ∩ B)")
        
        st.markdown("""
        ### Concepto:
        
        La **intersección** $P(A \\cap B)$ es la probabilidad de que **ambos eventos ocurran simultáneamente**.
        """)
        
        st.info("""
        **Para eventos independientes:**
        
        $P(A \\cap B) = P(A) \\times P(B)$
        
        **Para eventos dependientes:**
        
        Se requiere información adicional (probabilidad condicional).
        """)
        
        independencia = st.radio(
            "¿Los eventos son independientes?",
            ["Sí, son independientes", "No, tengo P(A ∩ B) directamente"],
            horizontal=True
        )
        
        if independencia == "Sí, son independientes":
            col_i1, col_i2 = st.columns(2)
            
            with col_i1:
                P_A_ind = st.number_input("P(A):", min_value=0.0, max_value=1.0, value=0.6, step=0.01, key="ind_PA")
            with col_i2:
                P_B_ind = st.number_input("P(B):", min_value=0.0, max_value=1.0, value=0.4, step=0.01, key="ind_PB")
            
            P_inter = P_A_ind * P_B_ind
            
            st.markdown("### 📊 Resultado:")
            
            st.latex(f"P(A \\cap B) = P(A) \\times P(B) = {P_A_ind:.3f} \\times {P_B_ind:.3f} = {P_inter:.4f}")
            
            st.success(f"### ✅ P(A ∩ B) = {P_inter:.4f} ({P_inter*100:.2f}%)")
            
            st.info("""
            **Interpretación de Independencia:**
            
            Dos eventos son independientes si la ocurrencia de uno NO afecta la probabilidad del otro.
            
            **Ejemplos:**
            - Lanzar dos monedas diferentes
            - Resultado de dos dados
            - Sacar dos cartas CON reemplazo
            """)
            
        else:
            P_inter_directo = st.number_input("P(A ∩ B):", min_value=0.0, max_value=1.0, value=0.15, step=0.01)
            
            st.success(f"### ✅ P(A ∩ B) = {P_inter_directo:.4f} ({P_inter_directo*100:.2f}%)")
            
            st.info("""
            **Eventos Dependientes:**
            
            En este caso, la ocurrencia de un evento SÍ afecta la probabilidad del otro.
            
            **Ejemplos:**
            - Sacar dos cartas SIN reemplazo
            - Probabilidad de lluvia dado que está nublado
            - Probabilidad de enfermedad dado síntomas
            """)
    
    elif tipo_calculo == "P(A') - Complemento de un evento":
        st.subheader("⚪ Cálculo de P(A') - Complemento")
        
        st.markdown("""
        ### Fórmula:
        """)
        
        st.latex(r"P(A') = 1 - P(A)")
        
        st.info("""
        **Significado:**
        
        El complemento $A'$ representa **todos los resultados que NO están en A**.
        
        **Propiedades:**
        - $P(A) + P(A') = 1$
        - $A \\cap A' = \\emptyset$ (mutuamente excluyentes)
        - $A \\cup A' = S$ (cubren todo el espacio muestral)
        """)
        
        P_A_comp = st.slider("P(A):", min_value=0.0, max_value=1.0, value=0.35, step=0.01)
        
        P_A_complemento = 1 - P_A_comp
        
        st.markdown("### 📊 Resultado:")
        
        st.latex(f"P(A') = 1 - P(A) = 1 - {P_A_comp:.3f} = {P_A_complemento:.4f}")
        
        col_comp1, col_comp2 = st.columns(2)
        
        with col_comp1:
            st.metric("P(A)", f"{P_A_comp:.4f}", delta=f"{P_A_comp*100:.2f}%")
        with col_comp2:
            st.metric("P(A')", f"{P_A_complemento:.4f}", delta=f"{P_A_complemento*100:.2f}%")
        
        # Visualización
        fig_comp_calc = go.Figure(data=[go.Pie(
            labels=['P(A)', "P(A')"],
            values=[P_A_comp, P_A_complemento],
            marker=dict(colors=['#3498DB', '#E74C3C']),
            textinfo='label+percent',
            hole=0.4
        )])
        
        fig_comp_calc.update_layout(
            title=f"Distribución: A y su Complemento (suman 1.0)",
            height=400
        )
        
        st.plotly_chart(fig_comp_calc, use_container_width=True)
        
        st.success(f"✅ Verificación: P(A) + P(A') = {P_A_comp:.4f} + {P_A_complemento:.4f} = {P_A_comp + P_A_complemento:.4f} = 1.0 ✓")
    
    elif tipo_calculo == "P(A - B) - Diferencia de eventos":
        st.subheader("🟣 Cálculo de P(A - B) - Diferencia")
        
        st.markdown("""
        ### Fórmula:
        """)
        
        st.latex(r"P(A - B) = P(A) - P(A \cap B)")
        
        st.info("""
        **Significado:**
        
        $A - B$ representa los elementos que están en $A$ pero **NO** están en $B$.
        
        Es la "parte exclusiva" de A.
        """)
        
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            P_A_dif = st.number_input("P(A):", min_value=0.0, max_value=1.0, value=0.5, step=0.01, key="dif_PA")
        with col_d2:
            max_inter_dif = P_A_dif
            P_AB_dif = st.number_input("P(A ∩ B):", min_value=0.0, max_value=max_inter_dif, value=min(0.2, max_inter_dif), step=0.01, key="dif_PAB")
        
        P_diferencia = P_A_dif - P_AB_dif
        
        st.markdown("### 📊 Resultado:")
        
        st.latex(f"P(A - B) = P(A) - P(A \\cap B) = {P_A_dif:.3f} - {P_AB_dif:.3f} = {P_diferencia:.4f}")
        
        st.success(f"### ✅ P(A - B) = {P_diferencia:.4f} ({P_diferencia*100:.2f}%)")
        
        # Visualización
        fig_dif = go.Figure(data=[go.Bar(
            x=['A - B (Exclusivo de A)', 'A ∩ B (Común)'],
            y=[P_diferencia, P_AB_dif],
            marker_color=['purple', 'orange'],
            text=[f"{P_diferencia:.3f}", f"{P_AB_dif:.3f}"],
            textposition='outside'
        )])
        
        fig_dif.update_layout(
            title=f"Descomposición de A: Total = {P_A_dif:.4f}",
            yaxis_title="Probabilidad",
            height=400
        )
        
        st.plotly_chart(fig_dif, use_container_width=True)
        
        st.info(f"✓ Verificación: P(A - B) + P(A ∩ B) = {P_diferencia:.4f} + {P_AB_dif:.4f} = {P_A_dif:.4f} = P(A) ✓")
    
    else:  # Verificar Axiomas
        st.subheader("✅ Verificador de Axiomas de Kolmogorov")
        
        st.markdown("""
        Ingresa un conjunto de probabilidades y verificaremos si cumplen con los axiomas.
        """)
        
        num_eventos = st.slider("Número de eventos en el espacio muestral:", 2, 10, 4)
        
        st.markdown(f"### Ingresa las probabilidades de {num_eventos} eventos mutuamente excluyentes:")
        
        cols = st.columns(min(num_eventos, 4))
        probs_axiomas = []
        
        for i in range(num_eventos):
            with cols[i % 4]:
                prob = st.number_input(f"P(E{i+1}):", min_value=0.0, max_value=1.0, value=1.0/num_eventos, step=0.01, key=f"axioma_{i}")
                probs_axiomas.append(prob)
        
        # Verificación de axiomas
        st.markdown("---")
        st.markdown("### 🔍 Verificación de Axiomas:")
        
        # Axioma 1: No negatividad
        st.markdown("#### 📏 Axioma 1: No Negatividad")
        st.latex(r"P(E_i) \geq 0 \text{ para todo } i")
        
        axioma1_cumple = all(p >= 0 for p in probs_axiomas)
        
        if axioma1_cumple:
            st.success("✅ **Axioma 1 cumplido:** Todas las probabilidades son ≥ 0")
        else:
            st.error("❌ **Axioma 1 NO cumplido:** Hay probabilidades negativas")
        
        for i, p in enumerate(probs_axiomas):
            if p < 0:
                st.warning(f"⚠️ P(E{i+1}) = {p} < 0")
        
        # Axioma 2: Normalización (suma = 1)
        st.markdown("#### ✅ Axioma 2: Certeza (Normalización)")
        st.latex(r"P(S) = \sum_{i=1}^{n} P(E_i) = 1")
        
        suma_total = sum(probs_axiomas)
        
        st.info(f"**Suma de probabilidades:** {' + '.join([f'{p:.3f}' for p in probs_axiomas])} = {suma_total:.6f}")
        
        tolerancia = 0.0001
        axioma2_cumple = abs(suma_total - 1.0) < tolerancia
        
        if axioma2_cumple:
            st.success(f"✅ **Axioma 2 cumplido:** Suma = {suma_total:.6f} ≈ 1.0")
        else:
            diferencia = suma_total - 1.0
            if diferencia > 0:
                st.error(f"❌ **Axioma 2 NO cumplido:** Suma = {suma_total:.6f} > 1.0 (exceso de {diferencia:.6f})")
            else:
                st.error(f"❌ **Axioma 2 NO cumplido:** Suma = {suma_total:.6f} < 1.0 (falta {-diferencia:.6f})")
        
        # Axioma 3: Aditividad (implícito si son mutuamente excluyentes)
        st.markdown("#### ➕ Axioma 3: Aditividad")
        st.latex(r"P(E_i \cup E_j) = P(E_i) + P(E_j) \text{ si } E_i \cap E_j = \emptyset")
        
        st.info("""
        **Nota:** Este axioma se cumple automáticamente si los eventos son mutuamente excluyentes 
        (lo cual asumimos en este caso).
        
        Para cualquier par de eventos $E_i$ y $E_j$:
        - $P(E_i \\cup E_j) = P(E_i) + P(E_j)$ porque $E_i \\cap E_j = \\emptyset$
        """)
        
        st.success("✅ **Axioma 3 cumplido** (por definición de eventos mutuamente excluyentes)")
        
        # Resumen final
        st.markdown("---")
        st.markdown("### 📋 Resumen Final:")
        
        if axioma1_cumple and axioma2_cumple:
            st.success("""
            ### ✅ ¡Todos los Axiomas se Cumplen!
            
            Este conjunto de probabilidades es **válido** y puede representar un espacio de probabilidad.
            """)
            
            # Visualización
            fig_axiomas = go.Figure(data=[go.Bar(
                x=[f"E{i+1}" for i in range(num_eventos)],
                y=probs_axiomas,
                marker_color='lightgreen',
                text=[f"{p:.3f}" for p in probs_axiomas],
                textposition='outside'
            )])
            
            fig_axiomas.add_hline(
                y=1.0,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Suma Total = {suma_total:.4f}"
            )
            
            fig_axiomas.update_layout(
                title="Distribución de Probabilidades",
                xaxis_title="Evento",
                yaxis_title="Probabilidad",
                yaxis=dict(range=[0, max(probs_axiomas) + 0.1]),
                height=400
            )
            
            st.plotly_chart(fig_axiomas, use_container_width=True)
            
        else:
            st.error("""
            ### ❌ Los Axiomas NO se Cumplen
            
            Este conjunto de probabilidades **NO es válido**. 
            Ajusta los valores para que cumplan con todos los axiomas.
            """)

elif page == "9. 🎯 Ejercicios Interactivos":
    st.title("🎯 Ejercicios Interactivos")
    st.markdown("### Practica tus conocimientos con ejercicios de diferentes niveles")
    
    st.markdown("---")
    
    # Selección de nivel
    nivel = st.selectbox(
        "Selecciona el nivel de dificultad:",
        ["🟢 Nivel 1: Básico", "🟡 Nivel 2: Intermedio", "🔴 Nivel 3: Avanzado"]
    )
    
    if nivel == "🟢 Nivel 1: Básico":
        st.subheader("🟢 Nivel Básico: Conceptos Fundamentales")
        
        ejercicios_basicos = [
            {
                "pregunta": "¿Cuál es el espacio muestral al lanzar una moneda?",
                "opciones": [
                    "{Cara}",
                    "{Cara, Sello}",
                    "{1, 2}",
                    "{0, 1}"
                ],
                "respuesta": "{Cara, Sello}",
                "explicacion": "El espacio muestral incluye TODOS los resultados posibles. Al lanzar una moneda, los únicos resultados posibles son Cara o Sello."
            },
            {
                "pregunta": "Si P(A) = 0.3, ¿cuál es P(A')?",
                "opciones": [
                    "0.3",
                    "0.7",
                    "1.0",
                    "0.0"
                ],
                "respuesta": "0.7",
                "explicacion": "El complemento se calcula como: P(A') = 1 - P(A) = 1 - 0.3 = 0.7"
            },
            {
                "pregunta": "¿Cuál es la probabilidad de obtener un número par al lanzar un dado de 6 caras?",
                "opciones": [
                    "1/6",
                    "1/3",
                    "1/2",
                    "2/3"
                ],
                "respuesta": "1/2",
                "explicacion": "Los números pares son {2, 4, 6}, es decir, 3 de 6 resultados. P(Par) = 3/6 = 1/2"
            },
            {
                "pregunta": "Si un evento es imposible, su probabilidad es:",
                "opciones": [
                    "1",
                    "0.5",
                    "0",
                    "-1"
                ],
                "respuesta": "0",
                "explicacion": "Un evento imposible nunca puede ocurrir, por lo tanto su probabilidad es 0. Ejemplo: obtener un 7 al lanzar un dado de 6 caras."
            },
            {
                "pregunta": "¿Qué significa que dos eventos sean mutuamente excluyentes?",
                "opciones": [
                    "Siempre ocurren juntos",
                    "No pueden ocurrir simultáneamente",
                    "Tienen la misma probabilidad",
                    "Son independientes"
                ],
                "respuesta": "No pueden ocurrir simultáneamente",
                "explicacion": "Eventos mutuamente excluyentes son aquellos que no pueden suceder al mismo tiempo. Su intersección es vacía: A ∩ B = ∅"
            }
        ]
        
        for i, ejercicio in enumerate(ejercicios_basicos):
            with st.expander(f"**Ejercicio {i+1}:** {ejercicio['pregunta']}"):
                respuesta_usuario = st.radio(
                    "Selecciona tu respuesta:",
                    ejercicio['opciones'],
                    key=f"basico_{i}"
                )
                
                if st.button("Verificar", key=f"btn_basico_{i}"):
                    if respuesta_usuario == ejercicio['respuesta']:
                        st.success("✅ ¡Correcto!")
                        st.info(f"**Explicación:** {ejercicio['explicacion']}")
                    else:
                        st.error(f"❌ Incorrecto. La respuesta correcta es: **{ejercicio['respuesta']}**")
                        st.info(f"**Explicación:** {ejercicio['explicacion']}")
    
    elif nivel == "🟡 Nivel 2: Intermedio":
        st.subheader("🟡 Nivel Intermedio: Cálculos y Aplicaciones")
        
        ejercicios_intermedios = [
            {
                "pregunta": "En una urna hay 5 bolas rojas y 3 azules. ¿Cuál es la probabilidad de sacar una bola roja?",
                "opciones": [
                    "5/8",
                    "3/8",
                    "1/2",
                    "5/3"
                ],
                "respuesta": "5/8",
                "explicacion": "Total de bolas = 5 + 3 = 8. P(Roja) = 5/8 = 0.625"
            },
            {
                "pregunta": "Si P(A) = 0.4 y P(B) = 0.5, y A y B son mutuamente excluyentes, ¿cuál es P(A ∪ B)?",
                "opciones": [
                    "0.9",
                    "0.2",
                    "0.7",
                    "1.0"
                ],
                "respuesta": "0.9",
                "explicacion": "Para eventos mutuamente excluyentes: P(A ∪ B) = P(A) + P(B) = 0.4 + 0.5 = 0.9"
            },
            {
                "pregunta": "Si P(A) = 0.6, P(B) = 0.5 y P(A ∩ B) = 0.3, ¿cuál es P(A ∪ B)?",
                "opciones": [
                    "1.1",
                    "0.8",
                    "0.5",
                    "0.3"
                ],
                "respuesta": "0.8",
                "explicacion": "Usando la fórmula: P(A ∪ B) = P(A) + P(B) - P(A ∩ B) = 0.6 + 0.5 - 0.3 = 0.8"
            },
            {
                "pregunta": "Al lanzar dos dados, ¿cuál es la probabilidad de que la suma sea 7?",
                "opciones": [
                    "1/6",
                    "1/36",
                    "1/12",
                    "1/18"
                ],
                "respuesta": "1/6",
                "explicacion": "Las combinaciones que suman 7 son: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) = 6 combinaciones. P(Suma=7) = 6/36 = 1/6"
            },
            {
                "pregunta": "En una fábrica, el 5% de las piezas son defectuosas. Si seleccionamos una pieza al azar, ¿cuál es la probabilidad de que NO sea defectuosa?",
                "opciones": [
                    "0.05",
                    "0.95",
                    "0.50",
                    "1.00"
                ],
                "respuesta": "0.95",
                "explicacion": "P(No defectuosa) = 1 - P(Defectuosa) = 1 - 0.05 = 0.95"
            }
        ]
        
        for i, ejercicio in enumerate(ejercicios_intermedios):
            with st.expander(f"**Ejercicio {i+1}:** {ejercicio['pregunta']}"):
                respuesta_usuario = st.radio(
                    "Selecciona tu respuesta:",
                    ejercicio['opciones'],
                    key=f"intermedio_{i}"
                )
                
                if st.button("Verificar", key=f"btn_intermedio_{i}"):
                    if respuesta_usuario == ejercicio['respuesta']:
                        st.success("✅ ¡Correcto!")
                        st.info(f"**Explicación:** {ejercicio['explicacion']}")
                    else:
                        st.error(f"❌ Incorrecto. La respuesta correcta es: **{ejercicio['respuesta']}**")
                        st.info(f"**Explicación:** {ejercicio['explicacion']}")
    
    else:  # Nivel Avanzado
        st.subheader("🔴 Nivel Avanzado: Problemas Complejos")
        
        ejercicios_avanzados = [
            {
                "pregunta": "Dos eventos A y B cumplen: P(A) = 0.5, P(B) = 0.4, P(A ∪ B) = 0.7. ¿Son A y B independientes?",
                "opciones": [
                    "Sí, son independientes",
                    "No, son dependientes",
                    "No hay suficiente información",
                    "Son mutuamente excluyentes"
                ],
                "respuesta": "Sí, son independientes",
                "explicacion": "Primero calculamos P(A ∩ B) = P(A) + P(B) - P(A ∪ B) = 0.5 + 0.4 - 0.7 = 0.2. Para independencia: P(A) × P(B) = 0.5 × 0.4 = 0.2 = P(A ∩ B). Por lo tanto, SÍ son independientes."
            },
            {
                "pregunta": "Si P(A ∪ B ∪ C) = 1 y los tres eventos son mutuamente excluyentes con P(A) = 0.3 y P(B) = 0.5, ¿cuál es P(C)?",
                "opciones": [
                    "0.2",
                    "0.8",
                    "0.3",
                    "No se puede determinar"
                ],
                "respuesta": "0.2",
                "explicacion": "Para eventos mutuamente excluyentes: P(A ∪ B ∪ C) = P(A) + P(B) + P(C). Entonces: 1 = 0.3 + 0.5 + P(C), por lo tanto P(C) = 0.2"
            },
            {
                "pregunta": "En un sistema con dos componentes independientes con confiabilidades 0.9 y 0.8, ¿cuál es la probabilidad de que AMBOS funcionen?",
                "opciones": [
                    "0.72",
                    "0.90",
                    "0.80",
                    "0.98"
                ],
                "respuesta": "0.72",
                "explicacion": "Para eventos independientes: P(Ambos funcionen) = P(A) × P(B) = 0.9 × 0.8 = 0.72"
            },
            {
                "pregunta": "Si P(A | B) significa 'probabilidad de A dado B', y sabemos que P(A ∩ B) = 0.15 y P(B) = 0.3, ¿cuál es el concepto correcto?",
                "opciones": [
                    "P(A | B) = P(A ∩ B) / P(B) = 0.5",
                    "P(A | B) = P(B) / P(A ∩ B) = 2",
                    "P(A | B) = P(A ∩ B) × P(B) = 0.045",
                    "No se puede calcular"
                ],
                "respuesta": "P(A | B) = P(A ∩ B) / P(B) = 0.5",
                "explicacion": "La probabilidad condicional se define como: P(A | B) = P(A ∩ B) / P(B) = 0.15 / 0.3 = 0.5"
            },
            {
                "pregunta": "Si un sistema falla cuando AL MENOS UNO de dos componentes independientes falla, y cada componente tiene confiabilidad 0.95, ¿cuál es la confiabilidad del sistema?",
                "opciones": [
                    "0.9025",
                    "0.95",
                    "0.9975",
                    "1.90"
                ],
                "respuesta": "0.9025",
                "explicacion": "El sistema funciona solo si AMBOS componentes funcionan. P(Sistema funciona) = 0.95 × 0.95 = 0.9025"
            }
        ]
        
        for i, ejercicio in enumerate(ejercicios_avanzados):
            with st.expander(f"**Ejercicio {i+1}:** {ejercicio['pregunta']}"):
                respuesta_usuario = st.radio(
                    "Selecciona tu respuesta:",
                    ejercicio['opciones'],
                    key=f"avanzado_{i}"
                )
                
                if st.button("Verificar", key=f"btn_avanzado_{i}"):
                    if respuesta_usuario == ejercicio['respuesta']:
                        st.success("✅ ¡Excelente! Respuesta correcta.")
                        st.info(f"**Explicación:** {ejercicio['explicacion']}")
                    else:
                        st.error(f"❌ Incorrecto. La respuesta correcta es: **{ejercicio['respuesta']}**")
                        st.info(f"**Explicación:** {ejercicio['explicacion']}")

elif page == "10. ❓ Cuestionario Final":
    st.title("❓ Cuestionario Final")
    st.markdown("### Evaluación completa de todos los conceptos")
    
    st.markdown("---")
    
    # Inicializar estado de sesión
    if 'quiz_probabilidad' not in st.session_state:
        st.session_state.quiz_probabilidad = {
            'respuestas': {},
            'finalizado': False,
            'indice': 0
        }
    
    # Preguntas del cuestionario
    preguntas_quiz = [
        {
            "pregunta": "¿Cuál de los siguientes NO es un axioma de Kolmogorov?",
            "opciones": [
                "P(A) ≥ 0 para todo evento A",
                "P(S) = 1",
                "P(A ∪ B) = P(A) + P(B) si A ∩ B = ∅",
                "P(A ∩ B) = P(A) × P(B) siempre"
            ],
            "respuesta": "P(A ∩ B) = P(A) × P(B) siempre",
            "explicacion": "Esta fórmula solo es válida para eventos INDEPENDIENTES, no es un axioma general."
        },
        {
            "pregunta": "En un diagrama de Venn, la región sombreada representa A ∪ B. ¿Qué significa esto?",
            "opciones": [
                "Solo los elementos en A",
                "Solo los elementos en B",
                "Los elementos que están en A o en B (o en ambos)",
                "Los elementos que están en A y en B simultáneamente"
            ],
            "respuesta": "Los elementos que están en A o en B (o en ambos)",
            "explicacion": "La unión (∪) incluye todos los elementos que pertenecen a A, a B, o a ambos."
        },
        {
            "pregunta": "Si P(A) = 0.4, P(B) = 0.6 y P(A ∩ B) = 0.2, ¿cuál es P(A ∪ B)?",
            "opciones": [
                "1.0",
                "0.8",
                "0.2",
                "0.4"
            ],
            "respuesta": "0.8",
            "explicacion": "P(A ∪ B) = P(A) + P(B) - P(A ∩ B) = 0.4 + 0.6 - 0.2 = 0.8"
        },
        {
            "pregunta": "¿Qué es un experimento aleatorio?",
            "opciones": [
                "Un experimento que siempre da el mismo resultado",
                "Un experimento cuyo resultado no se puede predecir con certeza",
                "Un experimento que no se puede repetir",
                "Un experimento con resultado imposible"
            ],
            "respuesta": "Un experimento cuyo resultado no se puede predecir con certeza",
            "explicacion": "Un experimento aleatorio se puede repetir bajo las mismas condiciones, pero su resultado no es predecible con certeza."
        },
        {
            "pregunta": "Si lanzamos dos monedas, ¿cuál es el tamaño del espacio muestral?",
            "opciones": [
                "2",
                "3",
                "4",
                "8"
            ],
            "respuesta": "4",
            "explicacion": "S = {(C,C), (C,S), (S,C), (S,S)}, por lo tanto |S| = 4"
        },
        {
            "pregunta": "La Ley de los Grandes Números establece que:",
            "opciones": [
                "La probabilidad siempre es grande",
                "Con muchos experimentos, la frecuencia relativa converge a la probabilidad teórica",
                "Los números grandes tienen mayor probabilidad",
                "La probabilidad aumenta con el tiempo"
            ],
            "respuesta": "Con muchos experimentos, la frecuencia relativa converge a la probabilidad teórica",
            "explicacion": "Esta ley es fundamental y demuestra que la probabilidad teórica predice el comportamiento a largo plazo."
        },
        {
            "pregunta": "Si P(A') = 0.35, ¿cuál es P(A)?",
            "opciones": [
                "0.35",
                "0.65",
                "1.35",
                "0.00"
            ],
            "respuesta": "0.65",
            "explicacion": "P(A) = 1 - P(A') = 1 - 0.35 = 0.65"
        },
        {
            "pregunta": "Dos eventos son mutuamente excluyentes si:",
            "opciones": [
                "P(A) = P(B)",
                "P(A ∩ B) = 0",
                "P(A ∪ B) = 1",
                "P(A) × P(B) = 0"
            ],
            "respuesta": "P(A ∩ B) = 0",
            "explicacion": "Eventos mutuamente excluyentes no pueden ocurrir simultáneamente, por lo tanto su intersección es vacía."
        },
        {
            "pregunta": "En una baraja estándar de 52 cartas, ¿cuál es P(sacar un Rey O una carta de corazones)?",
            "opciones": [
                "17/52",
                "16/52",
                "13/52",
                "4/52"
            ],
            "respuesta": "16/52",
            "explicacion": "P(Rey ∪ Corazón) = P(Rey) + P(Corazón) - P(Rey ∩ Corazón) = 4/52 + 13/52 - 1/52 = 16/52"
        },
        {
            "pregunta": "¿Cuál propiedad se deriva directamente de los axiomas de Kolmogorov?",
            "opciones": [
                "P(A) siempre es mayor que 0.5",
                "P(∅) = 0",
                "P(A) = P(B) siempre",
                "Todos los eventos son independientes"
            ],
            "respuesta": "P(∅) = 0",
            "explicacion": "Esta propiedad se puede demostrar usando los axiomas 2 y 3."
        }
    ]
    
    if not st.session_state.quiz_probabilidad['finalizado']:
        # Mostrar progreso
        progreso = len(st.session_state.quiz_probabilidad['respuestas']) / len(preguntas_quiz)
        st.progress(progreso)
        st.markdown(f"**Progreso:** {len(st.session_state.quiz_probabilidad['respuestas'])}/{len(preguntas_quiz)} preguntas respondidas")
        
        st.markdown("---")
        
        # Mostrar preguntas
        for i, pregunta in enumerate(preguntas_quiz):
            with st.expander(f"**Pregunta {i+1}:** {pregunta['pregunta']}", expanded=(i not in st.session_state.quiz_probabilidad['respuestas'])):
                respuesta = st.radio(
                    "Selecciona tu respuesta:",
                    pregunta['opciones'],
                    key=f"quiz_final_{i}"
                )
                
                if st.button("Confirmar respuesta", key=f"btn_quiz_{i}"):
                    st.session_state.quiz_probabilidad['respuestas'][i] = respuesta
                    st.success("✅ Respuesta registrada")
                    st.rerun()
        
        st.markdown("---")
        
        # Botón para finalizar
        if len(st.session_state.quiz_probabilidad['respuestas']) == len(preguntas_quiz):
            if st.button("🏁 Finalizar y Ver Resultados", type="primary"):
                st.session_state.quiz_probabilidad['finalizado'] = True
                st.rerun()
        else:
            st.warning(f"⚠️ Debes responder todas las preguntas antes de finalizar. Faltan {len(preguntas_quiz) - len(st.session_state.quiz_probabilidad['respuestas'])} preguntas.")
    
    else:
        # Mostrar resultados
        st.subheader("📊 Resultados del Cuestionario")
        
        correctas = 0
        incorrectas = 0
        
        for i, pregunta in enumerate(preguntas_quiz):
            respuesta_usuario = st.session_state.quiz_probabilidad['respuestas'].get(i, "")
            es_correcta = respuesta_usuario == pregunta['respuesta']
            
            if es_correcta:
                correctas += 1
                icono = "✅"
                color = "success"
            else:
                incorrectas += 1
                icono = "❌"
                color = "error"
            
            with st.expander(f"{icono} Pregunta {i+1}: {pregunta['pregunta']}"):
                st.markdown(f"**Tu respuesta:** {respuesta_usuario}")
                st.markdown(f"**Respuesta correcta:** {pregunta['respuesta']}")
                
                if es_correcta:
                    st.success("✅ ¡Correcto!")
                else:
                    st.error("❌ Incorrecto")
                
                st.info(f"**Explicación:** {pregunta['explicacion']}")
        
        # Estadísticas finales
        st.markdown("---")
        st.markdown("### 📈 Estadísticas Finales")
        
        porcentaje = (correctas / len(preguntas_quiz)) * 100
        
        col_r1, col_r2, col_r3 = st.columns(3)
        
        with col_r1:
            st.metric("Respuestas Correctas", f"{correctas}/{len(preguntas_quiz)}")
        with col_r2:
            st.metric("Respuestas Incorrectas", f"{incorrectas}/{len(preguntas_quiz)}")
        with col_r3:
            st.metric("Calificación", f"{porcentaje:.1f}%")
        
        # Visualización
        fig_resultados = go.Figure(data=[go.Pie(
            labels=['Correctas', 'Incorrectas'],
            values=[correctas, incorrectas],
            marker=dict(colors=['#2ECC71', '#E74C3C']),
            hole=0.4,
            textinfo='label+value+percent'
        )])
        
        fig_resultados.update_layout(
            title=f"Resultado: {correctas}/{len(preguntas_quiz)} correctas ({porcentaje:.1f}%)",
            height=400
        )
        
        st.plotly_chart(fig_resultados, use_container_width=True)
        
        # Mensaje según el desempeño
        if porcentaje >= 90:
            st.success("""
            ### 🏆 ¡Excelente trabajo!
            
            Has demostrado un dominio excepcional de los conceptos de probabilidad.
            ¡Felicitaciones! 🎉
            """)
        elif porcentaje >= 70:
            st.success("""
            ### ✅ ¡Buen trabajo!
            
            Tienes un buen entendimiento de los conceptos fundamentales.
            Repasa los temas donde tuviste errores para mejorar aún más.
            """)
        elif porcentaje >= 50:
            st.warning("""
            ### 🟡 Aprobado, pero hay margen de mejora
            
            Has comprendido los conceptos básicos, pero te recomendamos
            repasar los temas más complejos.
            """)
        else:
            st.error("""
            ### 📚 Necesitas repasar
            
            Te recomendamos revisar nuevamente las secciones del curso,
            especialmente los conceptos fundamentales y los axiomas.
            """)
        
        # Botón para reintentar
        if st.button("🔄 Reiniciar Cuestionario"):
            st.session_state.quiz_probabilidad = {
                'respuestas': {},
                'finalizado': False,
                'indice': 0
            }
            st.rerun()

elif page == "11. 📖 Resumen y Fórmulas":
    st.title("📖 Resumen y Fórmulas")
    st.markdown("### Guía de referencia rápida")
    
    st.markdown("---")
    
    # Tabla de contenido
    st.markdown("""
    ## 📑 Contenido:
    
    1. [Conceptos Fundamentales](#conceptos-fundamentales)
    2. [Axiomas de Kolmogorov](#axiomas-de-kolmogorov)
    3. [Fórmulas Principales](#formulas-principales)
    4. [Operaciones entre Eventos](#operaciones-entre-eventos)
    5. [Propiedades Importantes](#propiedades-importantes)
    """)
    
    st.markdown("---")
    
    # 1. Conceptos Fundamentales
    st.header("1️⃣ Conceptos Fundamentales")
    
    conceptos_df = pd.DataFrame({
        'Concepto': [
            'Experimento Aleatorio',
            'Espacio Muestral (S)',
            'Evento (A)',
            'Probabilidad P(A)',
            'Evento Imposible',
            'Evento Seguro',
            'Complemento (A\')',
            'Eventos Mutuamente Excluyentes'
        ],
        'Definición': [
            'Proceso cuyo resultado no se puede predecir con certeza',
            'Conjunto de todos los resultados posibles',
            'Subconjunto del espacio muestral',
            'Medida numérica de la certeza de que ocurra A',
            'Evento que nunca ocurre (∅), P(∅) = 0',
            'Evento que siempre ocurre (S), P(S) = 1',
            'Evento que contiene todos los resultados que NO están en A',
            'Eventos que no pueden ocurrir simultáneamente (A ∩ B = ∅)'
        ],
        'Notación': [
            '-',
            'S o Ω',
            'A, B, C, ...',
            'P(A), 0 ≤ P(A) ≤ 1',
            '∅',
            'S',
            'A\', Aᶜ, o Ā',
            'A ∩ B = ∅'
        ]
    })
    
    st.dataframe(conceptos_df, hide_index=True, use_container_width=True)
    
    st.markdown("---")
    
    # 2. Axiomas de Kolmogorov
    st.header("2️⃣ Axiomas de Kolmogorov")
    
    col_ax1, col_ax2, col_ax3 = st.columns(3)
    
    with col_ax1:
        st.markdown("""
        ### Axioma 1
        **No Negatividad**
        """)
        st.latex(r"P(A) \geq 0")
        st.info("La probabilidad nunca es negativa")
    
    with col_ax2:
        st.markdown("""
        ### Axioma 2
        **Certeza**
        """)
        st.latex(r"P(S) = 1")
        st.info("La probabilidad del espacio muestral es 1")
    
    with col_ax3:
        st.markdown("""
        ### Axioma 3
        **Aditividad**
        """)
        st.latex(r"A \cap B = \emptyset \Rightarrow P(A \cup B) = P(A) + P(B)")
        st.info("Para eventos mutuamente excluyentes")
    
    st.markdown("---")
    
    # 3. Fórmulas Principales
    st.header("3️⃣ Fórmulas Principales")
    
    formulas_df = pd.DataFrame({
        'Fórmula': [
            'Probabilidad Clásica',
            'Complemento',
            'Unión (General)',
            'Intersección (Independientes)',
            'Diferencia',
            'Probabilidad Condicional'
        ],
        'Expresión': [
            'P(A) = |A| / |S|',
            'P(A\') = 1 - P(A)',
            'P(A ∪ B) = P(A) + P(B) - P(A ∩ B)',
            'P(A ∩ B) = P(A) × P(B)',
            'P(A - B) = P(A) - P(A ∩ B)',
            'P(A | B) = P(A ∩ B) / P(B)'
        ],
        'Condiciones': [
            'Resultados equiprobables',
            'Siempre aplicable',
            'Siempre aplicable',
            'Solo para eventos independientes',
            'Siempre aplicable',
            'P(B) > 0'
        ]
    })
    
    st.dataframe(formulas_df, hide_index=True, use_container_width=True)
    
    st.markdown("---")
    
    # 4. Operaciones entre Eventos
    st.header("4️⃣ Operaciones entre Eventos")
    
    tab_ops1, tab_ops2, tab_ops3, tab_ops4 = st.tabs(["Unión", "Intersección", "Complemento", "Diferencia"])
    
    with tab_ops1:
        st.markdown("### Unión (A ∪ B)")
        st.latex(r"A \cup B = \{x : x \in A \text{ o } x \in B\}")
        st.markdown("**Significado:** Ocurre A **O** B (o ambos)")
        st.latex(r"P(A \cup B) = P(A) + P(B) - P(A \cap B)")
        st.info("Si son mutuamente excluyentes: $P(A \\cup B) = P(A) + P(B)$")
    
    with tab_ops2:
        st.markdown("### Intersección (A ∩ B)")
        st.latex(r"A \cap B = \{x : x \in A \text{ y } x \in B\}")
        st.markdown("**Significado:** Ocurre A **Y** B simultáneamente")
        st.latex(r"P(A \cap B) = P(A) \times P(B) \text{ (si son independientes)}")
        st.info("Si son dependientes, usar: $P(A \\cap B) = P(A) \\times P(B|A)$")
    
    with tab_ops3:
        st.markdown("### Complemento (A')")
        st.latex(r"A' = \{x : x \in S \text{ y } x \notin A\}")
        st.markdown("**Significado:** Todo lo que **NO** es A")
        st.latex(r"P(A') = 1 - P(A)")
        st.info("Propiedades: $A \\cup A' = S$ y $A \\cap A' = \\emptyset$")
    
    with tab_ops4:
        st.markdown("### Diferencia (A - B)")
        st.latex(r"A - B = \{x : x \in A \text{ y } x \notin B\}")
        st.markdown("**Significado:** Elementos en A pero **NO** en B")
        st.latex(r"P(A - B) = P(A) - P(A \cap B)")
        st.warning("Nota: $A - B \\neq B - A$ (no es conmutativa)")
    
    st.markdown("---")
    
    # 5. Propiedades Importantes
    st.header("5️⃣ Propiedades Importantes")
    
    propiedades_lista = [
        {
            "nombre": "Propiedad del Evento Imposible",
            "formula": r"P(\emptyset) = 0"
        },
        {
            "nombre": "Acotamiento de Probabilidades",
            "formula": r"0 \leq P(A) \leq 1"
        },
        {
            "nombre": "Suma de Probabilidades",
            "formula": r"P(A) + P(A') = 1"
        },
        {
            "nombre": "Monotonía",
            "formula": r"A \subseteq B \Rightarrow P(A) \leq P(B)"
        },
        {
            "nombre": "Primera Ley de De Morgan",
            "formula": r"(A \cup B)' = A' \cap B'"
        },
        {
            "nombre": "Segunda Ley de De Morgan",
            "formula": r"(A \cap B)' = A' \cup B'"
        },
        {
            "nombre": "Propiedad Distributiva (1)",
            "formula": r"A \cap (B \cup C) = (A \cap B) \cup (A \cap C)"
        },
        {
            "nombre": "Propiedad Distributiva (2)",
            "formula": r"A \cup (B \cap C) = (A \cup B) \cap (A \cup C)"
        }
    ]
    
    for prop in propiedades_lista:
        col_p1, col_p2 = st.columns([1, 2])
        with col_p1:
            st.markdown(f"**{prop['nombre']}:**")
        with col_p2:
            st.latex(prop['formula'])
    
    st.markdown("---")
    
    # 6. Casos Especiales
    st.header("6️⃣ Casos Especiales")
    
    col_esp1, col_esp2 = st.columns(2)
    
    with col_esp1:
        st.markdown("### Eventos Independientes")
        st.latex(r"P(A \cap B) = P(A) \times P(B)")
        st.latex(r"P(A | B) = P(A)")
        st.markdown("""
        **Ejemplos:**
        - Lanzar dos monedas
        - Resultado de dos dados
        - Eventos en experimentos separados
        """)
    
    with col_esp2:
        st.markdown("### Eventos Mutuamente Excluyentes")
        st.latex(r"A \cap B = \emptyset")
        st.latex(r"P(A \cup B) = P(A) + P(B)")
        st.markdown("""
        **Ejemplos:**
        - Obtener cara O sello (una moneda)
        - Número par O impar (un dado)
        - Ganar O perder (sin empate)
        """)
    
    st.markdown("---")
    
    # 7. Tabla de Fórmulas Rápidas
    st.header("7️⃣ Tabla de Referencia Rápida")
    
    formulas_rapidas = pd.DataFrame({
        'Operación': [
            'P(A ∪ B)',
            'P(A ∩ B) independientes',
            'P(A\')',
            'P(A - B)',
            'P(A ∪ B ∪ C)',
            'P(A | B)',
            'Regla del Producto',
            'Ley de Probabilidad Total'
        ],
        'Fórmula': [
            'P(A) + P(B) - P(A ∩ B)',
            'P(A) × P(B)',
            '1 - P(A)',
            'P(A) - P(A ∩ B)',
            'P(A) + P(B) + P(C) - P(A∩B) - P(A∩C) - P(B∩C) + P(A∩B∩C)',
            'P(A ∩ B) / P(B)',
            'P(A ∩ B) = P(A) × P(B|A) = P(B) × P(A|B)',
            'P(A) = Σ P(A|Bᵢ) × P(Bᵢ)'
        ]
    })
    
    st.dataframe(formulas_rapidas, hide_index=True, use_container_width=True)
    
    st.markdown("---")
    
    # 8. Ejemplos Numéricos
    st.header("8️⃣ Ejemplos Numéricos Resueltos")
    
    ejemplo_select = st.selectbox(
        "Selecciona un ejemplo:",
        [
            "Ejemplo 1: Unión de eventos",
            "Ejemplo 2: Complemento",
            "Ejemplo 3: Eventos independientes",
            "Ejemplo 4: Probabilidad condicional"
        ]
    )
    
    if ejemplo_select == "Ejemplo 1: Unión de eventos":
        st.markdown("""
        ### Ejemplo 1: Unión de Eventos
        
        **Problema:** 
        En una clase de 100 estudiantes:
        - 60 estudian Matemáticas (evento A)
        - 50 estudian Física (evento B)
        - 30 estudian ambas materias
        
        ¿Cuál es la probabilidad de que un estudiante aleatorio estudie Matemáticas O Física?
        
        **Solución:**
        """)
        
        st.latex(r"P(A) = \frac{60}{100} = 0.60")
        st.latex(r"P(B) = \frac{50}{100} = 0.50")
        st.latex(r"P(A \cap B) = \frac{30}{100} = 0.30")
        st.latex(r"P(A \cup B) = P(A) + P(B) - P(A \cap B)")
        st.latex(r"P(A \cup B) = 0.60 + 0.50 - 0.30 = 0.80")
        
        st.success("**Respuesta:** La probabilidad es 0.80 o 80%")
    
    elif ejemplo_select == "Ejemplo 2: Complemento":
        st.markdown("""
        ### Ejemplo 2: Complemento
        
        **Problema:** 
        La probabilidad de que llueva mañana es 0.35. 
        ¿Cuál es la probabilidad de que NO llueva?
        
        **Solución:**
        """)
        
        st.latex(r"P(\text{Lluvia}) = 0.35")
        st.latex(r"P(\text{No lluvia}) = 1 - P(\text{Lluvia})")
        st.latex(r"P(\text{No lluvia}) = 1 - 0.35 = 0.65")
        
        st.success("**Respuesta:** La probabilidad de que NO llueva es 0.65 o 65%")
    
    elif ejemplo_select == "Ejemplo 3: Eventos independientes":
        st.markdown("""
        ### Ejemplo 3: Eventos Independientes
        
        **Problema:** 
        Se lanzan dos dados independientes. 
        ¿Cuál es la probabilidad de obtener un 6 en el primer dado Y un número par en el segundo?
        
        **Solución:**
        """)
        
        st.latex(r"P(\text{6 en dado 1}) = \frac{1}{6}")
        st.latex(r"P(\text{Par en dado 2}) = \frac{3}{6} = \frac{1}{2}")
        st.markdown("Como los eventos son independientes:")
        st.latex(r"P(\text{6 en dado 1 Y Par en dado 2}) = \frac{1}{6} \times \frac{1}{2} = \frac{1}{12}")
        
        st.success("**Respuesta:** La probabilidad es 1/12 ≈ 0.0833 o 8.33%")
    
    else:  # Ejemplo 4
        st.markdown("""
        ### Ejemplo 4: Probabilidad Condicional
        
        **Problema:** 
        En una empresa, 70% de los empleados usan computadora (C) y 50% usan computadora Y tienen correo corporativo (E).
        
        Si un empleado usa computadora, ¿cuál es la probabilidad de que tenga correo corporativo?
        
        **Solución:**
        """)
        
        st.latex(r"P(C) = 0.70")
        st.latex(r"P(C \cap E) = 0.50")
        st.latex(r"P(E | C) = \frac{P(C \cap E)}{P(C)} = \frac{0.50}{0.70} = 0.714")
        
        st.success("**Respuesta:** La probabilidad es aproximadamente 0.714 o 71.4%")
    
    st.markdown("---")
    
    # 9. Consejos y Trucos
    st.header("9️⃣ Consejos y Trucos")
    
    st.info("""
    ### 💡 Consejos para Resolver Problemas de Probabilidad:
    
    1. **Identifica el espacio muestral (S)** primero
    2. **Define claramente el evento** que te interesa
    3. **Determina si los eventos son:**
       - Mutuamente excluyentes (A ∩ B = ∅)
       - Independientes (P(A∩B) = P(A)×P(B))
    4. **Usa diagramas de Venn** para visualizar relaciones
    5. **Verifica que las probabilidades sumen 1** cuando sea apropiado
    6. **El complemento es tu amigo:** A veces es más fácil calcular P(A') y luego usar P(A) = 1 - P(A')
    7. **Para "AL MENOS UNO":** Usa el complemento (ninguno)
    8. **Para "TODOS":** Usa multiplicación (si son independientes)
    """)
    
    st.warning("""
    ### ⚠️ Errores Comunes a Evitar:
    
    - ❌ Asumir que eventos son independientes sin verificar
    - ❌ Olvidar restar P(A ∩ B) en la fórmula de unión
    - ❌ Confundir P(A|B) con P(B|A)
    - ❌ No verificar que las probabilidades estén entre 0 y 1
    - ❌ Sumar probabilidades cuando los eventos NO son mutuamente excluyentes
    """)
    
    st.markdown("---")
    
    # 10. Recursos Adicionales
    st.header("🔟 Para Seguir Aprendiendo")
    
    st.markdown("""
    ### 📚 Temas Avanzados (para continuar tu aprendizaje):
    
    1. **Probabilidad Condicional y Teorema de Bayes**
       - P(A|B) y P(B|A)
       - Actualización de creencias con nueva información
    
    2. **Variables Aleatorias**
       - Discretas y continuas
       - Funciones de probabilidad y densidad
    
    3. **Distribuciones de Probabilidad**
       - Binomial, Poisson, Normal, Exponencial
    
    4. **Valor Esperado y Varianza**
       - Medidas de tendencia central y dispersión
    
    5. **Teorema del Límite Central**
       - Base de la inferencia estadística
    
    6. **Procesos Estocásticos**
       - Cadenas de Markov
       - Procesos de Poisson
    """)
    
    st.success("""
    ### 🎯 ¡Has completado el curso de Introducción a la Probabilidad!
    
    Ahora tienes las herramientas fundamentales para:
    - Entender experimentos aleatorios
    - Calcular probabilidades simples y compuestas
    - Visualizar eventos con diagramas de Venn
    - Aplicar los axiomas de Kolmogorov
    - Resolver problemas prácticos en diferentes áreas
    
    **¡Sigue practicando y explorando!** 🚀
    """)


# === FOOTER ===
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
📧 <strong>Contacto:</strong> carlosdl@uninorte.edu.co<br>
Desarrollado con 💙 para estudiantes de Uninorte 
</div>
""", unsafe_allow_html=True)







