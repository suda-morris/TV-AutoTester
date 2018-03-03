#!/usr/bin/python
# -*- coding: utf-8 -*-

# *************************************************************
# Filename @ serial.py
# Author @ wangshun
# Create date @ 2017-07-31 14:54:20
# Description @ read serial program
# *************************************************************
# Script starts from here
# time.strftime("%Y_%m_%d_%X",time.localtime())获取格式化时间字符串

import ConfigParser
import json
import logging
import logging.handlers
import time
import re

import serial


class SerialCom(object):
    def __dev_log_init(self):
        time_str = time.strftime("%Y_%m_%d_%X", time.localtime())
        self.__monitoring_log = "../logs/serial_log/dev_monitor_%s.log" % time_str
        handler = logging.handlers.RotatingFileHandler(self.__monitoring_log)
        fmt = "%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s"

        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        logger = logging.getLogger("dev_moni")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    def __init__(self, callback=None):
        cf = ConfigParser.ConfigParser()
        cf.read("../configs/serial/com.ini")
        self.__serial_path = cf.get("COM", "path")
        self.__baud_rate = cf.getint("COM", "baud")
        self.__ser_com = serial.Serial(self.__serial_path, self.__baud_rate)
        self.__dev_log_init()

        self.__callback = callback
        self.__new_cmd_time = 0
        self.__start_parser_flag = False
        self.__logs = []
        self.__device = None
        self.__operation = None

    def read_ser(self):
        logger = logging.getLogger("dev_moni")
        while True:
            count = self.__ser_com.inWaiting()
            if count != 0:
                recv = self.__ser_com.read(count)
                # print recv
                if self.__start_parser_flag:
                    self.__logs.append(recv)
                else:
                    logger.debug(recv)
            self.__ser_com.flushInput()
            time.sleep(0.1)

    def start_parser(self, device, operation):
        # 在下一操作开始前结束前面开启的分析器
        if self.__start_parser_flag:
            self.end_parser()
        self.__new_cmd_time = time.strftime("%Y_%m_%d_%X", time.localtime())
        self.__start_parser_flag = True
        self.__logs = []
        self.__device = device
        self.__operation = operation

    def end_parser(self):
        if not self.__start_parser_flag:
            return
        self.__start_parser_flag = False
        logger = logging.getLogger("dev_moni")
        self.__logs = ''.join(self.__logs)
        logger.debug(self.__logs)
        result = False
        with open('../configs/operations/success_fail.json') as json_file:
            root = json.load(json_file)
            for op in root[self.__device]:
                if op['operation'] == self.__operation:
                    for string in op['success']:
                        if re.search(string, self.__logs, re.I):
                            result = True
                            break
                    break
        # print('Result:', result)
        if self.__callback is not None:
            self.__callback(self.__device, self.__operation, result)

    def __del__(self):
        self.__ser_com.close()


if __name__ == '__main__':
    try:
        serial_usb1 = SerialCom()
        serial_usb1.read_ser()
    except KeyboardInterrupt:
        pass
