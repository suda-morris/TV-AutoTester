# -*- coding: utf-8 -*-

import subprocess
import thread
import time
import os

import pexpect
import wx
import wx.wizard
import wx.xrc


class DialogWaitingForKey(wx.Dialog):
    def __init__(self, parent, remote_name, key_name, shell):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"请按住遥控器按键", pos=wx.DefaultPosition,
                           size=wx.Size(250, 250), style=wx.STAY_ON_TOP | wx.SYSTEM_MENU)

        bSizer = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"请按住遥控器按键", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        self.m_staticText1.SetFont(
            wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString))

        bSizer.Add(self.m_staticText1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_bitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(u"../imgs/WAITING.png", wx.BITMAP_TYPE_ANY),
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer.Add(self.m_bitmap, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer.AddSpacer((0, 0), 1, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"正在接收...", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        bSizer.Add(self.m_staticText2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.__key_name = key_name
        self.__remote_name = remote_name
        self.__shell = shell
        thread.start_new_thread(self.__thread_learning, ())

    def __thread_learning(self):
        index = self.__shell.expect([self.__key_name, pexpect.EOF, pexpect.TIMEOUT])
        if index == 0:
            wx.CallAfter(self.m_staticText2.SetLabel, u"请按住按键" + self.__key_name)
            while True:
                index = self.__shell.expect(["<ENTER>", pexpect.EOF, pexpect.TIMEOUT])
                if index == 0:
                    wx.CallAfter(self.m_staticText2.SetLabel, u"成功学习按键" + self.__key_name)
                    print "learn " + self.__key_name + " OK"
                    time.sleep(1)
                    break
                else:
                    wx.CallAfter(self.m_staticText2.SetLabel, u"请重新按住按键" + self.__key_name)
        else:
            self.__shell.close(force=True)
            self.EndModal(wx.ID_CANCEL)
        self.EndModal(wx.ID_OK)


class EnterKeyNamePage(wx.wizard.WizardPageSimple):
    def __init__(self, parent):
        wx.wizard.WizardPageSimple.__init__(self, parent)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText = wx.StaticText(self, wx.ID_ANY, u"请输入新的按键名", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText.Wrap(-1)
        self.m_staticText.SetFont(
            wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))

        bSizer1.Add(self.m_staticText, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_bitmap1 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(u"../imgs/KEY.png", wx.BITMAP_TYPE_ANY),
                                         wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_bitmap1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_textCtrl = wx.TextCtrl(self, wx.ID_ANY, u"KEY NAME", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_textCtrl, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_button = wx.Button(self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_button, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        # Connect Events
        self.m_button.Bind(wx.EVT_BUTTON, self.__on_btn_ok)

        self.__remote_name = None
        self.__shell = None

    def __on_btn_ok(self, event):
        key_name = self.m_textCtrl.GetValue()
        if self.__shell.isalive():
            self.__shell.send(key_name + "\n")
            dialog = DialogWaitingForKey(self, self.__remote_name, key_name, self.__shell)
            result = dialog.ShowModal()
            if result == wx.ID_OK:
                print "OK"
            else:
                print "Cancel"
            dialog.Destroy()
        else:
            print "pexpect has closed"

    def set_new_remote_name(self, name):
        self.__remote_name = name

    def set_shell_controller(self, shell):
        self.__shell = shell


class EnterRemoteNamePage(wx.wizard.WizardPageSimple):
    def __init__(self, parent):
        wx.wizard.WizardPageSimple.__init__(self, parent)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText = wx.StaticText(self, wx.ID_ANY, u"请输入新的遥控器名", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText.Wrap(-1)
        self.m_staticText.SetFont(
            wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))

        bSizer1.Add(self.m_staticText, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_bitmap1 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(u"../imgs/REMOTE.png", wx.BITMAP_TYPE_ANY),
                                         wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_bitmap1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_textCtrl = wx.TextCtrl(self, wx.ID_ANY, u"REMOTE NAME", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_textCtrl, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer1)
        self.Layout()


class WizardNewKey(wx.wizard.Wizard):
    def __init__(self, parent):
        wx.wizard.Wizard.__init__(self, parent, id=wx.ID_ANY, title=u"添加新的按键", bitmap=wx.NullBitmap,
                                  pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE)

        self.m_pages = []
        self.remote_page = EnterRemoteNamePage(self)
        self.add_page(self.remote_page)
        self.key_page = EnterKeyNamePage(self)
        self.add_page(self.key_page)

        self.Centre(wx.BOTH)

        self.Bind(wx.wizard.EVT_WIZARD_CANCEL, self.__on_cancle)
        self.Bind(wx.wizard.EVT_WIZARD_FINISHED, self.__on_finish)
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.__on_changed)

        self.__child = None

    def add_page(self, page):
        if self.m_pages:
            previous_page = self.m_pages[-1]
            page.SetPrev(previous_page)
            previous_page.SetNext(page)
        self.m_pages.append(page)

    def __on_cancle(self, event):
        if self.__child and self.__child.isalive():
            self.__child.send("\n")
            self.__child.close(force=True)
        subprocess.check_call("sudo /etc/init.d/lirc start", shell=True)
        temp_file = "../configs/remote/NEC_template.conf.conf"
        if os.path.exists(temp_file):
            os.remove(temp_file)

    def __on_finish(self, event):
        if self.__child and self.__child.isalive():
            self.__child.send("\n")
            self.__child.close(force=True)
        subprocess.check_call("sudo /etc/init.d/lirc start", shell=True)

    def __on_changed(self, event):
        cur_page = self.GetCurrentPage()
        if cur_page.GetId() == self.key_page.GetId():
            self.__child = pexpect.spawn("irrecord -d /dev/lirc0 ../configs/remote/NEC_template.conf -n")
            index = self.__child.expect(["RETURN", pexpect.EOF, pexpect.TIMEOUT])
            if index == 0:
                self.__child.send("\n")
                index = self.__child.expect(["<ENTER>", pexpect.EOF, pexpect.TIMEOUT])
                if index != 0:
                    self.__child.close(force=True)
            else:
                self.__child.close(force=True)
            cur_page.set_new_remote_name(cur_page.GetPrev().m_textCtrl.GetValue())
            cur_page.set_shell_controller(self.__child)
        elif cur_page.GetId() == self.remote_page.GetId():
            subprocess.check_call("sudo /etc/init.d/lirc stop", shell=True)

    def run(self):
        self.RunWizard(self.remote_page)
        self.Destroy()


if __name__ == "__main__":
    app = wx.App(False)
    wizard = WizardNewKey(None)
    wizard.run()
    app.MainLoop()
