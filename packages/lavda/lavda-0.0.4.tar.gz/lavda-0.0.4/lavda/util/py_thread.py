# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : LGD
# create_time : 2021/3/16 16:56
# update_time : 2021/3/16 16:56
# copyright : Lavector
# ----------------------------------------------
import threading
from traceback import format_exc


class PyThread(threading.Thread):
    def __init__(self, target, args, kwargs={}):
        super(PyThread, self).__init__()
        self.function = target
        self.args = args
        self.kwargs = kwargs
        self.exit_code = 0
        self.exception = None
        self.exc_traceback = ''

    def run(self):
        try:
            self._run()
        except Exception as e:
            self.exit_code = 1
            self.exception = e
            self.exc_traceback = str(format_exc())

    def _run(self):
        try:
            self.function(*self.args, **self.kwargs)
        except Exception as e:
            raise e