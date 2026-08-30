import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="Marcasa | Análisis de Precios",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PALETA CORPORATIVA
# ============================================================

DORADO = "#FFB700"
NARANJA = "#FE6902"
AZUL = "#143458"
AZUL_OSCURO = "#0F2945"
AZUL_CLARO = "#1B456F"
GRIS = "#6B7280"
GRIS_CLARO = "#F3F4F6"
BLANCO = "#FFFFFF"
NEGRO = "#111827"
BORDE = "#E5E7EB"


# ============================================================
# ESTILOS CSS
# IMPORTANTE:
# Se evita HTML anidado dentro de st.markdown().
# Los componentes visuales personalizados usan HTML simple,
# lo que evita que Streamlit muestre las etiquetas <div>.
# ============================================================

st.markdown(
    f"""
<style>

/* ============================================================
   CONFIGURACIÓN GENERAL
   ============================================================ */

.stApp {{
    background: {BLANCO};
}}

.block-container {{
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}}

.stApp, .stApp p, .stApp label, .stApp span {{
    color: {NEGRO};
}}

/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {{
    background: linear-gradient(
        180deg,
        {AZUL} 0%,
        {AZUL_OSCURO} 100%
    );
}}

section[data-testid="stSidebar"] * {{
    color: {BLANCO};
}}

section[data-testid="stSidebar"] label {{
    color: {BLANCO} !important;
    font-weight: 600;
}}

section[data-testid="stSidebar"] div[data-baseweb="select"] {{
    background-color: {AZUL_OSCURO};
    border-radius: 8px;
}}

section[data-testid="stSidebar"] div[data-baseweb="select"] * {{
    color: {BLANCO} !important;
}}

section[data-testid="stSidebar"] input {{
    color: {BLANCO} !important;
}}

section[data-testid="stSidebar"] span[data-baseweb="tag"] {{
    background-color: {NARANJA};
    color: {BLANCO} !important;
    border-radius: 5px;
}}

section[data-testid="stSidebar"] hr {{
    border-top: 1px solid rgba(255,255,255,0.20);
}}

/* ============================================================
   CONTROLES PRINCIPALES
   ============================================================ */

/* Radio principal */
div[data-testid="stRadio"] label {{
    color: {NEGRO} !important;
}}

div[data-testid="stRadio"] label p {{
    color: {NEGRO} !important;
}}

div[data-testid="stRadio"] [role="radiogroup"] {{
    color: {NEGRO} !important;
}}

/* Labels principales */
div[data-testid="stFileUploader"] label,
div[data-testid="stTextInput"] label {{
    color: {NEGRO} !important;
}}

div[data-testid="stFileUploader"] label p,
div[data-testid="stTextInput"] label p {{
    color: {NEGRO} !important;
}}

/* File uploader */
div[data-testid="stFileUploader"] {{
    border: 2px dashed {DORADO};
    border-radius: 12px;
    padding: 12px;
    background: #FFFBEB;
}}

div[data-testid="stFileUploader"] section {{
    background: transparent;
}}

div[data-testid="stFileUploader"] button {{
    color: {AZUL} !important;
    border-color: {AZUL};
}}

/* Text input */
div[data-testid="stTextInput"] input {{
    color: {NEGRO} !important;
    background: {BLANCO} !important;
}}

div[data-testid="stTextInput"] input::placeholder {{
    color: #9CA3AF !important;
}}

/* ============================================================
   TÍTULOS NATIVOS
   ============================================================ */

h1, h2, h3 {{
    color: {AZUL} !important;
    font-weight: 800 !important;
}}

/* ============================================================
   HEADER CORPORATIVO
   ============================================================ */

.header-corporativo {{
    background: linear-gradient(
        135deg,
        {AZUL} 0%,
        {AZUL_CLARO} 55%,
        {AZUL} 100%
    );
    border-left: 7px solid {DORADO};
    border-radius: 14px;
    padding: 25px 30px;
    margin-bottom: 20px;
    box-shadow: 0 6px 18px rgba(20,52,88,0.15);
}}

.titulo-header {{
    color: {BLANCO};
    font-size: 32px;
    font-weight: 800;
    line-height: 1.2;
    margin: 0 0 8px 0;
}}

.subtitulo-header {{
    color: #E5E7EB;
    font-size: 15px;
    line-height: 1.6;
    margin: 0;
}}

/* ============================================================
   TÍTULOS DE SECCIÓN
   ============================================================ */

.seccion-titulo {{
    color: {AZUL};
    font-size: 22px;
    font-weight: 800;
    border-left: 6px solid {NARANJA};
    padding-left: 12px;
    margin-top: 25px;
    margin-bottom: 18px;
    line-height: 1.3;
}}

/* ============================================================
   KPIs
   ============================================================ */

.kpi-card {{
    background: {BLANCO};
    border: 1px solid {BORDE};
    border-radius: 12px;
    padding: 18px;
    min-height: 120px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.06);
}}

.kpi-label {{
    color: {GRIS};
    font-size: 13px;
    font-weight: 700;
    margin: 0;
}}

.kpi-value {{
    color: {AZUL};
    font-size: 28px;
    font-weight: 800;
    margin-top: 10px;
}}

.kpi-card.dorado {{
    border-top: 5px solid {DORADO};
}}

.kpi-card.naranja {{
    border-top: 5px solid {NARANJA};
}}

.kpi-card.azul {{
    border-top: 5px solid {AZUL};
}}

.kpi-card.gris {{
    border-top: 5px solid {GRIS};
}}

/* ============================================================
   BOTONES
   ============================================================ */

.stButton > button {{
    background: {NARANJA};
    color: {BLANCO};
    border: none;
    border-radius: 8px;
    font-weight: 700;
}}

.stButton > button:hover {{
    background: {DORADO};
    color: {AZUL};
}}

/* ============================================================
   ALERTAS
   ============================================================ */

.stAlert {{
    border-radius: 10px;
}}

/* ============================================================
   DIVISORES
   ============================================================ */

hr {{
    border: none;
    border-top: 1px solid {BORDE};
    margin: 25px 0;
}}

/* ============================================================
   PANTALLA INICIAL
   ============================================================ */

.inicio-card {{
    background: {GRIS_CLARO};
    border-left: 6px solid {DORADO};
    border-radius: 14px;
    padding: 40px;
    text-align: center;
    margin-top: 35px;
}}

.inicio-icono {{
    font-size: 48px;
    line-height: 1;
}}

.inicio-titulo {{
    color: {AZUL};
    font-size: 27px;
    font-weight: 800;
    margin-top: 12px;
}}

.inicio-texto {{
    color: {GRIS};
    font-size: 16px;
    line-height: 1.6;
}}

/* ============================================================
   LOGIN
   ============================================================ */

.login-card {{
    max-width: 550px;
    margin: 80px auto 20px auto;
    padding: 40px;
    background: {BLANCO};
    border-radius: 15px;
    border-top: 7px solid {DORADO};
    box-shadow: 0 5px 25px rgba(0,0,0,.10);
    text-align: center;
}}

.login-icon {{
    font-size: 55px;
    line-height: 1;
    margin-bottom: 12px;
}}

.login-title {{
    color: {AZUL};
    font-size: 30px;
    font-weight: 800;
}}

.login-text {{
    color: {GRIS};
    font-size: 15px;
    margin-top: 8px;
}}

/* ============================================================
   LOGO
   ============================================================ */

.logo-container {{
    text-align: center;
    padding-top: 10px;
}}

/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 900px) {{
    .titulo-header {{
        font-size: 25px;
    }}

    .subtitulo-header {{
        font-size: 13px;
    }}

    .seccion-titulo {{
        font-size: 19px;
    }}
}}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# FUNCIÓN PARA HTML PERSONALIZADO
# ============================================================

def mostrar_html(html):
    """
    Renderiza HTML simple mediante Streamlit.
    No utiliza indentación con bloques HTML anidados.
    """
    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# SISTEMA DE CONTRASEÑA
# ============================================================

def verificar_password():

    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    def password_entered():

        password = st.session_state.get("password", "")

        if password == "Marcasa2026":
            st.session_state["password_correct"] = True
            st.session_state["password_error"] = False
        else:
            st.session_state["password_correct"] = False
            st.session_state["password_error"] = True

    if not st.session_state["password_correct"]:

        mostrar_html(
            f"""
<div class="login-card">
<div class="login-icon">⛽</div>
<div class="login-title">Marcasa</div>
<div class="login-text">Sistema de Análisis de Competencia y Precios</div>
</div>
"""
        )

        st.text_input(
            "Ingresa la contraseña para acceder al aplicativo:",
            type="password",
            on_change=password_entered,
            key="password"
        )

        if st.session_state.get("password_error", False):
            st.error("😕 Contraseña incorrecta. Intenta nuevamente.")

        return False

    return True


if not verificar_password():
    st.stop()


# ============================================================
# CABECERA CORPORATIVA
# ============================================================

col_logo, col_header = st.columns([1, 5], vertical_alignment="center")

with col_logo:

    if os.path.exists("logo.png"):

        st.markdown('<div class="logo-container">', unsafe_allow_html=True)

        st.image(
            "logo.png",
            width=145
        )

        st.markdown("</div>", unsafe_allow_html=True)

    else:

        mostrar_html(
            """
<div class="logo-container" style="font-size:55px;">⛽</div>
"""
        )


with col_header:

    mostrar_html(
        f"""
<div class="header-corporativo">
<div class="titulo-header">Análisis Inteligente de Competencia y Precios</div>
<div class="subtitulo-header">Monitoreo estratégico de precios de combustibles · Información de mercado · Análisis comparativo</div>
</div>
"""
    )


# ============================================================
# FUNCIÓN DE CARGA DE DATOS
# ============================================================

@st.cache_data
def load_data(file_or_url):

    try:

        df = pd.read_excel(file_or_url)

        return df

    except Exception as e:

        st.error(f"Error al cargar la data: {e}")

        return None


# ============================================================
# ORIGEN DE DATOS
# ============================================================

mostrar_html(
    f'<div class="seccion-titulo">📁 Origen de Datos</div>'
)

origen = st.radio(
    "Selecciona cómo ingresar los datos:",
    [
        "Subir archivo Excel local",
        "Ingresar enlace URL de Osinergmin"
    ],
    key="origen_datos_principal",
    horizontal=True
)

df_original = None


# ============================================================
# ARCHIVO LOCAL
# ============================================================

if origen == "Subir archivo Excel local":

    uploaded_file = st.file_uploader(
        "Sube el archivo de precios de Osinergmin",
        type=["xlsx"],
        key="archivo_local",
        help="Formato permitido: Excel (.xlsx)"
    )

    if uploaded_file is not None:
        df_original = load_data(uploaded_file)


# ============================================================
# URL OSINERGMIN
# ============================================================

else:

    url = st.text_input(
        "Pega el enlace de descarga directa del Excel:",
        key="url_osinergmin",
        placeholder="https://..."
    )

    if url:
        df_original = load_data(url)


# ============================================================
# PROCESAMIENTO
# ============================================================

if df_original is not None:

    df_base = df_original.copy()

    # --------------------------------------------------------
    # VALIDACIÓN DE COLUMNAS
    # --------------------------------------------------------

    columnas_requeridas = [
        "PRECIO_VENTA",
        "DEPARTAMENTO",
        "PROVINCIA",
        "DISTRITO",
        "PRODUCTO",
        "RAZON",
        "DIRECCION"
    ]

    columnas_faltantes = [
        columna
        for columna in columnas_requeridas
        if columna not in df_base.columns
    ]

    if columnas_faltantes:

        st.error(
            "❌ El archivo no contiene las columnas necesarias: "
            + ", ".join(columnas_faltantes)
        )

        st.stop()


    # --------------------------------------------------------
    # LIMPIEZA DE DATOS
    # --------------------------------------------------------

    df_base["PRECIO_VENTA"] = pd.to_numeric(
        df_base["PRECIO_VENTA"],
        errors="coerce"
    )

    df_base = df_base.dropna(
        subset=["PRECIO_VENTA"]
    )

    # Normalización de campos de texto para filtros.
    for columna in [
        "DEPARTAMENTO",
        "PROVINCIA",
        "DISTRITO",
        "PRODUCTO",
        "RAZON",
        "DIRECCION"
    ]:
        df_base[columna] = (
            df_base[columna]
            .fillna("")
            .astype(str)
            .str.strip()
        )


    # ========================================================
    # SIDEBAR
    # ========================================================

    st.sidebar.markdown(
        f"""
<div style="text-align:center;padding:10px 0 20px 0;border-bottom:1px solid rgba(255,255,255,.20);">
<div style="font-size:32px;">📊</div>
<div style="font-size:20px;font-weight:800;color:{BLANCO};">Panel de Análisis</div>
<div style="font-size:12px;color:#D1D5DB;">Filtros de competencia</div>
</div>
""",
        unsafe_allow_html=True
    )


    # ========================================================
    # UBICACIÓN
    # ========================================================

    st.sidebar.markdown("### 📍 Ubicación")


    # --------------------------------------------------------
    # DEPARTAMENTO
    # --------------------------------------------------------

    departamentos_disponibles = sorted(
        df_base["DEPARTAMENTO"]
        .replace("", pd.NA)
        .dropna()
        .unique()
        .tolist()
    )

    departamentos_seleccionados = st.sidebar.multiselect(
        "1. Selecciona Departamentos",
        options=departamentos_disponibles,
        default=[],
        placeholder="Seleccionar departamentos..."
    )


    # --------------------------------------------------------
    # PROVINCIAS
    # --------------------------------------------------------

    if departamentos_seleccionados:

        df_provincias = df_base[
            df_base["DEPARTAMENTO"].isin(
                departamentos_seleccionados
            )
        ]

    else:

        df_provincias = df_base.copy()


    provincias_disponibles = sorted(
        df_provincias["PROVINCIA"]
        .replace("", pd.NA)
        .dropna()
        .unique()
        .tolist()
    )

    provincias_seleccionadas = st.sidebar.multiselect(
        "2. Selecciona Provincias",
        options=provincias_disponibles,
        default=[],
        placeholder="Seleccionar provincias..."
    )


    # --------------------------------------------------------
    # DISTRITOS
    # --------------------------------------------------------

    if provincias_seleccionadas:

        df_distritos = df_provincias[
            df_provincias["PROVINCIA"].isin(
                provincias_seleccionadas
            )
        ]

    else:

        df_distritos = df_provincias.copy()


    distritos_disponibles = sorted(
        df_distritos["DISTRITO"]
        .replace("", pd.NA)
        .dropna()
        .unique()
        .tolist()
    )

    distritos_seleccionados = st.sidebar.multiselect(
        "3. Selecciona Distritos",
        options=distritos_disponibles,
        default=[],
        placeholder="Seleccionar distritos..."
    )


    # ========================================================
    # PRODUCTO
    # ========================================================

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🛢️ Producto")


    productos_clave = [
        "GASOHOL REGULAR",
        "GASOHOL PREMIUM",
        "Diesel B5 S-50 UV",
        "DIESEL B5 UV"
    ]


    productos_existentes = sorted(
        df_base["PRODUCTO"]
        .replace("", pd.NA)
        .dropna()
        .unique()
        .tolist()
    )


    productos_disponibles = [
        producto
        for producto in productos_clave
        if producto in productos_existentes
    ]


    if not productos_disponibles:
        productos_disponibles = productos_existentes


    producto_opciones = [
        "Selecciona un combustible"
    ] + productos_disponibles


    producto_seleccionado = st.sidebar.selectbox(
        "4. Selecciona el combustible",
        options=producto_opciones,
        index=0
    )


    # ========================================================
    # APLICACIÓN DE FILTROS
    # ========================================================

    df = df_base.copy()


    if departamentos_seleccionados:
        df = df[
            df["DEPARTAMENTO"].isin(
                departamentos_seleccionados
            )
        ]


    if provincias_seleccionadas:
        df = df[
            df["PROVINCIA"].isin(
                provincias_seleccionadas
            )
        ]


    if distritos_seleccionados:
        df = df[
            df["DISTRITO"].isin(
                distritos_seleccionados
            )
        ]


    if producto_seleccionado != "Selecciona un combustible":

        df = df[
            df["PRODUCTO"] == producto_seleccionado
        ]


    # ========================================================
    # RESUMEN DE FILTROS
    # ========================================================

    filtros_activos = []


    if departamentos_seleccionados:
        filtros_activos.append(
            "Departamentos: "
            + ", ".join(departamentos_seleccionados)
        )


    if provincias_seleccionadas:
        filtros_activos.append(
            "Provincias: "
            + ", ".join(provincias_seleccionadas)
        )


    if distritos_seleccionados:
        filtros_activos.append(
            "Distritos: "
            + ", ".join(distritos_seleccionados)
        )


    if producto_seleccionado != "Selecciona un combustible":
        filtros_activos.append(
            "Producto: "
            + producto_seleccionado
        )


    if filtros_activos:

        st.info(
            "🔎 **Filtros activos:** "
            + " | ".join(filtros_activos)
        )

    else:

        st.success(
            "📊 **Vista general:** no hay filtros seleccionados. "
            "Se muestra toda la información disponible."
        )


    # ========================================================
    # RESULTADOS
    # ========================================================

    if not df.empty:

        mostrar_html(
            '<div class="seccion-titulo">📊 Resultados del Análisis Comparativo</div>'
        )


        # ====================================================
        # KPIs
        # ====================================================

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            mostrar_html(
                f"""
<div class="kpi-card dorado">
<div class="kpi-label">💵 PRECIO MÍNIMO</div>
<div class="kpi-value">S/ {df["PRECIO_VENTA"].min():.2f}</div>
</div>
"""
            )


        with col2:

            mostrar_html(
                f"""
<div class="kpi-card naranja">
<div class="kpi-label">📈 PRECIO PROMEDIO</div>
<div class="kpi-value">S/ {df["PRECIO_VENTA"].mean():.2f}</div>
</div>
"""
            )


        with col3:

            mostrar_html(
                f"""
<div class="kpi-card azul">
<div class="kpi-label">📉 PRECIO MÁXIMO</div>
<div class="kpi-value">S/ {df["PRECIO_VENTA"].max():.2f}</div>
</div>
"""
            )


        with col4:

            mostrar_html(
                f"""
<div class="kpi-card gris">
<div class="kpi-label">🏢 ESTACIONES ANALIZADAS</div>
<div class="kpi-value">{df["RAZON"].nunique()}</div>
</div>
"""
            )


        st.markdown("---")


        # ====================================================
        # GRÁFICO DE BARRAS
        # ====================================================

        mostrar_html(
            '<div class="seccion-titulo">📊 Comparativa de Precios por Distrito y Competidor</div>'
        )


        fig_bar = px.bar(
            df.sort_values("PRECIO_VENTA"),
            x="DISTRITO",
            y="PRECIO_VENTA",
            color="RAZON",
            barmode="group",
            hover_data=[
                "DIRECCION",
                "PRODUCTO"
            ],
            title="Comparativa Directa de Precios",
            labels={
                "DISTRITO": "Distrito",
                "PRECIO_VENTA": "Precio de Venta (S/)",
                "RAZON": "Estación / Empresa"
            },
            color_discrete_sequence=[
                DORADO,
                NARANJA,
                AZUL,
                GRIS
            ]
        )


        fig_bar.update_layout(
            plot_bgcolor=BLANCO,
            paper_bgcolor=BLANCO,
            font=dict(
                color=AZUL
            ),
            title_font=dict(
                color=AZUL,
                size=20
            ),
            xaxis=dict(
                title="Distrito",
                showgrid=False
            ),
            yaxis=dict(
                title="Precio de Venta (S/)",
                gridcolor=BORDE
            ),
            legend_title="Competidor",
            xaxis_tickangle=-45,
            margin=dict(
                l=20,
                r=20,
                t=70,
                b=80
            )
        )


        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )


        # ====================================================
        # BOXPLOT
        # ====================================================

        mostrar_html(
            '<div class="seccion-titulo">📦 Distribución y Dispersión de Precios</div>'
        )


        fig_box = px.box(
            df,
            x="DISTRITO",
            y="PRECIO_VENTA",
            color="DEPARTAMENTO",
            title="Variabilidad de Precios por Distrito",
            labels={
                "DISTRITO": "Distrito",
                "PRECIO_VENTA": "Precio (S/)",
                "DEPARTAMENTO": "Departamento"
            },
            color_discrete_sequence=[
                DORADO,
                NARANJA,
                AZUL,
                GRIS
            ]
        )


        fig_box.update_layout(
            plot_bgcolor=BLANCO,
            paper_bgcolor=BLANCO,
            font=dict(
                color=AZUL
            ),
            title_font=dict(
                color=AZUL,
                size=20
            ),
            xaxis=dict(
                showgrid=False
            ),
            yaxis=dict(
                gridcolor=BORDE
            ),
            margin=dict(
                l=20,
                r=20,
                t=70,
                b=80
            )
        )


        st.plotly_chart(
            fig_box,
            use_container_width=True
        )


        # ====================================================
        # TABLA
        # ====================================================

        mostrar_html(
            '<div class="seccion-titulo">🏢 Detalle de Registros de Competencia</div>'
        )


        columnas_tabla = [
            "DEPARTAMENTO",
            "PROVINCIA",
            "DISTRITO",
            "RAZON",
            "DIRECCION",
            "PRODUCTO",
            "PRECIO_VENTA"
        ]


        tabla = (
            df[columnas_tabla]
            .sort_values("PRECIO_VENTA")
            .reset_index(drop=True)
        )


        st.dataframe(
            tabla,
            use_container_width=True,
            hide_index=True,
            column_config={
                "PRECIO_VENTA": st.column_config.NumberColumn(
                    "PRECIO DE VENTA",
                    format="S/ %.2f"
                )
            }
        )


    # ========================================================
    # SIN RESULTADOS
    # ========================================================

    else:

        st.warning(
            "⚠️ No se encontraron registros de precios "
            "que coincidan con los filtros seleccionados. "
            "Intenta ampliar tu selección."
        )


# ============================================================
# PANTALLA INICIAL SIN DATOS
# ============================================================

else:

    mostrar_html(
        f"""
<div class="inicio-card">
<div class="inicio-icono">📊</div>
<div class="inicio-titulo">Listo para analizar</div>
<div class="inicio-texto">Carga el archivo de precios de Osinergmin o ingresa el enlace directo para comenzar.</div>
</div>
"""
    )
