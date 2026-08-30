"""
MARCASA | app.py organizada por secciones

Esta versión conserva la aplicación estable y la divide en funciones
para facilitar cambios visuales y funcionales por módulos.
"""


import os

import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# CONFIGURACIÓN
# ============================================================
st.set_page_config(
    page_title="MARCASA | Análisis de Competencia y Precios",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="expanded",
)

DORADO = "#FFB700"
NARANJA = "#FE6902"
AZUL = "#143458"
AZUL_OSCURO = "#0F2945"
AZUL_CLARO = "#1B456F"
GRIS = "#6B7280"
GRIS_CLARO = "#F3F4F6"
BLANCO = "#FFFFFF"
NEGRO = "#111827"
BORDE = "#D9DEE7"
VERDE = "#16A34A"

# ============================================================
# CSS
# Se usan marcadores %%...%% para evitar errores de sintaxis
# por llaves CSS dentro de strings Python.
# ============================================================
CSS = """
<style>
.stApp {
    background: %%BLANCO%%;
    color: %%NEGRO%%;
}

.block-container {
    width: 100% !important;
    max-width: 1500px;
    padding: 1.2rem 2rem 3rem 2rem;
    margin: 0 auto !important;
    box-sizing: border-box;
}


/* ---------- OCULTAR BARRA SUPERIOR DE STREAMLIT ---------- */
header[data-testid="stHeader"] {
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

#MainMenu {
    visibility: hidden !important;
}

footer {
    visibility: hidden !important;
}

/* ---------- CABECERA ---------- */
.header-corporativo {
    background: linear-gradient(135deg, %%AZUL%% 0%, %%AZUL_CLARO%% 55%, %%AZUL%% 100%);
    border-left: 7px solid %%DORADO%%;
    border-radius: 14px;
    padding: 26px 30px;
    margin-bottom: 22px;
    box-shadow: 0 8px 24px rgba(20,52,88,.14);
}
.titulo-header {
    color: %%BLANCO%% !important;
    font-size: 31px;
    font-weight: 800;
    line-height: 1.2;
}
.subtitulo-header {
    color: #E8EDF4 !important;
    font-size: 15px;
    line-height: 1.55;
    margin-top: 8px;
}

/* ---------- TÍTULOS ---------- */
.seccion-titulo {
    color: %%AZUL%% !important;
    font-size: 22px;
    font-weight: 800;
    border-left: 6px solid %%NARANJA%%;
    padding-left: 12px;
    margin: 26px 0 16px 0;
}

/* ---------- TARJETAS ---------- */
.carga-card,
.filtros-card {
    background: #F8FAFC;
    border: 1px solid %%BORDE%%;
    border-top: 5px solid %%DORADO%%;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 20px;
}

.estado-datos {
    background: #ECFDF5;
    border: 1px solid #A7F3D0;
    border-left: 6px solid %%VERDE%%;
    border-radius: 12px;
    padding: 13px 18px;
    margin-bottom: 18px;
    color: #065F46 !important;
    font-weight: 700;
}

.kpi-card {
    background: %%BLANCO%%;
    border: 1px solid %%BORDE%%;
    border-radius: 13px;
    padding: 18px 20px;
    min-height: 122px;
    box-shadow: 0 4px 14px rgba(0,0,0,.06);
}

.kpi-label {
    color: %%GRIS%% !important;
    font-size: 13px;
    font-weight: 800;
}

.kpi-value {
    color: %%AZUL%% !important;
    font-size: 28px;
    font-weight: 800;
    margin-top: 9px;
}

.kpi-dorado { border-top: 5px solid %%DORADO%%; }
.kpi-naranja { border-top: 5px solid %%NARANJA%%; }
.kpi-azul { border-top: 5px solid %%AZUL%%; }
.kpi-gris { border-top: 5px solid %%GRIS%%; }

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"] {
    background: %%AZUL_OSCURO%%;
}

section[data-testid="stSidebar"] > div {
    background: %%AZUL_OSCURO%%;
}

section[data-testid="stSidebar"] * {
    color: %%BLANCO%%;
}

section[data-testid="stSidebar"] label {
    color: %%BLANCO%% !important;
    font-weight: 700 !important;
}

section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] small {
    color: #D1D5DB !important;
}

.sidebar-titulo {
    color: %%BLANCO%% !important;
    font-size: 20px;
    font-weight: 800;
    margin: 4px 0 8px 0;
}

.sidebar-ayuda {
    color: #D1D5DB !important;
    font-size: 12px;
    line-height: 1.45;
    margin-bottom: 14px;
}

.sidebar-separador {
    border-top: 1px solid rgba(255,255,255,.22);
    margin: 16px 0;
}

/* Controles del sidebar: fondo claro + texto azul */
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: %%BLANCO%% !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: %%AZUL%% !important;
}

section[data-testid="stSidebar"] [data-baseweb="popover"] * {
    color: %%AZUL%% !important;
}

section[data-testid="stSidebar"] [data-baseweb="menu"] {
    background: %%BLANCO%% !important;
}

section[data-testid="stSidebar"] [data-baseweb="option"] {
    background: %%BLANCO%% !important;
    color: %%AZUL%% !important;
}

section[data-testid="stSidebar"] [data-baseweb="option"] * {
    color: %%AZUL%% !important;
}

section[data-testid="stSidebar"] [data-baseweb="option"]:hover {
    background: #FFF4D6 !important;
}

section[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: %%NARANJA%% !important;
    color: %%BLANCO%% !important;
}

section[data-testid="stSidebar"] [data-baseweb="tag"] * {
    color: %%BLANCO%% !important;
}

/* ---------- BOTONES ---------- */
.stButton > button {
    background: %%NARANJA%% !important;
    color: %%BLANCO%% !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}

.stButton > button:hover {
    background: %%DORADO%% !important;
    color: %%AZUL%% !important;
}

/* ---------- CARGA / UPLOADER ---------- */
[data-testid="stFileUploader"] {
    border: 2px dashed %%DORADO%% !important;
    border-radius: 10px !important;
    padding: 10px !important;
    background: #FFFBEB !important;
}

/* Texto del selector de archivo: siempre oscuro y legible */
[data-testid="stFileUploader"] *,
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] p {
    color: %%AZUL%% !important;
}

/* Área interna donde Streamlit coloca el botón y el texto */
[data-testid="stFileUploader"] section {
    background: #FFFBEB !important;
    border: none !important;
}

[data-testid="stFileUploader"] section > div {
    background: #FFFBEB !important;
}

/* Botón "Browse files / Examinar" */
[data-testid="stFileUploader"] button {
    background: %%BLANCO%% !important;
    color: %%AZUL%% !important;
    border: 1px solid %%AZUL%% !important;
    border-radius: 7px !important;
    font-weight: 700 !important;
}

[data-testid="stFileUploader"] button:hover {
    background: #FFF4D6 !important;
    color: %%AZUL_OSCURO%% !important;
    border-color: %%NARANJA%% !important;
}

/* Texto de formatos y tamaño máximo */
[data-testid="stFileUploader"] small {
    color: %%GRIS%% !important;
    opacity: 1 !important;
}

/* Etiqueta encima del cargador */
[data-testid="stFileUploader"] > label {
    color: %%AZUL%% !important;
    font-weight: 800 !important;
}

/* ---------- RADIO DE ORIGEN DE DATOS ---------- */
div[role="radiogroup"] {
    color: %%AZUL%% !important;
}

div[role="radiogroup"] > label,
div[role="radiogroup"] label span,
div[role="radiogroup"] label p {
    color: %%AZUL%% !important;
    font-weight: 700 !important;
}

/* Texto auxiliar debajo de los controles de carga */
.stCaption,
[data-testid="stCaptionContainer"] {
    color: %%GRIS%% !important;
}

/* ---------- RADIO ---------- */
div[role="radiogroup"] label {
    color: %%AZUL%% !important;
    font-weight: 700 !important;
}

/* ---------- SELECTS DEL ÁREA PRINCIPAL ---------- */
[data-testid="stMultiSelect"] label,
[data-testid="stSelectbox"] label {
    color: %%AZUL%% !important;
    font-weight: 800 !important;
}

[data-baseweb="select"] > div {
    background: %%BLANCO%% !important;
    border: 1px solid %%BORDE%% !important;
    border-radius: 9px !important;
}

[data-baseweb="select"] * {
    color: %%AZUL%% !important;
}

[data-baseweb="popover"] * {
    color: %%AZUL%% !important;
}

[data-baseweb="menu"],
[data-baseweb="option"] {
    background: %%BLANCO%% !important;
}

[data-baseweb="option"],
[data-baseweb="option"] * {
    color: %%AZUL%% !important;
}

[data-baseweb="option"]:hover {
    background: #FFF4D6 !important;
}

[data-baseweb="tag"] {
    background: %%NARANJA%% !important;
    color: %%BLANCO%% !important;
}

[data-baseweb="tag"] * {
    color: %%BLANCO%% !important;
}

/* ---------- MENSAJES ---------- */
div[data-testid="stAlert"] {
    border-radius: 10px;
}

/* ---------- RESPONSIVE ---------- */
/* ---------- RESPONSIVE: TABLET ---------- */
@media (max-width: 900px) {
    .block-container {
        width: 100% !important;
        max-width: 100% !important;
        padding: .8rem 1rem 2rem 1rem !important;
        margin: 0 auto !important;
    }

    .titulo-header {
        font-size: 23px;
    }

    .subtitulo-header {
        font-size: 13px;
    }

    .seccion-titulo {
        font-size: 19px;
    }

    .kpi-value {
        font-size: 24px;
    }

    .header-corporativo {
        padding: 20px;
    }

    section[data-testid="stSidebar"] {
        width: 300px !important;
    }

    [data-testid="stDataFrame"] {
        max-width: 100% !important;
        overflow-x: auto !important;
    }
}

/* ---------- RESPONSIVE: CELULAR ---------- */
@media (max-width: 640px) {
    .block-container {
        padding: .55rem .65rem 1.5rem .65rem !important;
    }

    .header-corporativo {
        width: 100% !important;
        box-sizing: border-box !important;
        padding: 18px 16px !important;
        margin-bottom: 14px !important;
        border-left-width: 5px !important;
        border-radius: 11px !important;
    }

    .titulo-header {
        font-size: 20px !important;
        line-height: 1.18 !important;
        word-break: normal !important;
    }

    .subtitulo-header {
        font-size: 12px !important;
        line-height: 1.4 !important;
        margin-top: 7px !important;
    }

    .seccion-titulo {
        font-size: 18px !important;
        line-height: 1.25 !important;
        padding-left: 9px !important;
        margin: 18px 0 12px 0 !important;
    }

    .carga-card,
    .filtros-card {
        padding: 15px 14px !important;
        border-radius: 11px !important;
    }

    .kpi-card {
        min-height: 95px !important;
        padding: 13px 14px !important;
    }

    .kpi-label {
        font-size: 11px !important;
    }

    .kpi-value {
        font-size: 21px !important;
        margin-top: 6px !important;
    }

    /* Los controles ocupan todo el ancho disponible. */
    [data-testid="stButton"] > button,
    .stButton > button,
    [data-testid="stTextInput"] input,
    [data-testid="stFileUploader"],
    [data-baseweb="select"] {
        max-width: 100% !important;
        box-sizing: border-box !important;
    }

    /* Radio de origen en columna para no deformarse. */
    div[role="radiogroup"] {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 8px !important;
    }

    /* Sidebar adaptable al ancho del teléfono. */
    section[data-testid="stSidebar"] {
        width: 88vw !important;
        max-width: 340px !important;
    }

    /* Evita desbordamiento horizontal de tablas y gráficos. */
    .element-container,
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    [data-testid="stPlotlyChart"],
    [data-testid="stDataFrame"] {
        max-width: 100% !important;
        box-sizing: border-box !important;
    }

    [data-testid="stPlotlyChart"] {
        overflow-x: hidden !important;
    }

    /* Texto largo no debe provocar scroll horizontal. */
    p, span, label, div {
        overflow-wrap: anywhere;
    }
}

/* ---------- CONTENCIÓN GENERAL ---------- */
html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] > .main {
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: hidden !important;
}

[data-testid="stAppViewContainer"] > .main {
    padding-top: 0 !important;
}

.main .block-container {
    padding-top: 1rem !important;
}

@media (max-width: 640px) {
    .main .block-container {
        padding-top: .5rem !important;
    }
}

.preview-banner {
    background: #FFF7D6;
    border: 1px solid #F4C542;
    border-left: 6px solid %%DORADO%%;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 18px;
    color: %%AZUL%% !important;
    font-size: 14px;
}
.preview-footer {
    margin-top: 30px;
    padding: 12px 14px;
    border-top: 1px solid %%BORDE%%;
    color: %%GRIS%% !important;
    font-size: 12px;
    text-align: center;
}

</style>
"""

for nombre, valor in {
    "BLANCO": BLANCO,
    "NEGRO": NEGRO,
    "AZUL": AZUL,
    "AZUL_OSCURO": AZUL_OSCURO,
    "AZUL_CLARO": AZUL_CLARO,
    "DORADO": DORADO,
    "NARANJA": NARANJA,
    "GRIS": GRIS,
    "BORDE": BORDE,
    "VERDE": VERDE,
}.items():
    CSS = CSS.replace(f"%%{nombre}%%", valor)

st.markdown(CSS, unsafe_allow_html=True)
# ============================================================
# 01. CONFIGURACIÓN DE DESARROLLO / PREVISUALIZACIÓN
# ============================================================
# False = aplicación normal para usuarios.
# True  = modo diseño con datos ficticios y selector de secciones.
# Mientras estés diseñando, cambia solo esta variable a True.
# Al publicar para usuarios, vuelve a False.
PREVISUALIZACION = False

SECCIONES_PREVIEW = [
    "Vista completa",
    "Cabecera",
    "Carga de datos",
    "Panel lateral / filtros",
    "Estado + resumen de filtros",
    "Indicadores",
    "Gráfico comparativo",
    "Gráfico de distribución",
    "Tabla",
]


# ============================================================
# 02. ESTADO DE SESIÓN
# ============================================================
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "df_data" not in st.session_state:
    st.session_state.df_data = None
if "fuente_datos" not in st.session_state:
    st.session_state.fuente_datos = ""


def verificar_password():
    """Valida el acceso al sistema."""
    if st.session_state.autenticado:
        return True

    st.markdown(
        f"""
        <div style="
            max-width:560px;
            margin:60px auto 20px auto;
            padding:38px;
            background:{BLANCO};
            border-radius:15px;
            border-top:7px solid {DORADO};
            box-shadow:0 5px 25px rgba(0,0,0,.10);
            text-align:center;">
            <div style="font-size:52px;">⛽</div>
            <div style="color:{AZUL};font-size:30px;font-weight:800;">MARCASA</div>
            <div style="color:{GRIS};font-size:15px;margin-top:8px;">
                Sistema de Análisis de Competencia y Precios
            </div>
            <div style="color:{AZUL};font-size:13px;margin-top:14px;font-weight:700;">
                Acceso autorizado
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    password = st.text_input(
        "Contraseña de acceso",
        type="password",
        key="login_password",
        placeholder="Ingresa tu contraseña",
    )

    if st.button("🔐 Ingresar al sistema", width="stretch"):
        if password == "Marcasa2026":
            st.session_state.autenticado = True
            st.session_state.pop("login_password", None)
            st.rerun()
        else:
            st.error("❌ Contraseña incorrecta.")

    return False


# FUNCIONES DE DATOS
# ============================================================
COLUMNAS_REQUERIDAS = [
    "PRECIO_VENTA",
    "DEPARTAMENTO",
    "PROVINCIA",
    "DISTRITO",
    "PRODUCTO",
    "RAZON",
    "DIRECCION",
]


@st.cache_data(show_spinner=False)
def leer_excel(origen):
    try:
        return pd.read_excel(origen)
    except Exception as e:
        st.error(f"❌ No fue posible cargar el Excel: {e}")
        return None


def preparar_dataframe(df_original):
    if df_original is None:
        return None

    df = df_original.copy()

    faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in df.columns]

    if faltantes:
        st.error(
            "❌ El archivo no contiene las columnas necesarias: "
            + ", ".join(faltantes)
        )
        return None

    for columna in [
        "DEPARTAMENTO",
        "PROVINCIA",
        "DISTRITO",
        "PRODUCTO",
        "RAZON",
        "DIRECCION",
    ]:
        df[columna] = (
            df[columna]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    df["PRECIO_VENTA"] = (
        df["PRECIO_VENTA"]
        .astype(str)
        .str.replace("S/", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    df["PRECIO_VENTA"] = pd.to_numeric(
        df["PRECIO_VENTA"],
        errors="coerce",
    )

    df = df.dropna(subset=["PRECIO_VENTA"]).copy()

    return df


def limpiar_filtros():
    for key in [
        "filtro_departamento",
        "filtro_provincia",
        "filtro_distrito",
        "filtro_producto",
    ]:
        st.session_state.pop(key, None)
def renderizar_cabecera():
    """Renderiza el encabezado corporativo y el logo."""
    col_logo, col_header = st.columns([1, 5], vertical_alignment="center")

    with col_logo:
        logo_encontrado = next(
            (
                nombre
                for nombre in [
                    "logo.png",
                    "logo.png.png",
                    "Logo.png",
                    "LOGO.png",
                ]
                if os.path.exists(nombre)
            ),
            None,
        )

        if logo_encontrado:
            st.image(logo_encontrado, width=145)
        else:
            st.markdown(
                "<div style='font-size:55px;text-align:center;'>⛽</div>",
                unsafe_allow_html=True,
            )

    with col_header:
        st.markdown(
            f"""
            <div class="header-corporativo">
                <div class="titulo-header">
                    Análisis Inteligente de Competencia y Precios
                </div>
                <div class="subtitulo-header">
                    Monitoreo estratégico de precios de combustibles
                    · Información de mercado · Análisis comparativo
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def renderizar_carga_datos():
    """Renderiza la carga real de Excel o enlace directo. Se detiene hasta que exista data procesada."""
    if st.session_state.df_data is None:

        st.markdown(
            '<div class="seccion-titulo">📁 Cargar información de precios</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="carga-card">
                <div style="color:{AZUL};font-size:18px;font-weight:800;">
                    Fuente de información
                </div>
                <div style="color:{GRIS};margin-top:7px;line-height:1.5;">
                    Carga los precios de Osinergmin mediante un archivo Excel
                    o mediante un enlace directo al archivo Excel.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        origen = st.radio(
            "Selecciona cómo ingresar los datos:",
            ["Archivo Excel", "Enlace directo de Osinergmin"],
            key="origen_datos_principal",
            horizontal=True,
        )

        if origen == "Archivo Excel":

            archivo = st.file_uploader(
                "Selecciona el archivo Excel de Osinergmin",
                type=["xlsx", "xls"],
                key="archivo_local",
                help="Se aceptan archivos .xlsx y .xls",
            )

            if archivo is not None:
                st.caption(f"Archivo seleccionado: {archivo.name}")

                if st.button(
                    "📥 Procesar archivo y abrir análisis",
                    type="primary",
                    width="stretch",
                ):
                    with st.spinner("Procesando información..."):
                        df_cargado = leer_excel(archivo)

                    if df_cargado is not None:
                        df_preparado = preparar_dataframe(df_cargado)

                        if (
                            df_preparado is not None
                            and not df_preparado.empty
                        ):
                            st.session_state.df_data = df_preparado
                            st.session_state.fuente_datos = (
                                f"Archivo: {archivo.name}"
                            )
                            limpiar_filtros()
                            st.rerun()
                        else:
                            st.error(
                                "❌ El archivo no contiene registros "
                                "con precios válidos."
                            )

        else:

            url = st.text_input(
                "Pega el enlace directo de descarga del Excel de Osinergmin:",
                key="url_osinergmin",
                placeholder="https://...",
            )

            st.caption(
                "El enlace debe apuntar directamente al archivo Excel (.xlsx o .xls)."
            )

            if st.button(
                "🌐 Descargar y procesar información",
                type="primary",
                width="stretch",
            ):
                if not url.strip():
                    st.warning("⚠️ Ingresa primero el enlace de Osinergmin.")
                else:
                    with st.spinner(
                        "Descargando y procesando información..."
                    ):
                        df_cargado = leer_excel(url.strip())

                    if df_cargado is not None:
                        df_preparado = preparar_dataframe(df_cargado)

                        if (
                            df_preparado is not None
                            and not df_preparado.empty
                        ):
                            st.session_state.df_data = df_preparado
                            st.session_state.fuente_datos = (
                                "Enlace directo de Osinergmin"
                            )
                            limpiar_filtros()
                            st.rerun()
                        else:
                            st.error(
                                "❌ El archivo descargado no contiene "
                                "registros con precios válidos."
                            )

        st.markdown(
            f"""
            <div style="
                background:{GRIS_CLARO};
                border-left:6px solid {DORADO};
                border-radius:14px;
                padding:35px;
                text-align:center;
                margin-top:25px;">
                <div style="font-size:46px;">📊</div>
                <div style="color:{AZUL};font-size:25px;font-weight:800;">
                    Listo para analizar
                </div>
                <div style="color:{GRIS};font-size:15px;line-height:1.6;margin-top:8px;">
                    Una vez procesada la información, esta pantalla desaparecerá
                    y quedará disponible el panel de filtros y el análisis interactivo.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.stop()


def aplicar_filtros(df_base, departamentos_seleccionados, provincias_seleccionadas, distritos_seleccionados, producto_seleccionado):
    """Aplica los filtros jerárquicos y devuelve el DataFrame resultante."""
    # ============================================================
    # APLICAR FILTROS
    # ============================================================
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

    if producto_seleccionado != "Todos los combustibles":
        df = df[
            df["PRODUCTO"] == producto_seleccionado
        ]

    # ============================================================
    return df


def renderizar_resumen_filtros(departamentos_seleccionados, provincias_seleccionadas, distritos_seleccionados, producto_seleccionado):
    """Muestra si la vista es general o qué filtros están activos."""
    # ============================================================
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

    if producto_seleccionado != "Todos los combustibles":
        filtros_activos.append(
            "Combustible: "
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


def renderizar_kpis(df):
    """Muestra los indicadores principales de la selección actual."""
    precio_min = float(df["PRECIO_VENTA"].min())
    precio_promedio = float(df["PRECIO_VENTA"].mean())
    precio_max = float(df["PRECIO_VENTA"].max())
    brecha = precio_max - precio_min

    estaciones = int(
        df["RAZON"]
        .replace("", pd.NA)
        .dropna()
        .nunique()
    )

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(
            f"""
            <div class="kpi-card kpi-dorado">
                <div class="kpi-label">💵 PRECIO MÍNIMO</div>
                <div class="kpi-value">S/ {precio_min:.2f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k2:
        st.markdown(
            f"""
            <div class="kpi-card kpi-naranja">
                <div class="kpi-label">📈 PRECIO PROMEDIO</div>
                <div class="kpi-value">S/ {precio_promedio:.2f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k3:
        st.markdown(
            f"""
            <div class="kpi-card kpi-azul">
                <div class="kpi-label">📉 PRECIO MÁXIMO</div>
                <div class="kpi-value">S/ {precio_max:.2f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k4:
        st.markdown(
            f"""
            <div class="kpi-card kpi-gris">
                <div class="kpi-label">🏢 ESTACIONES ANALIZADAS</div>
                <div class="kpi-value">{estaciones:,}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.metric(
        "Brecha entre precio máximo y mínimo",
        f"S/ {brecha:.2f}",
        help=(
            "Diferencia entre el precio máximo y mínimo "
            "de la selección actual."
        ),
    )


def renderizar_grafico_comparativo(df):
    """Muestra la comparativa de precios promedio por distrito y competidor."""
    st.markdown(
        '<div class="seccion-titulo">'
        "🏆 Comparativa de precios por distrito y competidor"
        "</div>",
        unsafe_allow_html=True,
    )

    grafico = (
        df.groupby(
            ["DISTRITO", "RAZON"],
            as_index=False
        )["PRECIO_VENTA"]
        .mean()
        .sort_values("PRECIO_VENTA")
    )

    if not grafico.empty:

        fig_bar = px.bar(
            grafico,
            x="DISTRITO",
            y="PRECIO_VENTA",
            color="RAZON",
            barmode="group",
            labels={
                "DISTRITO": "Distrito",
                "PRECIO_VENTA": "Precio promedio (S/)",
                "RAZON": "Competidor",
            },
            hover_data={
                "PRECIO_VENTA": ":.2f"
            },
        )

        fig_bar.update_layout(
            plot_bgcolor=BLANCO,
            paper_bgcolor=BLANCO,
            font=dict(
                color=AZUL,
                size=12
            ),
            title=dict(
                text="Precio promedio por distrito y competidor",
                font=dict(
                    color=AZUL,
                    size=20
                ),
            ),
            xaxis=dict(
                title="Distrito",
                showgrid=False,
                tickfont=dict(color=AZUL),
                title_font=dict(color=AZUL),
            ),
            yaxis=dict(
                title="Precio promedio (S/)",
                gridcolor=BORDE,
                tickfont=dict(color=AZUL),
                title_font=dict(color=AZUL),
            ),
            legend=dict(
                title=dict(
                    text="Competidor",
                    font=dict(color=AZUL),
                ),
                font=dict(
                    color=AZUL,
                    size=12
                ),
                bgcolor="rgba(255,255,255,0.95)",
                bordercolor=BORDE,
                borderwidth=1,
            ),
            hoverlabel=dict(
                bgcolor=BLANCO,
                font=dict(color=NEGRO),
            ),
            margin=dict(
                l=20,
                r=20,
                t=70,
                b=100
            ),
        )

        fig_bar.update_xaxes(
            tickangle=-45
        )

        st.plotly_chart(
            fig_bar,
            width="stretch",
            config={
                "displayModeBar": True
            },
        )


def renderizar_grafico_distribucion(df):
    """Muestra la distribución y dispersión de precios."""
    st.markdown(
        '<div class="seccion-titulo">'
        "📦 Distribución y dispersión de precios"
        "</div>",
        unsafe_allow_html=True,
    )

    fig_box = px.box(
        df,
        x="DISTRITO",
        y="PRECIO_VENTA",
        color="DEPARTAMENTO",
        labels={
            "DISTRITO": "Distrito",
            "PRECIO_VENTA": "Precio (S/)",
            "DEPARTAMENTO": "Departamento",
        },
        points="outliers",
    )

    fig_box.update_layout(
        plot_bgcolor=BLANCO,
        paper_bgcolor=BLANCO,
        font=dict(
            color=AZUL,
            size=12
        ),
        title=dict(
            text="Distribución de precios por distrito",
            font=dict(
                color=AZUL,
                size=20
            ),
        ),
        xaxis=dict(
            title="Distrito",
            showgrid=False,
            tickfont=dict(color=AZUL),
            title_font=dict(color=AZUL),
        ),
        yaxis=dict(
            title="Precio (S/)",
            gridcolor=BORDE,
            tickfont=dict(color=AZUL),
            title_font=dict(color=AZUL),
        ),
        legend=dict(
            font=dict(color=AZUL),
            bgcolor="rgba(255,255,255,0.95)",
        ),
        margin=dict(
            l=20,
            r=20,
            t=70,
            b=100
        ),
    )

    fig_box.update_xaxes(
        tickangle=-45
    )

    st.plotly_chart(
        fig_box,
        width="stretch",
        config={
            "displayModeBar": True
        },
    )


def renderizar_tabla(df):
    """Muestra el detalle de registros de competencia."""
    st.markdown(
        '<div class="seccion-titulo">'
        "🏢 Detalle de registros de competencia"
        "</div>",
        unsafe_allow_html=True,
    )

    columnas_tabla = [
        "DEPARTAMENTO",
        "PROVINCIA",
        "DISTRITO",
        "RAZON",
        "DIRECCION",
        "PRODUCTO",
        "PRECIO_VENTA",
    ]

    tabla = (
        df[columnas_tabla]
        .sort_values("PRECIO_VENTA")
        .reset_index(drop=True)
    )

    tabla["PRECIO_VENTA"] = (
        tabla["PRECIO_VENTA"].round(2)
    )

    st.dataframe(
        tabla,
        width="stretch",
        hide_index=True,
        column_config={
            "PRECIO_VENTA": st.column_config.NumberColumn(
                "PRECIO DE VENTA (S/)",
                format="S/ %.2f",
            ),
        },
    )

    st.caption(
        f"Mostrando {len(df):,} registros después de aplicar los filtros."
    )


def renderizar_sidebar(df_base, modo_preview=False):
    """Renderiza el panel lateral y devuelve los cuatro filtros seleccionados."""
    with st.sidebar:

        st.markdown(
            """
            <div style="text-align:center;padding:5px 0 15px 0;">
                <div style="font-size:38px;">📊</div>
                <div class="sidebar-titulo">Panel de Análisis</div>
                <div class="sidebar-ayuda">
                    MARCASA · Competencia y precios
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style="
                background:rgba(255,255,255,.08);
                border:1px solid rgba(255,255,255,.18);
                border-radius:10px;
                padding:12px;">
                <div style="color:#FFFFFF;font-weight:800;">
                    ✅ Datos procesados
                </div>
                <div style="color:#D1D5DB;font-size:12px;margin-top:7px;">
                    {len(df_base):,} registros analizados
                </div>
                <div style="color:#D1D5DB;font-size:12px;margin-top:4px;">
                    Fuente: {st.session_state.fuente_datos}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-separador"></div>',
            unsafe_allow_html=True,
        )

        st.markdown("### 🔎 Filtros de análisis")

        st.markdown(
            '<div class="sidebar-ayuda">'
            "Selecciona uno o varios criterios. "
            "Si un filtro queda vacío, se considera toda la información."
            "</div>",
            unsafe_allow_html=True,
        )

        # 1. DEPARTAMENTO
        departamentos_disponibles = sorted(
            x
            for x in df_base["DEPARTAMENTO"].unique()
            if str(x).strip()
        )

        departamentos_seleccionados = st.multiselect(
            "1. Región / Departamento",
            options=departamentos_disponibles,
            default=[],
            placeholder="Seleccionar departamentos...",
            key="filtro_departamento",
        )

        # 2. PROVINCIA
        df_provincias = (
            df_base[
                df_base["DEPARTAMENTO"].isin(
                    departamentos_seleccionados
                )
            ]
            if departamentos_seleccionados
            else df_base
        )

        provincias_disponibles = sorted(
            x
            for x in df_provincias["PROVINCIA"].unique()
            if str(x).strip()
        )

        provincias_seleccionadas = st.multiselect(
            "2. Provincia",
            options=provincias_disponibles,
            default=[],
            placeholder="Seleccionar provincias...",
            key="filtro_provincia",
        )

        # 3. DISTRITO
        df_distritos = (
            df_provincias[
                df_provincias["PROVINCIA"].isin(
                    provincias_seleccionadas
                )
            ]
            if provincias_seleccionadas
            else df_provincias
        )

        distritos_disponibles = sorted(
            x
            for x in df_distritos["DISTRITO"].unique()
            if str(x).strip()
        )

        distritos_seleccionados = st.multiselect(
            "3. Distrito",
            options=distritos_disponibles,
            default=[],
            placeholder="Seleccionar distritos...",
            key="filtro_distrito",
        )

        # 4. COMBUSTIBLE
        productos_existentes = sorted(
            x
            for x in df_base["PRODUCTO"].unique()
            if str(x).strip()
        )

        productos_preferidos = [
            "GASOHOL REGULAR",
            "GASOHOL PREMIUM",
            "DIESEL B5 UV",
            "Diesel B5 S-50 UV",
        ]

        productos_disponibles = [
            p for p in productos_preferidos
            if p in productos_existentes
        ]

        productos_disponibles += [
            p
            for p in productos_existentes
            if p not in productos_disponibles
        ]

        producto_seleccionado = st.selectbox(
            "4. Combustible",
            options=["Todos los combustibles"] + productos_disponibles,
            index=0,
            key="filtro_producto",
        )

        st.markdown(
            '<div class="sidebar-separador"></div>',
            unsafe_allow_html=True,
        )

        if not modo_preview:
            if st.button(
                "🔄 Cambiar / actualizar datos",
                width="stretch",
                key="btn_actualizar",
            ):
                st.session_state.df_data = None
                st.session_state.fuente_datos = ""
                limpiar_filtros()
                st.session_state.pop("archivo_local", None)
                st.session_state.pop("url_osinergmin", None)
                st.rerun()

    return (
        departamentos_seleccionados,
        provincias_seleccionadas,
        distritos_seleccionados,
        producto_seleccionado,
    )


def crear_dataframe_previsualizacion():
    """Crea datos ficticios pequeños para revisar diseño sin cargar el Excel real."""
    return pd.DataFrame({
        "DEPARTAMENTO": ["LA LIBERTAD", "LA LIBERTAD", "CAJAMARCA", "CAJAMARCA", "LA LIBERTAD", "LA LIBERTAD"],
        "PROVINCIA": ["CAJABAMBA", "CAJABAMBA", "CAJAMARCA", "CAJAMARCA", "CAJABAMBA", "CAJABAMBA"],
        "DISTRITO": ["MARCABAL", "MARCABAL", "CAJAMARCA", "CAJAMARCA", "MARCABAL", "MARCABAL"],
        "RAZON": ["ESTACIÓN A", "ESTACIÓN B", "ESTACIÓN C", "ESTACIÓN D", "ESTACIÓN E", "ESTACIÓN F"],
        "DIRECCION": ["Carretera principal"] * 6,
        "PRODUCTO": ["DIESEL B5 UV", "DIESEL B5 UV", "GASOHOL REGULAR", "GASOHOL REGULAR", "GASOHOL PREMIUM", "DIESEL B5 UV"],
        "PRECIO_VENTA": [14.50, 15.20, 16.10, 16.40, 17.20, 14.90],
    })


def renderizar_preview_carga():
    """Previsualización visual de la pantalla de carga; no procesa archivos."""
    st.markdown('<div class="seccion-titulo">📁 Cargar información de precios</div>', unsafe_allow_html=True)
    st.markdown(
        f'''<div class="carga-card"><div style="color:{AZUL};font-size:18px;font-weight:800;">Fuente de información</div><div style="color:{GRIS};margin-top:7px;line-height:1.5;">Carga los precios de Osinergmin mediante un archivo Excel o mediante un enlace directo al archivo Excel.</div></div>''',
        unsafe_allow_html=True,
    )
    st.radio(
        "Selecciona cómo ingresar los datos:",
        ["Archivo Excel", "Enlace directo de Osinergmin"],
        index=0,
        key="preview_origen",
        horizontal=True,
    )
    st.file_uploader(
        "Selecciona el archivo Excel de Osinergmin",
        type=["xlsx", "xls"],
        key="preview_archivo",
        help="Se aceptan archivos .xlsx y .xls",
    )
    st.markdown(
        f'''<div style="background:{GRIS_CLARO};border-left:6px solid {DORADO};border-radius:14px;padding:35px;text-align:center;margin-top:25px;"><div style="font-size:46px;">📊</div><div style="color:{AZUL};font-size:25px;font-weight:800;">Listo para analizar</div><div style="color:{GRIS};font-size:15px;line-height:1.6;margin-top:8px;">Esta es una previsualización. En la aplicación real, esta pantalla desaparece al procesar la información.</div></div>''',
        unsafe_allow_html=True,
    )


def renderizar_preview(modo_seccion):
    """Muestra una sección aislada o toda la interfaz usando datos ficticios."""
    df_preview = crear_dataframe_previsualizacion()
    st.session_state.fuente_datos = "Modo previsualización"
    st.markdown(
        '''<div class="preview-banner">🛠️ <b>MODO PREVISUALIZACIÓN</b> · Los datos son ficticios y solo sirven para revisar el diseño.</div>''',
        unsafe_allow_html=True,
    )

    if modo_seccion == "Cabecera":
        renderizar_cabecera()
    elif modo_seccion == "Carga de datos":
        renderizar_preview_carga()
    elif modo_seccion == "Panel lateral / filtros":
        renderizar_sidebar(df_preview, modo_preview=True)
    elif modo_seccion == "Estado + resumen de filtros":
        st.markdown(f'''<div class="estado-datos">✅ Información procesada correctamente · {len(df_preview):,} registros disponibles para análisis</div>''', unsafe_allow_html=True)
        st.markdown('<div class="seccion-titulo">🔎 Filtros de análisis</div>', unsafe_allow_html=True)
        st.markdown(f'''<div class="filtros-card"><b style="color:{AZUL};">Los filtros están en el panel izquierdo.</b> Selecciona departamento, provincia, distrito y/o combustible.</div>''', unsafe_allow_html=True)
        renderizar_resumen_filtros([], [], [], "Todos los combustibles")
    elif modo_seccion == "Indicadores":
        renderizar_kpis(df_preview)
    elif modo_seccion == "Gráfico comparativo":
        renderizar_grafico_comparativo(df_preview)
    elif modo_seccion == "Gráfico de distribución":
        renderizar_grafico_distribucion(df_preview)
    elif modo_seccion == "Tabla":
        renderizar_tabla(df_preview)
    else:
        renderizar_cabecera()
        renderizar_kpis(df_preview)
        renderizar_grafico_comparativo(df_preview)
        renderizar_grafico_distribucion(df_preview)
        renderizar_tabla(df_preview)

    st.markdown(
        '''<div class="preview-footer">Fin de la previsualización · Para volver a la aplicación normal cambia <code>PREVISUALIZACION = False</code>.</div>''',
        unsafe_allow_html=True,
    )

# ============================================================
# 03. ARRANQUE
# ============================================================
if PREVISUALIZACION:
    modo_seccion = st.sidebar.selectbox(
        "🛠️ Sección a previsualizar",
        SECCIONES_PREVIEW,
        index=0,
        key="seccion_preview",
    )
    renderizar_preview(modo_seccion)
    st.stop()

# ============================================================
# 04. AUTENTICACIÓN
# ============================================================
if not verificar_password():
    st.stop()

# ============================================================
# 05. CABECERA
# ============================================================
renderizar_cabecera()

# ============================================================
# 06. CARGA DE DATOS
# ============================================================
if st.session_state.df_data is None:
    renderizar_carga_datos()
    st.stop()

# ============================================================
# 07. DATA PROCESADA
# ============================================================
df_base = st.session_state.df_data.copy()

# ============================================================
# 08. PANEL LATERAL + FILTROS
# ============================================================
(
    departamentos_seleccionados,
    provincias_seleccionadas,
    distritos_seleccionados,
    producto_seleccionado,
) = renderizar_sidebar(df_base)

# ============================================================
# 09. ESTADO Y RESUMEN
# ============================================================
st.markdown(
    f'''<div class="estado-datos">✅ Información procesada correctamente · {len(df_base):,} registros disponibles para análisis</div>''',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="seccion-titulo">🔎 Filtros de análisis</div>',
    unsafe_allow_html=True,
)

st.markdown(
    f'''<div class="filtros-card"><b style="color:{AZUL};">Los filtros están en el panel izquierdo.</b> Selecciona departamento, provincia, distrito y/o combustible. Los campos vacíos no limitan la información.</div>''',
    unsafe_allow_html=True,
)

df = aplicar_filtros(
    df_base,
    departamentos_seleccionados,
    provincias_seleccionadas,
    distritos_seleccionados,
    producto_seleccionado,
)

renderizar_resumen_filtros(
    departamentos_seleccionados,
    provincias_seleccionadas,
    distritos_seleccionados,
    producto_seleccionado,
)

# ============================================================
# 10. RESULTADOS + INDICADORES
# ============================================================
st.markdown(
    '<div class="seccion-titulo">📊 Análisis comparativo de competencia</div>',
    unsafe_allow_html=True,
)

if df.empty:
    st.warning(
        "⚠️ No se encontraron registros para los filtros seleccionados. Amplía la selección."
    )
    st.stop()

renderizar_kpis(df)

# ============================================================
# 11. GRÁFICOS INTERACTIVOS
# ============================================================
renderizar_grafico_comparativo(df)
renderizar_grafico_distribucion(df)

# ============================================================
# 12. TABLA DETALLADA
# ============================================================
renderizar_tabla(df)

# ============================================================
# 13. PIE DE PÁGINA
# ============================================================
st.divider()
st.caption("MARCASA · Sistema de Análisis de Competencia y Precios")
