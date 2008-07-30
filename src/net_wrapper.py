import xmlrpclib
import pickle
'''
network layer wrapper for xmlrpc code
'''


class Session_manager(object):
    def __init__(self, url):
        self.session = xmlrpclib.Server(url)
        print self.session
        #self.user = user
        #self.pw = pw
        self.data_file = None
        
    def send_data(self, array):
        self.data = pickle.dumps(array)
        self.data_file = self.session.send_data(self.data)
        
    def send_job(self, job_def):
        if self.data_file  is None:
            raise ENoData
        else:
            job_id = self.session.send_job(job_def, self.data_file)
            return job_id
        
    def get_status(self, job_id):
        return self.session.get_status(job_id)
        
    def get_result(self, job_id):
        return self.session.get_result(job_id)
    
    def get_server_status(self):
        return self.session.server_status()

def connect(url, username, pw):
    '''
    eventually will setup a newwork connection and return the session_manager object
    '''
    
    return Session_manager(url)

if __name__ == '__main__':
    import numpy
    session = connect('http://localhost:8000', 'foo', 'bar')
    print session.get_server_status()
    foo = numpy.zeros((4,4))
    session.send_data(foo)
    print session.data_file
    print session.get_status(1)
