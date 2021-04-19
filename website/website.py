import Sites
import flask
import json
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_html_components as html
import traceback
import backend_website
# load settings from file
with open('settings.json', 'r') as rd:
    settings = json.loads(rd.read())

mqtt_broker = settings['GENERAL']['mqtt_broker']
mqtt_port = settings['GENERAL']['ports']['mqtt']
print(mqtt_broker, mqtt_port)

# creating empty site with header
app = Sites.Site.create_app(settings['GENERAL']['name'], [None])

client = backend_website.connect_mqtt(mqtt_broker, mqtt_port)

@app.callback(
    [Output("content-div", "children")],
    [Input("url", "pathname")]
)
def update_page(url):
    if url:
        url = str(url)
        url_list = url.split("/")
        not_found = Sites.Site.page_not_found()

        if url == "/" or url == "/home":
            return Sites.HOME.content

        elif url_list[1] == "evaluation":
            if not len(url_list) > 3:
                try:
                    if len(url_list) == 2:
                        measurement = None
                    else:
                        measurement = url_list[2]
                    Sites.EVALUATION.create_content(measurement)
                    return Sites.EVALUATION.content
                except Exception as e:
                    traceback.print_exc()
                    return [not_found]

        elif url_list[1] == "measurement":
            if not len(url_list) > 3:
                try:
                    if len(url_list) == 2:
                        measurement = None
                    else:
                        measurement = url_list[2]
                    Sites.MEASUREMENT.create_content(measurement)
                    return Sites.MEASUREMENT.content
                except Exception as e:
                    traceback.print_exc()
                    return [not_found]
       
        elif url_list[1] == "control":
            if not len(url_list) > 3:
                try:
                    if len(url_list) == 2:
                        measurement = None
                    else:
                        measurement = url_list[2]
                    Sites.CONTROL.create_content(measurement)
                    return Sites.CONTROL.content
                except Exception as e:
                    traceback.print_exc()
                    return [not_found]

#this callback updates the plot on evaluation page
@app.callback(
    [Output("plot-div", "children")],
    [Input("beleuchtung-checkbox", "checked"),
    Input("temperatur-checkbox", "checked"),]
)
def callback05(beleuchtung_check, temperatur_check):
    return Sites.EVALUATION.create_figure(beleuchtung_check, temperatur_check)


#this callback updates selection for plot if show-all button is triggered
@app.callback(
    [Output("beleuchtung-checkbox", "checked"),
    Output("temperatur-checkbox", "checked")],
    [Input("show-all-button", "n_clicks")]
)
def callback06(n_clicks):
    if n_clicks:
        return True, True
    else:
        raise PreventUpdate


#this callback is responsible for the slider on the control page
@app.callback(
    [Output("slider_output", "children")],
    [Input('slider_red', 'value'),
    Input('slider_green', 'value'),
    Input('slider_blue', 'value')]
)
def callback07(value_red, value_green, value_blue):
    if not client.is_connected:
        client.connect(mqtt_broker, mqtt_port)
    payload ={"red": value_red, "green": value_green, "blue": value_blue}
    backend_website.publish(client, json.dumps(payload), "projekt4/rgb_value")
    return [f"You have selected {value_red} for red, {value_green} for green and {value_blue} for blue."] 

app.config['suppress_callback_exceptions'] = True


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=settings["GENERAL"]["ports"]["dash"])
