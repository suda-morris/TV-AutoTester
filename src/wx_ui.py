# -*- coding:utf-8 -*-

import thread

import wx
import wx.grid
import wx.xrc

from app import App
from ui.com import PanelCom
from ui.control_process import PanelControlProcess
from ui.gpio import PanelGpio
from ui.key_order import PanelKeyOrder
from ui.learn_wizard import WizardNewKey
from ui.remote_chose import PanelRemoteChose

WINDOWS_WIDTH = 800
WINDOWS_HEIGHT = 500


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title=u"TV可靠性自动测试系统", pos=wx.DefaultPosition,
                          size=wx.Size(WINDOWS_WIDTH, WINDOWS_HEIGHT), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.icon = wx.Icon(u"../imgs/TV.png", wx.BITMAP_TYPE_ANY)
        self.SetIcon(self.icon)

        nb = wx.Notebook(self)
        panel_control_process = PanelControlProcess(nb)
        nb.AddPage(panel_control_process, u"流程控制配置")
        nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, panel_control_process.on_panel_changed)
        nb.AddPage(PanelKeyOrder(nb), u"按键顺序配置")
        nb.AddPage(PanelCom(nb), u"串口配置")
        nb.AddPage(PanelGpio(nb), u"GPIO配置")
        nb.AddPage(PanelRemoteChose(nb), u"遥控器选择")

        self.m_menubar = wx.MenuBar(0)
        self.m_menu1 = wx.Menu()
        self.m_menuItem1 = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"启动测试", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menuItem1.SetBitmap(wx.Bitmap(u"../imgs/TEST.png", wx.BITMAP_TYPE_ANY))
        self.m_menu1.AppendItem(self.m_menuItem1)

        self.m_menu1.AppendSeparator()

        self.m_menuItem2 = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"按键学习", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menuItem2.SetBitmap(wx.Bitmap(u"../imgs/STUDY.png", wx.BITMAP_TYPE_ANY))
        self.m_menu1.AppendItem(self.m_menuItem2)

        self.m_menubar.Append(self.m_menu1, u"功能")

        self.SetMenuBar(self.m_menubar)
        self.Center(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_MENU, self.__on_start_test, id=self.m_menuItem1.GetId())
        self.Bind(wx.EVT_MENU, self.__on_start_learn, id=self.m_menuItem2.GetId())

    def __on_start_test(self, event):
        self.__application = App()
        thread.start_new_thread(self.__application.run, ())

    def __on_start_learn(self, event):
        self.__new_remote = WizardNewKey(self)
        self.__new_remote.run()


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.SetMaxSize(wx.Size(WINDOWS_WIDTH, WINDOWS_HEIGHT))
    frame.SetMinSize(wx.Size(WINDOWS_WIDTH, WINDOWS_HEIGHT))
    frame.Show()
    frame.Refresh()
    app.MainLoop()
