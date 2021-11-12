
Fielddata is disabled on text fields by default. 
Set fielddata=true on [bug_author_name] in order to load fielddata in memory by uninverting the inverted index. 
Note that this can however use significant memory. Alternatively use a keyword field instead.

https://kalasearch.cn/community/tutorials/elasticsearch-fielddata-is-disabled-on-text-fields-error/



解决es 单节点状态下，状态为yellow的问题

Elasticsearch采用默认配置（5分片，1副本），但实际只部署了单节点集群。
index.number_of_shards：5
index.number_of_replicas：1


PUT http://192.168.1.156:9200/mew*/_settings
Content-Type: application/json


{
  "number_of_replicas": 0
}

参考： https://blog.csdn.net/laoyang360/article/details/81271491
