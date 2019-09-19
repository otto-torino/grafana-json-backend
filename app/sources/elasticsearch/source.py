import json
import os

from elasticsearch import Elasticsearch
from settings import ES_HOST, ES_INDEX, ES_PORT, ES_SECRET, ES_USERNAME
from sources.abstract import AbstractSource
from sources.elasticsearch.targets.categories_cnt import categories_cnt
from sources.elasticsearch.targets.categories_timeline import \
    categories_timeline
from sources.elasticsearch.targets.documents_raw import documents_raw
from sources.elasticsearch.targets.documents_tot import documents_tot

# load categories map from a json
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'categories.json')) as f:
    categories_dict = json.load(f)

with open(os.path.join(dir_path, 'categories_inv.json')) as f:
    categories_inv_dict = json.load(f)

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
        if target:
            t = json.loads(target)
            if t.get('variable', None) == 'categories':
                return self.get_categories_list()

        return [
            'categories_cnt',
            'categories_timeline',
            'documents_tot',
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
                        if var == 'categories':
                            val = ' OR '.join([
                                '"%s"' % categories_inv_dict.get(v)
                                for v in value
                            ])
                        else:
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
            return categories_cnt(self.es, categories_dict, from_date, to_date,
                                  query_string)
        if targets[0].get('target') == 'categories_timeline':
            return categories_timeline(self.es, categories_dict, from_date,
                                       to_date, interval, query_string)
        if targets[0].get('target') == 'documents_tot':
            return documents_tot(self.es, from_date, to_date, query_string)
        if targets[0].get('target') == 'documents_raw':
            return documents_raw(self.es, categories_dict, from_date, to_date,
                                 query_string)

    def get_categories_list(self):
        result = []
        res = self.es.search(
            index=ES_INDEX,
            body={
                "size": 0,
                "aggs": {
                    "categories": {
                        "terms": {
                            "field": "categories",
                            "size": 500,
                            "order": {
                                "_key": "asc"
                            }
                        }
                    }
                }
            })

        for b in res.get('aggregations').get('categories').get('buckets'):
            result.append(categories_dict.get(b.get('key')))
        return result
