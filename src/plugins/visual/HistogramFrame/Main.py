"""Need type, Plot() and ModelUpdate()."""
import wx
import sys
import os
from plots import PlotPanel
from numpy import cumsum

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

        self.widget = HistogramPanel(None, 1, self)
        self.widget.draw()
        
        self.MenuBar = wx.MenuBar()
        self.FileMenu = wx.Menu()
        self.MenuBar.Append(self.FileMenu, "File")
        self.SetMenuBar(self.MenuBar)
        export = self.FileMenu.Append(-1, "Export graphics")
        self.Bind(wx.EVT_MENU, self.OnExport, export)
        self.AddMenu = wx.Menu()
        self.MenuBar.Append(self.AddMenu, "Add histograms")
        self.AddHist = self.AddMenu.Append(-1, "Add New Histogram")
        self.Bind(wx.EVT_MENU, self.OnAddHist, self.AddHist)
        self.AddMenu.AppendSeparator()
        self.ExtraHists = []

        self.RadioButtons(['none'])
        self.box.Add(self.panel,0,wx.EXPAND)
        self.box.Add(self.widget,1,wx.EXPAND)
        self.SetSizer(self.box)
        self.Show()
    
    def OnAddHist(self, event):
        if not hasattr(self.widget, 'hists'):
            self.widget.hists = {}
        choices = self.model.GetDataGroups()
        dialog = wx.MultiChoiceDialog(None, "Chose data to add to histogram", 'choices', choices)
        if dialog.ShowModal() == wx.ID_OK:
            #print [choices[i] for i in dialog.GetSelections()]
            for groupName in [choices[i]  for i in dialog.GetSelections()]:
                #print groupName
                self.model.SelectGroupByPath(groupName)
                data = self.model.GetCurrentData()
                print data
                if hasattr(data.attrs, 'fields'):
                    newhist = data[:,data.getAttr('fields').index(self.radioX.GetStringSelection())]
                    #self.hists[group] = newhist
                    newmenu = self.AddMenu.AppendCheckItem(-1, groupName)
                    newmenu.Check(True)
                    self.Bind(wx.EVT_MENU, self.OnHistSelect, newmenu)
                    self.widget.hists[groupName]= newhist
                    self.widget.draw()
    
    def OnHistSelect(self, event):
        pass
    
    def OnExport(self, event):
        print "Test export graphics"
        self.widget.export()

    def RadioButtons(self,list):
        try:
            self.radioX.Destroy()
        except AttributeError:
            pass
        self.radioX = wx.RadioBox(self.panel,-1,"Marker to plot",(10,10), wx.DefaultSize, list,1,wx.RA_SPECIFY_COLS)
        self.radioX.Bind(wx.EVT_RADIOBOX, self.OnControlSwitch)

    def UpdateHistogram(self, x):
        self.widget.x = self.model.GetCurrentData()[:,x]
        fields = self.model.GetCurrentData().getAttr('fields')
        self.widget.name = fields[x]
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
        self.x = x
        self.hists = {}
  
    def draw(self):
        if not hasattr(self, 'subplot'):
            self.subplot = self.figure.add_subplot(111)
        self.subplot.clear()
        if self.x is not None:
            self.patches = []
            n, bins, hist = self.subplot.hist(self.x, 1024)
            self.patches.append(hist)
            self.subplot.set_xlabel(str(self.name), fontsize = 12)
            for group in self.hists.keys():
                n, bins, hist = self.subplot.hist(self.hists[group], 1024)
                self.patches.append(hist)
            sizes = [len(patch) for patch in self.patches]
            sizes.insert(0,0)
            print sizes
            splits = cumsum(sizes)
            upper = len(self.patches)
            self.subplot.patches = self.patches[splits[0]:splits[1]]
        self.Refresh()
        

