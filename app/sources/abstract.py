from abc import ABCMeta, abstractmethod

import six


@six.add_metaclass(ABCMeta)
class AbstractSource(object):
    """ Abstract class from which all sources inherits 
        It defines an interface for sources classes
    """
    @abstractmethod
    def test(self):
        raise NotImplementedError(
            'Source instance should define a test method')

    @abstractmethod
    def search(self, target=None):
        raise NotImplementedError(
            'Source instance should define a search method')

    @abstractmethod
    def query(self,
              range=[],
              interval=0,
              targets=[],
              max_data_points=0,
              scoped_vars={},
              filters={}):
        raise NotImplementedError(
            'Source instance should define a query method')
