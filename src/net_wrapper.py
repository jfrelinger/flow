import xmlrpclib
'''
network layer wrapper for xmlrpc code
'''


class Session_manager(object):
    def __init__(self, url):
        self.server = xmlrpclib.Server(url)
        
    def send_data(self, array):
        self.server.send_data(array)
        
    def send_job(self, job_def):
        self.server.send_job(job_def)
        
    def get_status(self, job_id):
        return self.server.get_status(job_id)
        
    def get_result(self, job_id):
        return self.server.get_result(job_id)

def connect(url, username, pw):
    '''
    eventually will setup a newwork connection and return the session_manager object
    '''
    
    return Session_manager(url)
