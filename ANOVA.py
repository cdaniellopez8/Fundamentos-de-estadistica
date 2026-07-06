
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

# ─────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Entendiendo ANOVA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# CSS PERSONALIZADO
# ─────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: white; border-radius: 10px; padding: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .concept-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border-radius: 12px; padding: 20px; margin: 10px 0;
    }
    .formula-box {
        background: #1e1e2e; color: #cdd6f4;
        border-radius: 10px; padding: 15px;
        font-family: monospace; font-size: 15px;
        border-left: 4px solid #89b4fa;
        margin: 10px 0;
    }
    .highlight-green { background-color: #d4edda; border-radius: 8px; padding: 10px; border-left: 4px solid #28a745; }
    .highlight-red   { background-color: #f8d7da; border-radius: 8px; padding: 10px; border-left: 4px solid #dc3545; }
    .highlight-blue  { background-color: #d1ecf1; border-radius: 8px; padding: 10px; border-left: 4px solid #17a2b8; }
    .highlight-yellow{ background-color: #fff3cd; border-radius: 8px; padding: 10px; border-left: 4px solid #ffc107; }
    .section-title { font-size: 1.8rem; font-weight: 700; color: #2d3748; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# BARRA LATERAL
# ─────────────────────────────────────────
st.sidebar.title("📐 ANOVA Interactivo")
st.sidebar.markdown("*Universidad del Norte*")
st.sidebar.markdown("---")

page = st.sidebar.radio("📌 Navegar a:", [
    "1. 🏠 Inicio",
    "2. 🤔 ¿Por qué no solo comparar medias?",
    "3. 🔬 Varianza Entre vs. Dentro",
])

COLORS = ["#4361ee", "#f72585", "#4cc9f0", "#7209b7"]
GROUP_NAMES = ["Grupo A", "Grupo B", "Grupo C", "Grupo D"]

# ─────────────────────────────────────────
# FUNCIONES AUXILIARES
# ─────────────────────────────────────────
def compute_anova(groups):
    """Calcula todos los componentes de ANOVA de una sola vía."""
    all_data  = np.concatenate(groups)
    grand_mean = np.mean(all_data)
    N          = len(all_data)
    k          = len(groups)
    ns         = [len(g) for g in groups]
    means      = [np.mean(g) for g in groups]

    SSF = sum(ns[i] * (means[i] - grand_mean)**2 for i in range(k))
    SSE = sum(np.sum((g - means[i])**2) for i, g in enumerate(groups))
    SST = SSF + SSE

    dfB  = k - 1
    dfW  = N - k
    MSB  = SSF / dfB
    MSW  = SSE / dfW if dfW > 0 else np.nan
    F    = MSB / MSW if MSW and MSW > 0 else np.nan
    p    = 1 - stats.f.cdf(F, dfB, dfW) if not np.isnan(F) else np.nan

    return {
        "grand_mean": grand_mean, "N": N, "k": k,
        "ns": ns, "means": means,
        "SSF": SSF, "SSE": SSE, "SST": SST,
        "dfB": dfB, "dfW": dfW,
        "MSB": MSB, "MSW": MSW, "F": F, "p": p
    }

def violin_plot(groups, title="", show_grand_mean=True):
    fig = go.Figure()
    all_vals = np.concatenate(groups)
    grand_mean = np.mean(all_vals)

    for i, g in enumerate(groups):
        fig.add_trace(go.Violin(
            y=g, name=GROUP_NAMES[i],
            box_visible=True, meanline_visible=True,
            fillcolor=COLORS[i], opacity=0.7,
            line_color="white", points="all",
            pointpos=0, marker=dict(size=4, opacity=0.5)
        ))

    if show_grand_mean:
        fig.add_hline(y=grand_mean, line_dash="dash", line_color="#ff6b6b",
                      line_width=2, annotation_text=f"Gran Media = {grand_mean:.2f}",
                      annotation_position="top right")

    fig.update_layout(
        title=title, height=420,
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Arial", size=13),
        legend=dict(orientation="h", y=-0.15),
        yaxis=dict(gridcolor="#e0e0e0")
    )
    return fig

def tabla_anova_html(res):
    html = f"""
    <table style="width:100%; border-collapse:collapse; font-family:Arial; font-size:14px;">
      <thead>
        <tr style="background:#4361ee; color:white;">
          <th style="padding:10px; text-align:left;">Fuente</th>
          <th style="padding:10px; text-align:center;">SS</th>
          <th style="padding:10px; text-align:center;">df</th>
          <th style="padding:10px; text-align:center;">MS</th>
          <th style="padding:10px; text-align:center;">F</th>
          <th style="padding:10px; text-align:center;">p-valor</th>
        </tr>
      </thead>
      <tbody>
        <tr style="background:#eef2ff;">
          <td style="padding:9px; font-weight:bold;">Entre grupos (SSF)</td>
          <td style="padding:9px; text-align:center;">{res["SSF"]:.3f}</td>
          <td style="padding:9px; text-align:center;">{res["dfB"]}</td>
          <td style="padding:9px; text-align:center;">{res["MSB"]:.3f}</td>
          <td style="padding:9px; text-align:center; font-weight:bold; color:#4361ee;">{res["F"]:.3f}</td>
          <td style="padding:9px; text-align:center; font-weight:bold; color:{'#dc3545' if res['p']<0.05 else '#28a745'};">{res["p"]:.4f}</td>
        </tr>
        <tr style="background:#fff0f5;">
          <td style="padding:9px; font-weight:bold;">Dentro grupos (SSE)</td>
          <td style="padding:9px; text-align:center;">{res["SSE"]:.3f}</td>
          <td style="padding:9px; text-align:center;">{res["dfW"]}</td>
          <td style="padding:9px; text-align:center;">{res["MSW"]:.3f}</td>
          <td style="padding:9px; text-align:center;">—</td>
          <td style="padding:9px; text-align:center;">—</td>
        </tr>
        <tr style="background:#f0fff4; font-weight:bold;">
          <td style="padding:9px;">Total (SST)</td>
          <td style="padding:9px; text-align:center;">{res["SST"]:.3f}</td>
          <td style="padding:9px; text-align:center;">{res["dfB"]+res["dfW"]}</td>
          <td style="padding:9px; text-align:center;">—</td>
          <td style="padding:9px; text-align:center;">—</td>
          <td style="padding:9px; text-align:center;">—</td>
        </tr>
      </tbody>
    </table>
    """
    return html

# ═══════════════════════════════════════════════════════
# PÁGINA 1: INICIO
# ═══════════════════════════════════════════════════════
if page == "1. 🏠 Inicio":
    st.markdown("### 📐 Entendiendo ANOVA desde Cero")
    st.markdown("#### *Analysis of Variance — Una forma intuitiva de comparar múltiples grupos*")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="concept-box">
        <h3>🎯 ¿Qué es ANOVA?</h3>
        <p>Una prueba estadística que nos permite comparar las medias de <b>3 o más grupos</b> simultáneamente, determinando si al menos uno es diferente.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg,#f72585,#7209b7); color:white; border-radius:12px; padding:20px; margin:10px 0;">
        <h3>🔑 La Pregunta Central</h3>
        <p>¿Las diferencias entre las medias de los grupos son <b>reales</b> o simplemente producto del <b>azar</b>?</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg,#4cc9f0,#4361ee); color:white; border-radius:12px; padding:20px; margin:10px 0;">
        <h3>⚙️ La Herramienta</h3>
        <p>ANOVA usa la <b>varianza</b> (no solo las medias) para responder esta pregunta. ¡Aquí aprenderás por qué!</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🗺️ Ruta de Aprendizaje")

    pasos = [
        ("2. 🤔 ¿Por qué no solo comparar medias?",  "El problema con solo mirar promedios"),
        ("3. 🔬 Varianza Entre vs. Dentro",           "La descomposición clave de ANOVA"),
        ("4. 📊 Construyendo el estadístico F",        "Cómo se arma el valor F paso a paso"),
        ("5. 🎛️ Simulador Interactivo",               "Experimenta con tus propios grupos"),
        ("6. 🎲 Explorador de Escenarios",             "Casos reales con decisiones"),
        ("7. ❓ Cuestionario Final",                   "Evalúa tu comprensión"),
    ]

    # SE CORRIGIÓ AQUÍ: Añadidos 4 espacios de indentación a todo este bloque para mantenerlo dentro de la Página 1
    for i, (titulo, desc) in enumerate(pasos):
        col_n, col_t = st.columns([1, 9])

        with col_n:
            st.markdown(
                f"""
                <div style='background:#4361ee;color:white;border-radius:50%;width:40px;height:40px;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:18px;margin-top:5px;'>
                    {i+1}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_t:
            st.markdown(f"""
    **{titulo}**

    *{desc}*
    """)
            
    st.markdown("---")
    st.markdown("### 🧪 Vista Previa: El Mismo Promedio, Conclusiones Distintas")
    st.markdown("Estos dos datasets tienen **exactamente las mismas medias por grupo**, pero ¿dirías lo mismo de ambos?")

    np.random.seed(42)
    # Dataset A: grupos COMPACTOS → diferencias reales
    gA = [np.random.normal(m, 1.5, 30) for m in [10, 15, 20, 25]]
    # Dataset B: grupos MUY DISPERSOS → diferencias dudosas
    gB = [np.random.normal(m, 9.0, 30) for m in [10, 15, 20, 25]]

    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(violin_plot(gA, "Dataset A — Grupos compactos"), use_container_width=True)
        st.markdown('<div class="highlight-green">✅ Las medias difieren <b>claramente</b>. La varianza <i>dentro</i> de cada grupo es pequeña.</div>', unsafe_allow_html=True)
    with col_b:
        st.plotly_chart(violin_plot(gB, "Dataset B — Grupos dispersos"), use_container_width=True)
        st.markdown('<div class="highlight-red">❓ Las mismas medias, pero los grupos se <b>solapan mucho</b>. ¿De verdad son diferentes?</div>', unsafe_allow_html=True)

    st.info("👉 Usa el menú lateral para navegar por las secciones y descubrir cómo ANOVA resuelve este dilema.")


# ═══════════════════════════════════════════════════════
# PÁGINA 2: ¿POR QUÉ NO SOLO COMPARAR MEDIAS?
# ═══════════════════════════════════════════════════════

elif page == "2. 🤔 ¿Por qué no solo comparar medias?":

    st.markdown("### 🤔 ¿Por qué no simplemente comparar las medias?")
    st.markdown("---")

    st.markdown("""
    ### El problema

    Imagina que eres un investigador y deseas comparar el **rendimiento académico**
    de estudiantes bajo **cuatro métodos de enseñanza**.

    Las medias observadas son:
    """)

    medias_ejemplo = [72, 75, 78, 74]

    cols = st.columns(4)

    for col, nombre, media in zip(cols, GROUP_NAMES, medias_ejemplo):
        with col:
            st.metric(nombre, f"{media} pts")

    st.info("🤔 ¿Estas diferencias son suficientes para concluir que los métodos producen resultados distintos?")

    st.markdown("---")

    st.markdown("""
    ## 🔍 Dos realidades con las mismas medias

    En ambos casos las medias son exactamente las mismas.

    Lo único que cambia es la **dispersión de los datos**.
    """)

    np.random.seed(7)

    sigma_compact = st.slider(
        "Dispersión interna de los grupos (σ)",
        min_value=1.0,
        max_value=15.0,
        value=3.0,
        step=0.5,
        help="Controla qué tan dispersos son los datos dentro de cada grupo."
    )

    g_compact = [
        np.random.normal(m, sigma_compact, 40)
        for m in medias_ejemplo
    ]

    g_spread = [
        np.random.normal(m, 12, 40)
        for m in medias_ejemplo
    ]

    col1, col2 = st.columns(2)

    # -----------------------
    # Caso 1
    # -----------------------
    with col1:

        st.subheader(f"📦 Grupos compactos (σ = {sigma_compact:.1f})")

        fig = violin_plot(g_compact, "")
        st.plotly_chart(fig, use_container_width=True)

        res = compute_anova(g_compact)

        st.metric("F", f"{res['F']:.2f}")
        st.metric("p-valor", f"{res['p']:.4f}")

        if res["p"] < 0.05:
            st.success(
                "Con poca variabilidad interna, las diferencias entre medias "
                "destacan claramente."
            )
        else:
            st.warning(
                "Aunque la dispersión es pequeña, en esta simulación no hay "
                "evidencia suficiente para rechazar H₀."
            )

    # -----------------------
    # Caso 2
    # -----------------------
    with col2:

        st.subheader("🌊 Grupos muy dispersos (σ = 12)")

        fig = violin_plot(g_spread, "")
        st.plotly_chart(fig, use_container_width=True)

        res = compute_anova(g_spread)

        st.metric("F", f"{res['F']:.2f}")
        st.metric("p-valor", f"{res['p']:.4f}")

        if res["p"] < 0.05:
            st.success(
                "A pesar de la gran dispersión, la diferencia entre medias sigue "
                "siendo suficientemente grande."
            )
        else:
            st.error(
                "La variabilidad dentro de los grupos oculta las diferencias "
                "entre las medias."
            )

    st.markdown("---")

    st.markdown("""
    ### 💡 La idea clave

    <div class="concept-box">

    <h4>¿Por qué no basta con comparar las medias?</h4>

    <ul>
        <li>Una diferencia de <b>6 puntos</b> puede ser enorme si cada grupo tiene muy poca variabilidad.</li>
        <li>La misma diferencia puede ser irrelevante si los grupos presentan mucha dispersión.</li>
        <li>Por eso ANOVA no compara únicamente las medias; también considera la variabilidad interna de cada grupo.</li>
    </ul>

    <b>ANOVA compara la señal (diferencias entre medias) con el ruido (variabilidad dentro de los grupos).</b>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("## 🚫 ¿Por qué no hacer varios t-test?")

    k = 4
    comparaciones = k * (k - 1) // 2
    alpha = 0.05
    prob_error = 1 - (1 - alpha) ** comparaciones

    st.markdown(
        f"""
Con **{k} grupos** existen **{comparaciones} comparaciones posibles**.

Si realizáramos un t-test para cada una usando un nivel de significancia de **5%**, la probabilidad de cometer **al menos un Error Tipo I** sería

$$
P(\\text{{al menos un error}})
=
1-(1-0.05)^{{{comparaciones}}}
=
{prob_error:.3f}
$$

Es decir, aproximadamente **{prob_error*100:.1f}%**.

👉 ANOVA evita este problema realizando **una única prueba global** para evaluar si todas las medias pueden considerarse iguales.
"""
    )



# ═══════════════════════════════════════════════════════
# PÁGINA 3: VARIANZA ENTRE VS DENTRO
# ═══════════════════════════════════════════════════════
elif page == "3. 🔬 Varianza Entre vs. Dentro":
    st.markdown("### 🔬 Varianza Entre Grupos vs. Varianza Dentro de Grupos")
    st.markdown("---")

    st.markdown("""
    ### La Descomposición Fundamental de ANOVA
    ANOVA parte de una idea brillante: **toda la variabilidad de los datos tiene dos fuentes**.
    """)

    st.markdown("""
    $$SST = SSF + SSE$$

    | Componente | Nombre | Pregunta que responde |
    |---|---|---|
    | **SST** | Suma de cuadrados Total | ¿Cuánto varían todos los datos respecto a la gran media? |
    | **SSF** | Suma de cuadrados Entre (Factor) | ¿Cuánto varían las medias de los grupos respecto a la gran media? |
    | **SSE** | Suma de cuadrados Dentro (Error) | ¿Cuánto varían los datos dentro de cada grupo? |
    """)

    st.markdown("---")
    st.markdown("### 🎛️ Experimenta con los datos")

    np.random.seed(99)
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        sep   = st.slider("Separación entre grupos (señal)", 0.0, 20.0, 8.0, 0.5)
    with col_s2:
        noise = st.slider("Dispersión dentro de grupos (ruido)", 0.5, 15.0, 3.0, 0.5)

    base_means = np.array([0, 1, 2, 3]) * sep / 3 + 50
    groups = [np.random.normal(m, noise, 30) for m in base_means]
    res    = compute_anova(groups)

    # ── GRÁFICO PRINCIPAL ──────────────────────────────
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=("Distribución de los Grupos", "Descomposición de la Varianza"),
                        column_widths=[0.6, 0.4])

    for i, g in enumerate(groups):
        fig.add_trace(go.Violin(
            y=g, name=GROUP_NAMES[i],
            box_visible=True, meanline_visible=True,
            fillcolor=COLORS[i], opacity=0.65,
            line_color="white", showlegend=True,
            points="all", pointpos=0,
            marker=dict(size=3, opacity=0.4)
        ), row=1, col=1)

    fig.add_hline(y=res["grand_mean"], line_dash="dash", line_color="#ff6b6b",
                  line_width=2.5, row=1, col=1,
                  annotation_text=f"Gran Media={res['grand_mean']:.1f}",
                  annotation_position="top right")

    fig.add_trace(go.Bar(
        x=["SSF (Factor)", "SSE (Error)", "SST (Total)"],
        y=[res["SSF"], res["SSE"], res["SST"]],
        marker_color=["#4361ee", "#f72585", "#7209b7"],
        text=[f"{res['SSF']:.1f}", f"{res['SSE']:.1f}", f"{res['SST']:.1f}"],
        textposition="outside",
        showlegend=False
    ), row=1, col=2)

    fig.update_layout(height=430, plot_bgcolor="white", paper_bgcolor="white",
                      font=dict(family="Arial", size=12),
                      legend=dict(orientation="h", y=-0.18))
    fig.update_yaxes(gridcolor="#e0e0e0")
    st.plotly_chart(fig, use_container_width=True)

    # ── MÉTRICAS ──────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("SSF (Entre)", f"{res['SSF']:.1f}")
    c2.metric("SSE (Dentro)", f"{res['SSE']:.1f}")
    c3.metric("SST (Total)", f"{res['SST']:.1f}")
    c4.metric("Estadístico F", f"{res['F']:.2f}")
    c5.metric("p-valor", f"{res['p']:.4f}")

    st.markdown("---")

    st.markdown("---")
    st.markdown("### 🧠 Regla Intuitiva")
    ratio = res["SSF"] / res["SST"] * 100 if res["SST"] > 0 else 0
    st.markdown(f"""
    <div class="concept-box">
    En este ejemplo, el <b>{ratio:.1f}%</b> de la variabilidad total se explica por las diferencias
    <b>entre grupos</b> (SSF), y el <b>{100-ratio:.1f}%</b> restante es variabilidad <i>dentro</i> de los grupos (SSE).<br><br>
    👉 <b>Cuanto mayor sea SSF respecto a SSE, más evidencia tenemos de que los grupos son realmente distintos.</b>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
📧 <strong>Contacto:</strong> carlosdl@uninorte.edu.co<br>
Desarrollado con 💙 para estudiantes de Uninorte 
</div>
""", unsafe_allow_html=True)
