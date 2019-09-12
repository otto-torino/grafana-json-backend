#!flask/bin/python
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from settings import BASE_PATH, HOST, PORT
from sources.factory import SourceFactory

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
methods = ('GET', 'POST')

# get the source instance
source = SourceFactory.instance()


# Root path /
# just a path called to see if the API is up
# The only requirement is returning a 200 status code.
@app.route(BASE_PATH + '/', methods=methods)
@cross_origin()
def test_connection():
    return source.test()


# Search path /search
# Should return a list of available fields to query.
# Is also called by the autocomplete feature of grafana,
# in such case a target is given:
# {'target': 'digited chars'}
@app.route(BASE_PATH + '/search', methods=methods)
@cross_origin()
def search():
    req = request.get_json()
    target = req.get('target', '*')
    return jsonify(source.search(target))


# Query path /query
# Should return a response for timeseries or table queries
# example of received request
# {'timezone': 'browser', 'panelId': 2, 'dashboardId': 4, 'range': {'from': '2019-09-06T02:29:24.953Z', 'to': '2019-09-06T08:29:24.953Z', 'raw': {'from': 'now-6h', 'to': 'now'}}, 'rangeRaw': {'from': 'now-6h', 'to': 'now'}, 'interval': '20s', 'intervalMs': 20000, 'targets': [{'data': None, 'target': 'mi', 'refId': 'A', 'hide': False, 'type': 'timeseries'}], 'maxDataPoints': 960, 'scopedVars': {'Cippo': {'text': '1m', 'value': '1m'}, '__from': {'text': '1567735232102', 'value': '1567735232102'}, '__to': {'text': '1567756832103', 'value': '1567756832103'}, '__interval': {'text': '20s', 'value': '20s'}, '__interval_ms': {'text': 20000, 'value': 20000}}, 'adhocFilters': []}
@app.route(BASE_PATH + '/query', methods=methods)
@cross_origin()
def query():
    req = request.get_json()
    range = req.get('range', {})
    interval = req.get('intervalMs', 0)
    targets = req.get('targets', [])
    max_data_points = req.get('maxDataPoints', 0)
    scoped_vars = req.get('scopedVars', {})
    filters = req.get('adhocFilters', {})

    return jsonify(source.query(
        range=range,
        interval=interval,
        targets=targets,
        max_data_points=max_data_points,
        scoped_vars=scoped_vars,
        filters=filters,
    ))


@app.route(BASE_PATH + '/annotations', methods=methods)
@cross_origin()
def annotations():
    return jsonify(source.annotations())


if __name__ == '__main__':
    app.run(debug=False, host=HOST, port=PORT)
