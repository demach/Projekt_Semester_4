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

    connection = sqlite3.connect(settings["db_path"])
    #print(settings["db_path"])
    df = pd.read_sql('SELECT * from Messwerttabelle', connection)

    connection.close()


    content = [
        html.Div(
            children=[
                Site.create_card_row(
                    f"{' '.join(df.columns[1])} / {' '.join(df.columns[2])} / {' '.join(df.columns[3])}",
                    [
                        Site.create_card("Timestamp", "timestamp-evaluation-card", " ", df["Timestamp"].iloc[-1]),
                        Site.create_card("Messwert", "messwert-evaluation-card", " ", df["Messwert"].iloc[-1]),
                        Site.create_card("Ort_ID", "ort-evaluation-card", " ", df["Ort_ID"].iloc[-1]),
                        Site.create_card("Sensor_ID", "sensor_id-evaluation-card", " ", df["Sensor_ID"].iloc[-1])
                    ]
                ),
                html.Br(),
                html.Div(
                    children=create_figure(True, True, True),
                    id="plot-div"
                ),
                dbc.Col(
                    html.Div(
                        children = [
                            create_checkbox("messwert-checkbox", "Messwert", True)
                        ]
                    ),
                    width = "auto"
                ),
                dbc.Col(
                    html.Div(
                        children = [
                            create_checkbox("ort-checkbox", "Ort", True)
                        ]
                    ),
                    width = "auto"
                ),
                dbc.Col(
                    html.Div(
                        children = [
                            create_checkbox("sensor-checkbox", "Sensor", True)
                        ]
                    ),
                    width = "auto"
                ),
                dbc.Col(
                    html.Div(
                        children = [
                            dbc.Button(
                                "SHOW ALL", 
                                color="secondary", 
                                className="mr-1",
                                id = "show-all-button"
                            )
                        ]
                    ),
                    width = "auto"
                )
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

    figure_list = args

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

    if figure_list[0]:
        create_trace("Messwert")
    if figure_list[1]:
        create_trace("Sensor_ID")
    if figure_list[2]:
        create_trace("Ort_ID")

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
