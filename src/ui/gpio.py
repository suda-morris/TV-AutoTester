#!/usr/bin/python 
# -*- coding:utf-8 -*-


import wx
import ConfigParser
import time


class PanelGpio(wx.Panel):
    def __init__(self, parent):
        # 状态读取relay.ini
        cf = ConfigParser.ConfigParser()
        cf.read("../configs/gpio/relay.ini")
        relayStatus = cf.get("RELAY", "Status")
        relayPin = cf.get("RELAY", "Pin")
        # 状态读取record.ini
        cft = ConfigParser.ConfigParser()
        cft.read("../configs/gpio/record.ini")
        ledStatus = cft.get("LED", "status")
        ledSuccessPin = cft.get("LED", "successpin")
        ledFailPin = cft.get("LED", "failpin")
        buzzerStatus = cft.get("BUZZER", "status")
        buzzerPin = cft.get("BUZZER", "pin")

        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(800, 480),
                          style=wx.TAB_TRAVERSAL)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Relay"), wx.VERTICAL)

        fgSizer1 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText1 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Status", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        fgSizer1.Add(self.m_staticText1, 0, wx.ALL, 5)

        m_comboBox1Choices = [u"ON", u"OFF"]
        self.m_comboBox1 = wx.ComboBox(sbSizer1.GetStaticBox(), wx.ID_ANY, relayStatus, wx.DefaultPosition,
                                       wx.DefaultSize, m_comboBox1Choices, 0)
        fgSizer1.Add(self.m_comboBox1, 0, wx.ALL, 5)

        self.m_staticText2 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Pin", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        fgSizer1.Add(self.m_staticText2, 0, wx.ALL, 5)

        m_comboBox2Choices = [u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14",
                              u"15", u"16", u"17", u"18", u"19", u"20", u"21", u"22", u"23", u"24", u"25", u"26", u"27"]
        self.m_comboBox2 = wx.ComboBox(sbSizer1.GetStaticBox(), wx.ID_ANY, relayPin, wx.DefaultPosition, wx.DefaultSize,
                                       m_comboBox2Choices, 0)
        fgSizer1.Add(self.m_comboBox2, 0, wx.ALL, 5)

        sbSizer1.Add(fgSizer1, 1, wx.EXPAND, 5)
        #
        sbSizer2 = wx.StaticBoxSizer(wx.StaticBox(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Led"), wx.VERTICAL)

        fgSizer2 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText3 = wx.StaticText(sbSizer2.GetStaticBox(), wx.ID_ANY, u"Status", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        fgSizer2.Add(self.m_staticText3, 0, wx.ALL, 5)

        m_comboBox3Choices = [u"ON", u"OFF"]
        self.m_comboBox3 = wx.ComboBox(sbSizer2.GetStaticBox(), wx.ID_ANY, ledStatus, wx.DefaultPosition,
                                       wx.DefaultSize, m_comboBox3Choices, 0)
        fgSizer2.Add(self.m_comboBox3, 0, wx.ALL, 5)

        self.m_staticText4 = wx.StaticText(sbSizer2.GetStaticBox(), wx.ID_ANY, u"SuccessPin", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        fgSizer2.Add(self.m_staticText4, 0, wx.ALL, 5)

        m_comboBox4Choices = [u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14",
                              u"15", u"16", u"17", u"18", u"19", u"20", u"21", u"22", u"23", u"24", u"25", u"26", u"27"]
        self.m_comboBox4 = wx.ComboBox(sbSizer2.GetStaticBox(), wx.ID_ANY, ledSuccessPin, wx.DefaultPosition,
                                       wx.DefaultSize, m_comboBox4Choices, 0)
        fgSizer2.Add(self.m_comboBox4, 0, wx.ALL, 5)

        self.m_staticText5 = wx.StaticText(sbSizer2.GetStaticBox(), wx.ID_ANY, u"FailPin", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        fgSizer2.Add(self.m_staticText5, 0, wx.ALL, 5)

        m_comboBox5Choices = [u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14",
                              u"15", u"16", u"17", u"18", u"19", u"20", u"21", u"22", u"23", u"24", u"25", u"26", u"27"]
        self.m_comboBox5 = wx.ComboBox(sbSizer2.GetStaticBox(), wx.ID_ANY, ledFailPin, wx.DefaultPosition,
                                       wx.DefaultSize, m_comboBox5Choices, 0)
        fgSizer2.Add(self.m_comboBox5, 0, wx.ALL, 5)

        sbSizer2.Add(fgSizer2, 1, wx.EXPAND, 5)

        sbSizer1.Add(sbSizer2, 1, wx.EXPAND, 5)
        #
        sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Buzzer"), wx.VERTICAL)

        fgSizer3 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer3.SetFlexibleDirection(wx.BOTH)
        fgSizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText6 = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY, u"Status", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)
        fgSizer3.Add(self.m_staticText6, 0, wx.ALL, 5)

        m_comboBox6Choices = [u"ON", u"OFF"]
        self.m_comboBox6 = wx.ComboBox(sbSizer3.GetStaticBox(), wx.ID_ANY, buzzerStatus, wx.DefaultPosition,
                                       wx.DefaultSize, m_comboBox6Choices, 0)
        fgSizer3.Add(self.m_comboBox6, 0, wx.ALL, 5)

        self.m_staticText7 = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY, u"Pin", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)
        fgSizer3.Add(self.m_staticText7, 0, wx.ALL, 5)

        m_comboBox7Choices = [u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14",
                              u"15", u"16", u"17", u"18", u"19", u"20", u"21", u"22", u"23", u"24", u"25", u"26", u"27"]
        self.m_comboBox7 = wx.ComboBox(sbSizer3.GetStaticBox(), wx.ID_ANY, buzzerPin, wx.DefaultPosition,
                                       wx.DefaultSize, m_comboBox7Choices, 0)
        fgSizer3.Add(self.m_comboBox7, 0, wx.ALL, 5)

        sbSizer3.Add(fgSizer3, 1, wx.EXPAND, 5)

        sbSizer1.Add(sbSizer3, 1, wx.EXPAND, 5)
        #

        self.SetSizer(sbSizer1)
        self.Layout()

        # relay Connect Events
        self.m_comboBox1.Bind(wx.EVT_COMBOBOX, self.relay_combo_bind1)
        self.m_comboBox2.Bind(wx.EVT_COMBOBOX, self.relay_combo_bind2)
        # record Connect Events
        self.m_comboBox3.Bind(wx.EVT_COMBOBOX, self.relay_combo_bind3)
        self.m_comboBox4.Bind(wx.EVT_COMBOBOX, self.relay_combo_bind4)
        self.m_comboBox5.Bind(wx.EVT_COMBOBOX, self.relay_combo_bind5)
        self.m_comboBox6.Bind(wx.EVT_COMBOBOX, self.relay_combo_bind6)
        self.m_comboBox7.Bind(wx.EVT_COMBOBOX, self.relay_combo_bind7)

    # Virtual event handlers, overide them in your derived class
    def relay_combo_bind1(self, event):
        c = self.m_comboBox1.GetValue()
        cf = ConfigParser.ConfigParser()
        cf.read("../configs/gpio/relay.ini")
        cf.set("RELAY", "status", c)
        cf.write(open("../configs/gpio/relay.ini", "w"))

    def relay_combo_bind2(self, event):
        c = self.m_comboBox2.GetValue()
        cf = ConfigParser.ConfigParser()
        cf.read("../configs/gpio/relay.ini")
        cf.set("RELAY", "pin", c)
        cf.write(open("../configs/gpio/relay.ini", "w"))

    def relay_combo_bind3(self, event):
        c = self.m_comboBox3.GetValue()
        cf = ConfigParser.ConfigParser()
        cf.read("../configs/gpio/record.ini")
        cf.set("LED", "status", c)
        cf.write(open("../configs/gpio/record.ini", "w"))

    def relay_combo_bind4(self, event):
        c = self.m_comboBox4.GetValue()
        cf = ConfigParser.ConfigParser()
        cf.read("../configs/gpio/record.ini")
        cf.set("LED", "successpin", c)
        cf.write(open("../configs/gpio/record.ini", "w"))

    def relay_combo_bind5(self, event):
        c = self.m_comboBox5.GetValue()
        cf = ConfigParser.ConfigParser()
        cf.read("../configs/gpio/record.ini")
        cf.set("LED", "failpin", c)
        cf.write(open("../configs/gpio/record.ini", "w"))

    def relay_combo_bind6(self, event):
        c = self.m_comboBox6.GetValue()
        cf = ConfigParser.ConfigParser()
        cf.read("../configs/gpio/record.ini")
        cf.set("BUZZER", "status", c)
        cf.write(open("../configs/gpio/record.ini", "w"))

    def relay_combo_bind7(self, event):
        c = self.m_comboBox7.GetValue()
        cf = ConfigParser.ConfigParser()
        cf.read("../configs/gpio/record.ini")
        cf.set("BUZZER", "pin", c)
        cf.write(open("../configs/gpio/record.ini", "w"))
