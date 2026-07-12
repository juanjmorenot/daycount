import streamlit as st
from datetime import datetime, timedelta, date, time
import sys
import time as _time
import math
import calendar

if not st.runtime.exists():
    print("[ERROR] Ejecuta con:  streamlit run app.py")
    sys.exit(1)

st.set_page_config(
    page_title="Daycount · Calculadora de Días y Horas",
    page_icon="⏳",
    layout="wide",
)

# =============================================================================
# TEMA – 6 paletas completas, cada una con light y dark
# =============================================================================

PALETTES = {
    "Púrpura oficial": {
        "light": {"primary": "#6E00B3", "accent": "#9D00FF", "bg": "#F7F2F7", "card": "#FFFFFF", "text": "#3C0061", "muted": "#6E00B3", "border": "#E4D7EF", "success": "#21A67A", "warning": "#E8A000", "error": "#B0003A", "gradient": "linear-gradient(180deg, #F7F2F7 0%, #EDE7F0 100%)"},
        "dark":  {"primary": "#B069DB", "accent": "#9D00FF", "bg": "#1A1A2E", "card": "#252542", "text": "#E8E0F0", "muted": "#C79BE0", "border": "#3A3A5C", "success": "#4ADE80", "warning": "#FBBF24", "error": "#F87171", "gradient": "linear-gradient(180deg, #1A1A2E 0%, #16213E 100%)"},
    },
    "Océano": {
        "light": {"primary": "#005A8C", "accent": "#0077BE", "bg": "#F0F7FC", "card": "#FFFFFF", "text": "#002B44", "muted": "#005A8C", "border": "#C5E1F0", "success": "#1B8A5E", "warning": "#D4880F", "error": "#B0003A", "gradient": "linear-gradient(180deg, #F0F7FC 0%, #E3F0F7 100%)"},
        "dark":  {"primary": "#5CB8E8", "accent": "#3D9BE0", "bg": "#0D1B2A", "card": "#1B2D3F", "text": "#D6E8F5", "muted": "#8BC4EA", "border": "#2A4055", "success": "#4ADE80", "warning": "#FBBF24", "error": "#F87171", "gradient": "linear-gradient(180deg, #0D1B2A 0%, #1A2D3E 100%)"},
    },
    "Bosque": {
        "light": {"primary": "#2E6B3A", "accent": "#3D8C4C", "bg": "#F2F8F3", "card": "#FFFFFF", "text": "#1A3D22", "muted": "#2E6B3A", "border": "#C8E0CD", "success": "#21A67A", "warning": "#D4880F", "error": "#B0003A", "gradient": "linear-gradient(180deg, #F2F8F3 0%, #E5F0E8 100%)"},
        "dark":  {"primary": "#6BC47E", "accent": "#4CAF50", "bg": "#0F1F14", "card": "#1A3322", "text": "#D4EDDA", "muted": "#81C784", "border": "#2A4D35", "success": "#4ADE80", "warning": "#FBBF24", "error": "#F87171", "gradient": "linear-gradient(180deg, #0F1F14 0%, #162E1F 100%)"},
    },
    "Terra": {
        "light": {"primary": "#8B4513", "accent": "#C65D1A", "bg": "#FDF6F0", "card": "#FFFFFF", "text": "#4A250E", "muted": "#8B4513", "border": "#E8D5C3", "success": "#21A67A", "warning": "#D4880F", "error": "#B0003A", "gradient": "linear-gradient(180deg, #FDF6F0 0%, #F5EDE5 100%)"},
        "dark":  {"primary": "#E8975A", "accent": "#D4732A", "bg": "#1E120A", "card": "#2D1C10", "text": "#F0E0D0", "muted": "#C4956A", "border": "#3D2A1A", "success": "#4ADE80", "warning": "#FBBF24", "error": "#F87171", "gradient": "linear-gradient(180deg, #1E120A 0%, #2A1A10 100%)"},
    },
    "Grafito": {
        "light": {"primary": "#3A3A5C", "accent": "#5A5A8C", "bg": "#F5F5F7", "card": "#FFFFFF", "text": "#1C1C2E", "muted": "#3A3A5C", "border": "#D4D4E0", "success": "#21A67A", "warning": "#E8A000", "error": "#B0003A", "gradient": "linear-gradient(180deg, #F5F5F7 0%, #EEEEF2 100%)"},
        "dark":  {"primary": "#A0A0C0", "accent": "#7C7CA8", "bg": "#12121E", "card": "#1E1E30", "text": "#D0D0E0", "muted": "#8888AA", "border": "#2E2E48", "success": "#4ADE80", "warning": "#FBBF24", "error": "#F87171", "gradient": "linear-gradient(180deg, #12121E 0%, #1A1A2C 100%)"},
    },
}

TAB_LABELS = ["📊 Panel", "🧮 Calculadora", "⚖️ Comparador", "⚙️ Configuración"]
MODO_CALCULO = ["Entre dos fechas", "Hasta una fecha objetivo", "Desde una fecha pasada"]
DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# =============================================================================
# SESIÓN – valores por defecto
# =============================================================================

DEFAULTS = {
    "modo_calculo": "Entre dos fechas",
    "d_ini": date.today(), "t_ini": time(0, 0),
    "d_fin": date.today() + timedelta(days=30), "t_fin": time(0, 0),
    "mostrar_detalle": True,
    "tema": "Púrpura oficial",
    "modo_oscuro": False,
    "densidad": "Cómodo",
    "precision": "Exacta",
    "auto_refresh": False,
    "refresh_interval": 10,
    "base": date.today(), "chk": date.today(),
    "cantidad": 7, "unidad": "Días", "op": "Sumar",
    "nacimiento": date(1990, 1, 1),
    "comp_a_ini": date.today(), "comp_a_fin": date.today() + timedelta(days=7),
    "comp_b_ini": date.today(), "comp_b_fin": date.today() + timedelta(days=14),
    "historial": [],
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =============================================================================
# HELPER – desglose de timedelta
# =============================================================================

def desglose(td: timedelta):
    ts = int(td.total_seconds())
    sgn = -1 if ts < 0 else 1
    ts = abs(ts)
    d = ts // 86400
    h = (ts % 86400) // 3600
    m = (ts % 3600) // 60
    seg = ts % 60
    return sgn, d, h, m, seg, d // 7, d // 30, d // 365

def format_diff(sgn, d, h, m):
    parts = []
    if d: parts.append(f"{sgn*d}d")
    if h: parts.append(f"{h}h")
    if m: parts.append(f"{m}m")
    return " ".join(parts) if parts else "0d"

def registrar_historial(modo, inicio, fin, delta_dias):
    h = st.session_state.historial
    entry = {
        "modo": modo,
        "inicio": inicio.strftime("%d/%m/%Y %H:%M"),
        "fin": fin.strftime("%d/%m/%Y %H:%M"),
        "dias": delta_dias,
        "ts": datetime.now().strftime("%H:%M"),
    }
    h.insert(0, entry)
    st.session_state.historial = h[:20]

# =============================================================================
# OBTENER PALETA ACTIVA
# =============================================================================

def paleta_activa():
    base = PALETTES.get(st.session_state.tema, PALETTES["Púrpura oficial"])
    mode = "dark" if st.session_state.modo_oscuro else "light"
    return base[mode]

# =============================================================================
# CSS INYECTADO
# =============================================================================

def inyectar_css(p):
    oscuro = st.session_state.modo_oscuro
    compacto = st.session_state.densidad == "Compacto"
    st.markdown(f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&family=Bitter:wght@500;700&display=swap" rel="stylesheet">

    <style>
        :root {{
            --dc-primary: {p["primary"]};
            --dc-accent: {p["accent"]};
            --dc-bg: {p["bg"]};
            --dc-card: {p["card"]};
            --dc-text: {p["text"]};
            --dc-muted: {p["muted"]};
            --dc-border: {p["border"]};
            --dc-success: {p["success"]};
            --dc-warning: {p["warning"]};
            --dc-error: {p["error"]};
            --dc-gradient: {p["gradient"]};
            --dc-radius: {"10px" if compacto else "14px"};
            --dc-pad: {"0.75rem 1rem" if compacto else "1.25rem 1.5rem"};
            --dc-gap: {"0.4rem" if compacto else "0.75rem"};
            --font: 'Open Sans', sans-serif;
        }}
        .stApp {{ background: var(--dc-gradient) !important; color: var(--dc-text); }}
        .stAppHeader {{ display: none !important; }}
        a {{ color: var(--dc-primary) !important; }}

        /* Bento cards */
        div[class*="st-key-card-"], div[class^="st-key-card-"] {{
            background: var(--dc-card) !important;
            border-radius: var(--dc-radius) !important;
            padding: var(--dc-pad) !important;
            border: 1px solid var(--dc-border) !important;
            box-shadow: 0 2px 6px rgba(0,0,0,{0.08 if oscuro else 0.04}) !important;
            height: 100%;
        }}
        .card-heading {{
            font-family: 'Open Sans', sans-serif;
            font-weight: 600;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--dc-muted);
            margin-bottom: 0.5rem;
        }}

        /* Hero */
        .st-key-card-hero {{ text-align: center !important; }}
        .hero-unit {{
            font-family: 'Bitter', serif; font-weight: 700; font-size: 0.85rem;
            color: var(--dc-muted); text-transform: uppercase; letter-spacing: 0.06em;
        }}
        .hero-number {{
            font-family: 'Open Sans', sans-serif; font-weight: 800;
            font-size: clamp(2.5rem, 7vw, 5rem); line-height: 1.05;
            color: var(--dc-text); margin: 0.1rem 0;
        }}
        .hero-number.negative {{ color: var(--dc-error); }}
        .hero-direction {{ font-size: 1rem; color: var(--dc-muted); margin-bottom: 0.5rem; }}
        .hero-metrics {{
            display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap;
            padding-top: 0.75rem; border-top: 1px solid var(--dc-border);
        }}
        .hm-item {{ text-align: center; min-width: 70px; }}
        .hm-value {{ font-weight: 700; font-size: 1.2rem; color: var(--dc-text); }}
        .hm-label {{
            font-size: 0.65rem; font-weight: 600; color: var(--dc-muted);
            text-transform: uppercase; letter-spacing: 0.04em; margin-top: 0.05rem;
        }}

        /* Status */
        .status-mode {{ font-weight: 600; font-size: 0.9rem; color: var(--dc-text); }}
        .neg-flag {{
            display: inline-flex; align-items: center; gap: 0.4rem;
            padding: 0.35rem 0.7rem; border-radius: 8px;
            font-weight: 600; font-size: 0.8rem;
            background: {"#2A1520" if oscuro else "#FFF0F0"};
            color: var(--dc-error); border: 1px solid {"#4A2030" if oscuro else "#FFD4D4"};
        }}

        /* Labels */
        .fecha-label {{ font-size: 0.72rem; font-weight: 600; color: var(--dc-muted); margin-bottom: 0.15rem; }}

        /* Progress */
        .stProgress > div > div {{ background-color: var(--dc-accent) !important; border-radius: 20px !important; }}

        /* Buttons */
        .stButton > button {{
            background-color: var(--dc-accent) !important;
            color: #FFFFFF !important; border: none !important;
            border-radius: 10px !important; font-weight: 600 !important;
            font-family: 'Open Sans', sans-serif !important;
        }}
        .stButton > button:hover {{ opacity: 0.85 !important; }}

        /* Sidebar */
        .stSidebar {{ background-color: {"#1A1A2E" if oscuro else "#EDE7F0"} !important; padding: 1rem !important; }}

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{ gap: 0.5rem; }}
        .stTabs [data-baseweb="tab"] {{
            font-family: 'Open Sans', sans-serif; font-weight: 600;
            border-radius: 8px 8px 0 0;
        }}

        /* Dividers */
        hr {{ border-color: var(--dc-border) !important; margin: 0.75rem 0 !important; }}

        /* Code / tool result */
        .tool-result {{ text-align: center; font-size: 1.1rem; font-weight: 600; color: var(--dc-text); margin-top: 0.5rem; }}
        .tool-sub {{ text-align: center; font-size: 0.85rem; color: var(--dc-muted); }}

        /* Historial item */
        .hist-item {{
            padding: 0.4rem 0.6rem; border-radius: 8px;
            background: {"#1E1E30" if oscuro else "#F5F0FA"};
            margin-bottom: 0.35rem; font-size: 0.82rem;
            border-left: 3px solid var(--dc-accent);
        }}
        .hist-item strong {{ color: var(--dc-text); }}

        /* Comparador */
        .comp-badge {{
            display: inline-block; padding: 0.2rem 0.6rem; border-radius: 6px;
            font-weight: 700; font-size: 0.75rem;
        }}
        .comp-a {{ background: {"#2A1540" if oscuro else "#F0E5F7"}; color: var(--dc-primary); }}
        .comp-b {{ background: {"#153040" if oscuro else "#E5F0F7"}; color: #005A8C; }}

        /* Config section */
        .config-section {{ margin-bottom: 1rem; }}
        .config-section h4 {{ color: var(--dc-muted); font-size: 0.85rem; margin-bottom: 0.3rem; }}

        @media (max-width: 640px) {{
            [data-testid="stHorizontalBlock"] {{ flex-direction: column !important; }}
        }}
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# HEADER / BRANDING
# =============================================================================

def mostrar_header():
    c1, c2 = st.columns([4, 1])
    with c1:
        st.markdown(
            '<span style="font-family:Open Sans,sans-serif;font-weight:800;font-size:1.8rem;letter-spacing:-0.5px;color:var(--dc-accent)">Day</span>'
            '<span style="font-family:Open Sans,sans-serif;font-weight:800;font-size:1.8rem;letter-spacing:-0.5px;color:var(--dc-primary)">count</span>'
            '<span style="font-family:Open Sans,sans-serif;font-weight:400;font-size:0.9rem;color:var(--dc-muted);margin-left:0.75rem">· Calculadora de Días y Horas</span>',
            unsafe_allow_html=True,
        )
    with c2:
        now_str = datetime.now().strftime("%d %b %Y · %H:%M")
        st.markdown(f'<div style="text-align:right;font-size:0.78rem;color:var(--dc-muted);font-weight:600">{now_str}</div>',
                    unsafe_allow_html=True)

# =============================================================================
# LÓGICA PRINCIPAL DE CÁLCULO
# =============================================================================

def calcular():
    modo = st.session_state.modo_calculo
    inicio = datetime.combine(st.session_state.d_ini, st.session_state.t_ini)
    fin = datetime.combine(st.session_state.d_fin, st.session_state.t_fin)

    if modo == "Hasta una fecha objetivo":
        inicio = datetime.now()
    elif modo == "Desde una fecha pasada":
        fin = datetime.now()

    delta = fin - inicio
    sgn, d, h, m, seg, sem, mes, an = desglose(delta)
    return inicio, fin, delta, sgn, d, h, m, seg, sem, mes, an

# =============================================================================
# SIDEBAR – CONFIGURACIÓN GLOBAL
# =============================================================================

def sidebar_config():
    with st.sidebar:
        st.markdown('<div class="card-heading" style="margin-top:0">⚙️ Configuración</div>', unsafe_allow_html=True)

        tema = st.selectbox(
            "Paleta de color",
            list(PALETTES.keys()),
            index=list(PALETTES.keys()).index(st.session_state.tema),
            key="tema",
        )
        modo_oscuro = st.toggle("Modo oscuro", value=st.session_state.modo_oscuro, key="modo_oscuro",
                                help="Alterna entre variante clara y oscura de la paleta actual")

        p = paleta_activa()
        st.markdown(
            f'<div style="display:flex;gap:0.3rem;margin:0.25rem 0 0.75rem">'
            f'<span style="display:inline-block;width:18px;height:18px;border-radius:4px;background:{p["primary"]}"></span>'
            f'<span style="display:inline-block;width:18px;height:18px;border-radius:4px;background:{p["accent"]}"></span>'
            f'<span style="display:inline-block;width:18px;height:18px;border-radius:4px;background:{p["card"]};border:1px solid {p["border"]}"></span>'
            f'<span style="display:inline-block;width:18px;height:18px;border-radius:4px;background:{p["bg"]};border:1px solid {p["border"]}"></span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.radio("Densidad", ["Cómodo", "Compacto"],
                 index=["Cómodo", "Compacto"].index(st.session_state.densidad),
                 key="densidad", horizontal=True)
        st.radio("Precisión", ["Exacta", "Redondeada"],
                 index=["Exacta", "Redondeada"].index(st.session_state.precision),
                 key="precision", horizontal=True)

        st.markdown("---")
        st.toggle("Mostrar desglose detallado", value=st.session_state.mostrar_detalle,
                   key="mostrar_detalle", help="Muestra cuentas regresivas, progreso y proporciones")
        auto_refresh = st.toggle("Actualización automática", value=st.session_state.auto_refresh,
                                  key="auto_refresh", help="Recarga automática para datos en tiempo real")
        if auto_refresh:
            st.select_slider("Intervalo (seg)", options=[5, 10, 15, 30, 60],
                             value=st.session_state.refresh_interval, key="refresh_interval")

        st.markdown("---")
        modo = st.radio(
            "Modo de cálculo",
            MODO_CALCULO,
            index=MODO_CALCULO.index(st.session_state.modo_calculo),
            key="modo_calculo",
        )

        if st.button("♻️ Restablecer todo", use_container_width=True, type="secondary"):
            for k, v in DEFAULTS.items():
                if k != "historial":
                    st.session_state[k] = v
            st.toast("Valores restablecidos.", icon="♻️")
            st.rerun()

# =============================================================================
# TAB 0 – PANEL (Dashboard)
# =============================================================================

def tab_panel():
    p = paleta_activa()
    inicio, fin, delta, sgn, d, h, m, seg, sem, mes, an = calcular()
    ahora = datetime.now()

    # Auto-refresh
    if st.session_state.auto_refresh:
        last = st.session_state.get("_last_refresh", 0)
        now_t = _time.time()
        if now_t - last >= st.session_state.refresh_interval:
            st.session_state._last_refresh = now_t
            st.rerun()

    # ── Hero ──
    direccion = "↩ atrás" if sgn < 0 else "↪ adelante"
    neg_class = " negative" if sgn < 0 else ""
    exacta = st.session_state.precision == "Exacta"
    total_h = sgn * (d * 24 + h)
    total_m = sgn * (d * 1440 + h * 60 + m)
    total_s = sgn * (d * 86400 + h * 3600 + m * 60 + seg)

    with st.container(key="card-hero"):
        st.markdown(f"""
        <div class="hero-unit">Días</div>
        <div class="hero-number{neg_class}">{sgn*d:,}</div>
        <div class="hero-direction">{direccion}{' · ' + format_diff(sgn, d, h, m) if exacta else ''}</div>
        <div class="hero-metrics">
            <div class="hm-item"><div class="hm-value">{sgn*sem:,}</div><div class="hm-label">Semanas</div></div>
            <div class="hm-item"><div class="hm-value">{sgn*mes:,}</div><div class="hm-label">Meses</div></div>
            <div class="hm-item"><div class="hm-value">{sgn*an:,}</div><div class="hm-label">Años</div></div>
        </div>
        """ if not exacta else f"""
        <div class="hero-unit">Días</div>
        <div class="hero-number{neg_class}">{sgn*d:,}</div>
        <div class="hero-direction">{direccion} · {format_diff(sgn, d, h, m)}</div>
        <div class="hero-metrics">
            <div class="hm-item"><div class="hm-value">{total_h:,}</div><div class="hm-label">Horas</div></div>
            <div class="hm-item"><div class="hm-value">{total_m:,}</div><div class="hm-label">Minutos</div></div>
            <div class="hm-item"><div class="hm-value">{total_s:,}</div><div class="hm-label">Segundos</div></div>
        </div>
        """, unsafe_allow_html=True)

    registrar_historial(st.session_state.modo_calculo, inicio, fin, sgn * d)

    # ── Row 2: fechas + estado ──
    cf, cs = st.columns([1.6, 1])
    with cf:
        with st.container(key="card-fechas"):
            st.markdown('<div class="card-heading">📅 Fechas</div>', unsafe_allow_html=True)
            fc1, fc2 = st.columns(2)
            with fc1:
                st.markdown('<div class="fecha-label">Inicio</div>', unsafe_allow_html=True)
                st.date_input("ini_d", key="d_ini", label_visibility="collapsed")
                st.time_input("ini_t", key="t_ini", label_visibility="collapsed")
            with fc2:
                st.markdown('<div class="fecha-label">Fin</div>', unsafe_allow_html=True)
                st.date_input("fin_d", key="d_fin", label_visibility="collapsed")
                st.time_input("fin_t", key="t_fin", label_visibility="collapsed")
    with cs:
        with st.container(key="card-status"):
            st.markdown('<div class="card-heading">⚙️ Estado</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="status-mode">Modo: <strong>{st.session_state.modo_calculo}</strong></div>',
                        unsafe_allow_html=True)
            st.markdown(f'<div style="margin:0.25rem 0;font-size:0.85rem;color:var(--dc-muted)">'
                        f'Inicio: {inicio:%d/%m/%Y %H:%M} &nbsp;·&nbsp; Fin: {fin:%d/%m/%Y %H:%M}</div>',
                        unsafe_allow_html=True)
            if sgn < 0:
                st.markdown('<div class="neg-flag">⚠️ Fin anterior a inicio</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div style="margin-top:0.4rem;font-size:0.78rem;color:var(--dc-muted)">'
                f'{sem} semanas · {mes} meses · {an} años'
                f'</div>', unsafe_allow_html=True)

    # ── Row 3: detalle ──
    if st.session_state.mostrar_detalle:
        c_cd, c_cp, c_pr = st.columns(3)
        with c_cd:
            with st.container(key="card-countdown"):
                st.markdown('<div class="card-heading">🔁 Cuenta regresiva</div>', unsafe_allow_html=True)
                if fin > ahora:
                    restante = fin - ahora
                    _, dd, hh, mm, ss, _, _, _ = desglose(restante)
                    st.markdown(f'<div style="font-size:1rem;color:var(--dc-text)"><strong>{dd}</strong> días, <strong>{hh}</strong> h, <strong>{mm}</strong> min</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="font-size:0.72rem;color:var(--dc-muted);margin-bottom:0.4rem">Hasta {fin:%d/%m/%Y %H:%M}</div>', unsafe_allow_html=True)
                    total_seg = max(1, delta.total_seconds())
                    pct = max(0.0, min(1.0, (ahora - inicio).total_seconds() / total_seg))
                    st.progress(pct, text="Progreso")
                else:
                    st.markdown(f'<div style="color:var(--dc-success);font-weight:600">✅ Ya llegó</div>', unsafe_allow_html=True)
        with c_cp:
            with st.container(key="card-progresiva"):
                st.markdown('<div class="card-heading">➡️ Cuenta progresiva</div>', unsafe_allow_html=True)
                if inicio < ahora:
                    trans = ahora - inicio
                    _, dd, hh, mm, ss, _, _, _ = desglose(trans)
                    st.markdown(f'<div style="font-size:1rem;color:var(--dc-text)">Pasaron <strong>{dd}</strong> días</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="font-size:0.72rem;color:var(--dc-muted);margin-bottom:0.4rem">Desde {inicio:%d/%m/%Y %H:%M}</div>', unsafe_allow_html=True)
                    total_seg = max(1, delta.total_seconds())
                    pp = max(0.0, min(1.0, trans.total_seconds() / total_seg))
                    st.progress(pp, text="Transcurrido")
                else:
                    st.markdown(f'<div style="color:#A0A0B0">⏳ Aún no ocurre</div>', unsafe_allow_html=True)
        with c_pr:
            with st.container(key="card-proporciones"):
                st.markdown('<div class="card-heading">📈 Proporciones</div>', unsafe_allow_html=True)
                datos = {"Días": abs(d), "Semanas": sem, "Meses": mes, "Años": an}
                st.bar_chart(datos, horizontal=True, height=140)

        with st.container(key="card-desglose"):
            st.markdown(
                f'<span style="font-weight:600;color:var(--dc-muted)">Detalle exacto:</span> '
                f'{sgn*d} días, {h} h, {m} min, {seg} s',
                unsafe_allow_html=True,
            )
    else:
        st.info("💡 Activa «Mostrar desglose detallado» en la barra lateral para ver cuentas regresivas y proporciones.", icon="💡")

    # ── Historial ──
    if st.session_state.historial:
        with st.expander("📜 Historial de cálculos recientes", expanded=False):
            for entry in st.session_state.historial[:10]:
                st.markdown(
                    f'<div class="hist-item">'
                    f'<strong>{entry["dias"]:,} días</strong> · {entry["modo"]} · '
                    f'{entry["inicio"]} → {entry["fin"]} '
                    f'<span style="color:var(--dc-muted);font-size:0.75rem">({entry["ts"]})</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

# =============================================================================
# TAB 1 – CALCULADORA
# =============================================================================

def tab_calculadora():
    tc1, tc2 = st.columns(2)

    with tc1:
        with st.container(key="card-sumar"):
            st.markdown('<div class="card-heading">➕ Sumar / restar tiempo</div>', unsafe_allow_html=True)
            with st.form("form_sumar", border=False):
                st.date_input("Base", key="base", label_visibility="collapsed")
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.number_input("Cant", min_value=0, key="cantidad", label_visibility="collapsed")
                with c2:
                    st.selectbox("Unidad", ["Días", "Semanas", "Meses", "Años"],
                                 key="unidad", label_visibility="collapsed")
                with c3:
                    st.radio("Op", ["Sumar", "Restar"], horizontal=True, key="op", label_visibility="collapsed")
                enviar = st.form_submit_button("Calcular", use_container_width=True)
            if enviar:
                mult = st.session_state.cantidad if st.session_state.op == "Sumar" else -st.session_state.cantidad
                u = st.session_state.unidad
                base = st.session_state.base
                if u == "Días":
                    nueva = base + timedelta(days=mult)
                elif u == "Semanas":
                    nueva = base + timedelta(weeks=mult)
                elif u == "Meses":
                    mes = base.month - 1 + mult
                    año = base.year + mes // 12
                    mes = mes % 12 + 1
                    nueva = date(año, mes, min(base.day, [31, 29 if año % 4 == 0 and (año % 100 != 0 or año % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mes - 1]))
                else:
                    nueva = date(base.year + mult, base.month, base.day)
                st.markdown(f'<div class="tool-result">📅 {nueva:%d/%m/%Y}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="tool-sub">{DIAS_SEMANA[nueva.weekday()]}</div>', unsafe_allow_html=True)

    with tc2:
        with st.container(key="card-dia"):
            st.markdown('<div class="card-heading">🎯 Día de la semana</div>', unsafe_allow_html=True)
            with st.form("form_dia", border=False):
                st.date_input("Verificar", key="chk", label_visibility="collapsed")
                enviar_dia = st.form_submit_button("Consultar", use_container_width=True)
            if enviar_dia:
                st.markdown(f'<div class="tool-result">{DIAS_SEMANA[st.session_state.chk.weekday()]}</div>', unsafe_allow_html=True)

    # -- Fila 2 --
    tc3, tc4 = st.columns(2)

    with tc3:
        with st.container(key="card-edad"):
            st.markdown('<div class="card-heading">🎂 Calcular edad</div>', unsafe_allow_html=True)
            with st.form("form_edad", border=False):
                st.date_input("Fecha de nacimiento", key="nacimiento", label_visibility="collapsed")
                enviar_edad = st.form_submit_button("Calcular edad", use_container_width=True)
            if enviar_edad:
                hoy = date.today()
                nac = st.session_state.nacimiento
                if nac > hoy:
                    st.markdown(f'<div class="tool-result" style="color:var(--dc-error)">⚠️ Fecha futura</div>', unsafe_allow_html=True)
                else:
                    años = hoy.year - nac.year - ((hoy.month, hoy.day) < (nac.month, nac.day))
                    cumple = date(hoy.year, nac.month, nac.day)
                    if cumple < hoy:
                        prox = date(hoy.year + 1, nac.month, nac.day)
                    elif cumple == hoy:
                        prox = cumple
                    else:
                        prox = cumple
                    dias_prox = (prox - hoy).days
                    # meses total
                    meses_tot = años * 12 + (hoy.month - nac.month) if hoy.day >= nac.day else años * 12 + (hoy.month - nac.month - 1)
                    st.markdown(f'<div class="tool-result">{años} años</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="tool-sub">{meses_tot} meses · ≈ {años*365 + (hoy - date(hoy.year - años, nac.month, nac.day)).days:,} días</div>', unsafe_allow_html=True)
                    if dias_prox > 0:
                        st.markdown(f'<div class="tool-sub" style="margin-top:0.2rem">🎉 Próximo cumpleaños en {dias_prox} días</div>', unsafe_allow_html=True)
                    elif dias_prox == 0:
                        st.markdown(f'<div class="tool-sub" style="margin-top:0.2rem;color:var(--dc-success);font-weight:700">🎉 ¡Hoy es su cumpleaños!</div>', unsafe_allow_html=True)

    with tc4:
        with st.container(key="card-relativas"):
            st.markdown('<div class="card-heading">📌 Fechas relativas</div>', unsafe_allow_html=True)
            with st.form("form_rel", border=False):
                base_rel = st.date_input("Desde", value=date.today(), label_visibility="collapsed")
                opcion = st.selectbox("Calcular", [
                    "Próximo lunes", "Próximo mes",
                    "Último día del mes", "Primer día del próximo mes",
                    "Fin de año", "Días hasta fin de año",
                ], label_visibility="collapsed")
                enviar_rel = st.form_submit_button("Calcular", use_container_width=True)
            if enviar_rel:
                if opcion == "Próximo lunes":
                    diff = (7 - base_rel.weekday()) % 7
                    if diff == 0:
                        diff = 7
                    target = base_rel + timedelta(days=diff)
                    st.markdown(f'<div class="tool-result">{target:%d/%m/%Y}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="tool-sub">En {diff} días ({DIAS_SEMANA[target.weekday()]})</div>', unsafe_allow_html=True)
                elif opcion == "Próximo mes":
                    m = base_rel.month % 12 + 1
                    y = base_rel.year + (1 if base_rel.month == 12 else 0)
                    target = date(y, m, 1)
                    st.markdown(f'<div class="tool-result">{target:%d/%m/%Y}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="tool-sub">En {(target - base_rel).days} días</div>', unsafe_allow_html=True)
                elif opcion == "Último día del mes":
                    _, last = calendar.monthrange(base_rel.year, base_rel.month)
                    target = date(base_rel.year, base_rel.month, last)
                    st.markdown(f'<div class="tool-result">{target:%d/%m/%Y}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="tool-sub">En {(target - base_rel).days} días ({DIAS_SEMANA[target.weekday()]})</div>', unsafe_allow_html=True)
                elif opcion == "Primer día del próximo mes":
                    m = base_rel.month % 12 + 1
                    y = base_rel.year + (1 if base_rel.month == 12 else 0)
                    target = date(y, m, 1)
                    st.markdown(f'<div class="tool-result">{target:%d/%m/%Y}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="tool-sub">En {(target - base_rel).days} días ({DIAS_SEMANA[target.weekday()]})</div>', unsafe_allow_html=True)
                elif opcion == "Fin de año":
                    target = date(base_rel.year, 12, 31)
                    st.markdown(f'<div class="tool-result">{target:%d/%m/%Y}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="tool-sub">En {(target - base_rel).days} días ({DIAS_SEMANA[target.weekday()]})</div>', unsafe_allow_html=True)
                elif opcion == "Días hasta fin de año":
                    target = date(base_rel.year, 12, 31)
                    diff_days = (target - base_rel).days
                    st.markdown(f'<div class="tool-result">{diff_days} días</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="tool-sub">Hasta el {target:%d/%m/%Y}</div>', unsafe_allow_html=True)

# =============================================================================
# TAB 2 – COMPARADOR
# =============================================================================

def tab_comparador():
    st.markdown('<div class="card-heading" style="margin-bottom:0.75rem">⚖️ Comparar dos periodos</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        with st.container(key="card-comp-a"):
            st.markdown(f'<div class="card-heading"><span class="comp-badge comp-a">A</span> Periodo A</div>', unsafe_allow_html=True)
            st.date_input("A Inicio", key="comp_a_ini", label_visibility="collapsed")
            st.date_input("A Fin", key="comp_a_fin", label_visibility="collapsed")
    with col_b:
        with st.container(key="card-comp-b"):
            st.markdown(f'<div class="card-heading"><span class="comp-badge comp-b">B</span> Periodo B</div>', unsafe_allow_html=True)
            st.date_input("B Inicio", key="comp_b_ini", label_visibility="collapsed")
            st.date_input("B Fin", key="comp_b_fin", label_visibility="collapsed")

    a_ini = st.session_state.comp_a_ini
    a_fin = st.session_state.comp_a_fin
    b_ini = st.session_state.comp_b_ini
    b_fin = st.session_state.comp_b_fin

    dur_a = abs((a_fin - a_ini).days)
    dur_b = abs((b_fin - b_ini).days)
    ini_diff = abs((a_ini - b_ini).days)
    fin_diff = abs((a_fin - b_fin).days)
    delta_centro = abs(((a_ini + (a_fin - a_ini) / 2) - (b_ini + (b_fin - b_ini) / 2)).days)

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("Duración A", f"{dur_a} días", delta=None)
    with col_m2:
        st.metric("Duración B", f"{dur_b} días", delta=None)
    with col_m3:
        dif = dur_a - dur_b
        st.metric("Diferencia", f"{abs(dif)} días", delta=f"{'A > B' if dif > 0 else 'B > A' if dif < 0 else '='}")
    with col_m4:
        st.metric("Inicio de A vs B", f"{ini_diff} días", delta=None)

    col_m5, col_m6, col_m7 = st.columns(3)
    with col_m5:
        st.metric("Fin de A vs B", f"{fin_diff} días")
    with col_m6:
        st.metric("Centro desplazado", f"{delta_centro} días")
    with col_m7:
        # Overlap
        overlap_start = max(a_ini, b_ini)
        overlap_end = min(a_fin, b_fin)
        overlap_days = max(0, (overlap_end - overlap_start).days + 1)
        st.metric("Solapamiento", f"{overlap_days} días")

    if overlap_days > 0:
        st.markdown(f'<div style="text-align:center;font-size:0.9rem;color:var(--dc-muted);margin-top:0.5rem">'
                    f'Los periodos se solapan del {overlap_start:%d/%m/%Y} al {overlap_end:%d/%m/%Y}'
                    f'</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align:center;font-size:0.9rem;color:var(--dc-error);margin-top:0.5rem">'
                    f'⚠️ Los periodos no se solapan'
                    f'</div>', unsafe_allow_html=True)

    # Visual timeline
    all_dates = [a_ini, a_fin, b_ini, b_fin]
    min_date = min(all_dates)
    max_date = max(all_dates)
    total_range = max(1, (max_date - min_date).days)

    def pos(d):
        return (d - min_date).days / total_range * 100

    timeline_html = f"""
    <div style="position:relative;height:80px;margin:1rem 0;background:var(--dc-border);border-radius:6px;">
        <div style="position:absolute;left:{pos(a_ini)}%;width:{(a_fin - a_ini).days / total_range * 100}%;height:20px;top:10px;background:var(--dc-primary);border-radius:4px;opacity:0.7;">
            <span style="position:absolute;left:4px;top:2px;font-size:0.6rem;color:white;font-weight:600">A</span>
        </div>
        <div style="position:absolute;left:{pos(b_ini)}%;width:{(b_fin - b_ini).days / total_range * 100}%;height:20px;top:40px;background:var(--dc-accent);border-radius:4px;opacity:0.7;">
            <span style="position:absolute;left:4px;top:2px;font-size:0.6rem;color:white;font-weight:600">B</span>
        </div>
    </div>
    <div style="display:flex;justify-content:space-between;font-size:0.7rem;color:var(--dc-muted)">
        <span>{min_date:%d/%m/%Y}</span>
        <span>{max_date:%d/%m/%Y}</span>
    </div>
    """
    st.markdown(timeline_html, unsafe_allow_html=True)

# =============================================================================
# TAB 3 – CONFIGURACIÓN
# =============================================================================

def tab_config():
    st.markdown('<div class="card-heading" style="margin-bottom:0.75rem">⚙️ Configuración avanzada</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        with st.container(key="card-cfg-tema"):
            st.markdown('<div class="card-heading">🎨 Personalizar tema</div>', unsafe_allow_html=True)
            tema_actual = st.session_state.tema
            for nombre, paleta in PALETTES.items():
                lt = paleta["light"]
                color = lt["primary"]
                selected = " ✓" if nombre == tema_actual else ""
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:0.5rem;padding:0.3rem 0">'
                    f'<span style="display:inline-block;width:20px;height:20px;border-radius:50%;background:{color};border:2px solid {"var(--dc-text)" if nombre == tema_actual else "transparent"}"></span>'
                    f'<span style="font-size:0.9rem;font-weight:{700 if nombre == tema_actual else 400}">{nombre}{selected}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            st.info("Selecciona el tema en el panel lateral", icon="💡")

    with c2:
        with st.container(key="card-cfg-prefs"):
            st.markdown('<div class="card-heading">🔧 Preferencias</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="font-size:0.85rem;margin:0.25rem 0">'
                        f'<strong>Densidad:</strong> {st.session_state.densidad}<br>'
                        f'<strong>Precisión:</strong> {st.session_state.precision}<br>'
                        f'<strong>Modo oscuro:</strong> {"Activado" if st.session_state.modo_oscuro else "Desactivado"}<br>'
                        f'<strong>Auto-refresh:</strong> {"Cada " + str(st.session_state.refresh_interval) + "s" if st.session_state.auto_refresh else "Desactivado"}<br>'
                        f'<strong>Modo cálculo:</strong> {st.session_state.modo_calculo}'
                        f'</div>', unsafe_allow_html=True)

    with st.container(key="card-cfg-info"):
        st.markdown('<div class="card-heading">ℹ️ Acerca de Daycount</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div style="font-size:0.85rem;color:var(--dc-text)">'
            f'<strong>Daycount</strong> — Calculadora de Días y Horas v2.0<br><br>'
            f'Construida con <a href="https://streamlit.io" target="_blank">Streamlit</a> · '
            f'Open Source · MVP<br>'
            f'<span style="color:var(--dc-muted)">© 2024 — Daycount</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    rc1, rc2, rc3 = st.columns([1, 2, 1])
    with rc2:
        if st.button("♻️ Restablecer todos los valores", use_container_width=True, type="secondary"):
            for k, v in DEFAULTS.items():
                if k != "historial":
                    st.session_state[k] = v
            st.toast("Valores restablecidos.", icon="♻️")
            st.rerun()

# =============================================================================
# MAIN
# =============================================================================

p = paleta_activa()
inyectar_css(p)
mostrar_header()
sidebar_config()

tabs = st.tabs(TAB_LABELS)
with tabs[0]:
    tab_panel()
with tabs[1]:
    tab_calculadora()
with tabs[2]:
    tab_comparador()
with tabs[3]:
    tab_config()
