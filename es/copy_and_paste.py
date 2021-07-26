import elasticsearch
import json


class ESSearchOptionError(Exception):
    pass


class ESSearchOption:
    _equal_map = {}
    _not_equal_map = {}
    _aggr_with_set = set()
    _keyword_mark_set = set()
    _remove_mark_set = set()

    _page_size = 1000

    def __init__(self):
        pass

    def search_count(self, ps: int):
        self._page_size = ps

    def with_equal(self, params: dict):
        '''
        查询条件，下面的例子表示查询task_id=a且author=zeno的结果，
        该方法可以多次调用，多次调用的结果会整合在一起，形成一个大的
        检索条件，各检索条件之间的关系是逻辑与，相当于 &&
        当一个key多次传入时，以最后一次传入的值为准
        eauql({"task_id": "a", "author": "zeno"})
        '''
        self._check_query(params)
        self._equal_map.update(params)

    def with_not_equal(self, params: dict):
        '''
        查询条件，下面的例子表示查询task_id!=a且author!=zeno的结果，
        该方法可以多次调用，多次调用的结果会整合在一起，形成一个大的
        检索条件，各检索条件之间的关系是逻辑与，相当于 &&
        当一个key多次传入时，以最后一次传入的值为准
        not_equal({"task_id": "a", "author": "zeno"})
        '''
        self._check_query(params)
        self._not_equal_map.update(params)

    def with_aggr(self, fields: list):
        for field in fields:
            self._aggr_with_set.add(field)

    def _add_new_aggr_query(self, aggr: str):
        self._keyword_mark_set.add(aggr)

    def _remove_aggr_query(self, aggr: str):
        self._remove_mark_set.add(aggr)

    def wrap_search_query(self) -> dict:
        self._pre_check()
        ret = {
            "size": self._page_size if not self._aggr_with_set else 0,  # 如果有聚合条件则不返回数据集
            "query": {
                "bool": {
                    "must": self._wrap_must_query(),
                    "must_not": self._wrap_must_not_query()
                }
            }
        }
        if self._aggr_with_set:
            ret.update(self._wrap_aggr_query())
        return ret

    def _wrap_must_query(self) -> list:
        li = []
        for k, v in self._equal_map.items():
            li.append({
                "term": {k: v}
            })
        return li

    def _wrap_must_not_query(self) -> list:
        li = []
        for k, v in self._not_equal_map.items():
            li.append({
                "term": {k: v}
            })
        return li

    def _wrap_aggr_query(self) -> dict:
        ret = {}
        probe: dict = {}
        for aggr in self._aggr_with_set:
            if aggr in self._remove_mark_set:
                continue
            temp = {
                "aggs": {
                    f"group_by_{aggr}": {
                        "terms": {
                            "field": aggr if aggr not in self._keyword_mark_set else f"{aggr}.keyword"
                        }
                    },
                }
            }
            if not ret:
                ret.update(temp)
                probe = ret["aggs"][f"group_by_{aggr}"]
            else:
                probe.update(temp)
                probe = probe["aggs"][f"group_by_{aggr}"]
        return ret

    def _pre_check(self):
        """
        检查equal map是否为空，至少指定一个equal的query，防止查询/聚合的数据量过大影响性能
        """
        if not self._equal_map:
            raise ESSearchOptionError("equal map must be specified")

    def _check_query(self, params: dict):
        """
        检查query params，目前只允许query的value为int, float, string三个基本类型
        """
        for _, v in params.items():
            if isinstance(v, dict) or isinstance(v, list):
                raise ESSearchOptionError("query cannot be specified as list or dict, must be basic type")

    def _check_aggr_keys(self, fields: list):
        for field in fields:
            if not isinstance(field, str):
                raise ESSearchOptionError("field must be string type")


class ESSearchFactory:
    def __init__(self, index: str, option: ESSearchOption):
        self._index = index
        self._option = option
        self._property_mapping = self._get_property_map()
        self._option_modified = False

    def property_map(self) -> dict:
        '''
        :return: property map
        '''
        if not self._property_mapping:
            self._get_property_map()
        return self._property_mapping

    def wrap_query(self) -> dict:
        '''
        :return: 此次查询的query
        '''
        if not self._option_modified:
            self._modify_option_aggr_query()
        return self._option.wrap_search_query()

    def search(self) -> dict:
        '''
        :return: 此次查询的结果
        '''
        pass

    def _get_property_map(self):
        es_property_mapping = {}
        mapping = es_property_mapping.get("data", {}).get(self._index, {}).get("mappings", {}).get("bug", {}).get(
            "properties", {})
        return mapping

    def _modify_option_aggr_query(self):
        remove_list = []
        update_list = []
        for aggr_option in self._option._aggr_with_set:
            if aggr_option not in self._property_mapping:
                self._option._remove_aggr_query(aggr_option)
            else:
                if self._property_mapping.get(aggr_option, {}).get("type") != "keyword":
                    self._option._add_new_aggr_query(aggr_option)
        self._option_modified = True

