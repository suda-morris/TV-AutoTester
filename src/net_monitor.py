#!/usr/bin/python
# -*- coding: utf-8 -*-

# *************************************************************
# Filename @ popen.py
# Author @ zhengxiasong
# Create date @ 2017-08-04 11:25:58
# Description @
# *************************************************************
# Script starts from here
import os
import sys
import commands
import time
from subprocess import Popen, PIPE
from os import kill
import signal
import ConfigParser
import logging
import logging.handlers


class ReadNetPrint(object):
    def __init__(self):
        self.__cf = ConfigParser.ConfigParser()
        self.__cf.read("../configs/net/net_conf.ini")

        self.__ip = self.__cf.get("NET","IP")
        self.__mess = self.__cf.get("NET","MESSAGE")
        # message = "tvos"
        self.__adbdiscon = "adb disconnect %s" % self.__ip
        self.__adbcon = "adb connect %s" % self.__ip
        self.__adblog = "adb logcat"
        self.__adblogfilter = "adb logcat -s %s" % self.__mess
        self.dev_log_init()
        # self.read_net_print()

    def read_net_print(self):
        # 获取log
        logger = logging.getLogger("net_moni")
        return_codes,output = commands.getstatusoutput(self.__adbdiscon)
        time.sleep(1)
        # 尝试连接网络最多10次
        for index in range(1,10):
            return_codes,output = commands.getstatusoutput(self.__adbcon)
            if ("connected to %s" % self.__ip) in output:
                break
            else:
                time.sleep(1)
        # 开始查看log
        self.__talkpipe = Popen(self.__adblogfilter,shell=True, stdout=PIPE)
        try:
            while True:
                line = self.__talkpipe.stdout.readline()
                if line:
                    # print  line.strip()
                    logger.debug(line)
                time.sleep(0.1)
        except KeyboardInterrupt:
            # print "Killing child..."
            commands.getstatusoutput(self.__adbdiscon)
            kill(self.__talkpipe.pid, signal.SIGTERM)
    
    def dev_log_init(self):
        time_str = time.strftime("%Y_%m_%d_%X",time.localtime())
        self.__monitoring_log = "../logs/net_log/net_monitor_%s.log" % (time_str)
        handler = logging.handlers.RotatingFileHandler(self.__monitoring_log)
        fmt = "%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s"

        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        logger = logging.getLogger("net_moni")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)


def main():
    read_net = ReadNetPrint()
    read_net.read_net_print()
if __name__ == "__main__":
    main()
