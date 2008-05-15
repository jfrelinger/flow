import wx

class annotateFrame(wx.Frame):
    def __init__(self, node, node_name = 'default', txt = ''):
        wx.Frame.__init__(self, None, -1, "Annotations for " + node_name,style = wx.DEFAULT_FRAME_STYLE | wx.RESIZE_BORDER )
        self.panel = wx.Panel(self, -1, size = self.GetSize() )
        self.textBox = wx.TextCtrl(self.panel, -1, txt, style= wx.TE_MULTILINE)
        self.okBtn = wx.Button(self.panel, id=wx.ID_OK)
        self.cancelBtn = wx.Button(self.panel, id=wx.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.OnOkay, self.okBtn)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancelBtn)
        
        self.node = node
        
        #layout
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(self.textBox,1,wx.EXPAND)
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        btnsizer.Add((10,10),1)
        btnsizer.Add(self.cancelBtn)
        btnsizer.Add((10,10))
        btnsizer.Add(self.okBtn)
        btnsizer.Add((10,10))
        mainsizer.Add(btnsizer, 0, wx.EXPAND)
        self.panel.SetSizer(mainsizer)
        mainsizer.Fit(self)
        
    def OnOkay(self, event):
        """
        do aproprate action on okay button press
        """
        # need to do stuff here
        self.node.setAttr('annotation', self.textBox.GetValue())
                          
        self.Destroy()
        
    def OnCancel(self, event):
        """
        cancel button handler
        """
        self.Destroy()
        
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    bar = annotateFrame('bar', 'test')
    bar.Show()
    app.MainLoop()