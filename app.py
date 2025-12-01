# -*- coding: utf-8 -*-
from dash import Dash, html, dash_table, Input, Output, dcc
import ccxt
import time

# 20 个最热 Alpha 币（后面你随便加到 200）
SYMBOLS = [
    "ACTUSDT","VIRTUALUSDT","PUMPUSDT","ZORAUSDT","COALUSDT",
    "TURBOUSDT","MOGUSDT","BRETTUSDT","PEPEUSDT","BONKUSDT",
    "WIFUSDT","FLOKIUSDT","SHIBUSDT","1000SATSUSDT","BOMEUSDT",
    "SLERFUSDT","MEWUSDT","POPCATUSDT","NEIROUSDT","GIGAUSDT"
]

app = Dash(__name__)
app.title = "终极山寨Alpha猎神面板"

app.layout = html.Div(style={'backgroundColor':'#0e1117','color':'#fff','fontFamily':'Arial'}, children=[
    html.H1("20币实时面板（Render版）", style={'textAlign':'center','padding':'20px'}),
    dash_table.DataTable(
        id='table',
        columns=[
            {"name":"币种","id":"sym"},
            {"name":"最新价","id":"price"},
            {"name":"24H涨跌","id":"chg"},
            {"name":"24H量(M)","id":"vol"}
        ],
        style_cell={'backgroundColor':'#161a1e','color':'#fff','textAlign':'center','border':'1px solid #323546'},
        style_header={'backgroundColor':'#1e2130','fontWeight':'bold'}
    ),
    dcc.Interval(id='interval', interval=8000, n_intervals=0)
])

@app.callback(Output('table','data'), Input('interval','n_intervals'))
def update(n):
    ex = ccxt.binance()
    rows = []
    for s in SYMBOLS:
        try:
            t = ex.fetch_ticker(s)
            rows.append({
                "sym": s.replace("USDT","/USDT"),
                "price": f"{t['last']:.6f}".rstrip('0').rstrip('.'),
                "chg": f"{t['percentage']:+.2f}%",
                "vol": f"{t['quoteVolume']/1e6:.1f}"
            })
        except:
            rows.append({"sym":s,"price":"—","chg":"—","vol":"—"})
    return rows

# 关键两行：Render 必须有这一行！
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
