import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from streamlit_option_menu import option_menu
from bs4 import BeautifulSoup
import re
import time
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import numpy_financial as npf
from scipy.optimize import bisect

# Configuración general
st.set_page_config(
    page_title="Valuador de proyectos ESGARI",
    page_icon="🚚",  # <- icono de camión
    layout="wide"    # <- modo pantalla completa
)

logo_base64 = """
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
"""

st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo de la Empresa" width="300">
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("<h1 style='text-align: center;'>Valuador de Proyectos ESGARI</h1>", unsafe_allow_html=True)

# Estilo corporativo global
st.markdown("""
    <style>
    h1, h2, h3, .css-10trblm, .css-1v0mbdj {
        color: #2c3e50;
        font-family: 'Segoe UI', sans-serif;
    }
    .stDataFrame thead tr th {
        background-color: #f0f2f6;
        color: #333;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar claves en session_state
def init_session_state():
    defaults = {
        "logged_in": False,
        "username": ""
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Función para validar login
def check_login(username, password):
    users = st.secrets["users"]
    return username in users and users[username] == password

# Si no ha iniciado sesión, mostrar login
if not st.session_state["logged_in"]:
    st.title("🔐 Inicio de Sesión")

    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Iniciar sesión")

        if submitted:
            if check_login(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success("¡Inicio de sesión exitoso!")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")
else:
    # Sidebar
    with st.sidebar:
        selected = option_menu(
            "Menú Principal", 
            ["Inicio", "Análisis", "Configuración", 'WACC Esgari', 'BALANCE'],
            icons=["house", "bar-chart", "gear", "cash", "file-earmark-text"],
            menu_icon="cast",
            default_index=0
        )
    # URLs de fuentes de datos
    comparables = 'https://docs.google.com/spreadsheets/d/13eS6lIAxijfkss69OuPHezPxHuOdQUJF50duelc0jZ4/export?format=xlsx'
    banace_esgari = st.secrets["balance"]["banace_esgari"]

    # Funciones
    @st.cache_data
    def cargar_datos(url):
        response = requests.get(url)
        response.raise_for_status()
        archivo_excel = BytesIO(response.content)
        return pd.read_excel(archivo_excel, engine="openpyxl")

    @st.cache_data
    def extra_beta(ticker):
        url = f'https://www.alphaspread.com/security/nyse/{ticker}/discount-rate'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        beta_value = None
        for beta_div in soup.find_all('div', class_='dotted-underline label pointer tooltip'):
            if 'Beta' in beta_div.text:
                value_div = beta_div.find_previous_sibling('div', class_='value weight-700')
                if value_div:
                    beta_value = value_div.text.strip()
                    break
        return beta_value

    @st.cache_data
    def info_balance(ticker, campo):
        url = f'https://www.alphaspread.com/security/nyse/{ticker}/financials/balance-sheet'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        html_text = soup.prettify()
        pattern = rf'"{campo}".*?"text":"([\d\s]+)"'
        match = re.search(pattern, html_text)
        number = int(match.group(1).replace(" ", "")) if match else 0
        return number

    @st.cache_data
    def des_beta(ticker, tax):
        beta = extra_beta(ticker)
        debt = info_balance(ticker, 'Total Liabilities & Equity') + info_balance(ticker, 'Current Portion of Long-Term Debt') + info_balance(ticker, 'Short-Term Debt')
        equity = info_balance(ticker, 'Total Equity')
        return float(beta) / (1+(1-tax) * debt/equity)

    @st.cache_data
    def mean_beta(com_list):
        sum_beta = 0
        numero = 0
        for x in com_list:
            tax = .3 if x == 'TRAXIONA' else .21
            beta = des_beta(x, tax)
            sum_beta += beta
            numero += 1
            time.sleep(20)
        return sum_beta/numero

    @st.cache_data
    def get_cetes_3y():
        TOKEN = 'eef020dafff1667cc5fb4dc1de10cf314857367cbd5c881511679bb2e7a7433a'
        SERIE_ID = "SF43936"
        url = f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/{SERIE_ID}/datos/oportuno"
        headers = {"Bmx-Token": TOKEN}
        response = requests.get(url, headers=headers)
        data = response.json()
        try:
            return float(data['bmx']['series'][0]['datos'][0]['dato'])
        except (KeyError, IndexError, ValueError):
            return None

    @st.cache_data
    def erp():
        url = "https://pages.stern.nyu.edu/~adamodar/pc/datasets/ctryprem.xlsx"
        df = pd.read_excel(url, sheet_name="ERPs by country", skiprows=5)
        df.columns = df.iloc[0]
        df = df[1:].iloc[:, :7]
        return df[df['Country'] == 'Mexico']['Total Equity Risk Premium'].values[0]

    @st.cache_data
    def cargar_datos_hoja(url, nombre_hoja=None):
        response = requests.get(url)
        archivo_excel = BytesIO(response.content)
        return pd.read_excel(archivo_excel, engine="openpyxl", sheet_name=nombre_hoja)

    @st.cache_data
    def apalancar_beta(beta_des, tax, debt, equity):
        return beta_des * (1 + (1 - tax) * (debt / equity))


    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
            'gasto_fijo': 500000,
            'gasto_variable_pct': 40,
            'numero_unidades': 0,
            'valor_amortizacion_unidades': 250000,
            'ingresos_mensuales': 1500000,
            'inversion_capital': 0,
            'inversion_deuda': 0,
            'tiempo_contrato': 24,
            'tiempo_amortizacion': 48,
            'tiempo_pagos': 0,
            'otro_amort': 0,
            'tiempo_amortizacion_activo': 1,
        }
    st.session_state.gasto_fijo = st.session_state.form_data['gasto_fijo']
    st.session_state.gasto_variable_pct = st.session_state.form_data['gasto_variable_pct']
    st.session_state.numero_unidades = st.session_state.form_data['numero_unidades']
    st.session_state.valor_amortizacion_unidades = st.session_state.form_data['valor_amortizacion_unidades']
    st.session_state.ingresos_mensuales = st.session_state.form_data['ingresos_mensuales']
    st.session_state.inversion_capital = st.session_state.form_data['inversion_capital']
    st.session_state.inversion_deuda = st.session_state.form_data['inversion_deuda']
    st.session_state.tiempo_contrato = st.session_state.form_data['tiempo_contrato']
    st.session_state.tiempo_amortizacion = st.session_state.form_data['tiempo_amortizacion']
    st.session_state.tiempo_pagos = st.session_state.form_data['tiempo_pagos']
    st.session_state.otro_amort = st.session_state.form_data['otro_amort']
    st.session_state.tiempo_amortizacion_activo = st.session_state.form_data['tiempo_amortizacion_activo']

    if 'form_contra' not in st.session_state:
        st.session_state.form_contra = {
            'contratos_1_tonelada': 0,
            'costo_mensual_1_tonelada': 0.00,
            'tiempo_contrato_1_tonelada': 0,
            'contratos_3_5_toneladas': 0,
            'costo_mensual_3_5_toneladas': 0.00,
            'tiempo_contrato_3_5_toneladas': 0,
            'contratos_5_toneladas': 0,
            'costo_mensual_5_toneladas': 0.00,
            'tiempo_contrato_5_toneladas': 0,
            'contratos_rabon': 0,
            'costo_mensual_rabon': 0.00,
            'tiempo_contrato_rabon': 0,
            'contratos_torton': 0,
            'costo_mensual_torton': 0.00,
            'tiempo_contrato_torton': 0,
            'contratos_tracto_sencillo': 0,
            'costo_mensual_tracto_sencillo': 0.00,
            'tiempo_contrato_tracto_sencillo': 0,
            'contratos_tracto_full': 0,
            'costo_mensual_tracto_full': 0.00,
            'tiempo_contrato_tracto_full': 0,
            'contratos_caja_seca': 0,
            'costo_mensual_caja_seca': 0.00,
            'tiempo_contrato_caja_seca': 0
        }

    st.session_state.contratos_1_tonelada = st.session_state.form_contra['contratos_1_tonelada']
    st.session_state.costo_mensual_1_tonelada = st.session_state.form_contra['costo_mensual_1_tonelada']
    st.session_state.tiempo_contrato_1_tonelada = st.session_state.form_contra['tiempo_contrato_1_tonelada']
    st.session_state.contratos_3_5_toneladas = st.session_state.form_contra['contratos_3_5_toneladas']
    st.session_state.costo_mensual_3_5_toneladas = st.session_state.form_contra['costo_mensual_3_5_toneladas']
    st.session_state.tiempo_contrato_3_5_toneladas = st.session_state.form_contra['tiempo_contrato_3_5_toneladas']
    st.session_state.contratos_5_toneladas = st.session_state.form_contra['contratos_5_toneladas']
    st.session_state.costo_mensual_5_toneladas = st.session_state.form_contra['costo_mensual_5_toneladas']
    st.session_state.tiempo_contrato_5_toneladas = st.session_state.form_contra['tiempo_contrato_5_toneladas']
    st.session_state.contratos_rabon = st.session_state.form_contra['contratos_rabon']
    st.session_state.costo_mensual_rabon = st.session_state.form_contra['costo_mensual_rabon']
    st.session_state.tiempo_contrato_rabon = st.session_state.form_contra['tiempo_contrato_rabon']
    st.session_state.contratos_torton = st.session_state.form_contra['contratos_torton']
    st.session_state.costo_mensual_torton = st.session_state.form_contra['costo_mensual_torton']
    st.session_state.tiempo_contrato_torton = st.session_state.form_contra['tiempo_contrato_torton']
    st.session_state.contratos_tracto_sencillo = st.session_state.form_contra['contratos_tracto_sencillo']
    st.session_state.costo_mensual_tracto_sencillo = st.session_state.form_contra['costo_mensual_tracto_sencillo']
    st.session_state.tiempo_contrato_tracto_sencillo = st.session_state.form_contra['tiempo_contrato_tracto_sencillo']
    st.session_state.contratos_tracto_full = st.session_state.form_contra['contratos_tracto_full']
    st.session_state.costo_mensual_tracto_full = st.session_state.form_contra['costo_mensual_tracto_full']
    st.session_state.tiempo_contrato_tracto_full = st.session_state.form_contra['tiempo_contrato_tracto_full']
    st.session_state.contratos_caja_seca = st.session_state.form_contra['contratos_caja_seca']
    st.session_state.costo_mensual_caja_seca = st.session_state.form_contra['costo_mensual_caja_seca']
    st.session_state.tiempo_contrato_caja_seca = st.session_state.form_contra['tiempo_contrato_caja_seca']

    # Guardar contratos_info en session_state para acceso global
    if "contratos_info" not in st.session_state:
        st.session_state["contratos_info"] = [
            {"nombre": "1 Tonelada", "key": "1_tonelada"},
            {"nombre": "3.5 Toneladas", "key": "3_5_toneladas"},
            {"nombre": "5 Toneladas", "key": "5_toneladas"},
            {"nombre": "Rabón", "key": "rabon"},
            {"nombre": "Torton", "key": "torton"},
            {"nombre": "Tracto Sencillo", "key": "tracto_sencillo"},
            {"nombre": "Tracto Full", "key": "tracto_full"},
            {"nombre": "Caja Seca", "key": "caja_seca"},
            {"nombre": "Renta local", "key": "renta_local"},
        ]


    def update_form_contra():
        st.session_state.form_contra['contratos_1_tonelada'] = st.session_state.contratos_1_tonelada
        st.session_state.form_contra['costo_mensual_1_tonelada'] = st.session_state.costo_mensual_1_tonelada
        st.session_state.form_contra['tiempo_contrato_1_tonelada'] = st.session_state.tiempo_contrato_1_tonelada
        st.session_state.form_contra['contratos_3_5_toneladas'] = st.session_state.contratos_3_5_toneladas
        st.session_state.form_contra['costo_mensual_3_5_toneladas'] = st.session_state.costo_mensual_3_5_toneladas
        st.session_state.form_contra['tiempo_contrato_3_5_toneladas'] = st.session_state.tiempo_contrato_3_5_toneladas
        st.session_state.form_contra['contratos_5_toneladas'] = st.session_state.contratos_5_toneladas
        st.session_state.form_contra['costo_mensual_5_toneladas'] = st.session_state.costo_mensual_5_toneladas
        st.session_state.form_contra['tiempo_contrato_5_toneladas'] = st.session_state.tiempo_contrato_5_toneladas
        st.session_state.form_contra['contratos_rabon'] = st.session_state.contratos_rabon
        st.session_state.form_contra['costo_mensual_rabon'] = st.session_state.costo_mensual_rabon
        st.session_state.form_contra['tiempo_contrato_rabon'] = st.session_state.tiempo_contrato_rabon
        st.session_state.form_contra['contratos_torton'] = st.session_state.contratos_torton
        st.session_state.form_contra['costo_mensual_torton'] = st.session_state.costo_mensual_torton
        st.session_state.form_contra['tiempo_contrato_torton'] = st.session_state.tiempo_contrato_torton
        st.session_state.form_contra['contratos_tracto_sencillo'] = st.session_state.contratos_tracto_sencillo
        st.session_state.form_contra['costo_mensual_tracto_sencillo'] = st.session_state.costo_mensual_tracto_sencillo
        st.session_state.form_contra['tiempo_contrato_tracto_sencillo'] = st.session_state.tiempo_contrato_tracto_sencillo
        st.session_state.form_contra['contratos_tracto_full'] = st.session_state.contratos_tracto_full
        st.session_state.form_contra['costo_mensual_tracto_full'] = st.session_state.costo_mensual_tracto_full
        st.session_state.form_contra['tiempo_contrato_tracto_full'] = st.session_state.tiempo_contrato_tracto_full
        st.session_state.form_contra['contratos_caja_seca'] = st.session_state.contratos_caja_seca
        st.session_state.form_contra['costo_mensual_caja_seca'] = st.session_state.costo_mensual_caja_seca
        st.session_state.form_contra['tiempo_contrato_caja_seca'] = st.session_state.tiempo_contrato_caja_seca

    def update_form_data():
        st.session_state.form_data['gasto_fijo'] = st.session_state.gasto_fijo
        st.session_state.form_data['gasto_variable_pct'] = st.session_state.gasto_variable_pct
        st.session_state.form_data['numero_unidades'] = st.session_state.numero_unidades
        st.session_state.form_data['valor_amortizacion_unidades'] = st.session_state.valor_amortizacion_unidades
        st.session_state.form_data['ingresos_mensuales'] = st.session_state.ingresos_mensuales
        st.session_state.form_data['inversion_capital'] = st.session_state.inversion_capital
        st.session_state.form_data['inversion_deuda'] = st.session_state.inversion_deuda
        st.session_state.form_data['tiempo_contrato'] = st.session_state.tiempo_contrato
        st.session_state.form_data['tiempo_amortizacion'] = st.session_state.tiempo_amortizacion
        st.session_state.form_data['tiempo_pagos'] = st.session_state.tiempo_pagos
        st.session_state.form_data['otro_amort'] = st.session_state.otro_amort
        st.session_state.form_data['tiempo_amortizacion_activo'] = st.session_state.tiempo_amortizacion_activo


    def inicializar_df_amortizacion(meses: int = 60):
        return pd.DataFrame({
            "Mes": list(range(1, meses + 1)),
            "Amortización": [0.0] * meses,
            "Interés": [0.0] * meses,
            "Pago Total": [0.0] * meses,
            "Saldo Restante": [0.0] * meses,
        })

    if "df_amortizacion_consolidada" not in st.session_state:
        st.session_state["df_amortizacion_consolidada"] = inicializar_df_amortizacion()


    # Cálculos de capital
    com = cargar_datos(comparables)
    com_list = com['ticket'].tolist()
    com = com.set_index('empresa')
    beta_pro = mean_beta(com_list)
    erp_mex = erp()
    risk_free = get_cetes_3y() / 100
    tiie_spread = risk_free + .05
    df_balance = cargar_datos_hoja(banace_esgari, '2025')
    df_balance['NETO 2025'] = df_balance['NETO 2025']*1000
    df_balance['NETO 2024'] = df_balance['NETO 2024']*1000
    deuda = df_balance[df_balance['CUENTA'] == 'Contrato de derecho de uso (CP)']['NETO 2025'].values[0] + \
            df_balance[df_balance['CUENTA'] == 'Creditos Bancarios']['NETO 2025'].values[0] + \
            df_balance[df_balance['CUENTA'] == 'Contratos por derecho de uso']['NETO 2025'].values[0]
    equity = df_balance[df_balance['CUENTA'] == 'Total Capital Contable']['NETO 2025'].values[0]
    cash = df_balance[df_balance['CUENTA'] == 'Bancos']['NETO 2025'].values[0]
    deuda_neta = deuda - cash
    beta_esg = apalancar_beta(beta_pro, .3, deuda, equity)
    eq = risk_free + (beta_esg * erp_mex)
    co_de = .1268
    kd = co_de * (1 - .3)
    wacc = (deuda_neta / (deuda_neta + equity)) * kd + (equity / (deuda_neta + equity)) * eq
    debt_weight = deuda_neta / (deuda_neta + equity)

    # Páginas del menú
    if selected == 'Inicio':
        st.markdown("## Bienvenido")
        st.markdown("Esta aplicación le permite calcular métricas clave para la valoración financiera de proyectos ESGARI utilizando información de mercado y financiera actualizada.")

    elif selected == 'Análisis':
        st.markdown("## Análisis de Comparables")
        st.dataframe(com.reset_index().style.format(precision=2))

    elif selected == 'Configuración':
        st.markdown("## Configuración del proyecto")
        sec = option_menu(
            "Cálculos del Proyecto",
            ["Calculo de Flujos", "Calculo de Contratos"],
            icons=["graph-up-arrow", "percent"],
            orientation="horizontal"
        )
        st.markdown("---")

        if sec == "Calculo de Flujos":
            
            st.info("Aquí puedes agregar futuros parámetros de configuración para personalizar los cálculos.")
            tipo_pro = st.checkbox("¿Es un proyecto de OH?",)

            col1, col2, col3 = st.columns(3)
            gasto_fijo = col1.number_input("Gasto Fijo $", format="%.2f", step=500000.0, help="Gasto fijo mensual del proyecto", key="gasto_fijo", on_change=update_form_data)
            gasto_variable_pct = col2.number_input("Gasto Variable (%)", min_value=0.0, max_value=100.0, step=0.5, format="%.1f", help="Porcentaje de gasto variable sobre ventas", key="gasto_variable_pct", on_change=update_form_data)
            gasto_variable = gasto_variable_pct / 100.0
            ingresos_mensuales = col3.number_input("Ingresos Mensuales $", format="%.2f", step=500000.0, help="Ingresos mensuales del proyecto u ahorro generado por proyecto", key="ingresos_mensuales", on_change=update_form_data)
            inversion_capital = col1.number_input("Inversión de Capital Inicial $", format="%.2f", step=500000.0, help="Inversión inicial del proyecto pagado con capital", key="inversion_capital", on_change=update_form_data)
            inversion_deuda = col2.number_input("Inversión de Deuda Inicial $", format="%.2f", step=500000.0, help="Inversión inicial del proyecto pagado con deuda", key="inversion_deuda", on_change=update_form_data)
            inversion = inversion_capital + inversion_deuda
            tiempo_contrato = col2.number_input("Tiempo de Contrato (meses)", step=1, help="Tiempo de contrato del proyecto", key="tiempo_contrato", on_change=update_form_data)
            tiempo_pagos = col3.number_input("Tiempo de Pagos (meses)", step=1, help="Meses que tarda en pagar el cliente", key="tiempo_pagos", on_change=update_form_data)

            df_amort = st.session_state.get("df_amortizacion_consolidada", None)
            kd_mensual = kd / 12

            if df_amort is None or df_amort.empty:
                st.warning("No hay tabla de amortización consolidada. Ve primero a 'Cálculo de Contratos'.")
            else:
                # --- Amortización de la deuda inicial ---
                amortizacion_mensual_deuda = inversion_deuda / tiempo_contrato
                saldo_restante = inversion_deuda
                tabla_amortizacion_deuda = []

                for mes in range(1, tiempo_contrato + 1):
                    interes_mes = saldo_restante * kd_mensual
                    saldo_restante -= amortizacion_mensual_deuda
                    saldo_restante = max(saldo_restante, 0)
                    tabla_amortizacion_deuda.append({
                        "Mes": mes,
                        "Interés Deuda": interes_mes,
                        "Amortizacion Deuda": amortizacion_mensual_deuda
                    })

                df_amort_deuda = pd.DataFrame(tabla_amortizacion_deuda)

                deuda_total = df_amort["Amortización"].sum()
                wacc_pro = (((deuda_neta + inversion_deuda + deuda_total) / (deuda_neta + inversion_deuda + equity - inversion_capital + deuda_total)) * kd +
                            ((equity - inversion_capital) / (deuda_neta + inversion_deuda + equity - inversion_capital + deuda_total)) * eq)
                wacc_mensual = wacc_pro / 12

                flujos = [{
                    "Mes": 0,
                    "Ingresos": 0,
                    "Gasto Fijo": 0,
                    "Gasto Variable": 0,
                    "Interés": 0,
                    "Amortizacion": 0,
                    "Flujo Neto": -inversion,
                    "Flujo Descontado": -inversion,
                    "Capital de Trabajo": inversion,
                }]

                amort_vida_contrato = df_amort[df_amort["Mes"] <= tiempo_contrato]["Amortización"].sum()
                npv = -inversion - amort_vida_contrato
                if not tipo_pro:
                    oh_pct = st.number_input(
                        "Porcentaje de Overhead (OH)", 
                        value=11.5, 
                        step=0.1, 
                        format="%.1f", 
                        key="oh_pct_input"
                    ) / 100
                else:
                    oh_pct = 0
                for mes in range(1, tiempo_contrato + 1):
                    ingresos = ingresos_mensuales
                    gastos_variables = ingresos * gasto_variable
                    gasto_total = gasto_fijo + gastos_variables

                    # Interés y amortización de contratos
                    interes_contratos = df_amort["Interés"].iloc[mes - 1] if mes - 1 < len(df_amort) else 0
                    amort_contratos = df_amort["Amortización"].iloc[mes - 1] if mes - 1 < len(df_amort) else 0

                    # Interés y amortización de la deuda inicial
                    interes_deuda = df_amort_deuda["Interés Deuda"].iloc[mes - 1] if mes - 1 < len(df_amort_deuda) else 0
                    amort_deuda = df_amort_deuda["Amortizacion Deuda"].iloc[mes - 1] if mes - 1 < len(df_amort_deuda) else 0

                    interes = interes_contratos + interes_deuda
                    capital = amort_contratos + amort_deuda
                    deuda = interes + capital

                    oh = ingresos * oh_pct if not tipo_pro else 0  
                    gasto_total_ajustado = gasto_total + oh

                    flujo_neto = ingresos - gasto_total_ajustado - deuda
                    flujo_descontado = flujo_neto / ((1 + wacc_mensual) ** mes)
                    npv += flujo_descontado

                    utilidad_operativa = ingresos - gasto_fijo - gastos_variables - capital 

                    capital_trabajo = 0
                    if flujo_neto < 0:
                        capital_trabajo = -flujo_neto
                        if mes <= tiempo_pagos:
                            capital_trabajo += gasto_total + interes + capital

                    flujos.append({
                        "Mes": mes,
                        "Ingresos": ingresos,
                        "Gasto Fijo": gasto_fijo,
                        "Gasto Variable": gastos_variables,
                        "Interés": interes,
                        "Amortizacion": capital,
                        "OH": oh,
                        "Flujo Neto": flujo_neto,
                        "Flujo Descontado": flujo_descontado,
                        "Capital de Trabajo": capital_trabajo,
                        "Utilidad Operativa": utilidad_operativa,
                    })

                def calcular_vpn_con_ingreso(ingreso_mensual, inversion, amort_vida_contrato, tiempo_contrato, gasto_fijo, gasto_variable, df_amort, df_amort_deuda, wacc_mensual, tiempo_pagos, tipo_pro):
                    npv = -inversion - amort_vida_contrato
                    for mes in range(1, tiempo_contrato + 1):
                        ingresos = ingreso_mensual
                        gastos_variables = ingresos * gasto_variable
                        gasto_total = gasto_fijo + gastos_variables

                        interes_contratos = df_amort["Interés"].iloc[mes - 1] if mes - 1 < len(df_amort) else 0
                        amort_contratos = df_amort["Amortización"].iloc[mes - 1] if mes - 1 < len(df_amort) else 0

                        interes_deuda = df_amort_deuda["Interés Deuda"].iloc[mes - 1] if mes - 1 < len(df_amort_deuda) else 0
                        amort_deuda = df_amort_deuda["Amortizacion Deuda"].iloc[mes - 1] if mes - 1 < len(df_amort_deuda) else 0

                        interes = interes_contratos + interes_deuda
                        capital = amort_contratos + amort_deuda
                        deuda = interes + capital

                        oh = ingresos * oh_pct if not tipo_pro else 0
                        gasto_total_ajustado = gasto_total + oh

                        flujo_neto = ingresos - gasto_total_ajustado - deuda
                        flujo_descontado = flujo_neto / ((1 + wacc_mensual) ** mes)
                        npv += flujo_descontado

                    return npv


                try:
                    ingreso_minimo = bisect(
                        lambda x: calcular_vpn_con_ingreso(
                            x,
                            inversion,
                            amort_vida_contrato,
                            tiempo_contrato,
                            gasto_fijo,
                            gasto_variable,
                            df_amort,
                            df_amort_deuda,
                            wacc_mensual,
                            tiempo_pagos,
                            tipo_pro
                        ),
                        0, 50_000_000
                    )

                except ValueError:
                    ingreso_minimo = "N/A"

                df_flujos = pd.DataFrame(flujos)

                capital_trabajo = []

                for i, row in df_flujos.iterrows():
                    mes = row["Mes"]
                    flujo_neto = row["Flujo Neto"]

                    capital_mes = 0

                    if mes <= tiempo_pagos and mes != 0:
                        capital_mes += row["Gasto Fijo"] + row["Gasto Variable"] + row["Interés"] + row["Amortizacion"] + row["OH"]

                    if flujo_neto < 0 and mes != 0:
                        capital_mes += -flujo_neto

                    capital_trabajo.append(capital_mes)

                df_flujos["Capital de Trabajo"] = capital_trabajo
                df_flujos.loc[df_flujos["Mes"] == 0, "Capital de Trabajo"] = inversion

                st.markdown("---")
                st.header("📊 Análisis Financiero del Proyecto")

                st.subheader("📈 Flujos del Proyecto")
                fig_flujo = px.line(df_flujos, x="Mes", y=["Flujo Neto", "Flujo Descontado"],
                                    labels={"value": "Monto ($)", "Mes": "Mes"}, markers=True,
                                    title="Flujo Neto vs Flujo Descontado")
                fig_flujo.update_layout(template="plotly_white", legend_title_text='Tipo de Flujo')
                st.plotly_chart(fig_flujo, use_container_width=True)

                fig_capital = px.area(df_flujos, x="Mes", y="Capital de Trabajo",
                                    labels={"Capital de Trabajo": "Capital Acumulado ($)", "Mes": "Mes"},
                                    title="Requerimiento de Capital Adicional (Capital de Trabajo)")
                fig_capital.update_layout(template="plotly_white")
                st.plotly_chart(fig_capital, use_container_width=True)

                st.markdown("---")
                st.subheader("📄 Tabla de Flujos")
                column_order = [
                    "Mes",
                    "Ingresos",
                    "Gasto Fijo",
                    "Gasto Variable",
                    "OH",
                    "Interés",
                    "Amortizacion",
                    "Utilidad Operativa",
                    "Flujo Neto",
                    "Flujo Descontado",
                    "Capital de Trabajo"
                ]

                df_flujos = df_flujos[column_order]
                df_flujos["Margen Operativo (%)"] = np.where(
                    df_flujos["Ingresos"] != 0,
                    (df_flujos["Utilidad Operativa"] / df_flujos["Ingresos"]) * 100,
                    0
                )
                st.dataframe(df_flujos.set_index("Mes").style.format({
                    "Ingresos": "${:,.2f}",
                    "Gasto Fijo": "${:,.2f}",
                    "Gasto Variable": "${:,.2f}",
                    "OH": "${:,.2f}",
                    "Interés": "${:,.2f}",
                    "Amortizacion": "${:,.2f}",
                    "Utilidad Operativa": "${:,.2f}",
                    "Flujo Neto": "${:,.2f}",
                    "Flujo Descontado": "${:,.2f}",
                    "Capital de Trabajo": "${:,.2f}",
                    "Margen Operativo (%)": "{:.2f}%",
                }), use_container_width=True, height=500)

                flujos_totales = [row["Flujo Neto"] for row in flujos]
                flujos_totales[0] -= amort_vida_contrato

                tir = npf.irr(flujos_totales)
                tir_anual = tir * 12
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                col1.metric(label="📌 Valor Presente Neto (NPV)", value=f"${npv:,.2f}")
                col2.metric(label="💰 Capital de Trabajo Total", value=f"${df_flujos['Capital de Trabajo'].sum():,.2f}")
                col3.metric(label="📉 WACC del Proyecto", value=f"{wacc_pro:.2%}")
                col1.metric(label="🧾 Amortización Total (Contrato)", value=f"${amort_vida_contrato:,.2f}")
                col2.metric(label="📈 Tasa Interna de Retorno (TIR)", value=f"{tir_anual:.2%}" if tir_anual is not None else "N/A")
                col3.metric(label="💵 Ingreso Mínimo Mensual", value=f"${ingreso_minimo:,.2f}" if isinstance(ingreso_minimo, (int, float)) else "N/A")
                margen_esperado = df_flujos.loc[df_flujos["Margen Operativo (%)"] > 0, "Margen Operativo (%)"].mean()
                col1.metric(label="📊 Rentabilidad Operativa Esperada del proyecto", value=f"{margen_esperado:.2f}%")
                st.markdown("---")
                st.subheader("📌 Consideraciones del Proyecto")

                if npv > 0:
                    st.success("✅ El proyecto es viable, ya que el Valor Presente Neto (NPV) es positivo.")
                    contratos_sobrantes = []
                    total_valor_pendiente = 0
                    contratos_info = st.session_state["contratos_info"]

                    for contrato in contratos_info:
                        nombre = contrato["nombre"]
                        key = contrato["key"]
                        num_contratos = st.session_state.get(f"contratos_{key}", 0)
                        tiempo_individual = st.session_state.get(f"tiempo_contrato_{key}", 0)
                        costo_mensual = st.session_state.get(f"costo_mensual_{key}", 0)

                        if num_contratos > 0 and tiempo_individual > tiempo_contrato:
                            meses_restantes = tiempo_individual - tiempo_contrato
                            tasa_mensual = tiie_spread / 12
                            valor_presente_unitario = costo_mensual * (1 - (1 + tasa_mensual) ** -tiempo_individual) / tasa_mensual
                            amortizacion_mensual = valor_presente_unitario / tiempo_individual
                            valor_pendiente = amortizacion_mensual * meses_restantes * num_contratos

                            contratos_sobrantes.append({
                                "Contrato": nombre,
                                "Unidades Contratadas": num_contratos,
                                "Meses Restantes": meses_restantes,
                                "Valor Pendiente por Amortizar": valor_pendiente
                            })
                            total_valor_pendiente += valor_pendiente

                    if contratos_sobrantes:
                        with st.expander("🔍 Contratos con duración mayor al proyecto"):
                            st.info("Al terminar el contrato del proyecto, los siguientes contratos deben utilizarse en nuevos proyectos para maximizar su valor:")
                            df_sobrantes = pd.DataFrame(contratos_sobrantes).set_index("Contrato")
                            st.dataframe(df_sobrantes.style.format({
                                "Valor Pendiente por Amortizar": "${:,.2f}"
                            }), use_container_width=True)

                            st.markdown("#### 💰 Valor total pendiente por amortizar:")
                            st.metric(label="Total aprovechable en nuevos proyectos", value=f"${total_valor_pendiente:,.2f}")
                else:
                    st.warning("⚠️ El proyecto no es viable, ya que el Valor Presente Neto (NPV) es negativo.")




        elif sec == "Calculo de Contratos":
            st.subheader("📄 Análisis de Contratos")

            # Definir tipos de contrato y metadatos
            contratos_info = [
                {"nombre": "1 Tonelada", "col": 0, "key": "1_tonelada"},
                {"nombre": "3.5 Toneladas", "col": 1, "key": "3_5_toneladas"},
                {"nombre": "5 Toneladas", "col": 2, "key": "5_toneladas"},
                {"nombre": "Rabón", "col": 0, "key": "rabon"},
                {"nombre": "Torton", "col": 1, "key": "torton"},
                {"nombre": "Tracto Sencillo", "col": 2, "key": "tracto_sencillo"},
                {"nombre": "Tracto Full", "col": 0, "key": "tracto_full"},
                {"nombre": "Caja Seca", "col": 1, "key": "caja_seca"},
                {"nombre": "Renta local", "col": 2, "key": "renta_local"},
            ]

            # Crear columnas
            cols = st.columns(3)

            # Inputs dinámicos
            for contrato in contratos_info:
                with cols[contrato["col"]]:
                    st.number_input(f"Contratos {contrato['nombre']}", step=1, key=f"contratos_{contrato['key']}", help=f"Número de contratos de camiones {contrato['nombre']}", on_change=update_form_contra)
                    st.number_input(f"Costo mensual {contrato['nombre']}", step=500000.00, key=f"costo_mensual_{contrato['key']}", help=f"Costo mensual de camiones {contrato['nombre']}", on_change=update_form_contra)
                    st.number_input(f"Tiempo de contrato {contrato['nombre']}", step=1, key=f"tiempo_contrato_{contrato['key']}", help=f"Tiempo de contrato de camiones {contrato['nombre']}", on_change=update_form_contra)

            st.markdown("---")

            # Resumen
            st.subheader("📄 Valor Presentes de Contratos")

            # Mostrar 3 contratos por fila usando columnas
            cols_resumen = st.columns(3)

            for i, contrato in enumerate(contratos_info):
                num = st.session_state.get(f"contratos_{contrato['key']}", 0)
                costo = st.session_state.get(f"costo_mensual_{contrato['key']}", 0)
                tiempo = st.session_state.get(f"tiempo_contrato_{contrato['key']}", 0)

                with cols_resumen[i % 3]:  # distribuye en columnas de 3
                    if num > 0 and costo > 0 and tiempo > 0:
                        valor_presente = costo * (1 - (1 + (tiie_spread / 12)) ** -tiempo) / (tiie_spread / 12)
                        st.metric(label=f"{contrato['nombre']}", value=f"${valor_presente:,.2f}")
                    else:
                        st.metric(label=f"{contrato['nombre']}", value="No aplica")

                # Cada 3 elementos reinicia las columnas
                if (i + 1) % 3 == 0 and i + 1 < len(contratos_info):
                    cols_resumen = st.columns(3)
                    
            st.markdown("---")
            st.subheader("📄 Tabla de Amortización Consolidada")
            amortizacion_total = {}
            saldos_individuales = {}  # Para llevar seguimiento del saldo por contrato

            for contrato in contratos_info:
                nombre = contrato["nombre"]
                key = contrato["key"]
                num = st.session_state.get(f"contratos_{key}", 0)
                costo = st.session_state.get(f"costo_mensual_{key}", 0)
                tiempo = st.session_state.get(f"tiempo_contrato_{key}", 0)

                if num > 0 and costo > 0 and tiempo > 0:
                    tasa_mensual = tiie_spread / 12
                    valor_presente_unitario = costo * (1 - (1 + tasa_mensual) ** -tiempo) / tasa_mensual
                    amortizacion_mensual = valor_presente_unitario / tiempo

                    for i in range(num):
                        saldo = valor_presente_unitario
                        for mes in range(1, tiempo + 1):
                            interes = saldo * tasa_mensual
                            pago_total = amortizacion_mensual + interes
                            saldo -= amortizacion_mensual

                            if mes not in amortizacion_total:
                                amortizacion_total[mes] = {
                                    "Amortización": 0,
                                    "Interés": 0,
                                    "Pago Total": 0,
                                    "Saldo Restante": 0,
                                }

                            amortizacion_total[mes]["Amortización"] += amortizacion_mensual
                            amortizacion_total[mes]["Interés"] += interes
                            amortizacion_total[mes]["Pago Total"] += pago_total
                            amortizacion_total[mes]["Saldo Restante"] += max(saldo, 0)

            if amortizacion_total:
                df_consolidado = pd.DataFrame([
                    {
                        "Mes": mes,
                        "Amortización": valores["Amortización"],
                        "Interés": valores["Interés"],
                        "Pago Total": valores["Pago Total"],
                        "Saldo Restante": valores["Saldo Restante"]
                    }
                    for mes, valores in sorted(amortizacion_total.items())
                ])
                st.session_state["df_amortizacion_consolidada"] = df_consolidado
                st.dataframe(df_consolidado.style.format({
                    "Amortización": "${:,.2f}",
                    "Interés": "${:,.2f}",
                    "Pago Total": "${:,.2f}",
                    "Saldo Restante": "${:,.2f}"
                }))
            else:
                st.info("No hay contratos válidos para mostrar amortización.")
                
    elif selected == 'WACC Esgari':
        st.markdown("<h2 style='text-align: center;'>Análisis de Tasa de Descuento (WACC)</h2>", unsafe_allow_html=True)
        st.markdown("---")

        sec = option_menu(
            "Cálculos Financieros",
            ["Cálculo del WACC", "Costo de Capital Propio", "Deuda"],
            icons=["graph-up-arrow", "percent", "bank"],
            orientation="horizontal"
        )

        if sec == "Costo de Capital Propio":
            with st.container():
                st.subheader("Empresas Comparables")
                st.dataframe(com.style.format(precision=2))

                st.markdown("### Parámetros de Mercado")
                col1, col2 = st.columns(2)
                col1.metric("Beta desapalancada Promedio", f"{beta_pro:.2f}")
                col2.metric("Beta Apalancado Esgari", f"{beta_esg:.2f}")
                col1.metric("Equity Risk Premium (ERP) México", f"{erp_mex*100:.2f}%")
                col2.metric("Tasa Libre de Riesgo", f"{risk_free*100:.2f}%")

                st.markdown("### Resultado Final")
                st.success(f"Costo de Capital Propio: {eq*100:.2f}%", icon="📊")

                st.markdown("---")
                st.markdown("### Explicación y Fórmula")
                st.markdown("""
                El **Costo de Capital Propio (Ke)** representa el rendimiento mínimo que los accionistas esperan por su inversión.

                Este valor es clave para decidir si una empresa debe seguir financiando sus operaciones con capital propio o buscar otras fuentes.

                Se basa en la sensibilidad de la empresa al mercado (Beta), ajustada por el apalancamiento financiero y el riesgo país.

                **Fórmula utilizada:**

                $$
                K_e = R_f + \\beta_{apal} \\times ERP
                $$

                Donde:

                - $R_f$ = Tasa libre de riesgo (CETES 28 dias)  
                - $\\beta_{apal}$ = Beta apalancada del proyecto  
                - $ERP$ = Prima de riesgo del mercado / Retorno esperado del mercado - $R_f$ (en este caso, para México)
                """)

        elif sec == "Cálculo del WACC":
            with st.container():
                st.subheader("Composición del WACC")
                col1, col2 = st.columns(2)
                col1.metric("Peso de la Deuda", f"{debt_weight*100:.2f}%")
                col2.metric("Costo de la Deuda (Neta)", f"{kd*100:.2f}%")
                col2.metric("Costo de Capital Propio", f"{eq*100:.2f}%")
                col1.metric("Peso del Capital", f"{(1-debt_weight)*100:.2f}%")

                st.markdown("### Resultado Final")
                st.success(f"WACC ESGARI: {wacc*100:.2f}%", icon="📊")

                st.markdown("---")
                st.markdown("### Explicación y Fórmula")
                st.markdown("""
                El **WACC (Weighted Average Cost of Capital)** es una métrica fundamental en finanzas corporativas.

                Indica el costo promedio que tiene una empresa para financiarse, considerando el costo del capital propio y de la deuda.

                Se utiliza para descontar flujos de caja en evaluaciones de proyectos, valuaciones y análisis de retorno.

                Un proyecto es financieramente viable si su retorno es **mayor al WACC**, lo que implica generación de valor.

                **Fórmula utilizada:**

                $$
                WACC = \\left(\\frac{D}{D + E}\\right) \\cdot K_d + \\left(\\frac{E}{D + E}\\right) \\cdot K_e
                $$

                Donde:

                - $D$ = Deuda neta  
                - $E$ = Capital contable  
                - $K_d$ = Costo de la deuda después de impuestos  
                - $K_e$ = Costo de capital propio
                """)

        else:
            with st.container():
                st.subheader("Deuda Neta")
                col1, col2 = st.columns(2)
                col1.metric("Deuda Neta", f"${deuda_neta:,.0f}")
                col2.metric("Deuda Total", f"${deuda:,.0f}")
                col1.metric("Costo de la Deuda", f"{co_de*100:.2f}%")
                col2.metric("Costo de la deuda con escudo fiscal", f"{kd*100:.2f}%")

                st.markdown("### Resultado Final")
                st.success(f"Deuda Neta: ${deuda_neta:,.2f}", icon="💰")

                st.markdown("---")
                st.markdown("### Explicación y Fórmula")
                st.markdown("""
                La **deuda neta** representa la deuda total descontando el efectivo disponible, reflejando lo que realmente se debe financiar con recursos externos.

                El **costo de la deuda** se ajusta con el beneficio fiscal que representa el poder deducir intereses.

                Estas métricas permiten valorar si es más conveniente financiar con deuda o capital, dependiendo de la tasa efectiva que se obtiene.

                **Fórmulas utilizadas:**

                $$
                K_d = K_{deuda} \\cdot (1 - T)
                $$

                $$
                Deuda\\ Neta = Deuda\\ Total - Efectivo
                $$

                Donde:

                - $K_{deuda}$ = Tasa de interés nominal sobre la deuda  
                - $T$ = Tasa de impuesto corporativo  
                - $Efectivo$ = Saldo en bancos disponible
                """)

    elif selected == 'BALANCE':
        
        def limpiar_valores(valor):
            if isinstance(valor, str):
                valor = valor.replace('$', '').replace(',', '').strip()
                if valor in ['-', '', '–', '—']:
                    return 0.0
                try:
                    return float(valor)
                except ValueError:
                    return 0.0
            return float(valor)
        st.markdown("<h2 style='text-align: center;'>Análisis balance</h2>", unsafe_allow_html=True)
        st.markdown("---")
        sec_ba = option_menu(
            "Cálculos Financieros",
            ["Balance General", "Análisis ratios"],
            icons=["graph-up-arrow", "percent"],
            orientation="horizontal"
        )
        if sec_ba == "Balance General":

            st.markdown("## Balance General Comparativo ESGARI")
            st.markdown("En miles de MXN")

            df = df_balance.copy()


            df['NETO 2025'] = df['NETO 2025'].apply(limpiar_valores)
            df['NETO 2024'] = df['NETO 2024'].apply(limpiar_valores)

            # Calcular % cambio
            df["% CAMBIO"] = np.where(
                df["NETO 2024"] == 0,
                0,
                ((df["NETO 2025"] - df["NETO 2024"]) / df["NETO 2024"]) * 100
            )

            # Agrupar por sección
            secciones = df["Clasificacion"].unique()
            col1, col2 = st.columns(2)
            for seccion in secciones:
                if seccion == 'ACTIVO':
                    s = col1
                else:
                    s = col2
                s.markdown(f"### {seccion.title()}")
                df_sec = df[df["Clasificacion"] == seccion]

                categorias = df_sec["Categoria"].unique()
                for cat in categorias:
                    s.markdown(f"#### {cat.title()}")
                    df_cat = df_sec[df_sec["Categoria"] == cat]

                    s.dataframe(
                        df_cat[["CUENTA", "NETO 2025", "NETO 2024", "% CAMBIO"]]
                        .style
                        .format({
                            "NETO 2025": "${:,.0f}",
                            "NETO 2024": "${:,.0f}",
                            "% CAMBIO": "{:+.1f}%",
                        })
                        .applymap(lambda x: "color: red" if isinstance(x, float) and x < 0 else "color: green", subset=["% CAMBIO"])
                    )

            st.markdown("---")
            st.markdown("### Explicación")
            st.markdown("""
            Este balance general comparativo muestra los cambios entre los ejercicios 2025 y 2024.

            - **Columna "NETO 2025"**: Datos proyectados o reales del ejercicio 2025.
            - **Columna "NETO 2024"**: Datos históricos del ejercicio anterior.
            - **Columna "% CAMBIO"**: Variación porcentual entre ambos periodos.

            El análisis permite identificar:
            - Incrementos o reducciones en activos y pasivos clave.
            - Tendencias en financiamiento y rentabilidad.
            - Cambios estructurales importantes en el capital contable.

            > Un cambio positivo en activos o capital puede indicar fortalecimiento, mientras que un aumento en pasivos puede requerir análisis adicional.
            """)
        elif sec_ba == "Análisis ratios":
            st.markdown("## 📊 Análisis de Ratios Financieros Comparativos")
            df = df_balance.copy()

            # Limpieza
            df['NETO 2025'] = df['NETO 2025'].apply(limpiar_valores)
            df['NETO 2024'] = df['NETO 2024'].apply(limpiar_valores)

            # Función para buscar valores por categoría
            def buscar_valor(categoria, year):
                try:
                    return df[df['Categoria'].str.upper() == categoria.upper()][f'NETO {year}'].sum()
                except:
                    return 0.0

            # Diccionario con claves = nombres de ratios y fórmulas
            ratio_definiciones = {
                "Razón Circulante": lambda a, p: a / p if p else 0,
                "Endeudamiento": lambda p, a: p / a if a else 0,
                "Autonomía Financiera": lambda c, a: c / a if a else 0,
                "Pasivo / Capital": lambda p, c: p / c if c else 0,
                "Capital / Pasivo Total": lambda c, p: c / p if p else 0,
                "Activo / Capital": lambda a, c: a / c if c else 0,
            }

            # Valores base
            vals = {
                'ACTIVO': {
                    2025: buscar_valor('TOTAL ACTIVO', 2025),
                    2024: buscar_valor('TOTAL ACTIVO', 2024)
                },
                'PASIVO': {
                    2025: buscar_valor('TOTAL PASIVO', 2025),
                    2024: buscar_valor('TOTAL PASIVO', 2024)
                },
                'CAPITAL': {
                    2025: buscar_valor('TOTAL CAPITAL CONTABLE', 2025),
                    2024: buscar_valor('TOTAL CAPITAL CONTABLE', 2024)
                },
                'ACTIVO CIRCULANTE': {
                    2025: buscar_valor('TOTAL ACTIVO CIRCULANTE', 2025),
                    2024: buscar_valor('TOTAL ACTIVO CIRCULANTE', 2024)
                },
                'PASIVO CP': {
                    2025: buscar_valor('TOTAL PASIVO CORTO PLAZO', 2025),
                    2024: buscar_valor('TOTAL PASIVO CORTO PLAZO', 2024)
                }
            }

            # Cálculo de ratios para ambos años
            resultados = []
            for nombre, formula in ratio_definiciones.items():
                if "Circulante" in nombre:
                    v25 = formula(vals['ACTIVO CIRCULANTE'][2025], vals['PASIVO CP'][2025])
                    v24 = formula(vals['ACTIVO CIRCULANTE'][2024], vals['PASIVO CP'][2024])
                elif "Endeudamiento" in nombre:
                    v25 = formula(vals['PASIVO'][2025], vals['ACTIVO'][2025])
                    v24 = formula(vals['PASIVO'][2024], vals['ACTIVO'][2024])
                elif "Autonomía" in nombre:
                    v25 = formula(vals['CAPITAL'][2025], vals['ACTIVO'][2025])
                    v24 = formula(vals['CAPITAL'][2024], vals['ACTIVO'][2024])
                elif "Pasivo / Capital" in nombre:
                    v25 = formula(vals['PASIVO'][2025], vals['CAPITAL'][2025])
                    v24 = formula(vals['PASIVO'][2024], vals['CAPITAL'][2024])
                elif "Capital / Pasivo" in nombre:
                    v25 = formula(vals['CAPITAL'][2025], vals['PASIVO'][2025])
                    v24 = formula(vals['CAPITAL'][2024], vals['PASIVO'][2024])
                elif "Activo / Capital" in nombre:
                    v25 = formula(vals['ACTIVO'][2025], vals['CAPITAL'][2025])
                    v24 = formula(vals['ACTIVO'][2024], vals['CAPITAL'][2024])
                else:
                    v25 = v24 = 0
                delta = v25 - v24
                resultados.append({"Ratio": nombre, "2025": v25, "2024": v24, "Δ": delta})

            df_ratios = pd.DataFrame(resultados)

            # Mostrar métricas individuales
            st.markdown("### 📈 Comparativo de ratios financieros clave")
            for i, row in df_ratios.iterrows():
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(row["Ratio"], f"{row['2025']:.2f}", delta=f"{row['Δ']:+.2f}")
                with col2:
                    st.metric(f"**2024:** ", f"{row['2024']:.2f}")
                with col3:
                    st.write(f"""
                        {row['Ratio']}:
                        {({
                            'Razón Circulante': "Capacidad para cubrir pasivos de corto plazo con activos líquidos.",
                            'Endeudamiento': "Porción de activos financiada por deuda.",
                            'Autonomía Financiera': "Grado de independencia financiera frente a terceros.",
                            'Pasivo / Capital': "Nivel de apalancamiento sobre capital propio.",
                            'Capital / Pasivo Total': "Capacidad de capital propio frente a obligaciones.",
                            'Activo / Capital': "Multiplicador del capital invertido en activos."
                        })[row['Ratio']]}
                    """)

            # Visualización interactiva con Plotly

            st.markdown("### 📊 Evolución gráfica comparativa")
            fig = go.Figure()
            fig.add_trace(go.Bar(x=df_ratios["Ratio"], y=df_ratios["2024"], name='2024'))
            fig.add_trace(go.Bar(x=df_ratios["Ratio"], y=df_ratios["2025"], name='2025'))
            fig.update_layout(
                barmode='group',
                title="Ratios Financieros: Comparación 2025 vs 2024",
                yaxis_title="Valor del Ratio",
                xaxis_title="Ratio",
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)
