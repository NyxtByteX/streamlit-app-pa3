import streamlit as st
import pandas as pd
import plotly.express as px
import urllib.parse

# --- 1. CONFIGURACIÓN DEL ENTORNO EMPRESARIAL ---
st.set_page_config(
    page_title="ChurnAI Horizon - Executive Analytics", 
    page_icon="🔮", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Estilo CSS Avanzado (Corrección de Alineación, Centrado y Simetría Cohesiva)
st.markdown("""
    <style>
        /* Fondo general oscuro y tipografía limpia */
        .reportview-container, .main { background: #0B0E14; }
        body { color: #E6EDF3; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
        
        /* Títulos principales */
        h1, h2, h3 { color: #00CED1 !important; font-weight: 600 !important; }
        
        /* Contenedores de Tarjetas KPI (Estilo Geckoboard) */
        .kpi-container {
            background-color: #161B22;
            border: 1px solid #30363D;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            margin-bottom: 15px;
        }
        .kpi-title { font-size: 0.85rem; color: #8B949E; text-transform: uppercase; letter-spacing: 1px; font-weight: bold; }
        .kpi-value { font-size: 2.2rem; color: #00CED1; font-weight: 700; margin: 10px 0 5px 0; }
        .kpi-sub { font-size: 0.8rem; color: #58A6FF; }

        /* Banner de Estrategia Central */
        .strategy-banner {
            background-color: #12161F; 
            padding: 22px; 
            border-radius: 10px; 
            border-left: 5px solid #FF1493; 
            margin-bottom: 30px;
            border-top: 1px solid #30363D;
            border-right: 1px solid #30363D;
            border-bottom: 1px solid #30363D;
        }

        /* Contenedor Flexbox para forzar que el gráfico y el texto compartan el mismo centro vertical */
        .grid-align-container {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            min-height: 380px;
        }
        
        /* Glosarios con tamaño controlado y padding estandarizado */
        .chart-glossary {
            background-color: #161B22;
            padding: 24px;
            border-radius: 8px;
            border: 1px solid #30363D;
            font-size: 0.9rem;
            color: #C9D1D9;
            line-height: 1.6;
            width: 100%;
            box-sizing: border-box;
        }

        /* Tarjetas de Papers (Top Papers) */
        .paper-card {
            background-color: #161B22;
            padding: 18px;
            border-radius: 8px;
            border-top: 4px solid #FF1493;
            margin-bottom: 12px;
            border-left: 1px solid #30363D;
            border-right: 1px solid #30363D;
            border-bottom: 1px solid #30363D;
        }

        /* Contenedor de Detalle de Fila Seleccionada */
        .detail-box {
            background-color: #161B22;
            border: 1px solid #00CED1;
            padding: 20px;
            border-radius: 8px;
            margin-top: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE PROCESAMIENTO DE DATOS ---
def process_data(file_source):
    df = pd.read_csv(file_source)
    df['Title'] = df['Title'].fillna('Untitled Paper')
    df['Source title'] = df['Source title'].fillna('Unknown Source')
    df['Cited by'] = df['Cited by'].fillna(0).astype(int)
    df['Year'] = df['Year'].fillna(2025).astype(int)
    df['Abstract'] = df['Abstract'].fillna('No abstract available.')
    df['Abstract_Clean'] = df['Abstract'].str.lower()
    df['Document Type'] = df['Document Type'].fillna('Article')
    df['Authors'] = df['Authors'].fillna('Unknown')
    
    # Generar URL dinámica de búsqueda en Google Scholar usando el título del artículo
    df['Link'] = df['Title'].apply(lambda x: f"https://scholar.google.com/scholar?q={urllib.parse.quote(x)}")
    return df

def main():
    # --- 1. DECLARACIÓN DE FUENTES DE DATOS ---
    nombre_archivo_base = "scopus_PA3.csv"
    archivo_subido = None
    busqueda = ""  # Inicialización preventiva para evitar el NameError

    # --- 2. BARRA LATERAL (Panel de Control y Entrada Dinámica) ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2103/2103832.png", width=50)
        st.title("Auditoría de Modelos")
        
        # Carga dinámica en el lateral para cumplir con el Criterio 3
        st.markdown("### 📥 Gestión de Datos")
        archivo_subido = st.file_uploader(
            "Opcional: Sube un archivo Scopus CSV externo:", 
            type=["csv"],
            help="Actualiza el ecosistema predictivo cargando un archivo local dinámicamente."
        )
        st.markdown("---")
        
        st.markdown("Configura el alcance técnico y el nivel de validación comercial para el ecosistema predictivo.")
        
        categoria_ia = st.selectbox(
            "⚙️ Arquitectura del Modelo de IA:",
            options=["Todos los Modelos", "Redes Neuronales / Deep Learning", "Árboles de Decisión / XGBoost", "Regresión Logística / Scoring Tradicional"]
        )
        
        if categoria_ia == "Redes Neuronales / Deep Learning":
            busqueda = "neural|deep learning"
        elif categoria_ia == "Árboles de Decisión / XGBoost":
            busqueda = "tree|forest|xgboost|boosting"
        elif categoria_ia == "Regresión Logística / Scoring Tradicional":
            busqueda = "logistic|regression|statistical"

    # --- 3. MOTOR DE ASIGNACIÓN DEL DATAFRAME ---
    df = None
    if archivo_subido is not None:
        try:
            df = process_data(archivo_subido)
        except Exception as e:
            st.error(f"🚨 Error al procesar el archivo subido: {e}")
            st.stop()
    else:
        try:
            df = process_data(nombre_archivo_base)
        except Exception:
            st.error(f"🚨 Error crítico: No se encontró el archivo base '{nombre_archivo_base}' en la raíz del repositorio.")
            st.stop()

    # --- 4. CONTINUACIÓN DE LA BARRA LATERAL (Sliders que dependen del DataFrame) ---
    with st.sidebar:
        max_citas_posibles = int(df['Cited by'].max()) if len(df) > 0 else 100
        min_citas = st.slider(
            "🛡️ Grado de Respaldo e Impacto en la Industria (Citas Mínimas):", 
            min_value=0, 
            max_value=max_citas_posibles, 
            value=0,
            help="Filtra las tecnologías según su nivel de réplica y éxito validado en la comunidad financiera global."
        )
        st.markdown("---")
     # --- SECCIÓN DE AUTORES Y ENLACES (INTEGRADA EN LA BARRA LATERAL) ---
        st.markdown("---")
        with st.expander("👥 Autores y Repositorio Académico"):
            st.markdown("""
                <div style='background-color: #0B0E14; padding: 12px; border-radius: 6px; border: 1px solid #30363D; margin-bottom: 8px;'>
                    <p style='margin: 0; font-size: 0.9rem; color: #00CED1; font-weight: bold;'>Peter Cajusol</p>
                </div>    
                <div style='background-color: #0B0E14; padding: 12px; border-radius: 6px; border: 1px solid #30363D; margin-bottom: 15px;'>
                    <p style='margin: 0; font-size: 0.9rem; color: #FF1493; font-weight: bold;'>Victoria De la Vega</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Enlace al Google Colab configurado como un link nativo de Streamlit
            st.link_button(
                "🔗 Ver Cuaderno Google Colab", 
                "https://colab.research.google.com/drive/1GUhTOVQ1noMUZL3y-jC0349brgKmFh4N?usp=sharing",
                use_container_width=True,
                help="Accede al entorno de desarrollo y procesamiento inicial en Google Colab."
            )
        st.caption("⚡ Powered by ChurnAI Engine v3.5 • Mercado Peruano 2026")

    # --- 5. FILTRADO DINÁMICO DE DATOS ---
    df_filtrado = df[df['Cited by'] >= min_citas].copy()
    if busqueda:
        df_filtrado = df_filtrado[df_filtrado['Abstract_Clean'].str.contains(busqueda.lower()) | 
                                  df_filtrado['Title'].str.lower().str.contains(busqueda.lower())]

    # --- 6. ENCABEZADO CORPORATIVO CENTRAL ---
    st.title("🔮 ChurnAI Horizon Dashboard")
    st.markdown("<p style='color:#8B949E; font-size:1.1rem; margin-top:-10px;'>Plataforma Ejecutiva de Inteligencia Analítica Aplicada al Riesgo Financiero</p>", unsafe_allow_html=True)
    
    if archivo_subido is not None:
        st.success("✅ Dataset externo cargado e integrado dinámicamente.")
    else:
        st.info(f"ℹ️ Datos activos: Consumiendo de manera directa desde el repositorio (`{nombre_archivo_base}`).")
    
    # --- 7. CÁLCULO DE PESOS PARA EL MOTOR CONECTOR ---
    menciones_trans = df_filtrado['Abstract_Clean'].str.contains('transaction|behavio|digital|channel').sum()
    menciones_score = df_filtrado['Abstract_Clean'].str.contains('credit score|credit history|credit|risk|sbs').sum()
    menciones_demo  = df_filtrado['Abstract_Clean'].str.contains('demograph|age|gender|income|status').sum()
    
    total_menciones = menciones_trans + menciones_score + menciones_demo
    peso_trans, peso_score, peso_demo = (menciones_trans / total_menciones, menciones_score / total_menciones, menciones_demo / total_menciones) if total_menciones > 0 else (0.50, 0.30, 0.20)

    # --- ESTRUCTURACIÓN DE PESTAÑAS ---
    tab1, tab2, tab3 = st.tabs([
        "📊 Dashboard de Control e Impacto", 
        "🔮 Simulador Financiero Conectado (Bancos Perú)", 
        "📚 Centro de Datos e Insights"
    ])

    # =========================================================================
    # PESTAÑA 1: DASHBOARD DE CONTROL CON MITADES PERFECTAS Y CENTRADO COMPLETO
    # =========================================================================
    with tab1:
        # 1. FILA DE TARJETAS KPI SUPERIORES
        col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
        
        with col_kpi1:
            st.markdown(f"""<div class="kpi-container"><div class="kpi-title">Volumen de Literatura</div><div class="kpi-value">{len(df_filtrado)}</div><div class="kpi-sub">Estudios Científicos Filtrados</div></div>""", unsafe_allow_html=True)
        with col_kpi2:
            st.markdown(f"""<div class="kpi-container"><div class="kpi-title">Impacto Global</div><div class="kpi-value">{df_filtrado['Cited by'].sum():,}</div><div class="kpi-sub">Citas Totales en Scopus</div></div>""", unsafe_allow_html=True)
        with col_kpi3:
            max_citas = df_filtrado['Cited by'].max() if len(df_filtrado) > 0 else 0
            st.markdown(f"""<div class="kpi-container"><div class="kpi-title">Récord de Relevancia</div><div class="kpi-value">{max_citas}</div><div class="kpi-sub">Máximo de Citas en un Paper</div></div>""", unsafe_allow_html=True)
        with col_kpi4:
            promedio_citas = df_filtrado['Cited by'].mean() if len(df_filtrado) > 0 else 0
            st.markdown(f"""<div class="kpi-container"><div class="kpi-title">Densidad Científica</div><div class="kpi-value">{promedio_citas:.1f}</div><div class="kpi-sub">Promedio de Citas por Registro</div></div>""", unsafe_allow_html=True)

  # 2. SECCIÓN ESTRATÉGICA CENTRAL 
        st.markdown(f"""
        <div class="strategy-banner">
            <h4 style='color: #FF1493; margin-top:0; margin-bottom:8px;'>📌 PREGUNTA DE INVESTIGACIÓN Y ENFOQUE ESTRATÉGICO</h4>
            <p style='color: #E6EDF3; font-size: 1.05rem; line-height: 1.5; margin:0;'>
                <b>¿Cómo optimiza el uso de machine learning la predicción de la fuga de clientes en el sector bancario?</b><br>
                La optimización se ejecuta mediante el análisis dinámico de comportamiento. Al interconectar la Big Data de Scopus con disparadores transaccionales locales (Yape, Plin, CTS y variaciones del Score SBS), la IA automatiza la toma de decisiones críticas para congelar la fuga de capitales antes de que el cliente abandone la entidad.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Contenedor de Palabras Clave en formato de Tarjetas Visuales (Scannable)
        st.markdown("<h5 style='color: #00CED1; margin-top:0; margin-bottom:15px;'>🔑 Estructura de Búsqueda Académica en Scopus (4 Keywords):</h5>", unsafe_allow_html=True)
        
        col_key1, col_key2, col_key3, col_key4 = st.columns(4)
        with col_key1:
            st.markdown("""<div style='background-color: #161B22; border: 1px solid #30363D; padding: 15px; border-radius: 8px; text-align: center; min-height: 110px;'>
                <div style='font-size: 1.1rem; color: #FF1493; font-weight: bold; margin-bottom: 5px;'>\"Machine learning\"</div>
                <div style='font-size: 0.8rem; color: #8B949E;'>Núcleo tecnológico y algoritmos predictivos.</div>
            </div>""", unsafe_allow_html=True)
        with col_key2:
            st.markdown("""<div style='background-color: #161B22; border: 1px solid #30363D; padding: 15px; border-radius: 8px; text-align: center; min-height: 110px;'>
                <div style='font-size: 1.1rem; color: #FF1493; font-weight: bold; margin-bottom: 5px;'>\"Churn prediction\"</div>
                <div style='font-size: 0.8rem; color: #8B949E;'>Objetivo matemático y fenómeno a resolver.</div>
            </div>""", unsafe_allow_html=True)
        with col_key3:
            st.markdown("""<div style='background-color: #161B22; border: 1px solid #30363D; padding: 15px; border-radius: 8px; text-align: center; min-height: 110px;'>
                <div style='font-size: 1.1rem; color: #FF1493; font-weight: bold; margin-bottom: 5px;'>\"Banking\"</div>
                <div style='font-size: 0.8rem; color: #8B949E;'>Sector de la industria delimitado.</div>
            </div>""", unsafe_allow_html=True)
        with col_key4:
            st.markdown("""<div style='background-color: #161B22; border: 1px solid #30363D; padding: 15px; border-radius: 8px; text-align: center; min-height: 110px;'>
                <div style='font-size: 1.1rem; color: #FF1493; font-weight: bold; margin-bottom: 5px;'>\"Customer retention\"</div>
                <div style='font-size: 0.8rem; color: #8B949E;'>Finalidad operativa y mitigación de riesgo.</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("""
            <p style='color: #8B949E; font-size: 0.85rem; margin-top: 15px; margin-bottom: 25px; font-family: monospace;'>
                <b>Sintaxis lógica aplicada:</b> TITLE-ABS-KEY("Machine learning" AND "Churn prediction" AND "Banking" AND "Customer retention")
            </p>
        """, unsafe_allow_html=True)
        
        # --- BLOQUE 1: DENSIDAD DE CONCEPTOS ---
        col_g1_izq, col_g1_der = st.columns([1, 1], gap="medium")
        
        with col_g1_izq:
            conceptos = ['churn', 'risk', 'accuracy', 'credit', 'transaction', 'banking', 'neural']
            conteos = [df_filtrado['Abstract_Clean'].str.contains(c).sum() for c in conceptos]
            df_conceptos = pd.DataFrame({'Concepto': [c.upper() for c in conceptos], 'Frecuencia': conteos}).sort_values(by='Frecuencia', ascending=True)
            
            fig_words = px.bar(df_conceptos, x='Frecuencia', y='Concepto', orientation='h', template='plotly_dark', color='Frecuencia', color_continuous_scale=['#FF1493', "#00CED1"])
            fig_words.update_layout(
                title={'text': "<b>Densidad de Conceptos de Riesgo en la Literatura</b>", 'y':0.95, 'x':0.0, 'xanchor': 'left', 'yanchor': 'top', 'font': {'size': 16, 'color': '#00CED1'}},
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False, margin=dict(l=10, r=10, t=60, b=10), height=380
            )
            st.plotly_chart(fig_words, use_container_width=True)
            
        with col_g1_der:
            st.markdown("""
            <div class="grid-align-container">
                <div class="chart-glossary">
                    <h5 style="color: #00CED1 !important; margin-top: 0; margin-bottom: 10px; font-size:1.1rem;">💡 Glosario de Conceptos de Riesgo</h5>
                    <p style="margin-bottom: 8px;">Este gráfico rastrea la frecuencia con la que los modelos predictivos asocian ciertas palabras dentro de los resúmenes académicos:</p>
                    • <b>CHURN / BANKING:</b> Volumen de investigaciones enfocadas estrictamente en la pérdida y retención de clientes en banca.<br>
                    • <b>RISK / CREDIT:</b> Estudios dirigidos a mitigar el peligro crediticio o de impago financiero.<br>
                    • <b>ACCURACY / NEURAL:</b> Documentos técnicos que priorizan la precisión algorítmica mediante redes neuronales complejas.
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # --- BLOQUE 2: PREDOMINANCIA DE MÉTRICAS ---
        col_g2_izq, col_g2_der = st.columns([1, 1], gap="medium")
        
        with col_g2_izq:
            metricas_data = [
                {'Métrica': 'Accuracy', 'Papers': df_filtrado['Abstract_Clean'].str.contains('accuracy').sum()},
                {'Métrica': 'F1-Score', 'Papers': df_filtrado['Abstract_Clean'].str.contains('f1|f-measure').sum()},
                {'Métrica': 'AUC-ROC', 'Papers': df_filtrado['Abstract_Clean'].str.contains('auc|roc').sum()}
            ]
            df_m = pd.DataFrame(metricas_data).sort_values(by="Papers", ascending=True)
            fig_bar = px.bar(df_m, x="Papers", y="Métrica", orientation="h", template="plotly_dark", color="Papers", color_continuous_scale=["#FF1493", "#00CED1"])
            fig_bar.update_layout(
                title={'text': "<b>Predominancia de Métricas de Evaluación</b>", 'y':0.95, 'x':0.0, 'xanchor': 'left', 'yanchor': 'top', 'font': {'size': 16, 'color': '#00CED1'}},
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False, margin=dict(l=10, r=10, t=60, b=10), height=380
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with col_g2_der:
            st.markdown("""
            <div class="grid-align-container">
                <div class="chart-glossary">
                    <h5 style="color: #FF1493 !important; margin-top: 0; margin-bottom: 10px; font-size:1.1rem;">🎯 Guía de Métricas de Machine Learning</h5>
                    <p style="margin-bottom: 8px;">Define qué criterio técnico se utilizó en la literatura para validar que el modelo realmente funciona:</p>
                    • <b>Accuracy (Exactitud):</b> Porcentaje total de predicciones correctas. Puede ser engañoso si los datos de fuga están muy desbalanceados.<br>
                    • <b>F1-Score:</b> Balance armónico entre precisión y exhaustividad. Es la métrica reina cuando hay pocos clientes que fugan frente a muchos que se quedan.<br>
                    • <b>AUC-ROC:</b> Mide la capacidad del modelo para separar correctamente a un cliente leal de uno en riesgo latente de abandono.
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # --- BLOQUE 3: ORIGEN DE VALIDACIÓN (DONA) - CON CORRECCIÓN DEL TEXTO FLOTANTE ---
        col_g3_izq, col_g3_der = st.columns([1, 1], gap="medium")
        
        with col_g3_izq:
            if len(df_filtrado) > 0:
                fig_pie = px.pie(
                    df_filtrado, 
                    names='Document Type', 
                    template='plotly_dark', 
                    hole=0.4, 
                    color_discrete_sequence=["#00CED1", "#FF1493", "#FFFF00", "#FF4500"]
                )
                
                # CORRECCIÓN DE TEXTO FLOTANTE AQUÍ
                fig_pie.update_traces(
                    textposition='inside', 
                    textinfo='percent',    
                    insidetextorientation='horizontal'
                )
                
                fig_pie.update_layout(
                    title={'text': "<b>Origen de Validación Académica (Distribución de Literatura)</b>", 'y':0.95, 'x':0.0, 'xanchor': 'left', 'yanchor': 'top', 'font': {'size': 16, 'color': '#00CED1'}},
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=60, b=50), height=380, legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.caption("Sin datos para segmentar.")
                
        with col_g3_der:
            st.markdown("""
            <div class="grid-align-container">
                <div class="chart-glossary">
                    <h5 style="color: #FFFF00 !important; margin-top: 0; margin-bottom: 10px; font-size:1.1rem;">📊 Tipos de Documentación Científica</h5>
                    <p style="margin-bottom: 8px;">Clasificación de los documentos según la rigurosidad e intención metodológica del estudio:</p>
                    • <b>Article (Artículo de Revista):</b> Investigaciones maduras, revisadas por pares y con validaciones matemáticas extensas. Ideal para sustentar metodologías robustas.<br>
                    • <b>Conference Paper (Actas de Congresos):</b> Tecnologías de última generación expuestas rápidamente en la industria tecnológica.<br>
                    • <b>Book / Book Chapter:</b> Compendios teóricos globales útiles para estructurar la gobernanza de datos a nivel corporativo.
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        # --- BLOQUE 4: GRÁFICA DE TENDENCIAS CONTINUAS ---
        if len(df_filtrado) > 0:
            col_g4_izq, col_g4_der = st.columns([1, 1], gap="medium")
            
            with col_g4_izq:
                text_comb = df_filtrado['Abstract_Clean'] + " " + df_filtrado['Title'].str.lower()
                df_trends = pd.DataFrame({
                    'Año': df_filtrado['Year'],
                    '📱 Transacciones e Interactividad': text_comb.str.contains('transaction|behavio|digital|channel|yape|plin').astype(int),
                    '💳 Historial Crediticio (SBS)': text_comb.str.contains('credit|score|history|risk|sbs|infocorp').astype(int),
                    '👤 Datos Demográficos y Perfil': text_comb.str.contains('demograph|age|gender|income|status|sueldo').astype(int)
                })
                df_trends_grouped = df_trends.groupby('Año').sum().reset_index()
                df_melted = df_trends_grouped.melt(id_vars='Año', var_name='Dimensión Crítica', value_name='Cantidad de Investigaciones')
                
                fig_line = px.line(
                    df_melted, x="Año", y="Cantidad de Investigaciones", color="Dimensión Crítica",
                    color_discrete_map={"📱 Transacciones e Interactividad": "#00CED1", "💳 Historial Crediticio (SBS)": "#FF1493", "👤 Datos Demográficos y Perfil": "#FFFF00"},
                    template="plotly_dark", markers=True, labels={"Cantidad de Investigaciones": "Número de Papers", "Año": "Año"}
                )
                fig_line.update_layout(
                    title={'text': "<b>📈 Evolución Histórica de Dimensiones Críticas de Entrada</b>", 'y':0.95, 'x':0.0, 'xanchor': 'left', 'yanchor': 'top', 'font': {'size': 16, 'color': '#00CED1'}},
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=60, b=50), height=380, legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig_line, use_container_width=True)
                
            with col_g4_der:
                st.markdown("""
                <div class="grid-align-container">
                    <div class="chart-glossary">
                        <h5 style="color: #00CED1 !important; margin-top: 0; margin-bottom: 10px; font-size:1.1rem;">📉 Análisis de Variables Críticas (Inputs)</h5>
                        <p style="margin-bottom: 8px;">Este análisis predictivo de líneas de tendencia evalúa el nivel de atención que la ciencia otorga a los pilares de comportamiento financiero:</p>
                        • <b>📱 Transacciones:</b> Mide la frecuencia de uso en ecosistemas móviles (Yape/Plin). Es el indicador más rápido para detectar desinterés.<br>
                        • <b>💳 Historial Crediticio (SBS):</b> Variaciones en el score de sobreendeudamiento externo. Detecta si el usuario busca sustitutos financieros.<br>
                        • <b>👤 Datos Demográficos:</b> Variables estructurales base (ingresos, edad) para la segmentación de riesgo.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown("---")

        # --- BLOQUE 5: DISTRIBUCIÓN DE MADUREZ ---
        if len(df_filtrado) > 0:
            col_g5_izq, col_g5_der = st.columns([1, 1], gap="medium")
            
            with col_g5_izq:
                fig_violin = px.violin(
                    df_filtrado, x="Year", y="Cited by", box=True, points="all", 
                    template="plotly_dark", color_discrete_sequence=["#00CED1"],
                    labels={"Year": "Año de Publicación", "Cited by": "Citas Recibidas (Scopus)"}
                )
                fig_violin.update_layout(
                    title={'text': "<b>📊 Distribución de Madurez e Impacto Científico por Año</b>", 'y':0.95, 'x':0.0, 'xanchor': 'left', 'yanchor': 'top', 'font': {'size': 16, 'color': '#00CED1'}},
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=60, b=10), height=380
                )
                st.plotly_chart(fig_violin, use_container_width=True)
                
            with col_g5_der:
                st.markdown("""
                <div class="grid-align-container">
                    <div class="chart-glossary">
                        <h5 style="color: #FF1493 !important; margin-top: 0; margin-bottom: 10px; font-size:1.1rem;">🛡️ Interpretación de Impacto Bibliométrico</h5>
                        <p style="margin-bottom: 8px;">Analiza la dispersión, consistencia y madurez del respaldo algorítmico a lo largo del tiempo:</p>
                        • <b>Eje Vertical (Citas Scopus):</b> Cuantifica el nivel de réplica y validación internacional que sostiene cada metodología.<br>
                        • <b>Densidad del Gráfico:</b> Las zonas más anchas muestran las tendencias donde la industria consolidó estándares homogéneos.<br>
                        • <b>Puntos Aislados (Outliers):</b> Representan papers pilar de la analítica de Churn, ideales para auditorías de alta exigencia técnica.
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("Sin datos suficientes.")

    # =========================================================================
    # PESTAÑA 2: SIMULADOR FINANCIERO PERÚ
    # =========================================================================
    with tab2:
        st.markdown("### 🔮 Motor de Simulación de Riesgo Bancario Local")
        st.info(f"🔗 **Estatus del Motor:** Sincronizado con {len(df_filtrado)} papers de Scopus. "
                f"Distribución de coeficientes: 📱 Digital: {peso_trans*100:.1f}% | 💳 Crédito: {peso_score*100:.1f}% | 👤 Perfil: {peso_demo*100:.1f}%")
        
        col_sim1, col_sim2 = st.columns(2)
        with col_sim1:
            st.markdown("#### ⚙️ Entrada del Perfil Transaccional")
            banco_seleccionado = st.selectbox("Selecciona la entidad a evaluar dentro del ecosistema nacional:", ["Banco de Crédito del Perú (BCP)", "BBVA Perú", "Interbank", "Scotiabank Perú"])
            caida_trans = st.slider("1. Contracción mensual en canales de pago móviles (Yape / Plin) (%):", 0, 100, 30)
            score_sbs = st.slider("2. Calificación del Score Crediticio interno (Sentinel / SBS / Equifax):", 300, 850, 710)
            portabilidad_sueldo = st.radio("3. ¿Registra alertas de portabilidad de Cuenta Sueldo o retiro de CTS?", ["No", "Sí"])
            
            score_ponderado = 12.0 + (caida_trans * (peso_trans * 1.2)) + ((850 - score_sbs) * (peso_score * 0.15))
            if portabilidad_sueldo == "Sí": score_ponderado += (28.0 * (peso_demo + 0.4))
            riesgo_final = min(max(score_ponderado, 0.0), 100.0)

        with col_sim2:
            st.markdown(f"#### 🎯 Diagnóstico Operativo ({banco_seleccionado})")
            color_alerta = "#00CED1" if riesgo_final < 50 else "#FF1493"
            st.markdown(f"""
            <div style='background-color: #161B22; padding: 25px; border-radius: 10px; border: 2px solid {color_alerta}; text-align: center;'>
                <p style='color: #E6EDF3; font-size: 1.1rem; margin-bottom: 5px; letter-spacing: 1px;'>RIESGO ESTIMADO DE ABANDONO DE CUENTA</p>
                <h1 style='color: {color_alerta} !important; font-size: 3.8rem; margin: 0;'>{riesgo_final:.1f}%</h1>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 📋 Plan de Acción Táctico de Retención")
            if riesgo_final < 40:
                st.success("🟢 **Zona Segura:** El cliente se mantiene fidelizado. Desplegar campañas pasivas de cross-selling (Millas/Puntos de beneficios).")
            elif 40 <= riesgo_final < 70:
                st.warning("🟡 **Retención Preventiva:** Descenso inusual de actividad digital. Se recomienda la exoneración proactiva de membresías o habilitación de compra de deuda preferencial.")
            else:
                st.error("🔴 **Intervención Inmediata / Alerta Crítica:** Fuga inminente. El protocolo exige asignar el caso de forma prioritaria a un asesor Élite de retención.")

    # =========================================================================
    # PESTAÑA 3: CENTRO DE DATOS
    # =========================================================================
    with tab3:
        st.markdown("### 📚 Centro de Inteligencia y Auditoría Bibliométrica")
        
        with st.expander("🔍 Inspeccionar Atributos de Calidad del Dataset Completo"):
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Journals Únicos Mapeados", df_filtrado['Source title'].nunique())
            col_m2.metric("Año Inicial del Ecosistema", int(df_filtrado['Year'].min()) if len(df_filtrado)>0 else 2024)
            col_m3.metric("Publicaciones en Co-Autoría", df_filtrado['Authors'].str.contains(';|,').sum())
        
        st.markdown("---")
        
        st.markdown("#### 🏆 Top 3 Papers Más Citados")
        top_papers = df_filtrado.sort_values(by="Cited by", ascending=False).head(3)
        
        if len(top_papers) > 0:
            col_card1, col_card2, col_card3 = st.columns(3)
            columnas_cards = [col_card1, col_card2, col_card3]
            
            for idx, (_, row) in enumerate(top_papers.iterrows()):
                with columnas_cards[idx]:
                    st.markdown(f"""
                    <div class="paper-card">
                        <span style="color: #8B949E; font-size: 0.8rem; font-weight: bold; text-transform: uppercase;">🔥 RELEVANCIA ALTA</span>
                        <h4 style="margin: 8px 0; color: #FFF !important; font-size: 1rem; line-height: 1.4;">{row['Title'][:80]}...</h4>
                        <p style="margin: 0; color: #8B949E; font-size: 0.85rem;">Año de publicación: <b>{row['Year']}</b></p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.metric(label="Total de Citas en Scopus", value=int(row['Cited by']))
        else:
            st.warning("⚠️ No se registran publicaciones que cumplan con los criterios mínimos de citas.")

        st.markdown("---")
        
        st.markdown("#### 🗂️ Data Lake Completo (Interactividad Activa)")
        st.markdown("💡 *Haz clic en cualquier fila para auditar detalles, o presiona el icono de enlace en la columna de la derecha para abrir la fuente.*")

        df_lake = df_filtrado[["Title", "Year", "Cited by", "Source title", "Abstract", "Link"]].sort_values(by="Cited by", ascending=False).reset_index(drop=True)
        
        seleccion = st.dataframe(
            df_lake[["Title", "Year", "Cited by", "Source title", "Link"]],
            use_container_width=True,
            hide_index=True,
            selection_mode="single-row",
            on_select="rerun",
            column_config={
                "Title": st.column_config.TextColumn("Título del Estudio Científico"),
                "Year": st.column_config.NumberColumn("Año", format="%d"),
                "Cited by": st.column_config.NumberColumn("Citas Scopus"),
                "Source title": st.column_config.TextColumn("Revista / Journal"),
                "Link": st.column_config.LinkColumn("🔗 Fuente Externa", display_text="Ver Documento")
            }
        )

        if len(seleccion.selection.rows) > 0:
            fila_idx = seleccion.selection.rows[0]
            paper_sel = df_lake.iloc[fila_idx]
            
            abs_text = paper_sel['Abstract'].lower()
            m_t = abs_text.count('transaction') + abs_text.count('behavio') + abs_text.count('digital') + abs_text.count('channel')
            m_s = abs_text.count('credit') + abs_text.count('score') + abs_text.count('risk') + abs_text.count('sbs')
            m_d = abs_text.count('demograph') + abs_text.count('age') + abs_text.count('gender') + abs_text.count('income')
            
            tot = m_t + m_s + m_d
            p_t, p_s, p_d = (m_t/tot*100, m_s/tot*100, m_d/tot*100) if tot > 0 else (33.3, 33.3, 33.3)
            
            st.markdown(f"""
            <div class="detail-box">
                <span style="color: #FF1493; font-weight: bold; font-size: 0.85rem; letter-spacing: 1px;">📋 AUDITORÍA AVANZADA DEL DOCUMENTO SELECCIONADO</span>
                <h3 style="margin-top: 10px; color: #FFF !important;">{paper_sel['Title']}</h3>
                <p style="color: #8B949E; font-size: 0.9rem;"><b>Publicado en:</b> {paper_sel['Source title']} ({paper_sel['Year']})  |  <b>Impacto:</b> {paper_sel['Cited by']} citas.</p>
                <hr style="border-color: #21262D;">
                <h5 style="color: #00CED1 !important;">Resumen Científico (Abstract)</h5>
                <p style="color: #E6EDF3; font-size: 0.95rem; line-height: 1.6; text-align: justify;">{paper_sel['Abstract']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                st.metric(label="📱 Afinidad Transaccional", value=f"{p_t:.1f}%")
            with col_p2:
                st.metric(label="💳 Afinidad Crediticia (Riesgo)", value=f"{p_s:.1f}%")
            with col_p3:
                st.metric(label="👤 Afinidad Demográfica (Perfil)", value=f"{p_d:.1f}%")
        else:
            st.info("💡 **Tip Ejecutivo:** Selecciona una fila de la tabla para abrir el inspector avanzado con el desglose del Abstract de forma inmediata.")

if __name__ == "__main__":
    main()
