# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 28 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import sys
import os
from os import listdir
from os.path import isfile
import json
import wx
import wx.xrc
from wx.lib.masked import NumCtrl
from ui.dialog_yes_no import DialogYesNo

###########################################################################
## Class PanelControlProcess
###########################################################################
STR_DEVICE = u'设备'
STR_FUNCTION = u'功能'
STR_REPEAT_TIMES = u'重复次数'
STR_DELAY = u'延时'
STR_DELAY_SECONDS = u'延时秒数'
PATH_PROCESS = '../configs/process/'

class PanelControlProcess ( wx.Panel ):

    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 800,480 ), style = wx.TAB_TRAVERSAL )

        top_box_sizer = wx.BoxSizer( wx.HORIZONTAL )

        self.list_operation = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 500,480 ), wx.LC_REPORT )
        top_box_sizer.Add( self.list_operation, 0, wx.ALL, 5 )

        right_sizer = wx.WrapSizer( wx.VERTICAL )

        sizer_device = wx.BoxSizer( wx.HORIZONTAL )

        self.text_device = wx.StaticText( self, wx.ID_ANY, STR_DEVICE + u"：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.text_device.Wrap( -1 )
        sizer_device.Add( self.text_device, 0, wx.ALL, 5 )

        choice_deviceChoices = []
        self.choice_device = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), choice_deviceChoices, wx.CB_SORT )
        self.choice_device.SetSelection( 0 )
        sizer_device.Add( self.choice_device, 1, wx.EXPAND, 5 )


        right_sizer.Add( sizer_device, 1, wx.BOTTOM|wx.EXPAND|wx.TOP, 5 )

        sizer_operation = wx.BoxSizer( wx.HORIZONTAL )

        self.text_operation = wx.StaticText( self, wx.ID_ANY, STR_FUNCTION + u"：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.text_operation.Wrap( -1 )
        sizer_operation.Add( self.text_operation, 0, wx.ALL, 5 )

        choice_operationChoices = []
        self.choice_operation = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_operationChoices, wx.CB_SORT )
        self.choice_operation.SetSelection( 0 )
        sizer_operation.Add( self.choice_operation, 1, wx.EXPAND, 5 )


        right_sizer.Add( sizer_operation, 1, wx.BOTTOM|wx.TOP|wx.EXPAND, 5 )

        sizer_times = wx.BoxSizer( wx.HORIZONTAL )

        self.text_times = wx.StaticText( self, wx.ID_ANY, STR_REPEAT_TIMES + u'：', wx.DefaultPosition, wx.DefaultSize, 0 )
        self.text_times.Wrap( -1 )
        sizer_times.Add( self.text_times, 0, wx.ALL, 5 )


        right_sizer.Add( sizer_times, 1, wx.BOTTOM|wx.TOP|wx.EXPAND, 5 )

        sizer_add_remove = wx.BoxSizer( wx.HORIZONTAL )

        self.button_add = wx.Button( self, wx.ID_ANY, u"插入", wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer_add_remove.Add( self.button_add, 1, wx.ALL, 5 )

        self.button_remove = wx.Button( self, wx.ID_ANY, u"删除", wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer_add_remove.Add( self.button_remove, 1, wx.ALL, 5 )


        right_sizer.Add( sizer_add_remove, 1, wx.BOTTOM|wx.TOP|wx.EXPAND, 5 )

        sizer_file = wx.BoxSizer( wx.HORIZONTAL )

        self.text_file = wx.StaticText( self, wx.ID_ANY, u"流程控制文件：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.text_file.Wrap( -1 )
        sizer_file.Add( self.text_file, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.button_delete_file = wx.Button( self, wx.ID_ANY, u"删除文件", wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer_file.Add( self.button_delete_file, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        right_sizer.Add( sizer_file, 1, wx.EXPAND, 5 )

        choice_fileChoices = []
        self.choice_file = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_fileChoices, wx.CB_SORT )
        self.choice_file.SetSelection( 0 )
        self.choice_file.SetMinSize( wx.Size( 150,-1 ) )

        right_sizer.Add( self.choice_file, 0, wx.EXPAND, 5 )

        self.text_save_file = wx.StaticText( self, wx.ID_ANY, u"保存为文件：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.text_save_file.Wrap( -1 )
        right_sizer.Add( self.text_save_file, 0, wx.ALL, 5 )

        self.text_ctrl_file_name = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.text_ctrl_file_name.SetMinSize( wx.Size( 150,-1 ) )

        right_sizer.Add( self.text_ctrl_file_name, 1, wx.ALL|wx.EXPAND, 5 )

        sizer_file_control = wx.BoxSizer( wx.HORIZONTAL )

        self.button_save = wx.Button( self, wx.ID_ANY, u"保存", wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer_file_control.Add( self.button_save, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.button_rename = wx.Button( self, wx.ID_ANY, u"重命名", wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer_file_control.Add( self.button_rename, 1, wx.ALL, 5 )


        right_sizer.Add( sizer_file_control, 1, wx.EXPAND, 5 )


        top_box_sizer.Add( right_sizer, 1, wx.ALL|wx.EXPAND, 10 )


        self.SetSizer( top_box_sizer )
        self.Layout()

        # Connect Events
        self.choice_device.Bind( wx.EVT_CHOICE, self.get_operation_choices )
        self.button_add.Bind( wx.EVT_BUTTON, self.add_item )
        self.button_remove.Bind( wx.EVT_BUTTON, self.remove_item )
        self.button_delete_file.Bind( wx.EVT_BUTTON, self.delete_file )
        self.choice_file.Bind( wx.EVT_CHOICE, self.load_file )
        self.button_save.Bind( wx.EVT_BUTTON, self.save_file )
        self.button_rename.Bind( wx.EVT_BUTTON, self.rename_file )
        # 添加重复次数/延时秒数输入框
        self.num_ctrl_times = NumCtrl(
            self, value = 1, fractionWidth = 0, allowNegative = False, allowNone = True)
        sizer_times.Add(self.num_ctrl_times, 0, wx.EXPAND, 5)
        # NumCtrl里设置为禁止为空容易触发BUG，故用这个事件来弥补这个问题
        self.num_ctrl_times.Bind(wx.EVT_KILL_FOCUS, self.set_default_value)
        # 初始化下拉列表的值
        self.__dict_operation = {}
        self.__read_devices_and_operations()
        self.choice_device.Set(self.__dict_operation.keys())
        self.choice_device.SetSelection(0)
        self.get_operation_choices(wx.CommandEvent())
        self.__files = []
        self.__refresh_files_list()
        self.choice_file.SetSelection(0)
        self.load_file(wx.CommandEvent())
        self.__page_number = parent.GetPageCount()

    def __del__( self ):
        pass

    # Virtual event handlers, overide them in your derived class
    def on_panel_changed(self, event):
        if event.GetEventObject().GetSelection() == self.__page_number:
            # TODO:切换标签页时检查文件更新
            pass

    def get_operation_choices( self, event ):
        device = self.choice_device.GetStringSelection()
        self.choice_operation.Set(self.__dict_operation[device])
        self.choice_operation.SetSelection(0)
        self.text_times.SetLabelText(
            (STR_DELAY_SECONDS if device == STR_DELAY else STR_REPEAT_TIMES) + u'：')
        self.num_ctrl_times.SetFractionWidth(3 if device == STR_DELAY else 0)
        if self.num_ctrl_times.GetValue() is None:
            self.num_ctrl_times.SetValue(1)
        event.Skip()

    def add_item( self, event ):
        index = self.list_operation.GetFirstSelected()
        index = sys.maxint if index == -1 else index
        row = self.list_operation.InsertStringItem(index,
                                                   self.choice_device.GetStringSelection())
        self.list_operation.SetStringItem(row, 1, self.choice_operation.GetStringSelection())
        self.list_operation.SetStringItem(row, 2, str(self.num_ctrl_times.GetValue()))
        self.list_operation.EnsureVisible(row)
        event.Skip()

    def remove_item( self, event ):
        # 有选中的时候，删除全部被选中的，否则删除最后一个
        index = self.list_operation.GetFirstSelected()
        if index == -1: index = self.list_operation.GetItemCount() - 1
        while index != -1:
            self.list_operation.EnsureVisible(index)
            self.list_operation.DeleteItem(index)
            index = self.list_operation.GetFirstSelected()
        event.Skip()

    def delete_file( self, event ):
        file_name = self.choice_file.GetStringSelection()
        if not file_name: return
        dialog = DialogYesNo(self, u'是否删除文件 ' + file_name + u' ？')
        result = dialog.ShowModal()
        if result != wx.ID_YES: return
        os.remove(os.path.join(PATH_PROCESS, file_name))
        self.__refresh_files_list()
        self.choice_file.SetSelection(0)
        self.load_file(wx.CommandEvent())
        event.Skip()

    def load_file( self, event ):
        self.list_operation.ClearAll()
        self.list_operation.InsertColumn(0, STR_DEVICE)
        self.list_operation.InsertColumn(1, STR_FUNCTION)
        self.list_operation.InsertColumn(2, STR_REPEAT_TIMES)
        file_name = self.choice_file.GetStringSelection()
        if not file_name: return
        self.text_ctrl_file_name.SetValue(file_name)
        process_file = os.path.join(PATH_PROCESS, file_name)
        process = []
        with open(process_file, 'r') as f:
            process = f.readlines()
        # 去除注释和空行
        process = [i for i in process
                   if not i.startswith(';') and i != '\r\n' and i != '\n']
        # 去掉换行符
        for i, v in enumerate(process):
            if v.endswith('\r\n'):
                v = v[:-2]
            elif v.endswith('\n'):
                v = v[:-1]
            v = v.split()
            if v[0] == 'd':
                self.list_operation.InsertStringItem(sys.maxint, STR_DELAY)
                self.list_operation.SetStringItem(i, 1, STR_DELAY)
                self.list_operation.SetStringItem(i, 2, v[1])
            else:
                self.list_operation.InsertStringItem(sys.maxint, v[0])
                self.list_operation.SetStringItem(i, 1, v[1])
                self.list_operation.SetStringItem(i, 2, v[2] if len(v) >= 3 else '1')
        self.list_operation.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.list_operation.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.list_operation.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        event.Skip()

    def save_file( self, event ):
        process = []
        for i in xrange(self.list_operation.GetItemCount()):
            operation = []
            for j in xrange(self.list_operation.GetColumnCount()):
                operation.append(self.list_operation.GetItemText(i, j))
            if operation[0] == STR_DELAY:
                operation = ['d', operation[2]]
            process.append(' '.join(operation))
        file_name = self.text_ctrl_file_name.GetValue()
        if not file_name: return
        with open(os.path.join(PATH_PROCESS, file_name), 'w') as file:
            file.write('\r\n'.join(process))
        self.__refresh_files_list()
        for i, v in enumerate(self.choice_file.GetStrings()):
            if v == file_name:
                self.choice_file.SetSelection(i)
                break
        event.Skip()

    def rename_file( self, event ):
        file_name = self.choice_file.GetStringSelection()
        if not file_name: return
        os.remove(os.path.join(PATH_PROCESS, file_name))
        self.save_file(wx.CommandEvent)
        event.Skip()

    def set_default_value(self, event):
        if self.num_ctrl_times.GetValue() is None:
            self.num_ctrl_times.SetValue(1)
        event.Skip()
    # Virtual event handlers end

    def __read_devices_and_operations(self):
        with open('../configs/operations/success_fail.json') as json_file:
            self.__dict_operation = json.load(json_file)
        # 转换为（设备，功能列表）的字典
        for i in self.__dict_operation:
            self.__dict_operation[i] = [j['operation'] for j in self.__dict_operation[i]]
        # IR设备的功能以key_order.json为准
        if 'IR' in self.__dict_operation:
            with open('../configs/operations/key_order.json') as json_file:
                self.__dict_operation['IR'] = json.load(json_file).keys()
        self.__dict_operation[STR_DELAY] = [STR_DELAY]

    def __refresh_files_list(self):
        path = '../configs/process/'
        # 文件与文件修改时间的字典，修改时间用于检查文件更新
        self.__files = {f: os.stat(os.path.join(path, f)).st_mtime
                        for f in listdir(path) if isfile(os.path.join(path, f))}
        self.choice_file.Set(self.__files.keys())
