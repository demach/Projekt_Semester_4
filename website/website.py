import Sites
import flask
import json
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_html_components as html
import traceback

# load settings from file
with open('settings.json', 'r') as rd:
    settings = json.loads(rd.read())

# creating empty site with header
app = Sites.Site.create_app(settings['GENERAL']['name'], [None])


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

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=settings["GENERAL"]["ports"]["dash"])
