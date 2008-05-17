import wx
import wx.grid
from plots import PlotPanel
import pylab
import numpy
from numpy.linalg import solve



class CompensationFrame(wx.Frame):
    def __init__(self, data, matrix=None):
        self.data = data
        self.matrix = matrix
        wx.Frame.__init__(self, None, -1, "Compensating", style = wx.DEFAULT_FRAME_STYLE | wx.RESIZE_BORDER )
        self.panel = wx.Panel(self, -1, size = self.GetSize() )
        
        #Object in the panel/frame
        instruct = wx.StaticText(self.panel, -1, "Instructions")
        self.graphs = GraphingPanel(self.panel, -1, self.data[:,0],self.data[:,0])
        self.grid = wx.grid.Grid(self.panel)
        
        try:
            self.headers = self.data.getAttr('fields')
        except AttributeError:
            self.headers = None
            
        #print self.headers
        self.gridSize = len(self.headers)
        self.grid.CreateGrid(self.gridSize,self.gridSize)
        #self.grid.CreateGrid(4,4)
        rgbtuple = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE).Get()
        self.gridDefaultColor = self.grid.GetCellBackgroundColour(0,0)
        self.grid.SetDefaultEditor(wx.grid.GridCellFloatEditor())
        self.pos = None
        for i in range(self.gridSize):
            self.grid.SetRowLabelValue(i,self.headers[i])
            self.grid.SetColLabelValue(i,self.headers[i])
            for j in range(self.gridSize):
                if i == j :
                    self.grid.SetCellBackgroundColour(i,j, wx.Colour(*rgbtuple))
                    self.grid.SetReadOnly(i,j, isReadOnly=True)
                self.grid.SetCellValue(i,j, '1')
                
        self.grid.AutoSize()
        self.grid.Bind(wx.EVT_SIZE, self.OnGridSize)
        self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.OnCellSelect, self.grid)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnEdit)
        
        self.okBtn = wx.Button(self.panel, id=wx.ID_OK)
        self.cancelBtn = wx.Button(self.panel, id=wx.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.OnOkay, self.okBtn)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancelBtn)
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        middleSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        mainSizer.Add(instruct,0,wx.EXPAND)
        
        middleSizer.Add(self.graphs,1,wx.EXPAND)
        middleSizer.Add(self.grid,0)
        
        mainSizer.Add(middleSizer,1, wx.EXPAND)
        
        btnSizer.Add((10,10),1)
        btnSizer.Add(self.cancelBtn)
        btnSizer.Add((10,10))
        btnSizer.Add(self.okBtn)
        btnSizer.Add((10,10))
        mainSizer.Add(btnSizer, 0, wx.EXPAND)
        
        self.panel.SetSizer(mainSizer)
        mainSizer.Fit(self)
        self.Layout()
        
        
    def OnGridSize(self, event):
        #self.grid.AutoSize()
        size = self.grid.GetBestSize()
        self.grid.SetSize(size)
        
    def OnOkay(self, event):
        """
        do aproprate action on okay button press
        """
        # need to do stuff here
                          
        self.Destroy()
        
    def OnCancel(self, event):
        """
        cancel button handler
        """
        self.Destroy()
        
    def OnCellSelect(self, event):
        """
        handle selecting cells so the oposite cell is highlighted
        """
        if self.pos is not None:
            if self.pos[0] != self.pos[1]:
                self.grid.SetCellBackgroundColour(self.pos[1], self.pos[0], self.gridDefaultColor )

        if event.Selecting():
            
            self.pos = [event.GetRow(), event.GetCol()]
            if self.pos[0] != self.pos[1]:
                self.grid.SetCellBackgroundColour(self.pos[1], self.pos[0], wx.Colour(*(255,128,128)))
            self.grid.Refresh()
            self.graphs.x = self.data[:,self.pos[0]]
            self.graphs.y = self.data[:,self.pos[1]]
            self.graphs.draw()

            
        event.Skip()
        
    def OnEdit(self, event):
        self.Compensate()
        event.Skip()
    
    def Compensate(self):
        comp = numpy.zeros((self.gridSize, self.gridSize))
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                comp[i,j] = float(self.grid.GetCellValue(i,j))
#        indices = [data.attrs.fields.index(data.attrs.NtoS[m])
#                       for m in self.headers]
#        observed = array([data[:,i] for i in indices])
        self.data = solve(comp.T, self.data[:])  ## todo fix matix sizes.
        

class GraphingPanel(PlotPanel):
    def __init__(self,parent, id, x,y,*args):
         super(GraphingPanel, self).__init__(parent=parent, id=id)
         self.x = x
         self.y = y
         
    def draw(self):
         if not hasattr(self, 'subplot'):
             self.subplot = self.figure.add_subplot(111)
         self.subplot.clear()
         bins = 250
         
         z, xedge, yedge = numpy.histogram2d(self.y, self.x, bins=[bins, bins], 
                                    range=[(numpy.min(self.y), numpy.max(self.y)),
                                           (numpy.min(self.x), numpy.max(self.x))])
         xint = map(int, (self.x - numpy.min(self.x))/(numpy.max(self.x)-numpy.min(self.x))*(bins-1))
         yint = map(int, (self.y - numpy.min(self.y))/(numpy.max(self.y)-numpy.min(self.y))*(bins-1))

         zvals = numpy.array([z[_y, _x] for _x, _y in zip(xint, yint)])
         
         
         self.subplot.scatter(self.x,self.y,s=1, c=zvals, faceted=False )
         self.Refresh()
         
      
if __name__ == '__main__':
    app = wx.PySimpleApp()
    import tables
    foo = tables.openFile('../data/3FITC_4PE_004.h5')
    data = foo.getNode('/3FITC_4PE_004/data')

    bar = CompensationFrame(data)
    bar.Show()
    app.MainLoop()