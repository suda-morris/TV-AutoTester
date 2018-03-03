# -*- coding:utf-8 -*-
import ConfigParser
import thread
import time

from excel import Excel
from record import Record
from relay import Relay
from remote import Remote
from serial_monitor import SerialCom


class App(object):
    """流程控制。

    读取流程脚本，开启串口
    开始输出分析器，调用设备（红外遥控和继电器），进行操作，结束输出分析器
    """

    def __init__(self):
        # 读取配置和脚本文件
        conf = ConfigParser.ConfigParser()
        conf.read('../configs/global.ini')
        process_file = ('../configs/process/' +
                        conf.get('ControlProcess', 'file') +
                        '.cp')
        with open(process_file, 'r') as f:
            self.__process = f.readlines()
        # 去除注释和空行
        self.__process = [i for i in self.__process
                          if not i.startswith(';') and i != '\r\n' and i != '\n']
        self.__step_num = len(self.__process)
        self.__step = 0
        self.__record = Record()
        self.__serial_com = SerialCom(self.__record.display_status)
        self.__remote = Remote()
        self.__relay = Relay()
        thread.start_new_thread(self.__serial_com.read_ser, ())
        self.log_name = self.__record.recording_log

    def next_operation(self):
        operation = self.__process[self.__step]
        self.__step += 1
        # 去掉换行符
        if operation.endswith('\r\n'):
            operation = operation[:-2]
        elif operation.endswith('\n'):
            operation = operation[:-1]
        operation = operation.split(' ')
        device = operation[0]
        args = operation[1:]
        args_num = len(args)
        if device == 'IR':
            # 红外遥控操作
            # print('IR', args)
            repeat_times = 1
            if args_num >= 2:
                repeat_times = int(args[1])
            for i in xrange(repeat_times):
                print('send %s operation' % args[0])
                self.__serial_com.start_parser(device, args[0])
                self.__remote.send_operation(args[0])
        elif device == 'RELAY':
            # 继电器
            print('set relay status %s' % args[0])
            self.__serial_com.start_parser(device, args[0])
            self.__relay.relay_switch(args[0] == 'ON')
        elif device == 'delay' or device == 'd':
            time.sleep(int(args[0]))
        if self.__step >= self.__step_num:
            self.__serial_com.end_parser()
            return False
        else:
            return True

    def run(self):
        while self.next_operation():
            pass
        exc = Excel(self.log_name)
        exc.read_log()


if __name__ == '__main__':
    app = App()
    while app.next_operation():
        pass
    ex = Excel(app.log_name)
    ex.read_log()
