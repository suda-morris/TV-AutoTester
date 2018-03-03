# -*- coding:utf-8 -*-
import ConfigParser
import json
import re

import wx
import wx.grid
import wx.xrc


class DialogNewKeyOrder(wx.Dialog):
    def __load_key_conf(self):
        cf = ConfigParser.ConfigParser()
        cf.read("../configs/remote/remote.ini")
        self.__remote_name = cf.get("REMOTE", "name")
        with open('../configs/remote/cvte_factory.conf') as remote_file:
            lines = remote_file.readlines()
        lines = [line for line in lines if not line.startswith("#") and line != "\r\n" and line != "\n"]
        self.remote_keys = []
        for line in lines:
            if line.find(self.__remote_name) == -1:
                lines = lines[1:]
            else:
                break
        for line in lines:
            if line.find("KEY_") == -1:
                lines = lines[1:]
            else:
                break
        for line in lines:
            result = re.search(r"KEY_[\w]*", line)
            if result:
                self.remote_keys.append(result.group())
        self.remote_keys.sort()

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"新增功能测试", pos=wx.DefaultPosition, size=wx.Size(300, 350),
                           style=wx.DEFAULT_DIALOG_STYLE)

        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"功能名称", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer2.Add(self.m_staticText1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_textCtrl = wx.TextCtrl(self, wx.ID_ANY, u"CG_POWER", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_textCtrl, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_button = wx.Button(self, wx.ID_ANY, u"保存", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_button, 0, wx.ALL, 5)

        bSizer1.Add(bSizer2, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"按键顺序", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        bSizer3.Add(self.m_staticText2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_grid = wx.grid.Grid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        self.m_grid.CreateGrid(10, 1)
        self.m_grid.EnableEditing(True)
        self.m_grid.EnableGridLines(True)
        self.m_grid.EnableDragGridSize(False)
        self.m_grid.SetMargins(0, 0)

        # Columns
        self.m_grid.EnableDragColMove(False)
        self.m_grid.EnableDragColSize(True)
        self.m_grid.SetColLabelSize(30)
        self.m_grid.SetColLabelValue(0, u"按键名")
        self.m_grid.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.m_grid.EnableDragRowSize(True)
        self.m_grid.SetRowLabelSize(80)
        self.m_grid.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Label Appearance

        # Cell Defaults
        self.m_grid.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)
        bSizer3.Add(self.m_grid, 0, wx.ALL, 5)

        bSizer1.Add(bSizer3, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button.Bind(wx.EVT_BUTTON, self.__on_btn_save)
        self.m_grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.__show_key_menu)

        self.__load_key_conf()

    def __on_btn_save(self, event):
        self.__json_root = None
        with open('../configs/operations/key_order.json') as json_file:
            self.__json_root = json.load(json_file)
            row = 0
            key_list = []
            while True:
                value = self.m_grid.GetCellValue(row, 0)
                if value:
                    row += 1
                    key_list.append(value)
                else:
                    break
            self.__json_root[self.m_textCtrl.GetLineText(0)] = key_list
        with open('../configs/operations/key_order.json', 'w') as json_file:
            json_file.write(json.dumps(self.__json_root))
        self.EndModal(wx.ID_OK)

    def __show_key_menu(self, event):
        self.row = event.GetRow()
        self.col = event.GetCol()
        self.m_grid.GoToCell(self.row, self.col)

        self.m_menu = wx.Menu()
        for key in self.remote_keys:
            menu_item = wx.MenuItem(self.m_menu, wx.ID_ANY, key, wx.EmptyString, wx.ITEM_NORMAL)
            self.m_menu.AppendItem(menu_item)
            self.Bind(wx.EVT_MENU, self.on_menu_selection, id=menu_item.GetId())

        self.PopupMenu(self.m_menu)
        self.m_menu.Destroy()

    def on_menu_selection(self, event):
        menu = event.GetEventObject()
        menu_item = menu.FindItemById(event.GetId())
        self.m_grid.SetCellValue(self.row, self.col, menu_item.GetLabel())


class PanelKeyOrder(wx.Panel):
    def __load_db_keys(self):
        self.m_treeCtrl.DeleteAllItems()
        with open('../configs/operations/key_order.json') as json_file:
            json_root = json.load(json_file)
            tree_root = self.m_treeCtrl.AddRoot(u"功能按键顺序")
            self.m_treeCtrl.SetPyData(tree_root, ('key', 'value'))
            for fun in json_root.keys():
                child = self.m_treeCtrl.AppendItem(tree_root, fun)
                self.m_treeCtrl.SetItemHasChildren(child)
                for key in json_root[fun]:
                    self.m_treeCtrl.AppendItem(child, key)

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(800, 480),
                          style=wx.TAB_TRAVERSAL)

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        sbSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"按键顺序"), wx.VERTICAL)

        fgSizer1 = wx.FlexGridSizer(1, 2, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_treeCtrl = wx.TreeCtrl(sbSizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size(500, 350),
                                      wx.TR_DEFAULT_STYLE)
        fgSizer1.Add(self.m_treeCtrl, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        gSizer2 = wx.GridSizer(2, 1, 0, 0)

        self.m_btn_new = wx.Button(sbSizer.GetStaticBox(), wx.ID_ANY, u"新建", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.m_btn_new, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_btn_save = wx.Button(sbSizer.GetStaticBox(), wx.ID_ANY, u"保存", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.m_btn_save, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        fgSizer1.Add(gSizer2, 1, wx.EXPAND, 5)

        sbSizer.Add(fgSizer1, 1, wx.EXPAND, 5)

        self.SetSizer(sbSizer)
        self.Layout()

        # Connect Events
        self.Bind(wx.EVT_PAINT, self.__on_paint)
        self.m_btn_new.Bind(wx.EVT_BUTTON, self.__on_btn_new_clicked)
        self.m_btn_save.Bind(wx.EVT_BUTTON, self.__on_btn_save_clicked)

        self.__load_db_keys()

    def __on_btn_new_clicked(self, event):
        dialog = DialogNewKeyOrder(self)
        result = dialog.ShowModal()
        if result == wx.ID_OK:
            print "OK"
        else:
            print "Cancel"
        dialog.Destroy()
        self.Refresh()

    def __on_btn_save_clicked(self, event):
        self.Refresh()

    def __on_paint(self, event):
        self.__load_db_keys()
