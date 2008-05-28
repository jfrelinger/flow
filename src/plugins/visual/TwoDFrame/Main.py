import wx

from plots import PlotPanel
import densities2 as dens
from numpy import array, arange, mgrid, isnan, sqrt, histogram2d, min, max, take, modf
from numpy.linalg import inv
from numpy.random import randn, rand
from pylab import cm, hist, zeros
import pylab
import os
import mpl_gate
from dialogs import ParameterDialog, ChoiceDialog
import colormap

from VizFrame import VizFrame
from OboFrame import OboTreeFrame

class TwoDDensity(VizFrame):
    type='2D Density'
    def __init__(self, parent=None, id=-1,
                 pos=wx.DefaultPosition,
                 title="2D Density", show=True):
        VizFrame.__init__(self, parent, id, pos, title)
        self.widget = TwoDPanel(None, 1, 1, self)
        self.widget.draw()

        # layout the frame
        self.box = wx.BoxSizer(wx.HORIZONTAL)
        self.leftPanel = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.box)
        self.box.Add(self.leftPanel, 0, wx.EXPAND)
        self.box.Add(self.widget, 1, wx.EXPAND)
        self.Layout()
        
        self.MenuBar = wx.MenuBar()
        self.FileMenu = wx.Menu()
        self.EditMenu = wx.Menu()
        self.VisualMenu = wx.Menu()
        self.GateMenu = wx.Menu()
        self.MenuBar.Append(self.FileMenu, "File")
        self.MenuBar.Append(self.EditMenu, "Edit")
        self.MenuBar.Append(self.VisualMenu, "Visuals")
        self.MenuBar.Append(self.GateMenu, "Gating")
        self.SetMenuBar(self.MenuBar)
        self.widget.scatter = self.VisualMenu.AppendCheckItem(-1,"Scatter Plot")
        self.widget.scatter.Check(True)
        self.widget.contour = self.VisualMenu.AppendCheckItem(-1,"Contour Plot")
        self.widget.ellipse = self.VisualMenu.AppendCheckItem(-1,"Confidence Ellipse")
        edit_fig = self.EditMenu.Append(-1, "Change figure attributes")
        edit_labels = self.EditMenu.Append(-1, "Change cell subset labels")
        self.Bind(wx.EVT_MENU, self.OnChangeFigAttr, edit_fig)
        self.Bind(wx.EVT_MENU, self.OnZLabel, edit_labels)

        self.colorGate = self.GateMenu.Append(-1, "Gate on visible colors only")
        polyGate = self.GateMenu.Append(-1, "Add 4-polygon gate")
        gate = self.GateMenu.Append(-1, "Capture gated events")
        ellipses = self.GateMenu.Append(-1, "Specify ellipse confidence")

        self.GateMenu.AppendSeparator()
        copyGate = self.GateMenu.Append(-1, "Copy 4-polygon gate")
        pasteGate = self.GateMenu.Append(-1, "Paste 4-polygon gate")

        self.Bind(wx.EVT_MENU, self.GateByColor, self.colorGate)
        self.colorGate.Enable(False)
        self.Bind(wx.EVT_MENU, self.OnEllipses, ellipses)
        self.Bind(wx.EVT_MENU, self.OnAddPolyGate, polyGate)
        self.Bind(wx.EVT_MENU, self.Gate, gate)
        self.Bind(wx.EVT_MENU, self.OnCopyGate, copyGate)
        self.Bind(wx.EVT_MENU, self.OnPasteGate, pasteGate)

        # try to save figures
        export = self.FileMenu.Append(-1, "Export graphics")
        self.Bind(wx.EVT_MENU, self.OnExport, export)

        self.Bind(wx.EVT_MENU, self.OnMenuSwitch, self.widget.scatter)
        self.Bind(wx.EVT_MENU, self.OnMenuSwitch, self.widget.contour)
        self.Bind(wx.EVT_MENU, self.OnMenuSwitch, self.widget.ellipse)
        if show:
            self.Show()
            self.SendSizeEvent()
        self.model = None
        
    def AttachModel(self, model):
        if self.model == None:
            self.model = model
            self.data = self.model.GetCurrentData()
            if self.model.IsZ():
                self.colors = array(self.model.GetCurrentZ()[:],'i')
                self.colorGate.Enable(True)
            else:
                self.colors = None
            try:
                fields = self.model.current_array.getAttr('fields')
            except AttributeError:
                # fields = map(str,range(1, self.model.current_array.shape[1]+1))
                print "debug this!"
            self.widget.model = self.model
            self.widget.Zs = self.colors
            self.RadioButtons(fields)
            self.BuildColors()
        
    def OnCopyGate(self, event):
        """Store current gate vertex locations."""
        try:
            self.model.gate = self.widget.p.poly
        except AttributeError:
            print "Cannot find poly"

    def OnPasteGate(self, event):
        """Paste stored gate."""
        try:
            self.OnAddPolyGate(event, self.model.gate)
        except AttributeError:
            print "Cannot find copied gate"

    def OnChangeFigAttr(self, event):
        inputs = {}
        ax = self.widget.subplot.axis()
        xlab = self.widget.xlab
        ylab = self.widget.ylab
        title = self.widget.title
        ms = self.widget.ms
        choices = [('xmin', 'FloatValidator', str(ax[0])),
                   ('xmax', 'FloatValidator', str(ax[1])),
                   ('ymin', 'FloatValidator', str(ax[2])),
                   ('ymax', 'FloatValidator', str(ax[3])),
                   ('xlab', 'BasicValidator', xlab),
                   ('ylab', 'BasicValidator', ylab),
                   ('title', 'BasicValidator', title),
                   ('ms', 'FloatValidator', str(ms))]
        dlg = ParameterDialog(choices, inputs, 'Change figure attributes')
        if dlg.ShowModal() == wx.ID_OK:
            self.widget.update_attributes(inputs)
        dlg.Destroy()
        self.widget.draw()
                   

    def OnExport(self, event):
        print "Test export graphics"
        self.widget.export()

    def BuildColors(self):
        self.colorPanel = self.BuildColorPanel()
        if self.colors is None:
            self.colorPanel.Hide()
        self.Refresh()
        
    def BuildColorPanel(self):
        """Select components by color and reassign labels if desired."""
        panel = wx.ScrolledWindow(self, -1, style=wx.VSCROLL)
        color_names = self.model.GetZLabels(self.model.GetCurrentZ())
        self.cbs = [wx.CheckBox(panel, -1, name) for name in color_names]

        if self.model.IsZ():
            z = array(self.model.GetCurrentZ()[:], 'i')
            maxz = max(z)
            colors = [colormap.floatRgb(i, 0, maxz+1, i/(maxz+1)) for i in range(maxz+1)]

            self.popup = wx.Menu()
            zlabel = self.popup.Append(-1, "Edit label")
            self.popup.Bind(wx.EVT_MENU, self.OnZLabel, zlabel)

            for i, cb in enumerate(self.cbs):
                r, g, b, alpha = colors[i]
                r = int(r*255)
                g = int(g*255)
                b = int(b*255)
                cb.SetValue(True)
                cb.SetBackgroundColour(wx.Colour(r,g,b))
                self.Bind(wx.EVT_CHECKBOX, self.DisableColors, cb)
                cb.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)

            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.AddMany(self.cbs)
            panel.SetSizer(sizer)
            self.leftPanel.Insert(1,panel,1, wx.ALL | wx.EXPAND) 
            panel.SetScrollRate(5,5)

        return panel

    def DisableColors(self, event):
        indices = [i for i, c in enumerate(self.cbs) if c.IsChecked()]
        self.widget.components = indices
        self.widget.draw()

    def OnZLabel(self, event):
        obo = OboTreeFrame(self.model, self)
        obo.Bind(wx.EVT_WINDOW_DESTROY, self.OnOboClose)
        obo.Show()

    def OnOboClose(self, event):
        color_names = self.model.GetZLabels(self.model.GetCurrentZ())
        
        for i, cb in enumerate(self.cbs):
            cb.SetLabel(color_names[i])
            
    def OnShowPopup(self, event):
        self.PopupMenu(self.popup)
        
    def OnEllipses(self, event):
        """Specify confidence level for ellipse of each component."""
        n = len(self.model.current_group.mu_end[:])
        inputs = {}
        choices = [('Component %d' % i, 'FloatValidator', str(0.95)) for i in range(1, n+1)]
        dlg = ParameterDialog(choices, inputs, 'Specify confidence level for ellipse of each component')
        if dlg.ShowModal() == wx.ID_OK:
            self.widget.levels = [inputs['Component %d' % i] for i in range(1, n+1)]
        dlg.Destroy()
        self.widget.draw()

    def OnAddPolyGate(self, event, poly=None):
        if poly is None:
            minx = min(self.widget.x)
            maxx = max(self.widget.x)
            miny = min(self.widget.y)
            maxy = max(self.widget.y)
            lenx = maxx - minx
            leny = maxy - miny
            loc = minx + lenx/4.0, miny + leny/4.0
            poly = mpl_gate.acRectangle(loc, lenx/2.0, leny/2.0, animated=True)
        poly.set_visible(False)

        self.widget.subplot.add_patch(poly)
        self.widget.p = mpl_gate.PolygonInteractor(self.widget, self.widget.subplot, poly)
        self.widget.subplot.add_line(self.widget.p.line)
        self.widget.draw()

    def RadioButtons(self, list):
        panel = wx.Panel(self, -1)
        try:
            self.radioX.Destroy()
            self.radioY.Destroy()
        except AttributeError:
            pass
        self.radioX = wx.RadioBox(panel, -1, "X Variable", (10,10), wx.DefaultSize, list, 1, wx.RA_SPECIFY_COLS)
        self.radioX.Bind(wx.EVT_RADIOBOX, self.OnControlSwitch)
        self.radioY = wx.RadioBox(panel, -1, "Y Variable", (self.radioX.GetPosition()[0]+self.radioX.GetSize()[0],10), wx.DefaultSize, list, 1, wx.RA_SPECIFY_COLS)
        self.radioY.Bind(wx.EVT_RADIOBOX, self.OnControlSwitch)
        
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.radioX, 0)
        box.Add(self.radioY, 0)
        panel.SetSizer(box)
        self.leftPanel.Insert(0, panel, 0)


    def UpdateSimple(self, x, y, xlab, ylab, title=''):
        self.widget.coord1 = x
        self.widget.coord2 = y
        self.widget.xlab = xlab
        self.widget.ylab = ylab
        self.widget.title = title
        self.widget.x = self.data[:,x]
        self.widget.y = self.data[:,y]

        if min(self.widget.x) <= 0:
            self.widget.minx = min(self.widget.x)
        else:
            self.widget.minx = 0
        if min(self.widget.y) <= 0:
            self.widget.miny = min(self.widget.y)
        else:
            self.widget.miny = 0
        self.widget.area = [self.widget.minx, max(self.widget.x), self.widget.miny, max(self.widget.y)]
        self.widget.name = str(x) + " vs " + str(y)
        self.widget.draw()
        
    def Plot(self):
        self.UpdateSimple(self.radioX.GetSelection(),self.radioY.GetSelection(), self.radioX.GetStringSelection(), self.radioY.GetStringSelection())
            

    def OnControlSwitch(self,event):
        self.UpdateSimple(self.radioX.GetSelection(),self.radioY.GetSelection(),self.radioX.GetStringSelection(), self.radioY.GetStringSelection())
    
    def OnMenuSwitch(self,event):
        self.widget.draw()
    
    def GateByColor(self, event):
        fields = self.data.getAttr('fields')
        results = []
        z = []
        # self.checked = [i for i, cb in enumerate(self.cbs) if cb.IsChecked()]
        for i in xrange(0, self.data.shape[0]):
            if self.cbs[self.colors[i]].IsChecked():     
                results.append(self.data[i,:])
                z.append(self.colors[i])
        mu_end = self.model.GetCurrentGroup().mu_end[:]
        sigma_end = self.model.GetCurrentGroup().sigma_end[:]

        filtered = array(results)
        newgroup = self.model.NewGroup('GatedByColor')
        self.model.NewArray('data',filtered, parent=newgroup)
        self.model.current_array.setAttr('fields', fields)
        self.model.hdf5.createArray(self.model.current_group, 'z', array(z))
        self.model.hdf5.createArray(self.model.current_group, 'mu_end', 
                                    mu_end)
        self.model.hdf5.createArray(self.model.current_group, 'sigma_end', 
                                    sigma_end)
        self.model.update()

    def Gate(self, event):
        """Capture events inside drawn gates."""
        results = []
        for i, d in enumerate(self.data):
            if self.widget.p.PointInPoly((self.widget.x[i], self.widget.y[i])):
                results.append(d)
        self.model.updateHDF('GatedData', array(results), self.data)
        self.model.GetCurrentData().attrs.batch=['gate', (self.radioX.GetStringSelection(),self.radioY.GetStringSelection()), self.widget.p.poly.verts]

class TwoDPanel(PlotPanel):
    def __init__(self, x, y, parent, *args):
        super(TwoDPanel, self).__init__(*args)
        self.x = x
        self.y = y
        self.parent = parent
        self.colors = None
        self.Zs = None

    def update_attributes(self, inputs):
        if not hasattr(self, 'subplot'):
            return
        self.area =[inputs['xmin'], inputs['xmax'], inputs['ymin'], inputs['ymax']]
        self.xlab = inputs['xlab']
        self.ylab = inputs['ylab']
        self.title = inputs['title']
        self.ms = inputs['ms']

    def draw(self):
      alpha = 1
      if not hasattr(self, 'ms'):
          try:
              self.ms = min(1, 1000.0/len(self.x))
          except (ZeroDivisionError, TypeError):
              self.ms = 1.0
      if not hasattr(self, 'subplot'):
          self.subplot = self.figure.add_subplot(111)
      self.subplot.clear()
      if self.x is not None:
        # sample at most 10000 points for display
        if len(self.x) > 10000:
          stride = len(self.x)/10000
        else:
            stride = 1
        
        x = self.x[:10000*stride:stride]
        y = self.y[:10000*stride:stride]

        self.subplot.set_xlabel(self.xlab)
        self.subplot.set_ylabel(self.ylab)
        self.subplot.set_title(self.title)
        if self.scatter.IsChecked() :
            # add stuff to color in and out of gate differently
            try:
                xi = []
                yi = []
                xo = []
                yo = []
                for pt in zip(x, y):
                    if self.p.PointInPoly(pt):
                        xi.append(pt[0])
                        yi.append(pt[1])
                    else:
                        xo.append(pt[0])
                        yo.append(pt[1])
                self.subplot.plot(xi, yi, 'r.', ms=self.ms)
                self.subplot.plot(xo, yo, 'b.', ms=self.ms)
            except AttributeError:
                # PUT COLOR CODE HERE
                # ONLY WORKS IF NOT GATING
                if hasattr(self, 'model') and self.Zs is not None:
                    z = array(self.Zs[:], 'i')
                    maxz = max(z)
                    self.colors = [colormap.floatRgb(i, 0, maxz+1, i/(maxz+1)) for i in range(maxz+1)]
                    for i in range(maxz+1):
                        if hasattr(self, 'components') and i not in self.components:
                            continue
                        xx = self.x[z==i][:10000*stride:stride]
                        yy = self.y[z==i][:10000*stride:stride]
                        self.subplot.plot(xx, yy, '.', c=self.colors[i], alpha=alpha, ms=self.ms)
                else:
                    bins = 100
                    z, xedge, yedge = histogram2d(y, x, bins=[bins, bins], 
                                                        range=[(min(y), max(y)),
                                                               (min(x), max(x))])
                    
                    # interpolate to get rid of blocky effect
                    # from http://en.wikipedia.org/wiki/Bilinear_interpolation
                    xfrac, xint = modf((x - min(x))/
                                             (max(x)-min(x))*(bins-1))
                    yfrac, yint = modf((y - min(y))/
                                             (max(y)-min(y))*(bins-1))
                    
                    zvals = zeros(len(xint), 'd')
                    for i, (_x, _y, _xf, _yf) in enumerate(zip(xint, yint, xfrac, yfrac)):
                        q11 = z[_y, _x]
                        if _xf:
                            q12 = z[_y, _x+1]
                        else:
                            q12 = 0
                        if _yf:
                            q21 = z[_y+1, _x]
                        else:
                            q21 = 0
                        if _xf and _yf:
                            q22 = z[_y+1, _x+1]
                        else:
                            q22 = 0
                    
                        zvals[i] = q11*(1-_xf)*(1-_yf) + q21*(1-_xf)*(_yf) + \
                            q12*(_xf)*(1-_yf) + q22*(_xf)*(_yf)

                    s = self.subplot.scatter(x, y, alpha=alpha, s=1, c=zvals, faceted=False )
            alpha = alpha - .25
        if self.contour.IsChecked() :
            bins = int(0.25*sqrt(len(self.x)))
            z, xedge, yedge = histogram2d(self.y, self.x, bins=[bins, bins], range=[(self.miny, max(self.y)),(self.minx, max(self.x))])
            c = self.subplot.contour(z, 25, cmap=cm.jet, alpha=alpha, extent=self.area)
            alpha = alpha - .25
        if self.ellipse.IsChecked() and (self.coord1 != self.coord2):
            try:
                mu = self.model.current_group.mu_end[:]
                try:
                    spread = self.model.current_group.omega_end[:]
                    spread_form = 'omega'
                except AttributeError:
                    spread = self.model.current_group.sigma_end[:]
                    spread_form = 'sigma'
                try:
                    self.levels
                except AttributeError:
                    self.levels = [0.67]*len(mu)
                lvl = 0
                for i, item in enumerate(zip(mu, spread)):
                    # only display selected components
                    lvl += 1

                    if hasattr(self, 'components') and i not in self.components:
                        continue
                    m, sp = item

                    if spread_form == 'omega':
                        sp = inv(sp)

                    Xe, Ye = dens.gauss_ell(m, sp, dim=[self.coord1, self.coord2], npoints=100, level=self.levels[i])
                    xk = Xe[int(0.1*len(Xe))]
                    yk = Ye[int(0.1*len(Ye))]

                    self.subplot.plot(Xe, Ye, 'r-', linewidth=2)
                    self.subplot.text(xk, yk, str(lvl), fontsize=14, weight='bold', bbox=dict(facecolor='yellow', alpha=0.5))

            except AttributeError, e:
                dlg = wx.MessageDialog(None, str(e), "EllipseDialog", wx.OK | wx.ICON_ERROR)
                result = dlg.ShowModal()
                dlg.Destroy()
                self.ellipse.Check(False)
        self.subplot.axis(self.area)

      self.Refresh()
    
