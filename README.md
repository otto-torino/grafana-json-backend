# Grafana JSON Plugin API Implementation

This is a python implementation of the backend needed by the [JSON grafana plugin](https://grafana.com/grafana/plugins/simpod-json-datasource).

## API

It uses flask to implement a JSON API. The following routes are served, (see `app.py`):

### `/`

This is just for testing purposes, grafana call it when testing the data source to see if it's up and running.

### `/search`

This endpoint returns a list of available fields. It gets a `target` parameter which contains the characters digited 
by the user when filtering the dropdown input.

### `/query`

This endpoint returns the actual query result, could be a timeseries set of data or a table set of data.
It receives the following json:


    # example of received request
    {
        'timezone': 'browser',
        'panelId': 2,
        'dashboardId': 4,
        'range': {
            'from': '2019-09-06T02:29:24.953Z',
            'to': '2019-09-06T08:29:24.953Z',
            'raw': {'from': 'now-6h', 'to': 'now'}
        },
        'rangeRaw': {'from': 'now-6h', 'to': 'now'},
        'interval': '20s',
        'intervalMs': 20000,
        'targets': [
            {'data': None, 'target': 'mi', 'refId': 'A', 'hide': False, 'type': 'timeseries'}
        ],
        'maxDataPoints': 960,
        'scopedVars': {'Cippo': {'text': '1m', 'value': '1m'},
        '__from': {'text': '1567735232102', 'value': '1567735232102'},
        '__to': {'text': '1567756832103', 'value': '1567756832103'},
        '__interval': {'text': '20s', 'value': '20s'},
        '__interval_ms': {'text': 20000, 'value': 20000}},
        'adhocFilters': []
    }

### `/annotations`

TBD


## Sources

The application architecture provides a simple way to connect new sources to the API interface.
The API interface calls a Source Factory (`sources/factory.py`) to retrieve an instance of a real source class, such instance depends on a setting configuration (now, in the future could depend on a part of the url).

Every source class should inherit from an `AbstractSource` class (`sources/abstract.py`) which defines the class interface.
Every source class should implement the following methods:

- `(string) test ()`
- `(list) search (target:string)`
- `(dict) query (range:array, interval:int, targets:array, max_data_points:int, scoped_vars:dict, filters:dict)`

In order to add a new source, just create a new class defining such methods, tweak the source factory class to return the right class basing on the `SOURCE` setting.
