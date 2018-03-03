# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 28 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class DialogYesNo
###########################################################################

class DialogYesNo ( wx.Dialog ):

    def __init__( self, parent, text ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

        # self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        top_sizer = wx.BoxSizer( wx.VERTICAL )

        self.text = wx.StaticText( self, wx.ID_ANY, text, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.text.Wrap( -1 )
        top_sizer.Add( self.text, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        sizer_button = wx.BoxSizer( wx.HORIZONTAL )

        self.button_yes = wx.Button( self, wx.ID_ANY, u"是", wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer_button.Add( self.button_yes, 0, wx.ALL, 5 )

        self.button_no = wx.Button( self, wx.ID_ANY, u"否", wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer_button.Add( self.button_no, 0, wx.ALL, 5 )


        top_sizer.Add( sizer_button, 1, wx.ALIGN_CENTER_HORIZONTAL, 5 )


        self.SetSizer( top_sizer )
        self.Layout()
        top_sizer.Fit( self )

        self.Centre( wx.BOTH )

        # Connect Events
        self.button_yes.Bind( wx.EVT_BUTTON, self.click_yes )
        self.button_no.Bind( wx.EVT_BUTTON, self.click_no )

    def __del__( self ):
        pass

    # Virtual event handlers, overide them in your derived class
    def click_yes( self, event ):
        self.EndModal(wx.ID_YES)
        event.Skip()

    def click_no( self, event ):
        self.EndModal(wx.ID_NO)
        event.Skip()
