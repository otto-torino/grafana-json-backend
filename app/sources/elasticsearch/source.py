from elasticsearch import Elasticsearch
from sources.abstract import AbstractSource
from sources.elasticsearch.targets.categories_cnt import categories_cnt
from sources.elasticsearch.targets.categories_timeline import categories_timeline
from sources.elasticsearch.targets.documents_raw import documents_raw
from settings import ES_HOST, ES_PORT, ES_USERNAME, ES_SECRET

# Map grafana variables to elasticsearch query_string terms
var_field_map = {
    'languages': 'language:({1})',
    'country': '{0}.name:({1})',
    'categories': '{0}:({1})',
    'organizations': '{0}:({1})',
    'people': 'persons:({1})',
    'profiling': '{0}.type:({1})',
    'deep_profiling': '{0}.type:({1})',
    'full_text': '(ft_body:{1}~) OR (ft_title:{1}~)'
}


class ElasticSearchSource(AbstractSource):
    """ Implementation of AbstractSource for elastic search source """

    def __init__(self):
        self.es = Elasticsearch(
            [ES_HOST],
            http_auth=(str(ES_USERNAME), str(ES_SECRET)),
            port=ES_PORT,
            use_ssl=False,
        )

    def test(self, target=None):
        return 'Grafana API ES source ready'

    # should return the available fields
    def search(self, target=None):
        return [
            'categories_cnt',
            'categories_timeline',
            'documents_raw',
        ]

    # should return the query result
    def query(self,
              range=[],
              interval=0,
              targets=[],
              max_data_points=0,
              scoped_vars={},
              filters={}):
        from_date = int(scoped_vars.get('__from').get('value'))
        to_date = int(scoped_vars.get('__to').get('value'))
        query_parts = []
        for var in scoped_vars:
            # wont consider from, to , etc...
            if not var.startswith('__'):
                value = scoped_vars.get(var).get('value')
                if value:
                    # if a list of values, concatenate as OR
                    if isinstance(value, list):
                        val = ' OR '.join(['"%s"' % v for v in value])
                    elif isinstance(value, str):
                        val = '"%s"' % value
                    else:
                        val = value
                    p = var_field_map.get(var).format(var, val)
                    query_parts.append(p)
        query_string = {
            'analyze_wildcard': True,
            'query': ' AND '.join(query_parts)
        }
        # every field returned by the search method is a target
        # targets' query implementation is splitted in target files under
        # the targets directory
        if targets[0].get('target') == 'categories_cnt':
            return categories_cnt(self.es, from_date, to_date, query_string)
        if targets[0].get('target') == 'categories_timeline':
            return categories_timeline(self.es, from_date, to_date, interval, query_string)
        if targets[0].get('target') == 'documents_raw':
            return documents_raw(self.es, from_date, to_date, query_string)
