#!/usr/bin/env python
#coding: utf-8

"""
==============================================================================================================================================================
                                                          
                                                    Python Script for Branch/Controlling/Region Ranking APP 10

==============================================================================================================================================================

"""


from dash_extensions.snippets import send_bytes
from dash_extensions import Download
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash

import cx_Oracle as cx
import pandas as pd
import numpy as np
import xlsxwriter


import base64
import flask
import io

import config
import config_1

'''
Creating app

'''

app = dash.Dash(__name__, requests_pathname_prefix = '/app10/', external_stylesheets = [dbc.themes.BOOTSTRAP])


red_button_style = {'background-color': 'red',
                    'color': 'white',
                   }

green_button_style = {'background-color': 'green',
                      'color': 'white',
                     }

row = html.Div([
                   dbc.Row([
                             dbc.Col([
                                       dcc.Dropdown(
                                                    id = 'year',
                                                    options = [{'label': y, 'value': y} for y in ['2018','2019',\
                                                                                                  '2020','2021']],
                                                    style = {'width':'50%','margin-left':'50%'} 
                                                    )
                                    ]),
                             dbc.Col([
                                       dcc.Dropdown(
                                                    id = 'month',
                                                    options = [{'label' : x, 'value' : x} for x in ['01','02','03',\
                                                                                                    '04','05','06',\
                                                                                                    '07','08','09',\
                                                                                                    '10','11','12']],
                                                    style = {'width':'50%'}
                                                   )
                                      ])
                          
                             
                          ]),
                  html.Br(),
                  dbc.Row([  
                             dbc.Col([
                                      html.Button("Download BRANCH", id = 'btn1', n_clicks = 0, style = red_button_style),
                                      Download(id="download1")
                                     ],style = {'margin-left':'25%','display': 'inline-block','border-radius': '12px'}),
                             dbc.Col([
                                      html.Button("Download CONTROLLING", id = 'btn2', n_clicks = 0, style = red_button_style), 
                                      Download(id="download2"),
                                     ], style = {'margin-left':'-30%','display': 'inline-block','border-radius': '12px'}),
                             dbc.Col([
                                      html.Button("Download REGION", id = 'btn3', n_clicks = 0, style = red_button_style), 
                                      Download(id="download3"),
                                     ],style = {'margin-left':'-26.3%','display': 'inline-block','border-radius': '12px'}),
                             
                          ]),
                   html.Br(),
                   dbc.Row([
                            dbc.Col([
                                     html.A(html.Button("Refresh"),href = '/app10/')
                                    ])
                          ],style = {'margin-left':'44%','display': 'inline-block','border-radius': '12px'})      
            ])

'''
Creating app layout

'''
                   
app.layout = html.Div([
                       html.Div(
                                [
                                 dbc.Container(children=[row])
                                ],style = {'margin-top':'225px'}
                               )
                     ])


@app.callback(Output('btn1', 'style'), [Input('btn1', 'n_clicks')])

def change_button_style(n_clicks):

    if n_clicks > 0:

        return green_button_style

    else:

        return red_button_style

@app.callback(Output('btn2', 'style'), [Input('btn2', 'n_clicks')])

def change_button_style(n_clicks):

    if n_clicks > 0:

        return green_button_style

    else:

        return red_button_style

@app.callback(Output('btn3', 'style'), [Input('btn3', 'n_clicks')])

def change_button_style(n_clicks):

    if n_clicks > 0:

        return green_button_style

    else:

        return red_button_style

@app.callback(Output('download1','data'),[Input('btn1','n_clicks'),
                                           Input('year','value'), 
                                           Input('month','value')], 
                                           prevent_initial_call = True)

def func_branch_ranking(n_clicks, year, month):

    if n_clicks is not None and n_clicks > 0:

         con = cx.connect(config.CONN_STR)

         con_1 = cx.connect(config_1.CONN_STR)

         sql = '''SELECT
                         xm.REGION_CODE
                        ,xm.CONTROLLING_CODE
                        ,xm.BRANCH_CODE
                        ,xm.BRANCH_NAME
                        ,xm.SATTLITEBRANCH
                        ,xm.STATUS
                        ,SUM(NVL(ct.TOT_FRT,0)) SURFACE_FRT
                        ,SUM(NVL(ct.LYA_TOT_FRT,0)) LY_SURFACE_FRT
                        ,ROUND(((SUM(NVL(ct.TOT_FRT,0)) - SUM(NVL(ct.LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(ct.LYA_TOT_FRT,0)),0)) * 100,0) SURFACE_FRT_GWT
                        ,SUM(NVL(ct.TOT_WT,0)) SURFACE_BKG_WT
                        ,SUM(NVL(ct.LYA_TOT_WT,0)) LY_SURFACE_BKG_WT
                        ,SUM(NVL(ct.DLY_WT,0)) SURFACE_DLY_WT
                        ,SUM(NVL(ct.LYA_DLY_WT,0)) LY_SURFACE_DLY_WT
                        ,ROUND(((SUM(NVL(ct.DLY_WT,0)) - SUM(NVL(ct.LYA_DLY_WT,0)))/NULLIF(SUM(NVL(ct.LYA_DLY_WT,0)),0)) * 100,0) SURFACE_WT_GWT
                FROM
                         CT_BUSINESS_GROWTH_NEW_IMPL ct
                LEFT JOIN
                    XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE                     
                WHERE
                    LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(ct.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                            BETWEEN '01-APR-'||CASE WHEN TO_CHAR(LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                    THEN TO_CHAR(TO_NUMBER(TO_CHAR(LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                        ELSE TO_CHAR(LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                            AND LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                    AND ct.DIVISION_CODE = '21'
                    AND ct.REGION_CODE <> 'XCRP'
                    AND xm.SATTLITEBRANCH NOT IN ('C','H','R')
                GROUP BY
                   xm.REGION_CODE
                  ,xm.CONTROLLING_CODE
                  ,xm.BRANCH_CODE
                  ,xm.BRANCH_NAME
                  ,xm.SATTLITEBRANCH
                  ,xm.STATUS
                ORDER BY
                  xm.REGION_CODE ASC

          '''%{'year':year,'month':month}

         df_0 = pd.read_sql_query(sql, con).replace(np.nan,0)

         df_0['MARK 1'] = df_0['SURFACE_FRT'].floordiv(600000).mul(1.052).round(0)
            
         df_0['MARK 5'] =  df_0['SURFACE_DLY_WT'].floordiv(200000).mul(1.651).round(0)
            
         df_0['MARK 3'] = [x if x <= 50 else 50 for x in df_0['SURFACE_FRT_GWT']]
        
         df_0['MARK 7'] = [x if x <= 50 else 50 for x in df_0['SURFACE_WT_GWT']]

         sql_1 = '''SELECT
                         xm.REGION_CODE
                        ,xm.CONTROLLING_CODE
                        ,xm.BRANCH_CODE
                        ,SUM(NVL(ct.TOT_FRT,0)) AIR_FRT
                        ,SUM(NVL(ct.LYA_TOT_FRT,0)) LY_AIR_FRT
                        ,ROUND(((SUM(NVL(ct.TOT_FRT,0)) - SUM(NVL(ct.LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(ct.LYA_TOT_FRT,0)),0)) * 100,0) AIR_FRT_GWT
                        ,SUM(NVL(ct.DLY_WT,0)) AIR_DLY_WT
                        ,SUM(NVL(ct.LYA_DLY_WT,0)) LY_AIR_DLY_WT
                        ,ROUND(((SUM(NVL(ct.DLY_WT,0)) - SUM(NVL(ct.LYA_DLY_WT,0)))/NULLIF(SUM(NVL(ct.LYA_DLY_WT,0)),0)) * 100,0) AIR_WT_GWT
                    FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL ct
                    LEFT JOIN
                        XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE
                    WHERE
                        LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(ct.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                        AND ct.DIVISION_CODE = '22'
                        AND ct.REGION_CODE <> 'XCRP'
                        AND xm.SATTLITEBRANCH NOT IN ('C','H','R')
                    GROUP BY
                         xm.REGION_CODE
                        ,xm.CONTROLLING_CODE
                        ,xm.BRANCH_CODE
                    ORDER BY
                         xm.REGION_CODE ASC
                '''%{'year':year,
                     'month':month
                    }


         df_1 = pd.read_sql_query(sql_1, con).replace(np.nan, 0)

         df_1['MARK 2'] = df_1['AIR_FRT'].floordiv(200000).mul(1.052).round(0)
            
         df_1['MARK 6'] =  df_1['AIR_DLY_WT'].floordiv(10000).mul(2.489).round(0)
            
         df_1['MARK 4'] = [x if x <= 50 else 50 for x in df_1['AIR_FRT_GWT']]
        
         df_1['MARK 8'] = [x if x <= 50 else 50 for x in df_1['AIR_WT_GWT']]
            
         df_2 = df_0.merge(df_1, on = ['REGION_CODE','CONTROLLING_CODE','BRANCH_CODE'], how = 'left')
            
         sql_3 = '''SELECT 
                         a.REGION_CODE 
                        ,a.CONTROLLING_CODE
                        ,a.BRANCH_CODE 
                        ,ROUND(SUM(NVL(b.OS_GT_90,0)),0) OS_ABOVE_90
                        ,ROUND(SUM(NVL(a.TBB_FREIGHT,0)),0) BUSINESS_AMT_TBB
                        ,ROUND(SUM(NVL(a.TBB_FREIGHT,0))/365,0) BUSINESS_PD
                        ,ROUND(NVL(SUM(NVL(b.OS_GT_90,0))/NULLIF((SUM(NVL(a.TBB_FREIGHT,0))/365),0),0),0) OS_TBB_PD
                    FROM 
                        (
                        SELECT 
                             xm.REGION_CODE 
                            ,xm.CONTROLLING_CODE 
                            ,xm.BRANCH_CODE
                            ,SUM(NVL(ct.TBB_FRT,0)) TBB_FREIGHT
                        FROM 
                                CT_BUSINESS_GROWTH_NEW_IMPL ct
                        LEFT JOIN
                               XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE
                        WHERE 
                             LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(ct.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                            
                            AND ct.DIVISION_CODE IN ('21','22')
                            AND ct.REGION_CODE <> 'XCRP'
                            AND xm.SATTLITEBRANCH NOT IN ('C','H','R')
                        GROUP BY 
                             xm.REGION_CODE 
                            ,xm.CONTROLLING_CODE 
                            ,xm.BRANCH_CODE
                        ) a
                        LEFT JOIN
                        (
                        SELECT 
                             xm.REGION_CODE 
                            ,xm.CONTROLLING_CODE 
                            ,xm.BRANCH_CODE
                            ,SUM(NVL(ct.OS_91TO120_DAYS,0)) + SUM(NVL(ct.OS_121TO180_DAYS,0)) + SUM(NVL(ct.OS_181TO365_DAYS,0)) + SUM(NVL(ct.OS_ABOVE_365_DAYS,0)) OS_GT_90
                        FROM 
                            CT_AGEWISE_BILLED_OS ct
                        LEFT JOIN
                            XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE
                        WHERE 
                             ct.REPORT_TYPE = 'BILLWISE'
                             AND ct.DIVISION_CODE IN ('21','22')
                             AND TRUNC(BILL_DATE) <= TRUNC(SYSDATE)
                             AND TRUNC(AUD_DATE) = TRUNC(SYSDATE)
                             AND NOT EXISTS(
                                            SELECT 
                                                  'X'
                                            FROM 
                                                CT_AGEWISE_BILLED_OS ca
                                            WHERE
                                                ct.BRANCH_CODE = ca.BRANCH_CODE 
                                                AND ct.BILL_NO = ca.BILL_NO 
                                                AND ct.BILL_DATE = ca.BILL_DATE 
                                                AND ca.REALISE_FLAG = 'R'
                                                AND ca.UPTO_BCS_DATE <= TRUNC(SYSDATE)
                                           )
                        GROUP BY 
                             xm.REGION_CODE 
                            ,xm.CONTROLLING_CODE 
                            ,xm.BRANCH_CODE
                        ) b
                    ON
                        a.BRANCH_CODE = b.BRANCH_CODE
                    GROUP BY 
                         a.REGION_CODE 
                        ,a.CONTROLLING_CODE
                        ,a.BRANCH_CODE 
                    ORDER BY 
                        a.REGION_CODE ASC
                '''%{'year' : year, 'month' : month}
                    
         df_3 = pd.read_sql_query(sql_3, con)

         df_4 = df_2.merge(df_3, on = ['REGION_CODE','CONTROLLING_CODE','BRANCH_CODE'], how = 'left')

         def os_tbb_rank(row):

             if row == 0:
                return 50
             elif row >= 1 and row <= 10:
                return 40
             elif row >= 11 and row <= 20:
                 return 30
             elif row > 20 and row <= 30:
                 return 20
             elif row > 30 and row <= 40:
                 return 10
             else:
                 return 0

         df_4['MARK 9'] = df_4['OS_TBB_PD'].apply(os_tbb_rank)

         sql_5 = '''    SELECT
                            Q2.TCS_REGION REGION_CODE,
                            Q2.TCS_CONTROLLING CONTROLLING_CODE,
                            Q2.TCS_BRANCH BRANCH_CODE,
                            NVL(Q1.LY_COST,0) LY_PC_COST,
                            NVL(Q2.CY_COST,0) CY_PC_COST
                        FROM
                        (
                        SELECT 
                            X.REGION_CODE TCS_REGION,
                            X.CONTROLLING_CODE TCS_CONTROLLING,
                            X.BRANCH_CODE TCS_BRANCH,
                            ROUND(SUM(NVL(C.TOTALCOST,0))/NULLIF(SUM(NVL(C.ACTUAL_WT,0)),0),2) LY_COST
                        FROM 
                            CT_PICKDLY_COST C,
                            XM_BRANCHS X 
                        WHERE 
                            C.TCSBRANCH=X.BRANCH_CODE 
                            AND C.REGION = X.REGION_CODE 
                            AND C.CONTROLLING = X.CONTROLLING_CODE
                            AND TO_DATE(TO_CHAR(TO_DATE(C.MONTH_YEAR,'MMYYYY'),'YYYYMM'),'YYYYMM')
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'MM') IN ('01','02','03')
                                      THEN TO_CHAR(TO_NUMBER(TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'YYYY'))-1)
                                         ELSE TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'YYYY') END
                                           AND ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12)
                            AND C.TCSTYPE NOT IN ('OD','DC')   
                            AND VEHTYPE!='TOT' 
                        GROUP BY
                            X.REGION_CODE,
                            X.CONTROLLING_CODE,
                            X.BRANCH_CODE
                        ) Q1
                        RIGHT JOIN
                        (
                        SELECT 
                            X.REGION_CODE TCS_REGION,
                            X.CONTROLLING_CODE TCS_CONTROLLING,
                            X.BRANCH_CODE TCS_BRANCH,
                            ROUND(SUM(NVL(C.TOTALCOST,0))/NULLIF(SUM(NVL(C.ACTUAL_WT,0)),0),2) CY_COST
                            
                        FROM 
                            CT_PICKDLY_COST C,
                            XM_BRANCHS X 
                        WHERE 
                            C.TCSBRANCH=X.BRANCH_CODE 
                            AND C.REGION = X.REGION_CODE 
                            AND C.CONTROLLING = X.CONTROLLING_CODE
                            AND TO_DATE(TO_CHAR(TO_DATE(C.MONTH_YEAR,'MMYYYY'),'YYYYMM'),'YYYYMM')
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                      THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                         ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                           AND TO_DATE('%(year)s%(month)s','YYYYMM')
                            AND C.TCSTYPE NOT IN ('OD','DC')   
                            AND VEHTYPE!='TOT' 
                        GROUP BY
                            X.REGION_CODE,
                            X.CONTROLLING_CODE,
                            X.BRANCH_CODE
                        ) Q2
                        ON
                        Q1.TCS_BRANCH = Q2.TCS_BRANCH
                        ORDER BY
                        Q2.TCS_BRANCH

                    '''%{'year':year,'month':month}
        
         df_5 = pd.read_sql_query(sql_5, con)

         df_6 = df_4.merge(df_5, on = ['REGION_CODE','CONTROLLING_CODE','BRANCH_CODE'], how = 'left')

         df_6['AMT_SAVING_PC'] = df_6['LY_PC_COST'].sub(df_6['CY_PC_COST']).mul(df_0['SURFACE_BKG_WT'])

         def pickup_amt_saving(row):

             if row > 50:
                 return 50
             else:
                 return row

         df_6['MARK 10'] = df_6['AMT_SAVING_PC'].floordiv(10000).apply(pickup_amt_saving)

         sql_7 = ''' SELECT
                            Q2.TCS_REGION REGION_CODE,
                            Q2.TCS_CONTROLLING CONTROLLING_CODE,
                            Q2.TCS_BRANCH BRANCH_CODE,
                            NVL(Q1.LY_COST, 0) LY_DY_COST,
                            NVL(Q2.CY_COST, 0) CY_DY_COST
                        FROM
                        (
                        SELECT 
                            X.REGION_CODE TCS_REGION,
                            X.CONTROLLING_CODE TCS_CONTROLLING,
                            X.BRANCH_CODE TCS_BRANCH,
                            ROUND(SUM(NVL(C.TOTALCOST,0))/NULLIF(SUM(NVL(C.ACTUAL_WT,0)),0),2) LY_COST
                        FROM 
                            CT_PICKDLY_COST C,
                            XM_BRANCHS X 
                        WHERE 
                            C.TCSBRANCH=X.BRANCH_CODE 
                            AND C.REGION = X.REGION_CODE 
                            AND C.CONTROLLING = X.CONTROLLING_CODE
                            AND TO_DATE(TO_CHAR(TO_DATE(C.MONTH_YEAR,'MMYYYY'),'YYYYMM'),'YYYYMM')
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'MM') IN ('01','02','03')
                                      THEN TO_CHAR(TO_NUMBER(TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'YYYY'))-1)
                                         ELSE TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'YYYY') END
                                           AND ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12)
                            AND C.TCSTYPE IN ('OD','DC')   
                            AND VEHTYPE!='TOT' 
                        GROUP BY
                            X.REGION_CODE,
                            X.CONTROLLING_CODE,
                            X.BRANCH_CODE
                        ) Q1
                        RIGHT JOIN
                        (
                        SELECT 
                            X.REGION_CODE TCS_REGION,
                            X.CONTROLLING_CODE TCS_CONTROLLING,
                            X.BRANCH_CODE TCS_BRANCH,
                            ROUND(SUM(NVL(C.TOTALCOST,0))/NULLIF(SUM(NVL(C.ACTUAL_WT,0)),0),2) CY_COST
                        FROM 
                            CT_PICKDLY_COST C,
                            XM_BRANCHS X 
                        WHERE 
                            C.TCSBRANCH=X.BRANCH_CODE 
                            AND C.REGION = X.REGION_CODE 
                            AND C.CONTROLLING = X.CONTROLLING_CODE
                            AND TO_DATE(TO_CHAR(TO_DATE(C.MONTH_YEAR,'MMYYYY'),'YYYYMM'),'YYYYMM')
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                      THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                         ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                           AND TO_DATE('%(year)s%(month)s','YYYYMM')
                            AND C.TCSTYPE IN ('OD','DC')   
                            AND VEHTYPE!='TOT' 
                        GROUP BY
                            X.REGION_CODE,
                            X.CONTROLLING_CODE,
                            X.BRANCH_CODE
                        ) Q2
                        ON
                        Q1.TCS_BRANCH = Q2.TCS_BRANCH
                        ORDER BY
                        Q2.TCS_BRANCH

                    '''%{'year':year,'month':month}
         
         df_7 = pd.read_sql_query(sql_7, con)

         df_8 = df_6.merge(df_7, on = ['REGION_CODE','CONTROLLING_CODE','BRANCH_CODE'], how = 'left')

         df_8['AMT_SAVING_DC'] = df_8['LY_DY_COST'].sub(df_8['CY_DY_COST']).mul(df_0['SURFACE_DLY_WT'])

         def delivery_cost_amt_saving(row):

             if row > 50:
                 return 50
             else:
                 return row

         df_8['MARK 11'] = df_8['AMT_SAVING_DC'].floordiv(10000).apply(delivery_cost_amt_saving)

         sql_9 = '''SELECT
                         xm.REGION_CODE
                        ,xm.CONTROLLING_CODE
                        ,xm.BRANCH_CODE
                        ,SUM(NVL(ct.TOT_FRT,0)) INTL_AIR_FRT
                        ,SUM(NVL(ct.LYA_TOT_FRT,0)) LY_INTL_AIR_FRT
                    FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL ct
                    LEFT JOIN
                        XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE 
                    WHERE
                        LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(ct.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                
                        AND ct.DIVISION_CODE = '26'
                        AND ct.REGION_CODE <> 'XCRP'
                        AND xm.SATTLITEBRANCH NOT IN ('C','H','R')
                    GROUP BY
                        xm.REGION_CODE
                        ,xm.CONTROLLING_CODE
                        ,xm.BRANCH_CODE
                    ORDER BY
                         xm.REGION_CODE ASC

          '''%{'year':year,'month':month}

         df_9 = pd.read_sql_query(sql_9, con)

         df_9['MARK 12'] = df_9['INTL_AIR_FRT'].floordiv(50000).mul(1.078).round(0)

         df_10 = df_8.merge(df_9, on = ['REGION_CODE','CONTROLLING_CODE','BRANCH_CODE'], how = 'left')

         sql_11 = '''SELECT
                             xm.REGION_CODE
                            ,xm.CONTROLLING_CODE
                            ,xm.BRANCH_CODE
                            ,SUM(NVL(ct.DLY_DWB,0)) DLYDWB        
                    FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL ct
                    LEFT JOIN
                        XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE 
                    WHERE
                        LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(ct.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                        AND ct.REGION_CODE <> 'XCRP'
                        AND xm.SATTLITEBRANCH NOT IN ('C','H','R')
                    GROUP BY
                         xm.REGION_CODE
                        ,xm.CONTROLLING_CODE
                        ,xm.BRANCH_CODE
                    ORDER BY
                        xm.REGION_CODE ASC

                '''%{'year':year, 'month':month}

         df_11 = pd.read_sql_query(sql_11, con)

         df_11['MARK 13'] = df_11['DLYDWB'].floordiv(603).round(0)

         df_12 = df_10.merge(df_11, on = ['REGION_CODE','CONTROLLING_CODE','BRANCH_CODE'], how = 'left')

         sql_13 = '''SELECT 
                            xm.REGION_CODE REGION_CODE,
                            xm.CONTROLLING_CODE CONTROLLING_CODE,
                            cp.DLY_BRANCH BRANCH_CODE, 
                            SUM(NVL(cp.DWB_ARRIVED,0)) TOTAL_DLY, 
                            SUM(NVL(cp.DWB_DLVRD_SAME_DAY,0)) SAME_DAY_DLY, 
                            SUM(NVL(cp.DLVRD_NEXT_DAY,0)) NEXT_DAY_DLY
                     FROM 
                         CT_BA_DBA_DLY_PERFORMANCE cp
                     LEFT JOIN
                        XM_BRANCHS xm ON cp.DLY_BRANCH = xm.BRANCH_CODE
                     WHERE 
                        TO_DATE(TO_CHAR(TO_DATE(cp.MONTH_YEAR,'MMYYYY'),'YYYYMM'),'YYYYMM')
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                                            THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                                                ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                                                AND TO_DATE('%(year)s%(month)s','YYYYMM')
                     GROUP BY
                        xm.REGION_CODE,
                        xm.CONTROLLING_CODE,
                        cp.DLY_BRANCH
                '''%{'year':year,'month':month}
         
         df_13 = pd.read_sql_query(sql_13, con)

         df_13['MARK 14'] = (((df_13['SAME_DAY_DLY'].add(df_13['NEXT_DAY_DLY'])).div(df_13['TOTAL_DLY'])).mul(100)).round(0)

         df_14 = df_12.merge(df_13, on = ['REGION_CODE','CONTROLLING_CODE','BRANCH_CODE'], how = 'left')

         sql_15 = '''SELECT 
                            xm.REGION_CODE REGION_CODE,
                            xm.CONTROLLING_CODE CONTROLLING_CODE,
                            ct.BRANCH_CODE BRANCH_CODE, 
                            SUM(ct.CREDIT_NOTE_AMOUNT) CR_NOTE_AMT
                        FROM 
                            CT_CREDIT_NOTE ct
                        LEFT JOIN
                            XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE
                        WHERE 
                            TO_DATE(TO_CHAR(ct.CREDIT_NOTE_DATE,'YYYYMM'),'YYYYMM') BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                                                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                                                                            ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                                                                                AND TO_DATE('%(year)s%(month)s','YYYYMM')
                        AND APPROVAL_FLAG = 'Y'
                        GROUP BY 
                            xm.REGION_CODE,
                            xm.CONTROLLING_CODE,
                            ct.BRANCH_CODE
                 '''%{'year' : year, 'month' : month}

         df_15 = pd.read_sql_query(sql_15, con)

         def cr_note_amt_rank(row):

             if row < -100:
                 return -100
             else:
                 return row

         df_15['MARK 15'] = df_15['CR_NOTE_AMT'].floordiv(-10000).apply(cr_note_amt_rank)

         df_15['MARK 15'] = df_15['MARK 15'].round(0)

         df_16 = df_14.merge(df_15, on = ['REGION_CODE','CONTROLLING_CODE','BRANCH_CODE'], how = 'left')

         sql_17 = ''' SELECT  xm.REGION_CODE BKG_REGION_CODE
                             ,xm.CONTROLLING_CODE BKG_CONTROLLING_CODE
                             ,A.UNLOADING_CNS_BRANCH_BRANCH_CO BKG_BRANCH_CODE
                             ,A.UNLOADING_CNS_CNS_NO DWB_NO
                             ,xm1.REGION_CODE DLY_REGION_CODE
                             ,xm1.CONTROLLING_CODE DLY_CONTROLLING_CODE
                             ,A.UNLOADING_BRANCH_BRANCH_CODE DLY_BRANCH_CODE
                             ,A.CLAIM_AMOUNT COFAMT 
                      FROM 
                             CT_COF A
                            ,CT_COF_CHK B
                            ,CT_DWB C
                            ,CM_GOODS_DETAIL D
                            ,xm_branchs xm
                            ,xm_branchs xm1 
                      WHERE 
                            A.UNLOADING_CNS_CNS_NO=B.CNS_NO 
                            AND A.UNLOADING_CNS_CNS_DATE=B.CNS_DATE 
                            AND UNLOADING_CNS_BRANCH_BRANCH_CO=B.CNS_BRANCH_CODE 
                            AND B.CNS_NO=C.DWB_NO 
                            AND B.CNS_DATE=C.DWB_BOOKING_DATE 
                            AND B.CNS_BRANCH_CODE=C.BRANCH_BRANCH_CODE 
                            AND A.UNLOADING_CNS_CNS_NO=C.DWB_NO 
                            AND A.UNLOADING_CNS_CNS_DATE=C.DWB_BOOKING_DATE 
                            AND A.UNLOADING_CNS_BRANCH_BRANCH_CO=C.BRANCH_BRANCH_CODE 
                            AND C.GOODS_DET_GOODS_CODE=D.GOODS_CODE 
                            AND A.UNLOADING_CNS_BRANCH_BRANCH_CO=xm.BRANCH_CODE 
                            AND A.UNLOADING_BRANCH_BRANCH_CODE=xm1.BRANCH_CODE 
                            AND TO_DATE(TO_CHAR(A.COF_DATE,'YYYYMM'),'YYYYMM')
                            BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                    ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                        AND TO_DATE('%(year)s%(month)s','YYYYMM') 
                            AND  xm.STATUS='VALID' 
                            AND  xm1.STATUS='VALID'   
                        
                '''%{'year' : year, 'month' : month}
            
         df_17 = pd.read_sql_query(sql_17, con)

         df_pvt_17 = pd.pivot_table(data = df_17, index = ['BKG_REGION_CODE','BKG_CONTROLLING_CODE','BKG_BRANCH_CODE'], values = ['DWB_NO','COFAMT'], aggfunc = {'DWB_NO':'count','COFAMT':'sum'}).reset_index()

         df_pvt_17 = df_pvt_17.rename(columns = {'BKG_REGION_CODE':'REGION_CODE','BKG_CONTROLLING_CODE':'CONTROLLING_CODE','BKG_BRANCH_CODE':'BRANCH_CODE','DWB_NO':'BKG_DWB_NO','COFAMT':'BKG_COF_AMT'})
         
         df_18 = df_16.merge(df_pvt_17, on = ['REGION_CODE','CONTROLLING_CODE','BRANCH_CODE'], how = 'left')

         df_pvt_17_A = pd.pivot_table(data = df_17, index = ['DLY_REGION_CODE','DLY_CONTROLLING_CODE','DLY_BRANCH_CODE'], values = ['DWB_NO','COFAMT'], aggfunc = {'DWB_NO':'count','COFAMT':'sum'}).reset_index()

         df_pvt_17_A = df_pvt_17_A.rename(columns = {'DLY_REGION_CODE':'REGION_CODE','DLY_CONTROLLING_CODE':'CONTROLLING_CODE','DLY_BRANCH_CODE':'BRANCH_CODE', 'DWB_NO':'DLY_DWB_NO','COFAMT':'DLY_COF_AMT'})

         df_19 = df_18.merge(df_pvt_17_A, on = ['REGION_CODE','CONTROLLING_CODE','BRANCH_CODE'], how = 'left')

         df_19['TOT_COF_AMT'] = df_19['BKG_COF_AMT'].add(df_19['DLY_COF_AMT'])

         def cof_amount_rank(row):

             if row < -100:

                 return -100
             else:
                 return row

         df_19['MARK 16'] = df_19['TOT_COF_AMT'].floordiv(-10000).apply(cof_amount_rank)

         sql_20 = '''SELECT 
                        REGION_CODE REGION_CODE,
                        CONTROLLING_CODE CONTROLLING_CODE,
                        BRANCH_CODE BRANCH_CODE,
                        SUM(FREIGHT) FREIGHT,
                        SUM(PROFIT) PROFIT,
                        ROUND((SUM(PROFIT)/NULLIF(SUM(FREIGHT),0)) * 100,2) PROFIT_PER
                    FROM 
                        (
                    SELECT 
                        REGION_CODE,
                        CONTROLLING_CODE,
                        BRANCH_CODE,
                        DWB_MONTH_YEAR,
                        MAX(A.FRT) FREIGHT,
                        MAX(A.IND_EXP + A.OPR_EXP) TOTAL_EXPENSES,
                        (MAX(A.FRT) - (MAX(A.IND_EXP) + MAX(A.OPR_EXP))) PROFIT,
                        ROUND(((MAX(A.FRT) - (MAX(A.IND_EXP) + MAX(A.OPR_EXP)))/NULLIF(MAX(A.FRT),0)) * 100,2) 
                    FROM 
                    (
                    SELECT 
                        xm.REGION_CODE REGION_CODE,
                        xm.CONTROLLING_CODE CONTROLLING_CODE,
                        cd.BRANCH_CODE BRANCH_CODE,
                        cd.DWB_MONTH_YEAR DWB_MONTH_YEAR,
                        cd.FREIGHT FRT,
                        cd.OPR_EXP + cd.PERSONAL_COST + cd.OS_INTEREST IND_EXP,
                        NVL(cd.PICKUP_COMM_BA,0) + NVL(cd.PICKUP_EXP,0) + NVL(cd.TOTAL_TRANSIT_EXP,0) + NVL(cd.DELIVERY_COMM_BA,0) + NVL(cd.DELIVERY_EXP,0) +  NVL(cd.MISC_DIR_EXP,0)  + NVL(cd.NON_CLN_DIR_EXP,0) +  NVL(cd.NON_CLN_DIR_EXP_EXTRA,0) OPR_EXP
                    FROM
                        CT_DOCKET_COSTING_MISC cd
                    LEFT JOIN
                        XM_BRANCHS xm ON cd.BRANCH_CODE = xm.BRANCH_CODE 
                    WHERE
                        TO_DATE(TO_CHAR(TO_DATE(cd.DWB_MONTH_YEAR,'MMYYYY'),'YYYYMM'),'YYYYMM') 
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                                            THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                                                ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                                                    AND TO_DATE('%(year)s%(month)s','YYYYMM')
                        
                        AND cd.DIVISION_CODE IN ('21','22')
                    ) A
                    GROUP BY
                        REGION_CODE,
                        CONTROLLING_CODE,
                        BRANCH_CODE,
                        DWB_MONTH_YEAR
                    ) B 
                    GROUP BY 
                        REGION_CODE,
                        CONTROLLING_CODE,
                        BRANCH_CODE

                '''%{'year':year, 'month': month}

         df_20 = pd.read_sql_query(sql_20, con_1)  

         df_20['MARK 17'] = df_20['PROFIT'].floordiv(100000).floordiv(2.78).round(0)

         df_20['MARK 18'] = df_20['PROFIT_PER'].round(0)

         df_21 = df_19.merge(df_20, on = ['REGION_CODE','CONTROLLING_CODE','BRANCH_CODE'], how = 'left')

         df_21['TOTAL MARKS'] = df_21.loc[:,['MARK 1','MARK 2', 'MARK 3','MARK 4','MARK 5','MARK 6','MARK 7','MARK 8','MARK 9','MARK 10',\
                                             'MARK 11','MARK 12','MARK 13','MARK 14','MARK 15', 'MARK 16','MARK 17', 'MARK 18']].sum(axis = 1)

         df_marks = df_21[['REGION_CODE','CONTROLLING_CODE','BRANCH_CODE','MARK 1','MARK 2', 'MARK 3','MARK 4','MARK 5','MARK 6','MARK 7','MARK 8','MARK 9','MARK 10',\
                           'MARK 11','MARK 12','MARK 13','MARK 14','MARK 15', 'MARK 16','MARK 17', 'MARK 18', 'TOTAL MARKS']].copy()

         df_desp = pd.DataFrame({'Marks' : ['Marks 1','Marks 2','Marks 3','Marks 4','Marks 5','Marks 6','Marks 7','Marks 8',\
                                 'Marks 9','Marks 10','Marks 11','Marks 12','Marks 13','Marks 14','Marks 15','Marks 16',\
                                 'Marks 17','Marks 18'],

                                 'Description' : ['BOOKING AMOUNT-SURFACE','BOOKING AMOUNT-AIR','BOOKING GROWTH-SURFACE','BOOKING GROWTH-AIR',\
                                 'DELIVERY WEIGHT-SURFACE','DELIVERY WEIGHT-AIR', 'DELIVERY WT GROWTH-SURFACE','DELIVERY WT GROWTH-AIR',\
                                 'ABOVE 90 DAYS O/S-S+A','PICKUP COST SAVING-S+A','DELIVERY COST SAVING-S+A','Air Intl BOOKING-Air Intl',\
                                 'DLY DWB NO-Total','DLY PERFORMANCE SD+ND-S+A','BILL DEDUCTION-S+A','COF ON B+D-S+A','Profit Amount-S+A',\
                                 'Profit %-S+A' ]})

         
         def to_xlsx(bytes_io):

                writer = pd.ExcelWriter(bytes_io, engine='xlsxwriter') # pylint: disable=abstract-class-instantiated

                df_21.to_excel(writer, sheet_name = 'Branch Rank Data', index = False)

                df_marks.to_excel(writer, sheet_name = 'Branch Rank', index = False)

                df_desp.to_excel(writer, sheet_name = 'Rank Description', index = False)

                workbook = writer.book

                worksheet1 = writer.sheets['Branch Rank Data']

                worksheet2 = writer.sheets['Branch Rank']

                worksheet3 = writer.sheets['Rank Description']

                border = workbook.add_format({'border': 2})

                background_color_1 = workbook.add_format({'bg_color': '#99e600'})

                background_color_2 = workbook.add_format({'bg_color': '#ffff4d'})

                background_color_3 = workbook.add_format({'bg_color': '#0dc8f2'})

                format_align = workbook.add_format({'align': 'center'})

                worksheet1.conditional_format('A2:BL755',  { 'type' : 'no_errors' , 'format' : border} )

                worksheet2.conditional_format('A2:V755',  { 'type' : 'no_errors' , 'format' : border})

                worksheet3.conditional_format('A1:B19',  { 'type' : 'no_errors' , 'format' : border} )

                worksheet1.conditional_format('A2:C755',  { 'type' : 'no_errors' , 'format' : background_color_1})

                worksheet2.conditional_format('A2:C755',  { 'type' : 'no_errors' , 'format' : background_color_1})

                worksheet3.conditional_format('A2:A19',  { 'type' : 'no_errors' , 'format' : background_color_1})

                worksheet1.conditional_format('D2:BL755',  { 'type' : 'no_errors' , 'format' : background_color_2})

                worksheet2.conditional_format('D2:V755',  { 'type' : 'no_errors' , 'format' : background_color_2})

                worksheet3.conditional_format('B2:B19',  { 'type' : 'no_errors' , 'format' : background_color_2})

                worksheet1.conditional_format('A1:BL1',  { 'type' : 'no_errors' , 'format' : background_color_3})

                worksheet2.conditional_format('A1:V1',  { 'type' : 'no_errors' , 'format' : background_color_3})

                worksheet3.conditional_format('A1:B1',  { 'type' : 'no_errors' , 'format' : background_color_3})

                worksheet1.hide_gridlines(option = 2)

                worksheet2.hide_gridlines(option = 2)

                worksheet3.hide_gridlines(option = 2)

                worksheet1.set_column('A:BL', 15.5, format_align)

                worksheet2.set_column('A:V', 15.5, format_align)

                worksheet3.set_column('A:A', 12)
                
                worksheet3.set_column('B:B', 30)

                worksheet2.write_comment('D1', 'BOOKING AMOUNT-SURFACE')

                worksheet2.write_comment('E1', 'BOOKING AMOUNT-AIR')

                worksheet2.write_comment('F1', 'BOOKING GROWTH-SURFACE')

                worksheet2.write_comment('G1', 'BOOKING GROWTH-AIR')

                worksheet2.write_comment('H1', 'DELIVERY WEIGHT-SURFACE' )

                worksheet2.write_comment('I1', 'DELIVERY WEIGHT-AIR')

                worksheet2.write_comment('J1', 'DELIVERY WT GROWTH-SURFACE')

                worksheet2.write_comment('K1', 'DELIVERY WT GROWTH-AIR')

                worksheet2.write_comment('L1', 'ABOVE 90 DAYS O/S-S+A')

                worksheet2.write_comment('M1', 'PICKUP COST SAVING-S+A')

                worksheet2.write_comment('N1', 'DELIVERY COST SAVING-S+A')

                worksheet2.write_comment('O1', 'Air Intl BOOKING-Air Intl')

                worksheet2.write_comment('P1', 'DLY DWB NO-Total')

                worksheet2.write_comment('Q1', 'DLY PERFORMANCE SD+ND-S+A')

                worksheet2.write_comment('R1', 'BILL DEDUCTION-S+A')

                worksheet2.write_comment('S1', 'COF ON B+D-S+A')

                worksheet2.write_comment('T1', 'Profit Amount-S+A')

                worksheet2.write_comment('U1', 'Profit %-S+A')

                worksheet3.write_comment('B2', '1 point = 6 Lac per Year')

                worksheet3.write_comment('B3', '1 Point = 2 Lac Per Year')

                worksheet3.write_comment('B4', 'Growth %')

                worksheet3.write_comment('B5', 'Growth %')

                worksheet3.write_comment('B6', '1 Point = 200000 Kg per year')

                worksheet3.write_comment('B7', '1 Point = 10000 Kg per year')

                worksheet3.write_comment('B8', 'Growth %')

                worksheet3.write_comment('B9', 'Growth %')

                worksheet3.write_comment('B10', '0 -> 50, 1 TO 10 -> 40, 11 TO 20 -> 30, 20 TO 30 -> 20, 30 TO 40 -> 10')

                worksheet3.write_comment('B11', '1 Point = Rs 10000.00')

                worksheet3.write_comment('B12', '1 Point = Rs 10000.00')

                worksheet3.write_comment('B13', '1 Point = Rs =50000.00')

                worksheet3.write_comment('B14', '1 Point = 547 DWB')

                worksheet3.write_comment('B15', '% of Delivery Performance Same Day+ Next Day')

                worksheet3.write_comment('B16', 'Rs 10000 = -1 Point')

                worksheet3.write_comment('B17', 'Rs 10000 = -1 Point')

                worksheet3.write_comment('B18', '1Lac =1 Point')

                worksheet3.write_comment('B19', '% of Profit %')

                writer.save()

         return send_bytes(to_xlsx, "download_branch.xlsx") 


@app.callback(Output('download2','data'),[Input('btn2','n_clicks'),
                                           Input('year','value'), 
                                           Input('month','value')], 
                                           prevent_initial_call = True)

def controlling_ranking(n_clicks, year, month):

    if n_clicks is not None and n_clicks > 0:
       
         con = cx.connect(config.CONN_STR)

         con_1 = cx.connect(config_1.CONN_STR)

         sql = '''SELECT
                         xm.REGION_CODE
                        ,xm.CONTROLLING_CODE
                        ,SUM(NVL(ct.TOT_FRT,0)) SURFACE_FRT
                        ,SUM(NVL(ct.LYA_TOT_FRT,0)) LY_SURFACE_FRT
                        ,ROUND(((SUM(NVL(ct.TOT_FRT,0)) - SUM(NVL(ct.LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(ct.LYA_TOT_FRT,0)),0)) * 100,0) SURFACE_FRT_GWT
                        ,SUM(NVL(ct.TOT_WT,0)) SURFACE_BKG_WT
                        ,SUM(NVL(ct.LYA_TOT_WT,0)) LY_SURFACE_BKG_WT
                        ,SUM(NVL(ct.DLY_WT,0)) SURFACE_DLY_WT
                        ,SUM(NVL(ct.LYA_DLY_WT,0)) LY_SURFACE_DLY_WT
                        ,ROUND(((SUM(NVL(ct.DLY_WT,0)) - SUM(NVL(ct.LYA_DLY_WT,0)))/NULLIF(SUM(NVL(ct.LYA_DLY_WT,0)),0)) * 100,0) SURFACE_WT_GWT
                FROM
                         CT_BUSINESS_GROWTH_NEW_IMPL ct
                LEFT JOIN
                         XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE                     
                WHERE
                    LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(ct.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                            BETWEEN '01-APR-'||CASE WHEN TO_CHAR(LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                    THEN TO_CHAR(TO_NUMBER(TO_CHAR(LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                        ELSE TO_CHAR(LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                            AND LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                
                    AND ct.DIVISION_CODE = '21'
                    AND ct.REGION_CODE <> 'XCRP'
                    AND xm.SATTLITEBRANCH NOT IN ('C','H','R')
                    AND xm.REGION_CODE <> xm.CONTROLLING_CODE
                GROUP BY
                   xm.REGION_CODE
                  ,xm.CONTROLLING_CODE
                ORDER BY
                  xm.REGION_CODE ASC

          '''%{'year':year,'month':month}


         df_0 = pd.read_sql_query(sql, con).replace(np.nan,0)

         df_0['MARK 1'] = df_0['SURFACE_FRT'].floordiv(1200000).mul(1.556).round(0)
            
         df_0['MARK 5'] =  df_0['SURFACE_DLY_WT'].floordiv(200000).mul(0.987).round(0)
            
         df_0['MARK 3'] = [x if x <= 50 else 50 for x in df_0['SURFACE_FRT_GWT']]
        
         df_0['MARK 7'] = [x if x <= 50 else 50 for x in df_0['SURFACE_WT_GWT']]

         sql_1 = '''SELECT
                         xm.REGION_CODE
                        ,xm.CONTROLLING_CODE
                        ,SUM(NVL(ct.TOT_FRT,0)) AIR_FRT
                        ,SUM(NVL(ct.LYA_TOT_FRT,0)) LY_AIR_FRT
                        ,ROUND(((SUM(NVL(ct.TOT_FRT,0)) - SUM(NVL(ct.LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(ct.LYA_TOT_FRT,0)),0)) * 100,0) AIR_FRT_GWT
                        ,SUM(NVL(ct.DLY_WT,0)) AIR_DLY_WT
                        ,SUM(NVL(ct.LYA_DLY_WT,0)) LY_AIR_DLY_WT
                        ,ROUND(((SUM(NVL(ct.DLY_WT,0)) - SUM(NVL(ct.LYA_DLY_WT,0)))/NULLIF(SUM(NVL(ct.LYA_DLY_WT,0)),0)) * 100,0) AIR_WT_GWT
                    FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL ct
                    LEFT JOIN
                        XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE
                    WHERE
                        LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(ct.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                        
                        AND ct.DIVISION_CODE = '22'
                        AND ct.REGION_CODE <> 'XCRP'
                        AND xm.SATTLITEBRANCH NOT IN ('C','H','R')
                        AND xm.REGION_CODE <> xm.CONTROLLING_CODE
                    GROUP BY
                         xm.REGION_CODE
                        ,xm.CONTROLLING_CODE      
                    ORDER BY
                         xm.REGION_CODE ASC
                '''%{'year':year,
                     'month':month
                    }


         df_1 = pd.read_sql_query(sql_1, con).replace(np.nan, 0)

         df_1['MARK 2'] = df_1['AIR_FRT'].floordiv(200000).mul(1.082).round(0)
            
         df_1['MARK 6'] =  df_1['AIR_DLY_WT'].floordiv(10000).mul(2.490).round(0)
            
         df_1['MARK 4'] = [x if x <= 50 else 50 for x in df_1['AIR_FRT_GWT']]
        
         df_1['MARK 8'] = [x if x <= 50 else 50 for x in df_1['AIR_WT_GWT']]
            
         df_2 = df_0.merge(df_1, on = ['REGION_CODE','CONTROLLING_CODE'], how = 'left')

         sql_3 = '''SELECT 
                         a.REGION_CODE 
                        ,a.CONTROLLING_CODE
                        ,ROUND(SUM(NVL(b.OS_GT_90,0)),0) OS_ABOVE_90
                        ,ROUND(SUM(NVL(a.TBB_FREIGHT,0)),0) BUSINESS_AMT_TBB
                        ,ROUND(SUM(NVL(a.TBB_FREIGHT,0))/365,0) BUSINESS_PD
                        ,ROUND(NVL(SUM(NVL(b.OS_GT_90,0))/NULLIF((SUM(NVL(a.TBB_FREIGHT,0))/365),0),0),0) OS_TBB_PD
                    FROM 
                        (
                        SELECT 
                             xm.REGION_CODE 
                            ,xm.CONTROLLING_CODE 
                            ,SUM(NVL(ct.TBB_FRT,0)) TBB_FREIGHT
                        FROM 
                            CT_BUSINESS_GROWTH_NEW_IMPL ct
                        LEFT JOIN
                               XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE
                        WHERE 
                             LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(ct.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                            
                            AND ct.DIVISION_CODE IN ('21','22')
                            AND ct.REGION_CODE <> 'XCRP'
                            AND xm.SATTLITEBRANCH NOT IN ('C','H','R')
                        GROUP BY 
                             xm.REGION_CODE 
                            ,xm.CONTROLLING_CODE 
                        ) a
                        LEFT JOIN
                        (
                        SELECT 
                             xm.REGION_CODE 
                            ,xm.CONTROLLING_CODE 
                            ,SUM(NVL(ct.OS_91TO120_DAYS,0)) + SUM(NVL(ct.OS_121TO180_DAYS,0)) + SUM(NVL(ct.OS_181TO365_DAYS,0)) + SUM(NVL(ct.OS_ABOVE_365_DAYS,0)) OS_GT_90
                        FROM 
                            CT_AGEWISE_BILLED_OS ct
                        LEFT JOIN
                            XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE
                        WHERE 
                             ct.REPORT_TYPE = 'BILLWISE'
                             AND ct.DIVISION_CODE IN ('21','22')
                             AND TRUNC(BILL_DATE) <= TRUNC(SYSDATE)
                             AND TRUNC(AUD_DATE) = TRUNC(SYSDATE)
                             AND NOT EXISTS(
                                            SELECT 
                                                  'X'
                                            FROM 
                                                CT_AGEWISE_BILLED_OS ca
                                            WHERE
                                                ct.BRANCH_CODE = ca.BRANCH_CODE 
                                                AND ct.BILL_NO = ca.BILL_NO 
                                                AND ct.BILL_DATE = ca.BILL_DATE 
                                                AND ca.REALISE_FLAG = 'R'
                                                AND ca.UPTO_BCS_DATE <= TRUNC(SYSDATE)
                                           )
                        GROUP BY 
                             xm.REGION_CODE 
                            ,xm.CONTROLLING_CODE 
                        ) b
                    ON
                        a.CONTROLLING_CODE = b.CONTROLLING_CODE
                    GROUP BY 
                         a.REGION_CODE 
                        ,a.CONTROLLING_CODE
                    ORDER BY 
                        a.REGION_CODE ASC
                '''%{'year' : year,'month' : month}

         df_3 = pd.read_sql_query(sql_3, con)

         df_4 = df_2.merge(df_3, on = ['REGION_CODE','CONTROLLING_CODE'], how = 'left')

         def os_tbb_rank(row):

             if row == 0:
                return 50
             elif row >= 1 and row <= 10:
                return 40
             elif row >= 11 and row <= 20:
                 return 30
             elif row > 20 and row <= 30:
                 return 20
             elif row > 30 and row <= 40:
                 return 10
             else:
                 return 0

         df_4['MARK 9'] = df_4['OS_TBB_PD'].apply(os_tbb_rank)

         sql_5 = '''    SELECT
                            Q2.TCS_REGION REGION_CODE,
                            Q2.TCS_CONTROLLING CONTROLLING_CODE,
                            NVL(Q1.LY_COST,0) LY_PC_COST,
                            NVL(Q2.CY_COST,0) CY_PC_COST
                        FROM
                        (
                        SELECT 
                            X.REGION_CODE TCS_REGION,
                            X.CONTROLLING_CODE TCS_CONTROLLING,
                            ROUND(SUM(NVL(C.TOTALCOST,0))/NULLIF(SUM(NVL(C.ACTUAL_WT,0)),0),2) LY_COST
                        FROM 
                            CT_PICKDLY_COST C,
                            XM_BRANCHS X 
                        WHERE 
                            C.TCSBRANCH=X.BRANCH_CODE 
                            AND TO_DATE(TO_CHAR(TO_DATE(C.MONTH_YEAR,'MMYYYY'),'YYYYMM'),'YYYYMM')
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'MM') IN ('01','02','03')
                                      THEN TO_CHAR(TO_NUMBER(TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'YYYY'))-1)
                                         ELSE TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'YYYY') END
                                           AND ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12)
                            AND C.TCSTYPE NOT IN ('OD','DC')   
                            AND VEHTYPE!='TOT' 
                        GROUP BY
                            X.CONTROLLING_CODE,
                            X.REGION_CODE
                        ) Q1
                        RIGHT JOIN
                        (
                        SELECT 
                            X.REGION_CODE TCS_REGION,
                            X.CONTROLLING_CODE TCS_CONTROLLING,
                            ROUND(SUM(NVL(C.TOTALCOST,0))/NULLIF(SUM(NVL(C.ACTUAL_WT,0)),0),2) CY_COST
                        FROM 
                            CT_PICKDLY_COST C,
                            XM_BRANCHS X 
                        WHERE 
                            C.TCSBRANCH=X.BRANCH_CODE 
                            AND TO_DATE(TO_CHAR(TO_DATE(C.MONTH_YEAR,'MMYYYY'),'YYYYMM'),'YYYYMM')
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                      THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                         ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                           AND TO_DATE('%(year)s%(month)s','YYYYMM')
                            AND C.TCSTYPE NOT IN ('OD','DC')   
                            AND VEHTYPE!='TOT' 
                        GROUP BY
                            X.CONTROLLING_CODE,
                            X.REGION_CODE
                        ) Q2
                        ON
                        Q1.TCS_CONTROLLING = Q2.TCS_CONTROLLING
                        ORDER BY
                        Q2.TCS_CONTROLLING

                    '''%{'year':year,'month':month}
        
         df_5 = pd.read_sql_query(sql_5, con)

         df_6 = df_4.merge(df_5, on = ['REGION_CODE','CONTROLLING_CODE'], how = 'left')

         df_6['AMT_SAVING_PC'] = df_6['LY_PC_COST'].sub(df_6['CY_PC_COST']).mul(df_0['SURFACE_BKG_WT'])

         def pickup_amt_saving(row):

             if row > 50:
                 return 50
             else:
                 return row

         df_6['MARK 10'] = df_6['AMT_SAVING_PC'].floordiv(50000).apply(pickup_amt_saving)

         sql_7 = ''' SELECT 
                            Q2.TCS_REGION REGION_CODE,
                            Q2.TCS_CONTROLLING CONTROLLING_CODE,
                            NVL(Q1.LY_COST, 0) LY_DY_COST,
                            NVL(Q2.CY_COST, 0) CY_DY_COST
                        FROM
                        (
                        SELECT 
                            X.REGION_CODE TCS_REGION,
                            X.CONTROLLING_CODE TCS_CONTROLLING,
                            ROUND(SUM(NVL(C.TOTALCOST,0))/NULLIF(SUM(NVL(C.ACTUAL_WT,0)),0),2) LY_COST
                        FROM 
                            CT_PICKDLY_COST C,
                            XM_BRANCHS X 
                        WHERE 
                            C.TCSBRANCH=X.BRANCH_CODE 
                            AND TO_DATE(TO_CHAR(TO_DATE(C.MONTH_YEAR,'MMYYYY'),'YYYYMM'),'YYYYMM')
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'MM') IN ('01','02','03')
                                      THEN TO_CHAR(TO_NUMBER(TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'YYYY'))-1)
                                         ELSE TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'YYYY') END
                                           AND ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12)
                            AND C.TCSTYPE IN ('OD','DC')   
                            AND VEHTYPE!='TOT' 
                        GROUP BY
                             X.REGION_CODE
                            ,X.CONTROLLING_CODE
                        ) Q1
                        RIGHT JOIN
                        (
                        SELECT 
                            X.REGION_CODE TCS_REGION,
                            X.CONTROLLING_CODE TCS_CONTROLLING,
                            ROUND(SUM(NVL(C.TOTALCOST,0))/NULLIF(SUM(NVL(C.ACTUAL_WT,0)),0),2) CY_COST
                        FROM 
                            CT_PICKDLY_COST C,
                            XM_BRANCHS X 
                        WHERE 
                            C.TCSBRANCH=X.BRANCH_CODE 
                            AND TO_DATE(TO_CHAR(TO_DATE(C.MONTH_YEAR,'MMYYYY'),'YYYYMM'),'YYYYMM')
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                      THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                         ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                           AND TO_DATE('%(year)s%(month)s','YYYYMM')
                            AND C.TCSTYPE IN ('OD','DC')   
                            AND VEHTYPE!='TOT' 
                        GROUP BY
                            X.REGION_CODE
                            ,X.CONTROLLING_CODE
                        ) Q2
                        ON
                        Q1.TCS_REGION = Q2.TCS_REGION
                        AND Q1.TCS_CONTROLLING = Q2.TCS_CONTROLLING
                    '''%{'year':year,'month':month}
         
         df_7 = pd.read_sql_query(sql_7, con)

         df_8 = df_6.merge(df_7, on = ['REGION_CODE','CONTROLLING_CODE'], how = 'left')

         df_8['AMT_SAVING_DC'] = df_8['LY_DY_COST'].sub(df_8['CY_DY_COST']).mul(df_0['SURFACE_DLY_WT'])

         def delivery_cost_amt_saving(row):

             if row > 50:
                 return 50
             else:
                 return row

         df_8['MARK 11'] = df_8['AMT_SAVING_DC'].floordiv(50000).apply(delivery_cost_amt_saving)

         sql_9 = '''SELECT
                         xm.REGION_CODE
                        ,xm.CONTROLLING_CODE
                        ,SUM(NVL(ct.TOT_FRT,0)) INTL_AIR_FRT
                        ,SUM(NVL(ct.LYA_TOT_FRT,0)) LY_INTL_AIR_FRT
                    FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL ct
                    LEFT JOIN
                        XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE 
                    WHERE
                        LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(ct.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                        
                        AND ct.DIVISION_CODE = '26'
                        AND ct.REGION_CODE <> 'XCRP'
                        AND xm.SATTLITEBRANCH NOT IN ('C','H','R')
                    GROUP BY
                        xm.REGION_CODE
                        ,xm.CONTROLLING_CODE
                    ORDER BY
                        xm.REGION_CODE ASC
                  '''%{'year':year,'month':month}

         df_9 = pd.read_sql_query(sql_9, con)

         df_9['MARK 12'] = df_9['INTL_AIR_FRT'].floordiv(50000).mul(2.350).round(0)

         df_10 = df_8.merge(df_9, on = ['REGION_CODE','CONTROLLING_CODE'], how = 'left')

         sql_11 = '''SELECT
                             xm.REGION_CODE
                            ,xm.CONTROLLING_CODE
                            ,SUM(NVL(ct.DLY_DWB,0)) DLYDWB        
                    FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL ct
                    LEFT JOIN
                        XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE 
                    WHERE
                        LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(ct.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                    
                        AND ct.REGION_CODE <> 'XCRP'
                        AND xm.SATTLITEBRANCH NOT IN ('C','H','R')
                    GROUP BY
                         xm.REGION_CODE
                        ,xm.CONTROLLING_CODE
                    ORDER BY
                        xm.REGION_CODE ASC
                   '''%{'year':year, 'month':month}

         df_11 = pd.read_sql_query(sql_11, con)

         df_11['MARK 13'] = df_11['DLYDWB'].floordiv(1542).round(0)

         df_12 = df_10.merge(df_11, on = ['REGION_CODE','CONTROLLING_CODE'], how = 'left')

         sql_13 = '''SELECT 
                            xm.REGION_CODE REGION_CODE, 
                            xm.CONTROLLING_CODE CONTROLLING_CODE,
                            SUM(NVL(cp.DWB_ARRIVED,0)) TOTAL_DLY, 
                            SUM(NVL(cp.DWB_DLVRD_SAME_DAY,0)) SAME_DAY_DLY, 
                            SUM(NVL(cp.DLVRD_NEXT_DAY,0)) NEXT_DAY_DLY
                    FROM 
                        CT_BA_DBA_DLY_PERFORMANCE cp
                    LEFT JOIN
                        XM_BRANCHS xm ON cp.DLY_BRANCH = xm.BRANCH_CODE
                    WHERE 
                        TO_DATE(TO_CHAR(TO_DATE(cp.MONTH_YEAR,'MMYYYY'),'YYYYMM'),'YYYYMM')
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                                            THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                                                ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                                                AND TO_DATE('%(year)s%(month)s','YYYYMM')

                    GROUP BY
                        xm.REGION_CODE
                       ,xm.CONTROLLING_CODE
                '''%{'year':year,'month':month}
         
         df_13 = pd.read_sql_query(sql_13, con)

         df_13['MARK 14'] = (((df_13['SAME_DAY_DLY'].add(df_13['NEXT_DAY_DLY'])).div(df_13['TOTAL_DLY'])).mul(100)).round(0)

         df_14 = df_12.merge(df_13, on = ['REGION_CODE','CONTROLLING_CODE'], how = 'left')

         sql_15 = '''SELECT 
                            xm.REGION_CODE REGION_CODE,
                            xm.CONTROLLING_CODE CONTROLLING_CODE, 
                            SUM(ct.CREDIT_NOTE_AMOUNT) CR_NOTE_AMT
                        FROM 
                            CT_CREDIT_NOTE ct
                        LEFT JOIN
                            XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE
                        WHERE 
                            TO_DATE(TO_CHAR(CREDIT_NOTE_DATE,'YYYYMM'),'YYYYMM') BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                                                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                                                                            ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                                                                                AND TO_DATE('%(year)s%(month)s','YYYYMM')
                            AND APPROVAL_FLAG = 'Y'
                        GROUP BY 
                           xm.REGION_CODE
                           ,xm.CONTROLLING_CODE
                 '''%{'year' : year, 'month' : month}

         df_15 = pd.read_sql_query(sql_15, con)

         def cr_note_amt_rank(row):
             if row < -100:
                 return -100
             else:
                 return row

         df_15['MARK 15'] = df_15['CR_NOTE_AMT'].floordiv(-100000).apply(cr_note_amt_rank)

         df_15['MARK 15'] = df_15['MARK 15'].round(0)

         df_16 = df_14.merge(df_15, on = ['REGION_CODE','CONTROLLING_CODE'], how = 'left')

         sql_17 = ''' SELECT 
                             xm.REGION_CODE BKG_REGION_CODE
                            ,xm.CONTROLLING_CODE BKG_CONTROLLING_CODE
                            ,A.UNLOADING_CNS_BRANCH_BRANCH_CO BKG_BRANCH_CODE
                            ,A.UNLOADING_CNS_CNS_NO DWB_NO
                            ,xm1.REGION_CODE DLY_REGION_CODE
                            ,xm1.CONTROLLING_CODE DLY_CONTROLLING_CODE
                            ,A.UNLOADING_BRANCH_BRANCH_CODE DLY_BRANCH_CODE
                            ,A.CLAIM_AMOUNT COFAMT 
                      FROM 
                             CT_COF A
                            ,CT_COF_CHK B
                            ,CT_DWB C
                            ,CM_GOODS_DETAIL D
                            ,xm_branchs xm
                            ,xm_branchs xm1 
                      WHERE 
                            A.UNLOADING_CNS_CNS_NO=B.CNS_NO 
                            AND A.UNLOADING_CNS_CNS_DATE=B.CNS_DATE 
                            AND UNLOADING_CNS_BRANCH_BRANCH_CO=B.CNS_BRANCH_CODE 
                            AND B.CNS_NO=C.DWB_NO 
                            AND B.CNS_DATE=C.DWB_BOOKING_DATE 
                            AND B.CNS_BRANCH_CODE=C.BRANCH_BRANCH_CODE 
                            AND A.UNLOADING_CNS_CNS_NO=C.DWB_NO 
                            AND A.UNLOADING_CNS_CNS_DATE=C.DWB_BOOKING_DATE 
                            AND A.UNLOADING_CNS_BRANCH_BRANCH_CO=C.BRANCH_BRANCH_CODE 
                            AND C.GOODS_DET_GOODS_CODE=D.GOODS_CODE 
                            AND A.UNLOADING_CNS_BRANCH_BRANCH_CO=xm.BRANCH_CODE 
                            AND A.UNLOADING_BRANCH_BRANCH_CODE=xm1.BRANCH_CODE 
                            AND TO_DATE(TO_CHAR(A.COF_DATE,'YYYYMM'),'YYYYMM')
                            BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                    ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                        AND TO_DATE('%(year)s%(month)s','YYYYMM') 
                            AND  xm.STATUS='VALID' 
                            AND  xm1.STATUS='VALID'   
                        
                '''%{'year' : year, 'month' : month}
            
         df_17 = pd.read_sql_query(sql_17, con)

         df_pvt_17 = pd.pivot_table(data = df_17, index = ['BKG_REGION_CODE','BKG_CONTROLLING_CODE'], values = ['DWB_NO','COFAMT'], aggfunc = {'DWB_NO':'count','COFAMT':'sum'}).reset_index()

         df_pvt_17 = df_pvt_17.rename(columns = {'BKG_REGION_CODE':'REGION_CODE','BKG_CONTROLLING_CODE':'CONTROLLING_CODE','DWB_NO':'BKG_DWB_NO','COFAMT':'BKG_COF_AMT'})
         
         df_18 = df_16.merge(df_pvt_17, on = ['REGION_CODE','CONTROLLING_CODE'], how = 'left')

         df_pvt_17_A = pd.pivot_table(data = df_17, index = ['DLY_REGION_CODE','DLY_CONTROLLING_CODE'], values = ['DWB_NO','COFAMT'], aggfunc = {'DWB_NO':'count','COFAMT':'sum'}).reset_index()

         df_pvt_17_A = df_pvt_17_A.rename(columns = {'DLY_REGION_CODE':'REGION_CODE','DLY_CONTROLLING_CODE':'CONTROLLING_CODE', 'DWB_NO':'DLY_DWB_NO','COFAMT':'DLY_COF_AMT'})

         df_19 = df_18.merge(df_pvt_17_A, on = ['REGION_CODE','CONTROLLING_CODE'], how = 'left')

         df_19['TOT_COF_AMT'] = df_19['BKG_COF_AMT'].add(df_19['DLY_COF_AMT'])

         def cof_amount_rank(row):

             if row < -100:
                 return -100
             else:
                 return row

         df_19['MARK 16'] = df_19['TOT_COF_AMT'].floordiv(-100000).apply(cof_amount_rank)

         sql_20 = '''SELECT 
                        REGION_CODE,
                        CONTROLLING_CODE,
                        SUM(FREIGHT) FREIGHT,
                        SUM(PROFIT) PROFIT,
                        ROUND((SUM(PROFIT)/NULLIF(SUM(FREIGHT),0)) * 100,2) PROFIT_PER
                    FROM 
                        (
                    SELECT 
                        DWB_MONTH_YEAR,
                        REGION_CODE,
                        CONTROLLING_CODE,
                        MAX(A.FRT) FREIGHT,
                        MAX(A.IND_EXP + A.OPR_EXP) TOTAL_EXPENSES,
                        (MAX(A.FRT) - (MAX(A.IND_EXP) + MAX(A.OPR_EXP))) PROFIT,
                        ROUND(((MAX(A.FRT) - (MAX(A.IND_EXP) + MAX(A.OPR_EXP)))/NULLIF(MAX(A.FRT),0)) * 100,2) 
                    FROM 
                    (
                    SELECT 
                        cd.DWB_MONTH_YEAR,
                        xm.REGION_CODE REGION_CODE,
                        xm.CONTROLLING_CODE CONTROLLING_CODE,
                        cd.FREIGHT FRT,
                        cd.OPR_EXP + cd.PERSONAL_COST + cd.OS_INTEREST IND_EXP,
                        NVL(cd.PICKUP_COMM_BA,0) + NVL(cd.PICKUP_EXP,0) + NVL(cd.TOTAL_TRANSIT_EXP,0) + NVL(cd.DELIVERY_COMM_BA,0) + NVL(cd.DELIVERY_EXP,0) +  NVL(cd.MISC_DIR_EXP,0)  + NVL(cd.NON_CLN_DIR_EXP,0) +  NVL(cd.NON_CLN_DIR_EXP_EXTRA,0) OPR_EXP
                    FROM
                        CT_DOCKET_COSTING_MISC cd
                    LEFT JOIN
                        XM_BRANCHS xm ON cd.BRANCH_CODE = xm.BRANCH_CODE 
                    WHERE
                        TO_DATE(TO_CHAR(TO_DATE(cd.DWB_MONTH_YEAR,'MMYYYY'),'YYYYMM'),'YYYYMM') 
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                                            THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                                                ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                                                    AND TO_DATE('%(year)s%(month)s','YYYYMM')
                 
                         AND DIVISION_CODE IN ('21','22')
                    ) A
                    GROUP BY
                    DWB_MONTH_YEAR,
                    REGION_CODE,
                    CONTROLLING_CODE
                    ) B 
                    GROUP BY 
                     REGION_CODE
                    ,CONTROLLING_CODE

                '''%{'year':year, 'month': month}

         df_20 = pd.read_sql_query(sql_20, con_1)  

         df_20['MARK 17'] = df_20['PROFIT'].floordiv(100000).floordiv(1.065).round(0)

         df_20['MARK 18'] = df_20['PROFIT_PER'].round(0)

         df_21 = df_19.merge(df_20, on = ['REGION_CODE','CONTROLLING_CODE'], how = 'left')

         df_21['TOTAL MARKS'] = df_21.loc[:,['MARK 1','MARK 2', 'MARK 3','MARK 4','MARK 5','MARK 6','MARK 7','MARK 8','MARK 9','MARK 10',\
                                             'MARK 11','MARK 12','MARK 13','MARK 14','MARK 15', 'MARK 16','MARK 17', 'MARK 18']].sum(axis = 1)

         df_marks = df_21[['REGION_CODE','CONTROLLING_CODE','MARK 1','MARK 2', 'MARK 3','MARK 4','MARK 5','MARK 6','MARK 7','MARK 8','MARK 9','MARK 10',\
                           'MARK 11','MARK 12','MARK 13','MARK 14','MARK 15', 'MARK 16','MARK 17', 'MARK 18', 'TOTAL MARKS']].copy()

         df_desp = pd.DataFrame({'Marks' : ['Marks 1','Marks 2','Marks 3','Marks 4','Marks 5','Marks 6','Marks 7','Marks 8',\
                                 'Marks 9','Marks 10','Marks 11','Marks 12','Marks 13','Marks 14','Marks 15','Marks 16',\
                                 'Marks 17','Marks 18'],

                                 'Description' : ['BOOKING AMOUNT-SURFACE','BOOKING AMOUNT-AIR','BOOKING GROWTH-SURFACE','BOOKING GROWTH-AIR',\
                                 'DELIVERY WEIGHT-SURFACE','DELIVERY WEIGHT-AIR', 'DELIVERY WT GROWTH-SURFACE','DELIVERY WT GROWTH-AIR',\
                                 'ABOVE 90 DAYS O/S-S+A','PICKUP COST SAVING-S+A','DELIVERY COST SAVING-S+A','Air Intl BOOKING-Air Intl',\
                                 'DLY DWB NO-Total','DLY PERFORMANCE SD+ND-S+A','BILL DEDUCTION-S+A','COF ON B+D-S+A','Profit Amount-S+A',\
                                 'Profit %-S+A' ]})

         def to_xlsx(bytes_io):

                writer = pd.ExcelWriter(bytes_io, engine='xlsxwriter') # pylint: disable=abstract-class-instantiated

                df_21.to_excel(writer, sheet_name = 'Controlling Rank Data', index = False)

                df_marks.to_excel(writer, sheet_name = 'Controlling Rank', index = False)

                df_desp.to_excel(writer, sheet_name = 'Rank Description', index = False)

                workbook = writer.book

                worksheet1 = writer.sheets['Controlling Rank Data']

                worksheet2 = writer.sheets['Controlling Rank']

                worksheet3 = writer.sheets['Rank Description']

                border = workbook.add_format({'border': 2})

                background_color_1 = workbook.add_format({'bg_color': '#99e600'})

                background_color_2 = workbook.add_format({'bg_color': '#ffff4d'})

                background_color_3 = workbook.add_format({'bg_color': '#0dc8f2'})

                format_align = workbook.add_format({'align': 'center'})

                worksheet1.conditional_format('A2:BH54',  { 'type' : 'no_errors' , 'format' : border} )

                worksheet2.conditional_format('A2:U54',  { 'type' : 'no_errors' , 'format' : border})

                worksheet3.conditional_format('A1:B19',  { 'type' : 'no_errors' , 'format' : border} )

                worksheet1.conditional_format('A2:B54',  { 'type' : 'no_errors' , 'format' : background_color_1})

                worksheet2.conditional_format('A2:B54',  { 'type' : 'no_errors' , 'format' : background_color_1})

                worksheet3.conditional_format('A2:A19',  { 'type' : 'no_errors' , 'format' : background_color_1})

                worksheet1.conditional_format('C2:BH54',  { 'type' : 'no_errors' , 'format' : background_color_2})

                worksheet2.conditional_format('B2:U54',  { 'type' : 'no_errors' , 'format' : background_color_2})

                worksheet3.conditional_format('B2:B19',  { 'type' : 'no_errors' , 'format' : background_color_2})

                worksheet1.conditional_format('A1:BH1',  { 'type' : 'no_errors' , 'format' : background_color_3})

                worksheet2.conditional_format('A1:U1',  { 'type' : 'no_errors' , 'format' : background_color_3})

                worksheet3.conditional_format('A1:B1',  { 'type' : 'no_errors' , 'format' : background_color_3})

                worksheet1.hide_gridlines(option = 2)

                worksheet2.hide_gridlines(option = 2)

                worksheet3.hide_gridlines(option = 2)

                worksheet1.set_column('A:BH', 15.5, format_align)

                worksheet2.set_column('A:U', 15.5, format_align)

                worksheet3.set_column('A:A', 12)
                
                worksheet3.set_column('B:B', 30)

                worksheet2.write_comment('C1', 'BOOKING AMOUNT-SURFACE')

                worksheet2.write_comment('D1', 'BOOKING AMOUNT-AIR')

                worksheet2.write_comment('E1', 'BOOKING GROWTH-SURFACE')

                worksheet2.write_comment('F1', 'BOOKING GROWTH-AIR')

                worksheet2.write_comment('G1', 'DELIVERY WEIGHT-SURFACE' )

                worksheet2.write_comment('H1', 'DELIVERY WEIGHT-AIR')

                worksheet2.write_comment('I1', 'DELIVERY WT GROWTH-SURFACE')

                worksheet2.write_comment('J1', 'DELIVERY WT GROWTH-AIR')

                worksheet2.write_comment('K1', 'ABOVE 90 DAYS O/S-S+A')

                worksheet2.write_comment('L1', 'PICKUP COST SAVING-S+A')

                worksheet2.write_comment('M1', 'DELIVERY COST SAVING-S+A')

                worksheet2.write_comment('N1', 'Air Intl BOOKING-Air Intl')

                worksheet2.write_comment('O1', 'DLY DWB NO-Total')

                worksheet2.write_comment('P1', 'DLY PERFORMANCE SD+ND-S+A')

                worksheet2.write_comment('Q1', 'BILL DEDUCTION-S+A')

                worksheet2.write_comment('R1', 'COF ON B+D-S+A')

                worksheet2.write_comment('S1', 'Profit Amount-S+A')

                worksheet2.write_comment('T1', 'Profit %-S+A')

                worksheet3.write_comment('B2', '1 point = 12 Lac per Year')

                worksheet3.write_comment('B3', '1 Point = 2 Lac Per Year')

                worksheet3.write_comment('B4', 'Growth %')

                worksheet3.write_comment('B5', 'Growth %')

                worksheet3.write_comment('B6', '1 Point = 200000 Kg per year')

                worksheet3.write_comment('B7', '1 Point = 10000 Kg per year')

                worksheet3.write_comment('B8', 'Growth %')

                worksheet3.write_comment('B9', 'Growth %')

                worksheet3.write_comment('B10', '0 -> 50, 1 TO 10 -> 40, 11 TO 20 -> 30, 20 TO 30 -> 20, 30 TO 40 -> 10')

                worksheet3.write_comment('B11', '1 Point = Rs 50000.00')

                worksheet3.write_comment('B12', '1 Point = Rs 50000.00')

                worksheet3.write_comment('B13', '1 Point = Rs 50000.00')

                worksheet3.write_comment('B14', '1 Point = 1164 DWB')

                worksheet3.write_comment('B15', '% of Delivery Performance Same Day+ Next Day')

                worksheet3.write_comment('B16', 'Rs 100000 = -1 Point')

                worksheet3.write_comment('B17', 'Rs 100000 = -1 Point')

                worksheet3.write_comment('B18', '1Lac =1 Point')

                worksheet3.write_comment('B19', '% of Profit %')

                writer.save()

         return send_bytes(to_xlsx, "download_controlling.xlsx")
                 
@app.callback(Output('download3','data'),[Input('btn3','n_clicks'),
                                           Input('year','value'), 
                                           Input('month','value')], 
                                           prevent_initial_call = True)

def region_ranking(n_clicks, year, month):

    if n_clicks is not None and n_clicks > 0:

         con = cx.connect(config.CONN_STR)

         con_1 = cx.connect(config_1.CONN_STR)

         sql = '''SELECT
                         xm.REGION_CODE
                        ,SUM(NVL(ct.TOT_FRT,0)) SURFACE_FRT
                        ,SUM(NVL(ct.LYA_TOT_FRT,0)) LY_SURFACE_FRT
                        ,ROUND(((SUM(NVL(ct.TOT_FRT,0)) - SUM(NVL(ct.LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(ct.LYA_TOT_FRT,0)),0)) * 100,0) SURFACE_FRT_GWT
                        ,SUM(NVL(ct.TOT_WT,0)) SURFACE_BKG_WT
                        ,SUM(NVL(ct.LYA_TOT_WT,0)) LY_SURFACE_BKG_WT
                        ,SUM(NVL(ct.DLY_WT,0)) SURFACE_DLY_WT
                        ,SUM(NVL(ct.LYA_DLY_WT,0)) LY_SURFACE_DLY_WT
                        ,ROUND(((SUM(NVL(ct.DLY_WT,0)) - SUM(NVL(ct.LYA_DLY_WT,0)))/NULLIF(SUM(NVL(ct.LYA_DLY_WT,0)),0)) * 100,0) SURFACE_WT_GWT
                FROM
                         CT_BUSINESS_GROWTH_NEW_IMPL ct
                LEFT JOIN
                         XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE                     
                WHERE
                    LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(ct.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                            BETWEEN '01-APR-'||CASE WHEN TO_CHAR(LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                    THEN TO_CHAR(TO_NUMBER(TO_CHAR(LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                        ELSE TO_CHAR(LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                            AND LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                
                    AND ct.DIVISION_CODE = '21'
                    AND ct.REGION_CODE <> 'XCRP'
                    
                GROUP BY
                   xm.REGION_CODE
         
                ORDER BY
                  xm.REGION_CODE ASC

          '''%{'year':year,'month':month}


         df_0 = pd.read_sql_query(sql, con).replace(np.nan,0)

         df_0['MARK 1'] = df_0['SURFACE_FRT'].floordiv(5000000).mul(1.750).round(0)
            
         df_0['MARK 5'] =  df_0['SURFACE_DLY_WT'].floordiv(700000).mul(0.854).round(0)
            
         df_0['MARK 3'] = [x if x <= 50 else 50 for x in df_0['SURFACE_FRT_GWT']]
        
         df_0['MARK 7'] = [x if x <= 50 else 50 for x in df_0['SURFACE_WT_GWT']]

         sql_1 = '''SELECT
                         xm.REGION_CODE
                        ,SUM(NVL(ct.TOT_FRT,0)) AIR_FRT
                        ,SUM(NVL(ct.LYA_TOT_FRT,0)) LY_AIR_FRT
                        ,ROUND(((SUM(NVL(ct.TOT_FRT,0)) - SUM(NVL(ct.LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(ct.LYA_TOT_FRT,0)),0)) * 100,0) AIR_FRT_GWT
                        ,SUM(NVL(ct.DLY_WT,0)) AIR_DLY_WT
                        ,SUM(NVL(ct.LYA_DLY_WT,0)) LY_AIR_DLY_WT
                        ,ROUND(((SUM(NVL(ct.DLY_WT,0)) - SUM(NVL(ct.LYA_DLY_WT,0)))/NULLIF(SUM(NVL(ct.LYA_DLY_WT,0)),0)) * 100,0) AIR_WT_GWT
                    FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL ct
                    LEFT JOIN
                        XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE
                    WHERE
                        LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(ct.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                        
                        AND ct.DIVISION_CODE = '22'
                        AND ct.REGION_CODE <> 'XCRP'
                       
                    GROUP BY
                         xm.REGION_CODE

                    ORDER BY
                         xm.REGION_CODE ASC
                '''%{'year': year,'month': month}


         df_1 = pd.read_sql_query(sql_1, con).replace(np.nan, 0)

         df_1['MARK 2'] = df_1['AIR_FRT'].floordiv(600000).mul(1.572).round(0)
            
         df_1['MARK 6'] =  df_1['AIR_DLY_WT'].floordiv(10000).mul(0.925).round(0)
            
         df_1['MARK 4'] = [x if x <= 50 else 50 for x in df_1['AIR_FRT_GWT']]
        
         df_1['MARK 8'] = [x if x <= 50 else 50 for x in df_1['AIR_WT_GWT']]
            
         df_2 = df_0.merge(df_1, on = ['REGION_CODE'], how = 'left')

         sql_3 = '''SELECT 
                         a.REGION_CODE 
                        ,ROUND(SUM(NVL(b.OS_GT_90,0)),0) OS_ABOVE_90
                        ,ROUND(SUM(NVL(a.TBB_FREIGHT,0)),0) BUSINESS_AMT_TBB
                        ,ROUND(SUM(NVL(a.TBB_FREIGHT,0))/365,0) BUSINESS_PD
                        ,ROUND(NVL(SUM(NVL(b.OS_GT_90,0))/NULLIF((SUM(NVL(a.TBB_FREIGHT,0))/365),0),0),0) OS_TBB_PD
                    FROM 
                        (
                        SELECT 
                             xm.REGION_CODE 
                            ,SUM(NVL(ct.TBB_FRT,0)) TBB_FREIGHT
                        FROM 
                            CT_BUSINESS_GROWTH_NEW_IMPL ct
                        LEFT JOIN
                            XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE
                        WHERE 
                             LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(ct.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                            
                            AND ct.DIVISION_CODE IN ('21','22')
                            AND ct.REGION_CODE <> 'XCRP'
                            AND xm.SATTLITEBRANCH NOT IN ('C','H','R')
                        GROUP BY 
                             xm.REGION_CODE      
                        ) a
                        LEFT JOIN
                        (
                        SELECT 
                             xm.REGION_CODE 
                            ,SUM(NVL(ct.OS_91TO120_DAYS,0)) + SUM(NVL(ct.OS_121TO180_DAYS,0)) + SUM(NVL(ct.OS_181TO365_DAYS,0)) + SUM(NVL(ct.OS_ABOVE_365_DAYS,0)) OS_GT_90
                        FROM 
                            CT_AGEWISE_BILLED_OS ct
                        LEFT JOIN
                            XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE
                        WHERE 
                             ct.REPORT_TYPE = 'BILLWISE'
                             AND ct.DIVISION_CODE IN ('21','22')
                             AND TRUNC(BILL_DATE) <= TRUNC(SYSDATE)
                             AND TRUNC(AUD_DATE) = TRUNC(SYSDATE)
                             AND NOT EXISTS(
                                            SELECT 
                                                  'X'
                                            FROM 
                                                CT_AGEWISE_BILLED_OS ca
                                            WHERE
                                                ct.BRANCH_CODE = ca.BRANCH_CODE 
                                                AND ct.BILL_NO = ca.BILL_NO 
                                                AND ct.BILL_DATE = ca.BILL_DATE 
                                                AND ca.REALISE_FLAG = 'R'
                                                AND ca.UPTO_BCS_DATE <= TRUNC(SYSDATE)
                                           )
                        GROUP BY 
                             xm.REGION_CODE 
                        ) b
                    ON
                        a.REGION_CODE = b.REGION_CODE
                    GROUP BY 
                         a.REGION_CODE 
                    ORDER BY 
                        a.REGION_CODE ASC
                '''%{'year' : year,'month' : month}

         df_3 = pd.read_sql_query(sql_3, con)

         df_4 = df_2.merge(df_3, on = ['REGION_CODE'], how = 'left')

         def os_tbb_rank(row):

             if row == 0:
                return 50
             elif row >= 1 and row <= 10:
                return 40
             elif row >= 11 and row <= 20:
                 return 30
             elif row > 20 and row <= 30:
                 return 20
             elif row > 30 and row <= 40:
                 return 10
             else:
                 return 0

         df_4['MARK 9'] = df_4['OS_TBB_PD'].apply(os_tbb_rank)

         sql_5 = '''    SELECT
                            Q2.TCS_REGION REGION_CODE,
                            NVL(Q1.LY_COST,0) LY_PC_COST,
                            NVL(Q2.CY_COST,0) CY_PC_COST
                        FROM
                        (
                        SELECT 
                            X.REGION_CODE TCS_REGION,
                            ROUND(SUM(NVL(C.TOTALCOST,0))/NULLIF(SUM(NVL(C.ACTUAL_WT,0)),0),2) LY_COST
                        FROM 
                            CT_PICKDLY_COST C,
                            XM_BRANCHS X 
                        WHERE 
                            C.TCSBRANCH=X.BRANCH_CODE 
                            AND TO_DATE(TO_CHAR(TO_DATE(C.MONTH_YEAR,'MMYYYY'),'YYYYMM'),'YYYYMM')
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'MM') IN ('01','02','03')
                                      THEN TO_CHAR(TO_NUMBER(TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'YYYY'))-1)
                                         ELSE TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'YYYY') END
                                           AND ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12)
                            AND C.TCSTYPE NOT IN ('OD','DC')   
                            AND VEHTYPE!='TOT' 
                        GROUP BY
                            X.REGION_CODE
                        ) Q1
                        RIGHT JOIN
                        (
                        SELECT 
                            X.REGION_CODE TCS_REGION,
                            ROUND(SUM(NVL(C.TOTALCOST,0))/NULLIF(SUM(NVL(C.ACTUAL_WT,0)),0),2) CY_COST
                            
                        FROM 
                            CT_PICKDLY_COST C,
                            XM_BRANCHS X 
                        WHERE 
                            C.TCSBRANCH=X.BRANCH_CODE 
                            
                            AND TO_DATE(TO_CHAR(TO_DATE(C.MONTH_YEAR,'MMYYYY'),'YYYYMM'),'YYYYMM')
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                      THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                         ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                           AND TO_DATE('%(year)s%(month)s','YYYYMM')
                            AND C.TCSTYPE NOT IN ('OD','DC')   
                            AND VEHTYPE!='TOT' 
                        GROUP BY
                            X.REGION_CODE
                        ) Q2
                        ON
                        Q1.TCS_REGION = Q2.TCS_REGION
                        ORDER BY
                        Q2.TCS_REGION

                    '''%{'year':year,'month':month}
        
         df_5 = pd.read_sql_query(sql_5, con)

         df_6 = df_4.merge(df_5, on = 'REGION_CODE', how = 'left')

         df_6['AMT_SAVING_PC'] = df_6['LY_PC_COST'].sub(df_6['CY_PC_COST']).mul(df_0['SURFACE_BKG_WT'])

         def pickup_amt_saving(row):

             if row > 50:
                 return 50
             else:
                 return row

         df_6['MARK 10'] = df_6['AMT_SAVING_PC'].floordiv(100000).apply(pickup_amt_saving)

         sql_7 = ''' SELECT 
                            Q2.TCS_REGION REGION_CODE,
                            NVL(Q1.LY_COST, 0) LY_DY_COST,
                            NVL(Q2.CY_COST, 0) CY_DY_COST
                        FROM
                        (
                        SELECT 
                            X.REGION_CODE TCS_REGION,
                            
                            ROUND(SUM(NVL(C.TOTALCOST,0))/NULLIF(SUM(NVL(C.ACTUAL_WT,0)),0),2) LY_COST
                        FROM 
                            CT_PICKDLY_COST C,
                            XM_BRANCHS X 
                        WHERE 
                            C.TCSBRANCH=X.BRANCH_CODE 
                            AND TO_DATE(TO_CHAR(TO_DATE(C.MONTH_YEAR,'MMYYYY'),'YYYYMM'),'YYYYMM')
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'MM') IN ('01','02','03')
                                      THEN TO_CHAR(TO_NUMBER(TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'YYYY'))-1)
                                         ELSE TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'YYYY') END
                                           AND ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12)
                            AND C.TCSTYPE IN ('OD','DC')   
                            AND VEHTYPE!='TOT' 
                        GROUP BY
                            X.REGION_CODE
                           
                        ) Q1
                        RIGHT JOIN
                        (
                        SELECT 
                            X.REGION_CODE TCS_REGION,
                          
                            ROUND(SUM(NVL(C.TOTALCOST,0))/NULLIF(SUM(NVL(C.ACTUAL_WT,0)),0),2) CY_COST
                            
                        FROM 
                            CT_PICKDLY_COST C,
                            XM_BRANCHS X 
                        WHERE 
                            C.TCSBRANCH=X.BRANCH_CODE 
                            
                            AND TO_DATE(TO_CHAR(TO_DATE(C.MONTH_YEAR,'MMYYYY'),'YYYYMM'),'YYYYMM')
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                      THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                         ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                           AND TO_DATE('%(year)s%(month)s','YYYYMM')
                            AND C.TCSTYPE IN ('OD','DC')   
                            AND VEHTYPE!='TOT' 
                        GROUP BY
                            X.REGION_CODE
                         
                        ) Q2
                        ON
                        Q1.TCS_REGION = Q2.TCS_REGION
                     
                    '''%{'year':year,'month':month}
         
         df_7 = pd.read_sql_query(sql_7, con)

         df_8 = df_6.merge(df_7, on = ['REGION_CODE'], how = 'left')

         df_8['AMT_SAVING_DC'] = df_8['LY_DY_COST'].sub(df_8['CY_DY_COST']).mul(df_0['SURFACE_DLY_WT'])

         def delivery_cost_amt_saving(row):

             if row > 50:
                 return 50
             else:
                 return row

         df_8['MARK 11'] = df_8['AMT_SAVING_DC'].floordiv(100000).apply(delivery_cost_amt_saving)

         sql_9 = '''SELECT
                         xm.REGION_CODE
                        ,SUM(NVL(ct.TOT_FRT,0)) INTL_AIR_FRT
                        ,SUM(NVL(ct.LYA_TOT_FRT,0)) LY_INTL_AIR_FRT
                       
                    FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL ct
                    LEFT JOIN
                        XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE 
                    WHERE
                        LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(ct.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                
                        AND ct.DIVISION_CODE = '26'
                        AND ct.REGION_CODE <> 'XCRP'
         
                    GROUP BY
                        xm.REGION_CODE
                    
                    ORDER BY
                        xm.REGION_CODE ASC

          '''%{'year':year,'month':month}

         df_9 = pd.read_sql_query(sql_9, con)

         df_9['MARK 12'] = df_9['INTL_AIR_FRT'].floordiv(100000).mul(0.920).round(0)

         df_10 = df_8.merge(df_9, on = ['REGION_CODE'], how = 'left')

         sql_11 = '''SELECT
                             xm.REGION_CODE
                            ,SUM(NVL(ct.DLY_DWB,0)) DLYDWB        
                    FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL ct
                    LEFT JOIN
                        XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE 
                                        
                    WHERE
                        LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(ct.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                            ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                        
                        AND ct.REGION_CODE <> 'XCRP'
                    GROUP BY
                         xm.REGION_CODE
               
                    ORDER BY
                        xm.REGION_CODE ASC

                '''%{'year':year, 'month':month}

         df_11 = pd.read_sql_query(sql_11, con)

         df_11['MARK 13'] = df_11['DLYDWB'].floordiv(6470).round(0)

         df_12 = df_10.merge(df_11, on = ['REGION_CODE'], how = 'left')

         sql_13 = '''SELECT 
                            xm.REGION_CODE REGION_CODE, 
                      
                            SUM(NVL(cp.DWB_ARRIVED,0)) TOTAL_DLY, 
                            SUM(NVL(cp.DWB_DLVRD_SAME_DAY,0)) SAME_DAY_DLY, 
                            SUM(NVL(cp.DLVRD_NEXT_DAY,0)) NEXT_DAY_DLY
                     FROM 
                            CT_BA_DBA_DLY_PERFORMANCE cp
                     LEFT JOIN
                            XM_BRANCHS xm ON cp.DLY_BRANCH = xm.BRANCH_CODE
                     WHERE 
                            TO_DATE(TO_CHAR(TO_DATE(cp.MONTH_YEAR,'MMYYYY'),'YYYYMM'),'YYYYMM')
                                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                                                    ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                                                    AND TO_DATE('%(year)s%(month)s','YYYYMM')
                     GROUP BY
                           xm.REGION_CODE
                
                '''%{'year':year,'month':month}
         
         df_13 = pd.read_sql_query(sql_13, con)

         df_13['MARK 14'] = (((df_13['SAME_DAY_DLY'].add(df_13['NEXT_DAY_DLY'])).div(df_13['TOTAL_DLY'])).mul(100)).round(0)

         df_14 = df_12.merge(df_13, on = ['REGION_CODE'], how = 'left')

         sql_15 = '''SELECT 
                            xm.REGION_CODE REGION_CODE,
                            SUM(ct.CREDIT_NOTE_AMOUNT) CR_NOTE_AMT
                        FROM 
                            CT_CREDIT_NOTE ct
                        LEFT JOIN
                            XM_BRANCHS xm ON ct.BRANCH_CODE = xm.BRANCH_CODE
                        WHERE 
                            TO_DATE(TO_CHAR(ct.CREDIT_NOTE_DATE,'YYYYMM'),'YYYYMM') BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                                                                        THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                                                                            ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                                                                                AND TO_DATE('%(year)s%(month)s','YYYYMM')
                            AND APPROVAL_FLAG = 'Y'
                        GROUP BY 
                           xm.REGION_CODE
                     
                 '''%{'year' : year, 'month' : month}

         df_15 = pd.read_sql_query(sql_15, con)

         def cr_note_amt_rank(row):
             if row < -100:
                 return -100
             else:
                 return row

         df_15['MARK 15'] = df_15['CR_NOTE_AMT'].floordiv(-100000).apply(cr_note_amt_rank)

         df_15['MARK 15'] = df_15['MARK 15'].round(0)

         df_16 = df_14.merge(df_15, on = ['REGION_CODE'], how = 'left')

         sql_17 = ''' SELECT 
                             xm.REGION_CODE BKG_REGION_CODE
                            ,A.UNLOADING_CNS_BRANCH_BRANCH_CO BKG_BRANCH_CODE
                            ,A.UNLOADING_CNS_CNS_NO DWB_NO
                            ,xm1.REGION_CODE DLY_REGION_CODE
                            ,A.UNLOADING_BRANCH_BRANCH_CODE DLY_BRANCH_CODE
                            ,A.CLAIM_AMOUNT COFAMT 
                      FROM 
                             CT_COF A
                            ,CT_COF_CHK B
                            ,CT_DWB C
                            ,CM_GOODS_DETAIL D
                            ,xm_branchs xm
                            ,xm_branchs xm1 
                      WHERE 
                            A.UNLOADING_CNS_CNS_NO=B.CNS_NO 
                            AND A.UNLOADING_CNS_CNS_DATE=B.CNS_DATE 
                            AND UNLOADING_CNS_BRANCH_BRANCH_CO=B.CNS_BRANCH_CODE 
                            AND B.CNS_NO=C.DWB_NO 
                            AND B.CNS_DATE=C.DWB_BOOKING_DATE 
                            AND B.CNS_BRANCH_CODE=C.BRANCH_BRANCH_CODE 
                            AND A.UNLOADING_CNS_CNS_NO=C.DWB_NO 
                            AND A.UNLOADING_CNS_CNS_DATE=C.DWB_BOOKING_DATE 
                            AND A.UNLOADING_CNS_BRANCH_BRANCH_CO=C.BRANCH_BRANCH_CODE 
                            AND C.GOODS_DET_GOODS_CODE=D.GOODS_CODE 
                            AND A.UNLOADING_CNS_BRANCH_BRANCH_CO=xm.BRANCH_CODE 
                            AND A.UNLOADING_BRANCH_BRANCH_CODE=xm1.BRANCH_CODE 
                            AND TO_DATE(TO_CHAR(A.COF_DATE,'YYYYMM'),'YYYYMM')
                            BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                    ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                        AND TO_DATE('%(year)s%(month)s','YYYYMM') 
                            AND  xm.STATUS='VALID' 
                            AND  xm1.STATUS='VALID'   
                        
                '''%{'year' : year, 'month' : month}
            
         df_17 = pd.read_sql_query(sql_17, con)

         df_pvt_17 = pd.pivot_table(data = df_17, index = ['BKG_REGION_CODE'], values = ['DWB_NO','COFAMT'], aggfunc = {'DWB_NO':'count','COFAMT':'sum'}).reset_index()

         df_pvt_17 = df_pvt_17.rename(columns = {'BKG_REGION_CODE':'REGION_CODE','DWB_NO':'BKG_DWB_NO','COFAMT':'BKG_COF_AMT'})
         
         df_18 = df_16.merge(df_pvt_17, on = ['REGION_CODE'], how = 'left')

         df_pvt_17_A = pd.pivot_table(data = df_17, index = ['DLY_REGION_CODE'], values = ['DWB_NO','COFAMT'], aggfunc = {'DWB_NO':'count','COFAMT':'sum'}).reset_index()

         df_pvt_17_A = df_pvt_17_A.rename(columns = {'DLY_REGION_CODE':'REGION_CODE','DWB_NO':'DLY_DWB_NO','COFAMT':'DLY_COF_AMT'})

         df_19 = df_18.merge(df_pvt_17_A, on = ['REGION_CODE'], how = 'left')

         df_19['TOT_COF_AMT'] = df_19['BKG_COF_AMT'].add(df_19['DLY_COF_AMT'])

         def cof_amount_rank(row):

             if row < -100:
                 return -100
             else:
                 return row

         df_19['MARK 16'] = df_19['TOT_COF_AMT'].floordiv(-100000).apply(cof_amount_rank)

         sql_20 = '''SELECT 
                        REGION_CODE,
                        SUM(FREIGHT) FREIGHT,
                        SUM(PROFIT) PROFIT,
                        ROUND((SUM(PROFIT)/NULLIF(SUM(FREIGHT),0)) * 100,2) PROFIT_PER
                    FROM 
                        (
                    SELECT 
                        DWB_MONTH_YEAR,
                        REGION_CODE,
                        MAX(A.FRT) FREIGHT,
                        MAX(A.IND_EXP + A.OPR_EXP) TOTAL_EXPENSES,
                        (MAX(A.FRT) - (MAX(A.IND_EXP) + MAX(A.OPR_EXP))) PROFIT,
                        ROUND(((MAX(A.FRT) - (MAX(A.IND_EXP) + MAX(A.OPR_EXP)))/NULLIF(MAX(A.FRT),0)) * 100,2) 
                    FROM 
                    (
                    SELECT 
                        cd.DWB_MONTH_YEAR,
                        xm.REGION_CODE REGION_CODE,
                        cd.FREIGHT FRT,
                        cd.OPR_EXP + cd.PERSONAL_COST + cd.OS_INTEREST IND_EXP,
                        NVL(cd.PICKUP_COMM_BA,0) + NVL(cd.PICKUP_EXP,0) + NVL(cd.TOTAL_TRANSIT_EXP,0) + NVL(cd.DELIVERY_COMM_BA,0) + NVL(cd.DELIVERY_EXP,0) +  NVL(cd.MISC_DIR_EXP,0)  + NVL(cd.NON_CLN_DIR_EXP,0) +  NVL(cd.NON_CLN_DIR_EXP_EXTRA,0) OPR_EXP
                    FROM
                        CT_DOCKET_COSTING_MISC cd
                    LEFT JOIN
                        XM_BRANCHS xm ON cd.BRANCH_CODE = xm.BRANCH_CODE 
                    WHERE
                        TO_DATE(TO_CHAR(TO_DATE(cd.DWB_MONTH_YEAR,'MMYYYY'),'YYYYMM'),'YYYYMM') 
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                                            THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                                                ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                                                    AND TO_DATE('%(year)s%(month)s','YYYYMM')
                        AND DIVISION_CODE IN ('21','22')
                    ) A
                    GROUP BY
                    DWB_MONTH_YEAR,
                    REGION_CODE
              
                    ) B 
                    GROUP BY 
                     REGION_CODE
         

                '''%{'year':year, 'month': month}

         df_20 = pd.read_sql_query(sql_20, con_1)  

         df_20['MARK 17'] = df_20['PROFIT'].floordiv(1000000).floordiv(3.180).round(0)

         df_20['MARK 18'] = df_20['PROFIT_PER'].round(0)

         df_21 = df_19.merge(df_20, on = ['REGION_CODE'], how = 'left')

         df_21['TOTAL MARKS'] = df_21.loc[:,['MARK 1','MARK 2', 'MARK 3','MARK 4','MARK 5','MARK 6','MARK 7','MARK 8','MARK 9','MARK 10',\
                                             'MARK 11','MARK 12','MARK 13','MARK 14','MARK 15', 'MARK 16','MARK 17', 'MARK 18']].sum(axis = 1)

         df_marks = df_21[['REGION_CODE','MARK 1','MARK 2', 'MARK 3','MARK 4','MARK 5','MARK 6','MARK 7','MARK 8','MARK 9','MARK 10',\
                           'MARK 11','MARK 12','MARK 13','MARK 14','MARK 15', 'MARK 16','MARK 17', 'MARK 18', 'TOTAL MARKS']].copy()

         df_desp = pd.DataFrame({'Marks' : ['Marks 1','Marks 2','Marks 3','Marks 4','Marks 5','Marks 6','Marks 7','Marks 8',\
                                 'Marks 9','Marks 10','Marks 11','Marks 12','Marks 13','Marks 14','Marks 15','Marks 16',\
                                 'Marks 17','Marks 18'],

                                 'Description' : ['BOOKING AMOUNT-SURFACE','BOOKING AMOUNT-AIR','BOOKING GROWTH-SURFACE','BOOKING GROWTH-AIR',\
                                 'DELIVERY WEIGHT-SURFACE','DELIVERY WEIGHT-AIR', 'DELIVERY WT GROWTH-SURFACE','DELIVERY WT GROWTH-AIR',\
                                 'ABOVE 90 DAYS O/S-S+A','PICKUP COST SAVING-S+A','DELIVERY COST SAVING-S+A','Air Intl BOOKING-Air Intl',\
                                 'DLY DWB NO-Total','DLY PERFORMANCE SD+ND-S+A','BILL DEDUCTION-S+A','COF ON B+D-S+A','Profit Amount-S+A',\
                                 'Profit %-S+A' ]})

         
         def to_xlsx(bytes_io):

                writer = pd.ExcelWriter(bytes_io, engine='xlsxwriter') # pylint: disable=abstract-class-instantiated

                df_21.to_excel(writer, sheet_name = 'Region Rank Data', index = False)

                df_marks.to_excel(writer, sheet_name = 'Region Rank', index = False)

                df_desp.to_excel(writer, sheet_name = 'Rank Description', index = False)

                workbook = writer.book

                worksheet1 = writer.sheets['Region Rank Data']

                worksheet2 = writer.sheets['Region Rank']

                worksheet3 = writer.sheets['Rank Description']

                border = workbook.add_format({'border': 2})

                background_color_1 = workbook.add_format({'bg_color': '#99e600'})

                background_color_2 = workbook.add_format({'bg_color': '#ffff4d'})

                background_color_3 = workbook.add_format({'bg_color': '#0dc8f2'})

                format_align = workbook.add_format({'align': 'center'})

                worksheet1.conditional_format('A2:BG10',  { 'type' : 'no_errors' , 'format' : border} )

                worksheet2.conditional_format('A2:T10',  { 'type' : 'no_errors' , 'format' : border} )

                worksheet3.conditional_format('A1:B19',  { 'type' : 'no_errors' , 'format' : border} )

                worksheet1.conditional_format('A2:A10',  { 'type' : 'no_errors' , 'format' : background_color_1})

                worksheet2.conditional_format('A2:A10',  { 'type' : 'no_errors' , 'format' : background_color_1})

                worksheet3.conditional_format('A2:A19',  { 'type' : 'no_errors' , 'format' : background_color_1})

                worksheet1.conditional_format('B2:BG10',  { 'type' : 'no_errors' , 'format' : background_color_2})

                worksheet2.conditional_format('B2:T10',  { 'type' : 'no_errors' , 'format' : background_color_2})

                worksheet3.conditional_format('B2:B19',  { 'type' : 'no_errors' , 'format' : background_color_2})

                worksheet1.conditional_format('A1:BG1',  { 'type' : 'no_errors' , 'format' : background_color_3})

                worksheet2.conditional_format('A1:T1',  { 'type' : 'no_errors' , 'format' : background_color_3})

                worksheet3.conditional_format('A1:B1',  { 'type' : 'no_errors' , 'format' : background_color_3})

                worksheet1.hide_gridlines(option = 2)

                worksheet2.hide_gridlines(option = 2)

                worksheet3.hide_gridlines(option = 2)

                worksheet1.set_column('A:BG', 15.5, format_align)

                worksheet2.set_column('A:T', 15.5, format_align)

                worksheet3.set_column('A:A', 12)
                
                worksheet3.set_column('B:B', 30)

                worksheet2.write_comment('B1', 'BOOKING AMOUNT-SURFACE')

                worksheet2.write_comment('C1', 'BOOKING AMOUNT-AIR')

                worksheet2.write_comment('D1', 'BOOKING GROWTH-SURFACE')

                worksheet2.write_comment('E1', 'BOOKING GROWTH-AIR')

                worksheet2.write_comment('F1', 'DELIVERY WEIGHT-SURFACE' )

                worksheet2.write_comment('G1', 'DELIVERY WEIGHT-AIR')

                worksheet2.write_comment('H1', 'DELIVERY WT GROWTH-SURFACE')

                worksheet2.write_comment('I1', 'DELIVERY WT GROWTH-AIR')

                worksheet2.write_comment('J1', 'ABOVE 90 DAYS O/S-S+A')

                worksheet2.write_comment('K1', 'PICKUP COST SAVING-S+A')

                worksheet2.write_comment('L1', 'DELIVERY COST SAVING-S+A')

                worksheet2.write_comment('M1', 'Air Intl BOOKING-Air Intl')

                worksheet2.write_comment('N1', 'DLY DWB NO-Total')

                worksheet2.write_comment('O1', 'DLY PERFORMANCE SD+ND-S+A')

                worksheet2.write_comment('P1', 'BILL DEDUCTION-S+A')

                worksheet2.write_comment('Q1', 'COF ON B+D-S+A')

                worksheet2.write_comment('R1', 'Profit Amount-S+A')

                worksheet2.write_comment('S1', 'Profit %-S+A')

                worksheet3.write_comment('B2', '1 point = 50 Lac per Year')

                worksheet3.write_comment('B3', '1 Point = 6 Lac Per Year')

                worksheet3.write_comment('B4', 'Growth %')

                worksheet3.write_comment('B5', 'Growth %')

                worksheet3.write_comment('B6', '1 Point = 700000 Kg per year')

                worksheet3.write_comment('B7', '1 Point = 10000 Kg per year')

                worksheet3.write_comment('B8', 'Growth %')

                worksheet3.write_comment('B9', 'Growth %')

                worksheet3.write_comment('B10', '0 -> 50, 1 TO 10 -> 40, 11 TO 20 -> 30, 20 TO 30 -> 20, 30 TO 40 -> 10')

                worksheet3.write_comment('B11', '1 Point = Rs 100000.00')

                worksheet3.write_comment('B12', '1 Point = Rs 100000.00')

                worksheet3.write_comment('B13', '1 Point = Rs 100000.00')

                worksheet3.write_comment('B14', '1 Point = 5071 DWB')

                worksheet3.write_comment('B15', '% of Delivery Performance Same Day+ Next Day')

                worksheet3.write_comment('B16', 'Rs 100000 = -1 Point')

                worksheet3.write_comment('B17', 'Rs 100000 = -1 Point')

                worksheet3.write_comment('B18', '10 Lac =1 Point')

                worksheet3.write_comment('B19', '% of Profit %')

                writer.save()

         return send_bytes(to_xlsx, "download_region.xlsx")




         

