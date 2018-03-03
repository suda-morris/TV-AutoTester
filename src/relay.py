#!/usr/bin/python
# -*- coding: utf-8 -*-
'''继电器高电平导通，低电平断开'''

import RPi.GPIO as GPIO
import time
import ConfigParser


class Relay(object):
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read("../configs/gpio/relay.ini")
        # relay状态读取
        self.relayStatus = cf.get("RELAY", "Status")
        self.relayPin = cf.getint("RELAY", "Pin")
        # GPIO初始化
        GPIO.setmode(GPIO.BCM)  # BCM编号方式
        GPIO.setwarnings(False)  # 关闭警告
        GPIO.setup(self.relayPin, GPIO.OUT)
        # 根据配置文件初始化relay
        if self.relayStatus == "ON":
            GPIO.output(self.relayPin, GPIO.HIGH)
        else:
            GPIO.output(self.relayPin, GPIO.LOW)

    def relay_switch(self, status):
        if status:
            GPIO.output(self.relayPin, GPIO.HIGH)
        else:
            GPIO.output(self.relayPin, GPIO.LOW)


# 实例化举例
if __name__ == '__main__':
    re = Relay()
    time.sleep(1)
    re.relay_switch(False)
