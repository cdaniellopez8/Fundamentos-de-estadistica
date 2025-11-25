import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuración inicial
st.set_page_config(page_title="Tipos de Datos Interactivos", page_icon="📊", layout="centered")

st.title("📊 Tipos y Escalas de Medida de los Datos")
st.write("""
Este módulo interactivo te permitirá **reconocer los distintos tipos y escalas de medida de los datos**, 
a través de ejemplos, retroalimentación y gráficos explicativos.
""")

# --- Función general de pregunta ---
def pregunta(
    texto_pregunta, 
    opciones, 
    correcta, 
    tipo_variable, 
    explicacion_bien, 
    explicacion_mal
):
    st.markdown(f"### ❓ {texto_pregunta}")

    respuesta = st.radio("Selecciona una respuesta:", [""] + opciones, index=0, label_visibility="collapsed")

    if respuesta != "":
        if respuesta == correcta:
            st.success(f"✅ ¡Correcto! {explicacion_bien}")

            # Introducción antes del gráfico
            st.markdown(
                f"💡 Con una variable **{tipo_variable}**, se pueden construir gráficos como el siguiente "
                "para representar sus valores y patrones de comportamiento:"
            )

            # Mostrar gráfico
            fig, ax = plt.subplots()

            if tipo_variable == "cualitativa":
                datos = pd.Series(["A", "B", "C", "A", "B", "A"])
                datos.value_counts().plot(kind="bar", color="skyblue", ax=ax)
                ax.set_title("Gráfico de barras - Variable cualitativa")
                ax.set_xlabel("Categorías")
                ax.set_ylabel("Frecuencia")

            elif tipo_variable == "cuantitativa":
                datos = np.random.randint(1, 100, 50)
                ax.hist(datos, bins=10, color="salmon", edgecolor="black")
                ax.set_title("Histograma - Variable cuantitativa")
                ax.set_xlabel("Valores")
                ax.set_ylabel("Frecuencia")

            elif tipo_variable == "nominal":
                datos = pd.Series(["Rojo", "Azul", "Verde", "Rojo", "Azul", "Rojo"])
                datos.value_counts().plot(kind="pie", autopct="%1.0f%%", ax=ax)
                ax.set_ylabel("")
                ax.set_title("Gráfico de pastel - Variable nominal")

            elif tipo_variable == "ordinal":
                categorias = ["Bajo", "Medio", "Alto"]
                datos = pd.Categorical(np.random.choice(categorias, 30), categories=categorias, ordered=True)
                pd.Series(datos).value_counts().reindex(categorias).plot(kind="bar", color="gold", ax=ax)
                ax.set_title("Gráfico de barras ordenadas - Variable ordinal")

            elif tipo_variable == "discreta":
                datos = np.random.poisson(3, 50)
                pd.Series(datos).value_counts().sort_index().plot(kind="bar", color="lightgreen", ax=ax)
                ax.set_title("Gráfico de barras - Variable discreta")
                ax.set_xlabel("Valores enteros")
                ax.set_ylabel("Frecuencia")

            elif tipo_variable == "continua":
                datos = np.random.normal(50, 10, 100)
                ax.boxplot(datos, vert=False)
                ax.set_title("Boxplot - Variable continua")
                ax.set_xlabel("Valores")

            elif tipo_variable == "intervalo":
                datos = np.random.normal(100, 15, 100)
                ax.hist(datos, bins=10, color="lightblue", edgecolor="black")
                ax.set_title("Histograma - Escala de intervalo")
                ax.set_xlabel("Valores (no hay cero absoluto)")
                ax.set_ylabel("Frecuencia")

            elif tipo_variable == "razon":
                x = np.random.uniform(0, 100, 50)
                y = x * 1.5 + np.random.normal(0, 10, 50)
                ax.scatter(x, y, color="purple")
                ax.set_title("Gráfico de dispersión - Escala de razón")
                ax.set_xlabel("X")
                ax.set_ylabel("Y")

            st.pyplot(fig)

        else:
            st.error(f"❌ Incorrecto. {explicacion_mal}")


# --------------------
# PREGUNTAS
# --------------------

pregunta(
    "1️⃣ ¿Cuál de las siguientes variables es cualitativa?",
    ["Edad", "Estrato socioeconómico", "Peso", "Temperatura"],
    "Estrato socioeconómico",
    "cualitativa",
    "Las variables cualitativas describen **categorías o cualidades**, no valores numéricos.",
    "Las variables cualitativas no se miden con números, sino que describen atributos o clases."
)

pregunta(
    "2️⃣ ¿Cuál de las siguientes variables es cuantitativa?",
    ["Color de ojos", "Género", "Altura", "Tipo de sangre"],
    "Altura",
    "cuantitativa",
    "Las variables cuantitativas representan **cantidades medibles numéricamente**.",
    "Las variables cuantitativas deben poder expresarse en números, no en palabras o categorías."
)

pregunta(
    "3️⃣ ¿Cuál de las siguientes variables es nominal?",
    ["Satisfacción (baja, media, alta)", "Género", "Puntaje en examen", "Temperatura en °C"],
    "Género",
    "nominal",
    "Las variables nominales clasifican **sin jerarquía**: no hay orden entre las categorías.",
    "En las nominales, las categorías no tienen orden (ej. masculino ≠ femenino en magnitud)."
)

pregunta(
    "4️⃣ ¿Cuál de las siguientes variables es ordinal?",
    ["Temperatura", "Color favorito", "Nivel educativo", "Edad"],
    "Nivel educativo",
    "ordinal",
    "Las variables ordinales tienen **categorías con un orden lógico** (bajo < medio < alto).",
    "En las ordinales sí hay jerarquía, aunque no se puede medir la distancia exacta entre niveles."
)

pregunta(
    "5️⃣ ¿Cuál de las siguientes variables es discreta?",
    ["Número de hijos", "Peso corporal", "Altura", "Temperatura"],
    "Número de hijos",
    "discreta",
    "Las variables discretas toman **valores enteros contables**, sin decimales.",
    "Las variables discretas no tienen valores intermedios entre números enteros."
)

pregunta(
    "6️⃣ ¿Cuál de las siguientes variables es continua?",
    ["Número de hermanos", "cantidad de vacas en un establo", "Altura", "Categoría de producto"],
    "Altura",
    "continua",
    "Las variables continuas pueden tomar **infinitos valores dentro de un rango** (ej. 1.75 m).",
    "Las continuas permiten valores decimales o fraccionarios, no solo enteros."
)

pregunta(
    "7️⃣ ¿Cuál de las siguientes variables está en escala de intervalo?",
    ["Temperatura en °C", "Altura", "Peso", "Número de hijos"],
    "Temperatura en °C",
    "intervalo",
    "La escala de intervalo tiene diferencias medibles pero **no un cero absoluto** (0°C ≠ ausencia de temperatura).",
    "En la escala de intervalo, el cero no representa ausencia real del fenómeno medido."
)

pregunta(
    "8️⃣ ¿Cuál de las siguientes variables está en escala de razón?",
    ["Edad", "Temperatura en °C", "Nivel educativo", "Estrato socioeconómico"],
    "Edad",
    "razon",
    "La escala de razón tiene **cero absoluto** y permite comparaciones proporcionales (20 años es el doble de 10).",
    "La escala de razón incluye el cero real, lo que permite hacer operaciones y proporciones."
)

# --- Nueva pregunta conceptual sobre intervalos ---
pregunta(
    "9️⃣ ¿Es correcto afirmar que el año 2000 es el doble del año 1000?",
    ["Verdadero", "Falso"],
    "Falso",
    "intervalo",
    "Correcto. Las fechas son una **escala de intervalo**, no de razón. El año 0 no representa ausencia de tiempo, por lo tanto, no se pueden hacer comparaciones proporcionales.",
    "Incorrecto. En una escala de intervalo, como los años o grados Celsius, **no hay cero absoluto**, por lo tanto no tiene sentido decir que algo es el doble que otro valor."
)


# ---------------------
# RESUMEN FINAL
# ---------------------
st.divider()
st.markdown("## 🧭 Resumen general de los tipos y escalas de datos")

st.markdown("""
### 🧩 **Tipos de variables**
- **Cualitativas** → describen características o categorías  
  - 🟢 *Nominal:* sin orden (ej. color de ojos, género)  
  - 🟡 *Ordinal:* con orden (ej. nivel educativo: bajo–medio–alto)

- **Cuantitativas** → expresan cantidades numéricas  
  - 🔵 *Discretas:* valores enteros contables (ej. número de hijos)  
  - 🔴 *Continuas:* valores infinitos o decimales (ej. altura, peso)
""")

st.markdown("""
### ⚖️ **Escalas de medida**
| Escala | Qué permite | Ejemplo |
|:--|:--|:--|
| **Nominal** | Clasificar sin orden | Tipo de sangre |
| **Ordinal** | Clasificar con jerarquía | Nivel de satisfacción |
| **Intervalo** | Medir diferencias, sin cero absoluto | Temperatura (°C), Años |
| **Razón** | Medir diferencias y proporciones, con cero real | Peso, Edad, Ingresos |
""")

st.info("""
💬 **Conclusión:**  
Comprender el tipo y escala de los datos permite elegir las técnicas estadísticas adecuadas 
y representar la información correctamente en gráficos o análisis posteriores.
""")