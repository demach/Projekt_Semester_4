from . import Site
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from paho.mqtt import client as mqtt_client

name = __name__.split(".")[1]
settings = Site.load_settings(name)

def create_slider(id, text, default, minimum, maximum, steps):
    return dcc.Slider(
            id=id,
            min=minimum,
            max=maximum,
            step=steps,
            value=default,
            )

def create_button(id, text):
    return html.Div(
            dbc.Button(
                children=text,
                id=id,
                color='primary',
                size='lg',
                className='mr-1',
            ),
            style={"width":"400px"}
        )   



def create_content(table=None):
    global content

    content = [
        html.Div(
            children=[
                html.Br(),
                html.Br(),
                dbc.Col(
                    html.Div("red"),
                    width="auto",
                    align='center'
                ),
                dbc.Col(
                    html.Div(
                        children=[
                            
                            create_slider("slider_red", "Rot-Wert", 0, 0, 255, 1)
                        ]
                    ),
                    width="auto",
                ),
                html.Br(),
                html.Br(),
                dbc.Col(
                    html.Div("green"),
                    width="auto",
                    align='center'
                ),
                dbc.Col(
                    html.Div(
                        children=[
                            
                            create_slider("slider_green", "Gruen-Wert", 0, 0, 255, 1)
                        ]
                    ),
                    width="auto"
                ),
                html.Br(),
                html.Br(),
                dbc.Col(
                    html.Div("blue"),
                    width="auto",
                    align='center'
                ),
                
                dbc.Col(
                    html.Div(
                        children=[
                            
                            create_slider("slider_blue", "Blau-Wert", 0, 0, 255, 1)
                        ]
                    ),
                    width="auto"
                ),
                dbc.Col(
                    html.Div(id='slider_output'),
                ),
                html.Br(),
                html.Br(),
                dbc.Col(
                        children=[
                            Site.create_card_row(
                                f"Hello",
                                [
                                    create_button("button_blue", "Blau"),
                                    create_button("button_red", "Rot"),
                                    create_button("button_green", "Gruen"),
                                    html.Div(id="button_output"), 
                                ]
                                )
                        ]
                ),
            ]
        ),
        
    ]
