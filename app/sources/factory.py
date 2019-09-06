from settings import SOURCE
from sources.es import ElasticSearchSource


class SourceFactory(object):
    def instance():
        if SOURCE == 'es':
            return ElasticSearchSource()
