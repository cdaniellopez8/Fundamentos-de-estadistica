import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Configuración inicial
st.set_page_config(page_title="Conceptos Básicos de Estadística", page_icon="📈", layout="centered")

st.title("📈 Conceptos y Definiciones Básicas de Estadística")

st.markdown(
    """
    <div style="
        text-align: justify;
        font-size: 16px;
        line-height: 1.6;
        max-width: 900px;
        margin: 0 auto;
    ">

    <p>
    Bienvenido a este cuestionario <strong>interactivo y educativo</strong> diseñado para que comprendas 
    los <strong>conceptos fundamentales de la estadística</strong>: qué es, para qué sirve, y cuáles son 
    sus elementos básicos como <strong>población, muestra, parámetro y estadístico</strong>.
    </p>

    <p>
    Este recurso te ayudará a <strong>construir bases sólidas</strong> para tu aprendizaje en estadística, 
    preparándote para temas más avanzados y para aplicar estos conocimientos en <strong>cualquier disciplina</strong>, 
    desde las ciencias exactas hasta las ciencias sociales.
    </p>

    <p>
    A través de preguntas prácticas con <strong>retroalimentación inmediata</strong>, aprenderás a distinguir 
    conceptos clave y a comprender por qué la estadística es una herramienta universal de análisis.
    </p>

    <p>
    Al responder, recibirás <strong>explicaciones detalladas</strong> que reforzarán tu comprensión, 
    junto con ejemplos visuales cuando sea apropiado.
    </p>

    <p>
    Al final, descubrirás datos curiosos sobre la <strong>historia de la estadística</strong> y un 
    <strong>mapa de ruta</strong> de lo que aprenderás en tus cursos. 
    </p>

    <p>
    Si tienes dudas o comentarios, escríbeme a 
    <a href="mailto:carlosdl@uninorte.edu.co">carlosdl@uninorte.edu.co</a>.
    </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# --- Función general de pregunta ---
def pregunta(
    texto_pregunta, 
    opciones, 
    correcta, 
    explicacion_bien, 
    explicacion_mal,
    mostrar_grafico=False,
    tipo_grafico=None
):
    st.markdown(f"### ❓ {texto_pregunta}")

    respuesta = st.radio("Selecciona una respuesta:", [""] + opciones, index=0, 
                        key=texto_pregunta, label_visibility="collapsed")

    if respuesta != "":
        if respuesta == correcta:
            st.success(f"✅ ¡Correcto! {explicacion_bien}")

            # Mostrar gráfico si corresponde
            if mostrar_grafico and tipo_grafico:
                
                if tipo_grafico == "poblacion_muestra":
                    # Visualización mejorada: círculo grande con círculo pequeño extraído
                    fig, ax = plt.subplots(figsize=(10, 8))
                    ax.set_xlim(0, 10)
                    ax.set_ylim(0, 10)
                    ax.axis('off')
                    
                    # Círculo grande (población)
                    circle_poblacion = plt.Circle((3.5, 5), 2.5, color='#3498db', alpha=0.3, linewidth=3, edgecolor='#2980b9')
                    ax.add_patch(circle_poblacion)
                    ax.text(3.5, 5, 'POBLACIÓN\n(Todos los elementos\nde interés)', 
                           ha='center', va='center', fontsize=13, fontweight='bold', color='#2c3e50')
                    
                    # Círculo pequeño (muestra) - dentro del grande
                    circle_muestra_dentro = plt.Circle((4.5, 6), 0.8, color='#e74c3c', alpha=0.5, 
                                                       linewidth=2, edgecolor='#c0392b')
                    ax.add_patch(circle_muestra_dentro)
                    
                    # Flecha indicando extracción
                    ax.annotate('', xy=(7.5, 6), xytext=(5.3, 6),
                               arrowprops=dict(arrowstyle='->', lw=3, color='#e74c3c'))
                    
                    # Círculo pequeño (muestra) - extraído
                    circle_muestra = plt.Circle((8.2, 6), 0.8, color='#e74c3c', alpha=0.7, 
                                               linewidth=3, edgecolor='#c0392b')
                    ax.add_patch(circle_muestra)
                    ax.text(8.2, 6, 'MUESTRA\n(Subconjunto\nrepresentativo)', 
                           ha='center', va='center', fontsize=8, fontweight='bold', color='white')
                    
                    # Etiquetas
                    ax.text(3.5, 1.5, 'N = Tamaño de la población', ha='center', fontsize=11, 
                           style='italic', color='#2980b9')
                    ax.text(8.2, 4.5, 'n = Tamaño de la muestra', ha='center', fontsize=11, 
                           style='italic', color='#c0392b')
                    
                    ax.set_title('Relación entre Población y Muestra', fontsize=15, fontweight='bold', pad=20)
                    st.pyplot(fig)

                elif tipo_grafico == "parametro_estadistico_ingresos":
                    st.markdown("📊 **Este gráfico se llama HISTOGRAMA** y muestra la distribución de una variable numérica.")
                    
                    # Comparación visual con datos de ingresos
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
                    
                    # Población completa - Ingresos
                    np.random.seed(42)
                    poblacion_datos = np.random.gamma(3, 950000, 10000)  # Distribución de ingresos más realista
                    media_poblacion = poblacion_datos.mean()
                    
                    ax1.hist(poblacion_datos, bins=40, color='#3498db', alpha=0.7, edgecolor='black')
                    ax1.axvline(media_poblacion, color='red', linestyle='--', linewidth=3, 
                               label=f'μ (parámetro) = ${media_poblacion:,.0f}')
                    ax1.set_title('POBLACIÓN COMPLETA\n(Todos los hogares de Barranquilla)', fontweight='bold', fontsize=12)
                    ax1.set_xlabel('Ingreso mensual (pesos)', fontsize=10)
                    ax1.set_ylabel('Frecuencia (número de hogares)', fontsize=10)
                    ax1.legend(fontsize=10)
                    ax1.grid(alpha=0.3)
                    
                    # Muestra - Ingresos
                    muestra_datos = np.random.choice(poblacion_datos, 500)
                    media_muestra = muestra_datos.mean()
                    
                    ax2.hist(muestra_datos, bins=25, color='#e74c3c', alpha=0.7, edgecolor='black')
                    ax2.axvline(media_muestra, color='darkred', linestyle='--', linewidth=3,
                               label=f'x̄ (estadístico) = ${media_muestra:,.0f}')
                    ax2.set_title('MUESTRA\n(500 hogares encuestados)', fontweight='bold', fontsize=12)
                    ax2.set_xlabel('Ingreso mensual (pesos)', fontsize=10)
                    ax2.set_ylabel('Frecuencia (número de hogares)', fontsize=10)
                    ax2.legend(fontsize=10)
                    ax2.grid(alpha=0.3)
                    
                    plt.tight_layout()
                    st.pyplot(fig)

                elif tipo_grafico == "parametro_estadistico_presion":
                    st.markdown("📊 **Este gráfico se llama HISTOGRAMA** y muestra la distribución de una variable numérica.")
                    
                    # Comparación visual con datos de presión arterial
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
                    
                    # Población completa - Presión arterial
                    np.random.seed(42)
                    # Presión arterial sistólica de pacientes hipertensos (140-180 mmHg típicamente)
                    poblacion_datos = np.random.normal(155, 15, 5000)
                    media_poblacion = poblacion_datos.mean()
                    
                    ax1.hist(poblacion_datos, bins=35, color='#3498db', alpha=0.7, edgecolor='black')
                    ax1.axvline(media_poblacion, color='red', linestyle='--', linewidth=3, 
                               label=f'μ (parámetro) = {media_poblacion:.1f} mmHg')
                    ax1.set_title('POBLACIÓN COMPLETA\n(Todos los pacientes hipertensos en Colombia)', 
                                 fontweight='bold', fontsize=11)
                    ax1.set_xlabel('Presión arterial sistólica (mmHg)', fontsize=10)
                    ax1.set_ylabel('Frecuencia (número de pacientes)', fontsize=10)
                    ax1.legend(fontsize=10)
                    ax1.grid(alpha=0.3)
                    
                    # Muestra - Presión arterial
                    muestra_datos = np.random.choice(poblacion_datos, 250)
                    media_muestra = muestra_datos.mean()
                    
                    ax2.hist(muestra_datos, bins=20, color='#e74c3c', alpha=0.7, edgecolor='black')
                    ax2.axvline(media_muestra, color='darkred', linestyle='--', linewidth=3,
                               label=f'x̄ (estadístico) = {media_muestra:.1f} mmHg')
                    ax2.set_title('MUESTRA\n(250 pacientes del estudio)', fontweight='bold', fontsize=11)
                    ax2.set_xlabel('Presión arterial sistólica (mmHg)', fontsize=10)
                    ax2.set_ylabel('Frecuencia (número de pacientes)', fontsize=10)
                    ax2.legend(fontsize=10)
                    ax2.grid(alpha=0.3)
                    
                    plt.tight_layout()
                    st.pyplot(fig)

                elif tipo_grafico == "descriptiva_inferencial":
                    # Ilustración del proceso inferencial
                    fig = plt.figure(figsize=(10, 6))
                    ax = fig.add_subplot(111)
                    ax.axis('off')
                    
                    # Población
                    circle1 = plt.Circle((0.25, 0.5), 0.15, color='#3498db', alpha=0.3)
                    ax.add_patch(circle1)
                    ax.text(0.25, 0.5, 'POBLACIÓN\n(Desconocida)', 
                           ha='center', va='center', fontsize=11, fontweight='bold')
                    
                    # Flecha de muestreo
                    ax.annotate('', xy=(0.45, 0.5), xytext=(0.4, 0.5),
                               arrowprops=dict(arrowstyle='->', lw=2, color='black'))
                    ax.text(0.425, 0.55, 'Muestreo', ha='center', fontsize=9)
                    
                    # Muestra
                    circle2 = plt.Circle((0.55, 0.5), 0.08, color='#e74c3c', alpha=0.5)
                    ax.add_patch(circle2)
                    ax.text(0.55, 0.5, 'Muestra', ha='center', va='center', 
                           fontsize=10, fontweight='bold')
                    
                    # Flecha de análisis
                    ax.annotate('', xy=(0.7, 0.5), xytext=(0.63, 0.5),
                               arrowprops=dict(arrowstyle='->', lw=2, color='black'))
                    ax.text(0.665, 0.55, 'Análisis', ha='center', fontsize=9)
                    
                    # Resultados
                    rect = plt.Rectangle((0.7, 0.4), 0.2, 0.2, 
                                        fill=True, facecolor='#2ecc71', alpha=0.3, edgecolor='black')
                    ax.add_patch(rect)
                    ax.text(0.8, 0.5, 'Estadística\nDescriptiva', 
                           ha='center', va='center', fontsize=10, fontweight='bold')
                    
                    # Flecha de inferencia
                    ax.annotate('', xy=(0.25, 0.3), xytext=(0.75, 0.35),
                               arrowprops=dict(arrowstyle='->', lw=3, color='#9b59b6', linestyle='dashed'))
                    ax.text(0.5, 0.25, 'INFERENCIA\n(Generalización)', 
                           ha='center', fontsize=11, fontweight='bold', color='#9b59b6')
                    
                    ax.set_xlim(0, 1)
                    ax.set_ylim(0, 1)
                    ax.set_title('Estadística Descriptiva vs Inferencial', 
                               fontsize=14, fontweight='bold', pad=20)
                    st.pyplot(fig)

        else:
            st.error(f"❌ Incorrecto. {explicacion_mal}")



# --------------------
# PREGUNTAS
# --------------------

pregunta(
    "1️⃣ ¿Qué es la estadística?",
    [
        "Una ciencia que estudia los números grandes en la industria",
        "Una ciencia que recolecta, organiza, analiza e interpreta datos para tomar decisiones",
        "Un método para hacer encuestas y obtener probabilidades",
        "Una técnica exclusiva de las matemáticas"
    ],
    "Una ciencia que recolecta, organiza, analiza e interpreta datos para tomar decisiones",
    """La estadística es una **ciencia formal** que nos permite transformar datos en información útil. 
    No solo cuenta o suma, sino que **interpreta patrones** y ayuda a tomar **decisiones informadas** 
    en contextos de incertidumbre. Es aplicable a todas las áreas del conocimiento.""",
    """La estadística va mucho más allá de solo hacer encuestas o trabajar con números. 
    Es una **metodología científica completa** que incluye diseño de estudios, recolección, 
    análisis e interpretación de datos para resolver problemas reales."""
)

pregunta(
    "2️⃣ ¿Qué es una población en estadística?",
    [
        "Las personas que viven en un determinado territorio",
        "Una muestra representativa de todos los elementos de interés en un estudio",
        "El conjunto completo de todos los elementos de interés en un estudio",
        "Todos los datos que recolectamos en un estudio"
    ],
    "El conjunto completo de todos los elementos de interés en un estudio",
    """¡Exacto! La **población** (denotada como **N**) es el **conjunto total** de elementos que queremos estudiar. 
    Pueden ser personas, animales, objetos, empresas, eventos, etc. Por ejemplo: todos los estudiantes de una 
    universidad, todas las empresas de un sector, o todos los pacientes con cierta condición.""",
    """La población no se refiere solo a personas. En estadística, es el **conjunto completo** de todos los 
    elementos (personas, objetos, eventos) sobre los cuales queremos obtener conclusiones. Una muestra, 
    en cambio, es solo una parte de esa población.""",
    mostrar_grafico=True,
    tipo_grafico="poblacion_muestra"
)

pregunta(
    "3️⃣ ¿Qué es una muestra en estadística?",
    [
        "Toda la población de estudio",
        "Los datos más importantes de un estudio",
        "Una técnica de análisis estadística",
        "Un subconjunto representativo de la población"
    ],
    "Un subconjunto representativo de la población",
    """¡Correcto! Una **muestra** (denotada como **n**) es un **subconjunto** de la población que seleccionamos 
    para estudiar. Debe ser **representativa** para que las conclusiones sean válidas. Por ejemplo: si queremos 
    saber la estatura promedio de los estudiantes de una universidad (población), podemos medir solo a 200 estudiantes 
    (muestra) seleccionados adecuadamente.""",
    """Una muestra no es toda la población ni solo los "datos importantes". Es un **subconjunto seleccionado** 
    de forma que represente fielmente las características de la población completa, permitiéndonos hacer inferencias 
    sin tener que estudiar a todos."""
)

pregunta(
    "4️⃣ ¿Qué es un parámetro en estadística?",
    [
        "Una medida cualquiera calculada en una muestra",
        "Una medida cualquiera calculada en la población completa",
        "Un tipo de variable a la hora de estudiar estadística",
        "Un método estadístico para llegar a conclusiones verdaderas"
    ],
    "Una medida cualquiera calculada en la población completa",
    """¡Perfecto! Un **parámetro** es una medida que describe una característica de la **población completa**. 
    Se denota con letras griegas: **μ** (mu) para la media poblacional, **σ** (sigma) para la desviación estándar poblacional, 
    **π** (pi) para la proporción poblacional. Generalmente **no conocemos los parámetros** (son desconocidos) y los estimamos 
    mediante estadísticos de muestras.""",
    """Un parámetro no se calcula en una muestra (eso sería un estadístico), sino que describe a **toda la población**. 
    Como casi nunca podemos estudiar a toda la población, los parámetros suelen ser **valores desconocidos** que intentamos estimar."""
)

pregunta(
    "5️⃣ ¿Qué es un estadístico?",
    [
        "Una medida cualquiera calculada en la población completa",
        "Una medida descriptiva calculada a partir de una muestra",
        "Los datos que obtengo en un muestreo para ser analizados",
        "Un tipo de gráfico utilizado en la estadística"
    ],
    "Una medida descriptiva calculada a partir de una muestra",
    """¡Excelente! Un **estadístico** es una medida calculada a partir de los datos de una **muestra**. 
    Se denota con letras latinas: **x̄** (equis barra) para la media muestral, **s** para la desviación estándar muestral, 
    **p** para la proporción muestral. Los estadísticos son **valores conocidos** que calculamos y usamos para **estimar** 
    los parámetros poblacionales desconocidos.""",
    """Un estadístico no describe a toda la población (eso es un parámetro), sino que es un **valor calculado** 
    a partir de datos de una muestra. Es nuestra "mejor estimación" del parámetro poblacional que no conocemos."""
)

# --- CASO DE ESTUDIO 1: Identificar parámetro ---
st.markdown("---")
st.markdown("""
<div style="background-color: #fff3cd; padding: 20px; border-radius: 10px; border-left: 5px solid #ffc107; color: #424242;">

### 📋 **Caso de Estudio 1**

Un investigador desea conocer el **ingreso promedio mensual** de todos los hogares en la ciudad de Barranquilla. 
Para ello, selecciona aleatoriamente 500 hogares y registra sus ingresos mensuales. Con estos datos, calcula 
que el **ingreso promedio de los 500 hogares encuestados** es de $2,850,000 pesos.

</div>
""", unsafe_allow_html=True)

pregunta(
    "6️⃣ En este estudio, ¿cuál es el **parámetro** de interés?",
    [
        "El ingreso promedio de los 500 hogares encuestados ($2,850,000)",
        "El ingreso promedio mensual de todos los hogares de Barranquilla",
        "Los 500 hogares seleccionados",
        "El método de selección aleatoria utilizado"
    ],
    "El ingreso promedio mensual de todos los hogares de Barranquilla",
    """¡Correcto! El **parámetro de interés** es el **ingreso promedio mensual de TODOS los hogares de Barranquilla** (μ). 
    Este valor describe a la **población completa** y es lo que realmente queremos conocer. Como no podemos encuestar a todos 
    los hogares, tomamos una muestra para estimarlo. El parámetro es **desconocido** y es nuestro objetivo de estudio. 
    Recuerda: los parámetros siempre se refieren a la población completa, no a la muestra.""",
    """Recuerda que un **parámetro** siempre describe a la **población completa**, no a la muestra. En este caso, 
    el investigador quiere conocer el ingreso promedio de TODOS los hogares de Barranquilla (población), no solo 
    de los 500 que encuestó (muestra). El valor de $2,850,000 es un estadístico (calculado de la muestra), no el parámetro.""",
    mostrar_grafico=True,
    tipo_grafico="parametro_estadistico_ingresos"
)

pregunta(
    "7️⃣ En el mismo estudio, ¿cuál es el estadístico?",
    [
        "Todos los hogares de Barranquilla",
        "Los 500 hogares seleccionados",
        "El ingreso promedio de los 500 hogares encuestados ($2,850,000)",
        "El ingreso promedio de todos los hogares de Barranquilla"
    ],
    "El ingreso promedio de los 500 hogares encuestados ($2,850,000)",
    """¡Excelente! El **estadístico** es el **ingreso promedio de los 500 hogares encuestados: $2,850,000** (x̄). 
    Este valor fue **calculado a partir de la muestra** y es un dato **conocido**. Lo usamos como nuestra mejor 
    **estimación** del parámetro poblacional desconocido (el verdadero ingreso promedio de todos los hogares de Barranquilla). 
    El estadístico es nuestra "ventana" hacia el parámetro que queremos conocer pero no podemos medir directamente.""",
    """El **estadístico** es la medida que **calculamos** a partir de los datos de la **muestra**, no de la población completa. 
    En este caso, el promedio de $2,850,000 fue calculado con los datos de los 500 hogares encuestados (muestra). 
    Los hogares en sí no son estadísticos, son las unidades de análisis. El promedio de TODOS los hogares de Barranquilla 
    sería el parámetro (que no conocemos)."""
)

# --- CASO DE ESTUDIO 2: Identificar población, muestra, parámetro y estadístico ---
st.markdown("---")
st.markdown("""
<div style="background-color: #d1ecf1; padding: 20px; border-radius: 10px; border-left: 5px solid #17a2b8; color: #424242;">

### 📋 **Caso de Estudio 2**

Una empresa farmacéutica desarrolla un nuevo medicamento para reducir la hipertensión. Para evaluar su efectividad, 
selecciona aleatoriamente a **250 pacientes diagnosticados con hipertensión** de diferentes clínicas en Colombia. 
Después del tratamiento, se observa que el 78% de estos 250 pacientes logró reducir su presión arterial a niveles normales. 
La empresa quiere determinar **la proporción real de todos los pacientes hipertensos en Colombia** que se beneficiarían 
del medicamento.

</div>
""", unsafe_allow_html=True)

pregunta(
    "8️⃣ En este estudio, ¿cuál es la población?",
    [   
        "Todos los pacientes con hipertensión en Colombia",
        "Los 250 pacientes seleccionados para el estudio",
        "El 78% de los pacientes que mejoraron",
        "Las clínicas donde se realizó el estudio"
    ],
    "Todos los pacientes con hipertensión en Colombia",
    """¡Correcto! La **población** son **todos los pacientes con hipertensión en Colombia**. Esta es la totalidad de individuos 
    sobre los cuales se quiere obtener conclusiones. La empresa farmacéutica no puede probar el medicamento en absolutamente 
    todos estos pacientes (sería imposible y costoso), por eso selecciona una muestra representativa. La población define 
    el alcance de nuestras conclusiones.""",
    """La **población** es el conjunto **completo** de elementos sobre los que queremos obtener conclusiones. En este caso, 
    la empresa quiere saber sobre TODOS los pacientes hipertensos de Colombia, no solo sobre los 250 del estudio (esos son la muestra). 
    Las clínicas son lugares, no la población de interés."""
)

pregunta(
    "9️⃣ En el mismo estudio, ¿cuál es el parámetro de interés?",
    [
        "El 78% de los 250 pacientes que mejoraron",
        "La proporción real de pacientes hipertensos en Colombia que se beneficiarían del medicamento",
        "Los 250 pacientes seleccionados para el estudio",
        "El número total de pacientes con hipertensión en Colombia"
    ],
    "La proporción real de pacientes hipertensos en Colombia que se beneficiarían del medicamento",
    """¡Perfecto! El **parámetro de interés** es la **proporción real (π) de TODOS los pacientes hipertensos en Colombia 
    que se beneficiarían del medicamento**. Este es el valor que la empresa realmente quiere conocer pero que es imposible 
    medir directamente (tendría que tratar a todos los pacientes del país). Por eso usan el 78% observado en la muestra 
    como su mejor **estimación** de este parámetro desconocido. El parámetro es poblacional, desconocido y es nuestro objetivo.""",
    """El **parámetro** siempre se refiere a la **población completa**, no a la muestra. El 78% es el resultado en los 250 pacientes 
    (un estadístico), pero lo que realmente se busca conocer es qué porcentaje de TODOS los pacientes hipertensos en Colombia 
    se beneficiaría (el parámetro). Este valor poblacional es desconocido y se estima con el estadístico muestral.""",
    mostrar_grafico=True,
    tipo_grafico="parametro_estadistico_presion"
)

pregunta(
    "🔟 ¿Cuál es la diferencia entre estadística descriptiva e inferencial?",
    [
        "No hay diferencia, son igual de aburridas",
        "Descriptiva resume datos; inferencial hace generalizaciones a partir de muestras",
        "Descriptiva usa gráficos; inferencial usa números",
        "Descriptiva es fácil; inferencial es difícil"
    ],
    "Descriptiva resume datos; inferencial hace generalizaciones a partir de muestras",
    """¡Correcto! La **estadística descriptiva** organiza, resume y presenta datos usando tablas, gráficos y medidas 
    (media, mediana, desviación estándar). La **estadística inferencial** va más allá: usa datos de una muestra para 
    hacer **generalizaciones, predicciones y pruebas de hipótesis** sobre la población completa, considerando la incertidumbre.""",
    """Ambas ramas de la estadística son importantes pero diferentes. La descriptiva nos dice "qué pasó en nuestros datos", 
    mientras que la inferencial nos permite decir "qué podemos concluir sobre la población completa a partir de nuestra muestra".""",
    mostrar_grafico=True,
    tipo_grafico="descriptiva_inferencial"
)

pregunta(
    "1️⃣1️⃣ ¿Qué es un censo?",
    [
        "Una muestra muy grande pero no tan grande como la población",
        "Una encuesta exclusiva realizada de forma no presencial donde se pueden responder muchas preguntas",
        "Un tipo de experimento aleatorio donde se miden probabilidades de ocurrencia de eventos",
        "El estudio de toda la población sin excepción"
    ],
    "El estudio de toda la población sin excepción",
    """¡Exacto! Un **censo** es el estudio de **todos y cada uno** de los elementos de una población. 
    Es completo y exacto, pero suele ser **costoso, lento y a veces imposible** de realizar. Ejemplos: 
    el censo nacional de población que se hace cada década, o el inventario completo de productos en una bodega pequeña.""",
    """Un censo no es una muestra grande, sino el estudio del **100% de la población**. Aunque es preciso, 
    en la mayoría de casos prácticos es más eficiente usar muestreo bien diseñado que logra resultados muy precisos 
    con menor costo y tiempo."""
)

pregunta(
    "1️⃣2️⃣ ¿Por qué es útil la estadística en carreras que 'no trabajan con números'?",
    [
        "Realmente no es tan útil, solo sirve para 'carreras que usan números'",
        "Porque permite analizar patrones en comportamientos, opiniones y fenómenos sociales de manera objetiva y fundamentada",
        "Para hacer gráficos bonitos para mis articulos :)",
        "La verdad solo quiero aprobar el curso para avanzar en mi carrera"
    ],
    "Porque permite analizar patrones en comportamientos, opiniones y fenómenos sociales de manera objetiva y fundamentada",
    """¡Perfecto! La estadística es fundamental en **ciencias sociales y humanidades** porque permite: 
    (1) **Validar teorías** con evidencia empírica, (2) **Identificar patrones** en comportamientos o fenómenos sociales, 
    (3) **Tomar decisiones informadas** en políticas públicas, (4) **Evitar sesgos** personales mediante análisis objetivos, 
    (5) **Cuantificar lo cualitativo** (opiniones, actitudes, percepciones). Por ejemplo: analizar el impacto de una 
    intervención social, estudiar tendencias en salud mental, o evaluar la efectividad de campañas de comunicación.""",
    """La estadística no es solo para matemáticos o ingenieros. Es una **herramienta universal** que ayuda a cualquier 
    profesional a comprender mejor su campo, respaldar argumentos con datos, y tomar decisiones basadas en evidencia, 
    no en intuiciones."""
)



# ---------------------
# SECCIÓN DE CURIOSIDADES
# ---------------------
st.divider()
st.markdown("## 🎓 ¿Sabías que...? Historia de la Estadística")

st.markdown("""
<div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; border-left: 5px solid #3498db; color: #424242;">

### 📜 **¿Por qué se llama "Estadística"?**

La palabra **"estadística"** proviene del latín **"status"** (estado). Originalmente se refería a la 
**recopilación de datos sobre el Estado**: población, recursos, impuestos, ejércitos.

En el siglo XVIII, los gobiernos europeos comenzaron a recopilar sistemáticamente información para 
administrar mejor sus territorios. Así nació la estadística como **ciencia del Estado**.

### 🌟 **Momentos clave en la historia:**

- **Antigüedad**: Los egipcios y romanos realizaban censos para cobrar impuestos y reclutar soldados.

- **Siglo XVII**: John Graunt (1620-1674) analiza registros de mortalidad en Londres, considerado el 
  primer estadístico moderno.

- **Siglo XVIII**: Se desarrolla la teoría de la probabilidad. Thomas Bayes formula su famoso teorema.

- **Siglo XIX**: Florence Nightingale usa gráficos estadísticos para mejorar la sanidad hospitalaria. 
  Karl Pearson y Ronald Fisher desarrollan métodos fundamentales que aún usamos hoy.

- **Siglo XX-XXI**: Con las computadoras, la estadística se democratiza. Hoy es la base del 
  **Big Data**, **Machine Learning** e **Inteligencia Artificial**.

</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------------
# ROAD MAP
# ---------------------
st.markdown("## 🗺️ Road Map: Tu viaje por la Estadística")

st.markdown("""
### 📊 **Estadística Descriptiva (Estadística I)**
Este es tu punto de partida. Aquí aprenderás a:

- **Organizar y visualizar datos**: tablas de frecuencias, histogramas, gráficos de barras, boxplots
- **Calcular medidas descriptivas**: 
  - *Tendencia central*: media, mediana, moda
  - *Dispersión*: rango, varianza, desviación estándar
  - *Posición*: percentiles, cuartiles
- **Entender distribuciones**: formas, simetría, valores atípicos
- **Explorar relaciones**: correlación, tablas de contingencia

**Objetivo**: Describir "¿qué pasó?" con los datos que tenemos.

---

### 🔬 **Estadística Inferencial (Estadística II)**
Aquí das el salto de describir a **generalizar y predecir**. Aprenderás:

- **Probabilidad**: fundamentos teóricos para entender la incertidumbre
- **Distribuciones de probabilidad**: normal, t-Student, chi-cuadrado
- **Estimación**: intervalos de confianza para medias, proporciones
- **Pruebas de hipótesis**: ¿es real la diferencia o es solo azar?
  - Pruebas t, ANOVA, chi-cuadrado, correlación
- **Regresión**: modelar y predecir relaciones entre variables

**Objetivo**: Responder "¿qué podemos concluir sobre la población?" y "¿qué pasará en el futuro?"

---

### 🌍 **¿Por qué es importante para TODAS las carreras?**

La estadística es una **competencia transversal** esencial en el siglo XXI:

#### 🏥 **Ciencias de la Salud**
- Evaluar efectividad de tratamientos
- Identificar factores de riesgo
- Tomar decisiones clínicas basadas en evidencia

#### 🧠 **Psicología y Ciencias Sociales**
- Validar instrumentos de medición
- Analizar comportamientos y actitudes
- Diseñar y evaluar intervenciones

#### 📢 **Comunicación y Marketing**
- Medir impacto de campañas
- Segmentar audiencias
- Analizar tendencias en redes sociales

#### ⚖️ **Derecho y Políticas Públicas**
- Interpretar evidencia pericial
- Evaluar políticas sociales
- Analizar datos criminológicos

#### 🎨 **Artes y Humanidades**
- Estudios de recepción de obras
- Análisis de tendencias culturales
- Investigación de públicos

#### 💼 **Administración y Economía**
- Análisis de mercados
- Pronósticos financieros
- Control de calidad

### 💡 **La estadística te permite:**
✅ Tomar decisiones informadas basadas en datos, no en intuiciones  
✅ Detectar patrones ocultos en información compleja  
✅ Evaluar críticamente estudios y noticias que citan "datos"  
✅ Comunicar hallazgos de forma clara y convincente  
✅ Ser un profesional más competitivo en cualquier campo  

---

> 💬 **En resumen**: La estadística no es solo "hacer cuentas". Es una **forma de pensar** 
> que te permite navegar en un mundo lleno de información, incertidumbre y decisiones importantes. 
> Es el lenguaje universal de la ciencia y la toma de decisiones del siglo XXI.

""")

st.divider()

st.markdown("""
<div style="background-color: #e8f5e9; padding: 15px; border-radius: 10px; text-align: center;color: #424242;">

### 🎯 **Recuerda**

La estadística es como aprender un nuevo idioma: al principio puede parecer difícil, pero cada concepto 
que dominas te abre nuevas puertas para entender el mundo. **No se trata de memorizar fórmulas**, 
sino de desarrollar un **pensamiento analítico** que te acompañará toda tu vida profesional.

**¡Sigue practicando y no te rindas! 💪📈**

</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 14px;color: #424242;">
Desarrollado con 💙 para estudiantes de Uninorte<br>
¿Dudas o sugerencias? Escribe a <a href="mailto:carlosdl@uninorte.edu.co">carlosdl@uninorte.edu.co</a>
</div>

""", unsafe_allow_html=True)



