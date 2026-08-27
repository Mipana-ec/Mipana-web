import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILOS DE COLOR
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="MiPana - Conectamos trabajo, movemos comunidades",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para destacar colores por categoría
st.markdown("""
    <style>
    .social-banner {
        background-color: #d4edda;
        border-left: 6px solid #28a745;
        padding: 15px;
        border-radius: 8px;
        color: #155724;
    }
    .badge-star {
        background-color: #ffc107;
        color: #000;
        padding: 3px 8px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.85em;
    }
    .badge-kyc {
        background-color: #007bff;
        color: #fff;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.85em;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# ESTADOS Y DATOS EN MEMORIA (MOCK DATA ENRIQUECIDO)
# -----------------------------------------------------------------------------
if "saldo" not in st.session_state:
    st.session_state.saldo = 125.50

if "verificado" not in st.session_state:
    st.session_state.verificado = False

if "es_voluntario" not in st.session_state:
    st.session_state.es_voluntario = True

if "donaciones_realizadas" not in st.session_state:
    st.session_state.donaciones_realizadas = []

if "requerimientos" not in st.session_state:
    st.session_state.requerimientos = [
        {"titulo": "Reparar tubería de cocina", "sector": "Norte", "pago": "$25.00", "tipo": "Comercial", "icono": "🚰"},
        {"titulo": "Pintado de fachada Comedor Popular", "sector": "Sur", "pago": "GRATIS (Solidario)", "tipo": "Social", "icono": "🎨"},
    ]

servicios_geo = pd.DataFrame({
    'servicio': ['Plomería Express', 'Electricista Residencial', 'Apoyo Escolar Gratuito ⭐', 'Técnico de A/C', 'Jardinería Comunitaria ⭐'],
    'proveedor': ['Juan Pérez', 'Ana Gómez', 'Luis Martínez (Voluntario)', 'Carlos Vera', 'María Loor (Donante)'],
    'tipo': ['Comercial', 'Comercial', 'Social', 'Comercial', 'Social'],
    'sector': ['Norte', 'Centro', 'Sur', 'Samborondón', 'Norte'],
    'lat': [-2.1709, -2.1899, -2.2050, -2.1350, -2.1500],
    'lon': [-79.9224, -79.8890, -79.8970, -79.8670, -79.8900]
})

# -----------------------------------------------------------------------------
# BARRA LATERAL (SIDEBAR) & PERFIL CON INSIGNIA
# -----------------------------------------------------------------------------
st.sidebar.title("🤝 MiPana")
st.sidebar.caption("“Conectamos trabajo, movemos comunidades.”")
st.sidebar.markdown("---")

st.sidebar.write("**Usuario:** Carlos Mendoza")
if st.session_state.verificado:
    st.sidebar.markdown("<span class='badge-kyc'>✔ Usuario Verificado (KYC)</span>", unsafe_allow_html=True)
else:
    st.sidebar.warning("⚠️ Perfil no verificado")

if st.session_state.es_voluntario:
    st.sidebar.markdown("<span class='badge-star'>⭐ Pana de Oro / Voluntario</span>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.metric(label="Saldo en Billetera", value=f"${st.session_state.saldo:.2f} USD")
st.sidebar.markdown("---")

opcion_menu = st.sidebar.radio(
    "Menú de Navegación",
    [
        "🏠 Inicio", 
        "📢 Publicar un Requerimiento", 
        "🛠️ Buscar Trabajo / Mapa por Sectores", 
        "🚗 Servicio en Ruta (Modo Uber)", 
        "🌱 Impacto Social & Certificados SRI", 
        "🔐 Verificación de Identidad (KYC)",
        "💳 Billetera Virtual"
    ]
)

# -----------------------------------------------------------------------------
# 1. INICIO & RUTEO DIRECTO
# -----------------------------------------------------------------------------
if opcion_menu == "🏠 Inicio":
    st.title("🤝 MiPana")
    st.subheader("“Conectamos trabajo, movemos comunidades.”")
    st.write("Plataforma segura de servicios profesionales y ayuda social directa.")
    
    st.markdown("---")
    st.write("### ¿Qué deseas hacer hoy?")
    
    col_acc1, col_acc2 = st.columns(2)
    with col_acc1:
        st.info("### 📢 Necesito Contratar o Pedir Ayuda")
        st.write("Publica un trabajo rápido desde tu teléfono para que un proveedor cercano acuda.")
        st.button("Publicar mi Requerimiento Ahora ➔")
        
    with col_acc2:
        st.success("### 🛠️ Busco Trabajo o Quiero Ayudar")
        st.write("Explora requerimientos en tu sector. ¡Gana dinero o suma puntos como Voluntario Estrella!")
        st.button("Ver Trabajos en el Mapa ➔")

    st.markdown("---")
    st.markdown("""
        <div class='social-banner'>
            <h4>🌱 Fondo Social MiPana Activo</h4>
            <p>Por cada servicio comercial contratado, el 3% se destina automáticamente al fondo de ayuda comunitaria. ¡Trabajas, ganas y apoyas a tu sector!</p>
        </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. PUBLICAR REQUERIMIENTO
# -----------------------------------------------------------------------------
elif opcion_menu == "📢 Publicar un Requerimiento":
    st.title("📢 Publica una Necesidad o Trabajo")
    st.caption("Cualquier persona con teléfono puede solicitar asistencia técnica o ayuda social.")
    
    with st.form("form_requerimiento"):
        titulo = st.text_input("¿Qué necesitas? (Ej. Reparar cerradura, Pintar pared, Cuidado de adulto mayor):")
        sector = st.selectbox("Selecciona tu Sector:", ["Norte", "Centro", "Sur", "Samborondón", "Cumbayá / Quito"])
        tipo = st.radio("Tipo de Solicitud:", ["🔵 Trabajo Pagado (Servicio Comercial)", "🟢 Solicitud de Ayuda Social / Gratuita"])
        pago_est = st.number_input("Ofrecimiento estimado de pago ($USD) [Pon 0 si es Ayuda Social]:", min_value=0.0, value=15.0)
        detalles = st.text_area("Detalles adicionales de la solicitud:")
        
        btn_publicar = st.form_submit_button("🚀 Publicar Solicitud en el Mapa")
        
        if btn_publicar:
            if not st.session_state.verificado:
                st.error("⚠️ Para mantener la seguridad de la comunidad, debes validar tu Cédula/RUC en el menú de Verificación (KYC) antes de publicar.")
            else:
                pago_str = f"${pago_est:.2f}" if pago_est > 0 else "GRATIS (Social)"
                st.session_state.requerimientos.append({
                    "titulo": titulo, "sector": sector, "pago": pago_str, "tipo": "Social" if pago_est == 0 else "Comercial", "icono": "🟢" if pago_est == 0 else "🔵"
                })
                st.success("¡Tu requerimiento fue publicado con éxito en el mapa y lista de trabajadores!")

# -----------------------------------------------------------------------------
# 3. BUSCAR TRABAJO / MAPA POR SECTORES
# -----------------------------------------------------------------------------
elif opcion_menu == "🛠️ Buscar Trabajo / Mapa por Sectores":
    st.title("🛠️ Servicios y Oportunidades por Sector")
    
    col_m, col_f = st.columns([2, 1])
    
    with col_f:
        st.subheader("🔍 Filtros de Búsqueda")
        sec_filtro = st.selectbox("Sector:", ["Todos", "Norte", "Centro", "Sur", "Samborondón"])
        cat_filtro = st.radio("Ver Categorías:", ["Todas", "🔵 Solo Trabajos Pagados", "🟢 Solo Ayudas Sociales (⭐ Oportunidad Voluntario)"])
        
        st.markdown("---")
        st.subheader("📋 Lista de Solicitudes en Vivo")
        for req in st.session_state.requerimientos:
            if req['tipo'] == 'Social':
                st.markdown(f"🟢 **{req['titulo']}** ({req['sector']}) - <span class='badge-star'>⭐ {req['pago']}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"🔵 **{req['titulo']}** ({req['sector']}) - **{req['pago']}**", unsafe_allow_html=True)
            st.button(f"Postularme / Aceptar ({req['titulo']})", key=req['titulo'])

    with col_m:
        st.subheader("🗺️ Geolocalización de Oferta y Demanda")
        st.map(servicios_geo[['lat', 'lon']])

# -----------------------------------------------------------------------------
# 4. SERVICIO EN RUTA (MODO UBER)
# -----------------------------------------------------------------------------
elif opcion_menu == "🚗 Servicio en Ruta (Modo Uber)":
    st.title("🚗 Monitoreo de Proveedor en Camino")
    st.warning("⏱️ **Estado:** Juan Pérez está en ruta hacia tu dirección. Llegada estimada: 6 minutos.")
    
    col_d, col_r = st.columns([1, 2])
    with col_d:
        st.subheader("👤 Conductor / Técnico")
        st.write("**Proveedor:** Juan Pérez <span class='badge-star'>⭐ Top Proveedor</span>", unsafe_allow_html=True)
        st.write("**Vehículo:** Moto Honda (Placa: H-3829)")
        st.button("📞 Llamar")
        st.button("💬 Chat WhatsApp")
    
    with col_r:
        st.subheader("📍 Mapa en Vivo")
        ruta_df = pd.DataFrame({'lat': [-2.1709, -2.1720, -2.1735], 'lon': [-79.9224, -79.9210, -79.9195]})
        st.map(ruta_df)

# -----------------------------------------------------------------------------
# 5. IMPACTO SOCIAL & CERTIFICADOS SRI (COLOR VERDE)
# -----------------------------------------------------------------------------
elif opcion_menu == "🌱 Impacto Social & Certificados SRI":
    st.markdown("""
        <div class='social-banner'>
            <h2>🌱 Módulo de Acción Social, Donaciones y Voluntariado</h2>
            <p>Haz donaciones directas o participa en proyectos sociales. Obtén tu estrella de <b>Voluntario/Donante</b> y descarga Certificados de Donación válidos para deducción del Impuesto a la Renta ante el <b>SRI Ecuador</b>.</p>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    
    tab_donar, tab_cert = st.tabs(["💰 Donar a una Causa", "📜 Descargar Certificados SRI"])
    
    with tab_donar:
        c1, c2 = st.columns(2)
        with c1:
            st.write("### 🥦 Huertos Comunitarios Norte")
            st.caption("Beneficiario: Fundación AgroComunidad (RUC: 0992381238001)")
            monto1 = st.number_input("Monto a Aportar ($USD):", min_value=1.0, value=10.0, step=5.0)
            if st.button("Aportar y Generar Certificado SRI"):
                if st.session_state.saldo >= monto1:
                    st.session_state.saldo -= monto1
                    st.session_state.es_voluntario = True
                    st.session_state.donaciones_realizadas.append({
                        "id": f"SRI-MP-2026-{len(st.session_state.donaciones_realizadas)+500}",
                        "causa": "Huertos Comunitarios Norte",
                        "entidad": "Fundación AgroComunidad",
                        "ruc": "0992381238001",
                        "monto": monto1,
                        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.success("¡Aporte registrado! Has obtenido tu Insignia ⭐ Voluntario y tu Certificado SRI.")
                    st.rerun()

    with tab_cert:
        if len(st.session_state.donaciones_realizadas) == 0:
            st.info("No posees donaciones registradas aún.")
        else:
            for c in st.session_state.donaciones_realizadas:
                st.success(f"📜 Certificado Tributario N° {c['id']} - Monto: ${c['monto']:.2f} USD")

# -----------------------------------------------------------------------------
# 6. VERIFICACIÓN DE IDENTIDAD (KYC RIGUROSO)
# -----------------------------------------------------------------------------
elif opcion_menu == "🔐 Verificación de Identidad (KYC)":
    st.title("🔐 Validación Rigurosa de Identidad (Cero Perfiles Falsos)")
    st.write("Para garantizar la seguridad de todos los usuarios en MiPana, valida tus documentos oficiales:")
    
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.file_uploader("1. Foto frontal de Cédula o RUC (PNG/JPG):", type=["jpg", "png"])
        st.file_uploader("2. Foto posterior de Cédula (PNG/JPG):", type=["jpg", "png"])
    with col_k2:
        st.file_uploader("3. Selfie / Foto con prueba de vida facial:", type=["jpg", "png"])
        if st.button("Enviar Documentos para Validación BIOMÉTRICA"):
            st.session_state.verificado = True
            st.success("✅ ¡Felicidades! Tu cuenta ha sido verificada exitosamente. Ahora puedes publicar requerimientos y brindar servicios.")
            st.rerun()

# -----------------------------------------------------------------------------
# 7. BILLETERA VIRTUAL
# -----------------------------------------------------------------------------
elif opcion_menu == "💳 Billetera Virtual":
    st.title("💳 Billetera Digital MiPana")
    st.metric("Saldo Disponible", f"${st.session_state.saldo:.2f} USD")
    m_rec = st.number_input("Monto a recargar ($USD):", min_value=5.0, value=20.0)
    if st.button("Recargar Saldo"):
        st.session_state.saldo += m_rec
        st.success("¡Saldo acreditado!")
        st.rerun()
