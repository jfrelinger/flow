import wx
import factory

class BlockWindow(wx.Panel): 
    def __init__(self, parent, ID=-1, label="", 
                 pos=wx.DefaultPosition, size=(350, 25)): 
        wx.Panel.__init__(self, parent, ID, pos, size, 
                          wx.RAISED_BORDER, label) 
        self.label = label 
        self.SetBackgroundColour("white") 
        self.SetMinSize(size) 
        self.Bind(wx.EVT_PAINT, self.OnPaint) 

    def OnPaint(self, evt): 
        sz = self.GetClientSize() 
        dc = wx.PaintDC(self) 
        w,h = dc.GetTextExtent(self.label) 
        dc.SetFont(self.GetFont()) 
        dc.DrawText(self.label, (sz.width-w)/2, (sz.height-h)/2) 

class ParameterDialog(wx.Dialog):
    def __init__(self, params, data, desc=''):
        """params is a list of (name, validator, defaults) tuples."""
        wx.Dialog.__init__(self, None, -1, "Specify parameters")

        text = self.MakeStaticBoxSizer('Function', [desc])
        # create the entries
        labels = []
        entries = []
        for name, validator, default in params:
            labels.append(wx.StaticText(self, -1, name + ': '))
            entries.append(wx.TextCtrl(self, validator=factory.factory('validators', validator, data, name), value=default))
        okay = wx.Button(self, wx.ID_OK)
        okay.SetDefault()
        cancel = wx.Button(self, wx.ID_CANCEL)

        # layout
        fgs = wx.FlexGridSizer(len(params)+1, 2, 5, 5)
        for label, entry in zip(labels, entries):
            fgs.Add(label, 0, wx.ALIGN_RIGHT)
            fgs.Add(entry, 0, wx.EXPAND)
        fgs.AddGrowableCol(1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text, 0, wx.ALIGN_CENTRE|wx.ALL, border=10)
        #for entry in entries:
        #    sizer.Add(entry)
        sizer.Add(fgs)
        btns = wx.StdDialogButtonSizer()
        btns.Add(okay)
        btns.Add(cancel)
        sizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)

    def MakeStaticBoxSizer(self, boxlabel, itemlabels): 
        box = wx.StaticBox(self, -1, boxlabel)   
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL) 
        for label in itemlabels:                     
            bw = BlockWindow(self, label=label)   
            sizer.Add(bw, 0, wx.EXPAND | wx.ALL, 2) 
        return sizer 

class ChoiceDialog(wx.Dialog):
    def __init__(self, choices, label ="Choose markers"):
        wx.Dialog.__init__(self, None, -1, label, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)

        # create the checklist box
        self.lb = wx.CheckListBox(self, -1, choices=choices)
        okay = wx.Button(self, wx.ID_OK)
        okay.SetDefault()
        cancel = wx.Button(self, wx.ID_CANCEL)

        # layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.lb, 1, wx.EXPAND|wx.ALL, 5)
        btns = wx.StdDialogButtonSizer()
        btns.Add(okay)
        btns.Add(cancel)
        sizer.Add(btns, 0, wx.EXPAND|wx.ALL)
        self.SetSizer(sizer)
        sizer.Fit(self)

    def GetSelections(self):
        selections = []
        for i in range(self.lb.GetCount()):
            if self.lb.IsChecked(i):
                selections.append(i)
        return selections

    def SetSelections(self, selections):
        for selection in selections:
            self.lb.Check(selection)

class DBInputDialog(wx.Dialog):
    def __init__(self, params, data, desc=''):
        """params is a list of (name, validator, defaults) tuples."""
        wx.Dialog.__init__(self, None, -1, "Specify parameters")

        text =wx.StaticText(self, -1, desc)
        # create the entries
        labels = []
        entries = []
        for name, validator, default in params:
            labels.append(wx.StaticText(self, -1, name + ': '))
            entries.append(wx.TextCtrl(self, validator=factory.factory('validators', validator, data, name), value=default))
        okay = wx.Button(self, wx.ID_OK)
        okay.SetDefault()
        cancel = wx.Button(self, wx.ID_CANCEL)

        # layout
        fgs = wx.FlexGridSizer(len(params)+1, 2, 5, 5)
        for label, entry in zip(labels, entries):
            fgs.Add(label, 0, wx.ALIGN_RIGHT)
            fgs.Add(entry, 0, wx.EXPAND)
        fgs.AddGrowableCol(1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text, 0, wx.ALIGN_CENTRE|wx.ALL, border=10)
        sizer.Add(fgs)
        btns = wx.StdDialogButtonSizer()
        btns.Add(okay)
        btns.Add(cancel)
        sizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)

class SaveDialog(wx.Dialog):
    """Dialog to prompt users to save thier work"""
    def __init__(self):
        """init the dialog"""
        wx.Dialog.__init__(self, None, -1, "Save your work?", size = (300, 100))
        text = wx.StaticText(self, -1, "Save your work?")
        self.yesButton = wx.Button(self, wx.ID_YES, "Yes", pos = (15, 15))
        self.yesButton.SetDefault()
        buttonPos = (self.yesButton.GetPosition()[0]+self.yesButton.GetSize()[0]+5, 15)
        self.noButton = wx.Button(self, wx.ID_NO, "No", pos = buttonPos)
        buttonPos = (self.noButton.GetPosition()[0]+self.noButton.GetSize()[0]+5, 15)
        cancelButton = wx.Button(self, wx.ID_CANCEL, "Cancel", pos = buttonPos)
        self.Bind(wx.EVT_BUTTON, self.onButton, self.yesButton)
        self.Bind(wx.EVT_BUTTON, self.onButton, self.noButton)

    def onButton(self,event):
        """handle button events to end dialog"""
        if event.GetId() == self.yesButton.GetId():
            self.EndModal(wx.ID_YES)
        elif event.GetId() == self.noButton.GetId():
            self.EndModal(wx.ID_NO)
            
