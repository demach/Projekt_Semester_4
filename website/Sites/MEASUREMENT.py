from . import Site
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_table
import sqlite3
import dash_daq as daq
import plotly.graph_objects as go
import pandas as pd

name = __name__.split(".")[1]
settings = Site.load_settings(name)


def create_checkbox(id, text, default):
    return dbc.FormGroup(
        children=[
            dbc.Checkbox(
                id=id,
                className="custom-control-input",
                checked=default
            ),
            dbc.Label(
                children=text,
                html_for=id,
                className="custom-control-label"
            ),
        ],
        check=True,
        className="custom-control custom-checkbox"
    )


def create_content(table=None):
    global content, df

    connection = sqlite3.connect(settings["db_path"])

    df = pd.read_sql('SELECT * from Messwerttabelle', connection)
    df_orte = pd.read_sql('SELECT * from Orte', connection)
    df_sensoren = pd.read_sql('SELECT * from Sensoren', connection)
    
    orte_dict = df_orte.to_dict()
    sensoren_dict = df_sensoren.to_dict()
    sensoren = [i for i in sensoren_dict["Sensorname"].values()]
    sensoren_id = [i for i in sensoren_dict["Sensoren_ID"].values()]

    orte = [i for i in orte_dict["Ortsbezeichnung"].values()]
    orte_id = [i for i in orte_dict["Ort_ID"].values()]


    orte_dict = dict(zip(orte_id,orte))
    sensoren_dict = dict(zip(sensoren_id, sensoren))
    

    df.replace({"Sensor_ID": sensoren_dict}, inplace=True)
    df.replace({"Ort_ID": orte_dict}, inplace=True)

    content = [
        html.Div(
            children=[
                Site.create_card_row(
                    f"Min./Max. \n {' '.join(df.columns[1])}/{' '.join(df.columns[2])}/{' '.join(df.columns[3])}",
                    [
                        Site.create_card("letzter Sensor", "sensor-evaluation-card", " ", f"{df['Sensor_ID'].iloc[-1]}"),
                        Site.create_card("letzter Ort", "ort-evaluation-card", " ", f"{df['Ort_ID'].iloc[-1]}"),
                    ]
                ),
                html.Br(),
                html.Div(
                    create_table(df),
                    id="database"
                ),
                html.Br(),
            ]
        )
    ]

def create_table(data):
    return dash_table.DataTable(
        data=data.to_dict('records'), 
        columns=[{"name": i, "id": i} for i in data.columns],
        sort_action="native",
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{Temperatur} > 18 && {Temperatur} < 25',
                    'column_id': 'Temperatur',
                },
                'backgroundColor': '#A9F5A9',
                'color': 'black'
            },

            {
                'if': {
                    'filter_query': '{Humidity} > 19 && {Humidity} < 41',
                    'column_id': 'Humidity'
                },
                'backgroundColor': 'tomato',
                'color': 'white'
            },
            {
                'if': {
                    'filter_query': '{CO2_Gehalt} > 2000',
                    'column_id': 'CO2Gehalt'
                },
                'backgroundColor': '#FF0000',
                'color': 'white'
            },

            

            {
                'if': {
                    'state': 'active'  # 'active' | 'selected'
                },
            'backgroundColor': 'rgba(0, 116, 217, 0.3)',
            'border': '1px solid rgb(0, 116, 217)'
            }

        ]
    )
