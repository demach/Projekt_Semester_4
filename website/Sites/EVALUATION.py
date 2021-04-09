from . import Site
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import sqlite3
import dash_daq as daq
import plotly.graph_objects as go

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
    global content, data

    connection = sqlite3.connect("E://Programmin//Datenbank.db")
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]


    table=["Timestamp", "Beleuchtung", "Temperatur"]
    data = {"Timestamp": [], "Temperatur": [], "Beleuchtung": []}
    dbdata = list(cursor.execute("""select * from ALLE_DATEN"""))
    for result in dbdata:
        data["Timestamp"].append(result[1])
        data["Beleuchtung"].append(result[2])
        data["Temperatur"].append(result[3])

    content = [
        html.Div(
            children=[
                Site.create_card_row(
                    f"{' '.join(table[1])} / {' '.join(table[2])}",
                    [
                        Site.create_card("Timestamp", "timestamp-evaluation-card", " ", data["Timestamp"][-1]),
                        Site.create_card("Beleuchtung", "beleuchtung-evaluation-card", " ", data["Beleuchtung"][-1]),
                        Site.create_card("Temperatur", "temperatur-evaluation-card", " ", data["Temperatur"][-1]),
                    ]
                ),
                html.Br(),
                html.Div(
                    children=create_figure(True, True),
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
def create_figure(beleuchtung, temperatur):
    global c
    c = 0
    fig = go.Figure()

    def create_trace(key):
        global c
        fig.add_trace(
            go.Scatter(
                x=data["Timestamp"],
                y=data[key],
                name=key,
                mode="lines+markers",
                line=dict(color=colors[c])
            )
        )
        c += 1

    if beleuchtung:
        create_trace("Beleuchtung")
    if temperatur:
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
