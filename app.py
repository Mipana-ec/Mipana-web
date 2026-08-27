import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="MiPana - Red Comunitaria & Servicios",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# ESTADOS Y DATOS DE PRUEBA (MOCK DATA)
# -----------------------------------------------------------------------------
if "saldo" not in st.session_state:
    st.session_state.saldo = 125.50

if "donaciones_realizadas" not in st.session_state:
    st.session_state.donaciones_realizadas = []

# Datos de proveedores en el mapa (Coordenadas de referencia - Ecuador)
servicios_geo = pd.DataFrame({
    'servicio': ['Plomería Express', 'Electricista Residencial', 'Clases de Matemáticas', 'Técnico de A/C', 'Servicio Limpieza'],
    'proveedor': ['Juan Pérez', 'Ana Gómez', 'Luis Martínez', 'Carlos Vera', 'María Loor'],
    'sector': ['Norte', 'Centro', 'Sur', 'Samborondón', 'Norte'],
    'lat': [-2.1709, -2.1899, -2.2050, -2.1350, -2.1500],
    'lon': [-79.9224, -79.8890, -79.8970, -79.8670, -79.8900]
})

# -----------------------------------------------------------------------------
# BARRA LATERAL (SIDEBAR)
# -----------------------------------------------------------------------------
st.sidebar.title("🤝 MiPana")
st.sidebar.write("**Usuario:** Carlos Mendoza")
st.sidebar.write("**RUC/CI:** 0993821049001")
st.sidebar.write("**Rol:** Cliente / Proveedor / Donante")
st.sidebar.markdown("---")

st.sidebar.metric(label="Saldo Disponible en Billetera", value=f"${st.session_state.saldo:.2f} USD")

st.sidebar.markdown("---")
opcion_menu = st.sidebar.radio(
    "Navegación Principal",
    ["🏠 Inicio & Resumen", "🛠️ Servicios & Mapa de Sectores", "🚗 Servicio en Ruta (Modo Uber)", "🎗️ Donaciones & Certificados SRI", "💳 Billetera Virtual"]
)

# -----------------------------------------------------------------------------
# 1. INICIO & RESUMEN
# -----------------------------------------------------------------------------
if opcion_menu == "🏠 Inicio & Resumen":
    st.title("👋 ¡Bienvenido a MiPana!")
    st.caption("Conectando tu comunidad con servicios profesionales y causas solidarias.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Billetera Virtual", f"${st.session_state.saldo:.2f}")
    col2.metric("Servicios Cercanos", "5 Activos")
    col3.metric("Certificados Emitidos", len(st.session_state.donaciones_realizadas))
    
    st.markdown("---")
    st.subheader("📌 Novedades Rápidas")
    st.info("🚗 **Nuevo:** Ahora puedes rastrear la ruta en vivo del proveedor de servicios asignado.")
    st.success("📄 **Certificados SRI:** Tus aportes solidarios ahora entregan certificados deducibles del Impuesto a la Renta.")

# -----------------------------------------------------------------------------
# 2. SERVICIOS & MAPA DE SECTORES
# -----------------------------------------------------------------------------
elif opcion_menu == "🛠️ Servicios & Mapa de Sectores":
    st.title("🛠️ Servicios Comunitarios y Proveedores por Sector")
    st.write("Explora ofertas de trabajo o ayuda cercana a tu zona residencial.")
    
    col_mapa, col_filtro = st.columns([2, 1])
    
    with col_filtro:
        st.subheader("🔍 Filtrar por Sector")
        sector_sel = st.selectbox("Selecciona tu Ubicación:", ["Todos", "Norte", "Centro", "Sur", "Samborondón"])
        
        if sector_sel != "Todos":
            df_filtrado = servicios_geo[servicios_geo['sector'] == sector_sel]
        else:
            df_filtrado = servicios_geo
            
        st.write(f"Mostrando **{len(df_filtrado)}** proveedores.")
        for idx, row in df_filtrado.iterrows():
            st.write(f"• **{row['servicio']}** - {row['proveedor']} ({row['sector']})")
    
    with col_mapa:
        st.subheader("🗺️ Ubicación en Mapa Interactivo")
        st.map(df_filtrado[['lat', 'lon']])

# -----------------------------------------------------------------------------
# 3. SERVICIO EN RUTA (ESTILO UBER)
# -----------------------------------------------------------------------------
elif opcion_menu == "🚗 Servicio en Ruta (Modo Uber)":
    st.title("🚗 Monitoreo de Servicio en Ruta")
    st.caption("Rastreo en tiempo real del técnico o proveedor contratado.")
    
    st.warning("⏱️ **Estado del Servicio:** En Camino (Llegada estimada: 8 mins)")
    
    col_driver, col_route = st.columns([1, 2])
    
    with col_driver:
        st.subheader("👤 Datos del Proveedor")
        st.write("**Técnico:** Juan Pérez")
        st.write("**Servicio:** Reparación de Fugas Express")
        st.write("**Vehículo:** Moto Honda Cargo (Placa: H-3829)")
        st.write("**Calificación:** ⭐ 4.9 (120 servicios)")
        st.button("📞 Llamar al Proveedor")
        st.button("💬 Chat por WhatsApp")
    
    with col_route:
        st.subheader("📍 Ruta del Vehículo Hacia tu Ubicación")
        # Simulación de coordenadas de ruta acercándose
        ruta_df = pd.DataFrame({
            'lat': [-2.1709, -2.1720, -2.1735],
            'lon': [-79.9224, -79.9210, -79.9195]
        })
        st.map(ruta_df)

# -----------------------------------------------------------------------------
# 4. DONACIONES & CERTIFICADOS SRI
# -----------------------------------------------------------------------------
elif opcion_menu == "🎗️ Donaciones & Certificados SRI":
    st.title("🎗️ Proyectos Solidarios y Certificación Tributaria SRI")
    st.caption("Apoya proyectos comunitarios y descarga tus certificados válidos para deducción de Impuesto a la Renta.")
    
    tab1, tab2 = st.tabs(["💰 Realizar Donación", "📜 Mis Certificados Tributarios SRI"])
    
    with tab1:
        st.subheader("Causas Activas")
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.write("### 🥦 Huertos Comunitarios Urbanos")
            st.caption("Entidad Beneficiaria: Fundación AgroComunidad (RUC: 0992381238001)")
            monto_donar = st.number_input("Monto a donar ($USD):", min_value=1.0, value=10.0, step=5.0, key="monto_1")
            if st.button("Aportar a Huertos Comunitarios"):
                if st.session_state.saldo >= monto_donar:
                    st.session_state.saldo -= monto_donar
                    cert_num = f"SRI-MP-2026-{len(st.session_state.donaciones_realizadas)+1001}"
                    st.session_state.donaciones_realizadas.append({
                        "id": cert_num,
                        "causa": "Huertos Comunitarios Urbanos",
                        "entidad": "Fundación AgroComunidad",
                        "ruc": "0992381238001",
                        "monto": monto_donar,
                        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.success(f"¡Gracias por tu aporte de ${monto_donar:.2f}! Certificado SRI generado exitosamente.")
                    st.rerun()
                else:
                    st.error("Saldo insuficiente en tu billetera virtual.")

        with col_c2:
            st.write("### 📚 Equipamiento Escolar Comunitario")
            st.caption("Entidad Beneficiaria: Asociación EducaPana (RUC: 1792837192001)")
            monto_donar2 = st.number_input("Monto a donar ($USD):", min_value=1.0, value=25.0, step=5.0, key="monto_2")
            if st.button("Aportar a Equipamiento Escolar"):
                if st.session_state.saldo >= monto_donar2:
                    st.session_state.saldo -= monto_donar2
                    cert_num = f"SRI-MP-2026-{len(st.session_state.donaciones_realizadas)+1001}"
                    st.session_state.donaciones_realizadas.append({
                        "id": cert_num,
                        "causa": "Equipamiento Escolar Comunitario",
                        "entidad": "Asociación EducaPana",
                        "ruc": "1792837192001",
                        "monto": monto_donar2,
                        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.success(f"¡Gracias por tu aporte de ${monto_donar2:.2f}! Certificado SRI generado exitosamente.")
                    st.rerun()
                else:
                    st.error("Saldo insuficiente en tu billetera virtual.")

    with tab2:
        st.subheader("📄 Certificados de Donación emitidos para Deducción SRI")
        if len(st.session_state.donaciones_realizadas) == 0:
            st.info("Aún no has realizado donaciones para generar certificados.")
        else:
            for cert in st.session_state.donaciones_realizadas:
                with st.expander(f"📜 Certificado N° {cert['id']} - {cert['causa']} (${cert['monto']:.2f})"):
                    st.markdown(f"""
                    ```text
                    ===================================================================
                    CERTIFICADO DE DONACIÓN DEDUCIBLE DE IMPUESTO A LA RENTA (SRI ECUADOR)
                    ===================================================================
                    N° Registro Tributario: {cert['id']}
                    Fecha de Emisión:      {cert['fecha']}
                    
                    DONANTE:               Carlos Mendoza
                    RUC / C.I. Donante:    0993821049001
                    
                    BENEFICIARIO:          {cert['entidad']}
                    RUC Beneficiario:      {cert['ruc']}
                    
                    CONCEPTO / PROYECTO:   {cert['causa']}
                    VALOR DONADO:          USD ${cert['monto']:.2f}
                    
                    Sustento Legal: Art. 10 de la Ley de Régimen Tributario Interno (LRTI).
                    Documento digital con validez para la declaración anual del SRI.
                    ===================================================================
                    ```
                    """)
                    st.button(f"📥 Descargar Certificado SRI en PDF ({cert['id']})", key=cert['id'])

# -----------------------------------------------------------------------------
# 5. BILLETERA VIRTUAL
# -----------------------------------------------------------------------------
elif opcion_menu == "💳 Billetera Virtual":
    st.title("💳 Mi Billetera Digital")
    st.metric("Saldo Actual", f"${st.session_state.saldo:.2f} USD")
    
    col_recarga, col_retiro = st.columns(2)
    with col_recarga:
        st.subheader("➕ Recargar Saldo")
        val_rec = st.number_input("Valor a recargar ($USD):", min_value=5.0, value=20.0, step=5.0)
        if st.button("Recargar con Tarjeta / Transferencia"):
            st.session_state.saldo += val_rec
            st.success(f"¡Recarga exitosa! Nuevo saldo: ${st.session_state.saldo:.2f}")
            st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("MiPana Web App 2026 • Estado: En línea")
