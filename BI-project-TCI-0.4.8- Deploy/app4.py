''' Importing Python Libraries '''

from flask import current_app

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash

import cx_Oracle as cx
import pandas as pd
import numpy as np

import urllib
import io
import flask
import base64
import config

import warnings
warnings.filterwarnings("ignore", category = UserWarning)

app = dash.Dash(__name__, requests_pathname_prefix='/app4/',external_stylesheets = [dbc.themes.BOOTSTRAP])

row = html.Div([
                   dbc.Row([
                             dbc.Col([
                                       html.H6('Year',style = {'font-weight':'bold','textAlign':'center','text-indent':'80%'}),
                                       dcc.Dropdown(
                                                    id = 'year',
                                                    options = [{'label': y, 'value': y} for y in [ '2018','2019','2020','2021']],
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
                                               download="download.pdf",
                                               href="",
                                               target="_blank",
                                               
                                             ))
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

        pdf_io = io.BytesIO()

        with PdfPages(pdf_io) as export_pdf:

            if month == '01':
               month = 'January'
            elif month  == '02':
                 month = 'Feburary'
            elif month == '03':
                 month = 'March'
            elif month == '04':
                 month = 'April'
            elif month == '05':
                 month = 'May'
            elif month == '06':
                 month = 'June'
            elif month == '07':
                 month = 'July'
            elif month == '08':
                 month = 'August'
            elif month == '09':
                 month = 'September'
            elif month == '10':
                 month = 'October'
            elif month == '11':
                 month = 'November'
            elif month == '12':
                 month = 'December'
            else:
                 month = 'None'

            with current_app.open_resource('static/index.png') as f:
                 
                img00 = plt.imread(f)

            plt.imshow(img00)   
         
            plt.axis('off')

            plt.title('MIS for ' + str(month) + ' ' + str(year), loc = 'center', color = 'firebrick', fontweight = 'bold')
            
            export_pdf.savefig(dpi = 360)

            plt.close()

            df0A = pd.DataFrame({'Particulars':[
                                              '1. Total Business Month Wise',\
                                              '2. Region wise For the month Business',\
                                              '3. Region wise Last Three Month Total Business',\
                                              '4. Surface Business Growth % FTM',\
                                              '5. Surface Business Growth % CUM',\
                                              '6. Air + Air Intl Business Growth % FTM',\
                                              '7. Air + Air Intl Business Growth % CUM',\
                                              '8. Total Business Growth % FTM',\
                                              '9. Total Business Growth % CUM',\
                                              '10. Air Intl Business Growth',\
                                              '11. Pharma Business Growth',\
                                              '12. Leg wise Cost Per Kg Last Year Vs Current Year',\
                                              '13. Month Wise Cost V/s Yield Per Kg',\
                                              '14. Leg wise LY V/s CY Weight loss%',\
                                              '15. Branch to hub weight loss%',\
                                              '16. HUB to hub weight loss%',
                                              '17. HUB to Branch weight loss%',\
                                              '18. Service Level LY V/s CY Average',\
                                              '19. Month Wise Service Level',\
                                              '20. Month Wise MO Cost %',\
                                              '21. Outstanding Days',\
                                              '22. Outstanding v/s Realization',\
                                              '23. Region wise No of COF',\
                                              '24. Region wise COF Amt.']})

            fig0A = plt.figure()

            cell_text = []
            
            for row in range(len(df0A)):

                cell_text.append(df0A.iloc[row]) 

            plt.table(cellText=cell_text, loc='upper center', colLabels = None, cellLoc='left').set_fontsize(8)

            fig0A.suptitle('Index', fontsize = 10, color = 'white', fontweight = 'bold', ha = 'right')
            
            plt.axis('off')

            with current_app.open_resource('static/logo.png') as f:
                 
                img0A = plt.imread(f)
            
            nax0A = fig0A.add_axes([0.1, 0.8, 0.85, 0.21], anchor='NW', zorder=-2)
            
            nax0A.imshow(img0A)   
         
            nax0A.axis('off')
    
            export_pdf.savefig(dpi = 360)

            plt.close()

            con = cx.connect(config.CONN_STR)

            sql1 = '''SELECT
                         to_char(to_date(YEAR_MONTH_DAY,'YYYYMMDD'),'MON-YY') MONTHS
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
                        to_date(MONTHS,'MON-YY')
                
              '''%{'year': year, 'month': month}
    
       
            df1 = pd.read_sql_query(sql1, con)
            
            fig1 = plt.figure()

            plt.plot(df1['MONTHS'], df1['CYF'])

            for i,j in df1['CYF'].items():
                
                plt.annotate(str(j), xy=(i, j), fontsize = 5)

            fig1.suptitle('Total Business in (Lacs)\n', fontsize = 10, color = 'white', fontweight = 'bold', ha = 'right')

            plt.xlabel('Month',fontsize = 5)

            plt.ylabel('Revenue',fontsize = 5)

            plt.xticks(fontsize = 5)

            plt.yticks(fontsize = 5)

            plt.gca().spines['top'].set_visible(False)

            plt.gca().spines['right'].set_visible(False)

            with current_app.open_resource('static/logo.png') as f:
                 
                img1 = plt.imread(f)
            
            nax1 = fig1.add_axes([0.1, 0.8, 0.85, 0.21], anchor='NW', zorder=-2)
            
            nax1.imshow(img1)   
         
            nax1.axis('off')
    
            export_pdf.savefig(dpi = 360)

            plt.close()

            sql2 = '''
                     SELECT
                         REGION_CODE REGION
                        ,ROUND(SUM(NVL(TOT_FRT,0))/100000,2) CYF
                     FROM
                        CT_BUSINESS_GROWTH_NEW_IMPL
                     WHERE
                        LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM'))  = LAST_DAY(TO_DATE('%(year)s%(month)s','YYYYMM')) 
                        AND REGION_CODE <> 'XCRP'
                     GROUP BY
                        REGION_CODE
                     ORDER BY
                        REGION_CODE
          
               '''%{'year' : year, 'month' : month}
    
            df2 = pd.read_sql_query(sql2, con)
            
            fig2 = plt.figure()
    
            plt.plot(df2['REGION'], df2['CYF'])

            for i,j in df2['CYF'].items():
                
                plt.annotate(str(j), xy=(i, j), fontsize = 5)

            fig2.suptitle('Region Wise for the month \nTotal Business in (Lacs)', fontsize = 10, color = 'white', fontweight = 'bold', ha = 'right')

            plt.xlabel('Region',fontsize = 5)

            plt.ylabel('Revenue',fontsize = 5)

            plt.xticks(fontsize = 5)

            plt.yticks(fontsize = 5)

            plt.gca().spines['top'].set_visible(False)

            plt.gca().spines['right'].set_visible(False)

            with current_app.open_resource('static/logo.png') as f:
                 
                img2 = plt.imread(f)
            
            nax2 = fig2.add_axes([0.1, 0.8, 0.85, 0.21], anchor='NW', zorder=-2)
            
            nax2.imshow(img2)   
         
            nax2.axis('off')
    
            export_pdf.savefig(dpi = 360)

            plt.close()

            sql3 = '''
                       SELECT
                            REGION_CODE REGION
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
                            REGION_CODE
                       ORDER BY
                            REGION_CODE 
          
                    '''%{'year' : year, 'month' : month}
    
            df3 = pd.read_sql_query(sql3, con)
            
            fig3 = plt.figure()
    
            plt.plot(df3['REGION'], df3['CYF'])

            for i,j in df3['CYF'].items():
                
                plt.annotate(str(j), xy=(i, j), fontsize = 5)

            fig3.suptitle('Region Wise Up to the month \nTotal Business in (Lacs)', fontsize = 10, color = 'white', fontweight = 'bold', ha = 'right')

            plt.xlabel('Region',fontsize = 5)

            plt.ylabel('Revenue',fontsize = 5)

            plt.xticks(fontsize = 5)

            plt.yticks(fontsize = 5)

            plt.gca().spines['top'].set_visible(False)

            plt.gca().spines['right'].set_visible(False)

            with current_app.open_resource('static/logo.png') as f:
                 
                img3 = plt.imread(f)
            
            nax3 = fig3.add_axes([0.1, 0.8, 0.85, 0.21], anchor='NW', zorder=-2)
            
            nax3.imshow(img3)   
         
            nax3.axis('off')
    
            export_pdf.savefig(dpi = 360)

            plt.close()

            sql4 = '''
                       SELECT
                            REGION_CODE AS REGION
                           ,ROUND(((SUM(NVL(TOT_FRT,0)) - SUM(NVL(LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(LYA_TOT_FRT,0)),0) * 100),2) CYF
                       FROM
                           CT_BUSINESS_GROWTH_NEW_IMPL
                       WHERE
                            DIVISION_CODE = '21'
                            AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) = last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                            AND REGION_CODE <> 'XCRP'
                       GROUP BY
                            REGION_CODE
                       ORDER BY
                            REGION_CODE
                    '''%{'year' : year, 'month' : month}
    
            df4 = pd.read_sql_query(sql4, con)

            fig4 = plt.figure()
            
            plt.plot(df4['REGION'], df4['CYF'])

            for i,j in df4['CYF'].items():
                
                plt.annotate(str(j), xy=(i, j), fontsize = 5)

            fig4.suptitle('Surface Business Growth % FTM', fontsize = 10, color = 'white', fontweight = 'bold', ha = 'right')

            plt.xlabel('Region',fontsize = 5)

            plt.ylabel('Revenue',fontsize = 5)

            plt.xticks(fontsize = 5)

            plt.yticks(fontsize = 5)

            plt.gca().spines['top'].set_visible(False)

            plt.gca().spines['right'].set_visible(False)

            with current_app.open_resource('static/logo.png') as f:
                 
                img4 = plt.imread(f)
            
            nax4 = fig4.add_axes([0.1, 0.8, 0.85, 0.21], anchor='NW', zorder=-2)
            
            nax4.imshow(img4)   
         
            nax4.axis('off')

            export_pdf.savefig(dpi = 360)

            plt.close()

            sql5 = '''
                       SELECT
                            REGION_CODE AS REGION
                           ,ROUND(((SUM(NVL(TOT_FRT,0)) - SUM(NVL(LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(LYA_TOT_FRT,0)),0) * 100),2) CYF
                       FROM
                           CT_BUSINESS_GROWTH_NEW_IMPL
                       WHERE
                            DIVISION_CODE = '21'
                            AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                     THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                         ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                             AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))  
                                                AND REGION_CODE <> 'XCRP'
                       GROUP BY
                            REGION_CODE
                       ORDER BY
                            REGION_CODE
                    '''%{'year' : year, 'month' : month}
    
            df5 = pd.read_sql_query(sql5, con)

            fig5 = plt.figure()
            
            plt.plot(df5['REGION'], df5['CYF'])

            for i,j in df5['CYF'].items():
                
                plt.annotate(str(j), xy=(i, j), fontsize = 5)

            fig5.suptitle('Surface Business Growth % CUM', fontsize = 10, color = 'white', fontweight = 'bold', ha = 'right')

            plt.xlabel('Region',fontsize = 5)

            plt.ylabel('Revenue',fontsize = 5)

            plt.xticks(fontsize = 5)

            plt.yticks(fontsize = 5)

            plt.gca().spines['top'].set_visible(False)

            plt.gca().spines['right'].set_visible(False)

            with current_app.open_resource('static/logo.png') as f:
                 
                img5 = plt.imread(f)
            
            nax5 = fig5.add_axes([0.1, 0.8, 0.85, 0.21], anchor='NW', zorder=-2)
            
            nax5.imshow(img5)   
         
            nax5.axis('off')
    
            export_pdf.savefig(dpi = 360)

            plt.close()

            sql6 = '''
                       SELECT
                            REGION_CODE AS REGION
                           ,ROUND(((SUM(NVL(TOT_FRT,0)) - SUM(NVL(LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(LYA_TOT_FRT,0)),0) * 100),2) CYF
                       FROM
                           CT_BUSINESS_GROWTH_NEW_IMPL
                       WHERE
                            DIVISION_CODE IN ('22','26')
                            AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) = last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                            AND REGION_CODE <> 'XCRP'
                       GROUP BY
                            REGION_CODE
                       ORDER BY
                            REGION_CODE     
                    '''%{'year' : year, 'month' : month}
    
            df6 = pd.read_sql_query(sql6, con)

            fig6 = plt.figure()
            
            plt.plot(df6['REGION'], df6['CYF'])

            for i,j in df6['CYF'].items():
                
                plt.annotate(str(j), xy=(i, j), fontsize = 5)

            fig6.suptitle('AIR & AIR INTL Business \nGrowth % FTM', fontsize = 10, color = 'white', fontweight = 'bold', ha = 'right')

            plt.xlabel('Region',fontsize = 5)

            plt.ylabel('Revenue',fontsize = 5)

            plt.xticks(fontsize = 5)

            plt.yticks(fontsize = 5)

            plt.gca().spines['top'].set_visible(False)

            plt.gca().spines['right'].set_visible(False)

            with current_app.open_resource('static/logo.png') as f:
                 
                img6 = plt.imread(f)
            
            nax6 = fig6.add_axes([0.1, 0.8, 0.85, 0.21], anchor='NW', zorder=-2)
            
            nax6.imshow(img6)   
         
            nax6.axis('off')

            export_pdf.savefig(dpi = 360)

            plt.close()

            sql7 = '''
                       SELECT
                            REGION_CODE AS REGION
                           ,ROUND(((SUM(NVL(TOT_FRT,0)) - SUM(NVL(LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(LYA_TOT_FRT,0)),0) * 100),2) CYF
                       FROM
                           CT_BUSINESS_GROWTH_NEW_IMPL
                       WHERE
                            DIVISION_CODE IN ('22','26')
                            AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) 
                                BETWEEN '01-APR-'||CASE WHEN TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'MM') IN ('01','02','03')
                                     THEN TO_CHAR(TO_NUMBER(TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY'))-1)
                                         ELSE TO_CHAR(last_day(TO_DATE('%(year)s%(month)s','YYYYMM')),'YYYY') END
                                             AND last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))  
                            AND REGION_CODE <> 'XCRP'
                       GROUP BY
                            REGION_CODE
                       ORDER BY
                            REGION_CODE
                    '''%{'year' : year, 'month' : month}
    
            df7 = pd.read_sql_query(sql7, con)

            fig7 = plt.figure()
            
            plt.plot(df7['REGION'], df7['CYF'])

            for i,j in df7['CYF'].items():
                
                plt.annotate(str(j), xy=(i, j), fontsize = 5)

            fig7.suptitle('AIR & AIR INTL Business \nGrowth % CUM', fontsize = 10, color = 'white', fontweight = 'bold', ha = 'right')

            plt.xlabel('Region',fontsize = 5)

            plt.ylabel('Revenue',fontsize = 5)

            plt.xticks(fontsize = 5)

            plt.yticks(fontsize = 5)

            plt.gca().spines['top'].set_visible(False)

            plt.gca().spines['right'].set_visible(False)

            with current_app.open_resource('static/logo.png') as f:
                 
                img7 = plt.imread(f)
            
            nax7 = fig7.add_axes([0.1, 0.8, 0.85, 0.21], anchor='NW', zorder=-2)
            
            nax7.imshow(img7)   
         
            nax7.axis('off')

            export_pdf.savefig(dpi = 360)

            plt.close()

            sql8 = '''
                       SELECT
                            REGION_CODE AS REGION
                           ,ROUND(((SUM(NVL(TOT_FRT,0)) - SUM(NVL(LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(LYA_TOT_FRT,0)),0) * 100),2) CYF
                       FROM
                           CT_BUSINESS_GROWTH_NEW_IMPL
                       WHERE
                            LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) = last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                            AND REGION_CODE <> 'XCRP'
                       GROUP BY
                            REGION_CODE
                       ORDER BY
                            REGION_CODE
                    '''%{'year' : year, 'month' : month}
    
            df8 = pd.read_sql_query(sql8, con)

            fig8 = plt.figure()
            
            plt.plot(df8['REGION'], df8['CYF'])

            for i,j in df8['CYF'].items():
                
                plt.annotate(str(j), xy=(i, j), fontsize = 5)

            fig8.suptitle('Total Business Growth % FTM', fontsize = 10, color = 'white', fontweight = 'bold', ha = 'right')

            plt.xlabel('Region',fontsize = 5)

            plt.ylabel('Revenue',fontsize = 5)

            plt.xticks(fontsize = 5)

            plt.yticks(fontsize = 5)

            plt.gca().spines['top'].set_visible(False)

            plt.gca().spines['right'].set_visible(False)

            with current_app.open_resource('static/logo.png') as f:
                 
                img8 = plt.imread(f)
            
            nax8 = fig8.add_axes([0.1, 0.8, 0.85, 0.21], anchor='NW', zorder=-2)
            
            nax8.imshow(img8)   
         
            nax8.axis('off')

            export_pdf.savefig(dpi = 360)

            plt.close()

            sql9 = '''
                       SELECT
                            REGION_CODE AS REGION
                           ,ROUND(((SUM(NVL(TOT_FRT,0)) - SUM(NVL(LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(LYA_TOT_FRT,0)),0) * 100),2) CYF
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
                            REGION_CODE
                       ORDER BY
                            REGION_CODE
                    '''%{'year' : year, 'month' : month}
    
            df9 = pd.read_sql_query(sql9, con)

            fig9 = plt.figure()
            
            plt.plot(df9['REGION'], df9['CYF'])

            for i,j in df9['CYF'].items():
                
                plt.annotate(str(j), xy=(i, j), fontsize = 5)

            fig9.suptitle('Total Business Growth % CUM', fontsize = 10, color = 'white', fontweight = 'bold', ha = 'right')

            plt.xlabel('Region',fontsize = 5)

            plt.ylabel('Revenue',fontsize = 5)

            plt.xticks(fontsize = 5)

            plt.yticks(fontsize = 5)

            plt.gca().spines['top'].set_visible(False)

            plt.gca().spines['right'].set_visible(False)

            with current_app.open_resource('static/logo.png') as f:
                 
                img9 = plt.imread(f)
            
            nax9 = fig9.add_axes([0.1, 0.8, 0.85, 0.21], anchor='NW', zorder=-2)
            
            nax9.imshow(img9)   
         
            nax9.axis('off')

            export_pdf.savefig(dpi = 360)

            plt.close()

            sql10 = '''
                        WITH CTE1 AS (
                                      SELECT
                                           REGION_CODE REGION
                                          ,ROUND(((SUM(NVL(TOT_FRT,0)) - SUM(NVL(LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(LYA_TOT_FRT,0)),0) * 100),2) CYF
                                      FROM
                                          CT_BUSINESS_GROWTH_NEW_IMPL
                                      WHERE
                                          DIVISION_CODE = '26'
                                          AND LAST_DAY(TO_DATE(TO_CHAR(TO_DATE(YEAR_MONTH_DAY, 'YYYYMMDD'),'YYYYMM'),'YYYYMM')) = last_day(TO_DATE('%(year)s%(month)s','YYYYMM'))
                                AND REGION_CODE <> 'XCRP'
                            GROUP BY
                                REGION_CODE
                                     ),
                            CTE2 AS (
                                     SELECT
                                          REGION_CODE REGION
                                         ,ROUND(((SUM(NVL(TOT_FRT,0)) - SUM(NVL(LYA_TOT_FRT,0)))/NULLIF(SUM(NVL(LYA_TOT_FRT,0)),0) * 100),2) CYF
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
                                         REGION_CODE
                                    )
                           
                                SELECT
                                    CTE1.REGION REGION
                                   ,CTE1.CYF FTM
                                   ,CTE2.CYF CUM
                                FROM
                                   CTE1,CTE2
                                WHERE
                                   CTE1.REGION = CTE2.REGION
                                ORDER BY
                                   CTE1.REGION
                    
                    '''%{'year' : year, 'month' : month}
    
            df10 = pd.read_sql_query(sql10, con)
     
            fig10 = plt.figure()
     
            plt.plot(df10['REGION'], df10['FTM'])
        
            plt.plot(df10['REGION'], df10['CUM'])

            fig10.suptitle('AIR INTL Growth %', fontsize = 10, color = 'white', fontweight = 'bold', ha = 'right')
    
            for i,j in df10['FTM'].items():
        
                 plt.annotate(str(j), xy=(i, j + 25.0), fontsize = 7)
            
            for m,n in df10['CUM'].items():
        
                 plt.annotate(str(n), xy=(m, n - 50.0), fontsize = 7)

            plt.xticks(fontsize = 5)

            plt.yticks(fontsize = 5)
            
            plt.gca().spines['top'].set_visible(False)

            plt.gca().spines['right'].set_visible(False)

            plt.legend(['FTM %','CUM %'], fontsize = 7)

            with current_app.open_resource('static/logo.png') as f:
                 
                img10 = plt.imread(f)
            
            nax10 = fig10.add_axes([0.1, 0.8, 0.85, 0.21], anchor='NW', zorder=-2)
            
            nax10.imshow(img10)   
         
            nax10.axis('off')

            export_pdf.savefig(dpi = 360)
    
            plt.close()

            sql11 = ''' SELECT 
                    CTE2.REGION_CY REGION,
                    SUM(NVL(CTE1.DWB_NO_LY,0)) DWB_NO_LY_FTM,
                    SUM(NVL(CTE1.WT_LY,0)) WT_LY_FTM,
                    SUM(NVL(CTE1.FREIGHT_LY,0)) FREIGHT_LY_FTM,
                    (SUM(NVL(CTE1.FREIGHT_LY,0))/NULLIF(SUM(NVL(CTE1.WT_LY,0)),0)) YEILD_LY_FTM,
                    SUM(NVL(CTE2.DWB_NO_CY,0)) DWB_NO_CY_FTM,
                    SUM(NVL(CTE2.WT_CY,0)) WT_CY_FTM,
                    SUM(NVL(CTE2.FREIGHT_CY,0)) FREIGHT_CY_FTM,
                    (SUM(NVL(CTE2.FREIGHT_CY,0))/ NULLIF(SUM(NVL(CTE2.WT_CY,0)),0)) YEILD_CY_FTM,
                    SUM(NVL(CTE3.DWB_NO_LY,0)) DWB_NO_LY_CUM,
                    SUM(NVL(CTE3.WT_LY,0)) WT_LY_CUM,
                    SUM(NVL(CTE3.FREIGHT_LY,0)) FREIGHT_LY_CUM,
                    (SUM(NVL(CTE3.FREIGHT_LY,0))/NULLIF(SUM(NVL(CTE3.WT_LY,0)),0)) YEILD_LY_CUM,
                    SUM(NVL(CTE4.DWB_NO_CY,0)) DWB_NO_CY_CUM,
                    SUM(NVL(CTE4.WT_CY,0)) WT_CY_CUM,
                    SUM(NVL(CTE4.FREIGHT_CY,0)) FREIGHT_CY_CUM,
                   (SUM(NVL(CTE4.FREIGHT_CY,0))/NULLIF(SUM(NVL(CTE4.WT_CY,0)),0)) YEILD_CY_CUM
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
                     CTE2.REGION_CY
                   ORDER BY
                     CTE2.REGION_CY

                '''%{'year': year, 'month': month}

            df11 = pd.read_sql_query(sql11, con)
        
            df11['FREIGHT_GROWTH%_FTM'] = (((df11['FREIGHT_CY_FTM'] - df11['FREIGHT_LY_FTM'])/df11['FREIGHT_LY_FTM']) * 100).replace(np.inf,0).round(2)
     
            df11['FREIGHT_GROWTH%_CUM'] = (((df11['FREIGHT_CY_CUM'] - df11['FREIGHT_LY_CUM'])/df11['FREIGHT_LY_CUM']) * 100).replace(np.inf, 0).round(2)
    
            fig11 = plt.figure()
     
            plt.plot(df11['REGION'], df11['FREIGHT_GROWTH%_FTM'], linewidth = 1)
        
            plt.plot(df11['REGION'], df11['FREIGHT_GROWTH%_CUM'])
    
            for i,j in df11['FREIGHT_GROWTH%_FTM'].items():
        
                plt.annotate(str(j), xy=(i, j + 25.0), fontsize = 7)
            
            for m,n in df11['FREIGHT_GROWTH%_CUM'].items():
        
                plt.annotate(str(n), xy=(m, n - 50.0), fontsize = 7)

            plt.xticks(fontsize = 5)

            plt.yticks(fontsize = 5)
            
            plt.gca().spines['top'].set_visible(False)

            plt.gca().spines['right'].set_visible(False)

            fig11.suptitle('Pharma Business Growth %', fontsize = 10, color = 'white', fontweight = 'bold', ha = 'right')
        
            plt.legend(['FTM %','CUM %'])

            with current_app.open_resource('static/logo.png') as f:
                 
                 img11 = plt.imread(f)
            
            nax11 = fig11.add_axes([0.1, 0.8, 0.85, 0.21], anchor='NW', zorder=-2)
            
            nax11.imshow(img11)   
         
            nax11.axis('off')

            export_pdf.savefig(dpi = 360)
    
            plt.close()

            sql12A = '''
                      SELECT 
                           to_char(to_date(REPDATE,'MMYYYY'),'MON-YY') MONTHS
                          ,PICKCOST_KG "Pick up"
                          ,B2H_COSTKG "Branch to Hub"
                          ,H2H_COSTKG "Hub to Hub"
                          ,H2B_COSTKG "Hub to Branch"
                          ,B2C_COSTPER_KG "Delivery"
                          ,PICKCOST_KG + B2H_COSTKG + H2H_COSTKG + H2B_COSTKG + B2C_COSTPER_KG "Total"
                          ,YEILD_PKG "Surface Yiled"
                      FROM 
                          MIS_Summary 
                      WHERE
                            to_date(to_char(to_date(REPDATE,'MMYYYY'),'YYYYMM'),'YYYYMM') = ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12) 
                            AND REGION = 'ALL' 
                            AND CONT = 'ALL' 
                            AND BRN = 'ALL' 
                      ORDER BY
                            MONTHS
    
                   '''%{'year' : year, 'month' : month}

            df12A = pd.read_sql_query(sql12A, con).transpose()

            sql12B = '''
                       SELECT 
                            to_char(to_date(REPDATE,'MMYYYY'),'MON-YY') MONTHS
                           ,PICKCOST_KG "Pick up"
                           ,B2H_COSTKG "Branch to Hub"
                           ,H2H_COSTKG "Hub to Hub"
                           ,H2B_COSTKG "Hub to Branch"
                           ,B2C_COSTPER_KG "Delivery"
                           ,PICKCOST_KG + B2H_COSTKG + H2H_COSTKG + H2B_COSTKG + B2C_COSTPER_KG "Total"
                           ,YEILD_PKG "Surface Yiled"
                      FROM 
                          MIS_Summary 
                      WHERE
                          to_date(to_char(to_date(REPDATE,'MMYYYY'),'YYYYMM'),'YYYYMM') = TO_DATE('%(year)s%(month)s','YYYYMM')
                          AND REGION = 'ALL' 
                          AND CONT = 'ALL' 
                          AND BRN = 'ALL'
                      ORDER BY
                          MONTHS
            '''%{'year' : year, 'month' : month}

            df12B = pd.read_sql_query(sql12B, con).transpose()
    
            df12C = pd.merge(df12A, df12B, left_index=True, right_index=True).rename(columns = {'0_x':'LY','0_y':'CY'})
    
            df12D = df12C[1:]
    
            df12D = pd.DataFrame(df12D).reset_index().rename(columns = {'index':'Period'})
    
            df12D['CHANGE'] = (df12D['CY'] - df12D['LY'])
    
            df12D['CHANGE'] = df12D['CHANGE'].astype(float).round(2)
    
            pos = list(range(len(df12D['LY']))) 
    
            width = 0.15
    
            fig12 = plt.figure()
    
            plt.bar(pos, df12D['LY'], width) 
    
            plt.bar([p + width for p in pos], df12D['CY'], width) 
    
            plt.bar([p + width * 2 for p in pos], df12D['CHANGE'], width) 

            fig12.suptitle('LEG Wise Cost Per Kg LY Vs CY', fontsize = 10, color = 'white', fontweight = 'bold', ha = 'right')
    
            for i,j in df12D['LY'].items():
        
                plt.annotate(str(j), xy=(i - 0.2, j), fontsize = 7)
            
            for i,j in df12D['CY'].items():
        
                plt.annotate(str(j), xy=(i + 0.1, j), fontsize = 7)
            
            for i,j in df12D['CHANGE'].items():
        
                plt.annotate(str(j), xy=(i + 0.40, j), fontsize = 7)
    
            ticks = range(0,len(df12D['Period']))
    
            labels = ['Pick up','Branch to Hub','Hub to Hub','Hub to Branch','Delivery','Total','Surface Yiled']

            plt.yticks(fontsize = 5)
    
            plt.xticks(ticks, labels, fontsize = 5)
    
            plt.legend(['LY','CY','CHANGE'], loc='best', fontsize = 7)
    
            plt.gca().spines['top'].set_visible(False)

            plt.gca().spines['right'].set_visible(False)

            with current_app.open_resource('static/logo.png') as f:
                 
                img12 = plt.imread(f)
            
            nax12 = fig12.add_axes([0.1, 0.8, 0.85, 0.21], anchor='NW', zorder=-2)
            
            nax12.imshow(img12)   
         
            nax12.axis('off')

            export_pdf.savefig(dpi = 360)
    
            plt.close()

            sql13 = '''
                       SELECT 
                            to_char(to_date(REPDATE,'MMYYYY'),'MON-YY') "MONTH"
                           ,YEILD_PKG "YPK"
                           ,PICKCOST_KG + B2H_COSTKG + H2H_COSTKG + H2B_COSTKG + B2C_COSTPER_KG "TOTAL_COST"
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
                    '''%{'year' : year, 'month' : month}
    
            df13 = pd.read_sql_query(sql13, con)
    
            fig13 = plt.figure()
    
            pos = list(range(len(df13['TOTAL_COST']))) 
    
            width = 0.25
    
            plt.bar(pos, df13['TOTAL_COST'], width) 
    
            plt.bar([p + width for p in pos], df13['YPK'], width) 
    
            plt.plot(df13['MONTH'], df13['TOTAL_COST'], linestyle = (0,(5,5)), linewidth = 1.0)
    
            plt.plot(df13['MONTH'], df13['YPK'], linestyle = (0,(5,5)), linewidth = 1.0)

            fig13.suptitle('Month wise Cost vs Yield/Kg', fontsize = 10, color = 'white', fontweight = 'bold', ha = 'right')
    
            ticks = range(0,len(df13['MONTH']))
    
            labels = df13['MONTH']

            plt.yticks(fontsize = 5)
    
            plt.xticks(ticks, labels, fontsize = 5)
    
            for i,j in df13['TOTAL_COST'].items():
        
                plt.annotate(str(j), xy=(i - 0.1, j), fontsize = 7)
            
            for i,j in df13['YPK'].items():
        
                plt.annotate(str(j), xy=(i + 0.1, j), fontsize = 7)
            
            plt.gca().spines['top'].set_visible(False)

            plt.gca().spines['right'].set_visible(False)

            with current_app.open_resource('static/logo.png') as f:
                 
                img13 = plt.imread(f)
            
            nax13 = fig13.add_axes([0.1, 0.8, 0.85, 0.21], anchor='NW', zorder=-2)
            
            nax13.imshow(img13)   
         
            nax13.axis('off')

            export_pdf.savefig(dpi = 360)

            plt.close()

            sql18A = '''
                       SELECT 
                            to_char(to_date(REPDATE,'MMYYYY'),'MON-YY') MONTHS
                           ,PER_SAMEDAY Delivery_Same_Day
                           ,PER_NEXTDAY Delivery_Next_Day
                           ,SERLBLB2B_PER Surface_B2B
                           ,SERLBLC2C_PER Surface_C2C
                       FROM 
                           MIS_Summary 
                       WHERE
                           to_date(to_char(to_date(REPDATE,'MMYYYY'),'YYYYMM'),'YYYYMM') = ADD_MONTHS(TO_DATE('%(year)s%(month)s','YYYYMM'),-12) 
                           AND REGION = 'ALL' 
                           AND CONT = 'ALL' 
                           AND BRN = 'ALL' 
                       ORDER BY
                           MONTHS
    
                    '''%{'year' : year, 'month' : month}
            
            df18A = pd.read_sql_query(sql18A, con).transpose()
    
            sql18B = '''
                       SELECT 
                            to_char(to_date(REPDATE,'MMYYYY'),'MON-YY') MONTHS
                           ,PER_SAMEDAY Delivery_Same_Day
                           ,PER_NEXTDAY Delivery_Next_Day
                           ,SERLBLB2B_PER Surface_B2B
                           ,SERLBLC2C_PER Surface_C2C
                       FROM 
                           MIS_Summary 
                       WHERE
                           to_date(to_char(to_date(REPDATE,'MMYYYY'),'YYYYMM'),'YYYYMM') = TO_DATE('%(year)s%(month)s','YYYYMM')
                           AND REGION = 'ALL' 
                           AND CONT = 'ALL' 
                           AND BRN = 'ALL'
                       ORDER BY
                           MONTHS
    
                    '''%{'year' : year, 'month' : month}
   
            df18B = pd.read_sql_query(sql18B, con).transpose()
    
            df18C = pd.merge(df18A, df18B, left_index=True, right_index=True).rename(columns = {'0_x':'LY','0_y':'CY'})
    
            df18C = df18C[1:]
    
            df18D = pd.DataFrame(df18C).reset_index().rename(columns = {'index':'Period'})
    
            df18D['CHANGE'] = (df18D['CY'] - df18D['LY'])
    
            df18D['CHANGE'] = df18D['CHANGE'].astype(float).round(2)
    
            pos = list(range(len(df18D['LY']))) 
    
            width = 0.15
    
            fig18 = plt.figure()
    
            plt.bar(pos, df18D['LY'], width) 
    
            plt.bar([p + width for p in pos], df18D['CY'], width) 
    
            plt.bar([p + width*2 for p in pos], df18D['CHANGE'], width) 

            fig18.suptitle('Service level LY Vs CY', fontsize = 10, color = 'white', fontweight = 'bold', ha = 'right')
    
            for i,j in df18D['LY'].items():
        
                plt.annotate(str(j), xy=(i - 0.1, j), fontsize = 7)
            
            for i,j in df18D['CY'].items():
        
                plt.annotate(str(j), xy=(i + 0.1, j), fontsize = 7)
            
            for i,j in df18D['CHANGE'].items():
        
                plt.annotate(str(j), xy=(i + 0.22, j), fontsize = 7)
    
            ticks = range(0,len(df18D['Period']))
    
            labels = ['DELIVERY SAME DAY','DELIVERY NEXT DAY','SURFACE B2B','SURFACE C2C']

            plt.yticks(fontsize = 5)
    
            plt.xticks(ticks, labels, fontsize = 5)
    
            plt.legend(['LY','CY','CHANGE'], loc='upper right')
    
            plt.gca().spines['top'].set_visible(False)

            plt.gca().spines['right'].set_visible(False)

            with current_app.open_resource('static/logo.png') as f:
                 
                img18 = plt.imread(f)
            
            nax18 = fig18.add_axes([0.1, 0.8, 0.85, 0.21], anchor='NW', zorder=-2)
            
            nax18.imshow(img18)   
         
            nax18.axis('off')

            export_pdf.savefig(dpi = 360)

            plt.close()

            sql19 = '''
                     SELECT 
                          to_char(to_date(REPDATE,'MMYYYY'),'MON-YY') "MONTH"
                         ,PER_SAMEDAY + PER_NEXTDAY "DLY Same + Next Day"
                         ,SERLBLB2B_PER "Surface B2B"
                         ,SERLBLC2C_PER "Surface C2C"
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
                  '''%{'year' : year, 'month' : month}
    
            df19 = pd.read_sql_query(sql19, con)

            fig19 = plt.figure()
    
            plt.plot(df19['MONTH'], df19['DLY Same + Next Day'])
    
            plt.plot(df19['MONTH'], df19['Surface B2B'])
    
            plt.plot(df19['MONTH'], df19['Surface C2C'])

            fig19.suptitle('Month wise Service Level', fontsize = 10, color = 'white', fontweight = 'bold', ha = 'right')
    
            for i,j in df19['DLY Same + Next Day'].items():
        
                plt.annotate(str(j), xy=(i, j), fontsize = 5)
            
            for k,l in df19['Surface B2B'].items():
        
                plt.annotate(str(l), xy=(k, l), fontsize = 5)
            
            for m,n in df19['Surface C2C'].items():
        
                plt.annotate(str(n), xy=(m, n), fontsize = 5)

            label = ['DLY Same + Next Day','Surface B2B','Surface C2C']

            plt.legend(labels = label, loc="upper left", fontsize = 7)

            plt.xticks(fontsize = 5)

            plt.yticks(fontsize = 5)
            
            plt.gca().spines['top'].set_visible(False)

            plt.gca().spines['right'].set_visible(False)

            with current_app.open_resource('static/logo.png') as f:
                 
                img19 = plt.imread(f)
            
            nax19 = fig19.add_axes([0.1, 0.8, 0.85, 0.21], anchor='NW', zorder=-2)
            
            nax19.imshow(img19)   
         
            nax19.axis('off')

            export_pdf.savefig(dpi = 360)

            plt.close()

            sql20 = ''' 
                       SELECT 
                           to_char(to_date(REPDATE,'MMYYYY'),'MON-YY') "MONTH"
                          ,TOT_MOHIRE "TotalMOHIRE"
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
                    '''%{'year' : year, 'month' : month}
    
            df20 = pd.read_sql_query(sql20, con)
     
            fig20 = plt.figure()
     
            plt.plot(df20['MONTH'], df20['TotalMOHIRE'], linewidth = 2)

            fig20.suptitle('Month wise MO Cost%', fontsize = 10, color = 'white', fontweight = 'bold', ha = 'right')
        
            for i,j in df20['TotalMOHIRE'].items():
        
                plt.annotate(str(j), xy=(i, j), fontsize = 5)

            label = ['Total MO Hire']

            plt.legend(labels = label, fontsize = 7)

            plt.xticks(fontsize = 5)

            plt.yticks(fontsize = 5)
            
            plt.gca().spines['top'].set_visible(False)

            plt.gca().spines['right'].set_visible(False)

            with current_app.open_resource('static/logo.png') as f:
                 
                img20 = plt.imread(f)
            
            nax20 = fig20.add_axes([0.1, 0.8, 0.85, 0.21], anchor='NW', zorder=-2)
            
            nax20.imshow(img20)   
         
            nax20.axis('off')

            export_pdf.savefig(dpi = 360)

            plt.close()

            sql23 = '''
                        SELECT 
                             xm.region_code bkg_reg
                            ,xm.controlling_code bkg_cont
                            ,A.UNLOADING_CNS_BRANCH_BRANCH_CO BKG_STN
                            ,A.UNLOADING_CNS_CNS_NO DWB_NO
                            ,TO_CHAR(A.UNLOADING_CNS_CNS_DATE,'DD/MON/YYYY') BKG_DATE
                            ,xm1.region_code dly_reg
                            ,xm1.controlling_code dly_cont
                            ,A.UNLOADING_BRANCH_BRANCH_CODE DLY_STN 
                            ,C.CNOR_NAME
                            ,C.CNEE_NAME
                            ,A.COF_NO,TO_CHAR(A.COF_DATE,'DD/MON/YYYY')COF_DATE
                            ,TO_CHAR(TO_DATE(A.COF_DATE,'DD-MON-YY'),'MON-YY') MTH 
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
                            MTH
                    '''%{'year' : year, 'month' : month}

            df23 = pd.read_sql_query(sql23, con)
        
            pvt23A = pd.pivot_table(data = df23, index = 'BKG_REG', values = 'DWB_NO', aggfunc = 'count').reset_index()
        
            pvt23B = pd.pivot_table(data = df23, index = 'DLY_REG', values = 'DWB_NO', aggfunc = 'count').reset_index()
    
            fig23 = plt.figure()
     
            plt.plot(pvt23A['BKG_REG'], pvt23A['DWB_NO'], linewidth = 2)
        
            plt.plot(pvt23B['DLY_REG'], pvt23B['DWB_NO'], linewidth = 2)

            fig23.suptitle('Region wise No of COF', fontsize = 10, color = 'white', fontweight = 'bold', ha = 'right')
        
            for i,j in pvt23A['DWB_NO'].items():
        
                plt.annotate(str(j), xy=(i, j),fontsize = 5)
            
            for i,j in pvt23B['DWB_NO'].items():
        
                plt.annotate(str(j), xy=(i, j),fontsize = 5)

            plt.xticks(fontsize = 5)

            plt.yticks(fontsize = 5)
            
            plt.gca().spines['top'].set_visible(False)

            plt.gca().spines['right'].set_visible(False)

            with current_app.open_resource('static/logo.png') as f:
                 
                img23 = plt.imread(f)
            
            nax23 = fig23.add_axes([0.1, 0.8, 0.85, 0.21], anchor='NW', zorder=-2)
            
            nax23.imshow(img23)   
         
            nax23.axis('off')

            export_pdf.savefig(dpi = 360)

            plt.close()

            sql24 = '''
                      SELECT 
                           xm.region_code bkg_reg
                          ,xm.controlling_code bkg_cont
                          ,A.UNLOADING_CNS_BRANCH_BRANCH_CO BKG_STN
                          ,A.UNLOADING_CNS_CNS_NO DWB_NO
                          ,TO_CHAR(A.UNLOADING_CNS_CNS_DATE,'DD/MON/YYYY') BKG_DATE
                          ,xm1.region_code dly_reg
                          ,xm1.controlling_code dly_cont
                          ,A.UNLOADING_BRANCH_BRANCH_CODE DLY_STN 
                          ,C.CNOR_NAME
                          ,C.CNEE_NAME
                          ,A.COF_NO,TO_CHAR(A.COF_DATE,'DD/MON/YYYY')COF_DATE
                          ,TO_CHAR(TO_DATE(A.COF_DATE,'DD-MON-YY'),'MON-YY') MTH 
                          ,A.CLAIM_AMOUNT COFAMT
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
                            MTH
                '''%{'year' : year, 'month' : month}

            df24 = pd.read_sql_query(sql24, con)
        
            pvt24A = pd.pivot_table(data = df24, index = 'BKG_REG', values = 'COFAMT', aggfunc = 'sum').reset_index()
        
            pvt24B = pd.pivot_table(data = df24, index = 'DLY_REG', values = 'COFAMT', aggfunc = 'sum').reset_index()

            pvt24A['COFAMT'] = (pvt24A['COFAMT']/100000).round(2)

            pvt24B['COFAMT'] = (pvt24B['COFAMT']/100000).round(2)
    
            fig24 = plt.figure()
     
            plt.plot(pvt24A['BKG_REG'], pvt24A['COFAMT'], linewidth = 2)
        
            plt.plot(pvt24B['DLY_REG'], pvt24B['COFAMT'], linewidth = 2)

            fig24.suptitle('Region wise COF Amt', fontsize = 10, color = 'white', fontweight = 'bold', ha = 'right')
        
            for i,j in pvt24A['COFAMT'].items():
        
                plt.annotate(str(j), xy=(i, j),fontsize = 5)
            
            for i,j in pvt24B['COFAMT'].items():
        
                plt.annotate(str(j), xy=(i, j),fontsize = 5)

            plt.xticks(fontsize = 5)

            plt.yticks(fontsize = 5)
            
            plt.gca().spines['top'].set_visible(False)

            plt.gca().spines['right'].set_visible(False)

            with current_app.open_resource('static/logo.png') as f:
                 
                img24 = plt.imread(f)
            
            nax24 = fig24.add_axes([0.1, 0.8, 0.85, 0.21], anchor='NW', zorder=-2)
            
            nax24.imshow(img24)   
         
            nax24.axis('off')

            export_pdf.savefig(dpi = 360) 

            plt.close() 

            with current_app.open_resource('static/thank_you.png') as f:
                 
                img25 = plt.imread(f)
            
            plt.imshow(img25)   
         
            plt.axis('off')

            export_pdf.savefig(dpi = 360)

            plt.close()
      
        plt.rcParams['image.composite_image'] = True

        pdf_io.seek(0)
             
        mimetype = "application/pdf"

        data = base64.b64encode(pdf_io.read()).decode("utf-8")

        pdf_string = f"data:{mimetype};base64,{data}"

        return pdf_string

