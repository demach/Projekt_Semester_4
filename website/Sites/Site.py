import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import json

# open setting file
with open('settings.json', 'r') as rd:
    settings = json.loads(rd.read())


# load general and specific settings for different sites
def load_settings(name):
    selected = settings['GENERAL']
    if name in settings:
        for key in settings[name]:
            selected[key] = settings[name][key]
    return selected

control = settings["CONTROL"]['intervall']

def create_app(name, content):
    settings = load_settings(name)
    app = dash.Dash(__name__)
    link = f"http://{settings['ip']}:{settings['ports']['dash']}"
    app.title = settings['name']
    app.layout = dbc.Container(
        [

       
            html.Div(
            id="main-div",
            children=[
                dcc.Location(id='url', refresh=False),
                dbc.NavbarSimple(
                    children=[
                        dbc.NavItem(dbc.NavLink('HOME', href=f"{link}/home")),
                        dbc.NavItem(dbc.NavLink('EVALUATION', href=f"{link}/evaluation")),
                        dbc.NavItem(dbc.NavLink('MEASUREMENT', href=f"{link}/measurement")),
                        #dbc.NavItem(dbc.NavLink('CONTROL', href=f"{link}/control")),

                    ],
                    brand=settings['name'],
                    brand_href=f"{link}/home",
                    color='primary',
                    dark=True
                ),
                html.Div(
                    id='content-div',
                    children=content,
                    
                ),
                html.Div(id="test", style={'display': 'none'})
            ]
            ),
            dcc.Interval(
                id="interval",
                interval=control,
                n_intervals=0
            )
        ]
    )
    return app


# this function creates a card for showing a value
def create_card(header, id, unit, default=None):
    card_font_big = 50
    card_font_small = 20

    if not default:
        default = '0'

    return dbc.Card(
        children=[
            dbc.CardHeader(header),
            dbc.CardBody(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                id=id,
                                children=[default],
                                style={'font-size': card_font_big}
                            ),
                            html.Div(
                                children=[unit],
                                style={'font-size': card_font_small}
                            )
                        ],
                        style={
                            'display': 'flex',
                            'justify-content': 'center',
                            'align-items': 'center'
                        }
                    )
                ]
            )
        ],
        color='primary',
        inverse=True
    )


# this function can create a row out of a list of cards
def create_card_row(header, cards):
    card_cols = []

    for card in cards:
        card_col = dbc.Col(
            html.Div(
                children=[card]
            )
        )
        card_cols.append(card_col)

    return html.Div(
        children=[
            html.Br(),
            html.Div(
                children=[header],
                style={
                    'font-size': 30,
                    'text-align': 'center'
                }
            ),
            html.Hr(
                style={
                    'border': '2px solid',
                    'width': '90%',
                    'color': '#060606'
                }
            ),
            html.Div(
                children=[
                    dbc.Row(children=card_cols)
                ],
                style={
                    'width': '90%',
                    'margin': 'auto'
                }
            )
        ]
    )


def page_not_found():
    return html.Div(
        children=[
            html.Div(
                children=['OOPS!'],
                style={'font-size': 75}
            ),
            html.Br(),
            html.Div(
                children=[
                    """SOMETHING JUST GOT MESSED UP
                    ERROR 404 PAGE NOT FOUND"""
                ]
            )
        ],
        style={
            'font-size': 25,
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center',
            'height': '700px'
        }
    )


def error_msg(msg):
    return html.Div(
        children=[
            html.Div(
                children=['ERROR'],
                style={'font-size': 75}
            ),
            html.Br(),
            html.Div(
                children=[msg]
            )
        ],
        style={
            'font-size': 25,
            'display': 'flex',
            'justify-center': 'center',
            'align-items': 'center',
            'height': '700px'
        }
    )
