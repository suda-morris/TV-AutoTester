import ConfigParser
import os
import json
import time

import lirc


class Remote(object):
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read("../configs/remote/remote.ini")
        self.name = cf.get("REMOTE", "name")
        self.delay = cf.getfloat("REMOTE", "delay")

    def __send_key(self, key):
        os.system("irsend SEND_ONCE " + self.name + " " + key)

    def send_operation(self, opname):
        with open('../configs/operations/key_order.json') as json_file:
            root = json.load(json_file)
            for key in root[opname]:
                self.__send_key(key)
                time.sleep(self.delay)


if __name__ == '__main__':
    sockid = lirc.init("myprogram", "../configs/lircrc")
    print(lirc.nextcode())
