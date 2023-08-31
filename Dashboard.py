# Importación de bibliotecas
import yfinance as yf
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

# Configuración de fechas
end_date = datetime.now()
start_date = end_date - timedelta(days=5*365)

# Descarga de datos
tickers = [
    'SQM', 'BCH', 'BSANTANDER.SN', 'CENCOSUD.SN', 'COPEC.SN', 'ENELAM.SN',
    'BCI.SN', 'CMPC.SN', 'FALABELLA.SN', 'ENELCHILE.SN', 'COLBUN.SN',
    'PARAUCO.SN', 'VAPORES.SN', 'AGUAS-A.SN', 'ANDINA-B.SN', 'CCU.SN',
    'QUINENCO.SN', 'CENCOSHOPP.SN', 'LTM.SN', 'CONCHATORO.SN', 'ENTEL.SN',
    'MALLPLAZA.SN', 'CAP.SN', 'ECL.SN', 'ITAUCL.SN', 'ORO-BLANCO.SN',
    'IAM.SN', 'SMU.SN', 'RIPLEY.SN'
]
prices = yf.download(tickers, start=start_date, end=end_date, interval='1wk')['Adj Close']
prices.drop(columns=['CENCOSHOPP.SN'], inplace=True)  # Eliminando el ticker CENCOSHOPP.SN

# Iniciando la aplicación de Dash
app = dash.Dash(__name__)

# Estructura de la aplicación
app.layout = html.Div([
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in prices.columns],
        value=prices.columns[0],  # valor por defecto
        multi=False  # no permitir selecciones múltiples
    ),
    dcc.Graph(id='time-series-plot'),
    dcc.Graph(id='return-distribution-plot')
])

# Definición de las callbacks para actualizar los gráficos
@app.callback(
    [Output('time-series-plot', 'figure'),
     Output('return-distribution-plot', 'figure')],
    [Input('ticker-dropdown', 'value')]
)
def update_graphs(selected_ticker):
    # Gráfico de serie temporal
    time_series = go.Figure()
    time_series.add_trace(go.Scatter(x=prices.index, y=prices[selected_ticker], mode='lines', name='Precio de cierre'))
    time_series.update_layout(title=f"Precio de cierre a lo largo del tiempo para {selected_ticker}",
                              xaxis_title="Fecha", yaxis_title="Precio")

    # Gráfico de distribución de retornos
    returns = prices[selected_ticker].pct_change().dropna()
    distribution = go.Figure()
    distribution.add_trace(go.Histogram(x=returns, name='Retornos'))
    distribution.update_layout(title=f"Distribución de retornos para {selected_ticker}",
                               xaxis_title="Retorno", yaxis_title="Frecuencia")

    return time_series, distribution


if __name__ == '__main__':
    app.run_server(debug=True)
