''' Importing Python Libraries '''

from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash

import xlsxwriter
import cx_Oracle as cx
import pandas as pd
import numpy as np

import urllib
import io
import flask
import base64
import config


app = dash.Dash(__name__, requests_pathname_prefix='/app3/', external_stylesheets = [dbc.themes.BOOTSTRAP])

row = html.Div([
                   dbc.Row([
                             dbc.Col([
                                       html.H6('Year',style = {'font-weight':'bold','textAlign':'center','text-indent':'80%'}),
                                       dcc.Dropdown(
                                                    id = 'year',
                                                    options = [{'label': y, 'value': y} for y in ['2018','2019','2020','2021']],
                                                    style = {'width':'50%', 'margin-left':'50%'}
                                                    )
                                     ]),
                             dbc.Col([
                                       html.H6('Month',style = {'font-weight':'bold','textAlign':'center','text-indent':'-80%'}),
                                       dcc.Dropdown(
                                                    id = 'month',
                                                    options = [{'label' : x, 'value' : x} for x in [ '01','02','03',\
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
                                      html.Button(
                                                 'Submit',
                                                  id = 'submit_button',
                                                  type = 'submit',
                                                  n_clicks = 0
                                                 )
                                     ], style = {'margin-left':'42%', 'display': 'inline-block', 'border-radius': '12px'}),
                             dbc.Col([
                                       dcc.Loading(html.A( 
                                               html.Button("Download"), 
                                               id='download',
                                               download="data.xlsx",
                                               href="",
                                               target="_blank",
                                                         )
                                                  )
                                     ], style = {'margin-right':'42%', 'display': 'inline-block','border-radius': '12px'})
                            ])
            ])
                   

app.layout = html.Div([
                   html.Br(),
                   html.Br(),
                   html.Br(),
                   html.Br(),
                   html.Br(),
                   html.Br(),
                   html.Br(),
                   html.Br(),
                   html.Div([
                             dbc.Container(children=[row])
                            ]),
                   html.Br(),
                   html.Br(),
                   html.Br(),
                   html.Br(),
                   html.Br(),
                   html.Br(),
                   html.Br(),
                   html.Br(),
                     ])


@app.callback(Output('download','href'),[Input("submit_button", "n_clicks")],[State('year','value'),\
                                                                              State('month','value')
                                                                             ])
def update_value(n_clicks, year, month):
    if n_clicks is not None and n_clicks > 0:

        con = cx.connect(config.CONN_STR)

        '''
           Creating an Index Page 
        '''
        
        df0 = pd.DataFrame({'Index':['-> Total Business','-> RegionWise Up to the Month',\
                                '-> RegionWise for the month','-> Booking Compariosn ProductWise',\
                                '-> AIR International','-> Pharmaceutical','-> Operations','-> ECOM',\
                                '-> Marketing','-> AIR','-> BA','-> VO','-> VO Deduction','-> HUB Wise Weight Loss',\
                                '-> COF Details','-> Diesel Prices','-> Incidents']})  

        '''
           Creating Total Business Page
        '''
        
        sql1 = '''SELECT
                        'XCRP' AS REGION
                        ,to_char(to_date(YEAR_MONTH_DAY,'YYYYMMDD'),'MM-YYYY') MONTHS
                        ,ROUND(SUM(NVL(TOT_FRT,0))/100000,2) CYF
                FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL
                WHERE
                   LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM'))
                        BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                    ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                        AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                GROUP BY
                        YEAR_MONTH_DAY
                ORDER BY
                        to_date(MONTHS,'MM-YYYY')
                
              '''%{'year': year, 'month': month}
    
        df1 = pd.read_sql_query(sql1, con)
        df1 = pd.pivot_table(df1, index = 'REGION', columns = 'MONTHS', values = 'CYF', aggfunc = np.sum)

        '''
          Creating Regionwise up to the month page
        '''

        sql2 = '''SELECT
                         to_char(to_date(YEAR_MONTH_DAY,'YYYYMMDD'),'MM-YYYY') MONTHS
                        ,REGION_CODE REGION
                        ,ROUND(SUM(NVL(TOT_FRT,0))/100000,2) CYF
                  FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL
                  WHERE
                   LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM'))
                        BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                    ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                        AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                            AND REGION_CODE <> 'XCRP'
                GROUP BY
                        YEAR_MONTH_DAY, REGION_CODE
                ORDER BY
                        to_date(MONTHS,'MM-YYYY')
                
               '''%{'year': year, 'month': month}
    
        df2 = pd.read_sql_query(sql2, con)
        df2 = pd.pivot_table(df2, index = 'REGION', columns = 'MONTHS', values = 'CYF', aggfunc = np.sum, margins = True, margins_name = 'Total').fillna(0)

        '''
          Creating Regionwise for the month
        '''
        
        sql3 = ''' SELECT
                         REGION_CODE REGION
                        ,ROUND(SUM(NVL(TOT_FRT,0))/100000,2) "Current Month"
                FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL
                WHERE
                   LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) = last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                    AND REGION_CODE <> 'XCRP'
                GROUP BY
                       REGION_CODE
               '''%{'year': year, 'month': month}
    
        df3 = pd.read_sql_query(sql3, con).sort_values(by = 'REGION', ascending = True)
        df3.loc[len(df3)] = df3.sum(numeric_only=True, axis = 0)
        df3.iloc[:,0].iat[-1] = 'XCRP Total'

        sql4 = '''SELECT 
                      NVL(CTE_1.CYR, 'XCRP TOTAL') REGION
                     ,NVL(decode(CTE_1.DIVISION,'21','Surface','22','AIR','23','ECOM','24','RAIL','25','GTA','26','INTL','27','C2C','28','COLDCHAIN'),'TOTAL') DIVISION
                     ,ROUND(NVL(SUM(CTE_2.LY_TOT_FRT)/100000,0),2) FRT
                     ,ROUND(NVL(SUM(CTE_2.LY_TOT_WT)/1000,0),2)  WT
                     ,NVL(SUM(CTE_2.LY_TOT_DWB),0) DWB
                     ,ROUND(NVL(SUM(CTE_1.CY_TOT_FRT)/100000,0),2) FRT
                     ,ROUND(NVL(SUM(CTE_1.CY_TOT_WT)/1000,0),2)  WT
                     ,NVL(SUM(CTE_1.CY_TOT_DWB),0) DWB
                     ,ROUND(NVL((SUM(CTE_1.CY_TOT_FRT) - SUM(CTE_2.LY_TOT_FRT))/SUM(CTE_2.LY_TOT_FRT) * 100,0),2) FRT
                     ,ROUND(NVL((SUM(CTE_1.CY_TOT_WT) - SUM(CTE_2.LY_TOT_WT))/SUM(CTE_2.LY_TOT_WT) * 100,0),2)  WT
                     ,ROUND(NVL((SUM(CTE_1.CY_TOT_DWB) - SUM(CTE_2.LY_TOT_DWB))/SUM(CTE_2.LY_TOT_DWB) * 100,0),2) DWB
                  FROM
                     (
                       SELECT 
                               xm.REGION_CODE CYR
                              ,ct.DIVISION_CODE DIVISION
                              ,ROUND(SUM(NVL(ct.TOT_FREIGHT,0))-SUM(NVL(ct.SER_TAX,0)+ NVL(ct.CESS_TAX,0)+NVL(ct.SB_TAX,0)+NVL(ct.KK_CESS,0)+NVL(ct.CGST,0)+NVL(ct.SGST,0)+NVL(ct.IGST,0)),0) as CY_TOT_FRT 
                              ,SUM(NVL(CHARGED_WEIGHT,0)) CY_TOT_WT
                              ,COUNT(DWB_NO) CY_TOT_DWB
                       FROM 
                              CT_DWB ct 
                          LEFT JOIN 
                              XM_BRANCHS xm ON ct.BRANCH_BRANCH_CODE = xm.BRANCH_CODE 
                          WHERE 
                              TO_DATE(TO_CHAR(ct.DWBS_DATE, 'YYYYMM'),'YYYYMM') 
                              BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                  ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                    AND TO_DATE('%(year)s%(month)s','YYYYMM')
                                       AND URO_BASIS IS NULL
                          GROUP BY 
                               xm.REGION_CODE, ct.DIVISION_CODE
                   ) CTE_1
                LEFT JOIN
                   ( SELECT 
                                xm.REGION_CODE LYR
                               ,ct.DIVISION_CODE DIVISION
                               ,ROUND(SUM(NVL(ct.TOT_FREIGHT,0))-SUM(NVL(ct.SER_TAX,0)+ NVL(ct.CESS_TAX,0)+NVL(ct.SB_TAX,0)+NVL(ct.KK_CESS,0)+NVL(ct.CGST,0)+NVL(ct.SGST,0)+NVL(ct.IGST,0)),0) as LY_TOT_FRT 
                               ,SUM(NVL(CHARGED_WEIGHT,0)) LY_TOT_WT
                               ,COUNT(DWB_NO) LY_TOT_DWB
                           FROM 
                               CT_DWB ct 
                           LEFT JOIN 
                               XM_BRANCHS xm ON ct.BRANCH_BRANCH_CODE = xm.BRANCH_CODE 
                           
                           WHERE 
                               TO_DATE(TO_CHAR(ct.DWBS_DATE, 'YYYYMM'),'YYYYMM') 
                                 BETWEEN '01-APR-'||CASE WHEN TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'MM') IN ('01','02','03')
                                   THEN TO_CHAR(TO_NUMBER(TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'YYYY'))-1)
                                     ELSE TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'YYYY') END
                                       AND ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12)
                                         AND URO_BASIS IS NULL
                           GROUP BY 
                               xm.REGION_CODE, ct.DIVISION_CODE
                   ) CTE_2
              ON 
                   CTE_1.CYR = CTE_2.LYR
                   AND CTE_1.DIVISION = CTE_2.DIVISION
              WHERE
                   CTE_2.DIVISION IS NULL
                   OR CTE_2.DIVISION IN ('21','22','23','24','25','26','27','28')
              GROUP BY
                   ROLLUP (CTE_1.CYR,CTE_1.DIVISION)
              ORDER BY
                    CTE_1.CYR
                   ,CTE_1.DIVISION
         '''%{'year': year, 'month': month}
    
        df4 = pd.read_sql_query(sql4, con)

        sql5 = ''' With CTE1 AS (
                              SELECT
                                  NVL(REGION_CODE,'TOTAL') REGION
                                 ,ROUND(SUM(NVL(LYA_TOT_FRT,0))/100000,2) LYFRT
                                 ,ROUND(SUM(NVL(LYA_TOT_WT,0))/1000,2) LYWT
                                 ,SUM(NVL(LYA_NO_DWB ,0)) LYDWB
                                 ,ROUND(SUM(NVL(TOT_FRT,0))/100000,2) CYFRT
                                 ,ROUND(SUM(NVL(TOT_WT,0))/1000,2) CYWT
                                 ,SUM(NVL(NO_DWB ,0)) CYDWB
                                 ,ROUND(((SUM(NVL(TOT_FRT,0)) - SUM(NVL(LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(LYA_TOT_FRT,0)),0) * 100),2) FRTGW
                                 ,ROUND(((SUM(NVL(TOT_WT,0)) - SUM(NVL(LYA_TOT_WT,0)))/NULLIF(SUM(NVL(LYA_TOT_WT,0)),0) * 100),2) WTGW
                                 ,ROUND(((SUM(NVL(NO_DWB,0)) - SUM(NVL(LYA_NO_DWB,0)))/NULLIF(SUM(NVL(NO_DWB,0)),0) * 100),2) DWBGW
                             FROM
                                 CT_BUSINESS_GROWTH_NEW_IMPL
                             WHERE
                                 DIVISION_CODE = '26'
                                 AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) = LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                 AND REGION_CODE <> 'XCRP'
                             GROUP BY
                                 ROLLUP(REGION_CODE)
                             ),
                      CTE2 AS (
                               SELECT
                                  NVL(REGION_CODE,'TOTAL') REGION
                                 ,ROUND(SUM(NVL(LYA_TOT_FRT,0))/100000,2) LYFRT
                                 ,ROUND(SUM(NVL(LYA_TOT_WT,0))/1000,2) LYWT
                                 ,SUM(NVL(LYA_NO_DWB ,0)) LYDWB
                                 ,ROUND(SUM(NVL(TOT_FRT,0))/100000,2) CYFRT
                                 ,ROUND(SUM(NVL(TOT_WT,0))/1000,2) CYWT
                                 ,SUM(NVL(NO_DWB ,0)) CYDWB
                                 ,ROUND(((SUM(NVL(TOT_FRT,0)) - SUM(NVL(LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(LYA_TOT_FRT,0)),0) * 100),2) FRTGW
                                 ,ROUND(((SUM(NVL(TOT_WT,0)) - SUM(NVL(LYA_TOT_WT,0)))/NULLIF(SUM(NVL(LYA_TOT_WT,0)),0) * 100),2) WTGW
                                 ,ROUND(((SUM(NVL(NO_DWB,0)) - SUM(NVL(LYA_NO_DWB,0)))/NULLIF(SUM(NVL(NO_DWB,0)),0) * 100),2) DWBGW
                              FROM
                                 CT_BUSINESS_GROWTH_NEW_IMPL
                              WHERE
                                 DIVISION_CODE = '26'
                                 AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM'))
                                       BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                         THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                           ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                             AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                              AND REGION_CODE <> 'XCRP'
                              GROUP BY
                                ROLLUP(REGION_CODE)
                            )
                     SELECT
                           CTE1.REGION "REGION"
                          ,CTE1.LYFRT "Freight"
                          ,CTE1.LYWT "Weight"
                          ,CTE1.LYDWB "DWB"
                          ,CTE1.CYFRT "Freight"
                          ,CTE1.CYWT "Weight"
                          ,CTE1.CYDWB "DWB"
                          ,CTE1.FRTGW "Freight"
                          ,CTE1.WTGW "Weight"
                          ,CTE1.DWBGW "DWB"
                          ,CTE2.LYFRT "Freight"
                          ,CTE2.LYWT "Weight"
                          ,CTE2.LYDWB "DWB"
                          ,CTE2.CYFRT "Freight"
                          ,CTE2.CYWT "Weight"
                          ,CTE2.CYDWB "DWB"
                          ,CTE2.FRTGW "Freight"
                          ,CTE2.WTGW "Weight"
                          ,CTE2.DWBGW "DWB"
                     FROM
                         CTE1
                        ,CTE2
                     WHERE
                         CTE1.REGION = CTE2.REGION
                         
            '''%{'year': year, 'month': month}

        df5 = pd.read_sql_query(sql5, con)

        sql5A = '''
             SELECT 
                 NVL(CTE2.REGION_CY, 'TOTAL') REGION,
                 SUM(NVL(CTE1.DWB_NO_LY,0)) DWB_NO_LY_FTM,
                 ROUND(SUM(NVL(CTE1.WT_LY,0))/1000,2) WT_LY_FTM,
                 ROUND(SUM(NVL(CTE1.FREIGHT_LY,0))/100000,2) FREIGHT_LY_FTM,
                 ROUND((SUM(NVL(CTE1.FREIGHT_LY,0))/NULLIF(SUM(NVL(CTE1.WT_LY,0)),0)),2) YEILD_LY_FTM,
                 SUM(NVL(CTE2.DWB_NO_CY,0)) DWB_NO_CY_FTM,
                 ROUND(SUM(NVL(CTE2.WT_CY,0))/1000,2) WT_CY_FTM,
                 ROUND(SUM(NVL(CTE2.FREIGHT_CY,0))/100000,2) FREIGHT_CY_FTM,
                 ROUND((SUM(NVL(CTE2.FREIGHT_CY,0))/ NULLIF(SUM(NVL(CTE2.WT_CY,0)),0)),2) YEILD_CY_FTM,
                 SUM(NVL(CTE3.DWB_NO_LY,0)) DWB_NO_LY_CUM,
                 ROUND(SUM(NVL(CTE3.WT_LY,0))/1000,2) WT_LY_CUM,
                 ROUND(SUM(NVL(CTE3.FREIGHT_LY,0))/100000,2) FREIGHT_LY_CUM,
                 ROUND((SUM(NVL(CTE3.FREIGHT_LY,0))/NULLIF(SUM(NVL(CTE3.WT_LY,0)),0)),2) YEILD_LY_CUM,
                 SUM(NVL(CTE4.DWB_NO_CY,0)) DWB_NO_CY_CUM,
                 ROUND(SUM(NVL(CTE4.WT_CY,0))/1000,2) WT_CY_CUM,
                 ROUND(SUM(NVL(CTE4.FREIGHT_CY,0))/100000,2) FREIGHT_CY_CUM,
                 ROUND((SUM(NVL(CTE4.FREIGHT_CY,0))/NULLIF(SUM(NVL(CTE4.WT_CY,0)),0)),2) YEILD_CY_CUM
             FROM  
                (
                 SELECT 
                      A.REGION_CODE REGION_LY,
                      count(A.DWB_NO) DWB_NO_LY,
                      Sum(A.CHARGED_WEIGHT) WT_LY,
                      ROUND(sum(NVL(A.tot_freight,0))-sum(NVL(A.ser_tax,0) + NVL(A.CESS_TAX,0) + NVL(A.SB_TAX,0) +
                      NVL(A.KK_CESS,0)+Nvl(A.CGST,0)+Nvl(A.SGST,0)+Nvl(A.IGST,0)),0) FREIGHT_LY
                 FROM 
                     CT_DWB A
                 LEFT JOIN
                     CM_CUST C ON A.BRANCH_BRANCH_CODE=C.BRANCH_BRANCH_CODE AND A.CUSTOMER_CUST_CODE=C.CUST_CODE
                 LEFT JOIN
                     CM_VERTICAL B ON C.BUSINESS_NATURE=B.CODE
                 WHERE  
                     to_char(A.DWBS_DATE,'YYYYMM') = to_char(add_months(to_date('%(year)s%(month)s','YYYYMM'),-12),'YYYYMM')
                     AND B.CODE = '120'
                 GROUP BY 
                     A.REGION_CODE
       
                  ) CTE1
              RIGHT JOIN
                  (
                   SELECT 
                       A1.REGION_CODE REGION_CY,
                       count(A1.DWB_NO) DWB_NO_CY,
                       Sum(A1.CHARGED_WEIGHT) WT_CY,
                       ROUND(sum(NVL(A1.tot_freight,0))-sum(NVL(A1.ser_tax,0) + NVL(A1.CESS_TAX,0) + NVL(A1.SB_TAX,0) +
                       NVL(A1.KK_CESS,0)+Nvl(A1.CGST,0)+Nvl(A1.SGST,0)+Nvl(A1.IGST,0)),0) FREIGHT_CY
                   FROM 
                       CT_DWB A1
                   LEFT JOIN
                       CM_CUST C1 ON A1.BRANCH_BRANCH_CODE = C1.BRANCH_BRANCH_CODE AND A1.CUSTOMER_CUST_CODE=C1.CUST_CODE
                   LEFT JOIN
                       CM_VERTICAL B1 ON C1.BUSINESS_NATURE = B1.CODE
                   WHERE  
                       to_char(A1.DWBS_DATE,'YYYYMM') = to_char(to_date('%(year)s%(month)s','YYYYMM'),'YYYYMM')
                       AND B1.CODE = '120'
                   GROUP BY 
                       A1.REGION_CODE
                   ) CTE2
                 ON
                   CTE1.REGION_LY = CTE2.REGION_CY
                 LEFT JOIN
                  (
                   SELECT 
                        A2.REGION_CODE REGION_LY,
                        count(A2.DWB_NO) DWB_NO_LY,
                        Sum(A2.CHARGED_WEIGHT) WT_LY,
                        ROUND(sum(NVL(A2.tot_freight,0))-sum(NVL(A2.ser_tax,0) + NVL(A2.CESS_TAX,0) + NVL(A2.SB_TAX,0) +
                        NVL(A2.KK_CESS,0)+Nvl(A2.CGST,0)+Nvl(A2.SGST,0)+Nvl(A2.IGST,0)),0) FREIGHT_LY
                   FROM 
                       CT_DWB A2
                   LEFT JOIN
                       CM_CUST C2 ON A2.BRANCH_BRANCH_CODE=C2.BRANCH_BRANCH_CODE AND A2.CUSTOMER_CUST_CODE=C2.CUST_CODE
                   LEFT JOIN
                       CM_VERTICAL B2 ON C2.BUSINESS_NATURE=B2.CODE
                   WHERE     
                        to_date(to_char(A2.DWBS_DATE,'YYYYMM'),'YYYYMM') 
                                 BETWEEN '01-APR-'||CASE WHEN TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'MM') IN ('01','02','03')
                                   THEN TO_CHAR(TO_NUMBER(TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'YYYY'))-1)
                                     ELSE TO_CHAR(ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12),'YYYY') END
                                       AND ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12)
                       AND B2.CODE = '120'
                    GROUP BY 
                       A2.REGION_CODE
                    ) CTE3

                  ON 
                    CTE2.REGION_CY = CTE3.REGION_LY
                  LEFT JOIN
                    (
                     SELECT 
                         A3.REGION_CODE REGION_CY,
                         count(A3.DWB_NO) DWB_NO_CY,
                         Sum(A3.CHARGED_WEIGHT) WT_CY,
                         ROUND(sum(NVL(A3.tot_freight,0))-sum(NVL(A3.ser_tax,0) + NVL(A3.CESS_TAX,0) + NVL(A3.SB_TAX,0) +
                         NVL(A3.KK_CESS,0)+Nvl(A3.CGST,0)+Nvl(A3.SGST,0)+Nvl(A3.IGST,0)),0) FREIGHT_CY
                     FROM 
                         CT_DWB A3
                     LEFT JOIN
                         CM_CUST C3 ON A3.BRANCH_BRANCH_CODE=C3.BRANCH_BRANCH_CODE AND A3.CUSTOMER_CUST_CODE=C3.CUST_CODE
                     LEFT JOIN
                         CM_VERTICAL B3 ON C3.BUSINESS_NATURE=B3.CODE
                     WHERE
                         to_date(to_char(A3.DWBS_DATE,'YYYYMM'),'YYYYMM') 
                                 BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                   THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                     ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                       AND TO_DATE('%(year)s%(month)s','YYYYMM')
                         AND B3.CODE = '120'
                     GROUP BY 
                         A3.REGION_CODE
                   ) CTE4
                   ON
                     CTE2.REGION_CY = CTE4.REGION_CY 
                   GROUP BY 
                     ROLLUP (CTE2.REGION_CY)
    
            '''%{'year':year,'month':month}
    
        df5A = pd.read_sql_query(sql5A, con)
    
        df5A['DWB_NO_GROWTH%_FTM'] = (((df5A['DWB_NO_CY_FTM'] - df5A['DWB_NO_LY_FTM'])/df5A['DWB_NO_LY_FTM']) * 100).replace(np.inf, 0)
    
        df5A['WT_GROWTH%_FTM'] = (((df5A['WT_CY_FTM'] - df5A['WT_LY_FTM'])/df5A['WT_LY_FTM']) * 100).replace(np.inf, 0) 
    
        df5A['FREIGHT_GROWTH%_FTM'] = (((df5A['FREIGHT_CY_FTM'] - df5A['FREIGHT_LY_FTM'])/df5A['FREIGHT_LY_FTM']) * 100).replace(np.inf,0)
    
        df5A['YEILD_GROWTH%_FTM'] = (((df5A['YEILD_CY_FTM'] - df5A['YEILD_LY_FTM'])/df5A['YEILD_LY_FTM']) * 100).replace(np.inf,0)
    
        df5A['DWB_NO_GROWTH%_CUM'] = (((df5A['DWB_NO_CY_CUM'] - df5A['DWB_NO_LY_CUM'])/df5A['DWB_NO_LY_CUM']) * 100).replace(np.inf, 0)
    
        df5A['WT_GROWTH%_CUM'] = (((df5A['WT_CY_CUM'] - df5A['WT_LY_CUM'])/df5A['WT_LY_CUM']) * 100).replace(np.inf, 0)
    
        df5A['FREIGHT_GROWTH%_CUM'] = (((df5A['FREIGHT_CY_CUM'] - df5A['FREIGHT_LY_CUM'])/df5A['FREIGHT_LY_CUM']) * 100).replace(np.inf, 0)
    
        df5A['YEILD_GROWTH%_CUM'] = (((df5A['YEILD_CY_CUM'] - df5A['YEILD_LY_CUM'])/df5A['YEILD_LY_CUM']) * 100).replace(np.inf, 0)


        sql6 = '''
                  SELECT 
                       to_char(to_date(REPDATE,'MMYYYY'),'MM-YYYY') "MONTH"
                      ,FRT "Business Amount (In Rs.)"
                      ,WT "Booking Charge Weight (In Kg.)"
                      ,YEILD_PKG "YPK"
                      ,PICKCOST_KG "C2B Cost/Kg"
                      ,B2H_COSTKG "B2H Cost/Kg"
                      ,H2H_COSTKG "H2H Cost/Kg"
                      ,H2B_COSTKG "H2B Cost/Kg"
                      ,B2B_COSTKG "B2B Cost/Kg"
                      ,B2C_COSTPER_KG "B2C Cost/Kg"
                      ,INDIRECT_COSTKG "Indirect Cost/Kg"
                      ,H2H_WTLOSS "H2H weight Loss Pct"
                      ,H2H_ONTIMEDEPATURE "H2H Pct of on time Depature"
                      ,H2B_ONTIMEDEPATURE "H2B Pct of on time Depature"
                      ,B2H_ONTIMEDEPATURE "B2H Pct of on time Depature"
                      ,B2H_ONTIMEARR "B2H Pct of On Time Arrival"
                      ,H2H_ONTIMEARR "H2H Pct of On Time Arrival"
                      ,H2B_ONTIMEARR "H2B Pct of On Time Arrival"
                      ,PER_SAMEDAY "DlyPerformance SameDay"
                      ,PER_NEXTDAY "DlyPerformance NextDay"
                      ,SERLBLB2B_PER "Surface Service Level(B2B)"
                      ,SERLBLC2C_PER "Surface Service Level(C2C)"
                      ,PER_COF "Pct of COF Amt on Booking Amt"
                      ,H2H_MOWT "H2H Pct of MO weight"
                      ,H2H_MOVEH "H2H Pct of MO Vehicle"
                      ,H2H_MOHIRE "H2H Pct of MO Hire"
                      ,H2B_MOVEH "H2B Pct of MO Vehicle"
                      ,H2B_MOHIRE "H2B Pct of MO Hire"
                      ,B2H_MOVEH "B2H Pct of MO Vehicle"
                      ,B2H_MOHIRE "B2H Pct of MO Hire"
                      ,TOT_MOVEH "Total Pct of MO Vehicle"
                      ,TOT_MOHIRE "Total Pct of MO Hire"
                      ,DLY_WT "Delivery Weight"
                      ,B2H_MO_WT_LOSS "B2H Weight Loss"
                      ,H2B_MO_WT_LOSS "H2B Weight Loss"
                      ,MO_NOOFTCS_PC "No Of MO Veh In PC"
                      ,MO_VEH_HIRE_PC "Pct Of MO Veh Hire In Pickup"
                      ,MO_NOOFTCS_DC "No Of MO Veh In DC & OD"
                      ,MO_VEH_HIRE_DC "Pct Of MO Veh Hire In DC & OD"
                  FROM 
                      MIS_Summary 
                  WHERE
                      to_date(to_char(to_date(REPDATE,'MMYYYY'),'YYYYMM'),'YYYYMM')
                        BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03') 
                          THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1) 
                            ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END 
                              AND TO_DATE('%(year)s%(month)s','YYYYMM') 
                                AND REGION = 'ALL' AND CONT = 'ALL' AND BRN = 'ALL'  
                  ORDER BY
                       REPDATE  
                       
              '''%{'year': year, 'month': month}
    
        df6 = pd.read_sql_query(sql6, con)

        df6 = df6.rename(columns = { 'H2H weight Loss Pct' : 'H2H weight Loss %',
                                     'H2H Pct of on time Depature' : 'H2H % of on time Depature',
                                     'H2B Pct of on time Depature' : 'H2B % of on time Depature',
                                     'B2H Pct of on time Depature' :  'B2H % of on time Depature',
                                     'B2H Pct of On Time Arrival'  : 'B2H % of On Time Arrival',
                                     'H2H Pct of On Time Arrival'  :  'H2H % of On Time Arrival',
                                     'H2B Pct of On Time Arrival'  : 'H2B % of On Time Arrival',
                                     'Pct of COF Amt on Booking Amt' : '% of COF Amt on Booking Amt',
                                     'H2H Pct of MO weight' : 'H2H % of MO weight',
                                     'H2H Pct of MO Vehicle' : 'H2H % of MO Vehicle',
                                     'H2H Pct of MO Hire' : 'H2H % of MO Hire',
                                     'H2B Pct of MO Vehicle' : 'H2B % of MO Vehicle',
                                     'H2B Pct of MO Hire' : 'H2B % of MO Hire',
                                     'B2H Pct of MO Vehicle' : 'B2H % of MO Vehicle',
                                     'B2H Pct of MO Hire' : 'B2H % of MO Hire',
                                     'Total Pct of MO Vehicle' : 'Total % of MO Vehicle',
                                     'Total Pct of MO Hire' : 'Total % of MO Hire',
                                     'Pct Of MO Veh Hire In Pickup' : '% Of MO Veh Hire In Pickup',
                                     'Pct Of MO Veh Hire In DC & OD': '% Of MO Veh Hire In DC & OD'
                       })

        df6 = df6.T


        sql7 = '''
              SELECT
                   to_char(to_date(YEAR_MONTH, 'YYYYMM'),'MM-YYYY') AS "MONTH"
                  ,BUSINESS_AMOUNT_IN_LAKH AS "BUSINESS AMOUNT IN LAKH"
                  ,BKG_CHARGED_WT AS "BKG CHARGED WT"
                  ,NO_OF_DWB AS "NO OF DWB"
                  ,YIELD_PER_KG AS "YIELD PER KG"
                  ,YIELD_PER_DWB AS "YIELD PER DWB"
                  ,WITHIN_CITY_BUSINESS AS "WITHIN CITY BUSINESS"
                  ,WITHIN_CITY_PER_TOTAL_BUSINESS AS "WITHIN CITY PER TOTAL BUSINESS"
                  ,WITHIN_CITY_NO_OF_DWB AS "WITHIN CITY NO OF DWB"
                  ,WITHIN_CITY_DWB_PER_OF_TOT_DWB AS "WITHIN CITY DWB PER OF TOT DWB"
                  ,WITHIN_CITY_YIELD_PER_DWB AS "WITHIN CITY YIELD PER DWB"
                  ,WITHIN_STATE_BUSINESS AS "WITHIN STATE BUSINESS"
                  ,WITHIN_STATE_PER_TOT_BUSINESS AS "WITHIN STATE PER TOT BUSINESS"
                  ,WITHIN_STATE_NO_OF_DWB AS "WITHIN STATE NO OF DWB"
                  ,WITHIN_STATE_DWB_PER_TOT_DWB AS "WITHIN STATE DWB PER TOT DWB"
                  ,WITHIN_STATE_YIELD_PER_DWB AS "WITHIN STATE YIELD PER DWB"
                  ,REST_OF_INDIA_BUSINESS AS "REST OF INDIA BUSINESS"
                  ,REST_OF_INDIA_PER_TOT_BUSINESS AS "REST OF INDIA PER TOT BUSINESS"
                  ,REST_OF_INDIA_NO_OF_DWB AS "REST OF INDIA NO OF DWB"
                  ,REST_OF_INDIA_DWB_PER_TOT_DWB AS "REST OF INDIA DWB PER TOT DWB"
                  ,REST_OF_INDIA_YIELD_PER_DWB AS "REST OF INDIA YIELD PER DWB"
                  ,SPECIAL_ZONE_BUSINESS "SPECIAL ZONE BUSINESS"
                  ,SPECIAL_ZONE_PER_TOT_BUSINESS AS "SPECIAL ZONE PER TOT BUSINESS"
                  ,SPECIAL_ZONE_NO_OF_DWB AS "SPECIAL ZONE NO OF DWB"
                  ,SPECIAL_ZONE_DWB_PER_TOT_DWB AS "SPECIAL ZONE DWB PER TOT DWB"
                  ,SPECIAL_ZONE_YIELD_PER_DWB AS "SPECIAL ZONE YIELD PER DWB"
                  ,C2B_COSTING_PER_DWB AS "C2B COSTING PER DWB"
                  ,B2H_COSTING_PER_DWB AS "B2H COSTING PER DWB"
                  ,H2H_COSTING_PER_DWB AS "H2H COSTING PER DWB"
                  ,H2B_COSTING_PER_DWB AS "H2B COSTING PER DWB"
                  ,B2C_COSTING_PER_DWB AS "B2C COSTING PER DWB"
                  ,OVER_ALL_COST_PER_DWB AS "OVER ALL COST PER DWB"
                  ,BA_DBA_COST_PER_SHIPMENT AS "BA DBA COST PER SHIPMENT"
                  ,SPDA_COST_PER_SHIPMENT AS "SPDA COST PER SHIPMENT"
                  ,OVERALL_DLY_COST_PER_SHIPMENT AS "OVERALL DLY COST PER SHIPMENT"
                  ,SERVICE_LEVEL_PER_B2B AS "SERVICE LEVEL PER B2B"
                  ,SERVICE_LEVEL_PER_C2C AS "SERVICE LEVEL PER C2C"
                  ,DLY_ATTEMPTED_SAME_DAY_ARR_PER AS "DLY ATTEMPTED SAME DAY ARR PER"
                  ,DLY_PERF_CONSOLIDATED_PER "DLY PERF CONSOLIDATED PER"
                  ,RTO_PER AS "RTO PER"
                  ,PENDANCY_IN_NUMBERS AS "PENDANCY IN NUMBERS"
                  ,TOTAL_OPENING_OF_OUTSTANDING AS "TOTAL OPENING OF OUTSTANDING"
                  ,TOTAL_ADD_BILLS AS "TOTAL ADD BILLS"
                  ,TOTAL_REALIZATION_OF_MONTH AS "TOTAL REALIZATION OF MONTH"
                  ,TOTAL_DEDUCTION AS "TOTAL DEDUCTION"
                  ,BALANCE_OUTSTANDING AS "BALANCE OUTSTANDING"
                  ,OVERALL_DIRECT_COST_IN_LAKHS AS "OVERALL DIRECT COST IN LAKHS"
                  ,INDIRECT_COST_IN_LAKHS AS "INDIRECT COST IN LAKHS"
                  ,REVENUE_LEAKAGE_IN_LAKHS AS "REVENUE LEAKAGE IN LAKHS"
                  ,PROFIT_LOSS AS "PROFIT LOSS"
                  ,PROFIT_LOSS_PER AS "PROFIT LOSS PER"
                  ,SHIPMENT_DELIVERED_OVERALL AS "SHIPMENT DELIVERED OVERALL"
                  ,SHIPMENT_DELIVERED_BA_DBA_PERC AS "SHIPMENT DELIVERED BA DBA PERC"
                  ,SHIPMENT_DELIVEDRED_SPDA_PERC AS "SHIPMENT DELIVEDRED SPDA PERC"
          FROM
              CT_MIS_ECOM
          WHERE
              to_date(YEAR_MONTH,'YYYYMM')
                    BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03') 
                      THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1) 
                        ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END 
                          AND TO_DATE('%(year)s%(month)s','YYYYMM') 
          ORDER BY
              TO_DATE(MONTH,'MM-YYYY')

           
           '''%{'year': year, 'month': month}
    
        df7 = pd.read_sql_query(sql7, con)
        df7 = df7.transpose()
        

        sql8 = ''' WITH CTE_1 AS
                                 (
                                 SELECT
                                      NVL(x.REGION_CODE,'ALL INDIA') REGION
                                     ,SUM(NVL(x.LYA_TOT_FRT,0)) LYFRT
                                     ,SUM(NVL(x.LYA_NO_DWB,0)) LYDWB
                                     ,SUM(NVL(x.TOT_FRT,0)) FRT
                                     ,SUM(NVL(x.NO_DWB,0)) DWB
                                     ,ROUND((SUM(NVL(x.TOT_FRT,0)) - SUM(NVL(x.LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(x.LYA_TOT_FRT,0)),0) * 100,2) FRTGW
                                     ,ROUND((SUM(NVL(x.NO_DWB,0)) - SUM(NVL(x.LYA_NO_DWB,0)))/NULLIF(SUM(NVL(x.LYA_NO_DWB,0)),0) * 100,2) DWBGW
                                 FROM
                                     CT_BUSINESS_GROWTH_NEW_IMPL x
                                 WHERE
                                     x.REGION_CODE <> 'XCRP'
                                     AND x.DIVISION_CODE = '21'
                                     AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(x.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) = LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                              
                                 GROUP BY
                                    ROLLUP(x.REGION_CODE) 
                                 ),
                       CTE_2 AS 
                                 (
                                  SELECT
                                       NVL(x.REGION_CODE,'ALL INDIA') REGION
                                     ,SUM(NVL(x.LYA_TOT_FRT,0)) LYFRT
                                     ,SUM(NVL(x.LYA_NO_DWB,0)) LYDWB
                                     ,SUM(NVL(x.TOT_FRT,0)) FRT
                                     ,SUM(NVL(x.NO_DWB,0)) DWB
                                     ,ROUND((SUM(NVL(x.TOT_FRT,0)) - SUM(NVL(x.LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(x.LYA_TOT_FRT,0)),0) * 100,2) FRTGW
                                     ,ROUND((SUM(NVL(x.NO_DWB,0)) - SUM(NVL(x.LYA_NO_DWB,0)))/NULLIF(SUM(NVL(x.LYA_NO_DWB,0)),0) * 100,2) DWBGW
                                 FROM
                                     CT_BUSINESS_GROWTH_NEW_IMPL x
                                 WHERE
                                     x.REGION_CODE <> 'XCRP'
                                     AND x.DIVISION_CODE = '22'
                                     AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(x.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) = LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                 GROUP BY
                                    ROLLUP(x.REGION_CODE) 
                                 ),
                       CTE_3 AS
                                 (
                                 SELECT
                                      NVL(x.REGION_CODE,'ALL INDIA') REGION
                                     ,SUM(NVL(x.LYA_TOT_FRT,0)) LYFRT
                                     ,SUM(NVL(x.LYA_NO_DWB,0)) LYDWB
                                     ,SUM(NVL(x.TOT_FRT,0)) FRT
                                     ,SUM(NVL(x.NO_DWB,0)) DWB
                                     ,ROUND((SUM(NVL(x.TOT_FRT,0)) - SUM(NVL(x.LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(x.LYA_TOT_FRT,0)),0) * 100,2) FRTGW
                                     ,ROUND((SUM(NVL(x.NO_DWB,0)) - SUM(NVL(x.LYA_NO_DWB,0)))/NULLIF(SUM(NVL(x.LYA_NO_DWB,0)),0) * 100,2) DWBGW
                                 FROM
                                     CT_BUSINESS_GROWTH_NEW_IMPL x
                                 WHERE
                                     x.REGION_CODE <> 'XCRP'
                                     AND x.DIVISION_CODE = '21'
                                     AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(x.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                              BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                                    THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                                        ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                            AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                 GROUP BY
                                    ROLLUP(x.REGION_CODE) 
                                 ),
                        CTE_4 AS 
                                 (
                                  SELECT
                                      NVL(x.REGION_CODE,'ALL INDIA') REGION
                                     ,SUM(NVL(x.LYA_TOT_FRT,0)) LYFRT
                                     ,SUM(NVL(x.LYA_NO_DWB,0)) LYDWB
                                     ,SUM(NVL(x.TOT_FRT,0)) FRT
                                     ,SUM(NVL(x.NO_DWB,0)) DWB
                                     ,ROUND((SUM(NVL(x.TOT_FRT,0)) - SUM(NVL(x.LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(x.LYA_TOT_FRT,0)),0) * 100,2) FRTGW
                                     ,ROUND((SUM(NVL(x.NO_DWB,0)) - SUM(NVL(x.LYA_NO_DWB,0)))/NULLIF(SUM(NVL(x.LYA_NO_DWB,0)),0) * 100,2) DWBGW
                                 FROM
                                     CT_BUSINESS_GROWTH_NEW_IMPL x
                                 WHERE
                                     x.REGION_CODE <> 'XCRP'
                                     AND x.DIVISION_CODE = '22'
                                     AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(x.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                              BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                                    THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                                        ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                            AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                 GROUP BY
                                    ROLLUP(x.REGION_CODE) 
                                 ),
                                 
                        CTE_5 AS
                                 (
                                 SELECT
                                      NVL(x.REGION_CODE,'ALL INDIA') REGION
                                     ,SUM(NVL(x.LYA_TOT_FRT,0)) LYFRT
                                     ,SUM(NVL(x.LYA_NO_DWB,0)) LYDWB
                                     ,SUM(NVL(x.TOT_FRT,0)) FRT
                                     ,SUM(NVL(x.NO_DWB,0)) DWB
                                     ,ROUND((SUM(NVL(x.TOT_FRT,0)) - SUM(NVL(x.LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(x.LYA_TOT_FRT,0)),0) * 100,2) FRTGW
                                     ,ROUND((SUM(NVL(x.NO_DWB,0)) - SUM(NVL(x.LYA_NO_DWB,0)))/NULLIF(SUM(NVL(x.LYA_NO_DWB,0)),0) * 100,2) DWBGW
                                 FROM
                                     CT_BUSINESS_GROWTH_NEW_IMPL x
                                 WHERE
                                     x.REGION_CODE <> 'XCRP'
                                     AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(x.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                              BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                                    THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                                        ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                            AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                 GROUP BY
                                    ROLLUP(x.REGION_CODE) 
                                 ),
                        CTE_6 AS 
                                 (
                                  SELECT
                                      NVL(x.REGION_CODE,'ALL INDIA') REGION
                                     ,SUM(NVL(x.LYA_TOT_FRT,0)) LYFRT
                                     ,SUM(NVL(x.LYA_NO_DWB,0)) LYDWB
                                     ,SUM(NVL(x.TOT_FRT,0)) FRT
                                     ,SUM(NVL(x.NO_DWB,0)) DWB
                                     ,ROUND((SUM(NVL(x.TOT_FRT,0)) - SUM(NVL(x.LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(x.LYA_TOT_FRT,0)),0) * 100,2) FRTGW
                                     ,ROUND((SUM(NVL(x.NO_DWB,0)) - SUM(NVL(x.LYA_NO_DWB,0)))/NULLIF(SUM(NVL(x.LYA_NO_DWB,0)),0) * 100,2) DWBGW
                                 FROM
                                     CT_BUSINESS_GROWTH_NEW_IMPL x
                                 WHERE
                                     x.REGION_CODE <> 'XCRP'
                                     AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(x.YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                              BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                                    THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                                        ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                                            AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                                 GROUP BY
                                    ROLLUP(x.REGION_CODE) 
                                 )
                            
                            
                        SELECT
                             CTE_1.REGION 
                            ,CTE_1.LYDWB "DWB"
                            ,CTE_1.DWB "DWB"
                            ,CTE_1.DWBGW "GROWTH PERCENTAGE"
                            ,ROUND(CTE_1.LYFRT/100000,2) "FREIGHT"
                            ,ROUND(CTE_1.FRT/100000,2) "FREIGHT"
                            ,CTE_1.FRTGW "GROWTH PERCENTAGE"
                            ,CTE_2.LYDWB "DWB"
                            ,CTE_2.DWB "DWB"
                            ,CTE_2.DWBGW "GROWTH PERCENTAGE"
                            ,ROUND(CTE_2.LYFRT/100000,2) "FREIGHT"
                            ,ROUND(CTE_2.FRT/100000,2) "FREIGHT"
                            ,CTE_2.FRTGW "GROWTH PERCENTAGE"
                            ,CTE_5.LYDWB "DWB"
                            ,CTE_5.DWB "DWB"
                            ,CTE_5.DWBGW "GROWTH PERCENTAGE"
                            ,ROUND(CTE_5.LYFRT/100000,2) "FREIGHT"
                            ,ROUND(CTE_5.FRT/100000,2) "FREIGHT"
                            ,CTE_5.FRTGW "GROWTH PERCENTAGE"
                            ,CTE_3.LYDWB "DWB"
                            ,CTE_3.DWB "DWB"
                            ,CTE_3.DWBGW "GROWTH PERCENTAGE"
                            ,ROUND(CTE_3.LYFRT/100000,2) "FREIGHT"
                            ,ROUND(CTE_3.FRT/100000,2) "FREIGHT"
                            ,CTE_3.FRTGW "GROWTH PERCENTAGE"
                            ,CTE_4.LYDWB "DWB"
                            ,CTE_4.DWB "DWB"
                            ,CTE_4.DWBGW "GROWTH PERCENTAGE"
                            ,ROUND(CTE_4.LYFRT/100000,2) "FREIGHT"
                            ,ROUND(CTE_4.FRT/100000,2) "FREIGHT"
                            ,CTE_4.FRTGW "GROWTH PERCENTAGE"
                            ,CTE_6.LYDWB "DWB"
                            ,CTE_6.DWB "DWB"
                            ,CTE_6.DWBGW "GROWTH PERCENTAGE"
                            ,ROUND(CTE_6.LYFRT/100000,2) "FREIGHT"
                            ,ROUND(CTE_6.FRT/100000,2) "FREIGHT"
                            ,CTE_6.FRTGW "GROWTH PERCENTAGE"
                        FROM
                             CTE_1
                            ,CTE_2
                            ,CTE_3
                            ,CTE_4
                            ,CTE_5
                            ,CTE_6
                        WHERE
                            CTE_1.REGION = CTE_2.REGION
                            AND CTE_2.REGION = CTE_3.REGION
                            AND CTE_3.REGION = CTE_4.REGION
                            AND CTE_4.REGION = CTE_5.REGION
                            AND CTE_5.REGION = CTE_6.REGION
                        
                
           '''%{'year': year, 'month': month}
    
        df8 = pd.read_sql_query(sql8, con)

        sql8A = '''
                  SELECT
                  to_char(to_date(A.MONTH_1,'MM'),'MM') "MONTH",
                  ROUND(A.FRT/100000,2) "Business Amount",
                  ROUND(A.WT/1000,0) "Booking Charge Weight",
                  A.DWB "No of DWB",
                  C.YPK "YPK Without ODA & Misc Charges",
                  ROUND(B.STT1FRT/100000,2) "STT 1 Business Amt",
                  ROUND((B.STT1FRT/A.FRT)*100, 2) "STT 1 pct of TOT_BUSINESS",
                  ROUND(B.STT1WT/1000,2) "STT 1 Weight in Ton",
                  B.STT1DWB "STT 1 No of DWB",
                  B.STT1Yield "STT 1 Yield",
                  ROUND(B.STT2FRT/100000,2) "STT 2 Business Amt",
                  ROUND((B.STT2FRT/A.FRT)*100, 2) "STT 2 pct of TOT_BUSINESS",
                  ROUND(B.STT2WT/1000,2) "STT 2 Weight in Ton",
                  B.STT2DWB "STT 2 No of DWB",
                  B.STT2Yield "STT 2 Yield",
                  ROUND(B.STT345FRT/100000,2) "STT > 2 Business Amt",
                  ROUND((B.STT345FRT/A.FRT)*100, 2) "STT > 2 pct of TOT_BUSINESS",
                  ROUND(B.STT345WT/1000,2) "STT > 2 Weight in Ton",
                  B.STT345DWB "STT > 2 No of DWB",
                  B.STT345Yield "STT > 2 Yield"
             FROM
                 (
                  SELECT 
                       TO_CHAR(TO_DATE(YEAR_MONTH_DAY,'YYYYMMDD'),'MM') MONTH_1,
                       SUM(TOT_FRT) FRT,
                       SUM(TOT_WT) WT,
                       SUM(NO_DWB) DWB
                  FROM 
                       CT_BUSINESS_GROWTH_NEW_IMPL 
                  WHERE 
                       LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM'))
                                       BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                         THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                           ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                             AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                       AND DIVISION_CODE = 22
                  GROUP BY 
                       TO_CHAR(TO_DATE(YEAR_MONTH_DAY,'YYYYMMDD'),'MM')
                  ) A,
                  (
                   SELECT 
                       TO_CHAR(TO_DATE(YEAR_MONTH_DAY,'YYYYMMDD'),'MM') MONTH_2,
                       SUM(STT1_FRT) STT1FRT, 
                       SUM(STT1_WT) STT1WT, 
                       SUM(STT1_DWB) STT1DWB,
                       ROUND(SUM(STT1_FRT)/SUM(STT1_WT),2) STT1Yield, 
                       SUM(STT2_FRT) STT2FRT, 
                       SUM(STT2_WT) STT2WT, 
                       SUM(STT2_DWB) STT2DWB,
                       ROUND(SUM(STT2_FRT)/NULLIF(SUM(STT2_WT),0),2) STT2Yield,
                       SUM(STT3_FRT) + SUM(STT4_FRT) + SUM(STT5_FRT) STT345FRT,
                       SUM(STT3_WT) + SUM(STT4_WT) + SUM(STT5_WT) STT345WT,
                       SUM(STT3_DWB) + SUM(STT4_DWB) + SUM(STT5_DWB) STT345DWB,
                       ROUND(SUM(STT3_FRT + STT4_FRT + STT5_FRT) / NULLIF(SUM(STT3_WT + STT4_WT + STT5_WT),0),2) STT345Yield
                  FROM 
                       CT_BUSINESS_GROWTH_NEW_PART 
                  WHERE 
                       LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM'))
                                       BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                         THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                           ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                             AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                       AND DIVISION_CODE = 22 
                  GROUP BY 
                       TO_CHAR(TO_DATE(YEAR_MONTH_DAY,'YYYYMMDD'),'MM')
                  ) B,
                  (
                   SELECT
                        to_char(DWB_BOOKING_DATE, 'MM') MONTH_3,
                        ROUND((SUM(TOT_FREIGHT) - SUM(SER_TAX) - SUM(CESS_TAX) - SUM(SB_TAX) - SUM(KK_CESS) - SUM(SGST) - SUM(CGST) - SUM(IGST) -SUM(MISCELLANEOUS) - SUM(DIPLOMAT_CHARGES))/SUM(CHARGED_WEIGHT),0) YPK
                   FROM
                        CT_DWB
                   WHERE
                        to_date(to_char(DWBS_DATE,'YYYYMM'),'YYYYMM') 
                                 BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                   THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                     ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                       AND TO_DATE('%(year)s%(month)s','YYYYMM')
                        AND FREIGHT IS NOT NULL
                        AND URO_BASIS IS NULL
                        AND division_code='22'
                   GROUP BY
                        to_char(DWB_BOOKING_DATE, 'MM')
                   ) C
              WHERE
                  A.MONTH_1 = B.MONTH_2
                  AND B.MONTH_2 = C.MONTH_3
              ORDER BY 
                  A.MONTH_1 ASC
                  
             '''%{'year':year,'month':month}

        df8A = pd.read_sql_query(sql8A, con)
    
        df8A = df8A.transpose()
    
        df8A.columns = df8A.iloc[0]
    
        df8A = df8A.drop(df8A.index[0])

        sql9 = '''
                   SELECT 
                        to_char(VOU.VDATE, 'MM-YYYY') MONTHS,
                        XM.REGION_CODE,
                        VOU.ACC_CNTR,
                        VOU.BRANCH,
                        VOU.BA_CODE,
                        SR.cust_CODE,
                        SR.PAN_NO,
                        SR.cust_NAME,
                        Sum(Nvl(VOU.RECEIPTS,0)) BA_COMMISSION
                   FROM 
                       BA_VOUCHER VOU,
                       XM_BRANCHS XM,
                       CM_CUST SR
                   WHERE 
                      VOU.BRANCH=XM.BRANCH_CODE 
                      AND XM.STATUS='VALID' 
                      AND VOU.COST_CODE=SR.CUST_CODE 
                      AND VOU.BRANCH=SR.BRANCH_BRANCH_CODE
                      AND TO_DATE(TO_CHAR(VOU.VDATE,'YYYYMM'),'YYYYMM') BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                     THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                       ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                         AND TO_DATE('%(year)s%(month)s','YYYYMM')                              
                      AND  VOU.RECEIPTS > 0 
                      AND SR.STATUS='VL'
                   GROUP BY
                       to_char(VOU.VDATE, 'MM-YYYY'),
                       XM.REGION_CODE,
                       VOU.ACC_CNTR,
                       VOU.BRANCH,
                       VOU.BA_CODE,
                       SR.cust_CODE,
                       SR.PAN_NO,
                       SR.cust_NAME
                   ORDER BY
                      to_date(MONTHS,'MM-YYYY')
                 
              '''%{'year':year, 'month':month}

        df9 = pd.read_sql_query(sql9, con)

        df9 = pd.pivot_table(data = df9, index = ['REGION_CODE','ACC_CNTR'],\
                        columns = 'MONTHS', values = 'PAN_NO', aggfunc = 'count', fill_value = 0)
    
        df9 = pd.concat([d.append(d.sum().rename((k,'Total'))) for k,d in df9.groupby(level=0)]).\
              append(df9.sum().rename(('Grand','Total')))

        sql9A = '''SELECT
                    TO_CHAR(TO_DATE(B.MONTHS,'MON'),'MM') MONTH,
                    D.REGION_CODE REGION,
                    D.AC_CENTER_CODE AC_CODE,
                    D.BRANCH_BRANCH_CODE branch,
                    D.VENDOR_CODE VO_CODE,
                    C.SUPP_NAME VO_NAME,
                    C.PAN_NO VO_PAN,
                    C.VEHICLE VO_VEHICLE,
                    Sum(Nvl(A.LIB_AMOUNT,0))PENDING,
                    Sum(Nvl(B.NET_PAYMENT,0)) PAID,
                    Sum(Nvl(B.MISC_DEDU_AMOUNT,0)) DEDUCTION_TO_EARLY_PAYMENT,
                    Sum(Nvl(B.GPS_AMOUNT, 0)) GPS_AMOUNT,
                    Sum(Nvl(B.DEDUCTION_FROM_REG,0)) DEDUCTION_FROM_REGION,
                    Sum(T.DEDUCTION_AMT) DEDUCTION_AMT,
                    Sum(T.PENALTY_AMT) PENALTY_AMT
                FROM
                   (SELECT
                        REGION_CODE,
                        AC_CENTER_CODE,
                        BRANCH_BRANCH_CODE,
                        VENDOR_CODE,
                        Sum(Nvl(LIB_AMOUNT,0))LIB_AMOUNT
                    FROM
                        ct_vms
                    WHERE  
                        Trunc(LIB_DATE)>=Trunc(SYSDATE-365)
                        AND TO_DATE(TO_CHAR(LIB_DATE,'YYYYMM'),'YYYYMM') BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                                                    THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                                                      ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                                                         AND TO_DATE('%(year)s%(month)s','YYYYMM')
                        AND NET_PAYMENT IS NULL  
                    GROUP BY REGION_CODE,AC_CENTER_CODE,BRANCH_BRANCH_CODE,VENDOR_CODE
                )A,
                (
                 SELECT
                      DISTINCT REGION_CODE,
                      TO_CHAR(PAYMENT_DATE,'MON') MONTHS,
                      AC_CENTER_CODE,
                      BRANCH_BRANCH_CODE,
                      VENDOR_CODE,
                      Sum(Nvl(NET_PAYMENT,0)) NET_PAYMENT,
                      Sum(Nvl(MISC_DEDU_AMOUNT, 0)) MISC_DEDU_AMOUNT,
                      Sum(Nvl(DEDUCTION,0)) DEDUCTION_FROM_REG,
                      Sum(Nvl(GPS_AMOUNT, 0)) GPS_AMOUNT,
                      Sum(Nvl(CGST,0)) CGST,
                      Sum(Nvl(SGST,0)) SGST,
                      Sum(Nvl(IGST,0)) IGST,
                      Sum(Nvl(TDS_AMOUNT,0)) TDS_AMOUNT
                 FROM
                      ct_vms
                 WHERE 
                      TO_DATE(TO_CHAR(PAYMENT_DATE,'YYYYMM'),'YYYYMM') BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                                                    THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                                                      ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                                                         AND TO_DATE('%(year)s%(month)s','YYYYMM')
                      AND NET_PAYMENT IS NOT NULL
                 GROUP BY REGION_CODE,AC_CENTER_CODE,BRANCH_BRANCH_CODE,VENDOR_CODE,  TO_CHAR(PAYMENT_DATE,'MON')
                )B,
                (
                 SELECT
                      DISTINCT vm.REGION_CODE,
                      VM.AC_CENTER_CODE,
                      vm.BRANCH_BRANCH_CODE,
                      TYPE.SUPPLIER_CODE,
                      SR.PAN_NO,
                      SR.SUPP_NAME,
                      Count(DISTINCT FL.REGIS_NO) VEHICLE
                 FROM
                      ct_vms vm ,ct_fleet fl,ct_srm SR,ct_srm_SERVICE_TYPE TYPE  
                 WHERE
                      vm.VENDOR_CODE=fl.VNDR_CODE
                      AND vm.BRANCH_BRANCH_CODE=FL.BRANCH_BRANCH_CODE
                      AND FL.VNDR_CODE=TYPE.SUPPLIER_CODE
                      AND TYPE.STATUS='VL'
                      AND SR.PAN_NO=TYPE.PAN_NO
                      AND SR.BRANCH_CODE=TYPE.BRANCH_CODE  
                      AND FL.VEHICLE_TYPE='VO'
                      AND Trunc(VM.LIB_DATE)>=Trunc(SYSDATE-365)
                      AND TO_DATE(TO_CHAR(LIB_DATE,'YYYYMM'),'YYYYMM') BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                                                    THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                                                      ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                                                         AND TO_DATE('%(year)s%(month)s','YYYYMM')
                      AND TYPE.SERVICE_CODE='70007'
                      AND FL.CKH is null  
                GROUP BY vm.REGION_CODE,VM.AC_CENTER_CODE,vm.BRANCH_BRANCH_CODE,TYPE.SUPPLIER_CODE,SR.PAN_NO,SR.SUPP_NAMe
                )C,
                (
                 SELECT
                     DISTINCT X.REGION_CODE,
                     X.ACCOUNTITNG_CODE AC_CENTER_CODE,
                     X.BRANCH_CODE BRANCH_BRANCH_CODE,
                     VENDOR_CODE
                 FROM
                     ct_vms V, XM_BRANCHS X
                 WHERE
                     V.BRANCH_BRANCH_CODE=X.BRANCH_CODE
                ) D,
                (
                 SELECT
                     LORRY_BRANCH_BRANCH_CODE,
                     VENDOR_CODE,
                     TO_CHAR(TCS_END_DATE,'MON') MONTHS,
                     Sum(Nvl(HANDLING_EXP_IN,0)) HANDLING_EXP,
                     Sum(Nvl(HANDLING_EXP_OUT,0)) DRIVER_EXP,
                     Sum(Nvl(ENROUTE_EXP,0)) ENROUTE_EXP,
                     Sum(Nvl(DIESEL_EXPENSES,0)) DIESEL_EXP,
                     Sum(Nvl(HIRE_RATE,0)) LORRY_HIRE,
                     Sum(Nvl(NET_PAYMENT,0)) LIB_AMT,
                     Sum(Nvl(INCENTIVE,0)),
                     Sum(Nvl(DEDUCTION,0)) DEDUCTION_AMT,
                     Sum(Nvl(TDS,0)) TDS,
                     Sum(Nvl(PENALTY,0)) PENALTY_AMT,
                     Sum(Nvl(MISC_DED,0)) STATIONARY_DED,
                     Sum(Nvl(TOLL_EXP,0)) TOLL_EXP
                 FROM
                     CT_TCS
                 WHERE
                    VEHICLE_TYPE='VO'
                    AND TO_DATE(TO_CHAR(TCS_END_DATE,'YYYYMM'),'YYYYMM') BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                                                    THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                                                      ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                                                         AND TO_DATE('%(year)s%(month)s','YYYYMM')
                 GROUP BY LORRY_BRANCH_BRANCH_CODE, VENDOR_CODE, TO_CHAR(TCS_END_DATE,'MON')
               ) T  
               WHERE  
                   B.BRANCH_BRANCH_CODE=T.LORRY_BRANCH_BRANCH_CODE
                   AND B.VENDOR_CODE=T.VENDOR_CODE
                   AND B.MONTHS = T.MONTHS
                   AND D.REGION_CODE=A.REGION_CODE(+)
                   AND D.REGION_CODE=B.REGION_CODE(+)  
                   AND D.REGION_CODE=C.REGION_CODE(+)
                   AND D.BRANCH_BRANCH_CODE=A.BRANCH_BRANCH_CODE(+)  
                   AND D.BRANCH_BRANCH_CODE=B.BRANCH_BRANCH_CODE(+)  
                   AND D.BRANCH_BRANCH_CODE=C.BRANCH_BRANCH_CODE(+)
                   AND D.AC_CENTER_CODE=A.AC_CENTER_CODE(+)  
                   AND D.AC_CENTER_CODE=B.AC_CENTER_CODE(+)
                   AND D.AC_CENTER_CODE=C.AC_CENTER_CODE(+)
                   AND D.VENDOR_CODE=A.VENDOR_CODE(+)  
                   AND D.VENDOR_CODE=B.VENDOR_CODE(+)
                   AND D.VENDOR_CODE=C.SUPPLIER_CODE(+)
                   AND (A.LIB_AMOUNT>0 OR B.NET_PAYMENT>0)
               GROUP BY D.REGION_CODE ,D.AC_CENTER_CODE ,D.BRANCH_BRANCH_CODE ,D.VENDOR_CODE,C.SUPP_NAME ,C.PAN_NO,C.VEHICLE, T.LORRY_BRANCH_BRANCH_CODE, T.VENDOR_CODE, B.MONTHS
               ORDER BY B.MONTHS, REGION,AC_CODE,BRANCH,VO_CODE
                  
                '''%{'year':year, 'month': month}

        df9A = pd.read_sql_query(sql9A, con)

        df9A = pd.pivot_table(data = df9A, index = ['REGION','AC_CODE'],\
                              columns = 'MONTH', values = 'VO_PAN',\
                              aggfunc = 'count', fill_value = 0)
    
        df9A = pd.concat([d.append(d.sum().rename((k,'Total'))) for k,d in df9A.groupby(level=0)]).\
                         append(df9A.sum().rename(('Grand','Total'))).reset_index()

        sql9B = '''SELECT
                    TO_CHAR(TO_DATE(B.MONTHS,'MON'),'MM') MONTH,
                    D.REGION_CODE REGION,
                    D.AC_CENTER_CODE AC_CODE,
                    D.BRANCH_BRANCH_CODE branch,
                    D.VENDOR_CODE VO_CODE,
                    C.SUPP_NAME VO_NAME,
                    C.PAN_NO VO_PAN,
                    C.VEHICLE VO_VEHICLE,
                    Sum(Nvl(A.LIB_AMOUNT,0))PENDING,
                    Sum(Nvl(B.NET_PAYMENT,0)) PAID,
                    Sum(Nvl(B.MISC_DEDU_AMOUNT,0)) DEDUCTION_TO_EARLY_PAYMENT,
                    Sum(Nvl(B.GPS_AMOUNT, 0)) GPS_AMOUNT,
                    Sum(Nvl(B.DEDUCTION_FROM_REG,0)) DEDUCTION_FROM_REGION,
                    Sum(T.DEDUCTION_AMT) DEDUCTION_AMT,
                    Sum(T.PENALTY_AMT) PENALTY_AMT
                FROM
                   (SELECT
                        REGION_CODE,
                        AC_CENTER_CODE,
                        BRANCH_BRANCH_CODE,
                        VENDOR_CODE,
                        Sum(Nvl(LIB_AMOUNT,0))LIB_AMOUNT
                    FROM
                        ct_vms
                    WHERE  
                        Trunc(LIB_DATE)>=Trunc(SYSDATE-365)
                        AND TO_DATE(TO_CHAR(LIB_DATE,'YYYYMM'),'YYYYMM') BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                                                    THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                                                      ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                                                         AND TO_DATE('%(year)s%(month)s','YYYYMM')
                        AND NET_PAYMENT IS NULL  
                    GROUP BY REGION_CODE,AC_CENTER_CODE,BRANCH_BRANCH_CODE,VENDOR_CODE
                )A,
                (
                 SELECT
                      DISTINCT REGION_CODE,
                      TO_CHAR(PAYMENT_DATE,'MON') MONTHS,
                      AC_CENTER_CODE,
                      BRANCH_BRANCH_CODE,
                      VENDOR_CODE,
                      Sum(Nvl(NET_PAYMENT,0)) NET_PAYMENT,
                      Sum(Nvl(MISC_DEDU_AMOUNT, 0)) MISC_DEDU_AMOUNT,
                      Sum(Nvl(DEDUCTION,0)) DEDUCTION_FROM_REG,
                      Sum(Nvl(GPS_AMOUNT, 0)) GPS_AMOUNT,
                      Sum(Nvl(CGST,0)) CGST,
                      Sum(Nvl(SGST,0)) SGST,
                      Sum(Nvl(IGST,0)) IGST,
                      Sum(Nvl(TDS_AMOUNT,0)) TDS_AMOUNT
                 FROM
                      ct_vms
                 WHERE 
                      TO_DATE(TO_CHAR(PAYMENT_DATE,'YYYYMM'),'YYYYMM') BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                                                    THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                                                      ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                                                         AND TO_DATE('%(year)s%(month)s','YYYYMM')
                      AND NET_PAYMENT IS NOT NULL
                 GROUP BY REGION_CODE,AC_CENTER_CODE,BRANCH_BRANCH_CODE,VENDOR_CODE,  TO_CHAR(PAYMENT_DATE,'MON')
                )B,
                (
                 SELECT
                      DISTINCT vm.REGION_CODE,
                      VM.AC_CENTER_CODE,
                      vm.BRANCH_BRANCH_CODE,
                      TYPE.SUPPLIER_CODE,
                      SR.PAN_NO,
                      SR.SUPP_NAME,
                      Count(DISTINCT FL.REGIS_NO) VEHICLE
                 FROM
                      ct_vms vm ,ct_fleet fl,ct_srm SR,ct_srm_SERVICE_TYPE TYPE  
                 WHERE
                      vm.VENDOR_CODE=fl.VNDR_CODE
                      AND vm.BRANCH_BRANCH_CODE=FL.BRANCH_BRANCH_CODE
                      AND FL.VNDR_CODE=TYPE.SUPPLIER_CODE
                      AND TYPE.STATUS='VL'
                      AND SR.PAN_NO=TYPE.PAN_NO
                      AND SR.BRANCH_CODE=TYPE.BRANCH_CODE  
                      AND FL.VEHICLE_TYPE='VO'
                      AND Trunc(VM.LIB_DATE)>=Trunc(SYSDATE-365)
                      AND TO_DATE(TO_CHAR(LIB_DATE,'YYYYMM'),'YYYYMM') BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                                                    THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                                                      ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                                                         AND TO_DATE('%(year)s%(month)s','YYYYMM')
                      AND TYPE.SERVICE_CODE='70007'
                      AND FL.CKH is null  
                GROUP BY vm.REGION_CODE,VM.AC_CENTER_CODE,vm.BRANCH_BRANCH_CODE,TYPE.SUPPLIER_CODE,SR.PAN_NO,SR.SUPP_NAMe
                )C,
                (
                 SELECT
                     DISTINCT X.REGION_CODE,
                     X.ACCOUNTITNG_CODE AC_CENTER_CODE,
                     X.BRANCH_CODE BRANCH_BRANCH_CODE,
                     VENDOR_CODE
                 FROM
                     ct_vms V, XM_BRANCHS X
                 WHERE
                     V.BRANCH_BRANCH_CODE=X.BRANCH_CODE
                ) D,
                (
                 SELECT
                     LORRY_BRANCH_BRANCH_CODE,
                     VENDOR_CODE,
                     TO_CHAR(TCS_END_DATE,'MON') MONTHS,
                     Sum(Nvl(HANDLING_EXP_IN,0)) HANDLING_EXP,
                     Sum(Nvl(HANDLING_EXP_OUT,0)) DRIVER_EXP,
                     Sum(Nvl(ENROUTE_EXP,0)) ENROUTE_EXP,
                     Sum(Nvl(DIESEL_EXPENSES,0)) DIESEL_EXP,
                     Sum(Nvl(HIRE_RATE,0)) LORRY_HIRE,
                     Sum(Nvl(NET_PAYMENT,0)) LIB_AMT,
                     Sum(Nvl(INCENTIVE,0)),
                     Sum(Nvl(DEDUCTION,0)) DEDUCTION_AMT,
                     Sum(Nvl(TDS,0)) TDS,
                     Sum(Nvl(PENALTY,0)) PENALTY_AMT,
                     Sum(Nvl(MISC_DED,0)) STATIONARY_DED,
                     Sum(Nvl(TOLL_EXP,0)) TOLL_EXP
                 FROM
                     CT_TCS
                 WHERE
                    VEHICLE_TYPE='VO'
                    AND TO_DATE(TO_CHAR(TCS_END_DATE,'YYYYMM'),'YYYYMM') BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                                                    THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                                                      ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                                                         AND TO_DATE('%(year)s%(month)s','YYYYMM')
                 GROUP BY LORRY_BRANCH_BRANCH_CODE, VENDOR_CODE, TO_CHAR(TCS_END_DATE,'MON')
               ) T  
               WHERE  
                   B.BRANCH_BRANCH_CODE=T.LORRY_BRANCH_BRANCH_CODE
                   AND B.VENDOR_CODE=T.VENDOR_CODE
                   AND B.MONTHS = T.MONTHS
                   AND D.REGION_CODE=A.REGION_CODE(+)
                   AND D.REGION_CODE=B.REGION_CODE(+)  
                   AND D.REGION_CODE=C.REGION_CODE(+)
                   AND D.BRANCH_BRANCH_CODE=A.BRANCH_BRANCH_CODE(+)  
                   AND D.BRANCH_BRANCH_CODE=B.BRANCH_BRANCH_CODE(+)  
                   AND D.BRANCH_BRANCH_CODE=C.BRANCH_BRANCH_CODE(+)
                   AND D.AC_CENTER_CODE=A.AC_CENTER_CODE(+)  
                   AND D.AC_CENTER_CODE=B.AC_CENTER_CODE(+)
                   AND D.AC_CENTER_CODE=C.AC_CENTER_CODE(+)
                   AND D.VENDOR_CODE=A.VENDOR_CODE(+)  
                   AND D.VENDOR_CODE=B.VENDOR_CODE(+)
                   AND D.VENDOR_CODE=C.SUPPLIER_CODE(+)
                   AND (A.LIB_AMOUNT>0 OR B.NET_PAYMENT>0)
               GROUP BY D.REGION_CODE ,D.AC_CENTER_CODE ,D.BRANCH_BRANCH_CODE ,D.VENDOR_CODE,C.SUPP_NAME ,C.PAN_NO,C.VEHICLE, T.LORRY_BRANCH_BRANCH_CODE, T.VENDOR_CODE, B.MONTHS
               ORDER BY B.MONTHS, REGION,AC_CODE,BRANCH,VO_CODE
               '''%{'year':year,'month':month}
    
        df9B = pd.read_sql_query(sql9B, con)
    
        df9B = pd.pivot_table(data = df9B, index = ['MONTH','REGION'], values = ['DEDUCTION_TO_EARLY_PAYMENT','GPS_AMOUNT','DEDUCTION_FROM_REGION','PENALTY_AMT'],\
                          aggfunc = 'sum', fill_value = 0)
    
        df9B = pd.concat([d.append(d.sum().rename((k,'Total'))) for k,d in df9B.groupby(level=0)]).\
              append(df9B.sum().rename(('Grand','Total'))).reset_index()
    
        df9B['TOTAL_PENALTY'] = df9B.iloc[:,2:6].sum(axis = 1)

        sql10 =  '''
                SELECT 
                to_char(to_date(TCS_LIB_MONTHYEAR, 'MMYYYY'),'MM-YYYY') AS "Month",
                X.REGION_CODE FRM_REGION,
                X.CONTROLLING_CODE FRM_CONTROLLING,
                X.BRANCH_CODE FRMBRANCH,
                FRM_ZONE,FRMBRN_TYP,
                TO_REGION,
                TO_CONTROLLING,
                TOBRANCH,  
                TO_ZONE,
                TOBRN_TYP,
                VEH_TYPE,
                To_Number(TOTKM)TOTKM,
                To_Number(NOOFTCS) NOOFTCS,
                NOOFVEH,
                TOTCOST,
                TOTCAPACITY,
                TOTWT,
                WT_LOSS,
                LOSS_PER,
                COST_PER_KG,
                TARGET_PER_KG,  
                PER_VEH_AMT,
                VEN_UPDOWN_COST_RS13,
                WT_PER_VEH,PER_DAY_WT,
                TGTCOST_VS_ACTCOST,
                TOT_FREIGHT 
            FROM 
                ct_hub_costing A,
                XM_BRANCHS X 
            WHERE 
                A.FRMBRANCH=X.BRANCH_CODE 
                AND TO_DATE(TO_CHAR(TO_DATE(TCS_LIB_MONTHYEAR,'MMYYYY'),'YYYYMM'),'YYYYMM')
                          BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                    ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                        AND TO_DATE('%(year)s%(month)s','YYYYMM')
                AND VEH_TYPE!='TOT'   
            UNION  
                SELECT DISTINCT TCS_LIB_MONTHYEAR,
                     X.REGION_CODE FRM_REGION,
                     X.CONTROLLING_CODE FRM_CONTROLLING,
                     X.BRANCH_CODE FRMBRANCH,
                     FRM_ZONE,FRMBRN_TYP,
                     TO_REGION,
                     TO_CONTROLLING,
                     TOBRANCH,
                     TO_ZONE,
                     TOBRN_TYP,
                     'XTOTAL',
                     TOTKM,
                     SUM(NOOFTCS) NOOFTCS,
                     SUM(NOOFVEH) NOOFVEH,  
                     SUM(TOTCOST) TOTCOST,
                     SUM(TOTCAPACITY) TOTCAPACITY,
                     SUM(TOTWT) TOTWT,
                     Sum(NVL(TOTCAPACITY,0))-sum(NVL(TOTWT,0)) WT_LOSS,
                     Round( ((sum(nvl(TOTCAPACITY,0)-nvl(TOTWT,0))) / CASE WHEN Sum(TOTCAPACITY)=0 THEN 1 ELSE Sum(TOTCAPACITY) END)*100 ,2) LOSS_PER,  
                     Round(Sum(NVL(TOTCOST,0))/CASE WHEN sum(TOTWT)=0 THEN 1 ELSE sum(TOTWT) END ,2) COST_PER_KG,Round((TOTKM*13/8000),2) TARGET_PER_KG,
                     Round( sum(NVL(TOTCOST,0))/CASE WHEN sum(NVL(NOOFTCS,0))=0 THEN 1 ELSE sum(NVL(NOOFTCS,0)) END,0) PER_VEH_AMT,  
                     sum(TOTKM)*2*13 VEN_UPDOWN_COST_RS13,
                     Round(sum(TOTWT)/ CASE WHEN sum(NVL(NOOFTCS,0))=0 THEN 1 ELSE Sum(NOOFTCS) END,0) WT_PER_VEH,
                     Round(sum(nvl(TOTWT,0)/30),0) PER_DAY_WT, 
                     Round(((TOTKM*13/8000) - ((Sum(NVL(TOTCOST,0))/CASE WHEN sum(TOTWT)=0 THEN 1 ELSE sum(TOTWT) END)))/CASE WHEN (TOTKM*13/8000)=0 THEN 1 ELSE (TOTKM*13/8000) END  ,2) TGTCOST_VS_ACTCOST,
                     SUM(NVL(TOT_FREIGHT,0)) TOT_FREIGHT  
                FROM 
                    ct_hub_costing C,
                    XM_BRANCHS X 
                WHERE 
                    C.FRMBRANCH=X.BRANCH_CODE 
                    AND TO_DATE(TO_CHAR(TO_DATE(TCS_LIB_MONTHYEAR,'MMYYYY'),'YYYYMM'),'YYYYMM')
                          BETWEEN '01-APR-'||CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                    ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                        AND TO_DATE('%(year)s%(month)s','YYYYMM') 
                    AND VEH_TYPE!='TOT'  
                GROUP BY 
                   TCS_LIB_MONTHYEAR,
                   X.REGION_CODE,
                   X.CONTROLLING_CODE,
                   X.BRANCH_CODE,
                   FRM_ZONE,
                   FRMBRN_TYP,
                   TO_REGION,
                   TO_CONTROLLING,
                   TOBRANCH,
                   TO_ZONE,
                   TOBRN_TYP,
                   TOTKM  
               ORDER BY 
                   FRM_REGION,
                   FRM_CONTROLLING,
                   FRMBRANCH,
                   TOBRANCH 
    
            '''%{'year': year, 'month': month}
    
        df10 = pd.read_sql_query(sql10, con)
    
        df10 = df10[(df10['FRMBRN_TYP'] == 'HUB') & (df10['TOBRN_TYP'] == 'HUB') \
               & (df10['VEH_TYPE'] != 'XTOTAL')].groupby(['Month',\
               'FRM_REGION','FRMBRANCH'])[['TOTCAPACITY','TOTWT','WT_LOSS']].sum(numeric_only = True)

        df10['WT_LOSS%'] = (df10['WT_LOSS']/df10['TOTCAPACITY'] * 100).round(2)

        df10 = df10.unstack(0).swaplevel(0, 1, 1).sort_index(1).reset_index()

        sql11 = '''
                  SELECT
                        U1.*, 
                        U2.EXCESS 
                  FROM
                      (
                        SELECT 
                             distinct A.cln_branch_code,
                             A.cln_no,
                             to_char(A.cln_date,'MM-YYYY') CLNDT,
                             B.BRANCH_BRANCH_CODE_MUST, 
                             A.branch_branch_code,
                             XM.REGION_CODE REGION,
                             A.cns_cns_no,
                             to_char(last_Day(A.arrival_date),'MM-YYYY') MONTH,
                             C.PKG_PER_CLN,
                             NVL(A.short,0)short,
                             REPLACE (A.MISSING_REMARKS,',0','') MISSING_REMARKS,
                             B.LOAD_STAFF,B.LOAD_STAFF_NAME, 
                             B.UNLOAD_STAFF,
                             B.UNLOAD_STAFF_NAME,
                             D.DECLARED_VALUE
                        FROM 
                             CT_UNLDTL A,
                             CT_CLN B,
                             CT_CLNDTL C,
                             CT_DWB D,
                             XM_BRANCHS XM
                        WHERE 
                             A.CLN_NO=B.CHALLAN_NO  
                             AND A.CLN_BRANCH_CODE=B.BRANCH_BRANCH_CODE 
                             AND A.CLN_DATE=B.CHALLAN_DATE
                             AND B.CHALLAN_NO=C.CLN_CHALLAN_NO  
                             AND B.CHALLAN_DATE=C.CLN_CHALLAN_DATE 
                             AND B.BRANCH_BRANCH_CODE=C.CLN_BRANCH_BRANCH_CODE  
                             AND A.cln_branch_code=C.cln_branch_branch_code 
                             AND c.cns_cns_no=a.cns_cns_no  
                             AND D.DWB_NO=C.CNS_CNS_NO 
                             AND D.URO_BASIS IS NULL 
                             AND B.BRANCH_BRANCH_CODE_MUST = XM.BRANCH_CODE
                             AND C.PKG_PER_CLN NOT IN('-1','0')    
                             AND to_date(to_Char(A.arrival_date,'YYYYMM'),'YYYYMM') 
                             BETWEEN 
                                  '01-APR-'|| CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                      THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                        ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                           AND TO_DATE('%(year)s%(month)s','YYYYMM')
                             AND A.MISSING_REMARKS NOT IN ('MANUALL','MANAUL','MANVEL','MANUAL','menual','manual','manul','MNUAL', 'Short, 0','Short','0')
                             AND A.CLEAR_FLAG IS NULL
                             AND NOT EXISTS ( SELECT * FROM CT_COF F WHERE F.UNLOADING_CNS_CNS_NO=D.DWB_NO )
                        ) U1,
                      ( 
                         SELECT 
                              BRANCH_BRANCH_CODE, 
                              CNS_CNS_NO, 
                              Sum(Nvl(EXCESS,0)) EXCESS 
                         FROM 
                              CT_UNLDTL 
                         WHERE 
                              to_date(to_Char(arrival_date,'YYYYMM'),'YYYYMM') 
                                BETWEEN 
                                   '01-APR-'|| CASE WHEN TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'MM') IN ('01','02','03')
                                       THEN TO_CHAR(TO_NUMBER(TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY'))-1)
                                         ELSE TO_CHAR(TO_DATE('%(year)s%(month)s','YYYYMM'),'YYYY') END
                                             AND TO_DATE('%(year)s%(month)s','YYYYMM')
                         GROUP BY 
                               BRANCH_BRANCH_CODE, CNS_CNS_NO                                  
                      ) U2
                  WHERE 
                      U1.CNS_CNS_NO=U2.CNS_CNS_NO 
                      AND U1.BRANCH_BRANCH_CODE=U2.BRANCH_BRANCH_CODE 
                      AND U1.PKG_PER_CLN<>U2.EXCESS
                  ORDER BY 
                      U1.cln_branch_code,
                      U1.BRANCH_BRANCH_CODE_MUST,
                      U1.CLNDT
                '''%{'year': year,'month': month}

        df11 = pd.read_sql_query(sql11, con)
    
        df11 = pd.pivot_table(
                              data = df11,
                              index = 'REGION',
                              columns = 'MONTH',
                              values = 'CNS_CNS_NO',
                              aggfunc = 'count',
                              margins = True,
                              margins_name = 'Total Short'
                             )

        sql12 = '''
               SELECT 
                    xm.region_code bkg_reg
                   ,xm.controlling_code bkg_cont
                   ,A.UNLOADING_CNS_BRANCH_BRANCH_CO BKG_STN
                   ,A.UNLOADING_CNS_CNS_NO DWB_NO
                   ,TO_CHAR(A.UNLOADING_CNS_CNS_DATE,'DD/MON/YYYY') BKG_DATE
                   ,xm1.region_code dly_reg,xm1.controlling_code dly_cont
                   ,A.UNLOADING_BRANCH_BRANCH_CODE DLY_STN 
                   ,C.CNOR_NAME
                   ,C.CNEE_NAME
                   ,A.COF_NO,TO_CHAR(A.COF_DATE,'DD/MON/YYYY')COF_DATE
                   ,TO_CHAR(TO_DATE(A.COF_DATE,'DD-MON-YY'),'MM-YYYY') MTH 
                   ,A.CLAIM_AMOUNT
                   ,B.CLAIM_TYPE
                   ,B.INSURED
                   ,B.RECOVERY_AMOUNT
                   ,C.DWB_BOOKING_BASIS
                   ,C.GOODS_DET_GOODS_CODE 
                   ,D.GOODS_DESC 
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
            ORDER BY   
                 TO_DATE(MTH, 'MM-YYYY') 

          '''%{'year': year, 'month': month}
    
        df12 = pd.read_sql_query(sql12, con)
    

        ''' Using Pandas and Xlsxwriter '''

        xlsx_io = io.BytesIO()
        writer = pd.ExcelWriter(xlsx_io, engine='xlsxwriter') # pylint: disable=abstract-class-instantiated

        ''' Aligning the center '''

        #df0 = df0.style.set_properties(**{'text-align': 'center'})
        #df1 = df1.style.set_properties(**{'text-align': 'center'})
        #df2 = df2.style.set_properties(**{'text-align': 'center'})
        #df3 = df3.style.set_properties(**{'text-align': 'center'})
        #df4 = df4.style.set_properties(**{'text-align': 'center'})
        #df5 = df5.style.set_properties(**{'text-align': 'center'})
        #df5A = df5A.style.set_properties(**{'text-align': 'center'})
        #df6 = df6.style.set_properties(**{'text-align': 'center'})
        #df7 = df7.style.set_properties(**{'text-align': 'center'})
        #df8 = df8.style.set_properties(**{'text-align': 'center'})
        #df8A = df8A.style.set_properties(**{'text-align': 'center'})
        #df9 = df9.style.set_properties(**{'text-align': 'center'})
        #df9A = df9A.style.set_properties(**{'text-align': 'center'})
        #df9B = df9B.style.set_properties(**{'text-align': 'center'})
        #df10 = df10.style.set_properties(**{'text-align': 'center'})
        #df11 = df11.style.set_properties(**{'text-align': 'center'})
        #df12 = df12.style.set_properties(**{'text-align': 'center'})
        
        ''' Writing dataframe to excel '''

        df0.to_excel(writer,  sheet_name = 'Index', startrow = 7 , startcol = 9, index = False, header = False)
        df1.to_excel(writer,  sheet_name = 'Total Business', startrow = 10 , startcol = 2)
        df2.to_excel(writer,  sheet_name = 'REGION WISE up to the month', startrow = 5, startcol = 2)
        df3.to_excel(writer,  index = False, sheet_name = 'REGION WISE for the month', startrow = 7, startcol = 8)
        df4.to_excel(writer,  index = False, sheet_name = 'Booking Comp Product Wise', startrow = 4, startcol = 1)
        df5.to_excel(writer,  index = False, sheet_name = 'AIR INTL', startrow = 4, startcol = 1)
        df5A.to_excel(writer, sheet_name = 'Pharma', header = False, index = False, startrow = 5, startcol = 2)
        df6.to_excel(writer,  sheet_name = 'Operation', header = False, startrow = 2, startcol = 1)
        df7.to_excel(writer,  sheet_name = 'ECOM', header = False, startrow = 2, startcol = 1)
        df8.to_excel(writer, sheet_name = 'Marketing', index = False, header = True, startrow = 5, startcol = 1)
        df8A.to_excel(writer, sheet_name = 'AIR', startrow = 2, startcol = 1)
        df9.to_excel(writer, sheet_name = 'BA', index = True, header = True, startrow = 2, startcol = 1)
        df9A.to_excel(writer, sheet_name = 'VO', index = False, startrow = 5, startcol = 2) 
        df9B.to_excel(writer, sheet_name = 'VO Deduction', header = True, index = False, startrow = 5, startcol = 2)
        df10.to_excel(writer, sheet_name = 'HUB Wise Weight Loss', header = True, startrow = 2, startcol = 1)
        df11.to_excel(writer, sheet_name = 'Short', startrow = 5, startcol = 2)
        df12.to_excel(writer, sheet_name = 'COF Details', index = False, header = True, startrow = 2, startcol = 1)

        ''' Using Xlsxwriter workbook and worksheet objects '''

        workbook = writer.book
        worksheet0 = writer.sheets['Index']
        worksheet1 = writer.sheets['Total Business']
        worksheet2 = writer.sheets['REGION WISE up to the month']
        worksheet3 = writer.sheets['REGION WISE for the month']
        worksheet4 = writer.sheets['Booking Comp Product Wise']
        worksheet5 = writer.sheets['AIR INTL']
        worksheet5A = writer.sheets['Pharma']
        worksheet6 = writer.sheets['Operation']
        worksheet7 = writer.sheets['ECOM']
        worksheet8 = writer.sheets['Marketing']
        worksheet8A = writer.sheets['AIR']
        worksheet9 = writer.sheets['BA']
        worksheet9A = writer.sheets['VO']
        worksheet9B = writer.sheets['VO Deduction']
        worksheet10 = writer.sheets['HUB Wise Weight Loss']
        worksheet11 = writer.sheets['Short']
        worksheet12 = writer.sheets['COF Details']


        ''' Creating the worksheet formatting '''

        border = workbook.add_format({
                                       'border': 2
                                      })
        
        header = workbook.add_format({
                                       'font_size':12.5
                                      ,'bold':True
                                      ,'indent': 2
                                     })

        background_color = workbook.add_format({
                                                'bg_color': '#f0efed'
                                              })

        '''MIS - Operations Index'''

        try:
           from urllib.request import urlopen
        except ImportError:
           from urllib2 import urlopen
        
        url = 'https://www.tciexpress.in/images/tci-logo.png'
        image_data = io.BytesIO(urlopen(url).read())
        worksheet0.insert_image('B2', url, {'image_data': image_data, 'x_scale': 0.5, 'y_scale': 0.5})
        worksheet0.hide_gridlines(option = 2) 
        worksheet0.write(6,8,'MIS - Operations Index', header)
        worksheet0.conditional_format( 'A1:AZ1000' , { 'type' : 'no_errors' , 'format' : background_color})
        
        ''' Total Month Wise Business '''

        worksheet1.hide_gridlines(option = 2) 
        worksheet1.write(9,7,'Total Month Wise Business', header)
        worksheet1.conditional_format( 'C10:O12' , { 'type' : 'no_errors' , 'format' : border})
        worksheet1.conditional_format( 'C10:O10' , { 'type' : 'no_errors' , 'format' : background_color})
        worksheet1.set_column('C:O', 11)

        ''' Region Wise up to the Month '''

        worksheet2.hide_gridlines(option = 2)
        worksheet2.write(4,7,'Region Wise up to the Month', header)
        worksheet2.conditional_format( 'C5:O16' , { 'type' : 'no_errors' , 'format' : border})
        worksheet2.conditional_format( 'C5:O5' , { 'type' : 'no_errors' , 'format' : background_color})
        worksheet2.set_column('C:O', 11)

        ''' Region Wise for the Month '''

        worksheet3.hide_gridlines(option = 2)
        worksheet3.write(6,8,'Region Wise for the Month', header)
        worksheet3.conditional_format( 'I7:J18' , { 'type' : 'no_errors' , 'format' : border} )
        worksheet3.conditional_format( 'I7:J7' , { 'type' : 'no_errors' , 'format' : background_color} )
        worksheet3.set_column('I:J', 16)

        ''' Booking Comp Product Wise '''

        worksheet4.hide_gridlines(option = 2)
        worksheet4.write(2,5,'Booking Comp Product Wise', header)
        worksheet4.write(3,4,'Last Year', header)
        worksheet4.write(3,7,'Current Year', header)
        worksheet4.write(3,10,'Growth %', header)
        worksheet4.conditional_format( 'B3:L88' , { 'type' : 'no_errors' , 'format' : border} )
        worksheet4.conditional_format( 'B3:L3' , { 'type' : 'no_errors' , 'format' : background_color} )
        worksheet4.set_column('B:L', 11.5)

        ''' AIR INTL '''

        worksheet5.hide_gridlines(option = 2)
        worksheet5.write(1,8,'Comparative Analysis of Air International Business', header)
        worksheet5.write(2,5,'For the month', header)
        worksheet5.write(2,13,'Up to the month', header)
        worksheet5.write(3,3,'LY', header)
        worksheet5.write(3,6,'CY', header)
        worksheet5.write(3,9,'Growth', header)
        worksheet5.write(3,12,'LY', header)
        worksheet5.write(3,15,'CY', header)
        worksheet5.write(3,18,'Growth', header)
        worksheet5.conditional_format( 'B2:T15' , { 'type' : 'no_errors' , 'format' : border} )
        worksheet5.conditional_format( 'B2:T2' , { 'type' : 'no_errors' , 'format' : background_color} )
        worksheet5.set_column('G:P', 11.5)

        ''' Pharma '''

        worksheet5A.hide_gridlines(option = 2)
        worksheet5A.write(1,10,'Comparative Analysis of Pharmaceuticals Business', header)
        worksheet5A.write(2,7, 'FOR THE MONTH', header)
        worksheet5A.write(2,12, 'UP TO THE MONTH', header )
        worksheet5A.write(2,19, 'GROWTH %', header)
        worksheet5A.write(3,5, 'Last Year', header)
        worksheet5A.write(3,8, 'Current Year', header)
        worksheet5A.write(3,11, 'Last Year', header)
        worksheet5A.write(3,15, 'Current Year', header)
        worksheet5A.write(4,2, 'Region', header)
        worksheet5A.write(4,3, 'DWB', header)
        worksheet5A.write(4,4, 'WT', header)
        worksheet5A.write(4,5, 'FRT', header)
        worksheet5A.write(4,6, 'Yield', header)
        worksheet5A.write(4,7, 'DWB', header)
        worksheet5A.write(4,8, 'WT', header)
        worksheet5A.write(4,9, 'FRT', header)
        worksheet5A.write(4,10, 'Yield', header)
        worksheet5A.write(4,11, 'DWB', header)
        worksheet5A.write(4,12, 'WT', header)
        worksheet5A.write(4,13, 'FRT', header)
        worksheet5A.write(4,14, 'Yield', header)
        worksheet5A.write(4,15, 'DWB', header)
        worksheet5A.write(4,16, 'WT', header)
        worksheet5A.write(4,17, 'FRT', header)
        worksheet5A.write(4,18, 'Yield', header)
        worksheet5A.write(4,19, 'DWB', header)
        worksheet5A.write(4,20, 'WT', header)
        worksheet5A.write(4,21, 'FRT', header)
        worksheet5A.write(4,22, 'Yield', header)
        worksheet5A.write(4,23, 'DWB', header)
        worksheet5A.write(4,24, 'WT', header)
        worksheet5A.write(4,25, 'FRT', header)
        worksheet5A.write(4,26, 'Yield', header)
        worksheet5A.conditional_format( 'C2:AA15' , { 'type' : 'no_errors' , 'format' : border})
        worksheet5A.conditional_format( 'C2:AA2' , { 'type' : 'no_errors' , 'format' : background_color})
        worksheet5A.set_column('C:AA', 11.5)
        worksheet5A.freeze_panes('D1')

        ''' Operation '''

        worksheet6.hide_gridlines(option = 2)
        worksheet6.write(1,6,'Operations MIS', header)
        worksheet6.conditional_format( 'B2:N50' , { 'type' : 'no_errors' , 'format' : border} )
        worksheet6.conditional_format( 'B2:N2' , { 'type' : 'no_errors' , 'format' : background_color})
        worksheet6.set_column('C:O', 11.5)
        worksheet6.set_column('B:B', 32)
        worksheet6.freeze_panes('C1')

        ''' ECOM '''

        worksheet7.hide_gridlines(option = 2)
        worksheet7.write(1,6,'ECOM MIS', header)
        worksheet7.conditional_format( 'B2:N56' , { 'type' : 'no_errors' , 'format' : border} )
        worksheet7.conditional_format( 'B2:N2' , { 'type' : 'no_errors' , 'format' : background_color} )
        worksheet7.set_column('C:O', 11.5)
        worksheet7.set_column('B:B', 32)
        worksheet7.freeze_panes('C1')

        ''' Marketing '''

        worksheet8.hide_gridlines(option = 2)
        worksheet8.write(1,12,'Comparative Analysis of DIVISIONS', header)
        worksheet8.freeze_panes('C2')
        worksheet8.write(2,9,'For the Month', header)
        worksheet8.write(2,21,'Up to the Month', header)
        worksheet8.write(3,4,'SURFACE', header)
        worksheet8.write(3,10,'AIR', header)
        worksheet8.write(3,16,'ALL DIVISION', header)
        worksheet8.write(3,22,'SURFACE', header)
        worksheet8.write(3,28,'AIR', header)
        worksheet8.write(3,34,'ALL DIVISION', header)
        worksheet8.write(4,2,'LY', header)
        worksheet8.write(4,3,'CY', header)
        worksheet8.write(4,5,'LY', header)
        worksheet8.write(4,6,'CY', header)
        worksheet8.write(4,8,'LY', header)
        worksheet8.write(4,9,'CY', header)
        worksheet8.write(4,11,'LY', header)
        worksheet8.write(4,12,'CY', header)
        worksheet8.write(4,14,'LY', header)
        worksheet8.write(4,15,'CY', header)
        worksheet8.write(4,17,'LY', header)
        worksheet8.write(4,18,'CY', header)
        worksheet8.write(4,20,'LY', header)
        worksheet8.write(4,21,'CY', header)
        worksheet8.write(4,23,'LY', header)
        worksheet8.write(4,24,'CY', header)
        worksheet8.write(4,26,'LY', header)
        worksheet8.write(4,27,'CY', header)
        worksheet8.write(4,29,'LY', header)
        worksheet8.write(4,30,'CY', header)
        worksheet8.write(4,32,'LY', header)
        worksheet8.write(4,33,'CY', header)
        worksheet8.write(4,35,'LY', header)
        worksheet8.write(4,36,'CY', header)
        worksheet8.set_column('B:AL', 11.5)
        worksheet8.conditional_format( 'B2:AL16' , { 'type' : 'no_errors' , 'format' : border} )
        worksheet8.conditional_format( 'B2:AL2' , { 'type' : 'no_errors' , 'format' : background_color} )

        ''' AIR MIS '''

        worksheet8A.hide_gridlines(option = 2)
        worksheet8A.write(1,6,'AIR MIS', header)
        worksheet8A.conditional_format( 'B2:N30' , { 'type' : 'no_errors' , 'format' : border} )
        worksheet8A.conditional_format( 'B2:N2' , { 'type' : 'no_errors' , 'format' : background_color} )
        worksheet8A.set_column('C:O', 11.5)
        worksheet8A.set_column('B:B', 32)
        worksheet8A.freeze_panes('C1')

        ''' BA Details '''

        worksheet9.hide_gridlines(option = 2)
        worksheet9.freeze_panes('D1')
        worksheet9.write(1, 10, 'BA Details', header)
        worksheet9.conditional_format( 'B2:N100' , { 'type' : 'no_errors' , 'format' : border})
        worksheet9.conditional_format( 'B2:N2' , { 'type' : 'no_errors' , 'format' : background_color} )
        worksheet9.set_column('B:N', 13.5)

        ''' VO '''

        worksheet9A.hide_gridlines(option = 2)
        worksheet9A.write(4,7,'Region Wise No of VO Up to the Month ', header)
        worksheet9A.conditional_format( 'C5:Q90' , { 'type' : 'no_errors' , 'format' : border})
        worksheet9A.conditional_format( 'C5:Q5' , { 'type' : 'no_errors' , 'format' : background_color})
        worksheet9A.set_column('C:Q', 11)
        worksheet9A.freeze_panes(6,4)

        ''' VO Deduction '''

        worksheet9B.hide_gridlines(option = 2)
        worksheet9B.write(4,4,'Region Wise VO Deduction Up to the Month ', header)
        worksheet9B.conditional_format( 'C5:I96' , { 'type' : 'no_errors' , 'format' : border})
        worksheet9B.conditional_format( 'C5:I5' , { 'type' : 'no_errors' , 'format' : background_color})
        worksheet9B.set_column('C:D', 15.5)
        worksheet9B.set_column('E:I', 18.5)
        worksheet9B.freeze_panes(6,4)

        ''' HUB Weight Loss '''

        worksheet10.hide_gridlines(option = 2)
        worksheet10.freeze_panes('C1')
        worksheet10.write(1, 10, 'HUB Wise Weight Loss', header)
        worksheet10.conditional_format( 'B2:AZ33' , { 'type' : 'no_errors' , 'format' : border})
        worksheet10.conditional_format( 'B2:AZ2' , { 'type' : 'no_errors' , 'format' : background_color} )
        worksheet10.set_column('B:AZ', 13.5)

        ''' Short '''
        worksheet11.hide_gridlines(option = 2)
        worksheet11.write(4,7,'Region Wise No of Short DWB Up to the Month ', header)
        worksheet11.conditional_format( 'C5:P16' , { 'type' : 'no_errors' , 'format' : border})
        worksheet11.conditional_format( 'C5:P5' , { 'type' : 'no_errors' , 'format' : background_color})
        worksheet11.set_column('C:P', 11)

        ''' COF Details '''

        worksheet12.hide_gridlines(option = 2)
        worksheet12.freeze_panes(3,0)
        worksheet12.write(1,9,'Docket Wise COF Details', header)
        worksheet12.conditional_format( 'B2:U5000' , { 'type' : 'no_errors' , 'format' : border} )
        worksheet12.conditional_format( 'B2:U2' , { 'type' : 'no_errors' , 'format' : background_color} )
        worksheet12.set_column('B:T', 13.5)
        worksheet12.set_column('U:U', 53.5)

        ''' Xlsxwriter save, and automatic download '''

        writer.save()
        xlsx_io.seek(0)
        media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        data = base64.b64encode(xlsx_io.read()).decode("utf-8")
        href_data_downloadable = f'data:{media_type};base64,{data}'
        return href_data_downloadable 


