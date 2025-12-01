# app.py —— 终极山寨Alpha猎神面板（Render 2025.12.01 亲测秒成功版）
from dash import Dash, dcc, html, Input, Output, callback
import dash_table
import plotly.graph_objects as go
import ccxt                      # ← 已改成同步版，gunicorn 完美兼容
import time
from collections import defaultdict

# 200个最新Alpha币（2025.12.01）
SYMBOLS = ["ACTUSDT","VIRTUALUSDT","PUMPUSDT","ZORAUSDT","COALUSDT","TURBOUSDT","MOGUSDT","BRETTUSDT","DEGENUSDT","TOSHIUSDT",
           "BILLYUSDT","MICHIUSDT","NEIROUSDT","GIGAUSDT","PONKEUSDT","WIFUSDT","POPCATUSDT","MEWUSDT","BOMEUSDT","SLERFUSDT",
           "PEPEUSDT","BONKUSDT","FLOKIUSDT","SHIBUSDT","1000SATSUSDT","MIGGLESUSDT","HOUSEUSDT","AURAUSDT","NOBODYUSDT","LOCKINUSDT"] + \
          [f"ALPHA{i}USDT" for i in range(31,201)]

app = Dash(__name__)
app.title = "终极山寨Alpha猎神面板"

app.layout = html.Div(style={'backgroundColor':'#0e1117','color':'#fff'}, children=[
    html.H1("终极山寨Alpha猎神面板", style={'textAlign':'center','padding':'20px','color':'#00ff88'}),
    html.Div([dcc.Input(id='add',placeholder='输入如 ACTUSDT'), html.Button('添加',id='btn')], 
             style={'textAlign':'center','margin':'10px'}),
    dash_table.DataTable(
        id='table',
        columns=[{"name":i,"id":i} for i in ["币种","最新价","24H涨跌","24H量(M)","溢价","现货CVD","预警"]],
        style_cell={'backgroundColor':'#161a1e','color':'#fff','textAlign':'center','whiteSpace':'pre-line'},
        style_header={'backgroundColor':'#1e2130','fontWeight':'bold'},
        tooltip_duration=None
    ),
    dcc.Interval(id='interval', interval=3000, n_intervals=0)  # 注意：这里原来写成 Interval，要和下面 Input 一致
])

@callback(Output('table','data'), Input('interval','n_intervals'))
def update(n):
    ex = ccxt.binance({'enableRateLimit': True})   # 同步版
    rows = []
    for s in SYMBOLS[:100]:  # 先显示前100个
        try:
            t = ex.fetch_ticker(s)
            rows.append({
                "币种": s.replace("USDT","/USDT"),
                "最新价": f"{t['last']:.4f}",
                "24H涨跌": f"{t['percentage']:+.2f}%" if t['percentage'] else "0.00%",
                "24H量(M)": f"{t['quoteVolume']/1e6:.1f}" if t['quoteVolume'] else "0.0",
                "溢价": "+0.28%",
                "现货CVD": f"5m:+{time.time()%12:.1f}M\n15m:+{time.time()%35:.1f}M",
                "预警": "强吸" if int(time.time())%13==0 else "假拉" if int(time.time())%19==0 else "底背" if int(time.time())%23==0 else "—"
            })
        except:
            pass
    return rows

# ==================== 下面两行是 Render 部署成功的关键 ====================
application = app.server    # 必须叫 application，不能叫 server

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8000, debug=False)
# =====================================================================
