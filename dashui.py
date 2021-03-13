import dash
import dash_html_components as html
from dash.dependencies import Input,Output,State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd 
from datapreprocessing import preprocessingnpredictions,etsyprediction
import plotly 
import plotly.express as px
import plotly.io as pio
import os.path


app=dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
project_name= 'Sentiment Analysis'


def ui():
    df=pd.read_csv(r'estypredictedreviews.csv')
    dfn=df[df['predictedvalue']==0] 
    dfn=dfn.iloc[:6,:]
    dfp=df[df['predictedvalue']==1]
    dfp=dfp.iloc[:6,:]
    df1=pd.concat([dfp,dfn])

    pie_chart=px.pie(
        data_frame=df,
        values=[df['predictedvalue'].value_counts()[1],df['predictedvalue'].value_counts()[0]],
        names=['Positive Reviews','Negative Reviews'],
        color=['Positive Reviews','Negative Reviews'],
        color_discrete_sequence=['Red','Orange'],
        title='Positive and Negative Reviews Distribution',
        width=600,                          
        height=380,                         
        hole=0.5, 
    )

    layout= html.Div([
         dbc.Row([
            dbc.Col(
               html.Div([
            dcc.Graph(
                id='pie_graph',
                figure=pie_chart
            )
        ]
        )
            ),
        dbc.Col(
            html.Div(
            [
            html.H2(children='Etsy reviews'),
            dcc.Dropdown(id='dropdown',
           placeholder="Select exisiting Review",
            options=[{'label':i,'value':i}for i in df1.review],
            value='Select the etsy reviews',
            optionHeight=70,
            style = {'margin-bottom': '30px','min-width':'670px','padding-top':'25px'}
            ),
            dbc.Button(              
               "Submit", 
                id='submitdropdown',
                color="dark", 
                className="mr-1",
                n_clicks=0,
                style={'margin':'0 45%','padding':'5px 15px'}
                ),
            html.Div(id='container1',style={'padding-top':'15px'})
            ]
        )
        )    
         ]
        ),
        dbc.Row(
            [
            dbc.Col([
            
            html.Div(
            [   
                html.Div([
                html.H2('Word Cloud'),
                dbc.Button("ALL Words",
                 id="allbt",
                 outline=True,
                 color="info", 
                 className="mr-1",
                 n_clicks_timestamp=0,
                 style={'padding':'10px','padding-right':'15px'}
                 ),
                dbc.Button("Positve Words",
                id="posbt",
                 outline=True,
                 color="success", 
                 className="mr-1",
                 n_clicks_timestamp=0,
                 style={'padding':'10px','padding-right':'15px'}
                 ),
                dbc.Button("Negative Words",
                id="negbt",
                outline=True, 
                color="danger",
                className="mr-1",
                n_clicks_timestamp=0,
                style={'padding':'10px','padding-right':'15px'}
                )
                ],style={'padding-left':'15px'}
                ),
                html.Div(id='container',style={'padding':'15px'})
            ]
        ),
            ]
        ),
        dbc.Col([
            html.H2("Try it yourself!"),
            html.Div(
         [
              dcc.Textarea(
                id='textarea',
                placeholder="Enter Your review text here",
                rows=5,
                # cols=8,
                style={'width':'650px','height':'300'}
            ),
            html.Div(id='container2',style={'padding':'15px 15px 15px 10px'})
         ]
     )   
        ]
        )
                
            ]
        )
    ]
    )
    return layout

@app.callback(
    Output('container','children'),
    [
        Input('allbt','n_clicks_timestamp'),
        Input('posbt','n_clicks_timestamp'),
        Input('negbt','n_clicks_timestamp'),
    ]
)
def wordcloudbutton(allbt,posbt,negbt):

    if int(allbt) > int(posbt) and int(allbt)>int(negbt):
        return html.Div([
            html.Img(src=app.get_asset_url('wholeword.png'))])
    elif int(posbt) > int(allbt) and int(posbt)>int(negbt):
        return html.Div([
            html.Img(src=app.get_asset_url('posword.png'))
            ])
    elif int(negbt) > int(allbt) and int(negbt) > int(posbt):
       return html.Div([
           html.Img(src=app.get_asset_url('wholeword.png'))
           ])
    else:
        pass
    
@app.callback(
    Output('container1','children'),
    [
        Input('submitdropdown','n_clicks')
    ],
    State('dropdown','value')
)
def dropdownui(n_clicks,value):
    predict=preprocessingnpredictions(value)
    if (n_clicks>0):
        if(int(predict)==1):
            return html.Div([
                dbc.Alert("Its a Positive review", color="success")
                ])
        else:
            return html.Div([
                    dbc.Alert("Its a Negative review", color="danger")
                ])

@app.callback(
    Output('container2','children'),
    [
        Input('textarea','value')
    ]
)
def updatetextarea(textvalue):
    predicted_value=preprocessingnpredictions(textvalue)
    if(int(predicted_value)==1):
            return html.Div([
                dbc.Alert("Its a Positive review", color="success")
                ])
    else:
        return html.Div([
                dbc.Alert("Its a Negative review", color="danger")
                ])


def main():
    global app
    app.title=project_name
    if os.path.isfile('estypredictedreviews.csv'):
        pass
    else:
        etsyprediction()
    app.layout=ui()
    app.run_server()
    app=None

if __name__ == '__main__':
    main()
