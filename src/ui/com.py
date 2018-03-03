#!/usr/bin/python 
# -*- coding:utf-8 -*-


import ConfigParser
import re
import subprocess

import wx


class PanelCom(wx.Panel):
    def __init__(self, parent):
        # 状态读取relay.ini
        cf = ConfigParser.ConfigParser()
        cf.read("../configs/serial/com.ini")
        comPath = cf.get("COM", "path")
        comPath = comPath[5:]
        comBaud = cf.get("COM", "baud")
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(800, 480),
                          style=wx.TAB_TRAVERSAL)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Com"), wx.VERTICAL)

        fgSizer1 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText1 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Path", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        fgSizer1.Add(self.m_staticText1, 0, wx.ALL, 5)

        m_comboBox1Choices = []
        self.m_comboBox1 = wx.ComboBox(sbSizer1.GetStaticBox(), wx.ID_ANY, comPath, wx.DefaultPosition, wx.DefaultSize,
                                       m_comboBox1Choices, 0)
        fgSizer1.Add(self.m_comboBox1, 0, wx.ALL, 5)

        self.m_staticText2 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Baud", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        fgSizer1.Add(self.m_staticText2, 0, wx.ALL, 5)

        m_comboBox2Choices = [u"9600", u"19200", u"38400", u"57600", u"115200"]
        self.m_comboBox2 = wx.ComboBox(sbSizer1.GetStaticBox(), wx.ID_ANY, comBaud, wx.DefaultPosition, wx.DefaultSize,
                                       m_comboBox2Choices, 0)
        fgSizer1.Add(self.m_comboBox2, 0, wx.ALL, 5)

        sbSizer1.Add(fgSizer1, 1, wx.EXPAND, 5)

        self.SetSizer(sbSizer1)
        self.Layout()

        # Connect Events
        self.m_comboBox1.Bind(wx.EVT_COMBOBOX, self.com_combo_bind1)
        self.m_comboBox2.Bind(wx.EVT_COMBOBOX, self.com_combo_bind2)

        # DO NOT change below
        result = subprocess.check_output("dmesg | grep tty*", shell=True)
        result = list(set(re.findall(r"tty[\w]+", result)))
        self.m_comboBox1.SetItems(result)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def com_combo_bind1(self, event):
        c = self.m_comboBox1.GetValue()
        s = "/dev/" + c
        cf = ConfigParser.ConfigParser()
        cf.read("../configs/serial/com.ini")
        cf.set("COM", "path", s)
        with open("../configs/serial/com.ini", "w") as cfile:
            cf.write(cfile)

    def com_combo_bind2(self, event):
        c = self.m_comboBox2.GetValue()
        cf = ConfigParser.ConfigParser()
        cf.read("../configs/serial/com.ini")
        cf.set("COM", "baud", c)
        with open("../configs/serial/com.ini", "w") as cfile:
            cf.write(cfile)
