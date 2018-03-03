# -*- coding: utf-8 -*- 


import wx
import wx.xrc
import ConfigParser


class PanelRemoteChose(wx.Panel):
    def __init__(self, parent):
        self.__cf = ConfigParser.ConfigParser()
        self.__cf.read("../configs/remote/remote.ini")
        cur_remote = self.__cf.get("REMOTE", "name")
        cur_delay = self.__cf.get("REMOTE", "delay")
        read_conf = [cur_remote]
        with open("../configs/remote/cvte_factory.conf", "r") as input:
            for line in input:
                line = line.split()
                if "name" in line:
                    if line[1] not in read_conf:
                        read_conf.append(line[1])
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300),
                          style=wx.TAB_TRAVERSAL)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Remote"), wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.RemoteChoseLabel = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"RemoteChose", wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.RemoteChoseLabel.Wrap(-1)
        bSizer2.Add(self.RemoteChoseLabel, 0, wx.ALL, 5)

        # RemoteChoiceChoices = []
        self.RemoteChoice = wx.ComboBox(sbSizer1.GetStaticBox(), wx.ID_ANY, read_conf[0], wx.DefaultPosition,
                                        wx.Size(200, -1), read_conf, wx.CB_READONLY)
        bSizer2.Add(self.RemoteChoice, 0, wx.ALL, 5)

        sbSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)

        self.DelayTime = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"DelayTime", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.DelayTime.Wrap(-1)
        bSizer4.Add(self.DelayTime, 0, wx.ALL, 5)

        self.DelayTimeText = wx.TextCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, cur_delay, wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        bSizer4.Add(self.DelayTimeText, 0, wx.ALL, 5)

        self.m_staticText6 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"s", wx.DefaultPosition, wx.DefaultSize,
                                           0)
        self.m_staticText6.Wrap(-1)
        bSizer4.Add(self.m_staticText6, 0, wx.ALL, 5)

        sbSizer1.Add(bSizer4, 1, wx.EXPAND, 5)

        self.SetSizer(sbSizer1)
        self.Layout()

        # Connect Events
        self.RemoteChoice.Bind(wx.EVT_COMBOBOX, self.ReChCK)
        self.DelayTimeText.Bind(wx.EVT_TEXT, self.DeTiText)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def ReChCK(self, event):
        sel_remote = self.RemoteChoice.GetStringSelection()
        self.__cf.set("REMOTE", "name", sel_remote)
        with open("../configs/remote/remote.ini", "w") as remote_ini:
            self.__cf.write(remote_ini)

    def DeTiText(self, event):
        input_time = self.DelayTimeText.GetValue()
        self.__cf.set("REMOTE", "delay", input_time)
        with open("../configs/remote/remote.ini", "w") as remote_ini:
            self.__cf.write(remote_ini)


'''
class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title=u"TV可靠性自动测试系统", size=(800, 480))
        nb = wx.Notebook(self)
        nb.AddPage(PanelRemoteChose(nb), u"流程控制配置")
        self.Center()
        


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.SetMaxSize((800, 480))
    frame.SetMinSize((800, 480))

    frame.Show()
    frame.Refresh()
    app.MainLoop()
'''
