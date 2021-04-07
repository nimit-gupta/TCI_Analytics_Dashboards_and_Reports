#!usr/bin/env python
#coding:utf-8

'''
=============================================================================================================================================================

                                                        Python Script for HUB WISE Weight Loss - APP 9

=============================================================================================================================================================

'''

from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash


import plotly.graph_objects as go
import cx_Oracle as cx
import pandas as pd
import numpy as np
import config 


app = dash.Dash(__name__, requests_pathname_prefix = '/app9/', external_stylesheets=[dbc.themes.BOOTSTRAP])

SIDEBAR_STYLE = {
                    "position": "fixed",
                    "top": 0,
                    "left": 0,
                    "bottom": 0,
                    "width": "16rem",
                    "padding": "2rem 1rem",
                    "background-color": "rgb(230, 225, 225)",
                }


CONTENT_STYLE = {
                    "margin-left": "18rem",
                    "margin-right": "2rem",
                    "padding": "2rem 1rem",
                }


sidebar = html.Div([
                    html.Br(),
                    html.Div([
                            dbc.Row([
                                    dbc.Col([   html.H6('From'),
                                                dcc.Dropdown(
                                                                id='from_branch_dropdown',
                                                                options = [
                                                                            {'label':'HUB','value':'H'},
                                                                          ],
                                                                clearable = False,
                                                                style = {'font-weight':'bold'}
                                                                
                                                            )
                                            ])
                                   ])
                            ]),
                    html.Br(),
                    html.Div([
                             dbc.Row([
                                    dbc.Col([   html.H6('Hub'),
                                                dcc.Dropdown(
                                                                id='tcs_from',
                                                                clearable = False,
                                                                style = {'font-weight':'bold'}
                                                                
                                                            )
                                            ])
                                     ])
                             ]),
                    html.Br(),
                    html.Div([
                             dbc.Row([
                                    dbc.Col([   html.H6('To'),
                                                dcc.Dropdown(
                                                                id='to_branch_dropdown',
                                                                options = [
                                                                            {'label':'BRANCH','value':'B'},
                                                                            {'label':'HUB','value':'H'},
                                                                          ],
                                                                clearable = False,
                                                                style = {'font-weight':'bold'}
                                                                
                                                            )
                                            ])
                                    ])
                            ]),
                    html.Br(),
                    html.Div([
                              dbc.Row([
                                    dbc.Col([   html.H6('Hub/Branch'),
                                                dcc.Dropdown(
                                                                id='to_stn',
                                                                clearable = False,
                                                                style = {'font-weight':'bold'}
                                                                
                                                            )
                                            ]),
                                        
                                    ])
                            ]),
                    html.Br(), 
                    html.Div([                         
                                html.Button(
                                            'Submit',
                                            id = 'submit_button',
                                            type = 'submit',
                                            style = {'width':'100px', 'height':'35px',\
                                                     'display':'inline-block',\
                                                     'margin-left' : '50px',\
                                                     'font-weight':'bold',\
                                                     'border-radius':'4px'}
                                        )
                            ])
               ],
                 style = SIDEBAR_STYLE,
            )

app.layout = html.Div([
                      html.Div(
                               [sidebar]
                              ), 
                      html.Br(),
                      html.Div(
                               [dcc.Loading(dcc.Graph(id = 'Graph-1'))
                               ], style = {"margin-left": "18rem", "margin-right" : "2rem"}),
                      html.Br(),
                      html.Div(
                               [dcc.Loading(dcc.Graph(id = 'Graph-2'))
                               ], style = {"margin-left": "18rem", "margin-right" : "2rem"}),
                       ],style = {'width' : 'auto', 'background-color': '#f2f2f2'}
                    )


@app.callback(Output('tcs_from','options'),[Input('from_branch_dropdown','value')], prevent_initial_call = True)

def tcs_from(hub):

       con_A = cx.connect(config.CONN_STR)

       sql_A = '''
                SELECT 
                     DISTINCT TCS_FROM 
                FROM 
                     TCS_VO_WT_LOSS_MAIL_CHG_WT 
                WHERE 
                     FROM_BRN_TYPE = '%(hub)s' 
                ORDER BY 
                     TCS_FROM
               '''%{'hub': hub}
       
       df_A = pd.read_sql_query(sql_A, con_A)
       df_A['COPY_TCS_FROM'] = df_A['TCS_FROM']
       df_A.loc[len(df_A)] = 'ALL'
       df_A['COPY_TCS_FROM'].iloc[-1] = ''
       return [{'label': k, 'value' : v} for k, v in zip(df_A['TCS_FROM'], df_A['COPY_TCS_FROM'])]

    

@app.callback(Output('to_stn','options'),[Input('to_branch_dropdown','value')], prevent_initial_call = True)

def to_stn(value):

    if value == 'H':

       con_A = cx.connect(config.CONN_STR)

       sql_A = '''
                SELECT 
                     DISTINCT TO_STN 
                FROM 
                     TCS_VO_WT_LOSS_MAIL_CHG_WT 
                WHERE 
                     TO_STN_TYPE = 'H' 
                ORDER BY 
                     TO_STN
               '''
       
       df_A = pd.read_sql_query(sql_A, con_A)
       df_A['COPY_TO_STN'] = df_A['TO_STN']
       df_A.loc[len(df_A)] = 'ALL'
       df_A['COPY_TO_STN'].iloc[-1] = ''
       return [{'label': k, 'value' : v} for k, v in zip(df_A['TO_STN'], df_A['COPY_TO_STN'])]

    elif value == 'B':

       con_B = cx.connect(config.CONN_STR)

       sql_B = '''
                SELECT 
                     DISTINCT TO_STN 
                FROM 
                     TCS_VO_WT_LOSS_MAIL_CHG_WT 
                WHERE 
                     TO_STN_TYPE = 'B' 
                ORDER BY 
                     TO_STN

               '''
       
       df_B = pd.read_sql_query(sql_B, con_B)
       df_B['COPY_TO_STN'] = df_B['TO_STN']
       df_B.loc[len(df_B)] = 'ALL'
       df_B['COPY_TO_STN'].iloc[-1] = ''
       return [{'label': k, 'value' : v} for k, v in zip(df_B['TO_STN'], df_B['COPY_TO_STN'])]

@app.callback(Output('Graph-1','figure'),[Input('submit_button','n_clicks')],\
                                         [State('from_branch_dropdown','value'),\
                                          State('tcs_from','value'),\
                                          State('to_branch_dropdown','value'),\
                                          State('to_stn', 'value')
                                         ], prevent_initial_call = True)

def update_grpah_1(n_clicks, from_brn_type, tcs_from_value, to_stn_type, to_stn_value):
    
    if n_clicks is not None and n_clicks > 0:

        con = cx.connect(config.CONN_STR)

        sql_0 = '''
                  SELECT 
                       TO_CHAR(TRUNC(SYSDATE, 'MM') + LEVEL - 1,'DD-MM-YYYY') AS DAILY_DATE
                  FROM 
                       DUAL
                  CONNECT BY 
                       TRUNC(TRUNC(SYSDATE, 'MM') + LEVEL - 1, 'MM') = TRUNC(SYSDATE, 'MM')

                '''

        df_0 = pd.read_sql_query(sql_0, con)

        sql_1 = '''
                 SELECT
                       TO_CHAR(DEP_DATE, 'DD-MM-YYYY') DAILY_DATE
                      ,ROUND((SUM(WT_LOSS)/SUM(CAPACITY))*100,2) PERCENT
                 FROM
                     TCS_VO_WT_LOSS_MAIL_CHG_WT
                 WHERE
                      TRUNC(DEP_DATE) 
                                    BETWEEN To_Date('01'||To_Char(Decode(To_Char(SYSDATE,'DD'),'01',Add_Months(SYSDATE,-1),SYSDATE),'MMYYYY'),'DDMMYYYY') 
                                          AND TRUNC(SYSDATE) 
                      AND FROM_BRN_TYPE = '%(from_brn_type)s'                    
                      AND TCS_FROM = NVL('%(tcs_from_value)s', TCS_FROM)
                      AND TO_STN_TYPE = '%(to_stn_type)s'
                      AND TO_STN = NVL('%(to_stn_value)s', TO_STN)
                      
                GROUP BY
                     TO_CHAR(DEP_DATE, 'DD-MM-YYYY')
                 
             '''%{'from_brn_type': from_brn_type,\
                  'tcs_from_value': tcs_from_value,\
                  'to_stn_type' : to_stn_type,\
                  'to_stn_value' : to_stn_value
                 }

        df_1 = pd.read_sql_query(sql_1, con)

        df_2 = df_0.merge(df_1, on = 'DAILY_DATE', how = 'left')

        y1 = df_2['PERCENT'].replace(np.nan,' ')

        x1 = df_2['DAILY_DATE']

        annot_1 = [
                     dict(
                            x=xi,
                            y=yi,
                            text= str(yi),
                            xanchor='center',  
                            yanchor='bottom',
                            showarrow=False,
                            font=dict(size = 10.5)) for xi, yi in zip(x1, y1)
                  ]

        annotations = annot_1

        return {
                    'data': [
                                go.Scatter(
                                            x=df_2['DAILY_DATE'],
                                            y=df_2['PERCENT'],
                                            mode = 'lines + markers',
                                            name = 'LOSS PERCENT',
                                            marker_color='rgb(255, 0, 0)'
                                        ),
                
                            ],
                    'layout' : go.Layout(
                                        title={
                                                    'text': 'From' + ' ' + str(tcs_from_value) + ' ' + 'To' + ' ' + str(to_stn_value) + ' ' + 'Weight Loss % Trend',
                                                    'y':0.90,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                              },
                                        annotations = annotations,
                                        legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.02,
                                        xanchor="right",
                                        x=1
                                        ),
                                        showlegend = True,
                                        xaxis=dict(
                                                    title= '<b>Date</b>',
                                                    tickangle = 30,
                                                    showticklabels = True,
                                                    ticks="outside", 
                                                    showgrid = False,
                                                    zeroline = False),
                                        yaxis=dict(
                                                    title="<b>Weight Loss</b>", 
                                                    showgrid = False,
                                                    ticks="outside",
                                                    zeroline = False
                                                ),
                                        paper_bgcolor = '#e6e6e6',
                                        yaxis_ticksuffix = "%",
                                        hovermode="x unified"
                                        )

        }
    else:
        return {}

@app.callback(Output('Graph-2','figure'),[Input('submit_button','n_clicks')],\
                                         [State('from_branch_dropdown','value'),\
                                          State('tcs_from','value'),\
                                          State('to_branch_dropdown','value'),\
                                          State('to_stn', 'value')
                                         ], prevent_initial_call = True)

def update_grpah_2(n_clicks, from_brn_type, tcs_from_value, to_stn_type, to_stn_value):
    
    if n_clicks is not None and n_clicks > 0:

        con = cx.connect(config.CONN_STR)

        sql_0 = '''
                   SELECT 
                        TO_CHAR(add_months(TRUNC(SYSDATE, 'mm'), 
                        DECODE(EXTRACT(MONTH FROM SYSDATE), 
                               1,-9,
                               2,-9,
                               3,-9,
                               4, 3,
                               3)
                        - EXTRACT(MONTH FROM SYSDATE) + level), 'MON-YYYY') DAILY_MONTH
                  FROM DUAL
                  CONNECT BY level <= 12

                '''

        df_0 = pd.read_sql_query(sql_0, con)

        sql_1 = '''
                 SELECT
                       TO_CHAR(DEP_DATE, 'MON-YYYY') DAILY_MONTH
                      ,ROUND((SUM(WT_LOSS)/SUM(CAPACITY))*100,2) PERCENT
                 FROM
                     TCS_VO_WT_LOSS_MAIL_CHG_WT
                 WHERE
                       TRUNC(DEP_DATE) 
                                     BETWEEN CASE WHEN EXTRACT(MONTH FROM SYSDATE) IN ( 1, 2, 3) 
                                            THEN ADD_MONTHS(TRUNC(SYSDATE,'year'),-9)
                                                ELSE ADD_MONTHS(TRUNC(SYSDATE,'year'),3) 
                                                    END AND TRUNC(SYSDATE) 
                      AND FROM_BRN_TYPE = '%(from_brn_type)s'                    
                      AND TCS_FROM = NVL('%(tcs_from_value)s', TCS_FROM)
                      AND TO_STN_TYPE = '%(to_stn_type)s'
                      AND TO_STN = NVL('%(to_stn_value)s', TO_STN)
                 GROUP BY
                      TO_CHAR(DEP_DATE, 'MON-YYYY')
                 
             '''%{'from_brn_type': from_brn_type,\
                  'tcs_from_value': tcs_from_value,\
                  'to_stn_type' : to_stn_type,\
                  'to_stn_value' : to_stn_value
                 }

        df_1 = pd.read_sql_query(sql_1, con)

        df_2 = df_0.merge(df_1, on = 'DAILY_MONTH', how = 'left')

        y1 = df_2['PERCENT'].replace(np.nan,'')

        x1 = df_2['DAILY_MONTH']

        annot_1 = [
                    dict(x=xi,y=yi,
                    text= str(yi),
                    xanchor='center',  
                    yanchor='bottom',
                    showarrow=False,
                    font=dict(size = 10.5)) for xi, yi in zip(x1, y1)
                  ]

        annotations = annot_1

        return {
                        'data': [
                                    go.Scatter(
                                                x=df_2['DAILY_MONTH'],
                                                y=df_2['PERCENT'],
                                                mode = 'lines + markers',
                                                name = 'LOSS PERCENT',
                                                marker_color='rgb(255, 0, 0)'
                                            ),

                                
                                ],
                        'layout' : go.Layout(
                                            title={
                                                        'text': 'From' + ' ' + str(tcs_from_value) + ' ' + 'To' + ' ' + str(to_stn_value) + ' ' + 'Weight Loss % Trend',
                                                        'y':0.90,
                                                        'x':0.5,
                                                        'xanchor': 'center',
                                                        'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(    
                                                        title= '<b>Month</b>',
                                                        tickangle = 30,
                                                        showticklabels = True, 
                                                        ticks="outside",
                                                        showgrid = False,
                                                        zeroline = False
                                                    ),
                                            yaxis=dict(
                                                        title="<b>Weight Loss</b>",
                                                        showgrid = False,
                                                        zeroline = False,
                                                        ticks="outside"
                                                    ),
                                            paper_bgcolor = '#e6e6e6',
                                            yaxis_ticksuffix = "%",
                                            hovermode="x unified"
                                            )

        }

    else:
        return {}





