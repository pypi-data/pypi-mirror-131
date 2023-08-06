import json
import os
import threading
import time
from copy import deepcopy

from pyrhd.utility.cprint import aprint

SAVING_INTERVAL = 10


class BaseHarvester:
    def __init__(
        self, ultimatum_path, saving_interval: int = None, default_ultimatum: dict = {}
    ) -> None:
        self.ultimatum_path = ultimatum_path
        # custom saving interval if given, else defaults to global variable SAVING_INTERVAL
        self.save_int = saving_interval or SAVING_INTERVAL
        self.ultimatum = {}
        self.save_flag = True
        self.getFileData(default_ultimatum)
        self.life_saver_thr = threading.Thread(target=self.lifeSaver, daemon=True)
        self.life_saver_thr.start()

    def getFileData(self, default_ultimatum):
        try:
            if os.path.exists(self.ultimatum_path):
                with open(self.ultimatum_path, "r") as f:
                    buffer = f.read()
                    for i in range(3):
                        last = "}" * i
                        try:
                            content = buffer + last
                            self.ultimatum = json.loads(content)
                            break
                        except:
                            ...
            else:
                raise Exception
        except:
            p = os.path.dirname(self.ultimatum_path)
            os.makedirs(p, exist_ok=True)
        if self.ultimatum == {}:
            self.ultimatum = default_ultimatum
        self.saveUltimatum()

    def saveUltimatum(self):
        try:
            with open(self.ultimatum_path, "w") as f:
                # use copy() to avoid "RuntimeError: dictionary changed size during iteration"
                json.dump(deepcopy(self.ultimatum), f, indent=4)
        except Exception as e:
            aprint(e, "red")

    def lifeSaver(self):
        while self.save_flag:
            self.saveUltimatum()
            time.sleep(self.save_int)

    def quitSaver(self):
        self.save_flag = False
        self.saveUltimatum()
