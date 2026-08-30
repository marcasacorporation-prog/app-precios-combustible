import streamlit as st
import pandas as pd
import plotly.express as px

def verificar_password():
    def password_entered():
        if st.session_state["password"] == "Marcasacorporation2026":  # Cambia '123456' por tu contraseña
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Ingresa la contraseña para acceder al aplicativo:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Ingresa la contraseña para acceder al aplicativo:", type="password", on_change=password_entered, key="password")
        st.error("😕 Contraseña incorrecta")
        return False
    else:
        return True

if not verificar_password():
    st.stop()

# Configuración inicial de la página
st.set_page_config(page_title="Análisis de Competencia - Combustible")
st.title("⛽ Análisis de Competencia - Precios de Combustibles")

# Selector de origen de datos
st.subheader("Selecciona cómo ingresar los datos:")
opcion_fuente = st.radio(
    "Elige una opción:",
    ("Subir archivo Excel local", "Ingresar enlace URL de Osinergmin")
)

df = None

if opcion_fuente == "Subir archivo Excel local":
    archivo_subido = st.file_uploader("Sube el archivo 'Ultimos-Precios-Registrados-EVPC.xlsx'", type=["xlsx"])
    if archivo_subido is not None:
        @st.cache_data
        def cargar_excel(file):
            return pd.read_excel(file)
        df = cargar_excel(archivo_subido)
else:
    url_input = st.text_input("Ingresa la URL directa del archivo Excel de Osinergmin:")
    if url_input:
        @st.cache_data
        def cargar_url(url):
            return pd.read_excel(url)
        df = cargar_url(url_input)

if df is not None:
    st.success("¡Datos cargados exitosamente!")
    # Aquí continúan tus filtros y tablas de análisis...
# Configuración inicial de la página
st.set_page_config(page_title="Análisis de Competencia - Combustibles", layout="wide")
st.title("⛽ Análisis de Competencia - Precios de Combustibles")

# Función para cargar datos de manera eficiente
@st.cache_data
def load_data(file_or_url):
    try:
        df = pd.read_excel(file_or_url)
        return df
    except Exception as e:
        st.error(f"Error al cargar la data: {e}")
        return None

# Panel principal: Selector de origen de datos
origen = st.radio("Selecciona cómo ingresar los datos:", ["Subir archivo Excel local", "Ingresar enlace URL de Osinergmin"])

df = None
if origen == "Subir archivo Excel local":
    uploaded_file = st.file_uploader("Sube el archivo 'Ultimos-Precios-Registrados-EVPC.xlsx'", type=["xlsx"])
    if uploaded_file:
        df = load_data(uploaded_file)
else:
    url = st.text_input("Pega el enlace de descarga directa del Excel:")
    if url:
        df = load_data(url)

if df is not None:
    # Limpiar filas sin precios
    df = df.dropna(subset=['PRECIO_VENTA'])
    
    st.sidebar.header("📍 Filtros de Ubicación")
    
    # Filtro: Departamento
    departamentos = df['DEPARTAMENTO'].dropna().unique()
    departamento = st.sidebar.selectbox("1. Departamento", ["Todos"] + list(departamentos))
    if departamento != "Todos":
        df = df[df['DEPARTAMENTO'] == departamento]
        
    # Filtro: Provincia
    provincias = df['PROVINCIA'].dropna().unique()
    provincia = st.sidebar.selectbox("2. Provincia", ["Todas"] + list(provincias))
    if provincia != "Todas":
        df = df[df['PROVINCIA'] == provincia]
        
    # Filtro: Distrito
    distritos = df['DISTRITO'].dropna().unique()
    distrito = st.sidebar.selectbox("3. Distrito", ["Todos"] + list(distritos))
    if distrito != "Todos":
        df = df[df['DISTRITO'] == distrito]

    st.sidebar.header("🛢️ Filtro de Producto")
    # Los productos principales de tu interés
    productos_clave = ['GASOHOL REGULAR', 'GASOHOL PREMIUM', 'Diesel B5 S-50 UV', 'DIESEL B5 UV']
    producto = st.sidebar.selectbox("Selecciona el combustible a analizar", ["Todos"] + productos_clave)
    
    if producto != "Todos":
        df = df[df['PRODUCTO'].str.contains(producto, case=False, na=False)]
    
    # Resultados y Analítica
    if not df.empty:
        st.subheader(f"📊 Resumen de Mercado: {distrito if distrito != 'Todos' else 'Zona Seleccionada'}")
        
        # Tarjetas de indicadores
        col1, col2, col3 = st.columns(3)
        col1.metric("Precio Más Bajo", f"S/ {df['PRECIO_VENTA'].min():.2f}")
        col2.metric("Precio Promedio", f"S/ {df['PRECIO_VENTA'].mean():.2f}")
        col3.metric("Precio Más Alto", f"S/ {df['PRECIO_VENTA'].max():.2f}")
        
        # Gráfico comparativo
        st.write("### 📉 Comparativa Gráfica de Competidores")
        fig = px.bar(df.sort_values('PRECIO_VENTA'), x='RAZON', y='PRECIO_VENTA', color='PRODUCTO', 
                     title="Estructura de Precios por Estación de Servicio",
                     labels={'RAZON': 'Competidor', 'PRECIO_VENTA': 'Precio (S/)'})
        st.plotly_chart(fig, use_container_width=True)

        # Tabla de detalles
        st.write("### 🏢 Lista de Precios al Detalle")
        st.dataframe(df[['RAZON', 'DIRECCION', 'PRODUCTO', 'PRECIO_VENTA']].sort_values('PRECIO_VENTA'))
        
    else:
        st.warning("No hay registros en la base de datos para los filtros seleccionados.")