import dash
import pandas as pd
import numpy as np

import flask
import cx_Oracle as cx
import plotly.graph_objs as go

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State

import config

app = dash.Dash(__name__, requests_pathname_prefix='/app2/', external_stylesheets = [dbc.themes.BOOTSTRAP])

con = cx.connect(config.CONN_STR)

sql = ''' 
        SELECT 
            DISTINCT REGION_CODE 
        FROM  
            XM_BRANCHS 
        WHERE 
            STATUS LIKE 'VALID' 
        ORDER BY
            REGION_CODE ASC
     '''

df = pd.read_sql_query(sql, con)
df['COPY_REGION_CODE'] = df['REGION_CODE']
df.loc[len(df)] = 'ALL'
df['COPY_REGION_CODE'].iloc[-1] = ''

row = html.Div([
                dbc.Row([
                        dbc.Col([html.H6('Region', style = {'font-weight':'bold','textAlign':'center'}),
                                  dcc.Dropdown(
                                    id ='region-dropdown',
                                    options = [{'label': k, 'value' : v} for k, v in zip(df['REGION_CODE'], df['COPY_REGION_CODE'])],
                                    style = {'font-weight' : 'bold'}
                                   )
                                 ]),
                       
                        dbc.Col([html.H6('Controlling', style = {'font-weight':'bold','textAlign':'center'}),
                                 dcc.Dropdown(
                                    id = 'controlling-dropdown',
                                    style = {'font-weight':'bold'}
                                   )
                               ]),
                       
                        dbc.Col([html.H6('Branch', style = {'font-weight':'bold','textAlign':'center'}),
                                 dcc.Dropdown(
                                    id = 'branch-dropdown',
                                    style = {'font-weight':'bold'}
                                   )
                               ]),
                         
                        dbc.Col([html.H6('Division', style = {'font-weight':'bold','textAlign':'center'}),
                                 dcc.Dropdown(
                                    id = 'division-dropdown',
                                    style = {'font-weight':'bold'}
                                   )
                               ]),
                         
                        dbc.Col([html.H6('Year', style = {'font-weight':'bold','textAlign':'center'}),
                                 dcc.Dropdown(
                                    id = 'year-dropdown',
                                    style = {'font-weight':'bold'}
                                    )
                              ]),

                        dbc.Col([html.H6('Month', style = {'font-weight':'bold','textAlign':'center'}),
                                 dcc.Dropdown(
                                     id = 'month-dropdown',
                                     style = {'font-weight':'bold'}
                                    )
                               ])
                        ]),#dbc.row1
                html.Br(),
                dbc.Row([
                         dbc.Col([
                                 html.Button(
                                              'Submit',
                                              id = 'submit_button',
                                              type = 'submit',
                                              style = {'width':'100px', 'height':'34.5px', 'display':'inline-block',\
                                                       'margin-left':'500px', 'background-color': '#ffffff',\
                                                       'font-weight':'bold', 'border-radius':'4px'}
                                            )
                                 ])
                       ])#dbc.row2
                 ])#html.div

app.layout = html.Div([
                       html.Br(),
                       html.Div([
                                 html.H3('Business Dashboard - Prosperity Report')
                                ],style={'marginBottom' : '25px', 'marginTop' : '0px', 'textAlign' : 'center'}),
                       html.Br(),
                       html.Div([
                                 dbc.Container(children=[row])
                                ]),
                       html.Br(),
                       html.Div([
                                dcc.Tabs([
                                           dcc.Tab(label = 'Month Wise Growth % \n (LY Vs CY)',
                                                children = [
                                                       html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-1'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '10px','border-style': 'groove'}
                                                               ),
                                                       html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-2'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '10px','border-style': 'groove'}
                                                               ),
                                                       
                                                       html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-3'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '-5px','border-style': 'groove'}
                                                               ),
                                                       html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-4'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '-5px','border-style': 'groove'}
                                                               ),
                                                       
                                                     ], style = {'textAlign':'center','font-weight':'bold'}
                                                 ),
                                           dcc.Tab(label = 'Region wise Growth % \n (LY Vs CY)',
                                                children = [
                                                       html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-5'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '10px','border-style': 'groove'}
                                                               ),
                                                       html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-6'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '10px','border-style': 'groove'}
                                                               ),
                                                       
                                                       html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-7'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '-5px','border-style': 'groove'}
                                                               ),
                                                       html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-8'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '-5px','border-style': 'groove'}
                                                               ),
                                                       
                                                     ], style = {'textAlign':'center','font-weight':'bold'}
                                                 ),
                                           dcc.Tab(label = 'Region Wise FTM (LY Vs CY)',
                                                children = [
                                                       html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-9'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '10px','border-style': 'groove'}
                                                               ),
                                                       html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-10'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '10px','border-style': 'groove'}
                                                               ),
                                                       
                                                      html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-11'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '-5px','border-style': 'groove'}
                                                               ),
                                                      html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-12'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '-5px','border-style': 'groove'}
                                                               ),
                                                       
                                                     ], style = {'textAlign':'center','font-weight':'bold'}
                                                 ),
                                            dcc.Tab(label = 'Region Wise CUM (LY Vs CY)',
                                                children = [
                                                       html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-9A'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '10px','border-style': 'groove'}
                                                               ),
                                                       html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-10A'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '10px','border-style': 'groove'}
                                                               ),
                                                       
                                                      html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-11A'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '-5px','border-style': 'groove'}
                                                               ),
                                                      html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-12A'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '-5px','border-style': 'groove'}
                                                               ),
                                                       
                                                     ], style = {'textAlign':'center','font-weight':'bold'}
                                                ),
                                           dcc.Tab(label = 'Month Wise Trend (CY)',
                                                children = [
                                                       html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-13'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '10px','border-style': 'groove'}
                                                               ),
                                                       html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-14'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '10px','border-style': 'groove'}
                                                               ),
                                                       
                                                      html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-15'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '-5px','border-style': 'groove'}
                                                               ),
                                                      html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-16'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '-5px','border-style': 'groove'}
                                                               ),
                                                      
                                                     ], style = {'textAlign':'center','font-weight':'bold'}
                                                 ),
                                           dcc.Tab(label = 'Region Wise Trend (CY)',
                                                children = [
                                                       html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-17'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '10px','border-style': 'groove'}
                                                               ),
                                                       html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-18'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '10px','border-style': 'groove'}
                                                               ),
                                                      
                                                       html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-19'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '-5px','border-style': 'groove'}
                                                               ),
                                                       html.Div([dcc.Loading(
                                                                 dcc.Graph(id = 'graph-20'))
                                                                ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                           'margin-top': '-5px','border-style': 'groove'}
                                                               ),
                                                      
                                                     ], style = {'textAlign':'center','font-weight':'bold'}
                                                 ),
                                            
                                           ]) #dcc.tabs
                                   ]),
                                   html.Br(),
                                   html.Div([
                                             html.A('Back to Index Page', href='/')
                                            ], style = {'textAlign':'center', 'color':'black'}
                                            ) 
                          ], style = {'width' : 'auto', 'background-color': '#f2f2f2'})

@app.callback(Output('controlling-dropdown', 'options'),[Input('region-dropdown', 'value')])
def set_controlling_options(selected_region):
    con = cx.connect(config.CONN_STR)
    sql = ''' SELECT 
                      DISTINCT CONTROLLING_CODE 
                FROM 
                     XM_BRANCHS 
                WHERE 
                     REGION_CODE = '%s' 
                     AND STATUS LIKE 'VALID' 
                ORDER BY
                    CONTROLLING_CODE ASC
            '''%(
                  selected_region
                )
    df = pd.read_sql_query(sql, con)
    df['COPY_CONTROLLING_CODE'] = df['CONTROLLING_CODE']
    df.loc[len(df)] = 'ALL'
    df['COPY_CONTROLLING_CODE'].iloc[-1] = ''
    return [{'label': k, 'value' : v} for k, v in zip(df['CONTROLLING_CODE'], df['COPY_CONTROLLING_CODE'])] 

@app.callback(Output('branch-dropdown', 'options'),[Input('controlling-dropdown', 'value')])
def set_branch_options(selected_controlling):
    con = cx.connect(config.CONN_STR)
    sql = ''' SELECT 
                      DISTINCT BRANCH_CODE 
                FROM 
                     XM_BRANCHS 
                WHERE 
                     CONTROLLING_CODE = '%s' 
                     AND STATUS LIKE 'VALID' 
                ORDER BY
                    BRANCH_CODE ASC
            '''%(
                  selected_controlling
                )
    df = pd.read_sql_query(sql, con)
    df['COPY_BRANCH_CODE'] = df['BRANCH_CODE']
    df.loc[len(df)] = 'ALL'
    df['COPY_BRANCH_CODE'].iloc[-1] = ''
    return [{'label': k, 'value' : v} for k, v in zip(df['BRANCH_CODE'], df['COPY_BRANCH_CODE'])] 

@app.callback(Output('division-dropdown', 'options'),[Input('branch-dropdown', 'value')])
def set_division_options(selected_division):
     dict_div = {'Surface':'21','Air':'22','ECOM':'23',\
                 'GTA':'24','RAIL':'25','AIR INTL':'26',\
                 'C2C':'27','ALL':''}
     return[{'label':l, 'value':m} for l, m in dict_div.items()]

@app.callback(Output('year-dropdown', 'options'),[Input('division-dropdown', 'value')])
def set_year_options(selected_month):
    return [{'label': y, 'value': y} for y in [ '2018','2019','2020','2021']]

@app.callback(Output('month-dropdown', 'options'),[Input('year-dropdown', 'value')])
def set_month_options(selected_branch):
    return [{'label' : x, 'value' : x} for x in [ '01','02','03',\
                                                  '04','05','06',\
                                                  '07','08','09',\
                                                  '10','11','12']
                                                ]
                                                
@app.callback(Output('graph-1','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])

def update_graph_1(n_clicks,value_1, value_2, value_3, value_4, value_5,\
                   value_6, value_7, value_8, value_9, value_10, value_11,\
                   value_12):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''SELECT
                        to_char(to_date(YEAR_MONTH_DAY,'YYYYMMDD'),'MON-YY') MONTHS
                        ,SUM(NVL(LYA_TOT_FRT,0)) LYF
                        ,SUM(NVL(TOT_FRT,0)) CYF
                FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL
                WHERE
                        REGION_CODE = NVL('%s',REGION_CODE)
                        AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                        AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                        AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                        AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                        BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'MM') IN ('01','02','03')
                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY'))-1)
                                    ELSE TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY') END
                                        AND last_day(TO_DATE('%s%s','YYYYMM')) 
                GROUP BY
                        YEAR_MONTH_DAY
                ORDER BY
                        to_date(MONTHS,'MON-YY')
             '''%(value_1, value_2, value_3, value_4, value_5,\
                  value_6, value_7, value_8, value_9, value_10, value_11,\
                  value_12)

        df = pd.read_sql_query(sql, con)
        df['CUMLYF'] = df['LYF'].cumsum()
        df['CUMCYF'] = df['CYF'].cumsum()
        df['FTMGP'] = (((df['CYF'] - df['LYF'])/df['LYF'])*100).round(2)
        df['CUMGP'] = (((df['CUMCYF'] - df['CUMLYF'])/df['CUMLYF'])*100).round(2)

        y1 = df['FTMGP']
        y2 = df['CUMGP']
        x1 = df['MONTHS']
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5)) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5)) for xi, yi in zip(x1, y2)]

        annotations = annot_1 + annot_2

        return {
                 'data': [ 
                             go.Scatter (
                                      x = df['MONTHS'],
                                      y = df['FTMGP'],
                                      name = 'FTM Growth %',
                                      mode = 'lines+markers',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Scatter (
                                      x = df['MONTHS'],
                                      y = df['CUMGP'],
                                      name = 'CUM Growth %',
                                      mode = 'lines+markers',
                                      marker_color='rgb(255, 51, 0)'
                                    ),
                      ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Months</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Growth %</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                         
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                title = '<b>Months Wise Freight Growth Percentage</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-2','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])
def update_graph_2(n_clicks,value_1, value_2, value_3, value_4, value_5,\
                   value_6, value_7, value_8, value_9, value_10, value_11,\
                   value_12):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''SELECT
                        to_char(to_date(YEAR_MONTH_DAY,'YYYYMMDD'),'MON-YY') MONTHS
                        ,SUM(NVL(LYA_TOT_WT,0)) LYW
                        ,SUM(NVL(TOT_WT,0)) CYW
                FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL
                WHERE
                        REGION_CODE = NVL('%s',REGION_CODE)
                        AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                        AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                        AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                        AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                        BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'MM') IN ('01','02','03')
                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY'))-1)
                                    ELSE TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY') END
                                        AND last_day(TO_DATE('%s%s','YYYYMM')) 
                GROUP BY
                        YEAR_MONTH_DAY
                ORDER BY
                        to_date(MONTHS,'MON-YY')
             '''%(value_1, value_2, value_3, value_4, value_5,\
                  value_6, value_7, value_8, value_9, value_10, value_11,\
                  value_12)

        df = pd.read_sql_query(sql, con)
        df['CUMLYW'] = df['LYW'].cumsum()
        df['CUMCYW'] = df['CYW'].cumsum()
        df['FTMGP'] = (((df['CYW'] - df['LYW'])/df['LYW'])*100).round(2)
        df['CUMGP'] = (((df['CUMCYW'] - df['CUMLYW'])/df['CUMLYW'])*100).round(2)

        y1 = df['FTMGP']
        y2 = df['CUMGP']
        x1 = df['MONTHS']
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5)) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5)) for xi, yi in zip(x1, y2)]

        annotations = annot_1 + annot_2

        return {
                 'data': [ 
                             go.Scatter (
                                      x = df['MONTHS'],
                                      y = df['FTMGP'],
                                      name = 'FTM Growth %',
                                      mode = 'lines+markers',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Scatter (
                                      x = df['MONTHS'],
                                      y = df['CUMGP'],
                                      name = 'CUM Growth %',
                                      mode = 'lines+markers',
                                      marker_color='rgb(255, 51, 0)'
                                    ),
                      ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Months</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Growth %</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                title = '<b>Months Wise Weight Growth Percentage</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-3','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])

def update_graph_3(n_clicks,value_1, value_2, value_3, value_4, value_5,\
                   value_6, value_7, value_8, value_9, value_10, value_11,\
                   value_12):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''SELECT
                        to_char(to_date(YEAR_MONTH_DAY,'YYYYMMDD'),'MON-YY') MONTHS
                        ,SUM(NVL(LYA_NO_DWB,0)) LYD
                        ,SUM(NVL(NO_DWB,0)) CYD
                FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL
                WHERE
                        REGION_CODE = NVL('%s',REGION_CODE)
                        AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                        AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                        AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                        AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                        BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'MM') IN ('01','02','03')
                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY'))-1)
                                    ELSE TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY') END
                                        AND last_day(TO_DATE('%s%s','YYYYMM')) 
                GROUP BY
                        YEAR_MONTH_DAY
                ORDER BY
                        to_date(MONTHS,'MON-YY')
             '''%(value_1, value_2, value_3, value_4, value_5,\
                  value_6, value_7, value_8, value_9, value_10, value_11,\
                  value_12)

        df = pd.read_sql_query(sql, con)
        df['CUMLYD'] = df['LYD'].cumsum()
        df['CUMCYD'] = df['CYD'].cumsum()
        df['FTMGP'] = (((df['CYD'] - df['LYD'])/df['LYD'])*100).round(2)
        df['CUMGP'] = (((df['CUMCYD'] - df['CUMLYD'])/df['CUMLYD'])*100).round(2)

        y1 = df['FTMGP']
        y2 = df['CUMGP']
        x1 = df['MONTHS']
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5)) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5)) for xi, yi in zip(x1, y2)]

        annotations = annot_1 + annot_2

        return {
                 'data': [ 
                             go.Scatter (
                                      x = df['MONTHS'],
                                      y = df['FTMGP'],
                                      name = 'FTM Growth %',
                                      mode = 'lines+markers',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Scatter (
                                      x = df['MONTHS'],
                                      y = df['CUMGP'],
                                      name = 'CUM Growth %',
                                      mode = 'lines+markers',
                                      marker_color='rgb(255, 51, 0)'
                                    ),
                      ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Months</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Growth %</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                title = '<b>Months Wise DWB Growth Percentage </b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-4','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])

def update_graph_4(n_clicks,value_1, value_2, value_3, value_4, value_5,\
                   value_6, value_7, value_8, value_9, value_10, value_11,\
                   value_12):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''SELECT
                        to_char(to_date(YEAR_MONTH_DAY,'YYYYMMDD'),'MON-YY') MONTHS
                        ,SUM(NVL(LYA_TOT_FRT,0))/NULLIF(SUM(NVL(LYA_TOT_WT,0)),0) LYY
                        ,SUM(NVL(TOT_FRT,0))/NULLIF(SUM(NVL(TOT_WT,0)),0)  CYY
                FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL
                WHERE
                        REGION_CODE = NVL('%s',REGION_CODE)
                        AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                        AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                        AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                        AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                        BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'MM') IN ('01','02','03')
                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY'))-1)
                                    ELSE TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY') END
                                        AND last_day(TO_DATE('%s%s','YYYYMM')) 
                GROUP BY
                        YEAR_MONTH_DAY
                ORDER BY
                        to_date(MONTHS,'MON-YY')
             '''%(value_1, value_2, value_3, value_4, value_5,\
                  value_6, value_7, value_8, value_9, value_10, value_11,\
                  value_12)

        df = pd.read_sql_query(sql, con)
        df['CUMLYY'] = df['LYY'].cumsum()
        df['CUMCYY'] = df['CYY'].cumsum()
        df['FTMGP'] = (((df['CYY'] - df['LYY'])/df['LYY'])*100).round(2)
        df['CUMGP'] = (((df['CUMCYY'] - df['CUMLYY'])/df['CUMLYY'])*100).round(2)

        y1 = df['FTMGP']
        y2 = df['CUMGP']
        x1 = df['MONTHS']
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5)) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5)) for xi, yi in zip(x1, y2)]

        annotations = annot_1 + annot_2

        return {
                 'data': [ 
                             go.Scatter (
                                      x = df['MONTHS'],
                                      y = df['FTMGP'],
                                      name = 'FTM Growth %',
                                      mode = 'lines+markers',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Scatter (
                                      x = df['MONTHS'],
                                      y = df['CUMGP'],
                                      name = 'CUM Growth %',
                                      mode = 'lines+markers',
                                      marker_color='rgb(255, 51, 0)'
                                    ),
                      ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Months</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Growth %</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                title = '<b>Months Wise Yield Growth Percentage </b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-5','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])
def update_graph_5(n_clicks,value_1, value_2, value_3, value_4, value_5,\
                   value_6, value_7, value_8, value_9, value_10, value_11,\
                   value_12, value_13, value_14, value_15, value_16, value_17,\
                   value_18):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''WITH CTE_1 AS (
                             SELECT
                                  REGION_CODE REGION
                                 ,SUM(NVL(LYA_TOT_FRT,0)) LYF
                                 ,SUM(NVL(TOT_FRT,0)) CYF
                             FROM
                                  CT_BUSINESS_GROWTH_NEW_IMPL
                             WHERE
                                  REGION_CODE = NVL('%s',REGION_CODE)
                                  AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                                  AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                                  AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                                  AND REGION_CODE <> 'XCRP'
                                  AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) = LAST_DAY(TO_DATE('%s%s','YYYYMM'))
                            GROUP BY
                                  REGION_CODE
                            ORDER BY
                                  REGION_CODE   
                            ),
                    CTE_2 AS (
                              SELECT
                                   REGION_CODE REGION
                                  ,SUM(NVL(LYA_TOT_FRT,0)) LYF
                                  ,SUM(NVL(TOT_FRT,0)) CYF
                              FROM
                                  CT_BUSINESS_GROWTH_NEW_IMPL
                              WHERE
                                  REGION_CODE = NVL('%s',REGION_CODE)
                                  AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                                  AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                                  AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                                  AND REGION_CODE <> 'XCRP'
                                  AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                  BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY') END
                                               AND last_day(TO_DATE('%s%s','YYYYMM')) 
                                  GROUP BY
                                       REGION_CODE
                                  ORDER BY
                                       REGION_CODE 
                                )
                        SELECT
                             CTE_1.REGION REGION
                            ,CTE_1.LYF
                            ,CTE_1.CYF
                            ,CTE_2.LYF
                            ,CTE_2.CYF
                            ,ROUND((((CTE_1.CYF - CTE_1.LYF)/NULLIF(NVL(CTE_1.LYF,0),0)) * 100),2) FTMGP
                            ,ROUND((((CTE_2.CYF - CTE_2.LYF)/NULLIF(NVL(CTE_2.LYF,0),0)) * 100),2) CUMGP
                    FROM
                        CTE_1
                    LEFT JOIN 
                        CTE_2 ON CTE_1.REGION = CTE_2.REGION
             '''%(value_1, value_2, value_3, value_4, value_5,\
                  value_6, value_7, value_8, value_9, value_10, value_11,\
                  value_12, value_13, value_14, value_15, value_16, value_17,\
                  value_18)

        df = pd.read_sql_query(sql, con)
        
        y1 = df['FTMGP']
        y2 = df['CUMGP']
        x1 = df['REGION']
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='right',yanchor='bottom', xshift = -1, showarrow=False,\
                   font=dict(size = 9.5), textangle=-90) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',yanchor='bottom', xshift = 1, showarrow=False,\
                   font=dict(size = 9.5), textangle=-90) for xi, yi in zip(x1, y2)]

        annotations = annot_1 + annot_2

        return {
                 'data': [ 
                             go.Bar (
                                      x = df['REGION'],
                                      y = df['FTMGP'],
                                      name = 'FTM Growth %',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Bar (
                                      x = df['REGION'],
                                      y = df['CUMGP'],
                                      name = 'CUM Growth %',
                                      marker_color='rgb(255, 51, 0)'
                                    ),
                      ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Region</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Growth %</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                         'autorange':'reversed'
                                         
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>Region Wise Freight Growth Percentage</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-6','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])
def update_graph_6(n_clicks,value_1, value_2, value_3, value_4, value_5,\
                   value_6, value_7, value_8, value_9, value_10, value_11,\
                   value_12, value_13, value_14, value_15, value_16, value_17,\
                   value_18):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''WITH CTE_1 AS (
                             SELECT
                                  REGION_CODE REGION
                                 ,SUM(NVL(LYA_TOT_WT,0)) LYW
                                 ,SUM(NVL(TOT_WT,0)) CYW
                             FROM
                                  CT_BUSINESS_GROWTH_NEW_IMPL
                             WHERE
                                  REGION_CODE = NVL('%s',REGION_CODE)
                                  AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                                  AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                                  AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                                  AND REGION_CODE <> 'XCRP'
                                  AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) = LAST_DAY(TO_DATE('%s%s','YYYYMM'))
                            GROUP BY
                                  REGION_CODE
                            ORDER BY
                                  REGION_CODE   
                            ),
                    CTE_2 AS (
                              SELECT
                                   REGION_CODE REGION
                                  ,SUM(NVL(LYA_TOT_WT,0)) LYW
                                  ,SUM(NVL(TOT_WT,0)) CYW
                              FROM
                                  CT_BUSINESS_GROWTH_NEW_IMPL
                              WHERE
                                  REGION_CODE = NVL('%s',REGION_CODE)
                                  AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                                  AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                                  AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                                  AND REGION_CODE <> 'XCRP'
                                  AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                  BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY') END
                                               AND last_day(TO_DATE('%s%s','YYYYMM')) 
                                  GROUP BY
                                       REGION_CODE
                                  ORDER BY
                                       REGION_CODE 
                                )
                     SELECT
                           CTE_1.REGION REGION
                          ,CTE_1.LYW
                          ,CTE_1.CYW
                          ,CTE_2.LYW
                          ,CTE_2.CYW
                          ,ROUND((((CTE_1.CYW - CTE_1.LYW)/NULLIF(NVL(CTE_1.LYW,0),0)) * 100),2) FTMGP
                          ,ROUND((((CTE_2.CYW - CTE_2.LYW)/NULLIF(NVL(CTE_2.LYW,0),0)) * 100),2) CUMGP
                    FROM
                        CTE_1
                    LEFT JOIN 
                        CTE_2 ON CTE_1.REGION = CTE_2.REGION
             '''%(value_1, value_2, value_3, value_4, value_5,\
                  value_6, value_7, value_8, value_9, value_10, value_11,\
                  value_12,value_13, value_14, value_15, value_16, value_17,\
                  value_18)

        df = pd.read_sql_query(sql, con)
        
        y1 = df['FTMGP']
        y2 = df['CUMGP']
        x1 = df['REGION']
           
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='right',yanchor='bottom', xshift = -1, showarrow=False,\
                   font=dict(size = 9.5), textangle=-90) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',yanchor='bottom', xshift = 1, showarrow=False,\
                   font=dict(size = 9.5), textangle=-90) for xi, yi in zip(x1, y2)]

        annotations = annot_1 + annot_2

        return {
                 'data': [ 
                             go.Bar (
                                      x = df['REGION'],
                                      y = df['FTMGP'],
                                      name = 'FTM Growth %',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Bar (
                                      x = df['REGION'],
                                      y = df['CUMGP'],
                                      name = 'CUM Growth %',
                                      marker_color='rgb(255, 51, 0)'
                                    ),
                      ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Region</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Growth %</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                         'autorange':'reversed'
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>Region Wise Weight Growth Percentage</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-7','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])

def update_graph_7(n_clicks,value_1, value_2, value_3, value_4, value_5,\
                   value_6, value_7, value_8, value_9, value_10, value_11,\
                   value_12, value_13, value_14, value_15, value_16, value_17,\
                   value_18):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''WITH CTE_1 AS (
                             SELECT
                                  REGION_CODE REGION
                                 ,SUM(NVL(LYA_NO_DWB,0)) LYD
                                 ,SUM(NVL(NO_DWB,0)) CYD
                             FROM
                                  CT_BUSINESS_GROWTH_NEW_IMPL
                             WHERE
                                  REGION_CODE = NVL('%s',REGION_CODE)
                                  AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                                  AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                                  AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                                  AND REGION_CODE <> 'XCRP'
                                  AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) = LAST_DAY(TO_DATE('%s%s','YYYYMM'))
                            GROUP BY
                                  REGION_CODE
                            ORDER BY
                                  REGION_CODE   
                            ),
                    CTE_2 AS (
                              SELECT
                                   REGION_CODE REGION
                                  ,SUM(NVL(LYA_NO_DWB,0)) LYD
                                  ,SUM(NVL(NO_DWB,0)) CYD
                              FROM
                                  CT_BUSINESS_GROWTH_NEW_IMPL
                              WHERE
                                  REGION_CODE = NVL('%s',REGION_CODE)
                                  AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                                  AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                                  AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                                  AND REGION_CODE <> 'XCRP'
                                  AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                  BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY') END
                                               AND last_day(TO_DATE('%s%s','YYYYMM')) 
                                  GROUP BY
                                       REGION_CODE
                                  ORDER BY
                                       REGION_CODE 
                                )
                     SELECT
                           CTE_1.REGION REGION
                          ,CTE_1.LYD
                          ,CTE_1.CYD
                          ,CTE_2.LYD
                          ,CTE_2.CYD
                          ,ROUND((((CTE_1.CYD - CTE_1.LYD)/NULLIF(NVL(CTE_1.LYD,0),0)) * 100),2) FTMGP
                          ,ROUND((((CTE_2.CYD - CTE_2.LYD)/NULLIF(NVL(CTE_2.LYD,0),0)) * 100),2) CUMGP
                    FROM
                        CTE_1
                    LEFT JOIN 
                        CTE_2 ON CTE_1.REGION = CTE_2.REGION
             '''%(value_1, value_2, value_3, value_4, value_5,\
                  value_6, value_7, value_8, value_9, value_10, value_11,\
                  value_12, value_13, value_14, value_15, value_16, value_17,\
                  value_18)

        df = pd.read_sql_query(sql, con)
        
        y1 = df['FTMGP']
        y2 = df['CUMGP']
        x1 = df['REGION']
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='right',yanchor='bottom', xshift = -1, showarrow=False,\
                   font=dict(size = 9.5), textangle=-90) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',yanchor='bottom', xshift = 1, showarrow=False,\
                   font=dict(size = 9.5), textangle=-90) for xi, yi in zip(x1, y2)]

        annotations = annot_1 + annot_2

        return {
                 'data': [ 
                             go.Bar (
                                      x = df['REGION'],
                                      y = df['FTMGP'],
                                      name = 'FTM Growth %',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Bar (
                                      x = df['REGION'],
                                      y = df['CUMGP'],
                                      name = 'CUM Growth %',
                                      marker_color='rgb(255, 51, 0)'
                                    ),
                      ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Region</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Growth %</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                         'autorange':'reversed'
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>Region Wise DWB Growth Percentage </b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-8','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])

def update_graph_8(n_clicks,value_1, value_2, value_3, value_4, value_5,\
                   value_6, value_7, value_8, value_9, value_10, value_11,\
                   value_12, value_13, value_14, value_15, value_16, value_17,\
                   value_18):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''WITH CTE_1 AS (
                             SELECT
                                  REGION_CODE REGION
                                 ,SUM(NVL(LYA_TOT_FRT,0))/NULLIF(SUM(NVL(LYA_TOT_WT,0)),0) LYY
                                 ,SUM(NVL(TOT_FRT,0))/NULLIF(SUM(NVL(TOT_WT,0)),0)  CYY
                             FROM
                                  CT_BUSINESS_GROWTH_NEW_IMPL
                             WHERE
                                  REGION_CODE = NVL('%s',REGION_CODE)
                                  AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                                  AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                                  AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                                  AND REGION_CODE <> 'XCRP'
                                  AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) = LAST_DAY(TO_DATE('%s%s','YYYYMM'))
                            GROUP BY
                                  REGION_CODE
                            ORDER BY
                                  REGION_CODE   
                            ),
                    CTE_2 AS (
                              SELECT
                                   REGION_CODE REGION
                                  ,SUM(NVL(LYA_TOT_FRT,0))/NULLIF(SUM(NVL(LYA_TOT_WT,0)),0) LYY
                                  ,SUM(NVL(TOT_FRT,0))/NULLIF(SUM(NVL(TOT_WT,0)),0)  CYY
                              FROM
                                  CT_BUSINESS_GROWTH_NEW_IMPL
                              WHERE
                                  REGION_CODE = NVL('%s',REGION_CODE)
                                  AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                                  AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                                  AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                                  AND REGION_CODE <> 'XCRP'
                                  AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                  BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY') END
                                               AND last_day(TO_DATE('%s%s','YYYYMM')) 
                                  GROUP BY
                                       REGION_CODE
                                  ORDER BY
                                       REGION_CODE 
                                )
                     SELECT
                           CTE_1.REGION REGION
                          ,CTE_1.LYY
                          ,CTE_1.CYY
                          ,CTE_2.LYY
                          ,CTE_2.CYY
                          ,ROUND((((CTE_1.CYY - CTE_1.LYY)/NULLIF(NVL(CTE_1.LYY,0),0)) * 100),2) FTMGP
                          ,ROUND((((CTE_2.CYY - CTE_2.LYY)/NULLIF(NVL(CTE_2.LYY,0),0)) * 100),2) CUMGP
                    FROM
                        CTE_1
                    LEFT JOIN 
                        CTE_2 ON CTE_1.REGION = CTE_2.REGION
             '''%(value_1, value_2, value_3, value_4, value_5,\
                  value_6, value_7, value_8, value_9, value_10, value_11,\
                  value_12,value_13, value_14, value_15, value_16, value_17,\
                  value_18)

        df = pd.read_sql_query(sql, con)
        
        y1 = df['FTMGP']
        y2 = df['CUMGP']
        x1 = df['REGION']
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='right',yanchor='bottom', xshift = -1, showarrow=False,\
                   font=dict(size = 9.5), textangle=-90) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',yanchor='bottom', xshift = 1, showarrow=False,\
                   font=dict(size = 9.5), textangle=-90) for xi, yi in zip(x1, y2)]

        annotations = annot_1 + annot_2

        return {
                 'data': [ 
                             go.Bar(
                                      x = df['REGION'],
                                      y = df['FTMGP'],
                                      name = 'FTM Growth %',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Bar(
                                      x = df['REGION'],
                                      y = df['CUMGP'],
                                      name = 'CUM Growth %',
                                      marker_color='rgb(255, 51, 0)'
                                    ),
                      ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Region</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Growth %</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>Region Wise Yield Growth Percentage </b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-9','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])

def update_graph_9(n_clicks,value_1, value_2, value_3, value_4, value_5, value_6):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''SELECT
                     REGION_CODE REGION
                    ,ROUND(SUM(NVL(LYA_TOT_FRT,0))/100000,1) LYF
                    ,ROUND(SUM(NVL(TOT_FRT,0))/100000,1) CYF
                    ,ROUND((SUM(NVL(TOT_FRT,0)) - SUM(NVL(LYA_TOT_FRT,0)))/100000,1) GP
                FROM
                    CT_BUSINESS_GROWTH_NEW_IMPL
                WHERE
                    REGION_CODE = NVL('%s',REGION_CODE)
                    AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                    AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                    AND DIVISION_CODE = NVL('%s', DIVISION_CODE)
                    AND REGION_CODE <> 'XCRP'
                    AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) = LAST_DAY(TO_DATE('%s%s','YYYYMM'))
                    GROUP BY
                        REGION_CODE
                    ORDER BY
                        REGION_CODE
              '''%(value_1, value_2, value_3, value_4, value_5, value_6)

        df = pd.read_sql_query(sql, con)

        df['color'] = np.where(df['GP'] < 0, 'red', 'green')

        y1 = df['LYF']
        y2 = df['CYF']
        y3 = df['GP']
        x1 = df['REGION']
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='right',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
        annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 18, yanchor='bottom', showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

        annotations = annot_1 + annot_2 + annot_3

        return {
                 'data': [ 
                             go.Bar (
                                      x = df['REGION'],
                                      y = df['LYF'],
                                      name = 'Last Year',
                                      marker_color='rgb(252, 177, 3)'
                                    ),
                             go.Bar(
                                      x = df['REGION'],
                                      y = df['CYF'],
                                      name = 'Current Year',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Bar(
                                      x = df['REGION'],
                                      y = df['GP'],
                                      name = 'Growth',
                                      marker_color= df['color']
                                    ),
                      ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Months</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Amount (Lkhs.)</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                #bargap = 0.6,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>Region Wise Freight Comparison</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-10','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])

def update_graph_10(n_clicks,value_1, value_2, value_3, value_4, value_5, value_6):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''SELECT
                     REGION_CODE REGION
                    ,ROUND(SUM(NVL(LYA_TOT_WT,0))/1000,2) LYW
                    ,ROUND(SUM(NVL(TOT_WT,0))/1000,0) CYW
                    ,ROUND((SUM(NVL(TOT_WT,0)) - SUM(NVL(LYA_TOT_WT,0)))/1000,0) GP
                FROM
                    CT_BUSINESS_GROWTH_NEW_IMPL
                WHERE
                    REGION_CODE = NVL('%s',REGION_CODE)
                    AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                    AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                    AND DIVISION_CODE = NVL('%s', DIVISION_CODE)
                    AND REGION_CODE <> 'XCRP'
                    AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) = LAST_DAY(TO_DATE('%s%s','YYYYMM'))
                    GROUP BY
                        REGION_CODE
                    ORDER BY
                        REGION_CODE
              '''%(value_1, value_2, value_3, value_4, value_5, value_6)

        df = pd.read_sql_query(sql, con)
        y1 = df['LYW']
        y2 = df['CYW']
        y3 = df['GP']
        x1 = df['REGION']

        df['color'] = np.where(df['GP'] < 0, 'red', 'green')
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='right',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
        annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 18, yanchor='bottom', showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

        annotations = annot_1 + annot_2 + annot_3

        return {
                 'data': [ 
                             go.Bar (
                                      x = df['REGION'],
                                      y = df['LYW'],
                                      name = 'Last Year',
                                      marker_color='rgb(252, 177, 3)'
                                    ),
                             go.Bar(
                                      x = df['REGION'],
                                      y = df['CYW'],
                                      name = 'Current Year',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Bar(
                                      x = df['REGION'],
                                      y = df['GP'],
                                      name = 'Growth',
                                      marker_color= df['color']
                                    ),
                      ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Months</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Amount (Tons)</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                #bargap = 0.6,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>Region Wise Weight Comparison</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-11','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])

def update_graph_11(n_clicks,value_1, value_2, value_3, value_4, value_5, value_6):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''SELECT
                     REGION_CODE REGION
                    ,SUM(NVL(LYA_NO_DWB,0)) LYD
                    ,SUM(NVL(NO_DWB,0)) CYD
                    ,(SUM(NVL(NO_DWB,0)) - SUM(NVL(LYA_NO_DWB,0))) GP
                FROM
                    CT_BUSINESS_GROWTH_NEW_IMPL
                WHERE
                    REGION_CODE = NVL('%s',REGION_CODE)
                    AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                    AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                    AND DIVISION_CODE = NVL('%s', DIVISION_CODE)
                    AND REGION_CODE <> 'XCRP'
                    AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) = LAST_DAY(TO_DATE('%s%s','YYYYMM'))
                    GROUP BY
                        REGION_CODE
                    ORDER BY
                        REGION_CODE
              '''%(value_1, value_2, value_3, value_4, value_5, value_6)

        df = pd.read_sql_query(sql, con)
        y1 = df['LYD']
        y2 = df['CYD']
        y3 = df['GP']
        x1 = df['REGION']

        df['color'] = np.where(df['GP'] < 0, 'red', 'green')
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='right',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
        annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 18, yanchor='bottom', showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

        annotations = annot_1 + annot_2 + annot_3

        return {
                 'data': [ 
                             go.Bar (
                                      x = df['REGION'],
                                      y = df['LYD'],
                                      name = 'Last Year',
                                      marker_color='rgb(252, 177, 3)'
                                    ),
                             go.Bar(
                                      x = df['REGION'],
                                      y = df['CYD'],
                                      name = 'Current Year',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Bar(
                                      x = df['REGION'],
                                      y = df['GP'],
                                      name = 'Growth',
                                      marker_color= df['color']
                                    ),
                      ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Months</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Number</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                #bargap = 0.6,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>Region Wise DWB Comparison</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-12','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])

def update_graph_12(n_clicks,value_1, value_2, value_3, value_4, value_5, value_6):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''SELECT
                     REGION_CODE REGION
                    ,ROUND(SUM(NVL(LYA_TOT_FRT,0))/NULLIF(SUM(NVL(LYA_TOT_WT,0)),0),1) LYY
                    ,ROUND(SUM(NVL(TOT_FRT,0))/NULLIF(SUM(NVL(TOT_WT,0)),0),1) CYY
                    ,ROUND(((SUM(NVL(TOT_FRT,0))/NULLIF(SUM(NVL(TOT_WT,0)),0)) - (SUM(NVL(LYA_TOT_FRT,0))/NULLIF(SUM(NVL(LYA_TOT_WT,0)),0))),2) GP 
                FROM
                    CT_BUSINESS_GROWTH_NEW_IMPL
                WHERE
                    REGION_CODE = NVL('%s',REGION_CODE)
                    AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                    AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                    AND DIVISION_CODE = NVL('%s', DIVISION_CODE)
                    AND REGION_CODE <> 'XCRP'
                    AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) = LAST_DAY(TO_DATE('%s%s','YYYYMM'))
                    GROUP BY
                        REGION_CODE
                    ORDER BY
                        REGION_CODE
              '''%(value_1, value_2, value_3, value_4, value_5, value_6)

        df = pd.read_sql_query(sql, con)

        df['color'] = np.where(df['GP'] < 0, 'red', 'green')

        y1 = df['LYY']
        y2 = df['CYY']
        y3 = df['GP']
        x1 = df['REGION']
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='right',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
        annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 18, yanchor='bottom', showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

        annotations = annot_1 + annot_2 + annot_3

        return {
                 'data': [ 
                             go.Bar (
                                      x = df['REGION'],
                                      y = df['LYY'],
                                      name = 'Last Year',
                                      marker_color='rgb(252, 177, 3)'
                                    ),
                             go.Bar(
                                      x = df['REGION'],
                                      y = df['CYY'],
                                      name = 'Current Year',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Bar(
                                      x = df['REGION'],
                                      y = df['GP'],
                                      name = 'Growth',
                                      marker_color= df['color']
                                    ),
                      ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Months</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Amount</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                #bargap = 0.6,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>Region Wise Yield Comparison</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}

@app.callback(Output('graph-9A','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])

def update_graph_9A(n_clicks,value_1, value_2, value_3, value_4, value_5, value_6,\
                    value_7, value_8, value_9, value_10, value_11,\
                    value_12):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''SELECT
                     REGION_CODE REGION
                    ,ROUND(SUM(NVL(LYA_TOT_FRT,0))/100000,1) LYF
                    ,ROUND(SUM(NVL(TOT_FRT,0))/100000,1) CYF
                    ,ROUND((SUM(NVL(TOT_FRT,0)) - SUM(NVL(LYA_TOT_FRT,0)))/100000,1) GP
                FROM
                    CT_BUSINESS_GROWTH_NEW_IMPL
                WHERE
                    REGION_CODE = NVL('%s',REGION_CODE)
                    AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                    AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                    AND DIVISION_CODE = NVL('%s', DIVISION_CODE)
                    AND REGION_CODE <> 'XCRP'
                    AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'MM') IN ('01','02','03')
                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY'))-1)
                                    ELSE TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY') END
                                        AND last_day(TO_DATE('%s%s','YYYYMM')) 
                    GROUP BY
                        REGION_CODE
                    ORDER BY
                        REGION_CODE
              '''%(value_1, value_2, value_3, value_4, value_5, value_6,\
                   value_7, value_8, value_9, value_10, value_11,\
                   value_12)

        df = pd.read_sql_query(sql, con)

        df['color'] = np.where(df['GP'] < 0, 'red', 'green')

        y1 = df['LYF']
        y2 = df['CYF']
        y3 = df['GP']
        x1 = df['REGION']
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='right',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
        annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 18, yanchor='bottom', showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

        annotations = annot_1 + annot_2 + annot_3

        return {
                 'data': [ 
                             go.Bar (
                                      x = df['REGION'],
                                      y = df['LYF'],
                                      name = 'Last Year',
                                      marker_color='rgb(252, 177, 3)'
                                    ),
                             go.Bar(
                                      x = df['REGION'],
                                      y = df['CYF'],
                                      name = 'Current Year',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Bar(
                                      x = df['REGION'],
                                      y = df['GP'],
                                      name = 'Growth',
                                      marker_color= df['color']
                                    ),
                      ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Months</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Amount (Lkhs.)</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                #bargap = 0.6,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>Region Wise Freight Comparison</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-10A','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])

def update_graph_10A(n_clicks,value_1, value_2, value_3, value_4, value_5, value_6,\
                    value_7, value_8, value_9, value_10, value_11,\
                    value_12):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''SELECT
                     REGION_CODE REGION
                    ,ROUND(SUM(NVL(LYA_TOT_WT,0))/1000,2) LYW
                    ,ROUND(SUM(NVL(TOT_WT,0))/1000,0) CYW
                    ,ROUND((SUM(NVL(TOT_WT,0)) - SUM(NVL(LYA_TOT_WT,0)))/1000,0) GP
                FROM
                    CT_BUSINESS_GROWTH_NEW_IMPL
                WHERE
                    REGION_CODE = NVL('%s',REGION_CODE)
                    AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                    AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                    AND DIVISION_CODE = NVL('%s', DIVISION_CODE)
                    AND REGION_CODE <> 'XCRP'
                    AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'MM') IN ('01','02','03')
                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY'))-1)
                                    ELSE TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY') END
                                        AND last_day(TO_DATE('%s%s','YYYYMM')) 
                    GROUP BY
                        REGION_CODE
                    ORDER BY
                        REGION_CODE
              '''%(value_1, value_2, value_3, value_4, value_5, value_6,\
                   value_7, value_8, value_9, value_10, value_11,\
                   value_12)

        df = pd.read_sql_query(sql, con)
        y1 = df['LYW']
        y2 = df['CYW']
        y3 = df['GP']
        x1 = df['REGION']

        df['color'] = np.where(df['GP'] < 0, 'red', 'green')
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='right',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
        annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 18, yanchor='bottom', showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

        annotations = annot_1 + annot_2 + annot_3

        return {
                 'data': [ 
                             go.Bar (
                                      x = df['REGION'],
                                      y = df['LYW'],
                                      name = 'Last Year',
                                      marker_color='rgb(252, 177, 3)'
                                    ),
                             go.Bar(
                                      x = df['REGION'],
                                      y = df['CYW'],
                                      name = 'Current Year',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Bar(
                                      x = df['REGION'],
                                      y = df['GP'],
                                      name = 'Growth',
                                      marker_color= df['color']
                                    ),
                      ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Months</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Amount (Tons)</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                #bargap = 0.6,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>Region Wise Weight Comparison</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-11A','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])

def update_graph_11A(n_clicks,value_1, value_2, value_3, value_4, value_5, value_6,\
                    value_7, value_8, value_9, value_10, value_11,\
                    value_12):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''SELECT
                     REGION_CODE REGION
                    ,SUM(NVL(LYA_NO_DWB,0)) LYD
                    ,SUM(NVL(NO_DWB,0)) CYD
                    ,(SUM(NVL(NO_DWB,0)) - SUM(NVL(LYA_NO_DWB,0))) GP
                FROM
                    CT_BUSINESS_GROWTH_NEW_IMPL
                WHERE
                    REGION_CODE = NVL('%s',REGION_CODE)
                    AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                    AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                    AND DIVISION_CODE = NVL('%s', DIVISION_CODE)
                    AND REGION_CODE <> 'XCRP'
                    AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'MM') IN ('01','02','03')
                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY'))-1)
                                    ELSE TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY') END
                                        AND last_day(TO_DATE('%s%s','YYYYMM')) 
                    GROUP BY
                        REGION_CODE
                    ORDER BY
                        REGION_CODE
              '''%(value_1, value_2, value_3, value_4, value_5, value_6,\
                   value_7, value_8, value_9, value_10, value_11,\
                   value_12)

        df = pd.read_sql_query(sql, con)
        y1 = df['LYD']
        y2 = df['CYD']
        y3 = df['GP']
        x1 = df['REGION']

        df['color'] = np.where(df['GP'] < 0, 'red', 'green')
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='right',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
        annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 18, yanchor='bottom', showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

        annotations = annot_1 + annot_2 + annot_3

        return {
                 'data': [ 
                             go.Bar (
                                      x = df['REGION'],
                                      y = df['LYD'],
                                      name = 'Last Year',
                                      marker_color='rgb(252, 177, 3)'
                                    ),
                             go.Bar(
                                      x = df['REGION'],
                                      y = df['CYD'],
                                      name = 'Current Year',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Bar(
                                      x = df['REGION'],
                                      y = df['GP'],
                                      name = 'Growth',
                                      marker_color= df['color']
                                    ),
                      ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Months</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Number</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                #bargap = 0.6,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>Region Wise DWB Comparison</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-12A','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])

def update_graph_12A(n_clicks,value_1, value_2, value_3, value_4, value_5, value_6,\
                    value_7, value_8, value_9, value_10, value_11,\
                    value_12):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''SELECT
                     REGION_CODE REGION
                    ,ROUND(SUM(NVL(LYA_TOT_FRT,0))/NULLIF(SUM(NVL(LYA_TOT_WT,0)),0),1) LYY
                    ,ROUND(SUM(NVL(TOT_FRT,0))/NULLIF(SUM(NVL(TOT_WT,0)),0),1) CYY
                    ,ROUND(((SUM(NVL(TOT_FRT,0))/NULLIF(SUM(NVL(TOT_WT,0)),0)) - (SUM(NVL(LYA_TOT_FRT,0))/NULLIF(SUM(NVL(LYA_TOT_WT,0)),0))),2) GP 
                FROM
                    CT_BUSINESS_GROWTH_NEW_IMPL
                WHERE
                    REGION_CODE = NVL('%s',REGION_CODE)
                    AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                    AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                    AND DIVISION_CODE = NVL('%s', DIVISION_CODE)
                    AND REGION_CODE <> 'XCRP'
                    AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'MM') IN ('01','02','03')
                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY'))-1)
                                    ELSE TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY') END
                                        AND last_day(TO_DATE('%s%s','YYYYMM')) 
                    GROUP BY
                        REGION_CODE
                    ORDER BY
                        REGION_CODE
              '''%(value_1, value_2, value_3, value_4, value_5, value_6,\
                   value_7, value_8, value_9, value_10, value_11,\
                   value_12)

        df = pd.read_sql_query(sql, con)

        df['color'] = np.where(df['GP'] < 0, 'red', 'green')

        y1 = df['LYY']
        y2 = df['CYY']
        y3 = df['GP']
        x1 = df['REGION']
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='right',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
        annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 18, yanchor='bottom', showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

        annotations = annot_1 + annot_2 + annot_3

        return {
                 'data': [ 
                             go.Bar (
                                      x = df['REGION'],
                                      y = df['LYY'],
                                      name = 'Last Year',
                                      marker_color='rgb(252, 177, 3)'
                                    ),
                             go.Bar(
                                      x = df['REGION'],
                                      y = df['CYY'],
                                      name = 'Current Year',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Bar(
                                      x = df['REGION'],
                                      y = df['GP'],
                                      name = 'Growth',
                                      marker_color= df['color']
                                    ),
                      ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Months</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Amount</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                #bargap = 0.6,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>Region Wise Yield Comparison</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}



@app.callback(Output('graph-13','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])
def update_graph_13(n_clicks,value_1, value_2, value_3, value_4, value_5,\
                   value_6, value_7, value_8, value_9, value_10, value_11,\
                   value_12):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''SELECT
                        to_char(to_date(YEAR_MONTH_DAY,'YYYYMMDD'),'MON-YY') MONTHS
                        ,ROUND(SUM(NVL(TOT_FRT,0))/100000,1) CYF
                FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL
                WHERE
                        REGION_CODE = NVL('%s',REGION_CODE)
                        AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                        AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                        AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                        AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                        BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'MM') IN ('01','02','03')
                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY'))-1)
                                    ELSE TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY') END
                                        AND last_day(TO_DATE('%s%s','YYYYMM')) 
                GROUP BY
                        YEAR_MONTH_DAY
                ORDER BY
                        to_date(MONTHS,'MON-YY')
             '''%(value_1, value_2, value_3, value_4, value_5,\
                  value_6, value_7, value_8, value_9, value_10, value_11,\
                  value_12)

        df = pd.read_sql_query(sql, con)
        df['CUMCYF'] = df['CYF'].cumsum()
        y1 = df['CYF']
        y2 = df['CUMCYF']
        x1 = df['MONTHS']
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5)) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5)) for xi, yi in zip(x1, y2)]
        

        annotations = annot_1 + annot_2

        return {
                 'data': [ 
                             go.Scatter (
                                      x = df['MONTHS'],
                                      y = df['CYF'],
                                      mode = 'lines+markers',
                                      name = 'FTM Freight',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Scatter (
                                      x = df['MONTHS'],
                                      y = df['CUMCYF'],
                                      mode = 'lines+markers',
                                      name = 'CUM Freight',
                                      marker_color='rgb(255, 51, 0)'
                                    ),
                             
                      ],

                 'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Months</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Amount (Lkhs.)</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                title = '<b>Months Wise Freight Trend</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-14','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])
def update_graph_14(n_clicks,value_1, value_2, value_3, value_4, value_5,\
                   value_6, value_7, value_8, value_9, value_10, value_11,\
                   value_12):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''SELECT
                        to_char(to_date(YEAR_MONTH_DAY,'YYYYMMDD'),'MON-YY') MONTHS
                        ,ROUND(SUM(NVL(TOT_WT,0))/1000,1) CYW
                FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL
                WHERE
                        REGION_CODE = NVL('%s',REGION_CODE)
                        AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                        AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                        AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                        AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                        BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'MM') IN ('01','02','03')
                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY'))-1)
                                    ELSE TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY') END
                                        AND last_day(TO_DATE('%s%s','YYYYMM')) 
                GROUP BY
                        YEAR_MONTH_DAY
                ORDER BY
                        to_date(MONTHS,'MON-YY')
             '''%(value_1, value_2, value_3, value_4, value_5,\
                  value_6, value_7, value_8, value_9, value_10, value_11,\
                  value_12)

        df = pd.read_sql_query(sql, con)
        df['CUMCYW'] = df['CYW'].cumsum().round(1)
        y1 = df['CYW']
        y2 = df['CUMCYW']
        x1 = df['MONTHS']
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5)) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5)) for xi, yi in zip(x1, y2)]

        annotations = annot_1 + annot_2

        return {
                 'data': [ 
                             go.Scatter (
                                      x = df['MONTHS'],
                                      y = df['CYW'],
                                      mode = 'lines+markers',
                                      name = 'FTM Weight',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Scatter (
                                      x = df['MONTHS'],
                                      y = df['CUMCYW'],
                                      mode = 'lines+markers',
                                      name = 'CUM Weight',
                                      marker_color='rgb(255, 51, 0)'
                                    ),
                             
                      ],

                 'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Months</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Amount (Tons)</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                title = '<b>Months Wise Weight Trend</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-15','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])
def update_graph_15(n_clicks,value_1, value_2, value_3, value_4, value_5,\
                   value_6, value_7, value_8, value_9, value_10, value_11,\
                   value_12):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''SELECT
                        to_char(to_date(YEAR_MONTH_DAY,'YYYYMMDD'),'MON-YY') MONTHS
                        ,SUM(NVL(NO_DWB,0)) CYD
                FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL
                WHERE
                        REGION_CODE = NVL('%s',REGION_CODE)
                        AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                        AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                        AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                        AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                        BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'MM') IN ('01','02','03')
                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY'))-1)
                                    ELSE TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY') END
                                        AND last_day(TO_DATE('%s%s','YYYYMM')) 
                GROUP BY
                        YEAR_MONTH_DAY
                ORDER BY
                        to_date(MONTHS,'MON-YY')
             '''%(value_1, value_2, value_3, value_4, value_5,\
                  value_6, value_7, value_8, value_9, value_10, value_11,\
                  value_12)

        df = pd.read_sql_query(sql, con)
        df['CUMCYD'] = df['CYD'].cumsum()
        y1 = df['CYD']
        y2 = df['CUMCYD']
        x1 = df['MONTHS']
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5)) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5)) for xi, yi in zip(x1, y2)]
        

        annotations = annot_1 + annot_2

        return {
                 'data': [ 
                             go.Scatter (
                                      x = df['MONTHS'],
                                      y = df['CYD'],
                                      mode = 'lines+markers',
                                      name = 'FTM DWB',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Scatter (
                                      x = df['MONTHS'],
                                      y = df['CUMCYD'],
                                      mode = 'lines+markers',
                                      name = 'CUM DWB',
                                      marker_color='rgb(255, 51, 0)'
                                    ),
                             
                      ],

                 'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Months</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Number</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                title = '<b>Months Wise DWB Trend</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-16','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])
def update_graph_16(n_clicks,value_1, value_2, value_3, value_4, value_5,\
                   value_6, value_7, value_8, value_9, value_10, value_11,\
                   value_12):
    
    if n_clicks is not None and n_clicks > 0:

        con = cx.connect(config.CONN_STR)
        
        sql = '''SELECT
                        to_char(to_date(YEAR_MONTH_DAY,'YYYYMMDD'),'MON-YY') MONTHS
                        ,SUM(NVL(TOT_FRT,0)) CCF
                        ,SUM(NVL(TOT_WT,0)) CCW
                        ,ROUND(SUM(NVL(TOT_FRT,0))/NULLIF(SUM(NVL(TOT_WT,0)),0),2) CYY
                FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL
                WHERE
                        REGION_CODE = NVL('%s',REGION_CODE)
                        AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                        AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                        AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                        AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                        BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'MM') IN ('01','02','03')
                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY'))-1)
                                    ELSE TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY') END
                                        AND last_day(TO_DATE('%s%s','YYYYMM')) 
                GROUP BY
                        YEAR_MONTH_DAY
                ORDER BY
                        to_date(MONTHS,'MON-YY')
             '''%(value_1, value_2, value_3, value_4, value_5,\
                  value_6, value_7, value_8, value_9, value_10, value_11,\
                  value_12)

        df = pd.read_sql_query(sql, con)

        df['CUMCCF'] = df['CCF'].cumsum()
        df['CUMCCW'] = df['CCW'].cumsum()
        df['CUMCCY'] = (df['CUMCCF']/df['CUMCCW']).round(2)

        y1 = df['CYY']
        y2 = df['CUMCCY']
        x1 = df['MONTHS']
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5)) for xi, yi in zip(x1, y1)]

        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5)) for xi, yi in zip(x1, y2)]
        
        annotations = annot_1 + annot_2

        return {
                 'data': [ 
                             go.Scatter (
                                      x = df['MONTHS'],
                                      y = df['CYY'],
                                      mode = 'lines+markers',
                                      name = 'FTM Yield',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Scatter (
                                      x = df['MONTHS'],
                                      y = df['CUMCCY'],
                                      mode = 'lines+markers',
                                      name = 'CUM Yield',
                                      marker_color='rgb(255, 51, 0)'
                                    )
                             
                         ],

                 'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Months</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Amount</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                title = '<b>Months Wise Yield Trend</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-17','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])
def update_graph_17(n_clicks,value_1, value_2, value_3, value_4, value_5,\
                   value_6, value_7, value_8, value_9, value_10, value_11,\
                   value_12, value_13, value_14, value_15, value_16, value_17,\
                   value_18):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''WITH CTE_1 AS (
                             SELECT
                                  REGION_CODE REGION
                                 ,ROUND(SUM(NVL(TOT_FRT,0))/100000,1) CYF
                             FROM
                                  CT_BUSINESS_GROWTH_NEW_IMPL
                             WHERE
                                  REGION_CODE = NVL('%s',REGION_CODE)
                                  AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                                  AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                                  AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                                  AND REGION_CODE <> 'XCRP'
                                  AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) = LAST_DAY(TO_DATE('%s%s','YYYYMM'))
                            GROUP BY
                                  REGION_CODE
                            ORDER BY
                                  REGION_CODE   
                            ),
                    CTE_2 AS (
                              SELECT
                                   REGION_CODE REGION
                                  ,ROUND(SUM(NVL(TOT_FRT,0))/100000,1) CYF
                              FROM
                                  CT_BUSINESS_GROWTH_NEW_IMPL
                              WHERE
                                  REGION_CODE = NVL('%s',REGION_CODE)
                                  AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                                  AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                                  AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                                  AND REGION_CODE <> 'XCRP'
                                  AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                  BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY') END
                                               AND last_day(TO_DATE('%s%s','YYYYMM')) 
                                  GROUP BY
                                       REGION_CODE
                                  ORDER BY
                                       REGION_CODE 
                                )
                        SELECT
                             CTE_1.REGION REGION
                            ,CTE_1.CYF FTMCYF
                            ,CTE_2.CYF CUMCYF
                        FROM
                             CTE_1
                        LEFT JOIN 
                             CTE_2 ON CTE_1.REGION = CTE_2.REGION
             '''%(value_1, value_2, value_3, value_4, value_5,\
                  value_6, value_7, value_8, value_9, value_10, value_11,\
                  value_12, value_13, value_14, value_15, value_16, value_17,\
                  value_18)

        df = pd.read_sql_query(sql, con)
        
        y1 = df['FTMCYF']
        y2 = df['CUMCYF']
        x1 = df['REGION']
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='right',yanchor='bottom', xshift = -1, showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',yanchor='bottom', xshift = 1, showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]

        annotations = annot_1 + annot_2

        return {
                 'data': [ 
                             go.Bar (
                                      x = df['REGION'],
                                      y = df['FTMCYF'],
                                      name = 'FTM Freight',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Bar (
                                      x = df['REGION'],
                                      y = df['CUMCYF'],
                                      name = 'CUM Freight',
                                      marker_color='rgb(255, 51, 0)'
                                    ),
                      ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Region</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Amount (Lkhs.)</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                        
                                         
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>Region Wise Freight Trend</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-18','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])
def update_graph_18(n_clicks,value_1, value_2, value_3, value_4, value_5,\
                   value_6, value_7, value_8, value_9, value_10, value_11,\
                   value_12, value_13, value_14, value_15, value_16, value_17,\
                   value_18):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''WITH CTE_1 AS (
                             SELECT
                                  REGION_CODE REGION
                                 ,ROUND(SUM(NVL(TOT_WT,0))/1000,1) CYW
                             FROM
                                  CT_BUSINESS_GROWTH_NEW_IMPL
                             WHERE
                                  REGION_CODE = NVL('%s',REGION_CODE)
                                  AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                                  AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                                  AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                                  AND REGION_CODE <> 'XCRP'
                                  AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) = LAST_DAY(TO_DATE('%s%s','YYYYMM'))
                            GROUP BY
                                  REGION_CODE
                            ORDER BY
                                  REGION_CODE   
                            ),
                    CTE_2 AS (
                              SELECT
                                   REGION_CODE REGION
                                  ,ROUND(SUM(NVL(TOT_WT,0))/1000,1) CYW
                              FROM
                                  CT_BUSINESS_GROWTH_NEW_IMPL
                              WHERE
                                  REGION_CODE = NVL('%s',REGION_CODE)
                                  AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                                  AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                                  AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                                  AND REGION_CODE <> 'XCRP'
                                  AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                  BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY') END
                                               AND last_day(TO_DATE('%s%s','YYYYMM')) 
                                  GROUP BY
                                       REGION_CODE
                                  ORDER BY
                                       REGION_CODE 
                                )
                     SELECT
                           CTE_1.REGION REGION
                          ,CTE_1.CYW FTMCYW
                          ,CTE_2.CYW CUMCYW
                    FROM
                        CTE_1
                    LEFT JOIN 
                        CTE_2 ON CTE_1.REGION = CTE_2.REGION
             '''%(value_1, value_2, value_3, value_4, value_5,\
                  value_6, value_7, value_8, value_9, value_10, value_11,\
                  value_12,value_13, value_14, value_15, value_16, value_17,\
                  value_18)

        df = pd.read_sql_query(sql, con)
        
        y1 = df['FTMCYW']
        y2 = df['CUMCYW']
        x1 = df['REGION']
           
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='right',yanchor='bottom', xshift = -1, showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',yanchor='bottom', xshift = 1, showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]

        annotations = annot_1 + annot_2

        return {
                 'data': [ 
                             go.Bar (
                                      x = df['REGION'],
                                      y = df['FTMCYW'],
                                      name = 'FTM Weight',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Bar (
                                      x = df['REGION'],
                                      y = df['CUMCYW'],
                                      name = 'CUM Weight',
                                      marker_color='rgb(255, 51, 0)'
                                    ),
                      ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Region</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Amount (Tons)</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                         
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>Region Wise Weight Trend</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-19','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])

def update_graph_19(n_clicks,value_1, value_2, value_3, value_4, value_5,\
                   value_6, value_7, value_8, value_9, value_10, value_11,\
                   value_12, value_13, value_14, value_15, value_16, value_17,\
                   value_18):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''WITH CTE_1 AS (
                             SELECT
                                  REGION_CODE REGION
                                 ,SUM(NVL(NO_DWB,0)) CYD
                             FROM
                                  CT_BUSINESS_GROWTH_NEW_IMPL
                             WHERE
                                  REGION_CODE = NVL('%s',REGION_CODE)
                                  AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                                  AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                                  AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                                  AND REGION_CODE <> 'XCRP'
                                  AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) = LAST_DAY(TO_DATE('%s%s','YYYYMM'))
                            GROUP BY
                                  REGION_CODE
                            ORDER BY
                                  REGION_CODE   
                            ),
                    CTE_2 AS (
                              SELECT
                                   REGION_CODE REGION
                                  ,SUM(NVL(NO_DWB,0)) CYD
                              FROM
                                  CT_BUSINESS_GROWTH_NEW_IMPL
                              WHERE
                                  REGION_CODE = NVL('%s',REGION_CODE)
                                  AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                                  AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                                  AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                                  AND REGION_CODE <> 'XCRP'
                                  AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                  BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY') END
                                               AND last_day(TO_DATE('%s%s','YYYYMM')) 
                                  GROUP BY
                                       REGION_CODE
                                  ORDER BY
                                       REGION_CODE 
                                )
                     SELECT
                           CTE_1.REGION REGION
                          ,CTE_1.CYD FTMCYD
                          ,CTE_2.CYD CUMCYD
                    FROM
                        CTE_1
                    LEFT JOIN 
                        CTE_2 ON CTE_1.REGION = CTE_2.REGION
             '''%(value_1, value_2, value_3, value_4, value_5,\
                  value_6, value_7, value_8, value_9, value_10, value_11,\
                  value_12, value_13, value_14, value_15, value_16, value_17,\
                  value_18)

        df = pd.read_sql_query(sql, con)
        
        y1 = df['FTMCYD']
        y2 = df['CUMCYD']
        x1 = df['REGION']
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='right',yanchor='bottom', xshift = -1, showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',yanchor='bottom', xshift = 1, showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]

        annotations = annot_1 + annot_2

        return {
                 'data': [ 
                             go.Bar (
                                      x = df['REGION'],
                                      y = df['FTMCYD'],
                                      name = 'FTM DWB',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Bar (
                                      x = df['REGION'],
                                      y = df['CUMCYD'],
                                      name = 'CUM DWB',
                                      marker_color='rgb(255, 51, 0)'
                                    ),
                      ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Region</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Number</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                        
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>Region Wise DWB Trend</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}


@app.callback(Output('graph-20','figure'), [Input('submit_button','n_clicks')],
                                          [State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('division-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          ])

def update_graph_20(n_clicks,value_1, value_2, value_3, value_4, value_5,\
                   value_6, value_7, value_8, value_9, value_10, value_11,\
                   value_12, value_13, value_14, value_15, value_16, value_17,\
                   value_18):
    
    if n_clicks is not None and n_clicks > 0:
        con = cx.connect(config.CONN_STR)
        sql = '''WITH CTE_1 AS (
                             SELECT
                                  REGION_CODE REGION
                                 ,SUM(NVL(TOT_FRT,0))/NULLIF(SUM(NVL(TOT_WT,0)),0)  CYY
                             FROM
                                  CT_BUSINESS_GROWTH_NEW_IMPL
                             WHERE
                                  REGION_CODE = NVL('%s',REGION_CODE)
                                  AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                                  AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                                  AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                                  AND REGION_CODE <> 'XCRP'
                                  AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) = LAST_DAY(TO_DATE('%s%s','YYYYMM'))
                            GROUP BY
                                  REGION_CODE
                            ORDER BY
                                  REGION_CODE   
                            ),
                    CTE_2 AS (
                              SELECT
                                   REGION_CODE REGION
                                  ,SUM(NVL(TOT_FRT,0))/NULLIF(SUM(NVL(TOT_WT,0)),0)  CYY
                              FROM
                                  CT_BUSINESS_GROWTH_NEW_IMPL
                              WHERE
                                  REGION_CODE = NVL('%s',REGION_CODE)
                                  AND CONTROLLING_CODE = NVL('%s',CONTROLLING_CODE) 
                                  AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
                                  AND DIVISION_CODE = NVL('%s',DIVISION_CODE)
                                  AND REGION_CODE <> 'XCRP'
                                  AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                  BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%s%s','YYYYMM')),'YYYY') END
                                               AND last_day(TO_DATE('%s%s','YYYYMM')) 
                                  GROUP BY
                                       REGION_CODE
                                  ORDER BY
                                       REGION_CODE 
                                )
                     SELECT
                           CTE_1.REGION REGION
                          ,ROUND(CTE_1.CYY,1) FTMCYY
                          ,ROUND(CTE_2.CYY,1) CUMCYY
                    FROM
                        CTE_1
                    LEFT JOIN 
                        CTE_2 ON CTE_1.REGION = CTE_2.REGION
             '''%(value_1, value_2, value_3, value_4, value_5,\
                  value_6, value_7, value_8, value_9, value_10, value_11,\
                  value_12,value_13, value_14, value_15, value_16, value_17,\
                  value_18)

        df = pd.read_sql_query(sql, con)
        
        y1 = df['FTMCYY']
        y2 = df['CUMCYY']
        x1 = df['REGION']
        
        
        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='right',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
        annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]

        annotations = annot_1 + annot_2

        return {
                 'data': [ 
                             go.Bar(
                                      x = df['REGION'],
                                      y = df['FTMCYY'],
                                      name = 'FTM Yield',
                                      marker_color='rgb(102, 153, 255)'
                                    ),
                             go.Bar(
                                      x = df['REGION'],
                                      y = df['CUMCYY'],
                                      name = 'CUM Yield',
                                      marker_color='rgb(255, 51, 0)'
                                    ),
                      ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Region</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Amount</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                        },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                annotations = annotations,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>Region Wise Yield Trend </b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                showlegend = True
                            )
                             
            }
    else:
            return {}

