import streamlit as st
from datetime import datetime, timedelta
import sys

if not st.runtime.exists():
    print("[ERROR] Este archivo debe ejecutarse con:  streamlit run app.py")
    print("        No uses:  python app.py")
    sys.exit(1)

st.set_page_config(
    page_title="Daycount · Calculadora de Días y Horas",
    page_icon="⏳",
    layout="wide",
)

# ---------- Branding ----------
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

# ---------- Stateful Design ----------
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
            --primary-color: #9D00FF !important;
            --background-color: #F7F2F7 !important;
            --secondary-background-color: #FFFFFF !important;
            --text-color: #3C0061 !important;
            --font: 'Open Sans', sans-serif !important;
            --dc-acento: #6E00B3;
            --dc-boton: #9D00FF;
            --dc-boton-hover: #6E00B3;
            --dc-borde: #B069DB;
            --dc-fondo-grad: linear-gradient(180deg, #F7F2F7 0%, #EDE7F0 100%);
        }
        body, .stApp { background: var(--dc-fondo-grad) !important; color: #3C0061; }
        .stAppHeader { display: none !important; }

        /* === Bento cards === */
        div[class*=" st-key-card-"], div[class^="st-key-card-"] {
            background: #FFFFFF !important;
            border-radius: 14px !important;
            padding: 1.25rem 1.5rem !important;
            border: 1px solid #E4D7EF !important;
            box-shadow: 0 2px 6px rgba(60, 0, 97, 0.06) !important;
            height: 100%;
        }

        .card-heading {
            font-family: 'Open Sans', sans-serif;
            font-weight: 600;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--dc-acento);
            margin-bottom: 0.5rem;
        }

        /* === Hero Card === */
        .st-key-card-hero { text-align: center !important; padding: 1.5rem 2rem !important; }
        .hero-unit {
            font-family: 'Bitter', serif;
            font-weight: 700;
            font-size: 0.85rem;
            color: var(--dc-acento);
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.1rem;
        }
        .hero-number {
            font-family: 'Open Sans', sans-serif;
            font-weight: 800;
            font-size: clamp(2.5rem, 7vw, 5rem);
            line-height: 1.05;
            color: #3C0061;
            margin: 0.1rem 0;
        }
        .hero-number.negative { color: #B0003A; }
        .hero-direction { font-size: 1rem; color: var(--dc-acento); margin-bottom: 0.75rem; }
        .hero-metrics {
            display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap;
            padding-top: 0.75rem; border-top: 1px solid #EDE7F0;
        }
        .hm-item { text-align: center; min-width: 80px; }
        .hm-value { font-weight: 700; font-size: 1.25rem; color: #3C0061; }
        .hm-label {
            font-size: 0.68rem; font-weight: 600; color: var(--dc-acento);
            text-transform: uppercase; letter-spacing: 0.04em; margin-top: 0.05rem;
        }

        /* === Status card === */
        .status-mode { font-weight: 600; font-size: 0.9rem; color: #3C0061; }
        .neg-flag {
            display: inline-flex; align-items: center; gap: 0.4rem;
            padding: 0.35rem 0.7rem; border-radius: 8px;
            font-weight: 600; font-size: 0.8rem;
            background: #FFF0F0; color: #B0003A; border: 1px solid #FFD4D4;
        }
        .detail-badge {
            display: inline-block; margin-top: 0.5rem;
            font-size: 0.75rem; color: var(--dc-acento);
        }

        /* === Date picker grid === */
        .fecha-label { font-size: 0.75rem; font-weight: 600; color: #6E00B3; margin-bottom: 0.15rem; }

        /* === Progress === */
        .stProgress > div { padding: 0 !important; }
        .stProgress > div > div { background-color: var(--dc-boton) !important; border-radius: 20px !important; }

        /* === Button === */
        .stButton > button {
            background-color: var(--dc-boton) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-family: 'Open Sans', sans-serif !important;
        }
        .stButton > button:hover { background-color: var(--dc-boton-hover) !important; }
        .stDateInput, .stTimeInput { width: 100% !important; }
        .stDateInput > div, .stTimeInput > div { width: 100% !important; }

        /* === Sidebar === */
        .stSidebar { background-color: #EDE7F0 !important; padding: 1rem !important; }

        /* === Spacing between rows === */
        [data-testid="column"] { gap: 0.75rem; display: flex; flex-direction: column; }
        [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"]:not(:first-child) {
            margin-top: 0.75rem;
        }
        .stAlert { border-radius: 10px !important; }

        /* === Tool cards compact forms === */
        .tool-result { text-align: center; font-size: 1.1rem; font-weight: 600; color: #3C0061; margin-top: 0.5rem; }

        @media (max-width: 640px) {
            [data-testid="stHorizontalBlock"] { flex-direction: column !important; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Logo ----------
st.markdown(
    '<div style="max-width:1000px;margin:0 auto 0.25rem">'
    '<span style="font-family:Open Sans,sans-serif;font-weight:800;font-size:1.8rem;letter-spacing:-0.5px;color:var(--dc-boton)">Day</span>'
    '<span style="font-family:Open Sans,sans-serif;font-weight:800;font-size:1.8rem;letter-spacing:-0.5px;color:var(--dc-acento)">count</span>'
    '</div>',
    unsafe_allow_html=True,
)
st.caption("Calcula la diferencia entre dos fechas con cuentas regresivas, progresivas y más — usando solo Streamlit.")

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown('<div class="card-heading" style="margin-top:0">⚙️ Configuración</div>', unsafe_allow_html=True)
    modo = st.radio(
        "Modo de cálculo",
        ["Entre dos fechas", "Hasta una fecha objetivo", "Desde una fecha pasada"],
        index=["Entre dos fechas", "Hasta una fecha objetivo", "Desde una fecha pasada"].index(st.session_state["modo"]),
        key="modo",
        help="Elige qué quieres comparar.",
    )
    mostrar_detalle = st.toggle("Mostrar desglose detallado", value=st.session_state["mostrar_detalle"], key="mostrar_detalle")
    tema = st.selectbox(
        "Estilo de color",
        list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state["tema"]),
        key="tema",
    )
    sel = THEMES[tema]
    st.markdown(
        f"""<style>:root{{"""
        f"""--primary-color:{sel['boton']} !important;"""
        f"""--dc-acento:{sel['acento']};"""
        f"""--dc-boton:{sel['boton']};"""
        f"""--dc-boton-hover:{sel['boton_hover']};"""
        f"""--dc-borde:{sel['borde']};"""
        f"""--dc-fondo-grad:{sel['fondo_grad']};"""
        f"""}}</style>""",
        unsafe_allow_html=True,
    )

# ---------- Lógica ----------
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

# Las lecturas de session_state se actualizan cuando los widgets (definidos abajo en cards)
# son modificados por el usuario.
_inicio = datetime.combine(st.session_state["d_ini"], st.session_state["t_ini"])
_fin = datetime.combine(st.session_state["d_fin"], st.session_state["t_fin"])

if modo == "Hasta una fecha objetivo":
    _inicio = datetime.now()
elif modo == "Desde una fecha pasada":
    _fin = datetime.now()

delta = _fin - _inicio
sign, dias, horas, minutos, segundos, semanas, meses, anos = desglose(delta)

# ---------- BENTO GRID (columnas) ----------

# ---- Row 1: Hero Card (full width) ----
with st.container(key="card-hero"):
    direccion = "↩ hacia atrás" if sign < 0 else "↪ hacia adelante"
    neg_class = " negative" if sign < 0 else ""
    st.markdown(
        f"""
        <div class="hero-unit">Días</div>
        <div class="hero-number{neg_class}">{sign*dias:,}</div>
        <div class="hero-direction">{direccion}</div>
        <div class="hero-metrics">
            <div class="hm-item">
                <div class="hm-value">{sign*dias*24 + sign*horas:,}</div>
                <div class="hm-label">Horas</div>
            </div>
            <div class="hm-item">
                <div class="hm-value">{sign*(dias*1440 + horas*60 + minutos):,}</div>
                <div class="hm-label">Minutos</div>
            </div>
            <div class="hm-item">
                <div class="hm-value">{sign*(dias*86400 + horas*3600 + minutos*60 + segundos):,}</div>
                <div class="hm-label">Segundos</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---- Row 2: Fechas + Status ----
col_f, col_s = st.columns([1.6, 1])

with col_f:
    with st.container(key="card-fechas"):
        st.markdown('<div class="card-heading">📅 Fechas</div>', unsafe_allow_html=True)
        fc1, fc2 = st.columns(2)
        with fc1:
            st.markdown('<div class="fecha-label">Inicio</div>', unsafe_allow_html=True)
            st.date_input("ini_d", value=st.session_state["d_ini"], key="d_ini", label_visibility="collapsed")
            st.time_input("ini_t", value=st.session_state["t_ini"], key="t_ini", label_visibility="collapsed")
        with fc2:
            st.markdown('<div class="fecha-label">Fin</div>', unsafe_allow_html=True)
            st.date_input("fin_d", value=st.session_state["d_fin"], key="d_fin", label_visibility="collapsed")
            st.time_input("fin_t", value=st.session_state["t_fin"], key="t_fin", label_visibility="collapsed")

with col_s:
    with st.container(key="card-status"):
        st.markdown('<div class="card-heading">⚙️ Estado</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="status-mode">Modo: <strong>{modo}</strong></div>', unsafe_allow_html=True)
        if sign < 0:
            st.markdown('<div class="neg-flag">⚠️ La fecha de fin es anterior a la de inicio</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="detail-badge">Desglose: {"✅ activo" if mostrar_detalle else "— inactivo"}</div>', unsafe_allow_html=True)
        # Pequeños datos adicionales
        st.markdown(f'<div style="margin-top:0.5rem;font-size:0.75rem;color:#6E00B3">{semanas} semanas · {meses} meses · {anos} años</div>', unsafe_allow_html=True)

# ---- Row 3: Detalle cards ----
if mostrar_detalle:
    col_cd, col_cp, col_pr = st.columns(3)

    with col_cd:
        with st.container(key="card-countdown"):
            st.markdown('<div class="card-heading">🔁 Cuenta regresiva</div>', unsafe_allow_html=True)
            if _fin > datetime.now():
                restante = _fin - datetime.now()
                s, dd, hh, mm, ss, _, _, _ = desglose(restante)
                st.markdown(f'<div style="font-size:1rem;color:#3C0061"><strong>{dd}</strong> días, <strong>{hh}</strong> h, <strong>{mm}</strong> min</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:0.72rem;color:var(--dc-acento);margin-bottom:0.4rem">Hasta {_fin:%d/%m/%Y %H:%M}</div>', unsafe_allow_html=True)
                p = max(0.0, min(1.0, (datetime.now() - _inicio).total_seconds() / max(1, delta.total_seconds())))
                st.progress(p, text="Progreso")
            else:
                st.markdown('<div style="color:#21A67A;font-weight:600">✅ Ya llegó</div>', unsafe_allow_html=True)

    with col_cp:
        with st.container(key="card-progresiva"):
            st.markdown('<div class="card-heading">➡️ Cuenta progresiva</div>', unsafe_allow_html=True)
            if _inicio < datetime.now():
                trans = datetime.now() - _inicio
                _, dd, hh, mm, ss, _, _, _ = desglose(trans)
                st.markdown(f'<div style="font-size:1rem;color:#3C0061">Pasaron <strong>{dd}</strong> días</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:0.72rem;color:var(--dc-acento);margin-bottom:0.4rem">Desde {_inicio:%d/%m/%Y %H:%M}</div>', unsafe_allow_html=True)
                pp = max(0.0, min(1.0, trans.total_seconds() / max(1, delta.total_seconds())))
                st.progress(pp, text="Transcurrido")
            else:
                st.markdown('<div style="color:#A0A0B0">⏳ Aún no ocurre</div>', unsafe_allow_html=True)

    with col_pr:
        with st.container(key="card-proporciones"):
            st.markdown('<div class="card-heading">📈 Proporciones</div>', unsafe_allow_html=True)
            datos = {"Días": abs(dias), "Semanas": semanas, "Meses": meses, "Años": anos}
            st.bar_chart(datos, horizontal=True, height=160)

    # ---- Desglose exacto (full-width) ----
    with st.container(key="card-desglose"):
        st.markdown(
            f'<span style="font-weight:600;color:var(--dc-acento)">Detalle exacto:</span> '
            f'{sign*dias} días, {horas} h, {minutos} min, {segundos} s',
            unsafe_allow_html=True,
        )
else:
    st.info("💡 Activa «Mostrar desglose detallado» en la barra lateral para ver cuentas regresivas y proporciones.", icon="💡")

# ---- Row 5: Tools ----
col_t1, col_t2 = st.columns(2)

with col_t1:
    with st.container(key="card-sumar"):
        st.markdown('<div class="card-heading">➕ Sumar / restar tiempo</div>', unsafe_allow_html=True)
        with st.form("form_sumar", border=False):
            st.date_input("Base", value=st.session_state["base"], key="base", label_visibility="collapsed")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.number_input("Cant", min_value=0, value=st.session_state["cantidad"], step=1, key="cantidad", label_visibility="collapsed")
            with c2:
                st.selectbox("Unidad", ["Días", "Semanas", "Meses", "Años"], index=["Días", "Semanas", "Meses", "Años"].index(st.session_state["unidad"]), key="unidad", label_visibility="collapsed")
            with c3:
                st.radio("Op", ["Sumar", "Restar"], index=["Sumar", "Restar"].index(st.session_state["op"]), horizontal=True, key="op", label_visibility="collapsed")
            enviar = st.form_submit_button("Calcular", use_container_width=True)
        if enviar:
            mult = st.session_state["cantidad"] if st.session_state["op"] == "Sumar" else -st.session_state["cantidad"]
            u = st.session_state["unidad"]
            if u == "Días":
                nueva = st.session_state["base"] + timedelta(days=mult)
            elif u == "Semanas":
                nueva = st.session_state["base"] + timedelta(weeks=mult)
            elif u == "Meses":
                mes = st.session_state["base"].month - 1 + mult
                año = st.session_state["base"].year + mes // 12
                mes = mes % 12 + 1
                nueva = st.session_state["base"].replace(year=año, month=mes)
            else:
                nueva = st.session_state["base"].replace(year=st.session_state["base"].year + mult)
            st.markdown(f'<div class="tool-result">📅 {nueva:%d/%m/%Y}</div>', unsafe_allow_html=True)

with col_t2:
    with st.container(key="card-dia"):
        st.markdown('<div class="card-heading">🎯 Día de la semana</div>', unsafe_allow_html=True)
        with st.form("form_dia", border=False):
            st.date_input("Verificar", value=st.session_state["chk"], key="chk", label_visibility="collapsed")
            enviar_dia = st.form_submit_button("Consultar", use_container_width=True)
        if enviar_dia:
            nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            st.markdown(f'<div class="tool-result">{nombres[st.session_state["chk"].weekday()]}</div>', unsafe_allow_html=True)

# ---- Row 6: Reset ----
rc1, rc2, rc3 = st.columns([1, 2, 1])
with rc2:
    if st.button("♻️ Restablecer valores", use_container_width=True, key="btn_reset"):
        for k, v in DEFAULTS.items():
            st.session_state[k] = v
        st.toast("Valores restablecidos.", icon="♻️")
        st.rerun()
