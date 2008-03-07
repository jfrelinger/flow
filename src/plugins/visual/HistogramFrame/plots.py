#!/usr/bin/env python

"""
A demonstration of creating a matlibplot window from within wx.
A resize only causes a single redraw of the panel.
The WXAgg backend is used as it is quicker.

Edward Abraham, Datamine, April, 2006
(works with wxPython 2.6.1, Matplotlib 0.87 and Python 2.4)
"""

import matplotlib

matplotlib.interactive(False)
#Use the WxAgg back end. The Wx one takes too long to render
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure
#used in the particular example
from matplotlib.numerix import arange, sin, cos, pi
import wx
import os

class NoRepaintCanvas(FigureCanvasWxAgg):
    """We subclass FigureCanvasWxAgg, overriding the _onPaint method, so that
    the draw method is only called for the first two paint events. After that,
    the canvas will only be redrawn when it is resized.
    """
    def __init__(self, *args, **kwargs):
        FigureCanvasWxAgg.__init__(self, *args, **kwargs) #IGNORE:W0142
        self._drawn = 0 

    def _onPaint(self, evt): #IGNORE:W0613
        """
        Called when wxPaintEvt is generated
        """
        if not self._isRealized:
            self.realize()
        if self._drawn < 2:
            self.draw(repaint = False)
            self._drawn += 1
        self.gui_repaint(drawDC=wx.PaintDC(self))

class PlotPanel(wx.Panel):
    """
    The PlotPanel has a Figure and a Canvas. OnSize events simply set a 
    flag, and the actually redrawing of the
    figure is triggered by an Idle event.
    """
    def __init__(self, parent, id = -1, color = None, \
        dpi = None, style = wx.NO_FULL_REPAINT_ON_RESIZE, **kwargs):
        # wx.Panel.__init__(self, parent, id = id, style = style, **kwargs)
        super(PlotPanel, self).__init__(parent, id, style = style, **kwargs)
        self.figure = Figure(None, dpi)
        # self.canvas = NoRepaintCanvas(self, -1, self.figure)
        self.canvas = FigureCanvasWxAgg(self, -1, self.figure)
        self.SetColor(color)
        self.Bind(wx.EVT_IDLE, self._onIdle)
        self.Bind(wx.EVT_SIZE, self._onSize)
        self._resizeflag = True
        self._SetSize()

    def SetColor(self, rgbtuple):
        """Set figure and canvas colours to be the same"""
        if not rgbtuple:
            rgbtuple = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE).Get()
        col = [c/255.0 for c in rgbtuple]
        self.figure.set_facecolor(col)
        self.figure.set_edgecolor(col)
        self.canvas.SetBackgroundColour(wx.Colour(*rgbtuple))

    def _onSize(self, event): #IGNORE:W0613
        """resize event"""
        self._resizeflag = True

    def _onIdle(self, evt): #IGNORE:W0613
        """idle event"""
        if self._resizeflag:
            self._resizeflag = False
            self._SetSize()
            self.draw()

    def _SetSize(self, pixels = None):
        """
        This method can be called to force the Plot to be a desired size, which defaults to
        the ClientSize of the panel
        """
        if not pixels:
            pixels = self.GetClientSize()
        self.canvas.SetSize(pixels)
        self.figure.set_size_inches(pixels[0]/self.figure.get_dpi(),
        pixels[1]/self.figure.get_dpi())

    def draw(self):
        """Where the actual drawing happens"""
        pass

    def export(self):
        """Export to graphics filetype with extension ext."""
        if hasattr(self, 'subplot'):
            wildcard = "Portable Network Graphics (*.png)|*.png|" \
                "Postscript (*.ps)|*.ps|" \
                "Encapsulated Postscript (*.eps)|*.eps"
            dialog = wx.FileDialog(None, "Export Graphics", os.getcwd(),
                                   "", wildcard, wx.SAVE|wx.OVERWRITE_PROMPT)
            if dialog.ShowModal() == wx.ID_OK:
                #print dialog.GetPath()
                path = dialog.GetPath()
                if path.split('.')[-1] in ['png', 'ps', 'eps']:
                    ext = ''
                else:
                    i = dialog.GetFilterIndex()
                    ext = ['.png', '.ps', '.eps'][i]
                self.subplot.get_figure().savefig(path + ext)
            dialog.Destroy()
        else:
            dialog = wx.MessageBox("No graphic to export from this frame.")
            dialog.Destroy()
    
class SpeedPlotPanel(PlotPanel):
    """An example plotting panel. The only method that needs 
    overriding is the draw method"""
    def __init__(self, model, *args, **kwargs):
        super(SpeedPlotPanel, self).__init__(*args, **kwargs)
        self.model = model
    
    def draw(self):
        """Draw on the panel"""
        if not hasattr(self, 'subplot'):
            self.subplot = self.figure.add_subplot(111)
        # wx.PaintDC(self).Clear()
        self.subplot.clear()
        speeds = [cell.speed for cell in self.model.cells]
        self.subplot.set_title("Cell speed distribution", fontsize = 12)
        try:
            self.subplot.hist(speeds, 20, normed=True)
        except ValueError: #IGNORE:W0704
            pass
  

class CountPlotPanel(PlotPanel):
    """An example plotting panel. The only method that needs 
      overriding is the draw method"""
    def __init__(self, model, *args, **kwargs):
        super(CountPlotPanel, self).__init__(*args, **kwargs) #IGNORE:W0142
        self.model = model
        self.x = []
        self.y = []
    
    def draw(self):
        """Draw the panel"""
        if not hasattr(self, 'subplot'):
            self.subplot = self.figure.add_subplot(111)
        # wx.PaintDC(self).Clear()
        self.subplot.clear()
    
        self.x.append(self.model.time)
        self.y.append(len(self.model.cells))
        self.subplot.set_title("Cell counts", fontsize = 16)
        self.subplot.set_xlabel("Time", fontsize = 14)
        self.subplot.set_ylabel("Counts", fontsize = 14)
        try:
            self.subplot.plot(self.x, self.y, 'r-')
        except ValueError: #IGNORE:W0704
            pass
  
    def clear(self):
        """clear the panel"""
        self.subplot.clear()
        self.subplot.axis([0, 1, 0, 1])
        self.x = []
        self.y = []

class ContourPlotPanel(PlotPanel):
    """Panel for Contour Plots"""
    def __init__(self, model, *args, **kwargs):
        super(ContourPlotPanel, self).__init__(*args, **kwargs) #IGNORE:W0142
        self.model = model
    
    def draw(self):
        """Draw the contour plot"""
        if not hasattr(self, 'subplot'):
            self.subplot = self.figure.add_subplot(111)
        self.subplot.clear()

        delta = 0.025
        x = p.arange(-3.0, 3.0, delta)
        y = p.arange(-2.0, 2.0, delta)
        X, Y = p.meshgrid(x, y)
        Z1 = p.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
        Z2 = p.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
        # difference of Gaussians
        Z = 10.0 * (Z2 - Z1)

        self.subplot.contourf(X, Y, Z)
        self.subplot.set_title("Cytokine contour", fontsize = 12)
        self.subplot.set_xlabel('X')
        self.subplot.set_ylabel('Y')

if __name__ == '__main__':
    class DemoPlotPanel(PlotPanel):
        """An example plotting panel. The only method that needs 
        overriding is the draw method"""
        def draw(self):
            """Drawing"""
            if not hasattr(self, 'subplot'):
                self.subplot = self.figure.add_subplot(111)
            theta = arange(0, 45*2*pi, 0.02)
            rad = (0.8*theta/(2*pi)+1)
            r = rad*(8 + sin(theta*7+rad/1.8))
            x = r*cos(theta)
            y = r*sin(theta)
            #Now draw it
            self.subplot.plot(x, y, '-r')
            #Set some plot attributes
            self.subplot.set_title("A polar flower (%s points)"%len(x),
                                   fontsize = 12)
            self.subplot.set_xlabel("Flower is from  http://www.physics.emory.edu/~weeks/ideas/rose.html",
                                    fontsize = 8)
            self.subplot.set_xlim([-400, 400])
            self.subplot.set_ylim([-400, 400])


    app = wx.PySimpleApp(0)
    #Initialise a frame ...
    frame = wx.Frame(None, -1, 'WxPython and Matplotlib')
    #Make a child plot panel...
    panel = DemoPlotPanel(frame)

    #Put it in a sizer ...   
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    panel.SetSizer(sizer)
    sizer.SetItemMinSize(panel, 300, 300)
    panel.Fit()
    panel._SetSize() #IGNORE:W0212
    #And we are done ...    
    frame.Show()
    app.MainLoop()
