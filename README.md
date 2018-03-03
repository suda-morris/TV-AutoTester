# TV可靠性自动测试系统

## 项目名称统一要求
1. 设备名
    * 红外设备：IR
    * 继电器设备：RELAY
2. 操作名
    * 上电：
        * 使用设备：RELAY
        * 设备操作：ON
    * 下电：
        * 使用设备：RELAY
        * 设备操作：OFF
    * 开机：
        * 使用设备：IR
        * 设备操作：KEY_POWER
    * 关机：
        * 使用设备：IR
        * 设备操作：
    * 

## 安装raspberry-gpio-python
* [下载链接](https://sourceforge.net/projects/raspberry-gpio-python/)
* sudo python setup.py install

```python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO
# BOARD编号方式，基于插座引脚编号
GPIO.setmode(GPIO.BOARD)
# 关闭警告
GPIO.setwarnings(False)
# 输出模式
GPIO.setup(11, GPIO.OUT)
while True:
    GPIO.output(11, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(11, GPIO.LOW)
    time.sleep(1)
```

## 串口编程pyserial
* sudo pip install pyserial

## excel报表openpyxl
* sudo pip install openpyxl
```python
# -*- coding: utf-8 -*-
import datetime

from openpyxl import Workbook

# 新建一个工作簿
wb = Workbook()
# 获取正在运行的工作表
ws = wb.active
# 重命名工作表
ws.title = "Test_Result"
# 改变标签栏的字体颜色：
ws.sheet_properties.tabColor = "1072BA"

# 修改单元格的内容
d = ws.cell(row=4, column=2)
d.value = datetime.datetime.now()

# 保存文件
wb.save('Test_Result.xlsx')

```

## 读取写入配置文件ConfigParser
* python内置configparser模块
```python
# -*- coding: utf-8 -*-
import ConfigParser

cf = ConfigParser.ConfigParser()

cf.read("../configs/success_fail.ini")
secs = cf.sections()
print('sections:', secs, type(secs))
opts = cf.options("IR")
print('options:', opts, type(opts))
kvs = cf.items("IR")
print('IR:', kvs)

ir_time = cf.get("IR", "IRKey_Power")
print("IRKey_Power", ir_time)
```

## 日志模块logging
* python内置logging模块
* 日志级别大小关系为：CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
```python
# -*- coding: utf-8 -*-

import logging.config

if __name__ == '__main__':
    logging.config.fileConfig("../configs/logger.conf")
    logger = logging.getLogger("root")

    logger.debug('This is debug message')
    logger.info('This is info message')
    logger.warning('This is warning message')
```

## 红外编解码LIRC
* [官网地址](http://www.lirc.org/)
* [参考博文](http://www.jianshu.com/p/9cfb0bf02006)
* sudo apt-get install python-lirc lirc
* 修改硬件配置文件 sudo vim /etc/lirc/hardware.conf

```
LIRCD_ATGS=""
DRIVER="default"
DEVICE="/dev/lirc0"
MODULES="lirc-rpi
```

* 修改内核模块配置文件 sudo vim /etc/modules

```
lirc-dev
lirc-rpi gpio_in_pin=18 gpio_out_pin=17
```

* 重启树莓派，使配置生效
* 重启LIRC软件 sudo /etc/init.d/lirc restart
* 测试红外接受是否正常
    * 关闭LIRC软件 sudo /etc/init.d/lirc stop
    * 开启检测 mode2 -d /dev/lirc0
* 用红外遥控器，对着接收器按下任意按键，屏幕会打印类似下面的内容

```
space 16300
pulse 95
space 28794
pulse 80
space 19395
```

* 查看LIRC支持的遥控按键，手动记录
    * sudo /etc/init.d/lirc stop
    * irrecord -list-namespace
* 红外编码录制
    * 把cvte_factory.conf文件拷贝到用户根目录下
    * irrecord -d /dev/lirc0 ~/cvte_factory.conf -n
    * 屏幕提示**Please enter the name for the next button (press ENTER to finish recording)**，然后依次输入想要录制的按键
    * 将录制好的配置文件覆盖lirc软件的相应文件 **sudo cp ~/lircd.conf /etc/lirc/lircd.conf**
* 测试遥控器与接收模块是否工作正常
    * sudo /etc/init.d/lirc start
    * irw
* 绑定按键与行为
    * vim ~/.lircrc
    * 重启lirc软件并执行"irexec"命令

```
begin
    prog = irexec
    button = KEY_POWER
    config = echo "Hello world"
end
```

* 红外发射功能
    * irsend SEND_ONCE cvte_factory KEY_POWER
    
## 图形界面wxPython
* sudo apt-get install python-wxgtk3.0

## 自动化交互模块pexpect
* sudo pip install wheel
* sudo pip install pexpect-4.2.1-py2.py3-none-any.whl

