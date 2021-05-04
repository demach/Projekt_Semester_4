from . import Site
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import sqlite3 as sql

name = __name__.split('.')[1]
settings = Site.load_settings(name)


connection = sql.connect(settings["db_path"])
    #print(settings["db_path"])
df = pd.read_sql('SELECT * from Orte', connection)

connection.close()

items = [{"label":i, "value":i} for i in df["Ortsbezeichnung"].unique()]

items = df["Ortsbezeichnung"].unique()



content = [
    html.Div(
        children=[
            html.Div(
                children=[
                    dbc.Row(
                        children=[
                            dbc.Col(
                                html.Div(
                                    children=[
                                        "Hello, I'm"
                                    ]
                                ),
                                width='auto'
                            ),
                            dbc.Col(
                                html.Div(
                                    children=[
                                        html.B(settings['name'])
                                    ],
                                    style={'font-size': 80}
                                ),
                                width='auto'
                            ),
                            dbc.Col(
                                html.Div(
                                    children=[
                                        "v1.0"
                                    ],
                                    style={
                                        'font-size': 40
                                    }
                                ),
                                width='auto'
                            )
                        ],
                        justify='center',
                        align='center'
                    ),
                    html.Br(),
                    dbc.Row(
                        children=[
                            dbc.Col(
                                html.Div(
                                    children=[
                                        html.A(
                                            dbc.Button(
                                                'Start Controlling',
                                                color='primary',
                                                size='lg',
                                                className='mr-1'
                                            ),
                                            href=f"http://{settings['ip']}:{settings['ports']['dash']}/control"
                                        )
                                    ]
                                ),
                                width='auto'
                            ),
                            dbc.Col(
                                html.Div(
                                    children=[
                                        html.A(
                                            dbc.Button(
                                                'Show Evaluation',
                                                color='primary',
                                                size='lg',
                                                className='mr-1'
                                            ),
                                            href=f"http://{settings['ip']}:{settings['ports']['dash']}/evaluation"
                                        )
                                    ]
                                ),
                                width='auto'
                            ),
                        ],
                        justify='center',
                        align='center',
                        
                        
                    ),
                    html.Br(),
                    html.Div([
                        dbc.Card(
                            [
                                dbc.FormGroup(
                                    [
                                    
                                        dcc.Dropdown(
                                            id="Ortsauswahl",
                                            options = [{"label":i, "value":i} for i in df["Ortsbezeichnung"].unique()],
                                            placeholder = "Ort auswählen"
                                        ),
                                        
                                        html.Div(id="ortsauswahl_output"),

                                        html.Br(),
                                        dbc.Input(id="Ortsinput", placeholder="Ort hinzufügen", type="text"),
                                        dbc.Button("Submit", id="OrtSub", color='primary', className="mr-1")
                                    ],
                                ),
                            ],
                            body=True,
                        ),
                        
                    ],
                    ),
                        dbc.DropDownMenu(
                            label="Ortsauswahl",
                            bs_size="mb-3",
                            children=items,
                            className="mb-3"
                        ),
                        
                        html.Div(id="ortsauswahl_output")
                    ],
                    ),
                ]
            )
        ],
        style={
            'font-size': 20,
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center',
            'height': '700px'
        }
    )
]
