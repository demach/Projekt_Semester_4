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

    connection = sqlite3.connect("E://Programmin//Datenbank.db")

    df = pd.read_sql('SELECT * from ALLE_DATEN', connection)
    df = df.rename(columns={"Zeitstempel": "Timestamp"})

    content = [
        html.Div(
            children=[
                Site.create_card_row(
                    f"{'MAX '.join(df.columns[1])} / {'MAX '.join(df.columns[2])}",
                    [
                        Site.create_card("Beleuchtung", "beleuchtung-evaluation-card", " ", df["Beleuchtung"].max()),
                        Site.create_card("Temperatur", "temperatur-evaluation-card", " ", df["Temperatur"].max()),
                    ]
                ),
                html.Br(),
                html.Div(
                    dash_table.DataTable(data=df.to_dict('records'), columns=[{"name": i, "id": i} for i in df.columns]),
                    id="database"
                ),
                html.Br(),
            ]
        )
    ]
