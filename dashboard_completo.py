import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import unicodedata
import json
import datetime

# ==========================================
# CONFIGURACIÓN DE PÁGINA Y ESTÉTICA
# ==========================================
st.set_page_config(page_title="Dashboard Directivo", layout="wide", initial_sidebar_state="collapsed")

ID_TABLERO_PROYECTOS = "18423885274" 

# CSS ULTRA PREMIUM Y COMPONENTES CUSTOM
st.markdown('''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;800&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Montserrat', sans-serif !important; }
    .stApp { background-color: #f1f5f9; }
    .block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 1600px; }
    
    h1 { color: #0f172a; text-align: center; font-weight: 800; font-size: 2.8rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0px; padding-top: 0px; }
    .subtitle { color: #0284c7; text-align: center; font-size: 1.1rem; font-weight: 600; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 10px; margin-top: 5px; }
    .branded-divider { height: 4px; background: linear-gradient(90deg, rgba(2,132,199,0) 0%, rgba(2,132,199,1) 50%, rgba(2,132,199,0) 100%); border-radius: 2px; margin-top: 15px; margin-bottom: 40px; }
    
    .section-title { color: #1e293b; font-size: 1.5rem; font-weight: 800; margin-top: 3.5rem; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 12px; }
    .section-title::before { content: ""; display: inline-block; width: 8px; height: 28px; background-color: #0284c7; border-radius: 4px; }
    
    /* COMPONENTES KPIs GLOBALES SUPERIORES */
    .top-kpi-container { display: flex; justify-content: space-between; gap: 25px; margin-bottom: 20px; }
    .top-kpi-card { flex: 1; background: white; padding: 25px; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); border: 1px solid #e2e8f0; display: flex; align-items: center; gap: 20px; transition: transform 0.3s ease; }
    .top-kpi-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.08); }
    .top-kpi-icon { width: 65px; height: 65px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 32px; color: white; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    .top-kpi-details { display: flex; flex-direction: column; }
    .top-kpi-title { font-size: 0.85rem; font-weight: 800; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .top-kpi-value { font-size: 2.4rem; font-weight: 800; color: #0f172a; line-height: 1; }
    
    /* COMPONENTES ZOOM DE PROYECTO */
    .info-bar-container { display: flex; flex-wrap: wrap; justify-content: space-around; align-items: center; background: white; padding: 25px 30px; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); margin-bottom: 25px; border: 1px solid #e2e8f0; }
    .info-item { display: flex; align-items: center; gap: 18px; }
    .info-icon { font-size: 32px; color: #475569; }
    .info-text-label { font-size: 0.75rem; font-weight: 800; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2px;}
    .info-text-val { font-size: 1.05rem; font-weight: 700; color: #0f172a; line-height: 1.2;}
    .info-divider { height: 40px; width: 2px; background: #f1f5f9; }
    
    .kpi-card-custom { background: white; padding: 25px 20px; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); text-align: center; border: 1px solid #e2e8f0; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 270px;}
    .kpi-title { font-size: 0.9rem; font-weight: 800; color: #1e293b; text-transform: uppercase; margin-bottom: 15px;}
    
    .icon-box-square { display: flex; align-items: center; justify-content: center; width: 70px; height: 70px; border-radius: 16px; font-size: 35px; color: white; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);}
    .icon-box-circle { display: flex; align-items: center; justify-content: center; width: 80px; height: 80px; border-radius: 50%; font-size: 40px; margin-bottom: 15px; }
    
    .kpi-pill { color: white; padding: 6px 18px; border-radius: 20px; font-weight: 700; font-size: 0.9rem; margin-bottom: 12px; letter-spacing: 0.5px;}
    .kpi-subtext { font-size: 0.85rem; color: #64748b; font-weight: 500;}
    
    /* Gráfico Circular SVG */
    .flex-wrapper { display: flex; justify-content: center; align-items: center; margin: 10px 0; }
    .single-chart { width: 140px; justify-content: center; }
    .circular-chart { display: block; margin: 0 auto; max-width: 100%; max-height: 250px; }
    .circle-bg { fill: none; stroke: #f1f5f9; stroke-width: 3.5; }
    .circle { fill: none; stroke-width: 3.5; stroke-linecap: round; animation: progress 1s ease-out forwards; }
    @keyframes progress { 0% { stroke-dasharray: 0 100; } }
    .circular-chart.green .circle { stroke: #10b981; }
    .percentage { fill: #0f172a; font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 0.45em; text-anchor: middle; }

    /* Hitos */
    .milestone-container { background: white; padding: 25px; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); border: 1px solid #e2e8f0; height: 100%; min-height: 270px; }
    .milestone-item { display: flex; align-items: center; justify-content: space-between; padding: 14px 0; border-bottom: 1px solid #f1f5f9; }
    .milestone-item:last-child { border-bottom: none; }
    .m-left { display: flex; align-items: center; gap: 15px; }
    .m-icon { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px; font-weight: bold;}
    .m-title { font-size: 0.95rem; font-weight: 700; color: #0f172a; margin:0;}
    .m-subtitle { font-size: 0.8rem; color: #64748b; margin:0; margin-top:3px;}
    .m-date { font-size: 0.9rem; font-weight: 800; text-transform: uppercase; white-space: nowrap; text-align: right; min-width: 95px;}
    
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# ==========================================
# PALETAS Y VARIABLES GLOBALES
# ==========================================
COLOR_MAP_ESTADOS = { 'Completado': '#10b981', 'Cerrado': '#0ea5e9', 'En desarrollo': '#3b82f6', 'En curso': '#f59e0b', 'En pruebas': '#f97316', 'No iniciado': '#cbd5e1', 'Sin iniciar': '#cbd5e1', 'Análisis': '#8b5cf6', '-': '#e2e8f0' }
COLOR_MAP_PRIORIDADES = { '🔴 1': '#ef4444', '🟠 2': '#f97316', '🟡 3': '#eab308', '⚪ -': '#94a3b8' }
COLOR_MAP_AREAS = { 'Supply Chain': '#475569', 'Ecommerce': '#e11d48', 'SSTT': '#f97316', 'Comercial': '#f43f5e', 'Finanzas': '#eab308', 'Internos': '#8b5cf6', 'Transversal': '#3b82f6' }
HOY_FECHA = pd.Timestamp.today().date()
HOY = pd.Timestamp.today().strftime('%Y-%m-%d')
LAYOUT_GRAFICOS = dict(font=dict(family="Montserrat, sans-serif"), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

def aplicar_estilo_estado(val):
    color_fondo = COLOR_MAP_ESTADOS.get(val, '#ffffff')
    color_texto = '#0f172a' if color_fondo in ['#cbd5e1', '#e2e8f0', '#ffffff'] else '#ffffff'
    return f'background-color: {color_fondo}; color: {color_texto}; font-weight: 600; text-align: center;'

def aplicar_negrita_proyecto(val): return 'font-weight: 800; color: #0f172a;'

def formatear_fecha_corta(fecha_str):
    try:
        fecha_obj = pd.to_datetime(fecha_str)
        meses = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]
        return f"{fecha_obj.day} {meses[fecha_obj.month - 1]} {fecha_obj.year}"
    except: return fecha_str

# ==========================================
# FUNCIONES BASE DE DATOS Y FORMATO
# ==========================================
def normalizar_texto(texto):
    if not texto: return ""
    return ''.join(c for c in unicodedata.normalize('NFD', str(texto).lower().strip()) if unicodedata.category(c) != 'Mn')

def formatear_prioridad(val):
    if val == '1': return '🔴 1'
    elif val == '2': return '🟠 2'
    elif val == '3': return '🟡 3'
    elif val == '-': return '⚪ -'
    return f'🔵 {val}'

@st.cache_data(ttl=600)
def obtener_datos_proyectos(api_key, board_id):
    if len(api_key) < 50: return None 
    url = "https://api.monday.com/v2"
    headers = {"Authorization": api_key, "API-Version": "2023-10"}
    query = f'{{ boards(ids: [{board_id}]) {{ items_page(limit: 100) {{ items {{ name group {{ title }} column_values {{ type text value column {{ title }} }} subitems {{ name column_values {{ type text value column {{ title }} }} }} }} }} }} }}'
    
    try:
        respuesta = requests.post(url=url, json={'query': query}, headers=headers, timeout=15)
        json_data = respuesta.json()
        if 'data' not in json_data: return None
            
        items = json_data['data']['boards'][0]['items_page']['items']
        filas = []
        
        def mapear_columnas(column_values):
            datos = {'OWNER': '-', 'ESTADO': 'No iniciado', 'PRIORIDAD': '-', 'FECHA INICIO': '-', 'FECHA TERMINO': '-', 'FECHA COMPROMISO': '-', 'STAKEHOLDER': '-'}
            for col in column_values:
                titulo = normalizar_texto(col.get('column', {}).get('title', '') if col.get('column') else "")
                texto = str(col.get('text') or "").strip()
                if not texto and col.get('value'):
                    try:
                        val_json = json.loads(col.get('value'))
                        if isinstance(val_json, dict) and 'date' in val_json: texto = val_json['date']
                    except: pass
                if not texto: continue
                
                if 'owner' in titulo or 'responsable' in titulo or col.get('type', '') == 'people': datos['OWNER'] = texto
                elif 'stakeholder' in titulo or 'sponsor' in titulo: datos['STAKEHOLDER'] = texto
                elif 'status' in titulo or 'estado' in titulo or 'etado' in titulo: datos['ESTADO'] = texto
                elif 'prioridad' in titulo: datos['PRIORIDAD'] = texto
                elif 'inicio' in titulo: datos['FECHA INICIO'] = texto
                elif 'compromiso' in titulo: datos['FECHA COMPROMISO'] = texto
                elif 'termino' in titulo or 'término' in titulo or 'fin' in titulo: datos['FECHA TERMINO'] = texto
            return datos

        for item in items:
            area = item['group']['title'] if item.get('group') else 'Sin Área'
            if 'proyectos td' in area.strip().lower(): continue
            
            datos_padre = mapear_columnas(item.get('column_values', []))
            
            subitems_data = []
            if 'subitems' in item and item['subitems']:
                for subitem in item['subitems']:
                    datos_sub = mapear_columnas(subitem.get('column_values', []))
                    
                    # CORRECCIÓN: Se eliminó la regla que cambiaba el estado del padre automáticamente.
                    # Ahora el estado del padre refleja exactamente lo que dice Monday.com
                    
                    if datos_padre['PRIORIDAD'] == '-' and datos_sub['PRIORIDAD'] != '-': datos_padre['PRIORIDAD'] = datos_sub['PRIORIDAD']
                    
                    subitems_data.append({
                        'PROYECTO_PADRE': item['name'], 'ÁREA': area, 'TIPO': 'Subetapa', 'PROYECTO': subitem['name'],
                        'PRIORIDAD': datos_sub['PRIORIDAD'], 'ESTADO': datos_sub['ESTADO'], 
                        'FECHA INICIO': datos_sub['FECHA INICIO'], 'FECHA TERMINO': datos_sub['FECHA TERMINO'],
                        'FECHA COMPROMISO': datos_sub['FECHA COMPROMISO'], 'OWNER': datos_sub['OWNER'], 'STAKEHOLDER': datos_sub['STAKEHOLDER']
                    })

            filas.append({
                'PROYECTO_PADRE': item['name'], 'ÁREA': area, 'TIPO': 'Proyecto', 'PROYECTO': item['name'],
                'PRIORIDAD': datos_padre['PRIORIDAD'], 'ESTADO': datos_padre['ESTADO'], 
                'FECHA INICIO': datos_padre['FECHA INICIO'], 'FECHA TERMINO': datos_padre['FECHA TERMINO'],
                'FECHA COMPROMISO': datos_padre['FECHA COMPROMISO'], 'OWNER': datos_padre['OWNER'], 'STAKEHOLDER': datos_padre['STAKEHOLDER']
            })
            filas.extend(subitems_data)
        
        df = pd.DataFrame(filas)
        df['PRIORIDAD'] = df['PRIORIDAD'].apply(formatear_prioridad)
        return df
    except Exception as e:
        return None

# ==========================================
# CABECERA VISUAL
# ==========================================
col_logo, col_titulo, col_vacia = st.columns([1.5, 7, 1.5], vertical_alignment="center")
with col_logo:
    try: st.image("IMEGA_VENTUS.webp", use_container_width=True)
    except: pass
with col_titulo:
    st.markdown("<h1>DASHBOARD DIRECTIVO TI</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Seguimiento Estratégico y Control de Portafolio</div>", unsafe_allow_html=True)
st.markdown("<div class='branded-divider'></div>", unsafe_allow_html=True)

# ==========================================
# OBTENCIÓN Y PREPARACIÓN DE DATOS
# ==========================================
df_proyectos = obtener_datos_proyectos(MONDAY_API_KEY, ID_TABLERO_PROYECTOS)

if df_proyectos is None or df_proyectos.empty:
    df_proyectos = pd.DataFrame({
        'PROYECTO_PADRE': ['Logística Avanzada', 'Migración App', 'Integración B2B'],
        'ÁREA': ['Supply Chain', 'Ecommerce', 'Comercial'],
        'TIPO': ['Proyecto', 'Proyecto', 'Proyecto'],
        'PROYECTO': ['Logística Avanzada', 'Migración App', 'Integración B2B'],
        'PRIORIDAD': ['🔴 1', '🟠 2', '🔴 1'],
        'ESTADO': ['En desarrollo', 'Análisis', 'En curso'],
        'FECHA INICIO': ['2026-06-01', '2026-07-01', '2026-01-15'],
        'FECHA TERMINO': ['2026-09-30', '2026-10-30', '2026-07-20'],
        'FECHA COMPROMISO': ['-', '-', '-'],
        'OWNER': ['MQ', 'JF', 'BC'],
        'STAKEHOLDER': ['Gerencia Op', 'Directorio', 'Gerencia Ventas']
    })

df_proyectos['PRIO_NUM'] = df_proyectos['PRIORIDAD'].apply(lambda x: 1 if '1' in x else (2 if '2' in x else (3 if '3' in x else 999)))
df_padres = df_proyectos[df_proyectos['TIPO'] == 'Proyecto'].copy()

# ==========================================
# KPIs GLOBALES SUPERIORES 
# ==========================================
cant_activos = len(df_padres)
cant_finalizados = len(df_padres[df_padres['ESTADO'].isin(['Cerrado', 'Completado'])])
cant_desarrollo = len(df_padres[df_padres['ESTADO'].isin(['En desarrollo', 'En curso', 'En pruebas'])])

html_kpis_top = f"""
<div class="top-kpi-container">
    <div class="top-kpi-card" style="border-bottom: 5px solid #0ea5e9;">
        <div class="top-kpi-icon" style="background-color: #0ea5e9;">📁</div>
        <div class="top-kpi-details">
            <div class="top-kpi-title">PROYECTOS ACTIVOS</div>
            <div class="top-kpi-value">{cant_activos}</div>
        </div>
    </div>
    <div class="top-kpi-card" style="border-bottom: 5px solid #10b981;">
        <div class="top-kpi-icon" style="background-color: #10b981;">✅</div>
        <div class="top-kpi-details">
            <div class="top-kpi-title">PROYECTOS FINALIZADOS</div>
            <div class="top-kpi-value">{cant_finalizados}</div>
        </div>
    </div>
    <div class="top-kpi-card" style="border-bottom: 5px solid #f59e0b;">
        <div class="top-kpi-icon" style="background-color: #f59e0b;">⚙️</div>
        <div class="top-kpi-details">
            <div class="top-kpi-title">EN DESARROLLO / PRUEBAS</div>
            <div class="top-kpi-value">{cant_desarrollo}</div>
        </div>
    </div>
</div>
"""
st.markdown(html_kpis_top, unsafe_allow_html=True)

# ==========================================
# 1. GRÁFICOS PRINCIPALES
# ==========================================
st.markdown("<div class='section-title'>Indicadores Generales del Portafolio</div>", unsafe_allow_html=True)
f_area_graf = st.multiselect("🏢 Filtrar Gráficos por Área (Vacío = Todas):", options=sorted(df_padres['ÁREA'].unique()))
df_graficos = df_padres[df_padres['ÁREA'].isin(f_area_graf)] if f_area_graf else df_padres.copy()

col_graf1, col_graf2, col_graf3, col_graf4 = st.columns(4)
with col_graf1:
    st.markdown("**Distribución por Área**")
    conteo_areas = df_graficos['ÁREA'].value_counts().reset_index()
    if not conteo_areas.empty:
        fig_areas = px.pie(conteo_areas, values='count', names='ÁREA', hole=0.6, color='ÁREA', color_discrete_map=COLOR_MAP_AREAS)
        fig_areas.update_traces(texttemplate='<b>%{label}</b><br>%{percent:.0%} (%{value})', textposition='inside', showlegend=False)
        fig_areas.update_layout(**LAYOUT_GRAFICOS, margin=dict(t=20, b=20, l=0, r=0), height=320)
        st.plotly_chart(fig_areas, use_container_width=True)

with col_graf2:
    st.markdown("**Estado General**")
    conteo_estados = df_graficos['ESTADO'].value_counts().reset_index()
    if not conteo_estados.empty:
        fig_estados = px.pie(conteo_estados, values='count', names='ESTADO', hole=0.6, color='ESTADO', color_discrete_map=COLOR_MAP_ESTADOS)
        fig_estados.update_traces(texttemplate='<b>%{percent:.0%}</b><br>(%{value})', textposition='inside')
        fig_estados.update_layout(**LAYOUT_GRAFICOS, margin=dict(t=20, b=20, l=0, r=0), height=320, showlegend=True, legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig_estados, use_container_width=True)

with col_graf3:
    st.markdown("**Criticidad (Prioridad)**")
    conteo_prio = df_graficos['PRIORIDAD'].value_counts().reset_index()
    if not conteo_prio.empty:
        fig_prio = px.pie(conteo_prio, values='count', names='PRIORIDAD', hole=0.6, color='PRIORIDAD', color_discrete_map=COLOR_MAP_PRIORIDADES)
        fig_prio.update_traces(texttemplate='<b>%{label}</b><br>%{percent:.0%} (%{value})', textposition='inside', showlegend=False)
        fig_prio.update_layout(**LAYOUT_GRAFICOS, margin=dict(t=20, b=20, l=0, r=0), height=320)
        st.plotly_chart(fig_prio, use_container_width=True)

with col_graf4:
    st.markdown("**Carga por Responsable**")
    df_workload = df_graficos[~df_graficos['OWNER'].isin(['-', 'Sin asignar', ''])].copy()
    if not df_workload.empty:
        workload_grp = df_workload.groupby(['OWNER', 'PRIORIDAD']).size().reset_index(name='count')
        orden_owners = workload_grp.groupby('OWNER')['count'].sum().sort_values().index
        fig_workload = px.bar(workload_grp, x='count', y='OWNER', color='PRIORIDAD', orientation='h', text_auto=True, color_discrete_map=COLOR_MAP_PRIORIDADES, category_orders={"PRIORIDAD": ["🔴 1", "🟠 2", "🟡 3", "⚪ -"]})
        fig_workload.update_layout(**LAYOUT_GRAFICOS, margin=dict(t=20, b=20, l=0, r=0), height=320, xaxis_title="", yaxis_title="", barmode='stack', xaxis=dict(showgrid=True, gridcolor='#e2e8f0'), legend=dict(orientation="h", y=-0.1, title=""))
        fig_workload.update_yaxes(categoryorder='array', categoryarray=orden_owners)
        st.plotly_chart(fig_workload, use_container_width=True)

# ==========================================
# 2. DIAGRAMA DE GANTT (CON CASCADA DE FECHAS)
# ==========================================
st.markdown("<div class='section-title'>Cronograma Estratégico (Gantt)</div>", unsafe_allow_html=True)

col_g1, col_g2 = st.columns(2)
f_area_gantt = col_g1.multiselect("🏢 Filtrar Gantt por Área (Vacío = Todas):", options=sorted(df_padres['ÁREA'].unique()), key='gantt_area')
f_prio_gantt = col_g2.multiselect("🚨 Filtrar Gantt por Prioridad (Vacío = Todas):", options=sorted([p for p in df_padres['PRIORIDAD'].unique() if p != '⚪ -']), key='gantt_prio')

df_gantt = df_padres.copy()

df_gantt['INICIO_CALC'] = pd.to_datetime(df_gantt['FECHA INICIO'], errors='coerce').fillna(pd.to_datetime(df_gantt['FECHA COMPROMISO'], errors='coerce'))
df_gantt['TERMINO_CALC'] = pd.to_datetime(df_gantt['FECHA TERMINO'], errors='coerce').fillna(pd.to_datetime(df_gantt['FECHA COMPROMISO'], errors='coerce')).fillna(df_gantt['INICIO_CALC'])
df_gantt['INICIO_CALC'] = df_gantt['INICIO_CALC'].fillna(df_gantt['TERMINO_CALC'])

if f_area_gantt: df_gantt = df_gantt[df_gantt['ÁREA'].isin(f_area_gantt)]
if f_prio_gantt: df_gantt = df_gantt[df_gantt['PRIORIDAD'].isin(f_prio_gantt)]

df_gantt = df_gantt.dropna(subset=['INICIO_CALC', 'TERMINO_CALC'])

if not df_gantt.empty:
    df_gantt.loc[df_gantt['INICIO_CALC'] == df_gantt['TERMINO_CALC'], 'TERMINO_CALC'] += pd.Timedelta(days=1)
    
    df_gantt = df_gantt.sort_values(by=['PRIO_NUM', 'INICIO_CALC'])
    df_gantt['HOVER_TEXT'] = df_gantt['PROYECTO'] + " | Prio: " + df_gantt['PRIORIDAD'] + " | Owner: " + df_gantt['OWNER']
    
    fig_gantt = px.timeline(df_gantt, x_start="INICIO_CALC", x_end="TERMINO_CALC", y="PROYECTO", color="ESTADO", color_discrete_map=COLOR_MAP_ESTADOS, text="ESTADO", hover_name="HOVER_TEXT")
    fig_gantt.add_vline(x=HOY, line_width=2, line_dash="dash", line_color="#ef4444", annotation_text=" HOY ", annotation_position="top right", annotation_font_color="#ef4444")
    fig_gantt.update_yaxes(autorange="reversed") 
    fig_gantt.update_layout(**LAYOUT_GRAFICOS, margin=dict(t=15, b=0, l=0, r=0), height=max(250, len(df_gantt)*40), xaxis_title="")
    fig_gantt.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e2e8f0')
    st.plotly_chart(fig_gantt, use_container_width=True)
else:
    st.info("No hay proyectos con fechas asignadas (Inicio, Término o Compromiso) para los filtros seleccionados.")

# ==========================================
# 3. ZOOM POR PROYECTO 
# ==========================================
st.markdown("<div class='section-title'>Análisis de Profundidad por Proyecto</div>", unsafe_allow_html=True)

col_z1, col_z2 = st.columns([1, 2])
area_zoom_sel = col_z1.selectbox("1. Filtrar por Área:", options=['Todas'] + sorted(df_padres['ÁREA'].unique()))
if area_zoom_sel != 'Todas': lista_proyectos = sorted(df_padres[df_padres['ÁREA'] == area_zoom_sel]['PROYECTO'].unique())
else: lista_proyectos = sorted(df_padres['PROYECTO'].unique())
proyecto_seleccionado = col_z2.selectbox("2. Seleccione un proyecto matriz:", options=lista_proyectos)

if proyecto_seleccionado:
    df_zoom = df_proyectos[df_proyectos['PROYECTO_PADRE'] == proyecto_seleccionado]
    df_zoom_subetapas = df_zoom[df_zoom['TIPO'] == 'Subetapa'].copy()
    info_padre = df_zoom[df_zoom['TIPO'] == 'Proyecto'].iloc[0]
    
    pm = info_padre['OWNER'] if info_padre['OWNER'] != '-' else 'No Asignado'
    sponsor = info_padre['STAKEHOLDER'] if 'STAKEHOLDER' in info_padre and info_padre['STAKEHOLDER'] != '-' else 'Gerencia General'
    
    st.write("")
    html_superior = f"""<div class="info-bar-container"><div class="info-item"><div class="info-icon">💼</div><div><div class="info-text-label">PROYECTO</div><div class="info-text-val">{proyecto_seleccionado}</div></div></div><div class="info-divider"></div><div class="info-item"><div class="info-icon">📅</div><div><div class="info-text-label">FECHA DE CORTE</div><div class="info-text-val">{formatear_fecha_corta(HOY)}</div></div></div><div class="info-divider"></div><div class="info-item"><div class="info-icon">👥</div><div><div class="info-text-label">SPONSOR</div><div class="info-text-val">{sponsor}</div></div></div><div class="info-divider"></div><div class="info-item"><div class="info-icon">👤</div><div><div class="info-text-label">PROJECT MANAGER</div><div class="info-text-val">{pm}</div></div></div></div>"""
    st.markdown(html_superior, unsafe_allow_html=True)
    
    estado = info_padre['ESTADO']
    # Manejo dinámico de estados del padre
    if estado in ['Completado', 'Cerrado']:
        estado_icon, estado_bg, estado_text, estado_desc = '✅', '#10b981', 'COMPLETADO', 'El proyecto ha sido completado con éxito'
    elif estado in ['En curso', 'En desarrollo', 'En pruebas']:
        estado_icon, estado_bg, estado_text, estado_desc = '🔄', '#3b82f6', 'EN CONTROL', 'El proyecto avanza según lo planificado'
    elif estado in ['Sin iniciar', 'No iniciado']:
        estado_icon, estado_bg, estado_text, estado_desc = '⏳', '#cbd5e1', 'NO INICIADO', 'El proyecto aún no ha comenzado'
    else:
        estado_icon, estado_bg, estado_text, estado_desc = '⚠️', '#f59e0b', 'ATENCIÓN', 'Requiere revisión de estado o fechas'

    total_sub = len(df_zoom_subetapas)
    sub_completadas = len(df_zoom_subetapas[df_zoom_subetapas['ESTADO'].isin(['Completado', 'Cerrado'])])
    avance_pct = int((sub_completadas / total_sub) * 100) if total_sub > 0 else 0
    
    fecha_fin = info_padre['FECHA TERMINO']
    fecha_fin_fmt = formatear_fecha_corta(fecha_fin)
    try:
        parsed_date = pd.to_datetime(fecha_fin, errors='coerce')
        if pd.isna(parsed_date): en_riesgo, color_riesgo = "Sin fecha válida", "#94a3b8"
        else:
            en_riesgo = "En riesgo alto" if parsed_date.date() < HOY_FECHA else "En riesgo bajo"
            color_riesgo = "#ef4444" if "alto" in en_riesgo else "#10b981"
    except: en_riesgo, color_riesgo = "Sin fecha válida", "#94a3b8"

    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns([1, 1, 1, 1.8])
    
    with col_kpi1:
        html_kpi1 = f"""<div class="kpi-card-custom"><div class="kpi-title">ESTADO GENERAL</div><div class="icon-box-square" style="background-color: {estado_bg}; color: {'#0f172a' if estado_bg == '#cbd5e1' else 'white'};">{estado_icon}</div><div class="kpi-pill" style="background-color: {estado_bg}; color: {'#0f172a' if estado_bg == '#cbd5e1' else 'white'};">{estado_text}</div><div class="kpi-subtext">{estado_desc}</div></div>"""
        st.markdown(html_kpi1, unsafe_allow_html=True)

    with col_kpi2:
        html_kpi2 = f"""<div class="kpi-card-custom"><div class="kpi-title" style="margin-bottom:0;">% AVANCE</div><div class="flex-wrapper"><div class="single-chart"><svg viewBox="0 0 36 36" class="circular-chart green"><path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" /><path class="circle" stroke-dasharray="{avance_pct}, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" /><text x="18" y="20.35" class="percentage">{avance_pct}%</text></svg></div></div><div class="kpi-subtext" style="margin-top:-5px;">Tareas Completadas: {sub_completadas}/{total_sub}</div></div>"""
        st.markdown(html_kpi2, unsafe_allow_html=True)

    with col_kpi3:
        html_kpi3 = f"""<div class="kpi-card-custom"><div class="kpi-title">FECHA ESTIMADA DE SALIDA<br>(Go Live)</div><div class="icon-box-circle" style="background-color: #e0f2fe; color: #0ea5e9;">📅</div><div style="font-size: 1.4rem; font-weight: 800; color: #10b981; margin-bottom: 5px;">{fecha_fin_fmt}</div><div style="font-size: 0.9rem; font-weight: 700; color: {color_riesgo};">{en_riesgo}</div></div>"""
        st.markdown(html_kpi3, unsafe_allow_html=True)
        
    with col_kpi4:
        html_hitos = """<div class="milestone-container"><div class="kpi-title" style="text-align:left;">PRÓXIMOS HITOS (SUBETAPAS)</div>"""
        if not df_zoom_subetapas.empty:
            df_m = df_zoom_subetapas.copy()
            df_m['FECHA_ORDEN'] = pd.to_datetime(df_m['FECHA TERMINO'], errors='coerce').fillna(pd.to_datetime(df_m['FECHA COMPROMISO'], errors='coerce'))
            df_m = df_m.dropna(subset=['FECHA_ORDEN']).sort_values('FECHA_ORDEN')
            
            colores_hitos = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6']
            for i, row in df_m.head(4).iterrows():
                color = colores_hitos[i % 4]
                f_texto = formatear_fecha_corta(row['FECHA_ORDEN'].strftime('%Y-%m-%d'))
                html_hitos += f"""<div class="milestone-item"><div class="m-left"><div class="m-icon" style="background-color: {color};">📍</div><div><p class="m-title">{row['PROYECTO']}</p><p class="m-subtitle">Owner: {row['OWNER']} | Status: {row['ESTADO']}</p></div></div><div class="m-date" style="color: {color};">{f_texto}</div></div>"""
        else: html_hitos += """<p style='color:#64748b; font-size:0.9rem; text-align:center; margin-top:40px;'>No hay subetapas registradas para este proyecto.</p>"""
        html_hitos += """</div>"""
        st.markdown(html_hitos, unsafe_allow_html=True)

    # Carta Gantt y Tabla Detallada
    st.write("")
    if not df_zoom_subetapas.empty:
        col_zGantt, col_zTabla = st.columns([1.2, 1])
        with col_zGantt:
            st.markdown("**Cronograma Detallado de Entregables**")
            df_gantt_sub = df_zoom_subetapas.copy()
            df_gantt_sub['INICIO_CALC'] = pd.to_datetime(df_gantt_sub['FECHA INICIO'], errors='coerce').fillna(pd.to_datetime(df_gantt_sub['FECHA COMPROMISO'], errors='coerce'))
            df_gantt_sub['TERMINO_CALC'] = pd.to_datetime(df_gantt_sub['FECHA TERMINO'], errors='coerce').fillna(df_gantt_sub['INICIO_CALC'])
            
            padre_inicio = pd.to_datetime(info_padre['FECHA INICIO'], errors='coerce')
            padre_termino = pd.to_datetime(info_padre['FECHA TERMINO'], errors='coerce')
            df_gantt_sub['INICIO_CALC'] = df_gantt_sub['INICIO_CALC'].fillna(padre_inicio)
            df_gantt_sub['TERMINO_CALC'] = df_gantt_sub['TERMINO_CALC'].fillna(padre_termino).fillna(df_gantt_sub['INICIO_CALC'])
            df_gantt_sub.loc[df_gantt_sub['INICIO_CALC'] == df_gantt_sub['TERMINO_CALC'], 'TERMINO_CALC'] += pd.Timedelta(days=1)
            
            df_gantt_sub = df_gantt_sub.dropna(subset=['INICIO_CALC', 'TERMINO_CALC'])
            if not df_gantt_sub.empty:
                df_gantt_sub = df_gantt_sub.sort_values(by='INICIO_CALC')
                fig_sub = px.timeline(df_gantt_sub, x_start="INICIO_CALC", x_end="TERMINO_CALC", y="PROYECTO", color="ESTADO", color_discrete_map=COLOR_MAP_ESTADOS, text="ESTADO")
                fig_sub.add_vline(x=HOY, line_width=2, line_dash="dash", line_color="#ef4444")
                fig_sub.update_yaxes(autorange="reversed") 
                fig_sub.update_layout(**LAYOUT_GRAFICOS, margin=dict(t=0, b=0, l=0, r=0), height=max(200, len(df_gantt_sub)*40), showlegend=False)
                fig_sub.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e2e8f0')
                st.plotly_chart(fig_sub, use_container_width=True)

        with col_zTabla:
            st.markdown("**Desglose de Tareas**")
            df_zoom_mostrar = df_zoom_subetapas[['PROYECTO', 'ESTADO', 'OWNER', 'FECHA COMPROMISO', 'FECHA TERMINO']].copy()
            estilo_zoom = df_zoom_mostrar.style
            if hasattr(estilo_zoom, 'map'): 
                estilo_zoom = estilo_zoom.map(aplicar_estilo_estado, subset=['ESTADO'])
                estilo_zoom = estilo_zoom.map(aplicar_negrita_proyecto, subset=['PROYECTO'])
            else: 
                estilo_zoom = estilo_zoom.applymap(aplicar_estilo_estado, subset=['ESTADO'])
                estilo_zoom = estilo_zoom.applymap(aplicar_negrita_proyecto, subset=['PROYECTO'])
            st.dataframe(estilo_zoom, use_container_width=True, hide_index=True)

# ==========================================
# 4. TABLA DETALLADA (SOLO PROYECTOS)
# ==========================================
st.markdown("<div class='section-title'>Matriz Operativa de Proyectos Principales</div>", unsafe_allow_html=True)

col_f1, col_f2, col_f3, col_f4 = st.columns(4)
f_tb_area = col_f1.multiselect("🏢 Filtrar Área (Vacío = Todas)", sorted(df_padres['ÁREA'].unique()), key='tb_area')
f_tb_owner = col_f2.multiselect("👤 Filtrar Responsable (Vacío = Todos)", sorted([x for x in df_padres['OWNER'].unique() if x != '-']))
f_tb_estado = col_f3.multiselect("📌 Filtrar Estado (Vacío = Todos)", sorted(df_padres['ESTADO'].unique()))
f_tb_prio = col_f4.multiselect("🚨 Filtrar Prioridad (Vacío = Todas)", sorted([x for x in df_padres['PRIORIDAD'].unique() if x != '⚪ -']))

df_visual = df_padres.copy()
if f_tb_area: df_visual = df_visual[df_visual['ÁREA'].isin(f_tb_area)]
if f_tb_owner: df_visual = df_visual[df_visual['OWNER'].isin(f_tb_owner)]
if f_tb_estado: df_visual = df_visual[df_visual['ESTADO'].isin(f_tb_estado)]
if f_tb_prio: df_visual = df_visual[df_visual['PRIORIDAD'].isin(f_tb_prio)]

df_visual = df_visual.sort_values(by=['PRIO_NUM', 'PROYECTO'])
columnas_orden = ['PRIORIDAD', 'ÁREA', 'PROYECTO', 'ESTADO', 'FECHA INICIO', 'FECHA TERMINO', 'OWNER']
df_visual = df_visual[columnas_orden]

estilo_principal = df_visual.style
if hasattr(estilo_principal, 'map'): 
    estilo_principal = estilo_principal.map(aplicar_estilo_estado, subset=['ESTADO'])
    estilo_principal = estilo_principal.map(aplicar_negrita_proyecto, subset=['PROYECTO'])
else: 
    estilo_principal = estilo_principal.applymap(aplicar_estilo_estado, subset=['ESTADO'])
    estilo_principal = estilo_principal.applymap(aplicar_negrita_proyecto, subset=['PROYECTO'])

st.dataframe(
    estilo_principal, use_container_width=True, hide_index=True,
    column_config={
        "PRIORIDAD": st.column_config.TextColumn("Prio", width="small"),
        "ÁREA": st.column_config.TextColumn("Área", width="small"),
        "PROYECTO": st.column_config.TextColumn("Proyecto", width="large"),
        "ESTADO": st.column_config.TextColumn("Status", width="small"),
        "FECHA INICIO": st.column_config.TextColumn("F. Inicio", width="small"),
        "FECHA TERMINO": st.column_config.TextColumn("F. Término", width="small"),
        "OWNER": st.column_config.TextColumn("Responsable", width="small"),
    }
)
