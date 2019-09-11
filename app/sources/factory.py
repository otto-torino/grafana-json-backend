from settings import SOURCE
from sources.elasticsearch.source import ElasticSearchSource


class SourceFactory(object):
    def instance():
        if SOURCE == 'es':
            return ElasticSearchSource()
