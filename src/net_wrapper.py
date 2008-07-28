import xmlrpclib
'''
network layer wrapper for xmlrpc code
'''


class Session_manager(object):
    def __init__(self, url):
        self.session = xmlrpclib.Server(url)
        print self.session
        #self.user = user
        #self.pw = pw

    def send_data(self, array):
        self.data = array
        #self.session.send_data(array)
        
    def send_job(self, job_def):
        self.session.send_job(job_def)
        
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
    session = connect('http://localhost:8000', 'foo', 'bar')
    print session.get_server_status()
