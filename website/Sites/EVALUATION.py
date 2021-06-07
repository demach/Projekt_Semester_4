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

    df = df.rename(columns={"Sensor_ID": "Sensor"})
    df = df.rename(columns={"Ort_ID": "Ort"})

    letzter_ort = df["Ort"].iloc[-1]
    # print(letzter_ort)

    content = [
        html.Div(
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            children=[
                                html.Div(
                                    children=[
                                        html.Br(),
                                        dbc.Tabs(
                                            generate_tabs(),           
                                            id="tabs",
                                            active_tab=letzter_ort,
                                        ),
                                        
                                    ]
                                ),
                                
                            ]
                                
                        ),
                        dbc.Col(
                            children=[
                                html.Br(),
                                daq.ToggleSwitch(
                                    id='toggle_interval',
                                    value=True,
                                    label="Toggle Auto-Update",
                                    labelPosition="bottom",
                                    color="#34eb37"
                                ),
                                
                            ]
                        )
                    ]
                ),
                html.Div(id="tab-content", className="p-4"),
            ]
        )
    ]


# colors for traces in plots
colors = ["rgb(0,0,0)", "rgb(0,255,100)", "rgb(255,0,10)"]

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

def generate_tabs():
    tabs = []
    for i in df["Ort"].unique():
        tabs.append(dbc.Tab(label=i, tab_id=i))
    return tabs

# function for creating graphs on evaluation page
def create_figure(*args, **kwargs):
    global c

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

    df = df.rename(columns={"Sensor_ID": "Sensor"})
    df = df.rename(columns={"Ort_ID": "Ort"})

    letzter_ort = df["Ort"].iloc[-1]


    figure_list = args

    c = 0
    fig = go.Figure()

    def create_trace(keys):
        # data_y = []
        # print(keys)
        data = df.loc[(df["Ort"] == keys[0]) & (df["Sensor"] == keys[1]), ["Timestamp", "Messwert"]]
        # print(df.loc[(df["Ort"] == keys[0]), "Messwert"])
        # print(data)

        global c
        fig.add_trace(
            go.Scatter(
                x=data["Timestamp"],
                y=data["Messwert"],
                name=keys[1],
                mode="lines+markers",
                line=dict(color=colors[c])
            )
        )
        c += 1

    for i in df["Sensor"].unique():
        # print(i)
        create_trace([figure_list[0], i])


    fig.update_layout(
        xaxis=axis_layout,
        yaxis=axis_layout,
        plot_bgcolor='rgb(235,235,235)',
        showlegend=True,
        legend_orientation='h',
        title={
            "text": "M E S S W E R T E",
            'x': 0.5,
            "xanchor": "center",
            "font": {"size": 25}
        },
        xaxis_title="Runtime",
        height=750
    )

    return [dcc.Graph(figure=fig)]

