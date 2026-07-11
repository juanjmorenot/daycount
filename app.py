import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Daycount · Calculadora de Días y Horas",
    page_icon="⏳",
    layout="wide",
)

# ---------- Branding: paleta y tipografía (Open Sans + Bitter) ----------
BRAND = {
    "principal": "#9D00FF",
    "acento_1": "#B069DB",
    "acento_2": "#6E00B3",
    "acento_3": "#3C0061",
    "fondo_1": "#F7F2F7",
    "fondo_2": "#E6E6E6",
}

st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&family=Bitter:wght@500;700&display=swap" rel="stylesheet">

    <style>
        html, body, [class*="stApp"] {
            background-color: #F7F2F7;
            font-family: 'Open Sans', sans-serif;
            color: #3C0061;
        }
        .stApp {
            background: linear-gradient(180deg, #F7F2F7 0%, #E6E6E6 100%);
        }
        h1, h2, h3, .stTitle {
            font-family: 'Bitter', serif;
            color: #6E00B3;
        }
        .daycount-logo {
            font-family: 'Open Sans', sans-serif;
            font-weight: 800;
            font-size: 3.2rem;
            letter-spacing: -1px;
            color: #9D00FF;
            line-height: 1.1;
            margin-bottom: 0.2rem;
        }
        .daycount-logo span {
            color: #6E00B3;
        }
        .stButton > button {
            background-color: #9D00FF;
            color: #FFFFFF;
            border: none;
            border-radius: 10px;
            font-family: 'Open Sans', sans-serif;
            font-weight: 600;
        }
        .stButton > button:hover {
            background-color: #6E00B3;
        }
        .stMetric {
            background-color: #FFFFFF;
            border-left: 4px solid #B069DB;
            border-radius: 10px;
            padding: 0.5rem 1rem;
        }
        .stSidebar {
            background-color: #E6E6E6;
        }
        .stProgress > div > div {
            background-color: #9D00FF;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Logo de la página ----------
st.markdown('<div class="daycount-logo">Day<span>count</span></div>', unsafe_allow_html=True)
st.caption("Calcula la diferencia entre dos fechas con cuentas regresivas, progresivas y más — usando solo Streamlit.")

# ---------- SIDEBAR: configuración ----------
with st.sidebar:
    st.header("⚙️ Configuración")
    modo = st.radio(
        "Modo de cálculo",
        ["Entre dos fechas", "Hasta una fecha objetivo", "Desde una fecha pasada"],
        help="Elige qué quieres comparar.",
    )
    mostrar_detalle = st.toggle("Mostrar desglose detallado", value=True)
    tema = st.selectbox(
        "Estilo de color",
        ["Púrpura oficial", "Acento claro", "Acento profundo", "Acento oscuro"],
        index=0,
    )
    color = {
        "Púrpura oficial": BRAND["principal"],
        "Acento claro": BRAND["acento_1"],
        "Acento profundo": BRAND["acento_2"],
        "Acento oscuro": BRAND["acento_3"],
    }[tema]

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

# ---------- Entradas de fecha (campos clickables) ----------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Fecha y hora de inicio")
    d_ini = st.date_input("Fecha inicio", value=datetime.now().date())
    t_ini = st.time_input("Hora inicio", value=datetime.now().time())

with col2:
    st.subheader("📅 Fecha y hora de fin")
    d_fin = st.date_input("Fecha fin", value=datetime.now().date() + timedelta(days=30))
    t_fin = st.time_input("Hora fin", value=datetime.now().time())

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

m1, m2, m3, m4 = st.columns(4)
m1.metric("Días", f"{sign*dias:,}", help="Días de diferencia (puede ser negativo).")
m2.metric("Horas totales", f"{sign*dias*24 + sign*horas:,}")
m3.metric("Minutos totales", f"{sign*(dias*1440 + horas*60 + minutos):,}")
m4.metric("Segundos totales", f"{sign*(dias*86400 + horas*3600 + minutos*60 + segundos):,}")

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

# ---------- Herramientas extra ----------
st.divider()
st.subheader("🧮 Herramientas adicionales")

exp1, exp2 = st.columns(2)

with exp1:
    with st.expander("➕ Sumar/restar tiempo a una fecha"):
        base = st.date_input("Fecha base", value=datetime.now().date(), key="base")
        cantidad = st.number_input("Cantidad", min_value=0, value=7, step=1)
        unidad = st.selectbox("Unidad", ["Días", "Semanas", "Meses", "Años"])
        op = st.radio("Operación", ["Sumar", "Restar"], horizontal=True)
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
        dchk = st.date_input("Verificar fecha", value=datetime.now().date(), key="chk")
        nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        st.write(f"Esa fecha cae un **{nombres[dchk.weekday()]}**.")

# ---------- Botón de acción ----------
if st.button("🔄 Recalcular", use_container_width=True):
    st.rerun()

st.divider()
st.caption(f"Total aproximado: {anos} años, {meses} meses y {dias} días · Generado solo con Streamlit.")
