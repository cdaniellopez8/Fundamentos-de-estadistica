import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from itertools import permutations, combinations, combinations_with_replacement, product
import math
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="Técnicas de Conteo - Probabilidad", page_icon="🎲")

# --- FUNCIONES AUXILIARES ---

def factorial(n):
    """Calcula el factorial de n"""
    if n <= 1:
        return 1
    return math.factorial(n)

def permutacion(n, r):
    """Calcula P(n,r) = n!/(n-r)!"""
    if r > n:
        return 0
    return factorial(n) // factorial(n - r)

def combinacion(n, r):
    """Calcula C(n,r) = n!/(r!(n-r)!)"""
    if r > n:
        return 0
    return factorial(n) // (factorial(r) * factorial(n - r))

def combinacion_repeticion(n, r):
    """Calcula C_r(n,r) = C(n+r-1, r)"""
    return combinacion(n + r - 1, r)

def con_reemplazo_con_orden(n, r):
    """Calcula n^r"""
    return n ** r

def generar_arbol_monedas(num_monedas):
    """Genera todas las combinaciones de lanzar monedas"""
    opciones = ['C', 'S']
    resultados = list(product(opciones, repeat=num_monedas))
    return resultados

def generar_arbol_dados(num_dados):
    """Genera todas las combinaciones de lanzar dados"""
    opciones = list(range(1, 7))
    resultados = list(product(opciones, repeat=num_dados))
    return resultados

def expandir_factorial(n):
    """Retorna la expansión de n! como string"""
    if n <= 1:
        return "1"
    return " × ".join([str(i) for i in range(n, 0, -1)])

# --- BANCO DE PROBLEMAS DEL MUNDO REAL ---
BANCO_PROBLEMAS = {
    "🧠 Psicología": [
        {
            "titulo": "Diseño Experimental",
            "contexto": "Estás diseñando un experimento con 3 grupos de tratamiento diferentes.",
            "pregunta": "¿De cuántas formas puedes asignar 3 pacientes a estos grupos si cada grupo debe tener exactamente 1 paciente?",
            "n": 3, "r": 3,
            "tecnica": "permutacion",
            "orden": True, "repeticion": False,
            "solucion": "P(3,3) = 3! = 6",
            "explicacion": "El orden importa porque cada grupo es diferente, y no hay repetición porque cada paciente va a un solo grupo."
        },
        {
            "titulo": "Batería de Tests",
            "contexto": "Tienes 8 tests psicológicos y debes seleccionar 3 para una evaluación.",
            "pregunta": "¿Cuántas baterías diferentes puedes formar si el orden de aplicación NO importa?",
            "n": 8, "r": 3,
            "tecnica": "combinacion",
            "orden": False, "repeticion": False,
            "solucion": "C(8,3) = 56",
            "explicacion": "El orden NO importa (solo nos interesa qué tests usamos, no en qué orden), y no hay repetición."
        },
        {
            "titulo": "Respuestas en Escala Likert",
            "contexto": "Un cuestionario tiene 5 preguntas con escala de 1 a 5 (totalmente en desacuerdo a totalmente de acuerdo).",
            "pregunta": "¿Cuántas combinaciones de respuestas diferentes son posibles?",
            "n": 5, "r": 5,
            "tecnica": "variacion_rep",
            "orden": True, "repeticion": True,
            "solucion": "5^5 = 3,125",
            "explicacion": "El orden importa (cada pregunta es diferente) y hay repetición (puedes responder '3' en varias preguntas)."
        }
    ],
    "💼 Admin. de Empresas": [
        {
            "titulo": "Comité Directivo",
            "contexto": "De 10 empleados destacados debes formar un comité de 4 personas.",
            "pregunta": "¿Cuántos comités diferentes puedes formar?",
            "n": 10, "r": 4,
            "tecnica": "combinacion",
            "orden": False, "repeticion": False,
            "solucion": "C(10,4) = 210",
            "explicacion": "El orden NO importa (todos los miembros del comité tienen el mismo rol), sin repetición."
        },
        {
            "titulo": "Asignación de Cargos",
            "contexto": "Tienes 8 candidatos y 3 cargos: Gerente, Subgerente y Coordinador.",
            "pregunta": "¿De cuántas formas puedes asignar estos cargos?",
            "n": 8, "r": 3,
            "tecnica": "permutacion",
            "orden": True, "repeticion": False,
            "solucion": "P(8,3) = 336",
            "explicacion": "El orden SÍ importa (cada cargo es diferente), sin repetición (una persona = un cargo)."
        },
        {
            "titulo": "Código de Empleado",
            "contexto": "Los códigos de empleado tienen 2 letras seguidas de 4 dígitos (ej: AB1234).",
            "pregunta": "¿Cuántos códigos únicos se pueden generar?",
            "n": None, "r": None,
            "tecnica": "multiplicativo",
            "orden": True, "repeticion": True,
            "solucion": "26×26×10×10×10×10 = 6,760,000",
            "explicacion": "Principio multiplicativo: 26 opciones para cada letra, 10 para cada dígito, con repetición."
        },
        {
            "titulo": "Selección de Productos",
            "contexto": "Una tienda debe elegir 3 productos de 7 categorías para una promoción, pueden elegir varios de la misma categoría.",
            "pregunta": "¿Cuántas selecciones son posibles?",
            "n": 7, "r": 3,
            "tecnica": "combinacion_rep",
            "orden": False, "repeticion": True,
            "solucion": "CR(7,3) = C(9,3) = 84",
            "explicacion": "El orden NO importa, pero SÍ hay repetición (puedes elegir varios productos de la misma categoría)."
        }
    ],
    "📊 Negocios Internacionales": [
        {
            "titulo": "Rutas Comerciales",
            "contexto": "Una empresa debe visitar 6 países en un viaje de negocios, visitando 3 de ellos.",
            "pregunta": "¿Cuántos itinerarios diferentes existen si el orden de visita importa?",
            "n": 6, "r": 3,
            "tecnica": "permutacion",
            "orden": True, "repeticion": False,
            "solucion": "P(6,3) = 120",
            "explicacion": "El orden SÍ importa (visitar México-Brasil-Chile es diferente a Chile-Brasil-México)."
        },
        {
            "titulo": "Portafolio de Inversión",
            "contexto": "Un inversionista quiere diversificar su portafolio seleccionando 4 sectores de 10 disponibles.",
            "pregunta": "¿Cuántas combinaciones de portafolio puede crear?",
            "n": 10, "r": 4,
            "tecnica": "combinacion",
            "orden": False, "repeticion": False,
            "solucion": "C(10,4) = 210",
            "explicacion": "El orden NO importa (tener tecnología y salud es igual a tener salud y tecnología)."
        },
        {
            "titulo": "Código de Producto Internacional",
            "contexto": "Los productos tienen un código de 6 dígitos.",
            "pregunta": "¿Cuántos códigos diferentes se pueden asignar?",
            "n": 10, "r": 6,
            "tecnica": "variacion_rep",
            "orden": True, "repeticion": True,
            "solucion": "10^6 = 1,000,000",
            "explicacion": "El orden importa (123456 ≠ 654321) y hay repetición (pueden repetirse dígitos)."
        }
    ],
    "💰 Economía": [
        {
            "titulo": "Canasta Básica",
            "contexto": "Un estudio económico debe seleccionar 5 productos de 12 categorías para monitorear la inflación.",
            "pregunta": "¿Cuántas canastas diferentes se pueden formar?",
            "n": 12, "r": 5,
            "tecnica": "combinacion",
            "orden": False, "repeticion": False,
            "solucion": "C(12,5) = 792",
            "explicacion": "El orden NO importa (solo nos interesa qué productos están en la canasta)."
        },
        {
            "titulo": "Políticas Fiscales",
            "contexto": "Un gobierno puede implementar 3 políticas fiscales en un orden específico (prioridad).",
            "pregunta": "Si hay 7 políticas disponibles, ¿cuántas estrategias ordenadas puede diseñar?",
            "n": 7, "r": 3,
            "tecnica": "permutacion",
            "orden": True, "repeticion": False,
            "solucion": "P(7,3) = 210",
            "explicacion": "El orden SÍ importa (implementar primero política fiscal vs monetaria da resultados diferentes)."
        },
        {
            "titulo": "Encuesta de Satisfacción",
            "contexto": "Una encuesta tiene 4 preguntas, cada una con 5 opciones de respuesta.",
            "pregunta": "¿Cuántos perfiles de respuesta diferentes son posibles?",
            "n": 5, "r": 4,
            "tecnica": "variacion_rep",
            "orden": True, "repeticion": True,
            "solucion": "5^4 = 625",
            "explicacion": "El orden importa (cada pregunta es diferente) y hay repetición."
        }
    ],
    "👶 Pedagogía Infantil": [
        {
            "titulo": "Grupos de Lectura",
            "contexto": "Tienes 12 niños y debes formar un grupo de 4 para lectura grupal.",
            "pregunta": "¿Cuántos grupos diferentes puedes formar?",
            "n": 12, "r": 4,
            "tecnica": "combinacion",
            "orden": False, "repeticion": False,
            "solucion": "C(12,4) = 495",
            "explicacion": "El orden NO importa (todos son compañeros de lectura por igual)."
        },
        {
            "titulo": "Orden de Presentación",
            "contexto": "6 niños van a presentar sus proyectos, solo hay tiempo para 3 presentaciones.",
            "pregunta": "¿De cuántas formas puedes organizar el orden de presentación?",
            "n": 6, "r": 3,
            "tecnica": "permutacion",
            "orden": True, "repeticion": False,
            "solucion": "P(6,3) = 120",
            "explicacion": "El orden SÍ importa (presentar primero vs último hace diferencia)."
        },
        {
            "titulo": "Combinación de Colores",
            "contexto": "En una actividad de arte, los niños pueden escoger 3 colores de 8 disponibles (pueden repetir).",
            "pregunta": "¿Cuántas selecciones de colores son posibles si el orden NO importa?",
            "n": 8, "r": 3,
            "tecnica": "combinacion_rep",
            "orden": False, "repeticion": True,
            "solucion": "CR(8,3) = C(10,3) = 120",
            "explicacion": "El orden NO importa, pero SÍ pueden repetir colores (rojo-rojo-azul es válido)."
        },
        {
            "titulo": "Juego de Colores Secuencial",
            "contexto": "Un juego educativo pide a los niños tocar 4 colores en secuencia, hay 6 colores disponibles y pueden repetirse.",
            "pregunta": "¿Cuántas secuencias diferentes son posibles?",
            "n": 6, "r": 4,
            "tecnica": "variacion_rep",
            "orden": True, "repeticion": True,
            "solucion": "6^4 = 1,296",
            "explicacion": "El orden SÍ importa (es una secuencia) y hay repetición."
        }
    ],
    "🏥 Medicina": [
        {
            "titulo": "Ensayo Clínico",
            "contexto": "De 20 pacientes voluntarios debes seleccionar 5 para un ensayo clínico.",
            "pregunta": "¿Cuántos grupos de estudio diferentes puedes formar?",
            "n": 20, "r": 5,
            "tecnica": "combinacion",
            "orden": False, "repeticion": False,
            "solucion": "C(20,5) = 15,504",
            "explicacion": "El orden NO importa (todos los pacientes tienen el mismo rol en el estudio)."
        },
        {
            "titulo": "Rotación Médica",
            "contexto": "Un estudiante de medicina debe rotar por 3 especialidades en un orden específico, hay 8 especialidades disponibles.",
            "pregunta": "¿Cuántos planes de rotación diferentes existen?",
            "n": 8, "r": 3,
            "tecnica": "permutacion",
            "orden": True, "repeticion": False,
            "solucion": "P(8,3) = 336",
            "explicacion": "El orden SÍ importa (rotar primero por cirugía vs pediatría cambia la experiencia)."
        },
        {
            "titulo": "Tratamiento Combinado",
            "contexto": "Un médico puede recetar 2 medicamentos de 6 disponibles (no importa el orden, son complementarios).",
            "pregunta": "¿Cuántas combinaciones de tratamiento puede prescribir?",
            "n": 6, "r": 2,
            "tecnica": "combinacion",
            "orden": False, "repeticion": False,
            "solucion": "C(6,2) = 15",
            "explicacion": "El orden NO importa (medicamento A + B = B + A), sin repetición."
        },
        {
            "titulo": "Historia Clínica Digital",
            "contexto": "Los códigos de historia clínica tienen 3 letras seguidas de 5 dígitos.",
            "pregunta": "¿Cuántas historias clínicas únicas se pueden generar?",
            "n": None, "r": None,
            "tecnica": "multiplicativo",
            "orden": True, "repeticion": True,
            "solucion": "26^3 × 10^5 = 1,757,600,000",
            "explicacion": "Principio multiplicativo con repetición permitida."
        }
    ],
    "🎵 Música": [
        {
            "titulo": "Escalas Musicales",
            "contexto": "Quieres crear una melodía de 4 notas usando las 7 notas naturales (Do, Re, Mi, Fa, Sol, La, Si), pueden repetirse.",
            "pregunta": "¿Cuántas secuencias diferentes puedes crear?",
            "n": 7, "r": 4,
            "tecnica": "variacion_rep",
            "orden": True, "repeticion": True,
            "solucion": "7^4 = 2,401",
            "explicacion": "El orden SÍ importa (Do-Re-Mi ≠ Mi-Re-Do) y hay repetición (Do-Do-Re-Mi es válido)."
        },
        {
            "titulo": "Repertorio de Concierto",
            "contexto": "De 10 piezas musicales debes seleccionar 5 para un concierto, el orden de interpretación importa.",
            "pregunta": "¿Cuántos repertorios ordenados diferentes puedes crear?",
            "n": 10, "r": 5,
            "tecnica": "permutacion",
            "orden": True, "repeticion": False,
            "solucion": "P(10,5) = 30,240",
            "explicacion": "El orden SÍ importa (comenzar con una pieza alegre vs triste cambia la experiencia)."
        },
        {
            "titulo": "Ensamble Musical",
            "contexto": "Debes formar un cuarteto de 4 músicos de un grupo de 9.",
            "pregunta": "¿Cuántos cuartetos diferentes puedes formar?",
            "n": 9, "r": 4,
            "tecnica": "combinacion",
            "orden": False, "repeticion": False,
            "solucion": "C(9,4) = 126",
            "explicacion": "El orden NO importa (todos tocan al mismo tiempo, sin jerarquía)."
        },
        {
            "titulo": "Acordes Musicales",
            "contexto": "Quieres formar un acorde de 3 notas de las 12 notas cromáticas, pueden repetirse para inversiones.",
            "pregunta": "¿Cuántas combinaciones son posibles si el orden NO importa?",
            "n": 12, "r": 3,
            "tecnica": "combinacion_rep",
            "orden": False, "repeticion": True,
            "solucion": "CR(12,3) = C(14,3) = 364",
            "explicacion": "El orden NO importa (Do-Mi-Sol = Sol-Mi-Do), pero SÍ hay repetición (Do-Do-Mi es válido)."
        }
    ]
}

# --- BARRA LATERAL ---
st.sidebar.title("🎲 Técnicas de Conteo")
st.sidebar.markdown("**Introducción a Probabilidad**")
st.sidebar.markdown("---")

page = st.sidebar.radio("📚 Navegar a:", [
    "1. 🏠 Inicio",
    "2. 🌳 Diagramas de Árbol",
    "3. 📊 Principio Multiplicativo",
    "4. 🧭 ¿Qué técnica usar?",
    "5. 🔢 Las 4 Técnicas",
    "6. 🎯 Problemas del Mundo Real",
    "7. 🎲 Práctica Interactiva",
    "8. 🧮 Calculadora Universal",
    "9. ❓ Cuestionario Final",
    "10. 📚 Tabla de Referencia"
], index=0)

# --- PÁGINA 1: INICIO ---

if page == "1. 🏠 Inicio":
    st.title("🎲 Técnicas de Conteo")
    st.markdown("### *Introducción a la Probabilidad*")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 🤔 ¿Para qué necesitamos saber contar?
        
        Para hablar de **probabilidad**, necesitamos saber:
        
        ### 📌 **¿Cuántas formas existen de que pase algo?**
        
        Sin saber contar correctamente los resultados posibles, no podemos calcular probabilidades.
        """)
        
        st.info("""
        **💡 Probabilidad Básica:**
        
        $$P(\\text{Evento}) = \\frac{\\text{Casos favorables}}{\\text{Casos totales posibles}}$$
        
        Para calcular esto, **¡necesitamos contar ambos!**
        """)
    
    with col2:
        st.markdown("### 🎯 Podemos calcular:")
        st.success("""
        ✅ Posibles resultados del **Baloto**
        
        ✅ Resultados de un **experimento**
        
        ✅ Cuántos **grupos** podemos armar
        
        ✅ Formas de responder un **test**
        
        ✅ Combinaciones de **ropa**
        
        ✅ **Contraseñas** posibles
        
        ✅ **Placas** de vehículos
        
        ✅ **Equipos de trabajo**
        
        ✅ **Tratamientos médicos**
        """)
    
    st.markdown("---")
    
    st.markdown("## 🛠️ ¿Cómo se puede contar?")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### 🌳 Diagramas")
        st.markdown("""
        - **Diagrama de Árbol**
        - Método visual
        - Funciona bien para casos simples
        - Se vuelve complejo rápidamente
        """)
    
    with col_b:
        st.markdown("### 🧮 Ecuaciones (Fórmulas)")
        st.markdown("""
        - **Principio Multiplicativo**
        - **Permutaciones** ($P$)
        - **Combinaciones** ($C$)
        - Método eficiente para casos complejos
        """)
    
    st.markdown("---")
    
    st.markdown("## 🚀 ¡Comencemos!")
    st.markdown("Usa el menú lateral para navegar por las diferentes secciones.")

# --- PÁGINA 2: DIAGRAMAS DE ÁRBOL ---

elif page == "2. 🌳 Diagramas de Árbol":
    st.title("🌳 Visualizador de Diagramas de Árbol")
    st.markdown("Método visual para contar resultados posibles")
    st.markdown("---")
    
    experimento = st.selectbox("🎯 Selecciona un experimento:", [
        "📀 Lanzar Monedas",
        "🎲 Lanzar Dados"
    ])
    
    if "Monedas" in experimento:
        num_items = st.slider("Número de monedas:", 1, 4, 2)
        
        st.markdown(f"### Lanzando {num_items} moneda(s)")
        st.markdown("""
        **Opciones por moneda:** Cara (C) o Sello (S)
        """)
        
        resultados = generar_arbol_monedas(num_items)
        total = len(resultados)
        
        st.success(f"### 🎯 Total de resultados posibles: **{total}**")
        
        st.markdown(f"""
        **Usando el Principio Multiplicativo:**
        
        $$\\text{{Total}} = 2 \\times 2 \\times ... \\times 2 = 2^{{{num_items}}} = {total}$$
        """)
        
        with st.expander("📋 Ver todos los resultados posibles"):
            resultados_str = ['-'.join(r) for r in resultados]
            
            cols = st.columns(4)
            for idx, res in enumerate(resultados_str):
                cols[idx % 4].markdown(f"**{idx+1}.** {res}")
        
        if num_items <= 3:
            st.markdown("### 🌳 Representación del Árbol:")
            
            if num_items == 2:
                st.code("""
           Inicio
          /      \\
         C        S
        / \\      / \\
       C   S    C   S
      (CC)(CS)(SC)(SS)
                """)
            elif num_items == 3:
                st.code("""
                    Inicio
                   /      \\
                  C        S
                /   \\    /   \\
               C     S  C     S
              / \\   / \\ / \\   / \\
             C  S  C S C S  C  S
           CCC CCS CSC CSS SCC SCS SSC SSS
                """)
        
        if num_items >= 4:
            st.warning(f"⚠️ Con {num_items} monedas, el árbol tiene **{total} ramas finales**. ¡Es demasiado complejo para dibujarlo! Por eso usamos **fórmulas**.")
    
    else:  # Dados
        num_items = st.slider("Número de dados:", 1, 3, 2)
        
        st.markdown(f"### Lanzando {num_items} dado(s)")
        st.markdown("""
        **Opciones por dado:** 1, 2, 3, 4, 5, 6
        """)
        
        resultados = generar_arbol_dados(num_items)
        total = len(resultados)
        
        st.success(f"### 🎯 Total de resultados posibles: **{total}**")
        
        st.markdown(f"""
        **Usando el Principio Multiplicativo:**
        
        $$\\text{{Total}} = 6 \\times 6 \\times ... \\times 6 = 6^{{{num_items}}} = {total}$$
        """)
        
        with st.expander("📋 Ver todos los resultados posibles"):
            if total <= 100:
                resultados_str = ['-'.join(map(str, r)) for r in resultados]
                
                cols = st.columns(6)
                for idx, res in enumerate(resultados_str):
                    cols[idx % 6].markdown(f"**{idx+1}.** ({res})")
            else:
                st.warning(f"⚠️ Demasiados resultados ({total}) para mostrar todos.")
                st.markdown("**Primeros 36 resultados:**")
                resultados_str = ['-'.join(map(str, r)) for r in resultados[:36]]
                cols = st.columns(6)
                for idx, res in enumerate(resultados_str):
                    cols[idx % 6].markdown(f"**{idx+1}.** ({res})")
        
        if num_items >= 3:
            st.warning(f"⚠️ Con {num_items} dados, el árbol tiene **{total} ramas finales**. ¡Por eso necesitamos **fórmulas**!")
    
    st.markdown("---")
    st.info("""
    ### 💡 Conclusión:
    
    Los **diagramas de árbol** son útiles para visualizar casos simples, pero cuando el número aumenta, 
    necesitamos **fórmulas matemáticas** para contar eficientemente.
    """)

# --- PÁGINA 3: PRINCIPIO MULTIPLICATIVO ---

elif page == "3. 📊 Principio Multiplicativo":
    st.title("📊 Principio Multiplicativo Interactivo")
    st.markdown("Base fundamental de las técnicas de conteo")
    st.markdown("---")
    
    st.markdown("""
    ## 🎯 Concepto Clave:
    
    Si una tarea consta de **$k$ etapas secuenciales**, donde:
    - La etapa 1 tiene $n_1$ opciones
    - La etapa 2 tiene $n_2$ opciones
    - ...
    - La etapa $k$ tiene $n_k$ opciones
    
    Entonces el **número total de formas** de completar la tarea es:
    
    ### $$\\text{Total} = n_1 \\times n_2 \\times ... \\times n_k$$
    """)
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📝 Ejemplo Guiado", "🧮 Calculadora", "🎯 Ejemplos del Mundo Real"])
    
    with tab1:
        st.markdown("### 🎲 Ejemplo: Lanzar 2 dados")
        
        col1, col2, col3 = st.columns([1, 0.3, 1])
        
        with col1:
            st.markdown("#### Dado 1")
            st.markdown("**Opciones:** 6")
            st.markdown("(1, 2, 3, 4, 5, 6)")
        
        with col2:
            st.markdown("#### ")
            st.markdown("## ×")
        
        with col3:
            st.markdown("#### Dado 2")
            st.markdown("**Opciones:** 6")
            st.markdown("(1, 2, 3, 4, 5, 6)")
        
        st.success("### Resultado: $6 \\times 6 = 36$ resultados posibles")
        
        st.markdown("---")
        st.markdown("#### ¿Qué pasa si agregamos un dado más?")
        
        resultado_3_dados = 6 * 6 * 6
        st.info(f"$$6 \\times 6 \\times 6 = {resultado_3_dados}$$ resultados posibles")
        
        # Gráfico de crecimiento
        data_dados = pd.DataFrame({
            'Número de Dados': [1, 2, 3, 4, 5],
            'Resultados Posibles': [6, 36, 216, 1296, 7776]
        })
        
        fig = px.bar(data_dados, x='Número de Dados', y='Resultados Posibles',
                     title='Crecimiento Exponencial de Resultados',
                     text='Resultados Posibles',
                     color='Resultados Posibles',
                     color_continuous_scale='Blues')
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 🧮 Calculadora de Principio Multiplicativo")
        
        num_etapas = st.slider("¿Cuántas etapas tiene tu problema?", 2, 6, 3)
        
        st.markdown("**Define las opciones para cada etapa:**")
        
        opciones = []
        cols = st.columns(num_etapas)
        
        for i in range(num_etapas):
            with cols[i]:
                valor = st.number_input(f"Etapa {i+1}", min_value=1, max_value=100, value=5, step=1, key=f"etapa_{i}")
                opciones.append(valor)
        
        # Cálculo
        total = 1
        formula_str = " \\times ".join(map(str, opciones))
        for op in opciones:
            total *= op
        
        st.markdown("---")
        st.markdown("### 📊 Resultado:")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**Fórmula:** $${formula_str}$$")
        with col_b:
            st.success(f"### **Total: {total:,}**")
        
        # Visualización del proceso
        st.markdown("### 📈 Crecimiento acumulativo:")
        
        acumulado = []
        actual = 1
        for i, op in enumerate(opciones):
            actual *= op
            acumulado.append(actual)
        
        df_acum = pd.DataFrame({
            'Etapa': [f"Etapa {i+1}" for i in range(len(opciones))],
            'Acumulado': acumulado
        })
        
        fig2 = px.line(df_acum, x='Etapa', y='Acumulado', markers=True,
                      title='Resultados Acumulados por Etapa',
                      text='Acumulado')
        fig2.update_traces(textposition='top center', line=dict(width=3))
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        st.markdown("### 🌍 Ejemplos del Mundo Real")
        
        ejemplo_seleccionado = st.selectbox("Selecciona un ejemplo:", [
            "🏦 Contraseña Bancaria (4 dígitos)",
            "🚗 Placa de Vehículo",
            "👕 Combinaciones de Ropa",
            "🎵 Secuencia Musical"
        ])
        
        if "Contraseña" in ejemplo_seleccionado:
            st.markdown("""
            ### 🏦 Contraseña Bancaria de 4 Dígitos
            
            **Situación:** Asignar una contraseña al azar con 4 dígitos (0-9).
            
            **CON reemplazo y CON orden** (se pueden repetir dígitos)
            """)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown("#### Dígito 1\n**10** opciones")
            with col2:
                st.markdown("#### Dígito 2\n**10** opciones")
            with col3:
                st.markdown("#### Dígito 3\n**10** opciones")
            with col4:
                st.markdown("#### Dígito 4\n**10** opciones")
            
            total_pass = 10 ** 4
            st.success(f"### Total: $$10 \\times 10 \\times 10 \\times 10 = 10^4 = {total_pass:,}$$ contraseñas posibles")
            
            st.info("💡 **Aplicación:** Seguridad bancaria - cuantas más opciones, más difícil adivinar.")
        
        elif "Placa" in ejemplo_seleccionado:
            st.markdown("""
            ### 🚗 Placa de Vehículo (Formato: ABC-123)
            
            **Situación:** 3 letras seguidas de 3 números
            """)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Letras (3 posiciones)\n**26** opciones cada una")
                st.markdown("$$26 \\times 26 \\times 26 = 26^3 = 17,576$$")
            with col2:
                st.markdown("#### Números (3 posiciones)\n**10** opciones cada uno")
                st.markdown("$$10 \\times 10 \\times 10 = 10^3 = 1,000$$")
            
            total_placas = (26**3) * (10**3)
            st.success(f"### Total: $$26^3 \\times 10^3 = {total_placas:,}$$ placas posibles")
            
            st.info("💡 **Aplicación:** Sistema de registro vehicular.")
        
        elif "Ropa" in ejemplo_seleccionado:
            st.markdown("""
            ### 👕 Combinaciones de Ropa
            
            **Situación:** Tienes:
            - 5 camisas
            - 3 pantalones
            - 4 pares de zapatos
            
            ¿Cuántos outfits diferentes puedes armar?
            """)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("#### Camisas\n**5** opciones")
            with col2:
                st.markdown("#### Pantalones\n**3** opciones")
            with col3:
                st.markdown("#### Zapatos\n**4** opciones")
            
            total_outfits = 5 * 3 * 4
            st.success(f"### Total: $$5 \\times 3 \\times 4 = {total_outfits}$$ outfits posibles")
            
            st.info("💡 **Aplicación:** Planificación de vestuario semanal.")
        else:
            st.markdown("""### 🎵 Secuencia Musical de 3 Notas
                    
                **Situación:** Crear una melodía simple de 3 notas usando las 7 notas naturales.
                    
                ¿Cuántas melodías diferentes puedes crear si las notas pueden repetirse?
                """)
        
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("#### Nota 1\n**7** opciones")
            with col2:
                st.markdown("#### Nota 2\n**7** opciones")
            with col3:
                st.markdown("#### Nota 3\n**7** opciones")
            
            total_melodias = 7 ** 3
            st.success(f"### Total: $$7 \\times 7 \\times 7 = 7^3 = {total_melodias}$$ melodías posibles")
            
            st.info("💡 **Aplicación:** Composición musical básica, análisis de patrones melódicos.")

# --- PÁGINA 4: MAPA DE DECISIÓN ---

elif page == "4. 🧭 ¿Qué técnica usar?":
    st.title("🧭 ¿Qué Técnica de Conteo Debo Usar?")
    st.markdown("Guía interactiva para identificar la técnica correcta")
    st.markdown("---")
    
    st.markdown("""
    ## 🎯 Las Dos Preguntas Clave:
    
    Para elegir la técnica correcta, debes responder:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 1️⃣ ¿Importa el ORDEN?
        
        **El orden importa cuando:**
        - Los elementos tienen posiciones específicas
        - Cambiar el orden produce un resultado diferente
        
        **Ejemplo:**
        - 🏅 **Podio:** 1° lugar ≠ 2° lugar (SÍ importa)
        - 👥 **Comité:** Todos iguales (NO importa)
        """)
    
    with col2:
        st.markdown("""
        ### 2️⃣ ¿Hay REPETICIÓN/REEMPLAZO?
        
        **Hay repetición cuando:**
        - Un elemento puede usarse múltiples veces
        - Después de elegir, se "devuelve" y puede elegirse de nuevo
        
        **Ejemplo:**
        - 🔢 **Contraseña:** Puede tener 111 (SÍ hay reemplazo)
        - 🎭 **Seleccionar amigos para un viaje:** Si ya seleccionaste a un amigo, no puedes volverlo a seleccionar, no tiene sentido (NO HAY REEMPLAZO)
        """)
    
    st.markdown("---")
    
    st.markdown("## 🔍 Simulador de Decisión")
    
    st.markdown("### Responde estas preguntas sobre tu problema:")
    
    orden_usuario = st.radio("**¿Importa el ORDEN?**", ["✅ SÍ", "❌ NO"], horizontal=True)
    repeticion_usuario = st.radio("**¿Hay REPETICIÓN?**", ["✅ SÍ", "❌ NO"], horizontal=True)
    
    orden_bool = "SÍ" in orden_usuario
    rep_bool = "SÍ" in repeticion_usuario
    
    st.markdown("---")
    
    # Determinar técnica
    if orden_bool and rep_bool:
        tecnica_nombre = "Variaciones con Repetición"
        formula = "n^r"
        color = "#FF6B6B"
        ejemplo = "Contraseña de 4 dígitos: $10^4 = 10,000$"
        cuando = "Cuando el orden importa y los elementos pueden repetirse"
    elif orden_bool and not rep_bool:
        tecnica_nombre = "Permutaciones"
        formula = "P(n,r) = \\frac{n!}{(n-r)!}"
        color = "#4ECDC4"
        ejemplo = "Podio de 10 personas (3 lugares): $P(10,3) = 720$"
        cuando = "Cuando el orden importa pero NO hay repetición"
    elif not orden_bool and not rep_bool:
        tecnica_nombre = "Combinaciones"
        formula = "C(n,r) = \\frac{n!}{r!(n-r)!}"
        color = "#95E1D3"
        ejemplo = "Escoger 2 amigos de 5: $C(5,2) = 10$"
        cuando = "Cuando el orden NO importa y NO hay repetición"
    else:  # not orden_bool and rep_bool
        tecnica_nombre = "Combinaciones con Repetición"
        formula = "C_r(n+r-1,r) = \\frac{(n+r-1)!}{r!(n-1)!}"
        color = "#F38181"
        ejemplo = "Escoger 3 sabores de helado de 5 (puedes repetir): $CR(5,3) = 35$"
        cuando = "Cuando el orden NO importa pero SÍ hay repetición"
    
    # Mostrar resultado
    st.markdown(f"""
    <div style="background-color: {color}; padding: 20px; border-radius: 10px; color: white;">
    <h2 style="color: white;">🎯 Técnica Recomendada: {tecnica_nombre}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"### Fórmula: $${formula}$$")
    st.markdown(f"**Cuándo usar:** {cuando}")
    st.markdown(f"**Ejemplo:** {ejemplo}")
    
    st.markdown("---")
    
    st.markdown("## 📊 Tabla Resumen de las 4 Técnicas")
    
    tabla_resumen = pd.DataFrame({
        "ORDEN": ["✅ SÍ", "✅ SÍ", "❌ NO", "❌ NO"],
        "REPETICIÓN": ["✅ SÍ", "❌ NO", "❌ NO", "✅ SÍ"],
        "Técnica": ["Variaciones con Repetición", "Permutaciones", "Combinaciones", "Combinaciones con Repetición"],
        "Fórmula": ["$n^r$", "$\\frac{n!}{(n-r)!}$", "$\\frac{n!}{r!(n-r)!}$", "$\\frac{(n+r-1)!}{r!(n-1)!}$"],
        "Ejemplo": ["Contraseña", "Podio", "Comité", "Helados"]
    })
    
    st.dataframe(tabla_resumen, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.markdown("## 🎓 Ejemplos Adicionales por Técnica:")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### ✅ CON Orden")
        st.info("""
        **Variaciones con Repetición ($n^r$):**
        - Lanzar 3 dados
        - PIN de celular
        - Placas de autos
        
        **Permutaciones $P(n,r)$:**
        - Orden de oradores
        - Carreras deportivas
        - Rotación médica
        """)
    
    with col_b:
        st.markdown("### ❌ SIN Orden")
        st.info("""
        **Combinaciones $C(n,r)$:**
        - Baloto
        - Formar equipos
        - Seleccionar tratamientos
        
        **Comb. con Repetición $C_r(n+r-1,r)$:**
        - Comprar frutas (3 manzanas)
        - Notas musicales en acordes
        - Distribución de recursos
        """)

# --- PÁGINA 5: LAS 4 TÉCNICAS ---

elif page == "5. 🔢 Las 4 Técnicas":
    st.title("🔢 Las 4 Técnicas de Conteo")
    st.markdown("Aprende cada técnica con ejemplos interactivos")
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔢 CON Orden + CON Repetición",
        "🎯 CON Orden + SIN Repetición", 
        "🎲 SIN Orden + SIN Repetición",
        "🍦 SIN Orden + CON Repetición"
    ])
    
    # TAB 1: Variaciones con Repetición
    with tab1:
        st.markdown("## 🔢 Variaciones con Repetición")
        st.markdown("### **Cuándo usar:** Orden importa + Se puede repetir")
        
        st.markdown("---")
        
        st.markdown("""
        ### 📐 Fórmula:
        
        $$n^r$$
        
        Donde:
        - $n$ = número de opciones disponibles
        - $r$ = número de selecciones a realizar
        """)
        
        st.markdown("---")
        
        st.markdown("### 📚 Ejemplos:")
        
        ejemplo_var = st.selectbox("Selecciona un ejemplo:", [
            "🏦 Contraseña bancaria de 4 dígitos",
            "🌍 Expansión a mercados internacionales",
            "🎵 Melodía de 4 notas",
            "🎨 Código de color RGB"
        ], key="ejemplo_variacion")
        
        if "Contraseña" in ejemplo_var:
            st.markdown("""
            #### 🏦 Contraseña Bancaria de 4 Dígitos
            
            **Situación:** 
            - Tenemos 10 dígitos (0-9)
            - Debemos elegir 4 dígitos
            - Los dígitos pueden repetirse
            - El orden importa (1234 ≠ 4321)
            """)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Datos:**")
                st.markdown("- $n = 10$ (dígitos)")
                st.markdown("- $r = 4$ (posiciones)")
            
            with col2:
                st.markdown("**Solución:**")
                st.markdown("$$10^4 = 10 \\times 10 \\times 10 \\times 10 = 10,000$$")
                st.success("### ✅ 10,000 contraseñas posibles")
            
            st.info("💡 **Interpretación:** Cada posición tiene 10 opciones independientes.")
        
        elif "mercados" in ejemplo_var:
            st.markdown("""
            #### 🌍 Expansión a Mercados Internacionales
            
            **Situación:**
            - Debes elegir una estrategia de entrada a 3 mercados diferentes
            - Para cada mercado hay 4 estrategias (Franquicia, Joint Venture, Subsidiaria, Exportación)
            - Las estrategias pueden repetirse entre mercados
            - El orden importa (Mercado 1 es diferente a Mercado 2)
            """)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Datos:**")
                st.markdown("- $n = 4$ (estrategias)")
                st.markdown("- $r = 3$ (mercados)")
            
            with col2:
                st.markdown("**Solución:**")
                st.markdown("$$4^3 = 4 \\times 4 \\times 4 = 64$$")
                st.success("### ✅ 64 planes de expansión posibles")
            
            st.info("💡 **Interpretación:** Puedes usar la misma estrategia en varios mercados (ej: Franquicia en los 3).")
        
        elif "Melodía" in ejemplo_var:
            st.markdown("""
            #### 🎵 Melodía de 4 Notas
            
            **Situación:**
            - Hay 7 notas naturales (Do, Re, Mi, Fa, Sol, La, Si)
            - Creamos una melodía de 4 notas
            - Las notas pueden repetirse
            - El orden importa (Do-Re-Mi ≠ Mi-Re-Do)
            """)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Datos:**")
                st.markdown("- $n = 7$ (notas)")
                st.markdown("- $r = 4$ (posiciones)")
            
            with col2:
                st.markdown("**Solución:**")
                st.markdown("$$7^4 = 7 \\times 7 \\times 7 \\times 7 = 2,401$$")
                st.success("### ✅ 2,401 melodías posibles")
        
        else:  # RGB
            st.markdown("""
            #### 🎨 Código de Color RGB
            
            **Situación:**
            - RGB tiene 3 canales (Rojo, Verde, Azul)
            - Cada canal: 0-255 (256 valores)
            - Los valores pueden repetirse
            - El orden importa (255,0,0 = rojo puro)
            """)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Datos:**")
                st.markdown("- $n = 256$ (valores)")
                st.markdown("- $r = 3$ (canales)")
            
            with col2:
                st.markdown("**Solución:**")
                st.markdown("$$256^3 = 256 \\times 256 \\times 256 = 16,777,216$$")
                st.success("### ✅ 16,777,216 colores posibles")
      
        st.markdown("---")
        
        st.markdown("### 🧮 Calculadora Interactiva")
        
        col_calc1, col_calc2 = st.columns(2)
        with col_calc1:
            n_var = st.number_input("Número de opciones (n):", min_value=1, max_value=100, value=10, key="n_var")
        with col_calc2:
            r_var = st.number_input("Número de selecciones (r):", min_value=1, max_value=20, value=4, key="r_var")
        
        resultado_var = n_var ** r_var
        
        st.markdown(f"### Resultado: $${n_var}^{{{r_var}}} = {resultado_var:,}$$")
        
        # Visualización
        if r_var <= 10:
            proceso = [n_var ** i for i in range(1, r_var + 1)]
            df_proceso = pd.DataFrame({
                'Selección': [f"{i}" for i in range(1, r_var + 1)],
                'Total Acumulado': proceso
            })
            
            fig = px.bar(df_proceso, x='Selección', y='Total Acumulado',
                        title=f'Crecimiento de opciones (n={n_var})',
                        text='Total Acumulado')
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB 2: Permutaciones
    with tab2:
        st.markdown("## 🎯 Permutaciones")
        st.markdown("### **Cuándo usar:** Orden importa + NO se repite")
        
        st.markdown("---")
        
        st.markdown("""
        ### 📐 Fórmula:
        
        $$P(n,r) = \\frac{n!}{(n-r)!}$$
        
        Donde:
        - $n$ = número total de elementos
        - $r$ = número de posiciones a llenar
        - $n!$ = factorial de $n$ (n × (n-1) × (n-2) × ... × 1)
        """)
        
        st.markdown("---")
        
        st.markdown("### 📚 Ejemplos:")
        
        ejemplo_perm = st.selectbox("Selecciona un ejemplo:", [
            "🏅 Podio de 10 personas (3 lugares)",
            "🎭 Orden de presentación de 5 estudiantes",
            "🏥 Rotación médica por 3 especialidades",
            "🔳 Orden de cuadros en un estante"
        ], key="ejemplo_permutacion")
        
        if "Podio" in ejemplo_perm:
            st.markdown("""
            #### 🏅 Podio de 10 Personas
            
            **Situación:**
            - Hay 10 competidores
            - Se asignan 3 lugares (1°, 2°, 3°)
            - Una persona no puede estar en dos lugares
            - El orden importa (1° ≠ 3°)
            """)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Datos:**")
                st.markdown("- $n = 10$ (personas)")
                st.markdown("- $r = 3$ (lugares)")
            
            with col2:
                st.markdown("**Solución:**")
                st.markdown("$$P(10,3) = \\frac{10!}{(10-3)!} = \\frac{10!}{7!}$$")
                st.markdown("$$= 10 \\times 9 \\times 8 = 720$$")
                st.success("### ✅ 720 podios posibles")
            
            st.info("💡 **Interpretación:** 10 opciones para 1°, quedan 9 para 2°, quedan 8 para 3°.")
        
        elif "presentación" in ejemplo_perm:
            st.markdown("""
            #### 🎭 Orden de Presentación
            
            **Situación:**
            - 5 estudiantes deben presentar
            - Solo hay tiempo para 3 presentaciones
            - Cada estudiante presenta una vez
            - El orden importa (primero vs último)
            """)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Datos:**")
                st.markdown("- $n = 5$ (estudiantes)")
                st.markdown("- $r = 3$ (turnos)")
            
            with col2:
                st.markdown("**Solución:**")
                st.markdown("$$P(5,3) = \\frac{5!}{2!} = 5 \\times 4 \\times 3 = 60$$")
                st.success("### ✅ 60 órdenes posibles")
        
        elif "Rotación" in ejemplo_perm:
            st.markdown("""
            #### 🏥 Rotación Médica
            
            **Situación:**
            - Hay 8 especialidades disponibles
            - El estudiante rota por 3 especialidades
            - Cada especialidad solo una vez
            - El orden importa (primera rotación tiene más impacto)
            """)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Datos:**")
                st.markdown("- $n = 8$ (especialidades)")
                st.markdown("- $r = 3$ (rotaciones)")
            
            with col2:
                st.markdown("**Solución:**")
                st.markdown("$$P(8,3) = \\frac{8!}{5!} = 8 \\times 7 \\times 6 = 336$$")
                st.success("### ✅ 336 planes de rotación posibles")
        
        else:  # Libros
            st.markdown("""
            #### 🔳 Orden de cuadros en un Estante
            
            **Situación:**
            - Tienes 7 cuadros
            - Solo caben 4 en la pared
            - Cada cuadro se ubica solo una vez
            - Supongamos que el orden importa visualmente por cuestiones estéticas.
            """)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Datos:**")
                st.markdown("- $n = 7$ (libros)")
                st.markdown("- $r = 4$ (espacios)")
            
            with col2:
                st.markdown("**Solución:**")
                st.markdown("$$P(7,4) = \\frac{7!}{3!} = 7 \\times 6 \\times 5 \\times 4 = 840$$")
                st.success("### ✅ 840 arreglos posibles")
        
        st.markdown("---")
        
        st.markdown("### 🧮 Calculadora Interactiva")
        
        col_calc1, col_calc2 = st.columns(2)
        with col_calc1:
            n_perm = st.number_input("Número total de elementos (n):", min_value=1, max_value=20, value=10, key="n_perm")
        with col_calc2:
            r_perm = st.number_input("Número de posiciones (r):", min_value=1, max_value=20, value=3, key="r_perm")
        
        if r_perm > n_perm:
            st.error("❌ Error: r no puede ser mayor que n")
        else:
            resultado_perm = permutacion(n_perm, r_perm)
            
            st.markdown(f"### Resultado: $$P({n_perm},{r_perm}) = \\frac{{{n_perm}!}}{{{n_perm-r_perm}!}} = {resultado_perm:,}$$")
            
            # Mostrar expansión
            with st.expander("🔍 Ver expansión paso a paso"):
                st.markdown(f"$$P({n_perm},{r_perm}) = {n_perm}! ÷ {n_perm-r_perm}!$$")
                factores = [str(i) for i in range(n_perm, n_perm - r_perm, -1)]
                factores_str = ' \\times '.join(factores)
                st.markdown(f"$$= {factores_str} = {resultado_perm:,}$$")
    
    # TAB 3: Combinaciones
    with tab3:
        st.markdown("## 🎲 Combinaciones")
        st.markdown("### **Cuándo usar:** Orden NO importa + NO se repite")
        
        st.markdown("---")
        
        st.markdown("""
        ### 📐 Fórmula:
        
        $$C(n,r) = \\frac{n!}{r!(n-r)!}$$
        
        También escrito como: $\\binom{n}{r}$ o $_nC_r$
        
        Donde:
        - $n$ = número total de elementos
        - $r$ = número de elementos a seleccionar
        """)
        
        st.markdown("---")
        
        st.markdown("### 🤔 Diferencia con Permutaciones:")
        
        col_dif1, col_dif2 = st.columns(2)
        
        with col_dif1:
            st.info("""
            **Permutación P(5,2) = 20**
            
            Orden importa:
            - {A, B} ≠ {B, A}
            - AB, BA, AC, CA, AD, DA...
            
            Resultado: **20 formas**
            """)
        
        with col_dif2:
            st.success("""
            **Combinación C(5,2) = 10**
            
            Orden NO importa:
            - {A, B} = {B, A}
            - AB, AC, AD, AE, BC...
            
            Resultado: **10 formas**
            """)
        
        st.markdown("---")
        
        st.markdown("### 📚 Ejemplos:")
        
        ejemplo_comb = st.selectbox("Selecciona un ejemplo:", [
            "👥 Comité de 4 personas de 10",
            "🎰 Baloto (6 números diferentes de 45)",
            "🏥 Tratamiento combinado (2 de 6 medicamentos)",
            "👶 Grupo de lectura (4 niños de 12)"
        ], key="ejemplo_combinacion")
        
        if "Comité" in ejemplo_comb:
            st.markdown("""
            #### 👥 Comité de 4 Personas
            
            **Situación:**
            - Hay 10 empleados
            - Se forma un comité de 4 personas
            - Todos tienen el mismo rol
            - El orden NO importa
            """)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Datos:**")
                st.markdown("- $n = 10$ (empleados)")
                st.markdown("- $r = 4$ (miembros)")
            
            with col2:
                st.markdown("**Solución:**")
                st.markdown("$$C(10,4) = \\frac{10!}{4!(10-4)!} = \\frac{10!}{4! \\times 6!}$$")
                st.markdown("$$= \\frac{10 \\times 9 \\times 8 \\times 7}{4 \\times 3 \\times 2 \\times 1} = \\frac{5040}{24} = 210$$")
                st.success("### ✅ 210 comités posibles")
            
            st.info("💡 **¿Por qué dividir entre r!?** Porque eliminamos las repeticiones por orden.")
        
        elif "Baloto" in ejemplo_comb:
            st.markdown("""
            #### 🎰 Baloto Colombiano
            
            **Situación:**
            - Hay 45 números disponibles
            - Se eligen 6 números diferentes
            - El orden NO importa (solo importa acertar los números)
            - Sin repetición
            """)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Datos:**")
                st.markdown("- $n = 45$ (números)")
                st.markdown("- $r = 6$ (selección)")
            
            with col2:
                st.markdown("**Solución:**")
                st.markdown("$$C(45,6) = \\frac{45!}{6! \\times 37!}$$")
                resultado_baloto = combinacion(45, 6)
                st.markdown(f"$$= {resultado_baloto:,}$$")
                st.success(f"### ✅ {resultado_baloto:,} combinaciones posibles")
            
            probabilidad = 1 / resultado_baloto
            st.warning(f"⚠️ **Probabilidad de ganar:** 1 en {resultado_baloto:,} = {probabilidad:.10f}")
        
        elif "Tratamiento" in ejemplo_comb:
            st.markdown("""
            #### 🏥 Tratamiento Médico Combinado
            
            **Situación:**
            - Hay 6 medicamentos disponibles
            - Se recetan 2 medicamentos complementarios
            - El orden NO importa (A+B = B+A)
            - Sin repetición (no se duplica medicamento)
            """)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Datos:**")
                st.markdown("- $n = 6$ (medicamentos)")
                st.markdown("- $r = 2$ (selección)")
            
            with col2:
                st.markdown("**Solución:**")
                st.markdown("$$C(6,2) = \\frac{6!}{2! \\times 4!} = \\frac{6 \\times 5}{2 \\times 1} = 15$$")
                st.success("### ✅ 15 combinaciones de tratamiento")
        
        else:  # Grupo lectura
            st.markdown("""
            #### 👶 Grupo de Lectura Infantil
            
            **Situación:**
            - Hay 12 niños en la clase
            - Se forma un grupo de 4 para lectura
            - Todos leen juntos (sin orden específico)
            - Cada niño va a un solo grupo
            """)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Datos:**")
                st.markdown("- $n = 12$ (niños)")
                st.markdown("- $r = 4$ (grupo)")
            
            with col2:
                st.markdown("**Solución:**")
                st.markdown("$$C(12,4) = \\frac{12!}{4! \\times 8!}$$")
                resultado_ninos = combinacion(12, 4)
                st.markdown(f"$$= {resultado_ninos}$$")
                st.success(f"### ✅ {resultado_ninos} grupos posibles")
        
        st.markdown("---")
        
        st.markdown("### 🧮 Calculadora Interactiva")
        
        col_calc1, col_calc2 = st.columns(2)
        with col_calc1:
            n_comb = st.number_input("Número total de elementos (n):", min_value=1, max_value=50, value=10, key="n_comb")
        with col_calc2:
            r_comb = st.number_input("Número de elementos a elegir (r):", min_value=1, max_value=50, value=4, key="r_comb")
        
        if r_comb > n_comb:
            st.error("❌ Error: r no puede ser mayor que n")
        else:
            resultado_comb = combinacion(n_comb, r_comb)
            
            st.markdown(f"### Resultado: $$C({n_comb},{r_comb}) = \\frac{{{n_comb}!}}{{{r_comb}! \\times {n_comb-r_comb}!}} = {resultado_comb:,}$$")
            
            # Comparación con Permutación
            resultado_perm_comp = permutacion(n_comb, r_comb)
            factor = factorial(r_comb)
            
            st.info(f"""
            📊 **Comparación:**
            - Permutación P({n_comb},{r_comb}) = **{resultado_perm_comp:,}** (orden importa)
            - Combinación C({n_comb},{r_comb}) = **{resultado_comb:,}** (orden NO importa)
            - Diferencia: Se divide entre {r_comb}! = {factor}
            """)
            
            # Visualización
            if n_comb <= 20:
                valores_c = [combinacion(n_comb, i) for i in range(0, n_comb + 1)]
                df_triangulo = pd.DataFrame({
                    'r': list(range(0, n_comb + 1)),
                    f'C({n_comb},r)': valores_c
                })
                
                fig = px.line(df_triangulo, x='r', y=f'C({n_comb},r)', markers=True,
                            title=f'Triángulo de Pascal: Fila {n_comb}')
                st.plotly_chart(fig, use_container_width=True)
    
    # TAB 4: Combinaciones con Repetición
    with tab4:
        st.markdown("## 🍦 Combinaciones con Repetición")
        st.markdown("### **Cuándo usar:** Orden NO importa + SÍ se repite")
        
        st.markdown("---")
        
        st.markdown("""
        ### 📐 Fórmula:
        
        $$C_r(n+r-1, r) = \\frac{(n+r-1)!}{r!(n-1)!}$$
        
        Donde:
        - $n$ = número de tipos diferentes
        - $r$ = número de selecciones a realizar
        """)
        
        st.markdown("---")
        
        st.markdown("### 🤔 ¿Por qué es diferente?")
        
        st.info("""
        **Ejemplo Ilustrativo: Escoger 3 frutas de 2 tipos {🍎, 🍊}**
        
        **Combinación normal C(2,3):** ❌ Imposible (no puedes escoger 3 de 2 sin repetir)
        
        **Combinación con repetición CR(2,3):** ✅ Posible
        - {🍎, 🍎, 🍎}
        - {🍎, 🍎, 🍊}
        - {🍎, 🍊, 🍊}
        - {🍊, 🍊, 🍊}
        
        Total: **4 formas** = CR(2,3) = C(4,3) = 4
        """)
        
        st.markdown("---")
        
        st.markdown("### 📚 Ejemplos:")
        
        ejemplo_comb_rep = st.selectbox("Selecciona un ejemplo:", [
            "🍦 Helado: 3 bolas de 5 sabores",
            "🎵 Acorde de 3 notas de 12 cromáticas",
            "🎨 Selección de 3 colores de 8 disponibles",
            "📦 Distribución de 4 productos en 3 categorías"
        ], key="ejemplo_comb_rep")
        
        if "Helado" in ejemplo_comb_rep:
            st.markdown("""
            #### 🍦 Helado con 3 Bolas
            
            **Situación:**
            - Hay 5 sabores disponibles
            - Pides 3 bolas
            - Puedes repetir sabores (3 de chocolate está bien)
            - El orden NO importa (fresa-vainilla = vainilla-fresa)
            """)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Datos:**")
                st.markdown("- $n = 5$ (sabores)")
                st.markdown("- $r = 3$ (bolas)")
            
            with col2:
                st.markdown("**Solución:**")
                st.markdown("$$CR(5,3) = C(5+3-1, 3) = C(7,3)$$")
                st.markdown("$$= \\frac{7!}{3! \\times 4!} = \\frac{7 \\times 6 \\times 5}{3 \\times 2 \\times 1} = 35$$")
                st.success("### ✅ 35 combinaciones posibles")
            
            st.info("💡 **Interpretación:** Es como distribuir 3 bolas idénticas en 5 categorías.")
        
        elif "Acorde" in ejemplo_comb_rep:
            st.markdown("""
            #### 🎵 Acorde Musical
            
            **Situación:**
            - Hay 12 notas cromáticas
            - Formas un acorde de 3 notas
            - Pueden repetirse (Do-Do-Mi es válido para inversiones)
            - El orden NO importa (Do-Mi-Sol = Sol-Mi-Do)
            """)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Datos:**")
                st.markdown("- $n = 12$ (notas)")
                st.markdown("- $r = 3$ (notas en acorde)")
            
            with col2:
                st.markdown("**Solución:**")
                st.markdown("$$CR(12,3) = C(14,3)$$")
                resultado_acorde = combinacion_repeticion(12, 3)
                st.markdown(f"$$= {resultado_acorde}$$")
                st.success(f"### ✅ {resultado_acorde} acordes posibles")
        
        elif "colores" in ejemplo_comb_rep:
            st.markdown("""
            #### 🎨 Selección de Colores en Arte
            
            **Situación:**
            - Hay 8 colores disponibles
            - Los niños eligen 3 colores para su obra
            - Pueden usar el mismo color varias veces
            - El orden NO importa (solo importa qué colores tienen)
            """)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Datos:**")
                st.markdown("- $n = 8$ (colores)")
                st.markdown("- $r = 3$ (selecciones)")
            
            with col2:
                st.markdown("**Solución:**")
                st.markdown("$$CR(8,3) = C(10,3)$$")
                resultado_colores = combinacion_repeticion(8, 3)
                st.markdown(f"$$= {resultado_colores}$$")
                st.success(f"### ✅ {resultado_colores} selecciones posibles")
        
        else:  # Distribución
            st.markdown("""
            #### 📦 Distribución de Productos
            
            **Situación:**
            - Una tienda tiene 3 categorías de productos
            - Debe seleccionar 4 productos para promoción
            - Pueden elegir varios de la misma categoría
            - El orden NO importa
            """)

            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Datos:**")
                st.markdown("- $n = 3$ (categorías)")
                st.markdown("- $r = 4$ (productos)")
            
            with col2:
                st.markdown("**Solución:**")
                st.markdown("$$CR(3,4) = C(6,4) = 15$$")
                st.success("### ✅ 15 formas de distribuir")

        st.markdown("---")
        
        st.markdown("### 🧮 Calculadora Interactiva")
        
        col_calc1, col_calc2 = st.columns(2)
        with col_calc1:
            n_comb_rep = st.number_input("Número de tipos (n):", min_value=1, max_value=30, value=5, key="n_comb_rep")
        with col_calc2:
            r_comb_rep = st.number_input("Número de selecciones (r):", min_value=1, max_value=30, value=3, key="r_comb_rep")
        
        resultado_comb_rep = combinacion_repeticion(n_comb_rep, r_comb_rep)
        
        st.markdown(f"### Resultado: $$CR({n_comb_rep},{r_comb_rep}) = C({n_comb_rep + r_comb_rep - 1},{r_comb_rep}) = {resultado_comb_rep:,}$$")
        
        # Comparación con combinación normal
        if r_comb_rep <= n_comb_rep:
            resultado_comb_normal = combinacion(n_comb_rep, r_comb_rep)
            st.info(f"""
            📊 **Comparación:**
            - Combinación C({n_comb_rep},{r_comb_rep}) = **{resultado_comb_normal:,}** (sin repetición)
            - Comb. con Rep. CR({n_comb_rep},{r_comb_rep}) = **{resultado_comb_rep:,}** (con repetición)
            - **La repetición aumenta las opciones en {resultado_comb_rep - resultado_comb_normal}**
            """)
        else:
            st.warning(f"⚠️ Combinación normal C({n_comb_rep},{r_comb_rep}) es imposible (r > n), pero CR({n_comb_rep},{r_comb_rep}) = {resultado_comb_rep:,} sí es posible.")

# --- PÁGINA 6: SIMULADOR DE PROBLEMAS ---

elif page == "6. 🎯 Problemas del Mundo Real":
    st.title("🎯 Simulador de Problemas del Mundo Real")
    st.markdown("Aprende a identificar y resolver problemas por área profesional")
    st.markdown("---")
    
    # Selector de carrera
    carrera_seleccionada = st.selectbox("🎓 Selecciona tu área de estudio:", list(BANCO_PROBLEMAS.keys()))
    
    problemas_carrera = BANCO_PROBLEMAS[carrera_seleccionada]
    
    st.markdown(f"## {carrera_seleccionada}")
    st.markdown(f"**Problemas disponibles:** {len(problemas_carrera)}")
    st.markdown("---")
    
    # Selector de problema
    titulos_problemas = [p["titulo"] for p in problemas_carrera]
    problema_idx = st.selectbox("Selecciona un problema:", range(len(titulos_problemas)), 
                                 format_func=lambda x: f"Problema {x+1}: {titulos_problemas[x]}")
    
    problema = problemas_carrera[problema_idx]
    
    st.markdown(f"### 📋 {problema['titulo']}")
    
    # Mostrar contexto y pregunta
    st.info(f"**Contexto:** {problema['contexto']}")
    st.markdown(f"**❓ Pregunta:** {problema['pregunta']}")
    
    st.markdown("---")
    
    # Modo guiado
    st.markdown("## 🧭 Paso 1: Identifica la técnica correcta")
    
    col1, col2 = st.columns(2)
    
    with col1:
        orden_respuesta = st.radio(
            "**¿Importa el ORDEN?**",
            ["Selecciona...", "✅ SÍ importa", "❌ NO importa"],
            key=f"orden_{problema_idx}"
        )
    
    with col2:
        rep_respuesta = st.radio(
            "**¿Hay REPETICIÓN?**",
            ["Selecciona...", "✅ SÍ hay", "❌ NO hay"],
            key=f"rep_{problema_idx}"
        )
    
    if "Selecciona" not in orden_respuesta and "Selecciona" not in rep_respuesta:
        orden_user = "SÍ" in orden_respuesta
        rep_user = "SÍ" in rep_respuesta
        
        # Verificar respuesta
        correcto_orden = orden_user == problema["orden"]
        correcto_rep = rep_user == problema["repeticion"]
        
        if correcto_orden and correcto_rep:
            st.success("✅ ¡Excelente! Identificaste correctamente las características del problema.")
            
            # Mostrar técnica
            st.markdown("---")
            st.markdown("## 📐 Paso 2: Aplica la fórmula")
            
            tecnica_map = {
                "variacion_rep": ("Variaciones con Repetición", "n^r"),
                "permutacion": ("Permutaciones", "P(n,r) = \\frac{n!}{(n-r)!}"),
                "combinacion": ("Combinaciones", "C(n,r) = \\frac{n!}{r!(n-r)!}"),
                "combinacion_rep": ("Combinaciones con Repetición", "CR(n,r) = \\frac{(n+r-1)!}{r!(n-1)!}"),
                "multiplicativo": ("Principio Multiplicativo", "n_1 \\times n_2 \\times ... \\times n_k")
            }
            
            tecnica_nombre, tecnica_formula = tecnica_map[problema["tecnica"]]
            
            st.info(f"""
            **Técnica a usar:** {tecnica_nombre}
            
            **Fórmula:** ${tecnica_formula}$
            """)
            
            # Mostrar solución
            if st.button("🔍 Ver Solución Completa", key=f"sol_{problema_idx}"):
                st.markdown("---")
                st.markdown("## ✅ Solución:")
                
                if problema["n"] is not None:
                    st.markdown(f"**Datos del problema:**")
                    st.markdown(f"- $n = {problema['n']}$")
                    if problema["r"] is not None:
                        st.markdown(f"- $r = {problema['r']}$")
                
                st.markdown(f"**Desarrollo:**")
                st.markdown(f"$${problema['solucion']}$$")
                
                st.success(f"**Explicación:** {problema['explicacion']}")
                
                # Calcular valor numérico
                if problema["tecnica"] == "variacion_rep" and problema["n"] and problema["r"]:
                    resultado_num = problema["n"] ** problema["r"]
                    st.metric("Resultado Final", f"{resultado_num:,}")
                elif problema["tecnica"] == "permutacion" and problema["n"] and problema["r"]:
                    resultado_num = permutacion(problema["n"], problema["r"])
                    st.metric("Resultado Final", f"{resultado_num:,}")
                elif problema["tecnica"] == "combinacion" and problema["n"] and problema["r"]:
                    resultado_num = combinacion(problema["n"], problema["r"])
                    st.metric("Resultado Final", f"{resultado_num:,}")
                elif problema["tecnica"] == "combinacion_rep" and problema["n"] and problema["r"]:
                    resultado_num = combinacion_repeticion(problema["n"], problema["r"])
                    st.metric("Resultado Final", f"{resultado_num:,}")
        else:
            st.error("❌ Revisa tu respuesta. Analiza bien si el orden importa y si hay repetición.")
            
            if not correcto_orden:
                st.warning("💡 **Pista sobre el ORDEN:** Pregúntate: ¿Cambiar el orden de selección produce un resultado diferente?")
            
            if not correcto_rep:
                st.warning("💡 **Pista sobre la REPETICIÓN:** Pregúntate: ¿Puede un mismo elemento aparecer más de una vez?")

# --- PÁGINA 7: PRÁCTICA INTERACTIVA ---

elif page == "7. 🎲 Práctica Interactiva":
    st.title("🎲 Generador de Ejercicios Aleatorios")
    st.markdown("Practica identificando y resolviendo problemas")
    st.markdown("---")
    
    # Inicializar session state
    if 'ejercicio_actual' not in st.session_state:
        st.session_state.ejercicio_actual = None
        st.session_state.puntaje = 0
        st.session_state.intentos = 0
    
    # Botón para generar nuevo ejercicio
    if st.button("🎲 Generar Nuevo Ejercicio") or st.session_state.ejercicio_actual is None:
        # Seleccionar carrera y problema aleatorio
        carrera_random = random.choice(list(BANCO_PROBLEMAS.keys()))
        problema_random = random.choice(BANCO_PROBLEMAS[carrera_random])
        st.session_state.ejercicio_actual = problema_random
        st.session_state.respondido = False
        st.rerun()
    
    ejercicio = st.session_state.ejercicio_actual
    
    # Mostrar puntaje
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.metric("🎯 Puntaje", st.session_state.puntaje)
    with col_p2:
        st.metric("📊 Ejercicios Resueltos", st.session_state.intentos)
    
    st.markdown("---")
    
    # Mostrar ejercicio
    st.markdown(f"### 📋 {ejercicio['titulo']}")
    st.info(f"**{ejercicio['contexto']}**")
    st.markdown(f"**❓ {ejercicio['pregunta']}**")
    
    st.markdown("---")
    
    # Pregunta 1: Técnica
    st.markdown("### Pregunta 1: ¿Qué técnica debes usar?")
    
    tecnica_usuario = st.radio(
        "Selecciona la técnica correcta:",
        [
            "Variaciones con Repetición (n^r)",
            "Permutaciones P(n,r)",
            "Combinaciones C(n,r)",
            "Combinaciones con Repetición C_r(n+r-1,r)",
            "Principio Multiplicativo"
        ],
        key="tecnica_user"
    )
    
    # Pregunta 2: Cálculo (si tiene n y r)
    if ejercicio["n"] is not None and ejercicio["r"] is not None:
        st.markdown("### Pregunta 2: ¿Cuál es el resultado?")
        
        respuesta_numerica = st.number_input(
            "Ingresa tu respuesta:",
            min_value=0,
            step=1,
            key="respuesta_num"
        )
    
    # Botón verificar
    if st.button("✅ Verificar Respuesta"):
        st.session_state.intentos += 1
        
        # Mapear respuesta del usuario a técnica interna
        tecnica_map_user = {
            "Variaciones con Repetición (n^r)": "variacion_rep",
            "Permutaciones P(n,r)": "permutacion",
            "Combinaciones C(n,r)": "combinacion",
            "Combinaciones con Repetición C_r(n+r-1,r)": "combinacion_rep",
            "Principio Multiplicativo": "multiplicativo"
        }
        
        tecnica_user_code = tecnica_map_user[tecnica_usuario]
        
        # Verificar técnica
        tecnica_correcta = (tecnica_user_code == ejercicio["tecnica"])
        
        # Calcular respuesta correcta numérica
        if ejercicio["tecnica"] == "variacion_rep":
            respuesta_correcta = ejercicio["n"] ** ejercicio["r"]
        elif ejercicio["tecnica"] == "permutacion":
            respuesta_correcta = permutacion(ejercicio["n"], ejercicio["r"])
        elif ejercicio["tecnica"] == "combinacion":
            respuesta_correcta = combinacion(ejercicio["n"], ejercicio["r"])
        elif ejercicio["tecnica"] == "combinacion_rep":
            respuesta_correcta = combinacion_repeticion(ejercicio["n"], ejercicio["r"])
        else:
            respuesta_correcta = None
        
        # Verificar respuesta numérica
        if respuesta_correcta is not None:
            numero_correcto = (respuesta_numerica == respuesta_correcta)
        else:
            numero_correcto = True  # No se evalúa si no hay valor numérico
        
        # Evaluar
        if tecnica_correcta and numero_correcto:
            st.success("🎉 ¡CORRECTO! Excelente trabajo.")
            st.session_state.puntaje += 10
            st.balloons()
        elif tecnica_correcta:
            st.warning(f"⚠️ La técnica es correcta, pero el cálculo no. La respuesta correcta es: **{respuesta_correcta:,}**")
            st.session_state.puntaje += 5
        else:
            st.error(f"❌ Incorrecto. La técnica correcta es: **{ejercicio['tecnica'].replace('_', ' ').title()}**")
        
        # Mostrar explicación
        st.markdown("---")
        st.markdown("## 📚 Explicación:")
        st.info(ejercicio["explicacion"])
        st.markdown(f"**Solución:** ${ejercicio['solucion']}$")
        
        st.session_state.respondido = True

# --- PÁGINA 8: CALCULADORA UNIVERSAL ---

elif page == "8. 🧮 Calculadora Universal":
    st.title("🧮 Calculadora Universal de Técnicas de Conteo")
    st.markdown("Calcula cualquier técnica con explicación paso a paso")
    st.markdown("---")
    
    tecnica_calc = st.selectbox("Selecciona la técnica:", [
        "🔢 Variaciones con Repetición (n^r)",
        "🎯 Permutaciones P(n,r)",
        "🎲 Combinaciones C(n,r)",
        "🍦 Combinaciones con Repetición C_r(n+r-1,r)"
    ])
    
    st.markdown("---")
    
    if "Variaciones" in tecnica_calc:
        st.markdown("## 🔢 Variaciones con Repetición")
        st.markdown("**Fórmula:** $$n^r$$")
        
        col1, col2 = st.columns(2)
        with col1:
            n = st.number_input("n (opciones disponibles):", min_value=1, value=10, key="n_var_calc")
        with col2:
            r = st.number_input("r (selecciones a realizar):", min_value=1, value=4, key="r_var_calc")
        
        resultado = n ** r
        
        st.success(f"## Resultado: $${n}^{{{r}}} = {resultado:,}$$")
        
        with st.expander("📖 Ver explicación paso a paso"):
            st.markdown(f"""
            **Paso 1:** Identificar los valores
            - Tenemos $n = {n}$ opciones disponibles
            - Debemos realizar $r = {r}$ selecciones
            
            **Paso 2:** Aplicar la fórmula
            - Cada selección tiene $n$ opciones
            - Como hay repetición, siempre hay $n$ opciones
            
            **Paso 3:** Calcular
            - ${n} \\times {n} \\times ... \\times {n}$ ({r} veces)
            - $= {n}^{{{r}}} = {resultado:,}$
            """)
    
    elif "Permutaciones" in tecnica_calc:
        st.markdown("## 🎯 Permutaciones")
        st.markdown("**Fórmula:** $$P(n,r) = \\frac{n!}{(n-r)!}$$")
        
        col1, col2 = st.columns(2)
        with col1:
            n = st.number_input("n (elementos totales):", min_value=1, value=10, key="n_perm_calc")
        with col2:
            r = st.number_input("r (posiciones a llenar):", min_value=1, value=3, key="r_perm_calc")
        
        if r > n:
            st.error("❌ Error: r no puede ser mayor que n")
        else:
            resultado = permutacion(n, r)
            
            st.success(f"## Resultado: $$P({n},{r}) = {resultado:,}$$")
            
            with st.expander("📖 Ver explicación paso a paso"):
                factores_str = ' \\times '.join([str(i) for i in range(n, n-r, -1)])
                
                st.markdown(f"""
                **Paso 1:** Expandir la fórmula
                - $P({n},{r}) = \\frac{{{n}!}}{{{n-r}!}}$
                
                **Paso 2:** Simplificar factoriales
                - ${n}! = {expandir_factorial(n)}$
                - ${n-r}! = {expandir_factorial(n-r)}$
                
                **Paso 3:** Cancelar términos comunes
                - $= {factores_str}$
                - $= {resultado:,}$
                
                **Interpretación:**
                - Para la primera posición: {n} opciones
                - Para la segunda: {n-1} opciones
                - Para la posición {r}: {n-r+1} opciones
                """)


    elif "Combinaciones con Repetición" in tecnica_calc:
            st.markdown("## 🍦 Combinaciones con Repetición")
            st.markdown("**Fórmula:** $$ C_r(n+r-1, r) = \\frac{(n+r-1)!}{r!(n-1)!}$$")
            
            col1, col2 = st.columns(2)
            with col1:
                n = st.number_input("n (tipos disponibles):", min_value=1, value=5, key="n_cr_calc")
            with col2:
                r = st.number_input("r (selecciones):", min_value=1, value=3, key="r_cr_calc")
            
            resultado = combinacion_repeticion(n, r)
            
            st.success(f"## Resultado: $$CR({n},{r}) = C({n+r-1},{r}) = {resultado:,}$$")
            
            with st.expander("📖 Ver explicación paso a paso"):
                st.markdown(f"""
                **Paso 1:** Transformar a combinación normal
                - $CR({n},{r}) = C({n}+{r}-1, {r})$
                - $= C({n+r-1}, {r})$
                
                **Paso 2:** Aplicar fórmula de combinación
                - $C({n+r-1},{r}) = \\frac{{({n+r-1})!}}{{{r}! \\times ({n-1})!}}$
                
                **Paso 3:** Calcular
                - $= {resultado:,}$
                
                **Interpretación:**
                Es como distribuir {r} elementos idénticos en {n} categorías diferentes.
                """)
        
    else:  # Combinaciones
        st.markdown("## 🎲 Combinaciones")
        st.markdown("**Fórmula:** $$C(n,r) = \\frac{n!}{r!(n-r)!}$$")
        
        col1, col2 = st.columns(2)
        with col1:
            n = st.number_input("n (elementos totales):", min_value=1, value=10, key="n_comb_calc")
        with col2:
            r = st.number_input("r (elementos a elegir):", min_value=1, value=4, key="r_comb_calc")
        
        if r > n:
            st.error("❌ Error: r no puede ser mayor que n")
        else:
            resultado = combinacion(n, r)
            resultado_perm = permutacion(n, r)
            
            st.success(f"## Resultado: $$C({n},{r}) = {resultado:,}$$")
            
            with st.expander("📖 Ver explicación paso a paso"):
                st.markdown(f"""
                **Paso 1:** Expandir la fórmula
                - $C({n},{r}) = \\frac{{{n}!}}{{{r}! \\times ({n-r})!}}$
                
                **Paso 2:** Calcular numerador (como Permutación)
                - $P({n},{r}) = {resultado_perm:,}$
                
                **Paso 3:** Dividir entre r! para eliminar orden
                - ${r}! = {factorial(r)}$
                - $\\frac{{{resultado_perm:,}}}{{{factorial(r)}}} = {resultado:,}$
                
                **Interpretación:**
                Hay {resultado_perm:,} formas ordenadas, pero como el orden NO importa,
                dividimos entre {factorial(r)} (formas de ordenar {r} elementos).
                """)

# --- PÁGINA 9: CUESTIONARIO FINAL ---

elif page == "9. ❓ Cuestionario Final":
    st.title("❓ Cuestionario Final de Evaluación")
    st.markdown("Evalúa tu comprensión completa del tema")
    st.markdown("---")
    
    # Preguntas del cuestionario
    preguntas = [
        {
            "pregunta": "¿Cuál es la diferencia clave entre Permutación y Combinación?",
            "opciones": [
                "La permutación permite repetición, la combinación no",
                "En la permutación importa el orden, en la combinación no",
                "La permutación es para números, la combinación para letras",
                "No hay diferencia, son lo mismo"
            ],
            "correcta": 1,
            "explicacion": "La diferencia clave es el ORDEN. En permutaciones el orden importa (ABC ≠ CBA), en combinaciones no ({A,B,C} = {C,B,A})."
        },
        {
            "pregunta": "Si debes elegir un comité de 3 personas de 8 disponibles, ¿qué técnica usas?",
            "opciones": [
                "Variaciones con repetición: 8³",
                "Permutaciones: P(8,3)",
                "Combinaciones: C(8,3)",
                "Combinaciones con repetición: CR(8,3)"
            ],
            "correcta": 2,
            "explicacion": "Es Combinación C(8,3) porque el orden NO importa (todos son miembros iguales del comité) y NO hay repetición."
        },
        {
            "pregunta": "¿Cuántas contraseñas de 4 dígitos (0-9) se pueden crear?",
            "opciones": [
                "10,000",
                "5,040",
                "210",
                "715"
            ],
            "correcta": 0,
            "explicacion": "Es Variación con repetición: 10⁴ = 10,000. Orden importa (1234 ≠ 4321) y hay repetición (1111 es válido)."
        },
        {
            "pregunta": "En el Baloto se eligen 6 números de 45. ¿Qué técnica se usa?",
            "opciones": [
                "P(45,6) - Permutación",
                "45⁶ - Variación con repetición",
                "C(45,6) - Combinación",
                "CR(45,6) - Combinación con repetición"
            ],
            "correcta": 2,
            "explicacion": "Es Combinación C(45,6) porque el orden NO importa (solo importa acertar los números) y NO hay repetición."
        },
        {
            "pregunta": "¿Cuándo usarías Combinaciones con Repetición?",
            "opciones": [
                "Para ordenar personas en una fila",
                "Para formar equipos sin líderes",
                "Para elegir helados donde puedes repetir sabor",
                "Para asignar cargos directivos"
            ],
            "correcta": 2,
            "explicacion": "CR se usa cuando el orden NO importa pero SÍ hay repetición. Ejemplo: elegir 3 helados de 5 sabores pudiendo repetir."
        },
        {
            "pregunta": "Si P(n,3) = 60, ¿cuál es el valor de n?",
            "opciones": [
                "n = 4",
                "n = 5",
                "n = 6",
                "n = 20"
            ],
            "correcta": 1,
            "explicacion": "P(5,3) = 5×4×3 = 60. Por lo tanto n = 5."
        },
        {
            "pregunta": "¿Cuál de estas situaciones requiere Permutación?",
            "opciones": [
                "Seleccionar 5 estudiantes para una excursión",
                "Asignar medallas de oro, plata y bronce",
                "Formar un comité de 4 personas",
                "Elegir 3 sabores de pizza"
            ],
            "correcta": 1,
            "explicacion": "Asignar medallas requiere Permutación porque el orden SÍ importa (oro ≠ bronce) y no hay repetición."
        },
        {
            "pregunta": "C(n,r) siempre es:",
            "opciones": [
                "Mayor que P(n,r)",
                "Menor o igual que P(n,r)",
                "Igual a n^r",
                "Igual a n!"
            ],
            "correcta": 1,
            "explicacion": "C(n,r) ≤ P(n,r) porque C(n,r) = P(n,r)/r!, es decir, la combinación elimina el orden dividiendo."
        },
        {
            "pregunta": "¿Qué representa el Principio Multiplicativo?",
            "opciones": [
                "La suma de todas las opciones",
                "El producto de las opciones en cada etapa",
                "La división de permutaciones entre combinaciones",
                "El factorial de n"
            ],
            "correcta": 1,
            "explicacion": "El Principio Multiplicativo dice que si hay n₁ opciones en etapa 1, n₂ en etapa 2, etc., el total es n₁ × n₂ × ..."
        },
        {
            "pregunta": "Si C(7,3) = 35, entonces C(7,4) es:",
            "opciones": [
                "35",
                "70",
                "21",
                "No se puede calcular"
            ],
            "correcta": 0,
            "explicacion": "Por simetría: C(n,r) = C(n,n-r). Entonces C(7,4) = C(7,3) = 35."
        }
    ]
    
    # Inicializar estado
    if 'respuestas_quiz' not in st.session_state:
        st.session_state.respuestas_quiz = {}
        st.session_state.quiz_enviado = False
    
    if not st.session_state.quiz_enviado:
        # Mostrar preguntas
        for i, q in enumerate(preguntas):
            st.markdown(f"### Pregunta {i+1}")
            st.markdown(f"**{q['pregunta']}**")
            
            respuesta = st.radio(
                "Selecciona tu respuesta:",
                q['opciones'],
                key=f"q_{i}",
                index=st.session_state.respuestas_quiz.get(i, 0)
            )
            
            st.session_state.respuestas_quiz[i] = q['opciones'].index(respuesta)
            st.markdown("---")
        
        # Botón enviar
        if st.button("📝 Enviar Cuestionario"):
            st.session_state.quiz_enviado = True
            st.rerun()
    
    else:
        # Mostrar resultados
        st.markdown("## 📊 Resultados del Cuestionario")
        
        correctas = 0
        for i, q in enumerate(preguntas):
            respuesta_usuario = st.session_state.respuestas_quiz.get(i, -1)
            es_correcta = (respuesta_usuario == q['correcta'])
            
            if es_correcta:
                correctas += 1
                st.success(f"✅ **Pregunta {i+1}:** Correcta")
            else:
                st.error(f"❌ **Pregunta {i+1}:** Incorrecta")
            
            st.markdown(f"**Pregunta:** {q['pregunta']}")
            st.markdown(f"**Tu respuesta:** {q['opciones'][respuesta_usuario]}")
            st.markdown(f"**Respuesta correcta:** {q['opciones'][q['correcta']]}")
            st.info(f"💡 {q['explicacion']}")
            st.markdown("---")
        
        # Puntaje final
        porcentaje = (correctas / len(preguntas)) * 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Correctas", f"{correctas}/{len(preguntas)}")
        with col2:
            st.metric("Porcentaje", f"{porcentaje:.1f}%")
        with col3:
            if porcentaje >= 80:
                st.metric("Calificación", "Excelente ⭐")
            elif porcentaje >= 60:
                st.metric("Calificación", "Aprobado ✓")
            else:
                st.metric("Calificación", "Revisar 📚")
        
        # Botón reiniciar
        if st.button("🔄 Reiniciar Cuestionario"):
            st.session_state.respuestas_quiz = {}
            st.session_state.quiz_enviado = False
            st.rerun()

# --- PÁGINA 10: TABLA DE REFERENCIA ---

elif page == "10. 📚 Tabla de Referencia":
    st.title("📚 Tabla de Referencia Rápida")
    st.markdown("Resumen completo de las 4 técnicas de conteo")
    st.markdown("---")
    
    st.markdown("## 🔍 Diagrama de Flujo de Decisión")
    
    st.code("""
    ┌─────────────────────────────────┐
    │  ¿Importa el ORDEN?             │
    └────────┬────────────────┬───────┘
             │                │
          ✅ SÍ            ❌ NO
             │                │
    ┌────────▼────────┐  ┌───▼────────────┐
    │ ¿Hay REPETICIÓN?│  │ ¿Hay REPETICIÓN?│
    └────┬────────┬───┘  └───┬─────────┬──┘
         │        │          │         │
      ✅ SÍ    ❌ NO      ✅ SÍ     ❌ NO
         │        │          │         │
    ┌────▼───┐ ┌─▼──────┐ ┌─▼─────────┐ ┌▼─────────┐
    │  n^r   │ │ P(n,r) │ │C_r(n+r-1,r│ │  C(n,r)  │
    └────────┘ └────────┘ └───────────┘ └──────────┘
    Variación  Permutación  Comb.Rep.  Combinación
    """)
    
    st.markdown("---")
    
    st.markdown("## 📊 Tabla Comparativa Completa")
    
    tabla_referencia = pd.DataFrame({
        "": ["ORDEN", "REPETICIÓN", "Fórmula", "Ejemplo Cotidiano", "Ejemplo Numérico"],
        "Variaciones con Repetición": ["✅ Importa", "✅ Permitida", "$n^r$", "Contraseña PIN", "$10^4 = 10,000$"],
        "Permutaciones": ["✅ Importa", "❌ NO permitida", "$\\frac{n!}{(n-r)!}$", "Podio deportivo", "$P(10,3) = 720$"],
        "Combinaciones": ["❌ NO importa", "❌ NO permitida", "$\\frac{n!}{r!(n-r)!}$", "Baloto/Lotería", "$C(43,6) = 6,096,454$"],
        "Comb. con Repetición": ["❌ NO importa", "✅ Permitida", "$CR(n,r) = C(n+r-1,r)$", "Helados con repetición", "$CR(5,3) = 35$"]
    })
    
    st.dataframe(tabla_referencia, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.markdown("## 🎯 Ejemplos por Área Profesional")
    
    tab_psi, tab_adm, tab_med, tab_mus = st.tabs(["🧠 Psicología", "💼 Administración", "🏥 Medicina", "🎵 Música"])
    
    with tab_psi:
        st.markdown("""
        ### 🧠 Psicología
        
        **Variaciones con Repetición:**
        - Respuestas en escala Likert (5 preguntas, 5 opciones c/u)
        
        **Permutaciones:**
        - Orden de aplicación de 3 tests de 8 disponibles
        
        **Combinaciones:**
        - Seleccionar 3 tests de 8 para una batería
        
        **Comb. con Repetición:**
        - Pacientes pueden repetir en diferentes grupos de terapia
        """)
    
    with tab_adm:
        st.markdown("""
        ### 💼 Administración
        
        **Variaciones con Repetición:**
        - Códigos de empleado (2 letras + 4 dígitos)
        
        **Permutaciones:**
        - Asignar 3 cargos (Gerente, Sub, Coord) de 8 candidatos
        
        **Combinaciones:**
        - Formar comité de 4 personas de 10 empleados
        
        **Comb. con Repetición:**
        - Seleccionar productos para promoción (pueden repetir categoría)
        """)
    
    with tab_med:
        st.markdown("""
        ### 🏥 Medicina
        
        **Variaciones con Repetición:**
        - Códigos de historia clínica (3 letras + 5 dígitos)
        
        **Permutaciones:**
        - Rotación médica por 3 especialidades de 8 disponibles
        
        **Combinaciones:**
        - Seleccionar 5 pacientes de 20 para ensayo clínico
        
        **Comb. con Repetición:**
        - Distribución de dosis (pueden repetirse medicamentos)
        """)
    
    with tab_mus:
        st.markdown("""
        ### 🎵 Música
        
        **Variaciones con Repetición:**
        - Melodía de 4 notas de 7 disponibles (pueden repetirse)
        
        **Permutaciones:**
        - Orden de 5 piezas de 10 para concierto
        
        **Combinaciones:**
        - Formar cuarteto de 4 músicos de 9 disponibles
        
        **Comb. con Repetición:**
        - Acorde de 3 notas de 12 cromáticas (pueden repetirse)
        """)
    
    st.markdown("---")
    
    
    st.markdown("## 🧮 Fórmulas con Notación Alternativa")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Notación Estándar
        
        **Variaciones con Repetición:**
        $$n^r$$
        
        **Permutaciones:**
        $$P(n,r) = \\frac{n!}{(n-r)!}$$
        
        **Combinaciones:**
        $$C(n,r) = \\frac{n!}{r!(n-r)!}$$
        
        **Comb. con Repetición:**
        $$C_r(n+r-1,r)=\\frac{(n+r-1)!}{r!(n-1)!}$$
        """)
    
    with col2:
        st.markdown("""
        ### Notación Alternativa
        
        **Variaciones con Repetición:**
        $$VR_{n,r} = n^r$$
        
        **Permutaciones:**
        $$_nP_r = P_r^n = \\frac{n!}{(n-r)!}$$
        
        **Combinaciones:**
        $$_nC_r = \\binom{n}{r} = \\frac{n!}{r!(n-r)!}$$
        
        **Comb. con Repetición:**
        $$CR_{n,r} = \\binom{n+r-1}{r}$$
        """)
    
    st.markdown("---")
    
    st.markdown("## 💡 Consejos para NO Confundirte")
    
    st.success("""
    ### ✅ Tips Clave:
    
    1. **Primero pregunta:** ¿Importa el orden? (Esto divide en 2 grupos)
    2. **Luego pregunta:** ¿Hay repetición? (Esto define la técnica exacta)
    3. **Combinación siempre ≤ Permutación** (porque elimina el orden)
    4. **Repetición aumenta las opciones** (más posibilidades)
    5. **n^r es la más simple** (solo multiplicar)
    6. **Si ves factorial (!), NO es variación con repetición**
    7. **Baloto/Lotería = Combinación** (99% de los casos)
    8. **Contraseñas = Variación con repetición** (casi siempre)
    9. **Podio/Ranking = Permutación** (el orden importa)
    10. **Comité/Grupo = Combinación** (el orden NO importa)
    """)
    
    st.markdown("---")
    
    st.markdown("## 📖 Recursos Adicionales")
    
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        st.info("""
        ### 📚 Para Profundizar:
        - Triángulo de Pascal
        - Teorema del Binomio
        - Principio de Inclusión-Exclusión
        - Permutaciones Circulares
        - Permutaciones con Repetición
        """)
    
    with col_rec2:
        st.info("""
        ### 🎯 Aplicaciones:
        - Probabilidad (siguiente tema)
        - Teoría de Grafos
        - Criptografía
        - Análisis de Algoritmos
        - Estadística Inferencial
        """)
    
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 14px;color: #424242;">
Desarrollado con 💙 para estudiantes de Uninorte<br>
¿Dudas o sugerencias? Escribe a <a href="mailto:carlosdl@uninorte.edu.co">carlosdl@uninorte.edu.co</a>
</div>

""", unsafe_allow_html=True)

# --- FIN DEL CÓDIGO ---
