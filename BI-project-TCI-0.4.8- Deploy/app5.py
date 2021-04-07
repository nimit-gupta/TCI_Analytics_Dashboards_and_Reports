import dash
import pandas as pd
import numpy as np

import config
import flask
import cx_Oracle as cx
import plotly.graph_objs as go
from itertools import cycle

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State

app = dash.Dash(__name__, requests_pathname_prefix='/app5/', external_stylesheets = [dbc.themes.BOOTSTRAP])

con = cx.connect(config.CONN_STR)

sql_1 = '''
          SELECT
                TO_CHAR(TRUNC(SYSDATE - 1),'DD-MM-YYYY') CURRENT_DATE
          FROM 
               DUAL
       '''

df_1 = pd.read_sql_query(sql_1, con)

date = df_1['CURRENT_DATE'].squeeze()

sql_2 = ''' 
        SELECT 
            DISTINCT REGION_CODE 
        FROM  
            XM_BRANCHS 
        WHERE 
            STATUS LIKE 'VALID' 
            AND REGION_CODE <> 'XCRP'
        ORDER BY
            REGION_CODE ASC
     '''

df_2 = pd.read_sql_query(sql_2, con)
df_2['COPY_REGION_CODE'] = df_2['REGION_CODE']
df_2.loc[len(df_2)] = 'ALL INDIA'
df_2['COPY_REGION_CODE'].iloc[-1] = ''

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

sidebar = html.Div(
    [
        dcc.Dropdown(id ='region-dropdown',
                     options = [{'label': k, 'value' : v} for k, v in zip(df_2['REGION_CODE'], df_2['COPY_REGION_CODE'])],
                     placeholder = 'Region',
                     style = {'font-weight':'bold'}
                    ),
        html.Br(),
        dcc.Dropdown(id ='division-dropdown', 
                     placeholder = 'Division',
                     style = {'font-weight':'bold'}
                    ),
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
                      html.Div([dcc.Loading(dcc.Graph(id = 'Graph-2'))], style = {"margin-left": "18rem", "margin-right" : "2rem"})
                      ],style = {'width' : 'auto', 'background-color': '#f2f2f2'})

@app.callback(Output('division-dropdown','options'), [Input('region-dropdown','value')])

def set_division_options(selected_division):

     dict_div = {'SURFACE':'21','AIR':'22','ECOM':'23','RAIL':'24','GTA':'25','INTL':'26','C2C':'27','ALL DIVISIONS':''}

     return[{'label':l, 'value':m} for l, m in dict_div.items()]

@app.callback(Output('Graph-1','figure'),[Input('submit_button','n_clicks')],
                                         [State('region-dropdown','value'),\
                                          State('division-dropdown','value')
                                         ])

def update_graph_1(n_clicks, region, division):

    if n_clicks is not None and n_clicks > 0:

        con = cx.connect(config.CONN_STR)

        sql0 = '''
            SELECT 
                  to_Char(day,'DD-MM-YYYY') BOOKING_DAY
            FROM
                  (
                   SELECT TRUNC(SYSDATE, 'MM') + LEVEL - 1 AS day
                   FROM dual
                   CONNECT BY TRUNC(TRUNC(SYSDATE, 'MM') + LEVEL - 1, 'MM') = TRUNC(SYSDATE, 'MM')
                  )
            WHERE 
                  to_char(day, 'DY', 'nls_date_language=american') not in('SUN') 
           '''
        df0 = pd.read_sql_query(sql0, con)
    
        sql1 = '''
               SELECT
                     A.DAY BOOKING_DAY,
                     SUM(A.TOT_FREIGHT) FREIGHT
               FROM(
               
               SELECT
                    to_char(ct.DWB_BOOKING_DATE, 'DD-MM-YYYY') DAY,
                    ROUND(SUM(NVL(ct.TOT_FREIGHT,0))/100000,2) as TOT_FREIGHT
               FROM
                    CT_DWB ct
               LEFT JOIN
                    XM_BRANCHS xm on ct.BRANCH_BRANCH_CODE = xm.BRANCH_CODE
               WHERE
                    ct.DWB_BOOKING_DATE between trunc((sysdate),'month') and trunc(sysdate - 1)
                    AND xm.REGION_CODE = NVL('%(region)s',xm.REGION_CODE)
                    AND ct.DIVISION_CODE = NVL('%(division)s',ct.DIVISION_CODE)
                    AND xm.STATUS = 'VALID'
                    AND ct.URO_BASIS IS NULL
               GROUP BY
                    to_char(ct.DWB_BOOKING_DATE, 'DD-MM-YYYY')
               ) A
               GROUP BY
                    A.DAY
               ORDER BY
                    A.DAY
              
           '''%{'region' : region,'division' : division}
    
        df1 = pd.read_sql_query(sql1, con)
    
        sql2 = '''
             SELECT
                  (TARGET * 90)/100 TARGET_90,
                  (TARGET * 80)/100 TARGET_80
             FROM
                  (
                   SELECT 
                        ROUND((SUM(cm.BKG_FRT + cm.BKG_FRT_INT)/100000)/26, 2) TARGET
                   FROM 
                        CM_TARGET cm 
                   LEFT JOIN 
                        XM_BRANCHS xm ON cm.BRANCH_CODE = xm.BRANCH_CODE 
                   WHERE
                        to_date(cm.MONTH_YEAR,'MMYYYY') between trunc((sysdate),'month') and trunc(last_day(sysdate))
                        AND xm.REGION_CODE = NVL('%(region)s',xm.REGION_CODE)
                        AND cm.DIVISION_CODE = NVL('%(division)s',cm.DIVISION_CODE)
                   ) 
            '''%{'region' : region, 'division' : division}

        df3 = pd.read_sql_query(sql2, con)
    
        df4 = df0.merge(df1, on = 'BOOKING_DAY', how = 'left' )
    
        T1 = df3['TARGET_90'][0]
    
        T2 = df3['TARGET_80'][0]
    
        seq1 = cycle([T1])
    
        seq2 = cycle([T2])
    
        df4['Target_90'] = [next(seq1) for count in range(df4.shape[0])]
    
        df4['Target_80'] = [next(seq2) for count in range(df4.shape[0])]
    
        df4['CUM_FREIGHT'] = df4['FREIGHT'].cumsum()
    
        df4['CUM_Target_90'] = df4['Target_90'].cumsum()

        df4['CUM_Target_80'] = df4['Target_80'].cumsum()

        width0 = [3]
    
        width1 = [3]
    
        return {
                 'data': [ 
                             go.Scatter( 
                                         x= df4['BOOKING_DAY'],
                                         y= df4['CUM_Target_90'],
                                         mode = 'lines',
                                         name = '>= 90% of Daily Target - Good',
                                         marker_color='rgb(96, 128, 0)',
                                         line=dict(width=width0[0], dash = 'dash'),
                                       ),
                             go.Scatter(
                                         x=df4['BOOKING_DAY'],
                                         y=df4['CUM_Target_80'],
                                         mode = 'lines',
                                         name = '<= 90% - > 80% of Daily Target - Average',
                                         marker_color='rgb(255, 153, 0)',
                                         line=dict(width=width1[0], dash = 'dash'),
                                        ),
                             go.Bar(
                                         x=df4['BOOKING_DAY'],
                                         y=df4['CUM_FREIGHT'],
                                         name = 'Booking Freight',
                                         marker_color='rgb(3, 90, 252)'
                                      )
                 ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                          'title' : 'Booking Date',
                                          'showgrid':False,
                                          'zeroline':False,
                                        },
                                yaxis = {
                                          'title' : 'Freight in Lkhs',
                                          'showgrid':False,
                                          'zeroline':False,
                                          
                                        },
                                title={
                                       'text': "Daily Cumulative Booking Freight Trend" + " - " + str(region),
                                       'y':0.98,
                                       'x':0.5,
                                       'xanchor': 'center',
                                       'yanchor': 'top'
                                      },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                yaxis_range = [10,''],
                                showlegend = True,
                                paper_bgcolor = 'rgb(230, 225, 225)',
                                #plot_bgcolor = 'rgb(0, 0, 0)',
                                hovermode = 'x unified'
                            )

               }
    else:
        return {}

@app.callback(Output('Graph-2','figure'),[Input('submit_button','n_clicks')],
                                         [State('region-dropdown','value'),\
                                          State('division-dropdown','value')
                                         ])

def update_graph_2(n_clicks, region, division):

    if n_clicks is not None and n_clicks > 0:

        con = cx.connect(config.CONN_STR)

        sql11 = '''
            SELECT 
                  to_Char(day,'DD-MM-YYYY') BOOKING_DAY
            FROM
                  (
                   SELECT TRUNC(SYSDATE, 'MM') + LEVEL - 1 AS day
                   FROM dual
                   CONNECT BY TRUNC(TRUNC(SYSDATE, 'MM') + LEVEL - 1, 'MM') = TRUNC(SYSDATE, 'MM')
                  )
            WHERE 
                  to_char(day, 'DY', 'nls_date_language=american') not in('SUN') 
           '''
        df11 = pd.read_sql_query(sql11, con)
    
        sql22 = '''
               SELECT
                     A.DAY BOOKING_DAY,
                     SUM(A.TOT_WEIGHT) WEIGHT
               FROM(
               
               SELECT
                    to_char(ct.DWB_BOOKING_DATE, 'DD-MM-YYYY') DAY,
                    ROUND(SUM(NVL(ct.CHARGED_WEIGHT,0))/1000,2) as TOT_WEIGHT
               FROM
                    CT_DWB ct
               LEFT JOIN
                    XM_BRANCHS xm on ct.BRANCH_BRANCH_CODE = xm.BRANCH_CODE
               WHERE
                    ct.DWB_BOOKING_DATE between trunc((sysdate),'month') and trunc(sysdate - 1)
                    AND xm.REGION_CODE = NVL('%(region)s',xm.REGION_CODE)
                    AND ct.DIVISION_CODE = NVL('%(division)s',ct.DIVISION_CODE)
                    AND xm.STATUS = 'VALID'
                    AND ct.URO_BASIS IS NULL
               GROUP BY
                    to_char(ct.DWB_BOOKING_DATE, 'DD-MM-YYYY')
               ) A
               GROUP BY
                    A.DAY
               ORDER BY
                    A.DAY
              
           '''%{'region' : region, 'division' : division}
    
        df22 = pd.read_sql_query(sql22, con)
    
        sql33 = '''
             SELECT
                  (TARGET * 90)/100 TARGET_90,
                  (TARGET * 80)/100 TARGET_80
             FROM
                  (
                   SELECT 
                        ROUND((SUM(cm.BKG_WGT + BKG_WGT_INT)/1000)/26, 2) TARGET
                   FROM 
                        CM_TARGET cm 
                   LEFT JOIN 
                        XM_BRANCHS xm ON cm.BRANCH_CODE = xm.BRANCH_CODE 
                   WHERE
                        to_date(cm.MONTH_YEAR,'MMYYYY') between trunc((sysdate),'month') and trunc(last_day(sysdate))
                        AND xm.REGION_CODE = NVL('%(region)s',xm.REGION_CODE)
                        AND cm.DIVISION_CODE = NVL('%(division)s',cm.DIVISION_CODE)
                  ) 
            '''%{'region' : region,'division' : division}

        df33 = pd.read_sql_query(sql33, con)
    
        df44 = df11.merge(df22, on = 'BOOKING_DAY', how = 'left' )
    
        T11 = df33['TARGET_90'][0]
    
        T22 = df33['TARGET_80'][0]
    
        seq11 = cycle([T11])
    
        seq22 = cycle([T22])
    
        df44['Target_90'] = [next(seq11) for count in range(df44.shape[0])]
    
        df44['Target_80'] = [next(seq22) for count in range(df44.shape[0])]
    
        df44['CUM_WEIGHT'] = df44['WEIGHT'].cumsum()
    
        df44['CUM_Target_90'] = df44['Target_90'].cumsum()
    
        df44['CUM_Target_80'] = df44['Target_80'].cumsum()
    
        width00 = [3]
    
        width11 = [3]
    
        return {
                 'data': [ 
                             go.Scatter( 
                                         x= df44['BOOKING_DAY'],
                                         y= df44['CUM_Target_90'],
                                         mode = 'lines',
                                         name = '>= 90% of Daily Target - Good',
                                         marker_color='rgb(96, 128, 0)',
                                         line=dict(width=width00[0], dash = 'dash'),
                                       ),
                             go.Scatter(
                                         x=df44['BOOKING_DAY'],
                                         y=df44['CUM_Target_80'],
                                         mode = 'lines',
                                         name = '<= 90% - >80% of Daily Target - Average',
                                         marker_color='rgb(255, 153, 0)',
                                         line=dict(width=width11[0], dash = 'dash'),
                                        ),
                             go.Bar(
                                         x=df44['BOOKING_DAY'],
                                         y=df44['CUM_WEIGHT'],
                                         name = 'Booking Tons',
                                         marker_color='rgb(3, 90, 252)'
                                      )
                 ],

            'layout':  
                     go.Layout (
                                xaxis = {
                                          'title' : 'Booking Date',
                                          'showgrid':False,
                                          'zeroline':False,
                                        },
                                yaxis = {
                                          'title' : 'Weight in Tons',
                                          'showgrid':False,
                                          'zeroline':False,
                                          
                                        },
                                title={
                                       'text': "Daily Cumulative Booking Weight Trend" + " - " + str(region),
                                       'y':0.98,
                                       'x':0.5,
                                       'xanchor': 'center',
                                       'yanchor': 'top'
                                      },
                                legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                           ),
                                yaxis_range = [10,''],
                                showlegend = True,
                                paper_bgcolor = 'rgb(230, 225, 225)',
                                #plot_bgcolor = 'rgb(0, 0, 0)',
                                hovermode = 'x unified'
                            )

               }
    else:
        return {}

        

