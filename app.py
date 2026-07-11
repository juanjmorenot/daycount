import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Daycount · Calculadora de Días y Horas",
    page_icon="⏳",
    layout="wide",
)

# ---------- Branding: paleta y tipografía (Open Sans + Bitter) ----------
# Cada tema define un acento (títulos/enlaces, contraste >=4.5:1 sobre fondo claro)
# y un color de botón (fondo oscuro suficiente para texto blanco >=4.5:1).
THEMES = {
    "Púrpura oficial": {
        "acento": "#6E00B3",
        "boton": "#9D00FF",
        "boton_hover": "#6E00B3",
        "borde": "#B069DB",
        "fondo_grad": "linear-gradient(180deg, #F7F2F7 0%, #EDE7F0 100%)",
    },
    "Acento claro": {
        "acento": "#8E24AA",
        "boton": "#6E00B3",
        "boton_hover": "#4A007A",
        "borde": "#C79BE0",
        "fondo_grad": "linear-gradient(180deg, #F7F2F7 0%, #EDE7F0 100%)",
    },
    "Acento profundo": {
        "acento": "#5A0099",
        "boton": "#4A007A",
        "boton_hover": "#2E004D",
        "borde": "#7A1FB0",
        "fondo_grad": "linear-gradient(180deg, #F7F2F7 0%, #E7DEEF 100%)",
    },
    "Acento oscuro": {
        "acento": "#3C0061",
        "boton": "#2A0044",
        "boton_hover": "#1A002B",
        "borde": "#5A0099",
        "fondo_grad": "linear-gradient(180deg, #F2ECF7 0%, #E2D6EC 100%)",
    },
}

# ---------- Stateful Design: persistencia de entradas ----------
# Centralizamos los valores por defecto en session_state para mantener la
# persistencia entre re-ejecuciones y permitir un "Restablecer" funcional.
DEFAULTS = {
    "modo": "Entre dos fechas",
    "mostrar_detalle": True,
    "tema": "Púrpura oficial",
    "d_ini": datetime.now().date(),
    "t_ini": datetime.now().time(),
    "d_fin": datetime.now().date() + timedelta(days=30),
    "t_fin": datetime.now().time(),
    "base": datetime.now().date(),
    "chk": datetime.now().date(),
    "cantidad": 7,
    "unidad": "Días",
    "op": "Sumar",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&family=Bitter:wght@500;700&display=swap" rel="stylesheet">

    <style>
        :root {
            --dc-acento: #6E00B3;
            --dc-boton: #9D00FF;
            --dc-boton-hover: #6E00B3;
            --dc-borde: #B069DB;
            --dc-fondo-grad: linear-gradient(180deg, #F7F2F7 0%, #EDE7F0 100%);
        }
        html, body, [class*="stApp"] {
            background-color: #F7F2F7;
            font-family: 'Open Sans', sans-serif;
            color: #3C0061;
        }
        .stApp {
            background: var(--dc-fondo-grad);
        }
        h1, h2, h3, .stTitle {
            font-family: 'Bitter', serif;
            color: var(--dc-acento);
        }
        .daycount-logo {
            font-family: 'Open Sans', sans-serif;
            font-weight: 800;
            font-size: 3.2rem;
            letter-spacing: -1px;
            color: var(--dc-boton);
            line-height: 1.1;
            margin-bottom: 0.2rem;
        }
        .daycount-logo span {
            color: var(--dc-acento);
        }
        .stButton > button {
            background-color: var(--dc-boton);
            color: #FFFFFF;
            border: none;
            border-radius: 10px;
            font-family: 'Open Sans', sans-serif;
            font-weight: 600;
        }
        .stButton > button:hover {
            background-color: var(--dc-boton-hover);
        }
        .stMetric {
            background-color: #FFFFFF;
            border-left: 4px solid var(--dc-borde);
            border-radius: 10px;
            padding: 0.5rem 1rem;
        }
        .stSidebar {
            background-color: #EDE7F0;
        }
        .stProgress > div > div {
            background-color: var(--dc-boton);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Logo de la página ----------
st.markdown('<div class="daycount-logo">Day<span>count</span></div>', unsafe_allow_html=True)
st.caption("Calcula la diferencia entre dos fechas con cuentas regresivas, progresivas y más — usando solo Streamlit.")

# ---------- SIDEBAR: configuración global ----------
with st.sidebar:
    st.header("⚙️ Configuración")
    modo = st.radio(
        "Modo de cálculo",
        ["Entre dos fechas", "Hasta una fecha objetivo", "Desde una fecha pasada"],
        index=["Entre dos fechas", "Hasta una fecha objetivo", "Desde una fecha pasada"].index(st.session_state["modo"]),
        key="modo",
        help="Elige qué quieres comparar.",
    )
    mostrar_detalle = st.toggle(
        "Mostrar desglose detallado",
        value=st.session_state["mostrar_detalle"],
        key="mostrar_detalle",
    )
    tema = st.selectbox(
        "Estilo de color",
        list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state["tema"]),
        key="tema",
    )
    # El tema seleccionado realmente se aplica vía variables CSS (feedback visual inmediato).
    sel = THEMES[tema]
    st.markdown(
        f"""<style>:root{{"""
        f"""--dc-acento:{sel['acento']};"""
        f"""--dc-boton:{sel['boton']};"""
        f"""--dc-boton-hover:{sel['boton_hover']};"""
        f"""--dc-borde:{sel['borde']};"""
        f"""--dc-fondo-grad:{sel['fondo_grad']};"""
        f"""}}</style>""",
        unsafe_allow_html=True,
    )

# ---------- Funciones auxiliares (datetime puro) ----------
def desglose(dt_delta: timedelta):
    total_seg = int(dt_delta.total_seconds())
    sign = -1 if total_seg < 0 else 1
    total_seg = abs(total_seg)
    dias = total_seg // 86400
    horas = (total_seg % 86400) // 3600
    minutos = (total_seg % 3600) // 60
    segundos = total_seg % 60
    semanas = dias // 7
    meses = dias // 30
    anos = dias // 365
    return sign, dias, horas, minutos, segundos, semanas, meses, anos

# ---------- Entradas de fecha (persistidas en session_state) ----------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Fecha y hora de inicio")
    d_ini = st.date_input("Fecha inicio", value=st.session_state["d_ini"], key="d_ini")
    t_ini = st.time_input("Hora inicio", value=st.session_state["t_ini"], key="t_ini")

with col2:
    st.subheader("📅 Fecha y hora de fin")
    d_fin = st.date_input("Fecha fin", value=st.session_state["d_fin"], key="d_fin")
    t_fin = st.time_input("Hora fin", value=st.session_state["t_fin"], key="t_fin")

inicio = datetime.combine(d_ini, t_ini)
fin = datetime.combine(d_fin, t_fin)

if modo == "Hasta una fecha objetivo":
    inicio = datetime.now()
elif modo == "Desde una fecha pasada":
    fin = datetime.now()

delta = fin - inicio
sign, dias, horas, minutos, segundos, semanas, meses, anos = desglose(delta)

# ---------- Métricas principales ----------
st.divider()
st.subheader("📊 Resultado principal")

# Visibilidad: si el resultado es negativo, lo advertimos de inmediato (no solo dentro de una pestaña).
if sign < 0:
    st.warning("⚠️ El resultado es negativo: la fecha final es anterior a la inicial.")

m1, m2, m3, m4 = st.columns(4)
direccion = "↩ hacia atrás" if sign < 0 else "↪ hacia adelante"
m1.metric("Días", f"{sign*dias:,}", delta=direccion, help="Días de diferencia (puede ser negativo).")
m2.metric("Horas totales", f"{sign*dias*24 + sign*horas:,}", help="Horas de diferencia.")
m3.metric("Minutos totales", f"{sign*(dias*1440 + horas*60 + minutos):,}", help="Minutos de diferencia.")
m4.metric("Segundos totales", f"{sign*(dias*86400 + horas*3600 + minutos*60 + segundos):,}", help="Segundos de diferencia.")

# ---------- Tabs con desglose ----------
if mostrar_detalle:
    tab1, tab2, tab3, tab4 = st.tabs(["🗓️ Desglose", "🔁 Cuenta Regresiva", "➡️ Cuenta Progresiva", "📈 Proporciones"])

    with tab1:
        c1, c2, c3 = st.columns(3)
        c1.metric("Semanas", f"{semanas:,}")
        c2.metric("Meses (≈30d)", f"{meses:,}")
        c3.metric("Años (≈365d)", f"{anos:,}")
        st.write(f"**Detalle exacto:** {sign*dias} días, {horas} h, {minutos} min, {segundos} s")
        if sign < 0:
            st.warning("⚠️ La fecha de fin es anterior a la de inicio.")

    with tab2:
        st.info("Cuenta regresiva: tiempo restante hasta la fecha de fin.")
        if fin > datetime.now():
            restante = fin - datetime.now()
            s, dd, hh, mm, ss, _, _, _ = desglose(restante)
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Días restantes", dd)
            col_b.metric("Horas restantes", hh)
            col_c.metric("Minutos restantes", mm)
            st.write(f"⏱️ Faltan **{dd} días, {hh} h, {mm} min y {ss} s** para llegar a {fin:%Y-%m-%d %H:%M}.")
            progreso = max(0.0, min(1.0, (datetime.now() - inicio).total_seconds() / max(1, delta.total_seconds())))
            st.progress(progreso, text="Progreso hasta la fecha objetivo")
        else:
            st.success("✅ ¡La fecha objetivo ya llegó!")

    with tab3:
        st.info("Cuenta progresiva: tiempo transcurrido desde el inicio.")
        if inicio < datetime.now():
            trans = datetime.now() - inicio
            _, dd, hh, mm, ss, _, _, _ = desglose(trans)
            st.write(f"⏳ Han pasado **{dd} días, {hh} h, {mm} min y {ss} s** desde {inicio:%Y-%m-%d %H:%M}.")
            prog = max(0.0, min(1.0, trans.total_seconds() / max(1, delta.total_seconds())))
            st.progress(prog, text="Tiempo transcurrido")
        else:
            st.warning("La fecha de inicio aún no ocurre.")

    with tab4:
        st.info("Distribución del tiempo en unidades.")
        datos = {
            "Días": abs(dias),
            "Semanas": semanas,
            "Meses": meses,
            "Años": anos,
        }
        st.bar_chart(datos)
else:
    st.info("Activa 'Mostrar desglose detallado' en la barra lateral para ver más.")

# ---------- Herramientas extra (agrupadas en formularios para batching) ----------
st.divider()
st.subheader("🧮 Herramientas adicionales")

exp1, exp2 = st.columns(2)

with exp1:
    with st.expander("➕ Sumar/restar tiempo a una fecha"):
        # st.form agrupa las entradas y evita recálculos en cada pulsación de tecla.
        with st.form("form_sumar", border=False):
            base = st.date_input("Fecha base", value=st.session_state["base"], key="base")
            cantidad = st.number_input("Cantidad", min_value=0, value=st.session_state["cantidad"], step=1, key="cantidad")
            unidad = st.selectbox("Unidad", ["Días", "Semanas", "Meses", "Años"], index=["Días", "Semanas", "Meses", "Años"].index(st.session_state["unidad"]), key="unidad")
            op = st.radio("Operación", ["Sumar", "Restar"], index=["Sumar", "Restar"].index(st.session_state["op"]), horizontal=True, key="op")
            enviar = st.form_submit_button("Calcular", use_container_width=True)
        if enviar:
            mult = cantidad if op == "Sumar" else -cantidad
            if unidad == "Días":
                nueva = base + timedelta(days=mult)
            elif unidad == "Semanas":
                nueva = base + timedelta(weeks=mult)
            elif unidad == "Meses":
                mes = base.month - 1 + mult
                año = base.year + mes // 12
                mes = mes % 12 + 1
                nueva = base.replace(year=año, month=mes)
            else:
                nueva = base.replace(year=base.year + mult)
            st.success(f"Resultado: **{nueva:%Y-%m-%d}**")

with exp2:
    with st.expander("🎯 ¿En qué día cae una fecha?"):
        with st.form("form_dia", border=False):
            dchk = st.date_input("Verificar fecha", value=st.session_state["chk"], key="chk")
            enviar_dia = st.form_submit_button("Consultar", use_container_width=True)
        if enviar_dia:
            nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            st.write(f"Esa fecha cae un **{nombres[dchk.weekday()]}**.")

# ---------- Acción de restablecer (Stateful Design + Feedback) ----------
st.divider()
if st.button("♻️ Restablecer valores", use_container_width=True):
    # Devolver todas las entradas a sus valores por defecto y notificar al usuario.
    for k, v in DEFAULTS.items():
        st.session_state[k] = v
    st.toast("Valores restablecidos a los predeterminados.", icon="♻️")
    st.rerun()

st.caption(f"Total aproximado: {anos} años, {meses} meses y {dias} días · Generado solo con Streamlit.")
