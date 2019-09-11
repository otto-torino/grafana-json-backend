from elasticsearch import Elasticsearch
from sources.abstract import AbstractSource
from sources.elasticsearch.targets.categories_cnt import categories_cnt

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
    def __init__(self):
        self.es = Elasticsearch(hosts=[{"host": "localhost", "port": 9200}])

    def test(self, target=None):
        return 'Grafana API ES source ready'

    def search(self, target=None):
        return [
            'categories_cnt',
        ]

    def query(self,
              range=[],
              interval=0,
              targets=[],
              max_data_points=0,
              scoped_vars={},
              filters={}):
        from_date = scoped_vars.get('__from').get('value')
        to_date = scoped_vars.get('__to').get('value')
        query_parts = []
        for var in scoped_vars:
            if not var.startswith('__'):
                print(var)
                print(scoped_vars.get('profiling'))
                value = scoped_vars.get(var).get('value')
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
        if targets[0].get('target') == 'categories_cnt':
            return categories_cnt(self.es, from_date, to_date, query_string)
