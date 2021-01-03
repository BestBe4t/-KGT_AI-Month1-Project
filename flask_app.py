#-*-coding:utf-8 -*-
#*******************************
# made by DuckBill
#*******************************
################################ import libaray ################################
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from flask import Flask
from data import dia, price_per_carat, price_combination, price_predict, standard_set_price
import plotly.graph_objects as go
import pandas as pd

################################ Define apps and value ################################
app = Flask(__name__)

base_app = dash.Dash(__name__, server=app, external_stylesheets=[dbc.themes.BOOTSTRAP], url_base_pathname='/')
base_app.title='DIA'

dia_df = pd.DataFrame(eval(dia()))
rank_list = standard_set_price()
rank_list.remove('price')

################################ Define css ################################
CONTENTS_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

RANK_BOARD_STYLE = {
    1: {
        "background-image": "url('static/image/ranking_background1.png')",
        "background-repeat": "no-repeat",
        "width": "10rem",
        "height": "28px"
    },
    2: {
        "background-image": "url('static/image/ranking_background2.png')",
        "background-repeat": "no-repeat",
        "width": "10rem",
        "height": "28px"
    },
    3: {
        "background-image": "url('static/image/ranking_background3.png')",
        "background-repeat": "no-repeat",
        "width": "10rem",
        "height": "28px"
    },
    4: {
        "background-image": "url('static/image/ranking_background4.png')",
        "background-repeat": "no-repeat",
        "width": "10rem",
        "height": "28px"
    }
}

RANK_CONTENT_STYLE = {
    1: {
        "color": "balck",
        "margin-left": "8px",
    },
    2: {
        "color": "balck",
        "margin-left": "8px",
        "margin-top": "8px",
    },
    3: {
        "color": "balck",
        "margin-left": "8px",
        "margin-top": "8px",
    },
    4: {
        "color": "balck",
        "margin-left": "8px",
        "margin-top": "8px",
    }
}

sidebar = html.Div(
    [
        html.P(
            "Menu", className="lead"
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Buy", href="/buy/", active="exact"),
                dbc.NavLink("Sell", href="/sell/", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


################################ main_app ################################
main_app_layout = html.Div(children =[
    sidebar, 
    html.Div(children=[
        html.Header(
                style={"textAlign": "center", "paddingTop": "50px"},
                children=[
                    html.H1("DIAMOND", 
                    style={
                        "fontSize": 40,
                        "font-family": "'Brush Script MT', cursive"
                        }
                    )
                ],
            ),
        html.H1('다이아 설명'),
        html.Hr(),
        html.Div(children = 
            dcc.Markdown(children = 
                '''
                ## 컷 
                ---
                - 대칭평가(빛이 돌 각 부분에서 고르게 얻으려면 각 연마면의 대칭성이 고도(8회 대칭)이여야 한다.)  
                - 플리쉬 평가(돌 내외부의 반사율을 높이기 위해 공손한 연마 여기에 전체 평면이 실현되지 않으면 안된다.)  
                - Excellent, Premium, Very Good, Good, Fair 순  
                ![cut](static/image/dia_cut.jpg)
                ''',
            style={
                "margin-top" : "8px"
            })
        ),
        html.Div(children = 
            dcc.Markdown(children = 
                '''
                ## 색  
                ---
                - D = 흰색, J=노란색 D ~ J순  
                ![color](static/image/dia_color.png)
                '''
            )
        ),
        html.Div(children = 
            dcc.Markdown(children = 
            '''
            ## 투명도
            ---
            - 흠의 크기, 개수, 위치, 눈 용이성, 성격등을 10배율 환경에서 관찰하여 빛의 손상 정도로 판별
            - I1 (worst), SI2, SI1, VS2, VS1, VVS2, VVS1, IF (best)  
            ![clarity](static/image/dia_clarity.jpg)
            '''
            )
        ),
        html.Hr(),
        html.H2("카테고리별 보유 현황:"),
        dcc.Dropdown(
            id='values', 
            value='carat', 
            options=[{'value': x, 'label': x} 
                    for x in ['carat', 'cut', 'color', 'clarity']],
            clearable=False
        ),

        dcc.Graph(
            id = 'pie-chart',
        ),
        html.Hr(),
        html.H2("다이아 몬드 가격 결정 요소"),
        html.Div(id = 'ranking',
            children=[
                html.Div(
                    children=[
                        dcc.Markdown(
                            children = '**' + str(idx + 1) + '등**　　' + str(k),
                            style=RANK_CONTENT_STYLE[idx + 1]
                            )
                    ],
                    style=RANK_BOARD_STYLE[idx + 1]
                ) for idx, k in enumerate(rank_list)
            ]
        ),
        html.Hr(),
        html.H2("캐럿당 가격"),
        dbc.Row(
            [
                dbc.Col(html.P(id='output-upper'), width="auto"),
                dbc.Col(dbc.Badge("이상", color="primary", className="mr-1"), width="auto"),
                dbc.Col(html.P(id='output-lower'), width="auto"),
                dbc.Col(dbc.Badge("이하", color="primary", className="mr-1"), width="auto")
            ]
        ),
        html.Div(
            children=[
                dbc.Spinner(
                    children = [dcc.Graph(id='price-per-carat')], 
                    id="loading-output", 
                    size='sm'
                )                
            ]
        ),
        dcc.RangeSlider(
            id='carat-slider',
            min=0.2,
            max=5.01,
            step=0.01,
            value=[1.0, 1.5]
        ),
        html.Div(id='output-container-range-slider')
    ],
    style=CONTENTS_STYLE)
])


################################ main_app_callback ################################
# 보유 다이아 현황
@base_app.callback(
    Output("pie-chart", "figure"),
    Input("values", "value")
    )
def generate_chart(values):
    labels = dia_df[values].unique().tolist()
    if values == 'carat':
        for i in range(len(labels)):
            if i == 3:
                labels[i] = str(labels[i]) + '캐럿 이상'
            else:
                labels[i] = str(labels[i]) + '캐럿 미만'
    values = dia_df.groupby(values).size()
    
    fig = go.Figure(data=[go.Pie(labels = labels, values = values, textinfo = 'label+percent',
                             insidetextorientation='radial')])
    return fig

# 캐럿당 가격
@base_app.callback(
    Output("price-per-carat", "figure"),
    [Input("carat-slider", "value")])
def generate_ppc(value):
    new_df, mean_list = price_per_carat(value[0], value[1])
    d_x = new_df['carat']
    d_y = new_df['price']
    m_x = mean_list.keys().tolist()
    m_y = mean_list.values
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=d_x, y=d_y, mode='markers', name='보유 다이아'))
    fig.add_trace(go.Scatter(x=m_x, y=m_y, mode='lines+markers', name='캐럿 평균'))

    fig.update_layout(
        xaxis_title="carat", 
        yaxis_title="price"
    )
    
    
    return fig

# 캐럿당 가격 범위
@base_app.callback(	
    Output('output-upper', 'children'),	
    Output('output-lower', 'children'),	
    [Input('carat-slider', 'value')])	
def update_output(value):	
    return value[0], value[1]
    

################################ buy_app ################################
buy_app_layout = html.Div(children =[
    sidebar, 

    html.Div(
        children = [
            html.Div(
                children=[
                    html.H2('검색하실 가격을 입력해 주세요(달러)',
                    style={
                        "margin-left": "10px",
                        "margin-top": "10px",
                    }),
                    dcc.Checklist(
                        options=[
                            {'label': '이상　', 'value': 'num1'},
                            {'label': '이하　', 'value': 'num2'}
                        ],
                        id='up_down',
                        style={
                            "margin-left": "10px"
                        }
                    )
                ]
            ),
            html.Div(id='num_input_box'),
            html.Hr(),
            dcc.Loading(
                id="can_by_value",
                type="dot",
                children=[
                    html.H4('검색 결과가 없습니다.', style={"margin-left": "10px"})
                    ],
                style={
                    "margin-left": "10px",
                    "margin-top": "15px"
                }
            )
        ],
        style = CONTENTS_STYLE,
    )
])


################################ buy_app_callback ################################
# 일정 금액 사이에 살 수 있는 다이아 리스트
@base_app.callback(
    Output('can_by_value', 'children'),
    Input('num1', 'value'),
    Input('num2', 'value')
)
def update_table(num1, num2):
    if (not num1 and not num2) or (num1 == 0 or num2 == 0):
        return html.H4('검색 결과가 없습니다.', style={"margin-left": "10px"})
    
    if (num1 and not num2):
        num2 = 18824
    elif (not num1 and num2):
        num1 = 0
    
    return dbc.Table.from_dataframe(price_combination(num1, num2), striped=True, bordered=True, hover=True, size='sm')


# 이상 이하 입력박스 비-활성화
@base_app.callback(
    Output('num_input_box', 'children'),
    Input('up_down', 'value')
)
def up_down_input_box(check_list):
    if not check_list: 
        return html.Div()

    if 'num2' in check_list and 'num1' in check_list:
        return html.Div(
                children=[
                    dbc.Row([
                        dbc.Col(html.Label('이상'), width=2),
                        dbc.Col(html.Label('이하', style={"margin-left": "5px"}), width=2)
                    ]),
                    dbc.Row([
                        dbc.Col(dcc.Input(type='number', value=0, max=18824, min=325, id='num1'), width=2),
                        dbc.Col(dcc.Input(type='number', value=0, max=18824, min=325, id='num2', style={"margin-left": "5px"}), width=2)
                    ]),
                    dbc.Row([
                        dbc.Col(dbc.FormText("최소 325", color="secondary"), width=2),
                        dbc.Col(dbc.FormText("최대 18824", color="secondary", style={"margin-left": "5px"}), width=2)
                    ])
                ],
                style={"margin-left": "10px"}
            )
    elif 'num1' in check_list:
        return html.Div(
                children=[
                    dbc.Row([
                        dbc.Col(html.Label('이상'), width=2)
                    ]),
                    dbc.Row([
                        dbc.Col(dcc.Input(type='number', value=0, max=18824, min=325, id='num1', style={"margin-left": "5px"}), width=2)
                    ]),
                    dbc.Row([
                        dbc.Col(dbc.FormText(
                            "최소 325", color="secondary"
                        ), width=2)
                    ]),
                    dcc.Input(type="hidden", id='num2', value=18824)
                ],
                style={"margin-left": "10px"}
            )
    elif 'num2' in check_list:
        return html.Div(
                children=[     
                    dbc.Row([               
                        dbc.Col(html.Label('이하'), width=2)
                    ]),
                    dbc.Row([
                        dbc.Col(dcc.Input(type='number', value=0, max=18824, min=325, id='num2', style={"margin-left": "5px"}), width=2)
                    ]),
                    dbc.Row([
                        dbc.Col(dbc.FormText(
                            "최대 18824", color="secondary"
                        ), width=2)
                    ]),
                    dcc.Input(type="hidden", id='num1', value=0)
                ],
                style={"margin-left": "10px"}
            )


################################ sell_app ################################
sell_app_layout = html.Div(children =[
    sidebar, 
    html.Div(children=[
        html.H2('카테고리를 선택하고 값을 입력하세요', style={"margin-left": "10px"}),
        html.Hr(),
        dcc.Dropdown(
            options=[
                {'label': 'carat', 'value': 'carat'},
                {'label': 'color', 'value': 'color'},
                {'label': 'cut', 'value': 'cut'},
                {'label': 'clarity', 'value': 'clarity'}
            ],
            multi=True,
            id='values',
            style={
                "margin-top": "5px"
                }
        ),
        html.Div(id='options',style={"margin-left": "10px", "margin-top": "5px"}),
        html.Button('search', id='search-btn', n_clicks=0, style={"margin-left": "10px", "margin-top": "5px"}),
        html.Hr(),
        html.Div(id='sell_price', style={"margin-left": "10px"})
    ],
    style=CONTENTS_STYLE)

])


################################ sell_app_callback ################################
# 옵션 체크 (입력 값 검사)
@base_app.callback(
    Output('options', 'children'),
    Input('values', 'value')
)
def check_options(values):
    children = []
    if values:
        for value in values:
            if value == 'cut':
                children.append(html.Label('cut'))
                children.append(
                    dcc.Dropdown(options=[
                        {'label': 'Excellent', 'value': 'Excellent'},
                        {'label': 'Premium', 'value': 'Premium'},
                        {'label': 'Very Good', 'value': 'Very Good'},
                        {'label': 'Good', 'value': 'Good'},
                        {'label': 'Fair', 'value': 'Fair'}
                    ], id='cut')
                )
                children.append(html.Br())
                
            if value == 'carat':
                children.append(html.Label('carat'))
                children.append(html.Br())
                children.append(dcc.Input(type='number', id='carat'))
                children.append(html.Br())
                
            if value == 'color':
                children.append(html.Label('color'))
                children.append(
                    dcc.Dropdown(options=[
                        {'label': 'D(투명)', 'value': 'D'},
                        {'label': 'E', 'value': 'E'},
                        {'label': 'F', 'value': 'F'},
                        {'label': 'G', 'value': 'G'},
                        {'label': 'H', 'value': 'H'},
                        {'label': 'I', 'value': 'I'},
                        {'label': 'J(노랑)', 'value': 'J'}
                    ], id='color')
                )
                children.append(html.Br())
                
            if value == 'clarity':
                children.append(html.Label('clarity'))
                children.append(
                    dcc.Dropdown(options=[
                        {'label': 'IF', 'value': 'IF'},
                        {'label': 'VVS1', 'value': 'VVS1'},
                        {'label': 'VVS2', 'value': 'VVS2'},
                        {'label': 'VS1', 'value': 'VS1'},
                        {'label': 'VS2', 'value': 'VS2'},
                        {'label': 'SI1', 'value': 'SI1'},
                        {'label': 'SI2', 'value': 'SI2'},
                        {'label': 'I1', 'value': 'I1'}
                    ], id='clarity')
                )
                children.append(html.Br())
    
    return children

# 검색
@base_app.callback(
    Output('sell_price', 'children'),
    Input('search-btn', 'n_clicks'),
    State('values', 'value'),
    State('options', 'children')
)
def predict_sell_price(n_clicks, values, options):
    option_dic = {
        'carat': '0',
        'cut': 'NONE',
        'color': 'NONE',
        'clarity': 'NONE'
    }    
    cnt = 1
    if values:
        for value in values:
            option_dic[value] = options[cnt]['props'].get('value', 'NONE')
            if value == 'carat':
                cnt += 1
            cnt += 3
            
    return price_predict(option_dic)


################################ base_app.layout ################################
base_app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-contents')
])


################################ share_callback ################################
@base_app.callback(
    Output('page-contents', 'children'),
    Input("url", "pathname")
)
def move_page(pathname):
    if pathname == '/sell/':
        return sell_app_layout
    elif pathname == '/buy/':
        return buy_app_layout
    else:
        return main_app_layout


if __name__ == '__main__':
    app.run_server(debug=True)