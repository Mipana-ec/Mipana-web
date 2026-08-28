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
# ESTADOS EN MEMORIA (BILLETERA Y FONDOS DUALES)
# -----------------------------------------------------------------------------
if "saldo" not in st.session_state:
    st.session_state.saldo = 125.50

if "fondo_solidario_acumulado" not in st.session_state:
    st.session_state.fondo_solidario_acumulado = 1420.00  # Fondo total comunitario acumulado

if "mis_aportes_sociales" not in st.session_state:
    st.session_state.mis_aportes_sociales = 15.30  # Aportes generados por transacciones del usuario

if "verificado" not in st.session_state:
    st.session_state.verificado = True

if "es_voluntario" not in st.session_state:
    st.session_state.es_voluntario = True

if "donaciones_realizadas" not in st.session_state:
    st.session_state.donaciones_realizadas = []

if "requerimientos" not in st.session_state:
    st.session_state.requerimientos = [
        {"id": 1, "titulo": "Reparar fuga de tubería en cocina", "sector": "Norte", "pago": 30.00, "tipo": "Comercial", "icono": "🚰", "cliente": "María Silva"},
        {"id": 2, "titulo": "Pintado de fachada Comedor Comunitario", "sector": "Sur", "pago": 0.00, "tipo": "Social", "icono": "🎨", "cliente": "Fundación Sonrisas"},
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
st.sidebar.metric(label="Saldo Disponible", value=f"${st.session_state.saldo:.2f} USD")
st.sidebar.caption(f"🌱 Tu aporte al Fondo Social: **${st.session_state.mis_aportes_sociales:.2f} USD**")

st.sidebar.markdown("---")
opcion_menu = st.sidebar.radio(
    "Menú de Navegación",
    [
        "🏠 Inicio", 
        "📢 Publicar un Requerimiento", 
        "🛠️ Buscar Trabajo / Mapa por Sectores", 
        "🚗 Servicio en Ruta (Modo Uber)", 
        "💳 Billetera & Flujo de Fondos",
        "🌱 Fundación & Certificados SRI", 
        "🔐 Verificación de Identidad (KYC)"
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
        st.write("Publica un trabajo rápido desde tu teléfono para que un trabajador cercano acuda.")
        
    with col_acc2:
        st.success("### 🛠️ Busco Trabajo o Quiero Ayudar")
        st.write("Explora requerimientos cerca de ti. ¡Gana dinero o suma puntos como Voluntario Estrella!")

    st.markdown("---")
    st.markdown(f"""
        <div class='social-banner'>
            <h4>🌱 Fondo Social MiPana Activo: ${st.session_state.fondo_solidario_acumulado:.2f} USD</h4>
            <p>De cada servicio contratado en la app, un <b>3%</b> se destina automáticamente al fondo manejado por la Fundación aliada. ¡Ganas tú, gana el trabajador y se apoya a la comunidad!</p>
        </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. PUBLICAR REQUERIMIENTO
# -----------------------------------------------------------------------------
elif opcion_menu == "📢 Publicar un Requerimiento":
    st.title("📢 Publica una Necesidad o Trabajo")
    st.caption("Cualquier persona con teléfono puede solicitar asistencia técnica o ayuda social.")
    
    with st.form("form_requerimiento"):
        titulo = st.text_input("¿Qué necesitas? (Ej. Reparación eléctrica, Pintado, Cuidado de personas):")
        sector = st.selectbox("Selecciona tu Sector:", ["Norte", "Centro", "Sur", "Samborondón", "Cumbayá / Quito"])
        tipo = st.radio("Tipo de Solicitud:", ["🔵 Trabajo Pagado (Servicio Comercial)", "🟢 Solicitud de Ayuda Social / Gratuita"])
        pago_est = st.number_input("Ofrecimiento estimado de pago ($USD) [0 para Ayuda Social]:", min_value=0.0, value=20.0)
        
        btn_publicar = st.form_submit_button("🚀 Publicar Solicitud en la Comunidad")
        
        if btn_publicar:
            if not st.session_state.verificado:
                st.error("⚠️ Debes validar tu Cédula/RUC en el menú de Verificación (KYC) antes de publicar.")
            else:
                st.session_state.requerimientos.append({
                    "id": len(st.session_state.requerimientos)+1,
                    "titulo": titulo, 
                    "sector": sector, 
                    "pago": pago_est, 
                    "tipo": "Social" if pago_est == 0 else "Comercial", 
                    "icono": "🟢" if pago_est == 0 else "🔵",
                    "cliente": "Carlos Mendoza"
                })
                st.success("¡Tu requerimiento fue publicado con éxito!")

# -----------------------------------------------------------------------------
# 3. BUSCAR TRABAJO / MAPA Y PAGO AUTOMÁTICO
# -----------------------------------------------------------------------------
elif opcion_menu == "🛠️ Buscar Trabajo / Mapa por Sectores":
    st.title("🛠️ Oportunidades de Trabajo y Mapa por Sectores")
    
    col_m, col_f = st.columns([2, 1])
    
    with col_f:
        st.subheader("📋 Solicitudes Cercanas")
        for req in st.session_state.requerimientos:
            pago_txt = f"${req['pago']:.2f}" if req['pago'] > 0 else "GRATIS (Social)"
            st.markdown(f"**{req['icono']} {req['titulo']}** ({req['sector']})")
            st.caption(f"Pago: **{pago_txt}** | Cliente: {req['cliente']}")
            
            if st.button(f"Contratar / Pagar Servicio ({req['id']})", key=f"pay_{req['id']}"):
                if req['pago'] > 0:
                    if st.session_state.saldo >= req['pago']:
                        monto_total = req['pago']
                        pago_trabajador = monto_total * 0.85
                        comision_mipana = monto_total * 0.12
                        aporte_social = monto_total * 0.03
                        
                        st.session_state.saldo -= monto_total
                        st.session_state.fondo_solidario_acumulado += aporte_social
                        st.session_state.mis_aportes_sociales += aporte_social
                        
                        st.success(f"""
                        ✅ **¡Pago Procesado Exitosamente!**
                        - 👷 **Pago al Trabajador (85%):** ${pago_trabajador:.2f} USD
                        - 💼 **Comisión MiPana Tech (12%):** ${comision_mipana:.2f} USD
                        - 🌱 **Aporte a Fundación (3%):** ${aporte_social:.2f} USD
                        """)
                        st.rerun()
                    else:
                        st.error("Saldo insuficiente en tu Billetera Virtual.")
                else:
                    st.success("¡Te has postulado a este servicio de Voluntariado! Ganaste tu insignia ⭐")

    with col_m:
        st.subheader("🗺️ Servicios Cercanos en Mapa")
        st.map(servicios_geo[['lat', 'lon']])

# -----------------------------------------------------------------------------
# 4. SERVICIO EN RUTA (MODO UBER)
# -----------------------------------------------------------------------------
elif opcion_menu == "🚗 Servicio en Ruta (Modo Uber)":
    st.title("🚗 Monitoreo de Servicio en Tiempo Real")
    st.warning("⏱️ **Estado:** Proveedor Juan Pérez en ruta. Tiempo estimado: 5 minutos.")
    
    col_d, col_r = st.columns([1, 2])
    with col_d:
        st.subheader("👤 Datos del Proveedor")
        st.write("**Técnico:** Juan Pérez <span class='badge-star'>⭐ Top Proveedor</span>", unsafe_allow_html=True)
        st.write("**Vehículo:** Moto Honda (Placa: H-3829)")
        st.button("📞 Llamar")
        st.button("💬 Chat WhatsApp")
    
    with col_r:
        st.subheader("📍 Mapa de Ruta")
        ruta_df = pd.DataFrame({'lat': [-2.1709, -2.1720, -2.1735], 'lon': [-79.9224, -79.9210, -79.9195]})
        st.map(ruta_df)

# -----------------------------------------------------------------------------
# 5. BILLETERA & FLUJO DE FONDOS
# -----------------------------------------------------------------------------
elif opcion_menu == "💳 Billetera & Flujo de Fondos":
    st.title("💳 Billetera Virtual Dual")
    st.write("Transparencia total en tus transacciones e impacto comunitario.")
    
    col_b1, col_b2, col_b3 = st.columns(3)
    col_b1.metric("Tu Saldo Disponible", f"${st.session_state.saldo:.2f} USD")
    col_b2.metric("Tu Impacto Social", f"${st.session_state.mis_aportes_sociales:.2f} USD")
    col_b3.metric("Fondo Comunitario Total", f"${st.session_state.fondo_solidario_acumulado:.2f} USD")
    
    st.markdown("---")
    st.subheader("🔄 Esquema Transparente de Reparto")
    st.info("""
    Cada vez que contratas un trabajo comercial en **MiPana**:
    * **85%** va directamente a la billetera del trabajador local.
    * **12%** sostiene la infraestructura tecnológica de MiPana Tech.
    * **3%** se transfiere de forma automática a la Fundación aliada para proyectos comunitarios.
    """)
    
    m_rec = st.number_input("Monto a recargar a tu billetera ($USD):", min_value=5.0, value=20.0)
    if st.button("Recargar Saldo"):
        st.session_state.saldo += m_rec
        st.success("¡Saldo acreditado con éxito!")
        st.rerun()

# -----------------------------------------------------------------------------
# 6. FUNDACIÓN & CERTIFICADOS SRI
# -----------------------------------------------------------------------------
elif opcion_menu == "🌱 Fundación & Certificados SRI":
    st.markdown("""
        <div class='social-banner'>
            <h2>🌱 Fundación MiPana & Certificación Tributaria</h2>
            <p>Donaciones canalizadas para proyectos sociales comunitarios con respaldo deducible de Impuesto a la Renta ante el <b>SRI Ecuador</b>.</p>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    
    tab_donar, tab_cert = st.tabs(["💰 Donación Voluntaria", "📜 Mis Certificados SRI"])
    
    with tab_donar:
        c1, c2 = st.columns(2)
        with c1:
            st.write("### 🥦 Huertos Comunitarios Urbanos")
            st.caption("Entidad Operadora: Fundación AgroComunidad (RUC: 0992381238001)")
            monto1 = st.number_input("Monto a Aportar ($USD):", min_value=1.0, value=10.0, step=5.0)
            if st.button("Donar y Solicitar Certificado SRI"):
                if st.session_state.saldo >= monto1:
                    st.session_state.saldo -= monto1
                    st.session_state.donaciones_realizadas.append({
                        "id": f"SRI-MP-2026-{len(st.session_state.donaciones_realizadas)+500}",
                        "causa": "Huertos Comunitarios Urbanos",
                        "entidad": "Fundación AgroComunidad",
                        "ruc": "0992381238001",
                        "monto": monto1,
                        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.success("¡Donación procesada! Certificado SRI disponible.")
                    st.rerun()

    with tab_cert:
        if len(st.session_state.donaciones_realizadas) == 0:
            st.info("No registras donaciones directas aún.")
        else:
            for c in st.session_state.donaciones_realizadas:
                st.success(f"📜 Certificado Tributario SRI N° {c['id']} - Monto: ${c['monto']:.2f} USD")

# -----------------------------------------------------------------------------
# 7. VERIFICACIÓN DE IDENTIDAD (KYC)
# -----------------------------------------------------------------------------
elif opcion_menu == "🔐 Verificación de Identidad (KYC)":
    st.title("🔐 Validación Rigurosa de Identidad")
    st.write("Seguridad garantizada para la tranquilidad de clientes y proveedores:")
    
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.file_uploader("1. Cédula o RUC (Frontal):", type=["jpg", "png"])
        st.file_uploader("2. Cédula (Posterior):", type=["jpg", "png"])
    with col_k2:
        st.file_uploader("3. Selfie de verificación facial:", type=["jpg", "png"])
        if st.button("Validar mi Cuenta (KYC Biométrico)"):
            st.session_state.verificado = True
            st.success("✅ Cuenta verificada exitosamente.")
            st.rerun()

# -----------------------------------------------------------------------------
# PIE DE PÁGINA Y DERECHOS RESERVADOS
# -----------------------------------------------------------------------------
st.markdown("---")
col_foot1, col_foot2 = st.columns([3, 1])
with col_foot1:
    st.caption("© 2026 MiPana Inc. Todos los derechos reservados. Plataforma Comunitaria de Servicios.")
with col_foot2:
    st.caption("🔒 Validación KYC & Alianza SRI")
