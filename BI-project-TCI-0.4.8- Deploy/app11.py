#! usr/bin/env python
#coding: utf-8

'''
_____________________________________________________________________________________________________________________________________________________________

                                                            DIESEL PRICES PYTHON SCRIPT APP-11
_____________________________________________________________________________________________________________________________________________________________

'''

from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash

import cx_Oracle as cx
import pandas as pd
import numpy as np

from dash_extensions.snippets import send_bytes
from dash_extensions import Download

import config_1

app = dash.Dash(__name__, requests_pathname_prefix = '/app11/')

row = html.Div([
                dbc.Row([
                          dbc.Col([
                                   html.Label('1st of month', style = {'font-weight':'bold', 'float':'left', 'margin':'2px'}),
                                   html.Button("Download Report", id = "btn0"),Download(id="download0"),
                                  ], style = {'float':'left', 'margin':'5px'}
                                 ),
                          dbc.Col([
                                   html.Label('For the month', style = {'font-weight':'bold','float':'left', 'margin':'2px'}),
                                   html.Button("Download Report", id = "btn1"),Download(id="download1"),
                                  ], style = {'float':'left', 'margin':'5px'}
                                 ),
                          dbc.Col([
                                   html.Label('Up to the month', style = {'font-weight':'bold','float':'left', 'margin':'2px'}),
                                   html.Button("Download Report", id = "btn2"),Download(id="download2"),
                                  ], style = {'float':'left', 'margin':'5px'}
                                )
                        ])
               ])

app.layout = html.Div([
                        dbc.Container(children = [row])
                      ],style = {'margin-left':'320px','margin-top':'200px'})


@app.callback(Output("download0", "data"), [Input("btn0", "n_clicks")], prevent_initial_call = True)

def generate_xlsx(n_clicks):

    if n_clicks is not None and n_clicks > 0:

        con = cx.connect(config_1.CONN_STR)

        sql = '''
                 SELECT 
                         TRUNC(PRICE_DATE,'MM') "Price Date"
                        ,CITY 
                        ,PRICES
                 FROM 
                         daily_diesel_prices
             WHERE
                 TRUNC(PRICE_DATE) >= '15-DEC-2020'
                 AND CITY IN ('New Delhi',
                              'Mumbai',
                              'Kolkata',
                              'Chennai',
                              'Gurgaon',
                              'Hyderabad',
                              'Bangalore',
                              'Jaipur')   
              '''

        df = pd.read_sql_query(sql, con)
    
        df['Price Date'] = df['Price Date'].dt.date
        
        df = pd.pivot_table(df, index = 'Price Date', columns = 'CITY', values = 'PRICES')
        
        df['Avg'] = df[['New Delhi','Mumbai','Kolkata','Chennai','Gurgaon','Hyderabad','Bangalore','Jaipur']].mean(axis = 1)
        
        df['Avg Chg'] = df['Avg'].diff().replace(np.nan,0)
        
        df['Cum Avg Chg'] = df['Avg Chg'].cumsum()
        
        df['% Avg Chg'] = df['Avg'].pct_change().mul(100).replace(np.nan,0)
        
        df['% Cum Avg Chg'] = df['Cum Avg Chg'].div(df['Avg'].shift(1)).mul(100).replace(np.nan,0)
        
        df = df.sort_values(by = 'Price Date', ascending = False).round(2)

        def to_xlsx(bytes_io):

            writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")

            df.to_excel(writer, index = True, sheet_name="Diesel Rates", startrow = 2, startcol = 1)

            workbook = writer.book

            worksheet = writer.sheets['Diesel Rates']

            border_fmt = workbook.add_format({'border': 2})

            headerfmt = workbook.add_format({'font_size':12.5,'bold':True,'indent': 2})

            startrow = 1
    
            endrow   = startrow + df.shape[0] + 1
    
            startcol = 1
    
            endcol   = startcol + df.shape[1] 

            format_align = workbook.add_format({'align': 'center'})

            worksheet.conditional_format(startrow, startcol, endrow, endcol,  { 'type' : 'no_errors' , 'format' : border_fmt} )

            worksheet.set_column('A:R', 15, format_align)

            worksheet.hide_gridlines(option = 2)

            worksheet.write(1,7,'Diesel Rates', headerfmt)

            writer.save()

        return send_bytes(to_xlsx, "diesel.xlsx")

@app.callback(Output("download1", "data"), [Input("btn1", "n_clicks")], prevent_initial_call = True)

def generate_xlsx(n_clicks):

    if n_clicks is not None and n_clicks > 0:

        con = cx.connect(config_1.CONN_STR)

        sql = '''
                 SELECT 
                         PRICE_DATE "Price Date"
                        ,CITY 
                        ,PRICES
                 FROM 
                         daily_diesel_prices
                 WHERE
                        TRUNC(PRICE_DATE) BETWEEN To_Date('01'||To_Char(Decode(To_Char(SYSDATE,'DD'),'01',Add_Months(SYSDATE,-1),SYSDATE),'MMYYYY'),'DDMMYYYY') 
                                          AND TRUNC(SYSDATE) 
                         AND CITY IN ('New Delhi',
                              'Mumbai',
                              'Kolkata',
                              'Chennai',
                              'Gurgaon',
                              'Hyderabad',
                              'Bangalore',
                              'Jaipur')  
                
            '''

        df = pd.read_sql_query(sql, con)
    
        df['Price Date'] = df['Price Date'].dt.date
        
        df = pd.pivot_table(df, index = 'Price Date', columns = 'CITY', values = 'PRICES')
        
        df['Avg'] = df[['New Delhi','Mumbai','Kolkata','Chennai','Gurgaon','Hyderabad','Bangalore','Jaipur']].mean(axis = 1)
        
        df['Avg Chg'] = df['Avg'].diff().replace(np.nan,0)
        
        df['Cum Avg Chg'] = df['Avg Chg'].cumsum()
        
        df['% Avg Chg'] = df['Avg'].pct_change().mul(100).replace(np.nan,0)
        
        df['% Cum Avg Chg'] = df['Cum Avg Chg'].div(df['Avg'].shift(1)).mul(100).replace(np.nan,0)
        
        df = df.sort_values(by = 'Price Date', ascending = False).round(2)

        def to_xlsx(bytes_io):

            writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")

            df.to_excel(writer, index = True, sheet_name="Diesel Rates", startrow = 2, startcol = 1)

            workbook = writer.book

            worksheet = writer.sheets['Diesel Rates']

            border_fmt = workbook.add_format({'border': 2})

            headerfmt = workbook.add_format({'font_size':12.5,'bold':True,'indent': 2})

            startrow = 1
    
            endrow   = startrow + df.shape[0] + 1
    
            startcol = 1
    
            endcol   = startcol + df.shape[1] 

            format_align = workbook.add_format({'align': 'center'})

            worksheet.conditional_format(startrow, startcol, endrow, endcol,  { 'type' : 'no_errors' , 'format' : border_fmt} )

            worksheet.set_column('A:R', 15, format_align)

            worksheet.hide_gridlines(option = 2)

            worksheet.write(1,7,'Diesel Rates', headerfmt)

            writer.save()

        return send_bytes(to_xlsx, "diesel.xlsx")

@app.callback(Output("download2", "data"), [Input("btn2", "n_clicks")], prevent_initial_call = True)

def generate_xlsx(n_clicks):

    if n_clicks is not None and n_clicks > 0:

        con = cx.connect(config_1.CONN_STR)

        sql = '''
                  SELECT 
                         PRICE_DATE "Price Date"
                        ,CITY 
                        ,PRICES
                 FROM 
                         daily_diesel_prices
                 WHERE
                        TRUNC(PRICE_DATE) >= '15-DEC-2020' 
                        AND CITY IN ('New Delhi',
                              'Mumbai',
                              'Kolkata',
                              'Chennai',
                              'Gurgaon',
                              'Hyderabad',
                              'Bangalore',
                              'Jaipur')  
                
            '''

        df = pd.read_sql_query(sql, con)
    
        df['Price Date'] = df['Price Date'].dt.date
        
        df = pd.pivot_table(df, index = 'Price Date', columns = 'CITY', values = 'PRICES')
        
        df['Avg'] = df[['New Delhi','Mumbai','Kolkata','Chennai','Gurgaon','Hyderabad','Bangalore','Jaipur']].mean(axis = 1)
        
        df['Avg Chg'] = df['Avg'].diff().replace(np.nan,0)
        
        df['Cum Avg Chg'] = df['Avg Chg'].cumsum()
        
        df['% Avg Chg'] = df['Avg'].pct_change().mul(100).replace(np.nan,0)
        
        df['% Cum Avg Chg'] = df['Cum Avg Chg'].div(df['Avg'].shift(1)).mul(100).replace(np.nan,0)
        
        df = df.sort_values(by = 'Price Date', ascending = False).round(2)

        def to_xlsx(bytes_io):

            writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")

            df.to_excel(writer, index = True, sheet_name="Diesel Rates", startrow = 2, startcol = 1)

            workbook = writer.book

            worksheet = writer.sheets['Diesel Rates']

            border_fmt = workbook.add_format({'border': 2})

            headerfmt = workbook.add_format({'font_size':12.5,'bold':True,'indent': 2})

            startrow = 1
    
            endrow   = startrow + df.shape[0] + 1
    
            startcol = 1
    
            endcol   = startcol + df.shape[1] 

            format_align = workbook.add_format({'align': 'center'})

            worksheet.conditional_format(startrow, startcol, endrow, endcol,  { 'type' : 'no_errors' , 'format' : border_fmt} )

            worksheet.set_column('A:R', 15, format_align)

            worksheet.hide_gridlines(option = 2)

            worksheet.write(1,7,'Diesel Rates', headerfmt)

            writer.save()

        return send_bytes(to_xlsx, "diesel.xlsx")



