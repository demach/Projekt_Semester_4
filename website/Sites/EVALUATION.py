from . import Site
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
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

    connection.close()

    df = df.rename(columns={"Zeitstempel": "Timestamp"})

    content = [
        html.Div(
            children=[
                Site.create_card_row(
                    f"{' '.join(df.columns[1])} / {' '.join(df.columns[2])}",
                    [
                        Site.create_card("Timestamp", "timestamp-evaluation-card", " ", df["Timestamp"].iloc[-1]),
                        Site.create_card("Beleuchtung", "beleuchtung-evaluation-card", " ", df["Beleuchtung"].iloc[-1]),
                        Site.create_card("Temperatur", "temperatur-evaluation-card", " ", df["Temperatur"].iloc[-1]),
                    ]
                ),
                html.Br(),
                html.Div(
                    children=create_figure("Beleuchtung", "Temperatur"),
                    id="plot-div"
                ),
            ]
        )
    ]


# colors for traces in plots
colors = ["rgb(0,0,0)", "rgb(100,25500,100)", "rgb(175,175,175)"]

# standard axis layout for graphs
axis_layout = dict(
    showline=True,
    showgrid=True,
    showticklabels=True,
    linewidth=3,
    ticks='outside',
    linecolor='rgb(0,0,0)',
    mirror=True
)


# function for creating graphs on evaluation page
def create_figure(*args, **kwargs):
    global c

    figure_list = [item for item in args]

    c = 0
    fig = go.Figure()

    def create_trace(key):
        
        global c
        fig.add_trace(
            go.Scatter(
                x=df["Timestamp"],
                y=df[key],
                name=key,
                mode="lines+markers",
                line=dict(color=colors[c])
            )
        )
        c += 1

    if "Beleuchtung" in figure_list:
        create_trace("Beleuchtung")
    if "Temperatur" in figure_list:
        create_trace("Temperatur")

    fig.update_layout(
        xaxis=axis_layout,
        yaxis=axis_layout,
        plot_bgcolor='rgb(235,235,235)',
        showlegend=True,
        legend_orientation='h',
        title={
            "text": "P L O T S",
            'x': 0.5,
            "xanchor": "center",
            "font": {"size": 25}
        },
        xaxis_title="Runtime",
        height=1000
    )

    return [dcc.Graph(figure=fig)]