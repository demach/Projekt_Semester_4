from . import Site
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output

name = __name__.split('.')[1]
settings = Site.load_settings(name)

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
                        dcc.Dropdown(
                            id="ortsauswahl",
                            options = [
                                {"label":"Valeo", "value":"Valeo"},
                                {"label":"Kuka", "value":"Kuka"},
                                {"label":"SPN", "value":"SPN"},
                            ],
                            value="Valeo"
                        ),
                        
                        html.Div(id="ortsauswahl_output")
                    ],
                    ),
                ]
            )
        ],
        style={
            'font-size': 50,
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center',
            'height': '700px'
        }
    )
]
