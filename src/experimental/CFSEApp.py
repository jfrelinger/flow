"""Simple GUI interface to CFSE fitting functions"""

import wx
import numpy
import sys
sys.path.append('..')
from dialogs import ParameterDialog, ChoiceDialog

class Model(object):
    """Model to store and manipulate data."""
    def __init__(self):
        self.sample = None
        self.control = None

    def fit_data(self, inputs):
        """Fit normals to data."""
        print "Fitting data to inputs: ", inputs

    def fit_sample(self, inputs):
        """Fit normals to sample data."""
        self.data = self.sample
        self.fit_data(inputs)

    def fit_control(self, inputs):
        """Fit normals to control data."""
        self.data = self.control
        self.fit_data(inputs)

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
        load_sample = fileMenu.Append(-1, "Load sample data")
        load_control = fileMenu.Append(-1, "Load control data")
        analysisMenu = wx.Menu()
        fit_sample = analysisMenu.Append(-1, "Fit sample data")
        fit_control = analysisMenu.Append(-1, "Fit control data")
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(analysisMenu, "&Analysis")
        self.SetMenuBar(menuBar)
        self.CreateStatusBar()
        self.SetStatusText("Ready for fitting")
        self.Bind(wx.EVT_MENU, self.OnLoadSample, load_sample)
        self.Bind(wx.EVT_MENU, self.OnLoadControl, load_control)
        self.Bind(wx.EVT_MENU, self.OnFitSample, fit_sample)
        self.Bind(wx.EVT_MENU, self.OnFitControl, fit_control)

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

    def OnFitData(self, event):
        """Generic data fitting."""
        inputs = {}
        dlg = ParameterDialog([('mix_interval', 'FloatValidator', str(50.0)),
                               ('max_intervall', 'FloatValidator', str(100.0))],
                               inputs,
                               'Some information to help the fitting')
        if dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy()
        return inputs

    def OnFitSample(self, event):
        """Fit the sample data."""
        inputs = self.OnFitData(event)
        self.model.fit_sample(inputs)

    def OnFitControl(self, event):
        """Fit the control data."""
        inputs = self.OnFitData(event)
        self.model.fit_control(inputs)


if __name__ == '__main__':
    app = CFSEApp()
    frame = MainFrame("CFSE fitting application")
    frame.Show(True)
    app.MainLoop()
