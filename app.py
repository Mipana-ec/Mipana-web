import streamlit as st
import datetime

# -----------------------------------------------------------------------------
# Configuración Inicial de la Página
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="MiPana - Red Comunitaria",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Personalizados
st.markdown("""
    <style>
    .main-header {
        color: #1E88E5;
        font-weight: 700;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 16px;
    }
    .metric-card {
        background-color: #F5F7FA;
        padding: 16px;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Inicialización de Datos en Estado de Sesión (Mock Data & Estado)
# -----------------------------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True
    st.session_state.user_name = "Carlos Mendoza"
    st.session_state.user_role = "Cliente / Proveedor"
    st.session_state.balance = 125.50
    st.session_state.transactions = [
        {"fecha": "2026-08-15", "concepto": "Pago de servicio de Plomería", "monto": -35.00},
        {"fecha": "2026-08-10", "concepto": "Recarga de billetera", "monto": 100.00},
        {"fecha": "2026-08-05", "concepto": "Aporte a Campaña Solidaria", "monto": -10.00},
    ]
    st.session_state.services = [
        {"id": 1, "nombre": "Reparación de Fugas e Instalaciones", "categoria": "Plomería", "proveedor": "Juan Pérez", "precio": 25.00, "rating": "⭐ 4.9"},
        {"id": 2, "nombre": "Mantenimiento Eléctrico Residencial", "categoria": "Electricidad", "proveedor": "Ana Gómez", "precio": 30.00, "rating": "⭐ 4.8"},
        {"id": 3, "nombre": "Clases Particulares de Matemáticas", "categoria": "Educación", "proveedor": "Luis Martínez", "precio": 15.00, "rating": "⭐ 5.0"},
    ]
    st.session_state.campaigns = [
        {"id": 1, "titulo": "Apoyo Alimentario para Adultos Mayores", "meta": 500.0, "recaudado": 320.0, "organizador": "Comité Barrio Central"},
        {"id": 2, "titulo": "Colecta de Útiles Escolares", "meta": 300.0, "recaudado": 210.0, "organizador": "Fundación Sonrisas"},
    ]

# -----------------------------------------------------------------------------
# Barra Lateral (Sidebar) - Navegación y Perfil
# -----------------------------------------------------------------------------
st.sidebar.title("🤝 MiPana")

if st.session_state.logged_in:
    st.sidebar.markdown(f"**Usuario:** {st.session_state.user_name}")
    st.sidebar.markdown(f"**Rol:** {st.session_state.user_role}")
    st.sidebar.metric(label="Saldo Disponible", value=f"${st.session_state.balance:.2f} USD")
    st.sidebar.divider()
    
    opcion = st.sidebar.radio(
        "Navegación",
        ["🏠 Inicio", "🔍 Buscar Servicios", "💳 Mi Billetera", "🤝 Ayuda Social / Campañas", "👤 Mi Perfil"]
    )
    
    st.sidebar.divider()
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()
else:
    opcion = "Autenticación"

# -----------------------------------------------------------------------------
# Pantalla de Autenticación (Login / Registro)
# -----------------------------------------------------------------------------
if not st.session_state.logged_in:
    st.title("🤝 Bienvenido a MiPana")
    st.subheader("Tu red comunitaria de servicios y solidaridad")
    
    tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
    
    with tab1:
        email = st.text_input("Correo Electrónico")
        password = st.text_input("Contraseña", type="password")
        if st.button("Ingresar"):
            st.session_state.logged_in = True
            st.success("¡Bienvenido de nuevo!")
            st.rerun()
            
    with tab2:
        nombre = st.text_input("Nombre Completo")
        nuevo_email = st.text_input("Correo Electrónico para Registro")
        nueva_pass = st.text_input("Crear Contraseña", type="password")
        rol = st.selectbox("Selecciona tu rol", ["Cliente", "Proveedor de Servicios", "Ambos"])
        if st.button("Crear Cuenta"):
            st.session_state.user_name = nombre if nombre else "Nuevo Usuario"
            st.session_state.user_role = rol
            st.session_state.logged_in = True
            st.success("Cuenta creada exitosamente.")
            st.rerun()

# -----------------------------------------------------------------------------
# VISTA: 🏠 Inicio
# -----------------------------------------------------------------------------
elif opcion == "🏠 Inicio":
    st.title(f"👋 ¡Hola, {st.session_state.user_name}!")
    st.write("Bienvenido a la plataforma comunitaria **MiPana**. Conecta con proveedores locales y participa en proyectos solidarios.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Billetera Virtual", f"${st.session_state.balance:.2f}")
    col2.metric("Servicios Disponibles", len(st.session_state.services))
    col3.metric("Campañas Activas", len(st.session_state.campaigns))
    
    st.divider()
    st.subheader("🌟 Servicios Destacados")
    cols = st.columns(3)
    for idx, s in enumerate(st.session_state.services):
        with cols[idx % 3]:
            st.subheader(s["nombre"])
            st.caption(f"Categoría: {s['categoria']} | {s['rating']}")
            st.write(f"**Proveedor:** {s['proveedor']}")
            st.write(f"**Precio:** ${s['precio']:.2f} / hr")
            if st.button(f"Contratar #{s['id']}", key=f"btn_home_{s['id']}"):
                st.info(f"Iniciando solicitud para: {s['nombre']}")

# -----------------------------------------------------------------------------
# VISTA: 🔍 Buscar Servicios
# -----------------------------------------------------------------------------
elif opcion == "🔍 Buscar Servicios":
    st.title("🔍 Catálogo de Servicios Comunitarios")
    
    col_busqueda, col_filtro = st.columns([3, 1])
    with col_busqueda:
        busqueda = st.text_input("Buscar por palabra clave (ej. plomería, clases, luz)...")
    with col_filtro:
        categoria = st.selectbox("Categoría", ["Todas", "Plomería", "Electricidad", "Educación"])
        
    st.divider()
    
    for s in st.session_state.services:
        if (categoria == "Todas" or s["categoria"] == categoria) and (busqueda.lower() in s["nombre"].lower()):
            with st.container():
                c1, c2, c3 = st.columns([3, 1, 1])
                with c1:
                    st.markdown(f"### {s['nombre']}")
                    st.write(f"**Proveedor:** {s['proveedor']} | **Categoría:** {s['categoria']}")
                with c2:
                    st.markdown(f"### ${s['precio']:.2f}")
                    st.write(s['rating'])
                with c3:
                    if st.button("Reservar Ahora", key=f"btn_res_{s['id']}"):
                        if st.session_state.balance >= s['precio']:
                            st.session_state.balance -= s['precio']
                            st.session_state.transactions.insert(0, {
                                "fecha": datetime.date.today().strftime("%Y-%m-%d"),
                                "concepto": f"Servicio: {s['nombre']}",
                                "monto": -s['precio']
                            })
                            st.success("¡Servicio contratado con éxito!")
                            st.rerun()
                        else:
                            st.error("Saldo insuficiente en tu billetera.")

# -----------------------------------------------------------------------------
# VISTA: 💳 Mi Billetera
# -----------------------------------------------------------------------------
elif opcion == "💳 Mi Billetera":
    st.title("💳 Billetera Virtual MiPana")
    
    col_saldo, col_acciones = st.columns([1, 2])
    with col_saldo:
        st.subheader("Saldo Actual")
        st.header(f"${st.session_state.balance:.2f} USD")
        
    with col_acciones:
        st.subheader("Operaciones Rápidas")
        tab_recarga, tab_transf = st.tabs(["Recargar Saldo", "Transferir a otro Pana"])
        
        with tab_recarga:
            monto_recarga = st.number_input("Monto a recargar ($)", min_value=5.0, value=20.0, step=5.0)
            if st.button("Confirmar Recarga"):
                st.session_state.balance += monto_recarga
                st.session_state.transactions.insert(0, {
                    "fecha": datetime.date.today().strftime("%Y-%m-%d"),
                    "concepto": "Recarga de Saldo",
                    "monto": monto_recarga
                })
                st.success(f"Recarga exitosa por ${monto_recarga:.2f}")
                st.rerun()
                
        with tab_transf:
            destinatario = st.text_input("Correo o ID del destinatario")
            monto_transf = st.number_input("Monto a transferir ($)", min_value=1.0, value=10.0, step=1.0)
            if st.button("Enviar Dinero"):
                if st.session_state.balance >= monto_transf and destinatario:
                    st.session_state.balance -= monto_transf
                    st.session_state.transactions.insert(0, {
                        "fecha": datetime.date.today().strftime("%Y-%m-%d"),
                        "concepto": f"Transferencia a {destinatario}",
                        "monto": -monto_transf
                    })
                    st.success("Transferencia realizada.")
                    st.rerun()
                else:
                    st.error("Verifica el destinatario y tu saldo disponible.")

    st.divider()
    st.subheader("📜 Historial de Transacciones")
    st.table(st.session_state.transactions)

# -----------------------------------------------------------------------------
# VISTA: 🤝 Ayuda Social / Campañas
# -----------------------------------------------------------------------------
elif opcion == "🤝 Ayuda Social / Campañas":
    st.title("🤝 Módulo de Ayuda Social y Solidaridad")
    st.write("Apoya causas comunitarias o solicita ayuda a la red de Panas.")
    
    for c in st.session_state.campaigns:
        with st.expander(f"📌 {c['titulo']} (Organiza: {c['organizador']})", expanded=True):
            progreso = min(c['recaudado'] / c['meta'], 1.0)
            st.progress(progreso)
            st.write(f"**Recaudado:** ${c['recaudado']:.2f} / Meta: ${c['meta']:.2f}")
            
            col_d1, col_d2 = st.columns([2, 1])
            with col_d1:
                donacion = st.number_input("Monto a donar ($)", min_value=1.0, value=5.0, key=f"don_{c['id']}")
            with col_d2:
                st.write("")
                st.write("")
                if st.button("Donar", key=f"btn_don_{c['id']}"):
                    if st.session_state.balance >= donacion:
                        st.session_state.balance -= donacion
                        c['recaudado'] += donacion
                        st.session_state.transactions.insert(0, {
                            "fecha": datetime.date.today().strftime("%Y-%m-%d"),
                            "concepto": f"Donación: {c['titulo']}",
                            "monto": -donacion
                        })
                        st.success("¡Gracias por tu apoyo solidario!")
                        st.rerun()
                    else:
                        st.error("Saldo insuficiente.")

# -----------------------------------------------------------------------------
# VISTA: 👤 Mi Perfil
# -----------------------------------------------------------------------------
elif opcion == "👤 Mi Perfil":
    st.title("👤 Perfil de Usuario")
    st.write(f"**Nombre:** {st.session_state.user_name}")
    st.write(f"**Rol:** {st.session_state.user_role}")
    
    st.divider()
    st.subheader("🏅 Insignias y Verificación")
    st.success("✔ Identidad Verificada")
    st.info("⭐ Proveedor Confiable de la Comunidad")
