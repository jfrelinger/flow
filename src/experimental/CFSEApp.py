"""Simple GUI interface to CFSE fitting functions"""

import wx
import numpy

class Model(object):
    """Model to store and manipulate data."""
    def __init__(self):
        self.sample = None
        self.control = None

class CFSEApp(wx.App):
    """Main application for fitting normals to CFSE data."""
    def __init__(self, redirect=False):
        wx.App.__init__(self, redirect)

    def OnInit(self):
        return True

class MainFrame(wx.Frame):
    """Main frame for CFSE application."""
    def __init__(self, title="", pos=wx.DefaultPosition, size=wx.DefaultSize):
        wx.Frame.__init__(self, None, -1, title, pos, size)
        fileMenu = wx.Menu()
        load_sample = fileMenu.Append(1, "Load sample data")
        load_control = fileMenu.Append(1, "Load control data")
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)
        self.CreateStatusBar()
        self.SetStatusText("Ready for fitting")
        self.Bind(wx.EVT_MENU, self.OnLoadSample, load_sample)
        self.Bind(wx.EVT_MENU, self.OnLoadControl, load_control)

        self.model = Model()

    def read_data(self, file):
        """Simple data reader.

        Expects floating point numbers in plain text separated by white space.
        """
        return numpy.array(map(float, open(file).read().strip().split()))

    def OnLoadData(self, event):
        """Generic data loader."""
        dlg = wx.FileDialog(self, 
                            wildcard="Text files (*.txt)|*.txt|All files (*.*)|*.*",
                            defaultDir='.',
                            style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            file = dlg.GetPath()
        else:
            file = None
        dlg.Destroy()
        return file

    def OnLoadSample(self, event):
        """Load a sample file for fitting."""
        file = self.OnLoadData(event)
        self.model.sample = self.read_data(file)

    def OnLoadControl(self, event):
        """Load a control file with well-defined peaks."""
        file = self.OnLoadData(event)
        self.model.control = self.read_data(file)

if __name__ == '__main__':
    app = CFSEApp()
    frame = MainFrame("CFSE fitting application")
    frame.Show(True)
    app.MainLoop()
