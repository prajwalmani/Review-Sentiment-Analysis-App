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
    pie_chart=px.pie(
        data_frame=df,
        values=[df['predictedvalue'].value_counts()[1],df['predictedvalue'].value_counts()[0]],
        names=['Positive Reviews','Negative Reviews'],
        color=['Positive Reviews','Negative Reviews'],
        color_discrete_sequence=['Red','Orange'],
        title='Title',
        width=800,                          #figure width in pixels
        height=600,                         #figure height in pixels
        hole=0.5, 
    )
    pio.show(pie_chart)

    layout= html.Div(
        # [
        #     html.H1(id='title',children="Sentiment Analysis Using Insights"),
        #     dcc.Textarea(
        #         id='textarea',
        #         placeholder="Enter the review text here",
        #         style={'width':'100%','height':'100'}
        #     ),
        #     dbc.Button(
        #         id='submit_button'
        #         ,children='check review'
        #         ,color='dark'
        #         ,style={'width':'100%','height':'100'}),
        #     html.H1(id='result',children=None)
        # ]
        
        # [
        #     dcc.Dropdown(id='dropdown',
        #     options=[{ 'value': idx} for i in df2],
        #     value=''
        #     )
        # ]
        [
            dcc.Graph(
                id='pie_graph',
                figure=pie_chart
            )
        ]
    )
    return layout

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