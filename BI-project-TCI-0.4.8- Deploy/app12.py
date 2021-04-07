#! usr/bin/env python
#coding: utf-8

'''
_____________________________________________________________________________________________________________________________________________________________

                                                            TOLL PRICES PYTHON SCRIPT APP-12
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

app = dash.Dash(__name__, requests_pathname_prefix = '/app12/',external_stylesheets = [dbc.themes.BOOTSTRAP])

row = html.Div([
                dbc.Row([
                          
                          dbc.Col([
                                   html.Label('NHAI TOLL Prices', style = {'font-weight':'bold'}),
                                   html.Br(),
                                   html.Button("Download Report", id = "btn"),Download(id="download"),
                                  ]
                                 )
                          
                        ])
               ])

app.layout = html.Div([
                        html.Div(
                                [
                                  dbc.Container(children = [row])
                                ], style = {'margin-left':'30%','margin-top':'10%'}
                                )
                      ],style = {'border-style': 'outset','margin-top':'200px','width': '30%', 'height': '150px','margin-left':'35%'})

@app.callback(Output("download", "data"), [Input("btn", "n_clicks")], prevent_initial_call = True)

def generate_xlsx(n_clicks):

    if n_clicks is not None and n_clicks > 0:

        con = cx.connect(config_1.CONN_STR)

        sql = '''SELECT 
                         A.TOLL_NAME 
                        ,A.TOLL_STATE 
                        ,B.LAT
                        ,B.LON
                        ,A.UPTO_2_AXLE 
                        ,A.UPTO_3_AXLE 
                    FROM 
                        NHAI_TOLL_PRICES A
                    LEFT JOIN
                        NHAI_TOLL_LAT_LONG B ON (A.TOLL_NAME = B.TOLL_NAME)
                    ORDER BY
                        A.TOLL_NAME 
               '''

        df = pd.read_sql_query(sql, con)

        def to_xlsx(bytes_io):
    
            writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")

            df.to_excel(writer, sheet_name="NHAI Toll Prices", startrow = 1, startcol = 1, index = False)

            workbook = writer.book

            worksheet = writer.sheets['NHAI Toll Prices']

            border_fmt = workbook.add_format({'border': 2})

            format_align = workbook.add_format({'align': 'center'})

            background_color = workbook.add_format({'bg_color': '#8cf2ff'})

            worksheet.set_column('B:B', 20)

            worksheet.set_column('C:C', 32)

            worksheet.set_column('D:G', 20, format_align)

            worksheet.hide_gridlines(option = 2)

            startrow = 1
    
            endrow   = startrow + df.shape[0] 
    
            startcol = 1
    
            endcol   = startcol + df.shape[1] - 1

            worksheet.conditional_format(startrow, startcol, endrow, endcol,  { 'type' : 'no_errors' , 'format' : border_fmt} )

            worksheet.conditional_format('B2:G2',  { 'type' : 'no_errors' , 'format' : background_color})


            writer.save()

        return send_bytes(to_xlsx, "toll_prices.xlsx")






