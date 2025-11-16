#!/usr/bin/python
#-*- coding:utf-8 -*-

from __future__ import (
                        absolute_import,
                        unicode_literals
                       )

try:

  import pandas as pd
  import numpy as np
  import cx_Oracle as cx

  import dash
  import plotly.graph_objects as go
  import dash_core_components as dcc
  import dash_html_components as html
  import dash_bootstrap_components as dbc
  from dash.dependencies import Input, Output, State

  import config

except ImportError as error:
    pass

app = dash.Dash(__name__,requests_pathname_prefix='/app1/',external_stylesheets = [dbc.themes.BOOTSTRAP])


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "rgb(230, 225, 225)",
    "overflow" : "scroll"
}


CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

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

sidebar = html.Div(
    [
        html.Div([html.H6('Region'),
                  dcc.Dropdown(
                               id = 'region-dropdown',
                               options = [{'label': k, 'value' : v} for k, v in zip(df['REGION_CODE'], df['COPY_REGION_CODE'])],
                               #placeholder = 'Region',
                               style = {'font-weight' : 'bold'})
                ]),
        html.Br(),
        html.Div([html.H6('Controlling'),
                  dcc.Dropdown(
                               id = 'controlling-dropdown',
                               #placeholder = 'Controlling',
                               style = {'font-weight' : 'bold'}
                              )
                ]),
        html.Br(),
        html.Div([html.H6('Branch'),
                  dcc.Dropdown(
                               id = 'branch-dropdown',
                               #placeholder = 'Branch',
                               style = {'font-weight' : 'bold'})
                ]),
        html.Br(),
        html.Div([
                  dbc.Row([ 
                           dbc.Col([html.H6('Year'),
                                    dcc.Dropdown(
                                                 id = 'year-dropdown',
                                                 #placeholder = 'Year',
                                                 style = {'font-weight' : 'bold'}
                                                )
                                   ]),
                           dbc.Col([html.H6('Month'),
                                    dcc.Dropdown(
                                                 id = 'month-dropdown',
                                                 #placeholder = 'Month',
                                                 style = {'font-weight' : 'bold'}
                                                 )
                           ])
                          ])
                 ]),
        html.Br(),                            
        html.Button(
                     'Submit',
                     id = 'submit_button',
                     type = 'submit',
                     style = {'width':'100px', 'height':'35px', 'display':'inline-block',\
                                                       'margin-left' : '50px','background-color': '#ffffff',\
                                                       'font-weight':'bold', 'border-radius':'4px'}
                   )

    ],
    style=SIDEBAR_STYLE,
)

app.layout = html.Div([
                      html.Div([sidebar]), 
                      html.Br(),
                      html.Div([dcc.Loading(dcc.Graph(id = 'Graph-1'))], style = {"margin-left": "18rem", "margin-right" : "2rem"}),
                      html.Br(),
                      html.Div([dcc.Loading(dcc.Graph(id = 'Graph-2'))], style = {"margin-left": "18rem", "margin-right" : "2rem"}),
                      html.Br(),
                      html.Div([dcc.Loading(dcc.Graph(id = 'Graph-3'))], style = {"margin-left": "18rem", "margin-right" : "2rem"}),
                      html.Br(),
                      html.Div([dcc.Loading(dcc.Graph(id = 'Graph-4'))], style = {"margin-left": "18rem", "margin-right" : "2rem"}),
                      html.Br(),
                      html.Div([dcc.Loading(dcc.Graph(id = 'Graph-5'))], style = {"margin-left": "18rem", "margin-right" : "2rem"}),
                      html.Br(),
                      ],style = {'width' : 'auto', 'background-color': '#f2f2f2'})

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

@app.callback(Output('year-dropdown', 'options'),[Input('branch-dropdown', 'value')])
def set_year_start_options(selected_month):
    return [{'label': p, 'value': p} for p in ['2020','2021']]

@app.callback(Output('month-dropdown', 'options'),[Input('year-dropdown', 'value')])
def set_month_start_options(selected_branch):
    return [{'label' : q, 'value' : q} for q in [ '01','02','03',\
                                                  '04','05','06',\
                                                  '07','08','09',\
                                                  '10','11','12']
                                                ]

@app.callback(Output('Graph-1','figure'), [Input('submit_button','n_clicks')],
                                          [State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value')])
def update_graph_1(n_clicks, value_1, value_2, value_3, value_4, value_5):
  if n_clicks is not None and n_clicks > 0:
    con = cx.connect(config.CONN_STR)
    sql = '''SELECT
                 ROUND(SUM(TOT_FRT)/100000,2) as ACHIEVED
                ,ROUND(SUM(TRGT_BKG_FRT)/100000,2) as TARGETED
             FROM 
                CT_BUSINESS_GROWTH_NEW_IMPL
             WHERE
                LAST_DAY(to_date(YEAR_MONTH_DAY,'YYYYMMDD')) = LAST_DAY(to_date('%s%s','YYYYMM'))
                AND REGION_CODE = NVL('%s', REGION_CODE)
                AND CONTROLLING_CODE = NVL('%s', CONTROLLING_CODE)
                AND BRANCH_CODE = NVL('%s', BRANCH_CODE)
         '''%(
              value_1,
              value_2,
              value_3,
              value_4,
              value_5
              
             )
    df = pd.read_sql_query(sql,con)
    df.index = ['Freight'] 

    y1 = df['TARGETED']
    y2 = df['ACHIEVED']

    xcoord = df.index 

    annot_1 = [dict(
                x=xi,
                y=yi,
                text= str(yi),
                xanchor='left',
                xshift = -45,
                yanchor='bottom',
                showarrow=False,
                font=dict(
                          size = 11.5,
                         ),
                textangle=-90
                ) for xi, yi in zip(xcoord, y1)]

    annot_2 = [dict(
                x=xi,
                y=yi,
                text=str(yi),
                xanchor='left',
                xshift = 30,
                yanchor='bottom',
                showarrow=False,
                font=dict(
                          size = 11.5,
                         ),
                textangle=-90
                ) for xi, yi in zip(xcoord, y2)]

    annotations = annot_1 + annot_2

    return {
              'data': [ 
                             go.Bar (
                                      x = df.index,
                                      y = df['TARGETED'],
                                      name = 'Targeted Freight',
                                      marker_color='rgb(255, 0, 0)'
                                    ),
                             go.Bar (
                                      x = df.index,
                                      y = df['ACHIEVED'],
                                      name = 'Achieved Freight',
                                      marker_color='rgb(0, 153, 0)'
                                    ),
                    ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : str(value_3) + '-' + str(value_4) + '-' + str(value_5),
                                         'showticklabels' : False,
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Amount (Lakhs)</b>',
                                         'showgrid': False,
                                         'zeroline':False,
                                        },
                                annotations = annotations,
                                bargap = 0.8,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>Business Growth - Targeted Vs Achieved Freight Revenue</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                legend = dict(orientation="h",yanchor="bottom", y=1.02, xanchor="right",\
                                              x=1, itemsizing = 'trace')
                               )
                             
            }
  else:
        return {}

@app.callback(Output('Graph-2','figure'), [Input('submit_button','n_clicks')],
                                          [State('year-dropdown','value'),\
                                           State('month-dropdown','value'),\
                                           State('region-dropdown','value'),\
                                           State('controlling-dropdown','value'),\
                                           State('branch-dropdown','value')])
def update_graph_2(n_clicks,value_1, value_2, value_3, value_4, value_5):
  if n_clicks is not None and n_clicks > 0:
    con = cx.connect(config.CONN_STR)
    sql = '''SELECT
                    CASE
                       WHEN DIVISION_CODE = 21 THEN 'Surface'
                       WHEN DIVISION_CODE = 22 THEN 'AIR'
                       WHEN DIVISION_CODE = 23 THEN 'ECOM'
                       WHEN DIVISION_CODE = 24 THEN 'RAIL'
                       WHEN DIVISION_CODE = 25 THEN 'GTA'
                       WHEN DIVISION_CODE = 26 THEN 'INTL AIR'
                       WHEN DIVISION_CODE = 27 THEN 'C2C'
                    END AS PRODUCT
                  ,CASE
                      WHEN DIVISION_CODE = 21 THEN ROUND(SUM(NVL(TRGT_BKG_FRT,0))/100000,2)
                      WHEN DIVISION_CODE = 22 THEN ROUND(SUM(NVL(TRGT_BKG_FRT,0))/100000,2)
                      WHEN DIVISION_CODE = 23 THEN ROUND(SUM(NVL(TRGT_BKG_FRT,0))/100000,2)
                      WHEN DIVISION_CODE = 24 THEN ROUND(SUM(NVL(TRGT_BKG_FRT,0))/100000,2)
                      WHEN DIVISION_CODE = 25 THEN ROUND(SUM(NVL(TRGT_BKG_FRT,0))/100000,2)
                      WHEN DIVISION_CODE = 26 THEN ROUND(SUM(NVL(TRGT_BKG_FRT,0))/100000,2)
                      WHEN DIVISION_CODE = 27 THEN ROUND(SUM(NVL(TRGT_BKG_FRT,0))/100000,2)
                   END AS TARGETED
                 ,CASE
                      WHEN DIVISION_CODE = 21 THEN ROUND(SUM(NVL(TOT_FRT,0))/100000,2)
                      WHEN DIVISION_CODE = 22 THEN ROUND(SUM(NVL(TOT_FRT,0))/100000,2)
                      WHEN DIVISION_CODE = 23 THEN ROUND(SUM(NVL(TOT_FRT,0))/100000,2)
                      WHEN DIVISION_CODE = 24 THEN ROUND(SUM(NVL(TOT_FRT,0))/100000,2)
                      WHEN DIVISION_CODE = 25 THEN ROUND(SUM(NVL(TOT_FRT,0))/100000,2)
                      WHEN DIVISION_CODE = 26 THEN ROUND(SUM(NVL(TOT_FRT,0))/100000,2)
                      WHEN DIVISION_CODE = 27 THEN ROUND(SUM(NVL(TOT_FRT,0))/100000,2)
                  END AS ACHIEVED
                FROM
                  CT_BUSINESS_GROWTH_NEW_IMPL 
                WHERE
                  LAST_DAY(to_date(YEAR_MONTH_DAY,'YYYYMMDD')) = LAST_DAY(to_date('%s%s','YYYYMM'))
                  AND REGION_CODE = NVL('%s', REGION_CODE)
                  AND CONTROLLING_CODE = NVL('%s', CONTROLLING_CODE)
                  AND BRANCH_CODE = NVL('%s', BRANCH_CODE) 
                GROUP BY
                  DIVISION_CODE
                ORDER BY
                  TARGETED DESC
          '''%(
                value_1,
                value_2,
                value_3,
                value_4,
                value_5
              )

    df = pd.read_sql_query(sql, con)
    df.set_index('PRODUCT', inplace = True)

    y1 = df['TARGETED']
    y2 = df['ACHIEVED']

    xcoord = df.index 

    annot_1 = [dict(
                x=xi,
                y=yi,
                text= str(yi),
                xanchor='left',
                xshift = -30,
                yanchor='bottom',
                showarrow=False,
                font=dict(
                          size = 11.5,
                         ),
                textangle=-90,
                ) for xi, yi in zip(xcoord, y1)]

    annot_2 = [dict(
                x=xi,
                y=yi,
                text=str(yi),
                xanchor='left',
                xshift = 12,
                yanchor='bottom',
                showarrow=False,
                font=dict(
                          size = 11.5,
                         ),
                textangle=-90
                ) for xi, yi in zip(xcoord, y2)]

    annotations = annot_1 + annot_2

    return {
              'data': [ 
                             go.Bar (
                                      x = df.index,
                                      y = df['TARGETED'],
                                      name = 'Targeted Freight',
                                      marker_color='rgb(255, 0, 0)'
                                    ),
                             go.Bar (
                                      x = df.index,
                                      y = df['ACHIEVED'],
                                      name = 'Achieved Freight',
                                      marker_color='rgb(0, 153, 0)'
                                    ),
                    ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Division</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Amount (Lakhs)</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                annotations = annotations,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>Product Wise Business Growth - Targeted Vs Achieved Freight Revenue</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                               legend = dict(orientation="h",yanchor="bottom", y=1.02, xanchor="right", x=1)

                               )
                             
            }
  else:
        return {}

@app.callback(Output('Graph-3','figure'),[Input('submit_button','n_clicks')],
                                         [State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('region-dropdown','value'),\
                                          State('controlling-dropdown','value'),\
                                          State('branch-dropdown','value')
                                         ])
def update_graph_3(n_clicks, value_1,value_2,value_3,value_4, value_5,\
                   value_6, value_7, value_8,value_9, value_10):
  if n_clicks is not None and n_clicks > 0:
      con = cx.connect(config.CONN_STR)
      sql_1 = '''SELECT
                   ROUND(SUM(NVL(OS_0TO30_DAYS,0))/100000,2) AS "0-30"
                  ,ROUND(SUM(NVL(OS_31TO60_DAYS,0))/100000,2) AS "31-60"
                  ,ROUND(SUM(NVL(OS_61TO75_DAYS,0))/100000,2) AS "61-75"
                  ,ROUND(SUM(NVL(OS_76TO90_DAYS,0))/100000,2) AS "76-90"
                  ,ROUND(SUM(NVL(OS_91TO120_DAYS,0))/100000,2) AS "91-120"
                  ,ROUND(SUM(NVL(OS_121TO180_DAYS,0))/100000,2) AS "121-180"
                  ,ROUND(SUM(NVL(OS_181TO365_DAYS,0))/100000,2) AS "181-365"
                  ,ROUND(SUM(NVL(OS_ABOVE_365_DAYS,0))/100000,2) AS ">365"
               FROM
                  CT_AGEWISE_BILLED_OS
               WHERE
                  LAST_DAY(to_date(to_char(UPTO_BILL_DATE,'YYYYMM'),'YYYYMM')) = LAST_DAY(to_date('%s%s','YYYYMM'))
                  AND REGION_CODE = NVL('%s', REGION_CODE)
                  AND CONTROLLING_CODE = NVL('%s', CONTROLLING_CODE)
                  AND BRANCH_CODE = NVL('%s', BRANCH_CODE)
                  AND REALISE_FLAG = 'O'
         '''%(
               value_1,
               value_2,
               value_3,
               value_4,
               value_5,
            )  
      sql_2 ='''SELECT
                   ROUND(SUM(NVL(OS_0TO30_DAYS,0))/100000,2) AS "0-30"
                  ,ROUND(SUM(NVL(OS_31TO60_DAYS,0))/100000,2) AS "31-60"
                  ,ROUND(SUM(NVL(OS_61TO75_DAYS,0))/100000,2) AS "61-75"
                  ,ROUND(SUM(NVL(OS_76TO90_DAYS,0))/100000,2) AS "76-90"
                  ,ROUND(SUM(NVL(OS_91TO120_DAYS,0))/100000,2) AS "91-120"
                  ,ROUND(SUM(NVL(OS_121TO180_DAYS,0))/100000,2) AS "121-180"
                  ,ROUND(SUM(NVL(OS_181TO365_DAYS,0))/100000,2) AS "181-365"
                  ,ROUND(SUM(NVL(OS_ABOVE_365_DAYS,0))/100000,2) AS ">365"
                FROM
                  CT_AGEWISE_BILLED_OS
                WHERE
                 LAST_DAY(to_date(to_char(UPTO_BILL_DATE,'YYYYMM'),'YYYYMM')) = LAST_DAY(to_date('%s%s','YYYYMM'))
                 AND REGION_CODE = NVL('%s', REGION_CODE)
                 AND CONTROLLING_CODE = NVL('%s', CONTROLLING_CODE)
                 AND BRANCH_CODE = NVL('%s', BRANCH_CODE)
                 AND REALISE_FLAG = 'R'
           '''%(
                 value_6,
                 value_7,
                 value_8,
                 value_9,
                 value_10
              )
      df_1 = pd.read_sql_query(sql_1, con).T
      df_2 = pd.read_sql_query(sql_2, con).T
      df_3 = pd.merge(df_1, df_2, left_index=True, right_index=True).rename(columns = {'0_x':'OUTSTANDING','0_y':'REALIZED'})

      y1 = df_3['OUTSTANDING']
      y2 = df_3['REALIZED']

      xcoord = df_3.index 

      annot_1 = [dict(
                x=xi,
                y=yi,
                text= str(yi),
                xanchor='left',
                xshift = -30,
                yanchor='bottom',
                showarrow=False,
                font=dict(
                          size = 11.5,
                         ),
                textangle=-90
                ) for xi, yi in zip(xcoord, y1)]

      annot_2 = [dict(
                x=xi,
                y=yi,
                text=str(yi),
                 xanchor='left',
                xshift = 12,
                yanchor='bottom',
                showarrow=False,
                font=dict(
                         size = 11.5,
                         ),
                textangle=-90
                ) for xi, yi in zip(xcoord, y2)]

      annotations = annot_1 + annot_2


      return {
              'data': [ 
                             go.Bar (
                                      x = df_3.index,
                                      y = df_3['OUTSTANDING'],
                                      name = 'Bill Outstanding',
                                      marker_color='rgb(255, 0, 0)'
                                    ),
                             go.Bar (
                                      x = df_3.index,
                                      y = df_3['REALIZED'],
                                      name = 'Bill Realization',
                                      marker_color='rgb(0, 153, 0)'
                                    ),
                    ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Aged Date</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Amount (Lakhs)</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                annotations = annotations,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>Bill Outstanding Vs Bill Realization</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                legend = dict(orientation="h",yanchor="bottom", y=1.02, xanchor="right", x=1)
                               )
                             
            }
  else:
        return {}

@app.callback(Output('Graph-4','figure'), [Input('submit_button','n_clicks')],
                                          [State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('branch-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('branch-dropdown','value')])
def update_graph_4(n_clicks,value_1, value_2, value_3, value_4,value_5,value_6):
  if n_clicks is not None and n_clicks > 0:
     con = cx.connect(config.CONN_STR)
     sql_1 = '''SELECT
               ROUND(SUM(NVL(AMOUNT,0)+NVL(AMOUNT_REV_1,0)+NVL(AMOUNT_REV_2,0)+NVL(AMOUNT_REV_3,0))/1000,-1) INDIRECT_EXPENSE_BUDGET
              FROM
               CM_SRM_ACCOUNT_BUDGET
              WHERE 
               LAST_DAY(to_date(MONTH_YEAR ,'YYYYMM')) = LAST_DAY(to_date('%s%s','YYYYMM'))
               AND BRANCH_CODE = NVL('%s',BRANCH_CODE)
               AND COMPANY_CODE ='8' 
               AND DIVISION_CODE = '2'
           '''%(
                value_1,
                value_2,
                value_3
                )
     sql_2 = '''SELECT 
                  ROUND(Nvl(Sum(Nvl(AMOUNT_TO_PAY,0)),0)/1000,0) ACTUAL_EXPENSE_AMOUNT
                FROM 
                 CT_SRM_PAYMENT
                WHERE
                LAST_DAY(to_date(to_char(PAYMENT_DATE,'YYYYMM'),'YYYYMM')) = LAST_DAY(to_date('%s%s','YYYYMM'))
                AND BRANCH_CODE = NVL('%s', BRANCH_CODE)
                AND DIV_CODE ='2' 
                AND (Nvl(APPROVAL_FLAG_1,'N') NOT IN ('R') AND Nvl(APPROVAL_FLAG_2,'N') NOT IN ('R') AND Nvl(APPROVAL_FLAG_3,'N') NOT IN ('R'))
             
             '''%(
                  value_4,
                  value_5,
                  value_6
                 )

     df_1 = pd.read_sql_query(sql_1, con)
     df_2 = pd.read_sql_query(sql_2,con)

     df_1.index = ['Status']
     df_2.index = ['Status']

     df_3 = pd.merge(df_1, df_2, left_index=True, right_index=True).rename(columns = {'0_x':'Indirect Expense Budget','0_y':'Indirect Expenses'})

     y1 = df_3['INDIRECT_EXPENSE_BUDGET']
     y2 = df_3['ACTUAL_EXPENSE_AMOUNT']

     xcoord = df_3.index 

     annot_1 = [dict(
                x=xi,
                y=yi,
                text= str(yi),
                xanchor='left',
                xshift = -45,
                yanchor='bottom',
                showarrow=False,
                font=dict(
                          size = 11.5,
                         ),
                textangle=-90
                ) for xi, yi in zip(xcoord, y1)]

     annot_2 = [dict(
                x=xi,
                y=yi,
                text=str(yi),
                xanchor='left',
                xshift = 30,
                yanchor='bottom',
                showarrow=False,
                font=dict(
                          size = 11.5,
                         ),
                textangle=-90
                ) for xi, yi in zip(xcoord, y2)]


     annotations = annot_1 + annot_2

     return {
              'data': [ 
                             go.Bar (
                                      x = df_3.index,
                                      y = df_3['INDIRECT_EXPENSE_BUDGET'],
                                      name = 'Indirect Expense Budget',
                                      marker_color='rgb(255, 0, 0)'
                                    ),
                             go.Bar (
                                      x = df_3.index,
                                      y = df_3['ACTUAL_EXPENSE_AMOUNT'],
                                      name = 'Indirect Expense',
                                      marker_color='rgb(0, 153, 0)'
                                      
                                    ),
                    ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Comparison Status</b>',
                                         'showticklabels' : False,
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>Amount (Thousands)</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                annotations = annotations,
                                bargap = 0.8,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>Indirect Expense Budget Vs Indirect Actual Expense</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                legend = dict(orientation="h",yanchor="bottom", y=1.02, xanchor="right", x=1)
                               )
                             
            }
  else:
        return {}

@app.callback(Output('Graph-5','figure'),[Input('submit_button','n_clicks')],
                                         [State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('branch-dropdown','value')])
def update_graph_5(n_clicks,value_1, value_2, value_3):
  if n_clicks is not None and n_clicks > 0:
     con = cx.connect(config.CONN_STR)
     sql = '''SELECT
                  SUM(DWB_ARRIVED) AS TO_BE_DELIEVED
                 ,SUM(DWB_DLVRD_SAME_DAY) SAME_DAY
                 ,SUM(DLVRD_NEXT_DAY) NEXT_DAY
              FROM
                 CT_BA_DBA_DLY_PERFORMANCE
              WHERE
                 LAST_DAY(to_date(MONTH_YEAR ,'MMYYYY')) = LAST_DAY(to_date('%s%s','YYYYMM'))
                 AND DLY_BRANCH = NVL('%s',DLY_BRANCH)
            '''%(
                    value_1,
                    value_2,
                    value_3
               )
    
     df = pd.read_sql_query(sql, con)
     df.index = ['Status']

     y1 = df['TO_BE_DELIEVED']
     y2 = df['SAME_DAY']
     y3 = df['NEXT_DAY']

     xcoord = df.index 

     annot_1 = [dict(
                x=xi,
                y=yi,
                text= str(yi),
                xanchor='left',
                xshift = -60,
                yanchor='bottom',
                showarrow=False,
                font=dict(
                          size = 11.5,
                        ),
                textangle=-90
                ) for xi, yi in zip(xcoord, y1)]

     annot_2 = [dict(
                x=xi,
                y=yi,
                text=str(yi),
                xanchor='center',
                yanchor='bottom',
                showarrow=False,
                font=dict(
                          size = 11.5,
                         ),
                textangle=-90
                ) for xi, yi in zip(xcoord, y2)]

     annot_3 = [dict(
                x=xi,
                y=yi,
                text=str(yi),
                xanchor='left',
                xshift = 50,
                yanchor='bottom',
                showarrow=False,
                font=dict(
                          size = 11.5,
                         ),
                textangle=-90
                ) for xi, yi in zip(xcoord, y3)]


     annotations = annot_1 + annot_2 + annot_3

     return {
              'data': [ 
                             go.Bar (
                                      x = df.index,
                                      y = df['TO_BE_DELIEVED'],
                                      name = 'To Be Delieved',
                                      marker_color='rgb(0, 0, 255)'
                                    ),
                             go.Bar (
                                      x = df.index,
                                      y = df['SAME_DAY'],
                                      name = 'Same Day',
                                      marker_color='rgb(0, 153, 0)'
                                    ),
                             go.Bar (
                                      x = df.index,
                                      y = df['NEXT_DAY'],
                                      name = 'Next Day',
                                      marker_color='rgb(255, 0, 0)'
                                      
                                    ),
                    ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                         'title' : '<b>Delivery Status</b>',
                                         'showticklabels' : False,
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                yaxis = {
                                         'title' : '<b>DWB Numbers</b>',
                                         'showgrid':False,
                                         'zeroline':False,
                                        },
                                annotations = annotations,
                                bargap = 0.8,
                                barmode = 'group',
                                bargroupgap = 0.2,
                                title = '<b>DWB Delivery Status (Same Day - Next Day)</b>', 
                                hovermode = 'closest',
                                paper_bgcolor = '#e6e6e6',
                                legend = dict(orientation="h",yanchor="bottom", y=1.02, xanchor="right", x=1)
                               )
                             
            }
  else:
        return {}


