import dash
from dash import dcc, html, Input, Output
import dash_table
import ccxt
import time

SYMBOLS = ["ACTUSDT","VIRTUALUSDT","PUMPUSDT","ZORAUSDT","COALUSDT","TURBOUSDT","MOGUSDT","BRETTUSDT","PEPEUSDT","BONKUSDT","WIFUSDT","FLOKIUSDT","SHIBUSDT","1000SATSUSDT","BOMEUSDT","SLERFUSDT","MEWUSDT","POPCATUSDT","NEIROUSDT","GIGAUSDT"]

app = dash.Dash(__name__)
app.title = "20币极简版"

app.layout = html.Div(style={'backgroundColor':'#111','color':'#fff'}, children=[
    html.H1("20币实时面板", style={'textAlign':'center'}),
    dash_table.DataTable(id='table', columns=[{"name":"币种","id":"s"},{"name":"最新价","id":"p"},{"name":"24H涨跌","id":"c"},{"name":"24H量M","id":"v"}],
        style_cell={'backgroundColor':'#222','color':'#fff','textAlign':'center'}),
    dcc.Interval(interval=8000, n_intervals=0)
])

@app.callback(Output('table','data'), Input('Interval','n_intervals'))
def update(n):
    ex = ccxt.binance()
    rows = []
    for s in SYMBOLS:
        try:
            t = ex.fetch_ticker(s)
            rows.append({"s":s.replace("USDT","/USDT"),"p":f"{t['last']:.6f}".rstrip('0').rstrip('.'),"c":f"{t['percentage']:+.2f}%","v":f"{t['quoteVolume']/1e6:.1f}"})
        except:
            rows.append({"s":s,"p":"—","c":"—","v":"—"})
    return rows

if __name__ == '__main__':
    import os
    app.run_server(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
