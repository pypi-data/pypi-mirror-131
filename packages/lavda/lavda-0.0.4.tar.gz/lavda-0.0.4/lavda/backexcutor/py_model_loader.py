# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : 
# create_time : 2020/6/30 18:27
# update_time : 2020/6/30 18:27
# copyright : Lavector
# ----------------------------------------------
import importlib
from lavda.util.file_tool import FileTool


class PyModelLoader(object):
    def __init__(self):
        package_list = list()
        package_list.append('lavda.analysis.da_pre')
        # package_list.append('maxda.analysis.da_save')
        package_list.append('lavda.analysis.da_extract')
        package_list.append('lavda.analysis.da_clean')
        package_list.append('lavda.analysis.da_tag')
        package_list.append('lavda.analysis.da_statis')

        m_list = list()
        for p_name in package_list:
            p_m = importlib.import_module(p_name)
            # TODO 每次使用时都重新加载，这样maxda更新时，不再需要更新autoda
            # importlib.reload(p_m)

            file_name_list = FileTool.get_all_file(p_m.__path__[0], suffix='.py')
            file_name_list = [FileTool.get_base_name(name) for name in file_name_list]
            file_name_list = [name.replace(".py", "") for name in file_name_list]
            file_name_list.remove("__init__")

            for py_name in file_name_list:
                py_m = importlib.import_module(p_name + '.' + py_name)
                m_list.append(py_m)

        self.m_list = m_list

    def load(self, class_name, **init_param):
        for m_py in self.m_list:
            if not hasattr(m_py, class_name):
                continue
            obj_class_name = getattr(m_py, class_name)
            if init_param is None:
                target_class = obj_class_name()
            else:
                target_class = obj_class_name(**init_param)
            return target_class

        return None
