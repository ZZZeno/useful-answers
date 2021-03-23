from elasticsearch import Elasticsearch
import json
ES_ADDR_ONLINE = ["127.0.0.1:9200"]
es = Elasticsearch(ES_ADDR_ONLINE)

query = [
    {'match': {"task_id": "c50c1276cfad11ea87d1246e968b8880"}},
]  # normal query
doc = {
    "size": 10000,
    'query': {
        'bool': {
            'must': query,
            # 'filter': filter_querys,
        }
    }
}
INDEX = "keep_scan_bug"
res = es.search(index=INDEX, body=doc)
print(json.dumps(res))

# query with aggregation
# equals  group by file_name union all group by rule_category
aggr_query = {
    "query": {
        "bool": {"must": query}
    },
    "aggs": {
        "file_name_count": {
            "terms": {
                "field": "file_name",
            }
        },
        "rule_category_count": {
            "terms": {
                "field": "rule_category",
            }
        }
    }
}

res = es.search(index=INDEX, body=aggr_query)
print(json.dumps(res))

# equals group by file_name, rule_name
aggr_query_group_by_many = {
    "query": {
        "bool": {"must": query}
    },
    "aggs": {
        "group_by_file_name": {
            "terms": {
                "field": "file_name",
            },
            "aggs": {
                "group_by_rule_name": {
                    "terms": {
                        "field": "rule_name"
                    }
                }
            }
        }
    }
}
res = es.search(index=INDEX, body=aggr_query_group_by_many)
print(json.dumps(res))
