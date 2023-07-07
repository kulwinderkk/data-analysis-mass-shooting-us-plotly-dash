###############################
# US Mass Shooting Dash app
# 
# Prepared By: Kulwinder Kaur
###############################

#importing necessary libraries
import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State


#instantiate the app
# app=Dash(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
#reading the dataset
df=pd.read_csv('cleaned_out.csv')
#setting the date column to date time format
df['Date']=pd.to_datetime(df['Date'])

state_list= df['State'].unique().tolist()
state_list.append('All available states')
#the four charts on the app
#chart-1
df_plot= df.groupby(['Year', 'State'])[['Date']].count().reset_index()
fig_1=px.bar(df_plot, x='Year', y='Date', 
                    labels={'Date': '# cases'},
                    color_discrete_sequence=['#bad6eb', '#2b7bba'])
fig_1.update_layout(width=500,
                      height=300,
                      margin=dict(l=40, r=20, t=20, b=30),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                 xaxis_title='Year', yaxis_title='Number of cases')

#chart-2
df_plot_2=df.groupby(['Year']).agg({'Fatalities': 'sum', 'Injured': 'sum', 'Total victims': 'sum'}).reset_index().sort_values('Year', ascending=True)
fig_2=go.Figure()
fig_2.add_trace(go.Scatter( x=df_plot_2['Year'], y=df_plot_2['Fatalities'],
                    mode='lines+markers',
                    name='Fatalities'))
fig_2.add_trace(go.Scatter(x=df_plot_2['Year'], y=df_plot_2['Injured'],
                    mode='lines+markers', name='Injured'))
fig_2.add_trace(go.Scatter(x=df_plot_2['Year'], y=df_plot_2['Total victims'],
                    mode='lines+markers', name='Total Victims'))
fig_2.update_layout(width=500,
                      height=300,
                      margin=dict(l=40, r=20, t=20, b=30),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                 xaxis_title='Year', yaxis_title='Individuals affected')
fig_2.update_layout(hovermode="x")
#chart-3
fig_3 = go.Figure()
fig_3.add_trace(go.Scattergeo(
        locationmode = 'USA-states', 
        text=[f'State: {x}; Fatalities: {y}; Target_group : {z}' for x,y,z in list(zip(df['State'], df['Fatalities'], df['Target_group']  ))] ,
        lat= df['Latitude'],
        lon= df['Longitude'],
        marker = dict(
                size = df['Fatalities']),

    ))

fig_3.update_layout(width=500,
                      height=300,
                      margin=dict(l=40, r=20, t=20, b=30),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
        showlegend = True,
        geo = dict(
            scope = 'usa'
        )
    )
fig_3.update_layout(showlegend=False)

#chart4
fig_4 = px.sunburst(df, path=['Race', 'Gender', 'Mental Health Issues'], values='Total victims', labels={'labels':'Mental Health Issues',
                                                                                                      'id': 'Race'})
fig_4.update_layout(width=500,
                      height=300,
                      margin=dict(l=40, r=20, t=20, b=30),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')

#specifying color of the app
colors = {
    'title': "#2E4053",
    'text': "#47476b",
    'background': '#161A1D'
}

#defining sidebar
sidebar = html.Div(
    [
        dbc.Row(
            [
                html.P('Settings')
                ],
            style={"height": "5vh"}, className='bg-primary text-white'
            ),
        dbc.Row(
            [
                html.Div([
                    html.P('Select State',
                           style={'margin-top': '8px', 'margin-bottom': '4px'},
                           className='font-weight-bold'),
                    dcc.Dropdown(id='dropdown-state', multi=False, value='All available states',
                                 options=[{'label': x, 'value': x}
                                          for x in state_list],
                                 style={'width': '240px'}
                    ),
                    html.P('Select the Year range',
                           style={'margin-top': '16px', 'margin-bottom': '4px'},
                           className='font-weight-bold')
                    ]),
                    
                html.Div([
                    
                    dcc.RangeSlider(1965, 2020,1,  
                    value=[1966, 2017], 
                    marks={i: '{}'.format(i) for i in range(1966,2020,2)},  
                    id='range-slider',
                    vertical=True
                    ),
                    html.Button(id='my-button', n_clicks=0, children='apply',
                                style={'margin-top': '16px'},
                                className='bg-dark text-white'),
                    html.Hr()
                    ]
                    , style ={'margin-left': '20px'},
            ),

        ],
        

                    
    ) ])
#defining heading
heading=html.Div(
    html.H1(children='Data Analysis - US Mass Shooting', style={"fontSize": "35px", "color": colors['title'], 'textAlign': 'center'}))

#defining content
content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div([
                            html.P(children='Total mass shooting incidences', id='fig_1_heading', className='font-weight-bold'),
                            dcc.Graph(id='fig_1', figure=fig_1, className='bg-light')
                        ])
                        
                        ]),
                dbc.Col(
                    [
                        html.P('Individuals affected in terms of fatalities/injured/total victims', className='font-weight-bold'),
                        dcc.Graph(id='fig_2', figure=fig_2, className='bg-light')
                    ],
                    className='bg-light'
                    )
            ],
            style={"height": "50vh"}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('State wise fatalities and target group', className='font-weight-bold'),
                        dcc.Graph(id='fig_3', figure=fig_3, className='bg-light')
                    ],
                    className='bg-light'
                    ),

                dbc.Col(
                    [
                        html.Div([
                            html.P(children='Shooter Race/Gender/Mental Health condition and victims involved', id='fig_4_heading', className='font-weight-bold'),
                            dcc.Graph(id='fig_4', figure=fig_4, className='bg-light')
                        ])
                        
                        ])
            ],
            style={"height": "50vh"}
            )
        ]
    )



#specifying the layout

app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(heading, className='bg-info')),

        dbc.Row(
            [
                dbc.Col(sidebar, width=2, className='bg-light'),
                dbc.Col(content, width=10)
                ],
            style={"height": "100vh"}
            ),
        ],
    fluid=True
    )
#adding call back for chart 1

@app.callback(Output('fig_1', 'figure'),
              Input('my-button', 'n_clicks'),
              State('dropdown-state', 'value'),
              State('range-slider', 'value'))

def chart_1(n_clicks, state_sel, year_sel):
    
    filtered_df = df_plot.loc[(df_plot['Year']>=year_sel[0]) & (df_plot['Year']<=year_sel[1])]
    if state_sel=='All available states':
        new_df=filtered_df.groupby('Year')[['Date']].count().reset_index()
        chart1=px.bar(new_df, x='Year', y='Date', 
                    labels={'Date': '# cases'},
                    color_discrete_sequence=['#bad6eb', '#2b7bba'])
        chart1.update_layout(width=500,
                      height=300,
                      margin=dict(l=40, r=20, t=20, b=30),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                 xaxis_title='Year', yaxis_title='Number of cases')
    else:
        filtered_df_case=filtered_df[filtered_df['State']==state_sel]
        chart1=px.bar(filtered_df_case, x='Year', y='Date', 
                    labels={'Date': '# cases'},
                    color_discrete_sequence=['#bad6eb', '#2b7bba'])
        chart1.update_layout(width=500,
                      height=300,
                      margin=dict(l=40, r=20, t=20, b=30),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                 xaxis_title='Year', yaxis_title='Number of cases')
    return chart1

#adding call back for chart 2
@app.callback(Output('fig_2', 'figure'),
              Input('my-button', 'n_clicks'),
              State('dropdown-state', 'value'),
              State('range-slider', 'value'))



def chart_2(n_clicks, state_sel, year_sel):
    df_plot_2=df.groupby(['Year']).agg({'Fatalities': 'sum', 'Injured': 'sum', 'Total victims': 'sum'}).reset_index().sort_values('Year', ascending=True)
    filtered_df = df_plot_2.loc[(df_plot_2['Year']>=year_sel[0]) & (df_plot_2['Year']<=year_sel[1])]
    chart2=go.Figure()
    if state_sel=='All available states':

        chart2.add_trace(go.Scatter( x=filtered_df['Year'], y=filtered_df['Fatalities'],
                    mode='lines+markers',
                    name='Fatalities'))
        chart2.add_trace(go.Scatter(x=filtered_df['Year'], y=filtered_df['Injured'],
                    mode='lines+markers', name='Injured'))
        chart2.add_trace(go.Scatter(x=filtered_df['Year'], y=filtered_df['Total victims'],
                    mode='lines+markers', name='Total Victims'))
        chart2.update_layout(width=500,
                      height=300,
                      margin=dict(l=40, r=20, t=20, b=30),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                 xaxis_title='Year', yaxis_title='Individuals affected')
        chart2.update_layout(hovermode="x")
    else:
        df_plot_2=df.groupby(['Year', 'State']).agg({'Fatalities': 'sum', 'Injured': 'sum', 'Total victims': 'sum'}).reset_index().sort_values('Year', ascending=True)
        filtered_df = df_plot_2.loc[(df_plot_2['Year']>=year_sel[0]) & (df_plot_2['Year']<=year_sel[1])]
        filtered_df_case=filtered_df[filtered_df['State']==state_sel]
        chart2.add_trace(go.Scatter( x=filtered_df_case['Year'], y=filtered_df_case['Fatalities'],
                    mode='lines+markers',
                    name='Fatalities'))
        chart2.add_trace(go.Scatter(x=filtered_df_case['Year'], y=filtered_df_case['Injured'],
                    mode='lines+markers', name='Injured'))
        chart2.add_trace(go.Scatter(x=filtered_df_case['Year'], y=filtered_df_case['Total victims'],
                    mode='lines+markers', name='Total Victims'))
        chart2.update_layout(width=500,
                      height=300,
                      margin=dict(l=40, r=20, t=20, b=30),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                 xaxis_title='Year', yaxis_title='Individuals affected')
        chart2.update_layout(hovermode="x")
    
    return chart2

#adding call back for chart 3
@app.callback(Output('fig_3', 'figure'),
              Input('my-button', 'n_clicks'),
              State('dropdown-state', 'value'),
              State('range-slider', 'value'))



def chart_3(n_clicks, state_sel, year_sel):
    filtered_df = df.loc[(df['Year']>=year_sel[0]) & (df['Year']<=year_sel[1])]
    if state_sel=='All available states':
        chart3 = go.Figure()
        chart3.add_trace(go.Scattergeo(
                locationmode = 'USA-states',
                text=[f'State: {x}; Fatalities: {y}; Target_group : {z}' for x,y,z in list(zip(filtered_df['State'], filtered_df['Fatalities'], filtered_df['Target_group']  ))] ,
                lat= filtered_df['Latitude'],
                lon= filtered_df['Longitude'],
                marker = dict(
                size = filtered_df['Fatalities']),

                ))

        chart3.update_layout(width=500,
                      height=300,
                      margin=dict(l=40, r=20, t=20, b=30),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      showlegend = True,
                      geo = dict(
                      scope = 'usa'
                      )
                    )
        chart3.update_layout(showlegend=False)
        
    else:
        filtered_df_case=filtered_df[filtered_df['State']==state_sel]
        chart3 = go.Figure()
        chart3.add_trace(go.Scattergeo(
                locationmode = 'USA-states',
                text=[f'State: {x}; Fatalities: {y}; Target_group : {z}' for x,y,z in list(zip(filtered_df_case['State'], filtered_df_case['Fatalities'], filtered_df_case['Target_group']  ))] ,
                lat= filtered_df_case['Latitude'],
                lon= filtered_df_case['Longitude'],
                marker = dict(
                size = filtered_df_case['Fatalities']),

                ))

        chart3.update_layout(width=500,
                      height=300,
                      margin=dict(l=40, r=20, t=20, b=30),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      showlegend = True,
                      geo = dict(
                      scope = 'usa'
                      )
                    )
        chart3.update_layout(showlegend=False)
    return chart3

#adding call back for chart 4
@app.callback(Output('fig_4', 'figure'),
              Input('my-button', 'n_clicks'),
              State('dropdown-state', 'value'),
              State('range-slider', 'value'))



def chart_4(n_clicks, state_sel, year_sel):
    filtered_df = df.loc[(df['Year']>=year_sel[0]) & (df['Year']<=year_sel[1])]
    if state_sel=='All available states':
        chart4 = px.sunburst(filtered_df, path=['Race', 'Gender', 'Mental Health Issues'], values='Total victims', labels={'labels':'Mental Health Issues',
                                                                                                      'id': 'Race'},
                                                                                                      color_discrete_sequence=px.colors.qualitative.Pastel)
        chart4.update_layout(width=500,
                      height=300,
                      margin=dict(l=40, r=20, t=20, b=30),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')
        
    else:
        filtered_df_case=filtered_df[filtered_df['State']==state_sel]
        chart4 = px.sunburst(filtered_df_case, path=['Race', 'Gender', 'Mental Health Issues'], values='Total victims', labels={'labels':'Mental Health Issues',
                                                                                                      'id': 'Race'},
                                                                                                      color_discrete_sequence=px.colors.qualitative.Pastel)
        chart4.update_layout(width=500,
                      height=300,
                      margin=dict(l=40, r=20, t=20, b=30),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')
    return chart4



if __name__ == '__main__':
    app.run(debug=True)
