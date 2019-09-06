from sources.abstract import AbstractSource


class ElasticSearchSource(AbstractSource):
    def test(self, target=None):
        return 'Grafana API ES source ready'

    def search(self, target=None):
        return ['field1', 'field2', 'field3']

    def query(self,
              range=[],
              interval=0,
              targets=[],
              max_data_points=0,
              scoped_vars={},
              filters={}):
        return [
          {
            "target": "upper_75", # The field being queried for
            "datapoints": [
              [622, 1567771201000],  # Metric value as a float , unixtimestamp in milliseconds
              [365, 1567760209000]
            ]
          },
          {
            "target": "upper_90",
            "datapoints": [
              [861, 1567471251000],
              [767, 1567760209000]
            ]
          }
        ]
        # target = req.get('target', '*')
        return [{
            "columns": [{
                "text": "Time",
                "type": "time"
            }, {
                "text": "Country",
                "type": "string"
            }, {
                "text": "Number",
                "type": "number"
            }],
            "rows": [[1234567, "SE", 123], [1234567, "DE", 231],
                     [1234567, "US", 321]],
            "type":
            "table"
        }]
