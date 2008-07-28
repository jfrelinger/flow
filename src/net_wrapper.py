'''
network layer wrapper for xmlrpc code
'''

class Session_manager(object):
    def __init__(self):
        pass
    def send_data(self, array):
        pass
    def send_job(self, job_def):
        pass
    def get_status(self, job_id):
        pass
    def get_result(self, job_id):
        pass

def connect():
    '''
    eventually will setup a newwork connection and return the session_manager object
    '''
    return Session_manager()
