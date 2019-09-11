# ElasticSearch Source


## Query

Example of query used to retrieve a timeseries of number of documents aggregated by category and date interval of one day

    {
      "size": 0,
      "query": {
        "bool": {
          "filter": [
            {
              "range": {
                "date": {
                  "gte": "1552302780902",
                  "lte": "1568196780902",
                  "format": "epoch_millis"
                }
              }
            },
            {
              "query_string": {
                "analyze_wildcard": true,
                "query": "categories:(\"01000000\" OR \"01001000\" OR \"01001001\" OR \"01001003\" OR \"01002000\" OR \"01003000\" OR \"01004000\" OR \"01005000\" OR \"01006000\" OR \"01007000\" OR \"01008000\" OR \"01008001\" OR \"01008002\" OR \"01014000\" OR \"01014003\" OR \"01019000\" OR \"02000000\" OR \"02001000\" OR \"02001001\" OR \"02001003\" OR \"02002000\" OR \"02002001\" OR \"02002002\" OR \"02002003\" OR \"03000000\" OR \"03001000\" OR \"03001002\" OR \"03002000\" OR \"03002001\" OR \"03002002\" OR \"03002004\" OR \"03002006\" OR \"03003000\" OR \"03003001\" OR \"03003002\" OR \"03003003\" OR \"03003004\" OR \"03003006\" OR \"03003007\" OR \"03003008\" OR \"03003009\" OR \"03003010\" OR \"03003011\" OR \"03003012\" OR \"03003014\" OR \"03003016\" OR \"03004000\" OR \"03004001\" OR \"03004002\" OR \"03006000\" OR \"03008000\" OR \"03009000\" OR \"03010000\" OR \"03011000\" OR \"04000000\" OR \"04001000\" OR \"04001001\" OR \"04001002\" OR \"04001003\" OR \"04001004\" OR \"04001005\" OR \"04001006\" OR \"04002000\" OR \"04002001\" OR \"04002002\" OR \"04002003\" OR \"04002004\" OR \"04003000\" OR \"04003001\" OR \"04003003\" OR \"04003004\" OR \"04003005\" OR \"04004000\" OR \"04004001\" OR \"04004002\" OR \"04004003\" OR \"04004004\" OR \"04005000\" OR \"04006000\" OR \"05000000\" OR \"05004000\" OR \"05005000\" OR \"05006000\" OR \"05007000\" OR \"05007001\" OR \"05007003\" OR \"05007004\" OR \"05008000\" OR \"06000000\") AND organizations:(\"\\<NONE\\>\") AND persons:(\"\\<NONE\\>\") AND profiling.type:(\"\\-1\") AND deep_profiling.type:(\"\\-1\") AND ((ft_body:\"\"~) OR (ft_title:\"\"~))"
              }
            }
          ]
        }
      },
      "aggs": {
        "3": {
          "terms": {
            "field": "categories",
            "size": 20,
            "order": {
              "_count": "desc"
            },
            "min_doc_count": 1
          },
          "aggs": {
            "2": {
              "date_histogram": {
                "interval": "1d",
                "field": "date",
                "min_doc_count": 1,
                "extended_bounds": {
                  "min": "1552302780902",
                  "max": "1568196780902"
                },
                "format": "epoch_millis"
              },
              "aggs": {}
            }
          }
        }
      }
    }


## Responses

Example of a timeseries response


    return [
        {
            "target":
            "10000001",  # The field being queried for
            "datapoints": [
                [622, 1567771201000],  # Metric value as a float , unixtimestamp in milliseconds
                [365, 1567760209000]
            ]
        },
        {
            "target": "10000002",
            "datapoints": [[622, 1567471251000], [365, 1567760209000]]
        }
    ]

Example of a table response:

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
