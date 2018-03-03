#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import ConfigParser
import logging
import logging.handlers


class Record(object):
    """record test result"""

    def __dev_log_init(self):
        time_str = time.strftime("%Y_%m_%d_%X", time.localtime())
        self.recording_log = "../logs/record_log/dev_record_%s.log" % time_str
        handler = logging.handlers.RotatingFileHandler(self.recording_log)
        fmt = "%(asctime)s - %(name)s :[%(message)s]"

        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        logger = logging.getLogger("dev_record")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    def __init__(self):
        self.__dev_log_init()

        cf = ConfigParser.ConfigParser()
        cf.read("../configs/gpio/record.ini")
        # led读取
        self.ledStatus = cf.get("LED", "Status")
        self.ledSuccessPin = cf.getint("LED", "SuccessPin")
        self.ledFailPin = cf.getint("LED", "FailPin")
        # buzzer读取
        self.buzzerStatus = cf.get("BUZZER", "Status")
        self.buzzerPin = cf.getint("BUZZER", "Pin")
        # GPIO初始化
        GPIO.setmode(GPIO.BCM)  # BCM编号方式
        GPIO.setwarnings(False)  # 关闭警告
        GPIO.setup(self.ledSuccessPin, GPIO.OUT)
        GPIO.setup(self.ledFailPin, GPIO.OUT)
        GPIO.setup(self.buzzerPin, GPIO.OUT)
        # 根据配置文件初始化led和buzzer
        if self.ledStatus == "ON":
            GPIO.output(self.ledSuccessPin, GPIO.HIGH)
            GPIO.output(self.ledFailPin, GPIO.LOW)
        else:
            GPIO.output(self.ledSuccessPin, GPIO.LOW)
            GPIO.output(self.ledFailPin, GPIO.HIGH)
        if self.buzzerStatus == "ON":
            GPIO.output(self.buzzerPin, GPIO.LOW)
            time.sleep(0.1)
            GPIO.output(self.buzzerPin, GPIO.HIGH)
        else:
            GPIO.output(self.buzzerPin, GPIO.HIGH)

    def display_status(self, device, operation, result):
        logger = logging.getLogger("dev_record")
        logger.debug(device + " " + operation + " " + str(result))
        if result:
            GPIO.output(self.ledSuccessPin, GPIO.HIGH)
            GPIO.output(self.ledFailPin, GPIO.LOW)
            time.sleep(1)
            GPIO.output(self.ledSuccessPin, GPIO.LOW)
            GPIO.output(self.buzzerPin, GPIO.HIGH)
        else:
            GPIO.output(self.ledSuccessPin, GPIO.LOW)
            GPIO.output(self.ledFailPin, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.ledFailPin, GPIO.LOW)
            GPIO.output(self.buzzerPin, GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(self.buzzerPin, GPIO.HIGH)  # 实例化举例


if __name__ == '__main__':
    rec = Record()
    time.sleep(1)
