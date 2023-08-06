import copy
import hashlib
import os
import time
from threading import Thread

from pyrhd.utility.utils import Utils


class Dupy:
    def __init__(self, root_path) -> None:
        self.root_path = root_path
        self.dups = []
        self.hm = {}
        self.saverthread = Thread(target=self.saveDeamon)
        self.saveflag = True
        self.saverthread.start()

        self.main()
        self.saveflag = False
        self.saverthread.join()
        cache_path = os.path.join(self.root_path, "dupy.json")
        Utils.json.saveDict(copy.deepcopy(self.hm), cache_path)

    def getHash(self, file_path, first_chunk_only=True) -> str:
        with open(file_path, "rb") as f:
            file_data = f.read(1024 if first_chunk_only else None)
            hashed = hashlib.sha1(file_data).digest().hex()
        return hashed

    def main(self):
        self.hm = dict()
        # size based hashmap
        for i in Utils.os.getAllFiles(self.root_path):
            file_size = os.path.getsize(i)
            self.hm[file_size] = self.hm.get(file_size, {0: [], 1: {}, 2: {}})
            self.hm[file_size][0].append(i)
        print(len(self.hm))

        # first 1024 bytes based hashmap
        for i, j in ((i, j) for (i, j) in self.hm.items() if len(j[0]) > 1):
            for file_path in j[0]:
                hashed = self.getHash(file_path)
                self.hm[i][1][hashed] = self.hm[i][1].get(hashed, [])
                self.hm[i][1][hashed].append(file_path)

        # full-file based hashmap
        for i, j in self.hm.items():
            for a, b in j[1].items():
                if len(b) > 1:
                    for file_path in b:
                        hashed = self.getHash(file_path, False)
                        self.hm[i][2][hashed] = self.hm[i][2].get(hashed, [])
                        self.hm[i][2][hashed].append(file_path)

        # analysis
        count = 0
        for size, size_based in self.hm.items():
            for file, file_based in size_based[2].items():
                count += 1
                if len(file_based) > 1:
                    self.dups.append(file_based)

    def saveDeamon(self):
        cache_path = os.path.join(self.root_path, "dupy.json")
        while self.saveflag:
            try:
                Utils.json.saveDict(copy.deepcopy(self.hm), cache_path)
            except:
                ...
            time.sleep(5)

    def getDups(self):
        return self.dups
