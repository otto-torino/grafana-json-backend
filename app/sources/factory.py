from settings import SOURCE
from sources.elasticsearch.source import ElasticSearchSource


class SourceFactory(object):
    """ Factory pattern
        Returns a real source class basing upon a config parameter
    """
    def instance():
        if SOURCE == 'es':
            return ElasticSearchSource()
