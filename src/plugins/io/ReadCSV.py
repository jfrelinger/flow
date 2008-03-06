from io import Io
import numpy
import os

class ReadCSV(Io):
    newMethods=('ReadCSV','Load CSV data file')
    type = 'Read'
    supported = "CSV files (*.csv)|*.csv|All files (*.*)|*.*"

    def ReadCSV(self, filename):
        """reads a csv file and populates data structures"""
        # self.model.ready = False

        text = open(filename).readlines()
        headers = text[0].strip('\n').strip('\r').split(',')
        arr = numpy.array([map(float, line.strip().split(',')) for line in text[1:]])        

        # create a new group
        basename = os.path.basename(filename)
        base, ext = os.path.splitext(basename)
        self.model.NewGroup(base)
            
        # create an hdf5 file
        self.model.LoadData(headers, arr, 'Original data')
