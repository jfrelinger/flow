"""Need type, Plot() and ModelUpdate()."""
import wx
import sys
import os
from plots import PlotPanel

from VizFrame import VizFrame

class HistogramFrame(VizFrame):
    """frame for viewing histograms"""
    type = 'Histogram'

    def __init__(self, parent=None, id=-1,
                 pos=wx.DefaultPosition,
                 title="Histogram"):
        VizFrame.__init__(self, parent, id, pos, title)
        self.box = wx.BoxSizer(wx.HORIZONTAL)
        self.panel = wx.Panel(self,-1)

        self.widget = HistogramPanel([1], 1, self)
        self.widget.draw()
        
        self.MenuBar = wx.MenuBar()
        self.FileMenu = wx.Menu()
        self.MenuBar.Append(self.FileMenu, "File")
        self.AddMenu = wx.Menu()
        self.MenuBar.Append(self.AddMenu, "Add histograms")
        self.SetMenuBar(self.MenuBar)
        export = self.FileMenu.Append(-1, "Export graphics")
        self.AddHist = self.AddMenu.Append(-1, "Add New Histogram")
        self.Bind(wx.EVT_MENU, self.OnExport, export)
        self.Bind(wx.EVT_MENU, self.OnAddHist, self.AddHist)

        self.RadioButtons(['none'])
        self.box.Add(self.panel,0,wx.EXPAND)
        self.box.Add(self.widget,1,wx.EXPAND)
        self.SetSizer(self.box)
        self.Show()
        
    def OnExport(self, event):
        print "Test export graphics"
        self.widget.export()
        
    def OnAddHist(self, event):
        pass

    def RadioButtons(self,list):
        try:
            self.radioX.Destroy()
        except AttributeError:
            pass
        self.radioX = wx.RadioBox(self.panel,-1,"Marker to plot",(10,10), wx.DefaultSize, list,1,wx.RA_SPECIFY_COLS)
        self.radioX.Bind(wx.EVT_RADIOBOX, self.OnControlSwitch)

    def UpdateHistogram(self, x):
        #self.widget.x = self.model.GetCurrentData()[:,x]
        fields = self.model.GetCurrentData().getAttr('fields')
        #self.widget.name = fields[x]
        self.widget.xs = {fields[x]: self.model.GetCurrentData()[:,x]}
        self.widget.draw()
        
    def Plot(self):
        try:
            if self.model.ready:
                self.RadioButtons(self.model.GetCurrentData().getAttr('fields'))
                self.UpdateHistogram(self.radioX.GetSelection())
            else:
                pass
        except AttributeError:
            pass

    def OnControlSwitch(self,event):
        self.UpdateHistogram(self.radioX.GetSelection())
    
    def ModelUpdate(self,model):
        self.model = model
        self.Plot()

class HistogramPanel(PlotPanel):
    """An example plotting panel. The only method that needs 
    overriding is the draw method"""
    def __init__(self, x, name='', *args):
        super(HistogramPanel, self).__init__(*args)
        self.xs = {name: x}
  
    def draw(self):
        if not hasattr(self, 'subplot'):
            self.subplot = self.figure.add_subplot(111)
        self.subplot.clear()
        if self.xs is not None:
            print self.xs
            for name, x in self.xs.items():
                self.subplot.hist(x, 1024)
                self.subplot.set_xlabel(str(name), fontsize = 12)
        self.Refresh()

