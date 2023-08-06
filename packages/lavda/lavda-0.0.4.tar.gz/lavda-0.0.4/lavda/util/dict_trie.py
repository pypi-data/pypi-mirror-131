# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : LGD
# create_time : 2021/4/12 14:14
# update_time : 2021/4/12 14:14
# copyright : Lavector
# ----------------------------------------------


class DictTrieNode(object):
    # 中间节点
    STATUS_MIDDLE = 1
    # 结束节点(实际上也可能是树的中间节点)
    STATUS_END = 2

    def __init__(self, node_value=None, parent_node=None):
        # 节点值
        self.node_value = node_value
        # 父节点：DictTrieNode
        self.parent_node = parent_node
        # 子节点
        self.child_node_dict = dict()
        # 节点元数据
        self.meta_data = None
        # 节点状态
        self.node_status = self.STATUS_MIDDLE

    def get_parent_node(self):
        return self.parent_node

    def has_child(self):
        return True if len(self.child_node_dict) > 0 else False

    def delete_child(self, child_node):
        node_value = child_node.get_node_value()
        if node_value in self.child_node_dict:
            self.child_node_dict.pop(node_value)

    def get_child_by_value(self, value):
        if value in self.child_node_dict:
            return self.child_node_dict[value]
        else:
            return None

    def add_child_node(self, value, child_node):
        self.child_node_dict[value] = child_node

    def get_node_value(self):
        return self.node_value

    def set_meta_data(self, meta_data):
        self.meta_data = meta_data

    def get_meta_data(self):
        return self.meta_data

    def get_node_status(self):
        return self.node_status

    def set_as_end_node(self):
        self.node_status = DictTrieNode.STATUS_END

    def is_end_node(self):
        if self.node_status == DictTrieNode.STATUS_END:
            return True

        return False

    def set_node_status(self, node_status):
        self.node_status = node_status

    def clear_node_data(self):
        """
        清空数据,删除节点时使用，但不能删除value等数据，因为它可能是某一条路径的中间节点
        :return:
        """
        self.meta_data = None
        self.node_status = DictTrieNode.STATUS_MIDDLE


class DictTrie(object):
    def __init__(self):
        self.root_node = DictTrieNode()

    def insert(self, value_list, meta_data=None):
        """
        添加数据
        :param value_list: list(string)
        :param meta_data: 单条数据的元数据
        :return:
        """
        cur_node = self.root_node

        for i, value in enumerate(value_list):
            child_node = cur_node.get_child_by_value(value)
            if child_node is None:
                child_node = DictTrieNode(value, cur_node)
                cur_node.add_child_node(value, child_node)
            cur_node = child_node

            # 最后一条数据了
            if i == len(value_list) - 1:
                cur_node.set_meta_data(meta_data)
                cur_node.set_as_end_node()

    def __find_node(self, value_list):
        cur_node = self.root_node
        for i, value in enumerate(value_list):
            child_node = cur_node.get_child_by_value(value)
            if child_node is None:
                break
            else:
                cur_node = child_node

            if i == len(value_list) - 1:
                if cur_node.is_end_node():
                    return cur_node

        return None

    def search_node(self, value_list):
        """
        查找节点
        完整匹配
        :param value_list:list(string)
        :return:
        """
        target_node = self.__find_node(value_list)
        if target_node is None:
            return None
        value = target_node.get_node_value()
        meta_data = target_node.get_meta_data()

        return value, meta_data

    def search_path(self, value_list):
        """
        查找路径
        查找部分，取最长的匹配路径
        :param value_list:
        :return:
        """
        candidate_value_list = list()
        target_value_list = None
        target_meta = None

        cur_node = self.root_node
        for i, value in enumerate(value_list):
            child_node = cur_node.get_child_by_value(value)
            if child_node is None:
                break
            else:
                candidate_value_list.append(value)
                if child_node.is_end_node():
                    target_value_list = candidate_value_list[:]
                    target_meta = child_node.get_meta_data()
                cur_node = child_node

        return target_value_list, target_meta

    def search_path_for_all(self, value_list):
        """
        从头开始查找所有符合的数据
        :param value_list:
        :return:
        """
        start = 0
        result_list = list()

        while start < len(value_list):
            search_text = value_list[start:]
            r_result = self.search_path(search_text)
            if r_result is None or r_result[1] is None:
                start += 1
            else:
                find_item = dict()
                find_item['value'] = r_result[0]
                find_item['meta'] = r_result[1]
                find_item['start'] = start
                find_item['end'] = start + len(find_item['value'])
                result_list.append(find_item)

                t_text = find_item['value']
                start += len(t_text)

        return result_list

    def delete(self, value_list):
        """
        删除对应的节点
        :param value_list:
        :return:
        """
        target_node = self.__find_node(value_list)
        if target_node:
            target_node.clear_node_data()
            if not target_node.has_child():
                parent_node = target_node.get_parent_node()
                if parent_node:
                    parent_node.delete_child(target_node)