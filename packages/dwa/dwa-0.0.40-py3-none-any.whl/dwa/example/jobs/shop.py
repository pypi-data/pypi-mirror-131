from dwa import *
import re
import json
import copy
import datetime
import queue
import requests
import urllib.parse
import threadwrapper
from lxml import html
import omnitools


class item_info_worker(workers.base_worker):
    item_info = {}
    updating = False
    getting = True

    def update_item_info(self):
        self.item_info.clear()
        id = 0
        data = 1
        self.item_info[id] = data

    def job(self) -> None:
        self.export_functions = {
            "get_item_info": self.get_item_info,
        }
        if len(self.item_info) > 0 or self.getting:
            for i in range(0, 5):
                if self.terminate:
                    return
                time.sleep(1)
        self.updating = True
        self.update_item_info()
        self.updating = False

    def wait_for_updating(self):
        while self.updating:
            time.sleep(1/1000)
        self.getting = True

    def copy(self, d, b=False):
        c = copy.deepcopy(d)
        self.getting = b
        return c

    def get_item_info(self, id, *args, **kwargs):
        self.wait_for_updating()
        item_info = self.copy(self.item_info)
        try:
            return item_info[int(id)]
        except:
            return Exception("404 Not Found")


class reserve_order_worker(workers.base_worker):
    roq = queue.Queue()
    ro_done = {}

    def job(self) -> None:
        self.export_functions = {
            "reserve_order": self.reserve_order,
        }
        if self.roq.qsize() == 0:
            time.sleep(1)
            return
        data, signature = self.roq.get()
        result = str(data)+" done"
        self.ro_done[signature] = result
        self.roq.task_done()

    def reserve_order(self, data, *args, **kwargs):
        signature = omnitools.sha3_512hd(json.dumps(data)+str(int(time.time())))
        self.roq.put((data, signature))
        while signature not in self.ro_done:
            time.sleep(1/1000)
        return self.ro_done.pop(signature)

