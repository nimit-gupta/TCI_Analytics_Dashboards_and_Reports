import pandas as pd
import numpy as np
import cx_Oracle as cx

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go

import config 

app = dash.Dash(__name__, requests_pathname_prefix='/app6/', external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "rgb(230, 225, 225)",
    "overflow":"scroll"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.Div([html.H6('Division'),
                  dcc.Dropdown(
                               id = 'division-dropdown',
                               options = [{'label':'SURFACE','value': '21'},
                                          {'label':'AIR','value':'22'},
                                          {'label':'ECOM','value':'23'},
                                          {'label':'RAIL','value':'24'},
                                          {'label':'GTA','value':'25'},
                                          {'label':'AIR INTL','value':'26'},
                                          {'label':'C2C','value':'27'},
                                          {'label':'COLD CHAIN','value':'28'}, 
                                          {'label':'ALL','value':''}],
                               #placeholder = 'Division',
                               style = {'font-weight' : 'bold'})
                ]),
        html.Br(),
        html.Div([html.H6('Basis'),
                  dcc.Dropdown(
                               id = 'basis-dropdown',
                               options = [{'label':'PAID','value':'PAID'},
                                          {'label':'TBB','value':'TBB'},
                                          {'label':'FOD','value':'FOD'},
                                          {'label':'BOD','value':'BOD'},
                                          {'label':'ALL','value':'ALL'}],
                               #placeholder = 'Basis',
                               style = {'font-weight' : 'bold'}
                              )
                ]),
        html.Br(),
        html.Div([
                  dbc.Row([ 
                           dbc.Col([html.H6('Year'),
                                    dcc.Dropdown(
                                                 id = 'year-dropdown',
                                                 options = [{'label': p, 'value': p} for p in ['2020','2021']],
                                                 #placeholder = 'Year',
                                                 style = {'font-weight' : 'bold'}
                                                )
                                  ]),
                           dbc.Col([html.H6('Month'),
                                    dcc.Dropdown(
                                                 id = 'month-dropdown',
                                                 options = [{'label' : q, 'value' : q} for q in [ '01','02','03',\
                                                  '04','05','06',\
                                                  '07','08','09',\
                                                  '10','11','12']
                                                ],
                                                 #placeholder = 'Month',
                                                 style = {'font-weight' : 'bold'}
                                                 )
                                  ])
                          ])
                 ]),
        html.Br(),
        html.Div([html.H6('Period'),
                  dcc.Dropdown(
                                id = 'checklist-dropdown',
                                options=[
                                         {'label': ' For the Month', 'value':'FTM'},
                                         {'label': ' Up to the Month', 'value':'CUM'}
                                        ],
                                #placeholder = 'Period',
                                style = {'font-weight' : 'bold'}
                                
                               )  
                 ]),
        html.Br(),
        html.Div([
                  dcc.RadioItems(
                                 id = 'comparison-period-dropdown',
                                 options = [
                                            {'label' :'Between Months - No', 'value' : 'No'},
                                            {'label' :'Between Months - Yes','value' : 'Yes'}
                                           ],
                                 value = 'No',
                                 style = {'display' : 'block', 'font-weight' : 'bold', 'margin-left' : '2rem'}
                                )
         ]), 
        html.Br(),
        html.Div([
                  dbc.Row([ 
                           dbc.Col([
                                    dcc.Dropdown(
                                                 id = 'visible-year-dropdown',
                                                 options = [{'label': p, 'value': p} for p in ['2020','2021']],
                                                 value = ' ',
                                                 style = {'display':'none','font-weight' : 'bold'}
                                                )
                                  ]),
                           dbc.Col([
                                    dcc.Dropdown(
                                                 id = 'visible-month-dropdown',
                                                 options = [{'label' : q, 'value' : q} for q in [ '01','02','03',\
                                                  '04','05','06',\
                                                  '07','08','09',\
                                                  '10','11','12']
                                                ],
                                                 value = ' ',
                                                 style = {'display':'none','font-weight' : 'bold'}
                                                 )
                                  ])
                          ])
                 ]),
        html.Br(),                            
        html.Div([
                  dbc.Row([
                            dbc.Col([
                                      html.Button(
                                                    'Submit',
                                                    id = 'submit_button',
                                                    type = 'submit',
                                                    style = {'height':'35px','display':'inline-block',\
                                                                                    'background-color': '#ffffff',\
                                                                                    'font-weight':'bold', 'border-radius':'4px'}
                                                )
                                    ]),
                            dbc.Col([
                                      html.A(
                                                html.Button('Refresh', style = {'height':'35px','display':'inline-block',\
                                                                                        'background-color': '#ffffff',\
                                                                                        'font-weight':'bold', 'border-radius':'4px'}),
                                                href = '/app6/',
                                                )
                                    ])
                          ]) 
                 ])              

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
                      ],style = {'width' : 'auto', 'background-color': '#f2f2f2'})

@app.callback(Output('comparison-period-dropdown','style'),[
                                                            Input('checklist-dropdown','value')
                                                           ])
def visible_checklist(checklist):
    if checklist == 'FTM':
       return {'display' : 'block', 'font-weight' : 'bold'}
    elif checklist == 'CUM':
       return {'display' : 'none', 'font-weight' : 'bold'}  
    else:
       return {'display' : 'none', 'font-weight' : 'bold'}

@app.callback(Output('visible-year-dropdown','style'),[
                                                       Input('comparison-period-dropdown','value')
                                                      ])
def visible_year(visible):
    if visible == 'Yes':
        return {'display' : 'block','font-weight' : 'bold'}
    elif visible == 'No':
        return {'display' : 'none','font-weight' : 'bold'}
    else:
        return {'display' : 'none','font-weight' : 'bold'}

@app.callback(Output('visible-month-dropdown','style'),[
                                                        Input('comparison-period-dropdown','value')
                                                      ])
def visible_month( visible):
    if visible == 'Yes':
        return {'display' : 'block','font-weight' : 'bold'}
    elif visible == 'No':
        return {'display' : 'none','font-weight' : 'bold'}
    else:
        return {'display' : 'none','font-weight' : 'bold'}

@app.callback(Output('Graph-1','figure'),[Input('submit_button','n_clicks')],
                                         [State('division-dropdown','value'),\
                                          State('basis-dropdown','value'),\
                                          State('checklist-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('visible-year-dropdown', 'value'),\
                                          State('visible-month-dropdown','value')])

def update_graph_1(n_clicks, division, basis, checklist, year, month, year_1, month_1):

    if n_clicks is not None and n_clicks > 0:

        con = cx.connect(config.CONN_STR)
        
        if basis == 'PAID':

            if checklist == 'FTM':

                if year_1 == ' ' and month_1 == ' ':
                   
                    sql = '''
                        SELECT
                            REGION_CODE REGION
                            ,ROUND(SUM(NVL(PAID_FRT,0))/100000,2) CYF
                            ,ROUND(SUM(NVL(LYA_PAID_FRT,0))/100000,2) LYF
                            ,ROUND((SUM(NVL(PAID_FRT,0)) - SUM(NVL(LYA_PAID_FRT,0)))/100000,2) GP
                        FROM
                            CT_BUSINESS_GROWTH_NEW_IMPL
                        WHERE
                            LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                                                                                                  AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                            AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                            AND REGION_CODE <> 'XCRP'
                        GROUP BY
                            REGION_CODE
                        ORDER BY
                            REGION_CODE
                            '''%{'year':year, 'month':month, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYF']
                    y2 = df['CYF']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYF'],
                                    name = 'LYF',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYF'],
                                    name = 'CYF',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise Freight Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="Freight (in Lkhs)", showgrid = False)
                                            )

                            }

                elif year_1 != ' ' and month_1 != ' ':

                    sql = '''
                        SELECT
                            REGION_CODE REGION
                            ,ROUND(SUM(NVL(PAID_FRT,0))/100000,2) CYF
                            ,ROUND(SUM(NVL(LYA_PAID_FRT,0))/100000,2) LYF
                            ,ROUND((SUM(NVL(PAID_FRT,0)) - SUM(NVL(LYA_PAID_FRT,0)))/100000,2) GP
                        FROM
                            CT_BUSINESS_GROWTH_NEW_IMPL
                        WHERE
                            LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN Last_day(TO_DATE('%(year_1)s%(month_1)s','YYYYMM'))
                                                                                                                    AND Last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                            AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                            AND REGION_CODE <> 'XCRP'
                        GROUP BY
                            REGION_CODE
                        ORDER BY
                            REGION_CODE
                            '''%{'year':year, 'month':month, 'year_1':year_1,'month_1':month_1, 'division': division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYF']
                    y2 = df['CYF']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYF'],
                                    name = 'LYF',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYF'],
                                    name = 'CYF',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise Freight Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="Freight (in Lkhs)", showgrid = False)
                                            )

                            }
            
            elif checklist == 'CUM':
    
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(PAID_FRT,0))/100000,2) CYF
                                ,ROUND(SUM(NVL(LYA_PAID_FRT,0))/100000,2) LYF
                                ,ROUND((SUM(NVL(PAID_FRT,0)) - SUM(NVL(LYA_PAID_FRT,0)))/100000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                        '''%{'year':year, 'month':month,'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYF']
                    y2 = df['CYF']
                    y3 = df['GP']
                    x1 = df['REGION']
            
                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                    
                    return {
                            'data': [
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['LYF'],
                                        name = 'LYF',
                                        marker_color='rgb(242, 109, 7)'),
                    
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['CYF'],
                                        name = 'CYF',
                                        marker_color='rgb(7, 128, 242)'),
                        
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['GP'],
                                        name = 'Growth',
                                        marker_color= df['color'])
                                   ],
                            'layout' : go.Layout(
                                                 title={
                                                        'text': "Region Wise Freight Comparison LY Vs CY",
                                                        'y':0.98,
                                                        'x':0.5,
                                                        'xanchor': 'center',
                                                        'yanchor': 'top'
                                                       },
                                                annotations = annotations,
                                                barmode = 'group',
                                                bargroupgap = 0.1,
                                                legend=dict(
                                                orientation="h",
                                                yanchor="bottom",
                                                y=1.02,
                                                xanchor="right",
                                                x=1
                                                ),
                                                showlegend = True,
                                                xaxis=dict(title="Region", showgrid = False),
                                                yaxis=dict(title="Freight (in Lkhs)", showgrid = False)
                                                )
                        
                        }
            else:
                return{}

        elif basis == 'TBB':
        
            if checklist == 'FTM':

                if year_1 == ' ' and month_1 == ' ':
            
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(TBB_FRT,0))/100000,2) CYF
                                ,ROUND(SUM(NVL(LYA_TBB_FRT,0))/100000,2) LYF
                                ,ROUND((SUM(NVL(TBB_FRT,0)) - SUM(NVL(LYA_TBB_FRT,0)))/100000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                                                                                                      AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))                                                                         
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYF']
                    y2 = df['CYF']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                        
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYF'],
                                    name = 'LYF',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYF'],
                                    name = 'CYF',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise Freight Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="Freight (in Lkhs)", showgrid = False)
                                            )

                    }
                
                elif year_1 != ' ' and month_1 != ' ':
            
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(TBB_FRT,0))/100000,2) CYF
                                ,ROUND(SUM(NVL(LYA_TBB_FRT,0))/100000,2) LYF
                                ,ROUND((SUM(NVL(TBB_FRT,0)) - SUM(NVL(LYA_TBB_FRT,0)))/100000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                 LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN Last_day(TO_DATE('%(year_1)s%(month_1)s','YYYYMM'))
                                                                                                                   AND Last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))                                                                        
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'year_1':year_1,'month_1':month_1, 'division': division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYF']
                    y2 = df['CYF']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                        
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYF'],
                                    name = 'LYF',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYF'],
                                    name = 'CYF',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise Freight Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="Freight (in Lkhs)", showgrid = False)
                                            )

                    }

            
            elif checklist == 'CUM':
    
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(TBB_FRT,0))/100000,2) CYF
                                ,ROUND(SUM(NVL(LYA_TBB_FRT,0))/100000,2) LYF
                                ,ROUND((SUM(NVL(TBB_FRT,0)) - SUM(NVL(LYA_TBB_FRT,0)))/100000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                        '''%{'year':year, 'month':month,'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYF']
                    y2 = df['CYF']
                    y3 = df['GP']
                    x1 = df['REGION']
            
                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                    
                    return {
                            'data': [
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['LYF'],
                                        name = 'LYF',
                                        marker_color='rgb(242, 109, 7)'),
                    
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['CYF'],
                                        name = 'CYF',
                                        marker_color='rgb(7, 128, 242)'),
                        
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['GP'],
                                        name = 'Growth',
                                        marker_color= df['color'])
                                   ],
                            'layout' : go.Layout(
                                                 title={
                                                        'text': "Region Wise Freight Comparison LY Vs CY",
                                                        'y':0.98,
                                                        'x':0.5,
                                                        'xanchor': 'center',
                                                        'yanchor': 'top'
                                                       },
                                                annotations = annotations,
                                                barmode = 'group',
                                                bargroupgap = 0.1,
                                                legend=dict(
                                                orientation="h",
                                                yanchor="bottom",
                                                y=1.02,
                                                xanchor="right",
                                                x=1
                                                ),
                                                showlegend = True,
                                                xaxis=dict(title="Region", showgrid = False),
                                                yaxis=dict(title="Freight (in Lkhs)", showgrid = False)
                                                )
                        
                        }
            else:
                return{}

        elif basis == 'FOD':
        
            if checklist == 'FTM':

                if year_1 == ' ' and month_1 == ' ':
            
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(FOD_FRT,0))/100000,2) CYF
                                ,ROUND(SUM(NVL(LYA_FOD_FRT,0))/100000,2) LYF
                                ,ROUND((SUM(NVL(FOD_FRT,0)) - SUM(NVL(LYA_FOD_FRT,0)))/100000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                                                                                                  AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYF']
                    y2 = df['CYF']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYF'],
                                    name = 'LYF',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYF'],
                                    name = 'CYF',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise Freight Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="Freight (in Lkhs)", showgrid = False)
                                            )

                    }

                elif year_1 != ' ' and month_1 != ' ':
                
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(FOD_FRT,0))/100000,2) CYF
                                ,ROUND(SUM(NVL(LYA_FOD_FRT,0))/100000,2) LYF
                                ,ROUND((SUM(NVL(FOD_FRT,0)) - SUM(NVL(LYA_FOD_FRT,0)))/100000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year_1)s%(month_1)s','YYYYMM'))
                                                                                                                  AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'year_1': year_1, 'month_1': month_1, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYF']
                    y2 = df['CYF']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYF'],
                                    name = 'LYF',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYF'],
                                    name = 'CYF',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise Freight Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="Freight (in Lkhs)", showgrid = False)
                                            )

                    }
            
            elif checklist == 'CUM':
    
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(FOD_FRT,0))/100000,2) CYF
                                ,ROUND(SUM(NVL(LYA_FOD_FRT,0))/100000,2) LYF
                                ,ROUND((SUM(NVL(FOD_FRT,0)) - SUM(NVL(LYA_FOD_FRT,0)))/100000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                        '''%{'year':year, 'month':month,'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYF']
                    y2 = df['CYF']
                    y3 = df['GP']
                    x1 = df['REGION']
            
                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                    
                    return {
                            'data': [
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['LYF'],
                                        name = 'LYF',
                                        marker_color='rgb(242, 109, 7)'),
                    
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['CYF'],
                                        name = 'CYF',
                                        marker_color='rgb(7, 128, 242)'),
                        
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['GP'],
                                        name = 'Growth',
                                        marker_color= df['color'])
                                   ],
                            'layout' : go.Layout(
                                                 title={
                                                        'text': "Region Wise Freight Comparison LY Vs CY",
                                                        'y':0.98,
                                                        'x':0.5,
                                                        'xanchor': 'center',
                                                        'yanchor': 'top'
                                                       },
                                                annotations = annotations,
                                                barmode = 'group',
                                                bargroupgap = 0.1,
                                                legend=dict(
                                                orientation="h",
                                                yanchor="bottom",
                                                y=1.02,
                                                xanchor="right",
                                                x=1
                                                ),
                                                showlegend = True,
                                                xaxis=dict(title="Region", showgrid = False),
                                                yaxis=dict(title="Freight (in Lkhs)", showgrid = False)
                                                )
                        
                        }
            else:
                return{}

        elif basis == 'BOD':
        
            if checklist == 'FTM':

                if year_1 == ' ' and month_1 == ' ':
            
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(BOD_FRT,0))/100000,2) CYF
                                ,ROUND(SUM(NVL(LYA_BOD_FRT,0))/100000,2) LYF
                                ,ROUND((SUM(NVL(BOD_FRT,0)) - SUM(NVL(LYA_BOD_FRT,0)))/100000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                                                                                                      AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYF']
                    y2 = df['CYF']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYF'],
                                    name = 'LYF',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYF'],
                                    name = 'CYF',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise Freight Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="Freight (in Lkhs)", showgrid = False)
                                            )

                    }

                elif year_1 != ' ' and month_1 != ' ':
                
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(BOD_FRT,0))/100000,2) CYF
                                ,ROUND(SUM(NVL(LYA_BOD_FRT,0))/100000,2) LYF
                                ,ROUND((SUM(NVL(BOD_FRT,0)) - SUM(NVL(LYA_BOD_FRT,0)))/100000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year_1)s%(month_1)s','YYYYMM'))
                                                                                                                      AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'year_1': year_1, 'month_1': month_1, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYF']
                    y2 = df['CYF']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYF'],
                                    name = 'LYF',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYF'],
                                    name = 'CYF',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise Freight Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="Freight (in Lkhs)", showgrid = False)
                                            )

                    }
            
            
            elif checklist == 'CUM':
    
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(BOD_FRT,0))/100000,2) CYF
                                ,ROUND(SUM(NVL(LYA_BOD_FRT,0))/100000,2) LYF
                                ,ROUND((SUM(NVL(BOD_FRT,0)) - SUM(NVL(LYA_BOD_FRT,0)))/100000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                        '''%{'year':year, 'month':month,'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYF']
                    y2 = df['CYF']
                    y3 = df['GP']
                    x1 = df['REGION']
            
                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                    
                    return {
                            'data': [
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['LYF'],
                                        name = 'LYF',
                                        marker_color='rgb(242, 109, 7)'),
                    
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['CYF'],
                                        name = 'CYF',
                                        marker_color='rgb(7, 128, 242)'),
                        
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['GP'],
                                        name = 'Growth',
                                        marker_color= df['color'])
                                   ],
                            'layout' : go.Layout(
                                                 title={
                                                        'text': "Region Wise Freight Comparison LY Vs CY",
                                                        'y':0.98,
                                                        'x':0.5,
                                                        'xanchor': 'center',
                                                        'yanchor': 'top'
                                                       },
                                                annotations = annotations,
                                                barmode = 'group',
                                                bargroupgap = 0.1,
                                                legend=dict(
                                                orientation="h",
                                                yanchor="bottom",
                                                y=1.02,
                                                xanchor="right",
                                                x=1
                                                ),
                                                showlegend = True,
                                                xaxis=dict(title="Region", showgrid = False),
                                                yaxis=dict(title="Freight (in Lkhs)", showgrid = False)
                                                )
                        
                        }
            else:
                return{}
        
        elif basis == 'ALL':
        
            if checklist == 'FTM':

                if year_1 == ' ' and month_1 == ' ':
            
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(PAID_FRT,0) + NVL(TBB_FRT,0) + NVL(FOD_FRT,0) + NVL(BOD_FRT,0))/100000,2) CYF
                                ,ROUND(SUM(NVL(LYA_PAID_FRT,0) + NVL(LYA_TBB_FRT,0) + NVL(LYA_FOD_FRT,0) + NVL(LYA_BOD_FRT,0))/100000, 2) LYF
                                ,ROUND((SUM(NVL(PAID_FRT,0) + NVL(TBB_FRT,0) + NVL(FOD_FRT,0) + NVL(BOD_FRT,0)) 
                                - SUM(NVL(LYA_PAID_FRT,0) + NVL(LYA_TBB_FRT,0) + NVL(LYA_FOD_FRT,0) + NVL(LYA_BOD_FRT,0)))/100000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                                                                                                  AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYF']
                    y2 = df['CYF']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYF'],
                                    name = 'LYF',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYF'],
                                    name = 'CYF',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise Freight Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="Freight (in Lkhs)", showgrid = False)
                                            )

                    }

                elif year_1 != ' ' and month_1 != ' ':
                
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(PAID_FRT,0) + NVL(TBB_FRT,0) + NVL(FOD_FRT,0) + NVL(BOD_FRT,0))/100000,2) CYF
                                ,ROUND(SUM(NVL(LYA_PAID_FRT,0) + NVL(LYA_TBB_FRT,0) + NVL(LYA_FOD_FRT,0) + NVL(LYA_BOD_FRT,0))/100000, 2) LYF
                                ,ROUND((SUM(NVL(PAID_FRT,0) + NVL(TBB_FRT,0) + NVL(FOD_FRT,0) + NVL(BOD_FRT,0)) 
                                - SUM(NVL(LYA_PAID_FRT,0) + NVL(LYA_TBB_FRT,0) + NVL(LYA_FOD_FRT,0) + NVL(LYA_BOD_FRT,0)))/100000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year_1)s%(month_1)s','YYYYMM'))
                                                                                                                  AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'year_1':year_1, 'month_1':month_1, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYF']
                    y2 = df['CYF']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYF'],
                                    name = 'LYF',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYF'],
                                    name = 'CYF',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise Freight Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="Freight (in Lkhs)", showgrid = False)
                                            )

                    }
            
            
            elif checklist == 'CUM':
    
                    sql = '''
                            SELECT
                                 REGION_CODE REGION
                                ,ROUND(SUM(NVL(PAID_FRT,0) + NVL(TBB_FRT,0) + NVL(FOD_FRT,0) + NVL(BOD_FRT,0))/100000,2) CYF
                                ,ROUND(SUM(NVL(LYA_PAID_FRT,0) + NVL(LYA_TBB_FRT,0) + NVL(LYA_FOD_FRT,0) + NVL(LYA_BOD_FRT,0))/100000, 2) LYF
                                ,ROUND((SUM(NVL(PAID_FRT,0) + NVL(TBB_FRT,0) + NVL(FOD_FRT,0) + NVL(BOD_FRT,0)) 
                                - SUM(NVL(LYA_PAID_FRT,0) + NVL(LYA_TBB_FRT,0) + NVL(LYA_FOD_FRT,0) + NVL(LYA_BOD_FRT,0)))/100000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                        '''%{'year':year, 'month':month,'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYF']
                    y2 = df['CYF']
                    y3 = df['GP']
                    x1 = df['REGION']
            
                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                    
                    return {
                            'data': [
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['LYF'],
                                        name = 'LYF',
                                        marker_color='rgb(242, 109, 7)'),
                    
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['CYF'],
                                        name = 'CYF',
                                        marker_color='rgb(7, 128, 242)'),
                        
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['GP'],
                                        name = 'Growth',
                                        marker_color= df['color'])
                                   ],
                            'layout' : go.Layout(
                                                 title={
                                                        'text': "Region Wise Freight Comparison LY Vs CY",
                                                        'y':0.98,
                                                        'x':0.5,
                                                        'xanchor': 'center',
                                                        'yanchor': 'top'
                                                       },
                                                annotations = annotations,
                                                barmode = 'group',
                                                bargroupgap = 0.1,
                                                legend=dict(
                                                orientation="h",
                                                yanchor="bottom",
                                                y=1.02,
                                                xanchor="right",
                                                x=1
                                                ),
                                                showlegend = True,
                                                xaxis=dict(title="Region", showgrid = False),
                                                yaxis=dict(title="Freight (in Lkhs)", showgrid = False)
                                                )
                        
                        }
            else:
                return{}
    else:
        return {}
        
@app.callback(Output('Graph-2','figure'),[Input('submit_button','n_clicks')],
                                         [State('division-dropdown','value'),\
                                          State('basis-dropdown','value'),\
                                          State('checklist-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('visible-year-dropdown', 'value'),\
                                          State('visible-month-dropdown','value')])

def update_graph_2(n_clicks, division, basis, checklist, year, month, year_1, month_1):

    if n_clicks is not None and n_clicks > 0:
    
        con = cx.connect(config.CONN_STR)
        
        if basis == 'PAID':

            if checklist == 'FTM':

                if year_1 == ' ' and month_1 == ' ':
            
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(PAID_WT,0))/1000,2) CYW
                                ,ROUND(SUM(NVL(LYA_PAID_WT,0))/1000,2) LYW
                                ,ROUND((SUM(NVL(PAID_WT,0)) - SUM(NVL(LYA_PAID_WT,0)))/1000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                                                                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYW']
                    y2 = df['CYW']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYW'],
                                    name = 'LYW',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYW'],
                                    name = 'CYW',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise Weight Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="Weight (in Tons)", showgrid = False)
                                            )

                    }
                    
                elif year_1 != ' ' and month_1 != ' ':

                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(PAID_WT,0))/1000,2) CYW
                                ,ROUND(SUM(NVL(LYA_PAID_WT,0))/1000,2) LYW
                                ,ROUND((SUM(NVL(PAID_WT,0)) - SUM(NVL(LYA_PAID_WT,0)))/1000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year_1)s%(month_1)s','YYYYMM'))
                                                                                                                  AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'year_1':year_1, 'month_1':month_1, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYW']
                    y2 = df['CYW']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYW'],
                                    name = 'LYW',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYW'],
                                    name = 'CYW',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise Weight Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="Weight (in Tons)", showgrid = False)
                                            )

                    }
                  
            elif checklist == 'CUM':
    
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(PAID_WT,0))/1000,2) CYW
                                ,ROUND(SUM(NVL(LYA_PAID_WT,0))/1000,2) LYW
                                ,ROUND((SUM(NVL(PAID_WT,0)) - SUM(NVL(LYA_PAID_WT,0)))/1000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                        '''%{'year':year, 'month':month,'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYW']
                    y2 = df['CYW']
                    y3 = df['GP']
                    x1 = df['REGION']
            
                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                    
                    return {
                            'data': [
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['LYW'],
                                        name = 'LYW',
                                        marker_color='rgb(242, 109, 7)'),
                    
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['CYW'],
                                        name = 'CYW',
                                        marker_color='rgb(7, 128, 242)'),
                        
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['GP'],
                                        name = 'Growth',
                                        marker_color= df['color'])
                                   ],
                            'layout' : go.Layout(
                                                 title={
                                                        'text': "Region Wise Weight Comparison LY Vs CY",
                                                        'y':0.98,
                                                        'x':0.5,
                                                        'xanchor': 'center',
                                                        'yanchor': 'top'
                                                       },
                                                annotations = annotations,
                                                barmode = 'group',
                                                bargroupgap = 0.1,
                                                legend=dict(
                                                orientation="h",
                                                yanchor="bottom",
                                                y=1.02,
                                                xanchor="right",
                                                x=1
                                                ),
                                                showlegend = True,
                                                xaxis=dict(title="Region", showgrid = False),
                                                yaxis=dict(title="Weight (in Tons)", showgrid = False)
                                                )
                        
                        }
            else:
                return{}
        
        elif basis == 'TBB':
    
            if checklist == 'FTM':

                if year_1 == ' ' and month_1 == ' ':
            
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(TBB_WT,0))/1000,2) CYW
                                ,ROUND(SUM(NVL(LYA_TBB_WT,0))/1000,2) LYW
                                ,ROUND((SUM(NVL(TBB_WT,0)) - SUM(NVL(LYA_TBB_WT,0)))/1000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                                                                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYW']
                    y2 = df['CYW']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYW'],
                                    name = 'LYW',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYW'],
                                    name = 'CYW',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise Weight Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="Weight (in Tons)", showgrid = False)
                                            )

                    }

                elif year_1 != ' ' and month_1 != ' ':

                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(TBB_WT,0))/1000,2) CYW
                                ,ROUND(SUM(NVL(LYA_TBB_WT,0))/1000,2) LYW
                                ,ROUND((SUM(NVL(TBB_WT,0)) - SUM(NVL(LYA_TBB_WT,0)))/1000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year_1)s%(month_1)s','YYYYMM'))
                                                                                                                  AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'year_1':year_1, 'month_1':month_1, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYW']
                    y2 = df['CYW']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYW'],
                                    name = 'LYW',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYW'],
                                    name = 'CYW',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise Weight Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="Weight (in Tons)", showgrid = False)
                                            )

                    }       
            
            elif checklist == 'CUM':
    
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(TBB_WT,0))/1000,2) CYW
                                ,ROUND(SUM(NVL(LYA_TBB_WT,0))/1000,2) LYW
                                ,ROUND((SUM(NVL(TBB_WT,0)) - SUM(NVL(LYA_TBB_WT,0)))/1000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                        '''%{'year':year, 'month':month,'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYW']
                    y2 = df['CYW']
                    y3 = df['GP']
                    x1 = df['REGION']
            
                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                    
                    return {
                            'data': [
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['LYW'],
                                        name = 'LYW',
                                        marker_color='rgb(242, 109, 7)'),
                    
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['CYW'],
                                        name = 'CYW',
                                        marker_color='rgb(7, 128, 242)'),
                        
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['GP'],
                                        name = 'Growth',
                                        marker_color= df['color'])
                                   ],
                            'layout' : go.Layout(
                                                 title={
                                                        'text': "Region Wise Weight Comparison LY Vs CY",
                                                        'y':0.98,
                                                        'x':0.5,
                                                        'xanchor': 'center',
                                                        'yanchor': 'top'
                                                       },
                                                annotations = annotations,
                                                barmode = 'group',
                                                bargroupgap = 0.1,
                                                legend=dict(
                                                orientation="h",
                                                yanchor="bottom",
                                                y=1.02,
                                                xanchor="right",
                                                x=1
                                                ),
                                                showlegend = True,
                                                xaxis=dict(title="Region", showgrid = False),
                                                yaxis=dict(title="Weight (in Tons)", showgrid = False)
                                                )
                        
                        }
            else:
                return{}

        elif basis == 'FOD':
    
            if checklist == 'FTM':

                if year_1 == ' ' and month_1 == ' ':
            
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(FOD_WT,0))/1000,2) CYW
                                ,ROUND(SUM(NVL(LYA_FOD_WT,0))/1000,2) LYW
                                ,ROUND((SUM(NVL(FOD_WT,0)) - SUM(NVL(LYA_FOD_WT,0)))/1000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                                                                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYW']
                    y2 = df['CYW']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYW'],
                                    name = 'LYW',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYW'],
                                    name = 'CYW',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise Weight Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="Weight (in Tons)", showgrid = False)
                                            )

                    }

                elif year_1 != ' ' and month_1 != ' ':

                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(FOD_WT,0))/1000,2) CYW
                                ,ROUND(SUM(NVL(LYA_FOD_WT,0))/1000,2) LYW
                                ,ROUND((SUM(NVL(FOD_WT,0)) - SUM(NVL(LYA_FOD_WT,0)))/1000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year_1)s%(month_1)s','YYYYMM'))
                                                                                                                  AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'year_1':year_1, 'month_1':month_1, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYW']
                    y2 = df['CYW']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYW'],
                                    name = 'LYW',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYW'],
                                    name = 'CYW',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise Weight Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="Weight (in Tons)", showgrid = False)
                                            )

                    }        
                
            elif checklist == 'CUM':
    
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(FOD_WT,0))/1000,2) CYW
                                ,ROUND(SUM(NVL(LYA_FOD_WT,0))/1000,2) LYW
                                ,ROUND((SUM(NVL(FOD_WT,0)) - SUM(NVL(LYA_FOD_WT,0)))/1000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                        '''%{'year':year, 'month':month,'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYW']
                    y2 = df['CYW']
                    y3 = df['GP']
                    x1 = df['REGION']
            
                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                    
                    return {
                            'data': [
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['LYW'],
                                        name = 'LYW',
                                        marker_color='rgb(242, 109, 7)'),
                    
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['CYW'],
                                        name = 'CYW',
                                        marker_color='rgb(7, 128, 242)'),
                        
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['GP'],
                                        name = 'Growth',
                                        marker_color= df['color'])
                                   ],
                            'layout' : go.Layout(
                                                 title={
                                                        'text': "Region Wise Weight Comparison LY Vs CY",
                                                        'y':0.98,
                                                        'x':0.5,
                                                        'xanchor': 'center',
                                                        'yanchor': 'top'
                                                       },
                                                annotations = annotations,
                                                barmode = 'group',
                                                bargroupgap = 0.1,
                                                legend=dict(
                                                orientation="h",
                                                yanchor="bottom",
                                                y=1.02,
                                                xanchor="right",
                                                x=1
                                                ),
                                                showlegend = True,
                                                xaxis=dict(title="Region", showgrid = False),
                                                yaxis=dict(title="Weight (in Tons)", showgrid = False)
                                                )
                        
                        }
            else:
                return{}

        elif basis == 'BOD':
    
            if checklist == 'FTM':

                if year_1 == ' ' and month_1 == ' ':
            
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(BOD_WT,0))/1000,2) CYW
                                ,ROUND(SUM(NVL(LYA_BOD_WT,0))/1000,2) LYW
                                ,ROUND((SUM(NVL(BOD_WT,0)) - SUM(NVL(LYA_BOD_WT,0)))/1000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                                                                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYW']
                    y2 = df['CYW']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYW'],
                                    name = 'LYW',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYW'],
                                    name = 'CYW',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise Weight Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="Weight (in Tons)", showgrid = False)
                                            )

                    }

                elif year_1 != ' ' and month_1 != ' ':
                     
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(BOD_WT,0))/1000,2) CYW
                                ,ROUND(SUM(NVL(LYA_BOD_WT,0))/1000,2) LYW
                                ,ROUND((SUM(NVL(BOD_WT,0)) - SUM(NVL(LYA_BOD_WT,0)))/1000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year_1)s%(month_1)s','YYYYMM'))
                                                                                                                  AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'year_1':year_1, 'month_1':month_1, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYW']
                    y2 = df['CYW']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYW'],
                                    name = 'LYW',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYW'],
                                    name = 'CYW',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise Weight Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="Weight (in Tons)", showgrid = False)
                                            )

                    }
  
            elif checklist == 'CUM':
    
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(BOD_WT,0))/1000,2) CYW
                                ,ROUND(SUM(NVL(LYA_BOD_WT,0))/1000,2) LYW
                                ,ROUND((SUM(NVL(BOD_WT,0)) - SUM(NVL(LYA_BOD_WT,0)))/1000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                        '''%{'year':year, 'month':month,'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYW']
                    y2 = df['CYW']
                    y3 = df['GP']
                    x1 = df['REGION']
            
                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                    
                    return {
                            'data': [
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['LYW'],
                                        name = 'LYW',
                                        marker_color='rgb(242, 109, 7)'),
                    
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['CYW'],
                                        name = 'CYW',
                                        marker_color='rgb(7, 128, 242)'),
                        
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['GP'],
                                        name = 'Growth',
                                        marker_color= df['color'])
                                   ],
                            'layout' : go.Layout(
                                                 title={
                                                        'text': "Region Wise Weight Comparison LY Vs CY",
                                                        'y':0.98,
                                                        'x':0.5,
                                                        'xanchor': 'center',
                                                        'yanchor': 'top'
                                                       },
                                                annotations = annotations,
                                                barmode = 'group',
                                                bargroupgap = 0.1,
                                                legend=dict(
                                                orientation="h",
                                                yanchor="bottom",
                                                y=1.02,
                                                xanchor="right",
                                                x=1
                                                ),
                                                showlegend = True,
                                                xaxis=dict(title="Region", showgrid = False),
                                                yaxis=dict(title="Weight (in Tons)", showgrid = False)
                                                )
                        
                        }
            else:
                return{}

        elif basis == 'ALL':
    
            if checklist == 'FTM':

                if year_1 == ' ' and month_1 == ' ':
            
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(PAID_WT,0) + NVL(TBB_WT,0) + NVL(FOD_WT,0) + NVL(BOD_WT,0))/1000,2) CYW
                                ,ROUND(SUM(NVL(LYA_PAID_WT,0) + NVL(LYA_TBB_WT,0) + NVL(LYA_FOD_WT,0) + NVL(LYA_BOD_WT,0))/1000, 2) LYW
                                ,ROUND((SUM(NVL(PAID_WT,0) + NVL(TBB_WT,0) + NVL(FOD_WT,0) + NVL(BOD_WT,0)) 
                                - SUM(NVL(LYA_PAID_WT,0) + NVL(LYA_TBB_WT,0) + NVL(LYA_FOD_WT,0) + NVL(LYA_BOD_WT,0)))/1000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                                                                                                  AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYW']
                    y2 = df['CYW']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYW'],
                                    name = 'LYW',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYW'],
                                    name = 'CYW',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise Weight Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="Weight (in Tons)", showgrid = False)
                                            )

                    }

                elif year_1 != ' ' and month_1 != ' ':

                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(PAID_WT,0) + NVL(TBB_WT,0) + NVL(FOD_WT,0) + NVL(BOD_WT,0))/1000,2) CYW
                                ,ROUND(SUM(NVL(LYA_PAID_WT,0) + NVL(LYA_TBB_WT,0) + NVL(LYA_FOD_WT,0) + NVL(LYA_BOD_WT,0))/1000, 2) LYW
                                ,ROUND((SUM(NVL(PAID_WT,0) + NVL(TBB_WT,0) + NVL(FOD_WT,0) + NVL(BOD_WT,0)) 
                                - SUM(NVL(LYA_PAID_WT,0) + NVL(LYA_TBB_WT,0) + NVL(LYA_FOD_WT,0) + NVL(LYA_BOD_WT,0)))/1000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year_1)s%(month_1)s','YYYYMM'))
                                                                                                                  AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'year_1':year_1, 'month_1':month_1, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYW']
                    y2 = df['CYW']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYW'],
                                    name = 'LYW',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYW'],
                                    name = 'CYW',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise Weight Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="Weight (in Tons)", showgrid = False)
                                            )

                    }

            elif checklist == 'CUM':
    
                    sql = '''
                            SELECT
                                 REGION_CODE REGION
                                ,ROUND(SUM(NVL(PAID_WT,0) + NVL(TBB_WT,0) + NVL(FOD_WT,0) + NVL(BOD_WT,0))/100000,2) CYW
                                ,ROUND(SUM(NVL(LYA_PAID_WT,0) + NVL(LYA_TBB_WT,0) + NVL(LYA_FOD_WT,0) + NVL(LYA_BOD_WT,0))/100000, 2) LYW
                                ,ROUND((SUM(NVL(PAID_WT,0) + NVL(TBB_WT,0) + NVL(FOD_WT,0) + NVL(BOD_WT,0)) 
                                - SUM(NVL(LYA_PAID_WT,0) + NVL(LYA_TBB_WT,0) + NVL(LYA_FOD_WT,0) + NVL(LYA_BOD_WT,0)))/100000,2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                        '''%{'year':year, 'month':month,'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYW']
                    y2 = df['CYW']
                    y3 = df['GP']
                    x1 = df['REGION']
            
                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                    
                    return {
                            'data': [
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['LYW'],
                                        name = 'LYW',
                                        marker_color='rgb(242, 109, 7)'),
                    
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['CYW'],
                                        name = 'CYW',
                                        marker_color='rgb(7, 128, 242)'),
                        
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['GP'],
                                        name = 'Growth',
                                        marker_color= df['color'])
                                   ],
                            'layout' : go.Layout(
                                                 title={
                                                        'text': "Region Wise Weight Comparison LY Vs CY",
                                                        'y':0.98,
                                                        'x':0.5,
                                                        'xanchor': 'center',
                                                        'yanchor': 'top'
                                                       },
                                                annotations = annotations,
                                                barmode = 'group',
                                                bargroupgap = 0.1,
                                                legend=dict(
                                                orientation="h",
                                                yanchor="bottom",
                                                y=1.02,
                                                xanchor="right",
                                                x=1
                                                ),
                                                showlegend = True,
                                                xaxis=dict(title="Region", showgrid = False),
                                                yaxis=dict(title="Weight (in Tons)", showgrid = False)
                                                )
                        
                        }
            else:
                return{}

    else:
        return {}

@app.callback(Output('Graph-3','figure'),[Input('submit_button','n_clicks')],
                                         [State('division-dropdown','value'),\
                                          State('basis-dropdown','value'),\
                                          State('checklist-dropdown','value'),\
                                          State('year-dropdown','value'),\
                                          State('month-dropdown','value'),\
                                          State('visible-year-dropdown', 'value'),\
                                          State('visible-month-dropdown','value')])

def update_graph_3(n_clicks, division, basis, checklist, year, month, year_1, month_1):

    if n_clicks is not None and n_clicks > 0:
    
        con = cx.connect(config.CONN_STR)
        
        if basis == 'PAID':

            if checklist == 'FTM':

                if year_1 == ' ' and month_1 == ' ':
            
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(PAID_DWB,0)),2) CYD
                                ,ROUND(SUM(NVL(LYA_PAID_DWB,0)),2) LYD
                                ,ROUND((SUM(NVL(PAID_DWB,0)) - SUM(NVL(LYA_PAID_DWB,0))),2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                                                                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYD']
                    y2 = df['CYD']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYD'],
                                    name = 'LYD',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYD'],
                                    name = 'CYD',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise DWB Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="DWB", showgrid = False)
                                            )

                    }

                elif year_1 != ' ' and month_1 != ' ':

                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(PAID_DWB,0)),2) CYD
                                ,ROUND(SUM(NVL(LYA_PAID_DWB,0)),2) LYD
                                ,ROUND((SUM(NVL(PAID_DWB,0)) - SUM(NVL(LYA_PAID_DWB,0))),2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year_1)s%(month_1)s','YYYYMM'))
                                                                                                                  AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'year_1':year_1, 'month_1':month_1, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYD']
                    y2 = df['CYD']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYD'],
                                    name = 'LYD',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYD'],
                                    name = 'CYD',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise DWB Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="DWB", showgrid = False)
                                            )

                    }

            elif checklist == 'CUM':
    
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(PAID_DWB,0)),2) CYD
                                ,ROUND(SUM(NVL(LYA_PAID_DWB,0)),2) LYD
                                ,ROUND((SUM(NVL(PAID_DWB,0)) - SUM(NVL(LYA_PAID_DWB,0))),2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                        '''%{'year':year, 'month':month,'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYD']
                    y2 = df['CYD']
                    y3 = df['GP']
                    x1 = df['REGION']
            
                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                    
                    return {
                            'data': [
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['LYD'],
                                        name = 'LYD',
                                        marker_color='rgb(242, 109, 7)'),
                    
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['CYD'],
                                        name = 'CYD',
                                        marker_color='rgb(7, 128, 242)'),
                        
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['GP'],
                                        name = 'Growth',
                                        marker_color= df['color'])
                                   ],
                            'layout' : go.Layout(
                                                 title={
                                                        'text': "Region Wise DWB Comparison LY Vs CY",
                                                        'y':0.98,
                                                        'x':0.5,
                                                        'xanchor': 'center',
                                                        'yanchor': 'top'
                                                       },
                                                annotations = annotations,
                                                barmode = 'group',
                                                bargroupgap = 0.1,
                                                legend=dict(
                                                orientation="h",
                                                yanchor="bottom",
                                                y=1.02,
                                                xanchor="right",
                                                x=1
                                                ),
                                                showlegend = True,
                                                xaxis=dict(title="Region", showgrid = False),
                                                yaxis=dict(title="DWB", showgrid = False)
                                                )
                        
                        }
            else:
                return{}
        
        elif basis == 'TBB':
    
            if checklist == 'FTM':

                if year_1 == ' ' and month_1 == ' ':
            
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(TBB_DWB,0)),2) CYD
                                ,ROUND(SUM(NVL(LYA_TBB_DWB,0)),2) LYD
                                ,ROUND((SUM(NVL(TBB_DWB,0)) - SUM(NVL(LYA_TBB_DWB,0))),2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                                                                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYD']
                    y2 = df['CYD']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYD'],
                                    name = 'LYD',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYD'],
                                    name = 'CYD',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise DWB Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="DWB", showgrid = False)
                                            )

                    }

                elif year_1 != ' ' and month_1 != ' ':

                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(TBB_DWB,0)),2) CYD
                                ,ROUND(SUM(NVL(LYA_TBB_DWB,0)),2) LYD
                                ,ROUND((SUM(NVL(TBB_DWB,0)) - SUM(NVL(LYA_TBB_DWB,0))),2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year_1)s%(month_1)s','YYYYMM'))
                                                                                                                  AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'year_1':year_1, 'month_1':month_1, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYD']
                    y2 = df['CYD']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYD'],
                                    name = 'LYD',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYD'],
                                    name = 'CYD',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise DWB Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="DWB", showgrid = False)
                                            )

                    }        
            
            elif checklist == 'CUM':
    
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(TBB_DWB,0)),2) CYD
                                ,ROUND(SUM(NVL(LYA_TBB_DWB,0)),2) LYD
                                ,ROUND((SUM(NVL(TBB_DWB,0)) - SUM(NVL(LYA_TBB_DWB,0))),2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                        '''%{'year':year, 'month':month,'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYD']
                    y2 = df['CYD']
                    y3 = df['GP']
                    x1 = df['REGION']
            
                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                    
                    return {
                            'data': [
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['LYD'],
                                        name = 'LYD',
                                        marker_color='rgb(242, 109, 7)'),
                    
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['CYD'],
                                        name = 'CYD',
                                        marker_color='rgb(7, 128, 242)'),
                        
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['GP'],
                                        name = 'Growth',
                                        marker_color= df['color'])
                                   ],
                            'layout' : go.Layout(
                                                 title={
                                                        'text': "Region Wise DWB Comparison LY Vs CY",
                                                        'y':0.98,
                                                        'x':0.5,
                                                        'xanchor': 'center',
                                                        'yanchor': 'top'
                                                       },
                                                annotations = annotations,
                                                barmode = 'group',
                                                bargroupgap = 0.1,
                                                legend=dict(
                                                orientation="h",
                                                yanchor="bottom",
                                                y=1.02,
                                                xanchor="right",
                                                x=1
                                                ),
                                                showlegend = True,
                                                xaxis=dict(title="Region", showgrid = False),
                                                yaxis=dict(title="DWB", showgrid = False)
                                                )
                        
                        }
            else:
                return{}

        elif basis == 'FOD':
    
            if checklist == 'FTM':

                if year_1 == ' ' and month_1 == ' ':
            
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(FOD_DWB,0)),2) CYD
                                ,ROUND(SUM(NVL(LYA_FOD_DWB,0)),2) LYD
                                ,ROUND((SUM(NVL(FOD_DWB,0)) - SUM(NVL(LYA_FOD_DWB,0))),2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                                                                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYD']
                    y2 = df['CYD']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYD'],
                                    name = 'LYD',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYD'],
                                    name = 'CYD',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise DWB Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="DWB", showgrid = False)
                                            )

                    }

                elif year_1 != ' ' and month_1 != ' ':

                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(FOD_DWB,0)),2) CYD
                                ,ROUND(SUM(NVL(LYA_FOD_DWB,0)),2) LYD
                                ,ROUND((SUM(NVL(FOD_DWB,0)) - SUM(NVL(LYA_FOD_DWB,0))),2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year_1)s%(month_1)s','YYYYMM'))
                                                                                                                  AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'year_1':year_1, 'month_1':month_1, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYD']
                    y2 = df['CYD']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYD'],
                                    name = 'LYD',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYD'],
                                    name = 'CYD',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise DWB Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="DWB", showgrid = False)
                                            )

                    }

            elif checklist == 'CUM':
    
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(FOD_DWB,0)),2) CYD
                                ,ROUND(SUM(NVL(LYA_FOD_DWB,0)),2) LYD
                                ,ROUND((SUM(NVL(FOD_DWB,0)) - SUM(NVL(LYA_FOD_DWB,0))),2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                        '''%{'year':year, 'month':month,'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYD']
                    y2 = df['CYD']
                    y3 = df['GP']
                    x1 = df['REGION']
            
                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                    
                    return {
                            'data': [
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['LYF'],
                                        name = 'LYF',
                                        marker_color='rgb(242, 109, 7)'),
                    
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['CYF'],
                                        name = 'CYF',
                                        marker_color='rgb(7, 128, 242)'),
                        
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['GP'],
                                        name = 'Growth',
                                        marker_color= df['color'])
                                   ],
                            'layout' : go.Layout(
                                                 title={
                                                        'text': "Region Wise DWB Comparison LY Vs CY",
                                                        'y':0.98,
                                                        'x':0.5,
                                                        'xanchor': 'center',
                                                        'yanchor': 'top'
                                                       },
                                                annotations = annotations,
                                                barmode = 'group',
                                                bargroupgap = 0.1,
                                                legend=dict(
                                                orientation="h",
                                                yanchor="bottom",
                                                y=1.02,
                                                xanchor="right",
                                                x=1
                                                ),
                                                showlegend = True,
                                                xaxis=dict(title="Region", showgrid = False),
                                                yaxis=dict(title="DWB", showgrid = False)
                                                )
                        
                        }
            else:
                return{}

        elif basis == 'BOD':
    
            if checklist == 'FTM':

                if year_1 == ' ' and month_1 == ' ':
            
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(BOD_DWB,0)),2) CYD
                                ,ROUND(SUM(NVL(LYA_BOD_DWB,0)),2) LYD
                                ,ROUND((SUM(NVL(BOD_DWB,0)) - SUM(NVL(LYA_BOD_DWB,0))),2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                                                                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYD']
                    y2 = df['CYD']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYD'],
                                    name = 'LYD',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYD'],
                                    name = 'CYD',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise DWB Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="DWB", showgrid = False)
                                            )

                    }

                elif year_1 != ' ' and month_1 != ' ':

                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(BOD_DWB,0)),2) CYD
                                ,ROUND(SUM(NVL(LYA_BOD_DWB,0)),2) LYD
                                ,ROUND((SUM(NVL(BOD_DWB,0)) - SUM(NVL(LYA_BOD_DWB,0))),2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year_1)s%(month_1)s','YYYYMM'))
                                                                                                                  AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'year_1':year_1, 'month_1':month_1, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYD']
                    y2 = df['CYD']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYD'],
                                    name = 'LYD',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYD'],
                                    name = 'CYD',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise DWB Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="DWB", showgrid = False)
                                            )

                    }
   
            elif checklist == 'CUM':
    
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(BOD_DWB,0)),2) CYD
                                ,ROUND(SUM(NVL(LYA_BOD_DWB,0)),2) LYD
                                ,ROUND((SUM(NVL(BOD_DWB,0)) - SUM(NVL(LYA_BOD_DWB,0))),2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                        '''%{'year':year, 'month':month,'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYD']
                    y2 = df['CYD']
                    y3 = df['GP']
                    x1 = df['REGION']
            
                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                    
                    return {
                            'data': [
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['LYD'],
                                        name = 'LYD',
                                        marker_color='rgb(242, 109, 7)'),
                    
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['CYD'],
                                        name = 'CYD',
                                        marker_color='rgb(7, 128, 242)'),
                        
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['GP'],
                                        name = 'Growth',
                                        marker_color= df['color'])
                                   ],
                            'layout' : go.Layout(
                                                 title={
                                                        'text': "Region Wise DWB Comparison LY Vs CY",
                                                        'y':0.98,
                                                        'x':0.5,
                                                        'xanchor': 'center',
                                                        'yanchor': 'top'
                                                       },
                                                annotations = annotations,
                                                barmode = 'group',
                                                bargroupgap = 0.1,
                                                legend=dict(
                                                orientation="h",
                                                yanchor="bottom",
                                                y=1.02,
                                                xanchor="right",
                                                x=1
                                                ),
                                                showlegend = True,
                                                xaxis=dict(title="Region", showgrid = False),
                                                yaxis=dict(title="DWB", showgrid = False)
                                                )
                        
                        }
            else:
                return{}

        elif basis == 'ALL':
    
            if checklist == 'FTM':

                if year_1 == ' ' and month_1 == ' ':
            
                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(PAID_DWB,0) + NVL(TBB_DWB,0) + NVL(FOD_DWB,0) + NVL(BOD_DWB,0)),2) CYD
                                ,ROUND(SUM(NVL(LYA_PAID_DWB,0) + NVL(LYA_TBB_DWB,0) + NVL(LYA_FOD_DWB,0) + NVL(LYA_BOD_DWB,0)), 2) LYD
                                ,ROUND((SUM(NVL(PAID_DWB,0) + NVL(TBB_DWB,0) + NVL(FOD_DWB,0) + NVL(BOD_DWB,0)) 
                                - SUM(NVL(LYA_PAID_DWB,0) + NVL(LYA_TBB_DWB,0) + NVL(LYA_FOD_DWB,0) + NVL(LYA_BOD_DWB,0))),2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                                                                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYD']
                    y2 = df['CYD']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYD'],
                                    name = 'LYD',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYD'],
                                    name = 'CYD',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise DWB Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="DWB", showgrid = False)
                                            )

                    }

                elif year_1 != ' ' and month_1 != ' ':

                    sql = '''
                            SELECT
                                REGION_CODE REGION
                                ,ROUND(SUM(NVL(PAID_DWB,0) + NVL(TBB_DWB,0) + NVL(FOD_DWB,0) + NVL(BOD_DWB,0)),2) CYD
                                ,ROUND(SUM(NVL(LYA_PAID_DWB,0) + NVL(LYA_TBB_DWB,0) + NVL(LYA_FOD_DWB,0) + NVL(LYA_BOD_DWB,0)), 2) LYD
                                ,ROUND((SUM(NVL(PAID_DWB,0) + NVL(TBB_DWB,0) + NVL(FOD_DWB,0) + NVL(BOD_DWB,0)) 
                                - SUM(NVL(LYA_PAID_DWB,0) + NVL(LYA_TBB_DWB,0) + NVL(LYA_FOD_DWB,0) + NVL(LYA_BOD_DWB,0))),2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) BETWEEN last_day(TO_DATE('%(year_1)s%(month_1)s','YYYYMM'))
                                                                                                                  AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                    '''%{'year':year, 'month':month, 'year_1':year_1, 'month_1':month_1, 'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYD']
                    y2 = df['CYD']
                    y3 = df['GP']
                    x1 = df['REGION']

                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                            
                    return {
                        'data': [
                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['LYD'],
                                    name = 'LYD',
                                    marker_color='rgb(242, 109, 7)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['CYD'],
                                    name = 'CYD',
                                    marker_color='rgb(7, 128, 242)'),

                                    go.Bar(
                                    x=df['REGION'],
                                    y=df['GP'],
                                    name = 'Growth',
                                    marker_color= df['color'])
                                ],
                        'layout' : go.Layout(
                                                title={
                                                    'text': "Region Wise DWB Comparison LY Vs CY",
                                                    'y':0.98,
                                                    'x':0.5,
                                                    'xanchor': 'center',
                                                    'yanchor': 'top'
                                                    },
                                            annotations = annotations,
                                            barmode = 'group',
                                            bargroupgap = 0.1,
                                            legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1
                                            ),
                                            showlegend = True,
                                            xaxis=dict(title="Region", showgrid = False),
                                            yaxis=dict(title="DWB", showgrid = False)
                                            )

                    }

            elif checklist == 'CUM':
    
                    sql = '''
                            SELECT
                                 REGION_CODE REGION
                                ,ROUND(SUM(NVL(PAID_DWB,0) + NVL(TBB_DWB,0) + NVL(FOD_DWB,0) + NVL(BOD_DWB,0)),2) CYD
                                ,ROUND(SUM(NVL(LYA_PAID_DWB,0) + NVL(LYA_TBB_DWB,0) + NVL(LYA_FOD_DWB,0) + NVL(LYA_BOD_DWB,0)), 2) LYD
                                ,ROUND((SUM(NVL(PAID_DWB,0) + NVL(TBB_DWB,0) + NVL(FOD_DWB,0) + NVL(BOD_DWB,0)) 
                                - SUM(NVL(LYA_PAID_DWB,0) + NVL(LYA_TBB_DWB,0) + NVL(LYA_FOD_DWB,0) + NVL(LYA_BOD_DWB,0))),2) GP
                            FROM
                                CT_BUSINESS_GROWTH_NEW_IMPL
                            WHERE
                                LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                AND DIVISION_CODE = NVL('%(division)s',DIVISION_CODE)
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                            ORDER BY
                                REGION_CODE
                        '''%{'year':year, 'month':month,'division':division}

                    df = pd.read_sql_query(sql, con)
                        
                    df['color'] = np.where(df['GP'] < 0, 'red', 'green')

                    y1 = df['LYD']
                    y2 = df['CYD']
                    y3 = df['GP']
                    x1 = df['REGION']
            
                    annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='left',xshift = -28, yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y1)]
                    annot_2 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y2)]
                    annot_3 = [dict(x=xi,y=yi,text= str(yi),xanchor='left', xshift = 34, yanchor='bottom', showarrow=False,\
                    font=dict(size = 9.5), textangle = -90) for xi, yi in zip(x1, y3)]

                    annotations = annot_1 + annot_2 + annot_3
                    
                    return {
                            'data': [
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['LYD'],
                                        name = 'LYD',
                                        marker_color='rgb(242, 109, 7)'),
                    
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['CYD'],
                                        name = 'CYD',
                                        marker_color='rgb(7, 128, 242)'),
                        
                                      go.Bar(
                                        x=df['REGION'],
                                        y=df['GP'],
                                        name = 'Growth',
                                        marker_color= df['color'])
                                   ],
                            'layout' : go.Layout(
                                                 title={
                                                        'text': "Region Wise DWB Comparison LY Vs CY",
                                                        'y':0.98,
                                                        'x':0.5,
                                                        'xanchor': 'center',
                                                        'yanchor': 'top'
                                                       },
                                                annotations = annotations,
                                                barmode = 'group',
                                                bargroupgap = 0.1,
                                                legend=dict(
                                                orientation="h",
                                                yanchor="bottom",
                                                y=1.02,
                                                xanchor="right",
                                                x=1
                                                ),
                                                showlegend = True,
                                                xaxis=dict(title="Region", showgrid = False),
                                                yaxis=dict(title="DWB", showgrid = False)
                                                )
                        
                        }
            else:
                return{}
    else:
        return {}
    
