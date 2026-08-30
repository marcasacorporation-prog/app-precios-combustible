import streamlit as st
import pandas as pd
import plotly.express as px

# --- SISTEMA DE CONTRASEÑA ---
def verificar_password():
    def password_entered():
        if st.session_state["password"] == "Marcasa2026":
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
# -----------------------------

# Configuración inicial de la página
st.set_page_config(page_title="Análisis Avanzado - Precios de Combustibles", layout="wide")

# --- CABECERA Y SECCIÓN DE IMAGEN (Opcional) ---
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    # Si tienes una imagen corporativa, puedes descomentar la siguiente línea subiéndola a tu repositorio:
    # st.image("tu_logo.png", width=120)
    st.markdown("### ⛽")
with col_titulo:
    st.title("Análisis Inteligente de Competencia y Precios")

st.markdown("---")

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
st.subheader("📁 Origen de Datos")
origen = st.radio("Selecciona cómo ingresar los datos:", ["Subir archivo Excel local", "Ingresar enlace URL de Osinergmin"], key="origen_datos_principal", horizontal=True)

df = None
if origen == "Subir archivo Excel local":
    uploaded_file = st.file_uploader("Sube el archivo 'Ultimos-Precios-Registrados-EVPC.xlsx'", type=["xlsx"], key="archivo_local")
    if uploaded_file:
        df = load_data(uploaded_file)
else:
    url = st.text_input("Pega el enlace de descarga directa del Excel:", key="url_osinergmin")
    if url:
        df = load_data(url)

if df is not None:
    # Limpiar filas sin precios y estandarizar nombres de columnas si es necesario
    df = df.dropna(subset=['PRECIO_VENTA'])
    
    # --- FILTROS AVANZADOS EN BARRA LATERAL ---
    st.sidebar.header("📍 Filtros Geográficos Avanzados")
    
    # 1. Filtro Multiselección de Departamentos / Regiones
    departamentos_disponibles = sorted(df['DEPARTAMENTO'].dropna().unique())
    departamentos_seleccionados = st.sidebar.multiselect(
        "1. Selecciona Regiones / Departamentos", 
        options=departamentos_disponibles,
        default=departamentos_disponibles[:2] if len(departamentos_disponibles) >= 2 else departamentos_disponibles
    )
    
    if departamentos_seleccionados:
        df = df[df['DEPARTAMENTO'].isin(departamentos_seleccionados)]
    
    # 2. Filtro Multiselección de Provincias basadas en las regiones elegidas
    provincias_disponibles = sorted(df['PROVINCIA'].dropna().unique())
    provincias_seleccionadas = st.sidebar.multiselect(
        "2. Selecciona Provincias", 
        options=provincias_disponibles,
        default=provincias_disponibles[:2] if len(provincias_disponibles) >= 2 else provincias_disponibles
    )
    
    if provincias_seleccionadas:
        df = df[df['PROVINCIA'].isin(provincias_seleccionadas)]

    # 3. Filtro Multiselección de Distritos (Ideal para comparar múltiples distritos a la vez)
    distritos_disponibles = sorted(df['DISTRITO'].dropna().unique())
    distritos_seleccionados = st.sidebar.multiselect(
        "3. Selecciona Distritos a Comparar", 
        options=distritos_disponibles,
        default=distritos_disponibles[:3] if len(distritos_disponibles) >= 3 else distritos_disponibles
    )
    
    if distritos_seleccionados:
        df = df[df['DISTRITO'].isin(distritos_seleccionados)]

    st.sidebar.header("🛢️ Filtro de Producto")
    productos_clave = ['GASOHOL REGULAR', 'GASOHOL PREMIUM', 'Diesel B5 S-50 UV', 'DIESEL B5 UV']
    # Filtrar solo los productos que existan realmente en la data filtrada o mostrar los clave
    productos_disponibles = [p for p in productos_clave if p in df['PRODUCTO'].values]
    if not productos_disponibles:
        productos_disponibles = df['PRODUCTO'].dropna().unique().tolist()
        
    producto_seleccionado = st.sidebar.selectbox("Selecciona el combustible", ["Todos"] + productos_disponibles)
    
    if producto_seleccionado != "Todos":
        df = df[df['PRODUCTO'] == producto_seleccionado]
    
    # --- PANEL DE RESULTADOS Y ANALÍTICA ---
    if not df.empty:
        st.markdown(f"### 📊 Resultados de Análisis Comparativo")
        
        # Tarjetas de Indicadores Clave (KPIs globales para la selección actual)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💵 Precio Mínimo", f"S/ {df['PRECIO_VENTA'].min():.2f}")
        col2.metric("📈 Precio Promedio", f"S/ {df['PRECIO_VENTA'].mean():.2f}")
        col3.metric("📉 Precio Máximo", f"S/ {df['PRECIO_VENTA'].max():.2f}")
        col4.metric("🏢 Estaciones Analizadas", f"{df['RAZON'].nunique()}")
        
        st.markdown("---")
        
        # --- GRÁFICOS INTERACTIVOS ---
        st.markdown("### 📉 Comparativa de Precios por Distrito y Competidor")
        
        # Gráfico de barras interactivo agrupado por Distrito y Estación
        fig_bar = px.bar(
            df.sort_values('PRECIO_VENTA'), 
            x='DISTRITO', 
            y='PRECIO_VENTA', 
            color='RAZON', 
            barmode='group',
            hover_data=['DIRECCION', 'PRODUCTO'],
            title="Estructura de Precios: Comparativa Directa entre Distritos Seleccionados",
            labels={'DISTRITO': 'Distrito', 'PRECIO_VENTA': 'Precio de Venta (S/)', 'RAZON': 'Estación / Empresa'}
        )
        fig_bar.update_layout(xaxis_tickangle=-45, template="plotly_dark")
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Gráfico de caja (Boxplot) para ver dispersión de precios por zona
        st.markdown("### 📦 Distribución y Dispersión de Precios (Mínimos, Medianos y Máximos)")
        fig_box = px.box(
            df, 
            x='DISTRITO', 
            y='PRECIO_VENTA', 
            color='DEPARTAMENTO',
            title="Rango de Variabilidad de Precios por Distrito y Región",
            labels={'DISTRITO': 'Distrito', 'PRECIO_VENTA': 'Precio (S/)'}
        )
        fig_box.update_layout(template="plotly_dark")
        st.plotly_chart(fig_box, use_container_width=True)

        # --- TABLA DE DETALLES ---
        st.markdown("### 🏢 Detalle de Registros de Competencia")
        st.dataframe(
            df[['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO', 'RAZON', 'DIRECCION', 'PRODUCTO', 'PRECIO_VENTA']]
            .sort_values('PRECIO_VENTA'),
            use_container_width=True
        )
        
    else:
        st.warning("⚠️ No se encontraron registros de precios que coincidan con la combinación de filtros seleccionada. Intenta ampliar tu selección en la barra lateral.")