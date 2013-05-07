#TO RUN: joey2 project_create_tests.py
# OR TO RUN SPECIFIC METHODS: 
# joey2 -m unittest project_tests.TestProjectCreate.test_create_project_via_package_xml_file
# joey2 -m unittest project_tests.TestProjectCreate.test_create_project_via_package_dict

import sys
import os
import unittest
import shutil
import io
import rfc822
sys.path.append('../')
import lib.server.config as server_map
import BaseHTTPServer

class TestLocalServer(unittest.TestCase):

    def __init__(self, *args, **kwargs): 
        super(TestLocalServer, self).__init__(*args, **kwargs) 
        self.base_url = 'http://localhost:9000/'

    def setUp(self):
        pass

    def test_new_project(self):
        request_body = '''
            {
                "pn" : "MavensMateAppServerUnitTest",
                "un" : "mm@force.com",
                "pw" : "force",
                "org_type" : "developer",
                "package" : {
                    "ApexClass" : "*",
                    "ApexPage"  : "*",
                    "ApexComponent" : "*",
                    "ApexTrigger" : "*",
                    "CustomObject" : ["Account","Lead","Opportunity"]   
                }   
            }
        '''
        h = MockRequestHandler(command='POST',path=self.base_url+'project',request_body=request_body)
        response = server_map.project_request(h)
        print 'response: ', response
        #self.do_project_assumptions()
        #shutil.rmtree(config.connection.workspace+"/MavensMateUnitTestProject")

    def test_get_active_session(self):
        request_body = 'username=mm@force.com&password=force&org_type=developer'
        h = MockRequestHandler(command='GET',path=self.base_url+'session?username=mm@force.com&password=force&org_type=developer',request_body=request_body)
        response = server_map.get_active_session_request(h)
        print 'response: ', response

    def tearDown(self):
        pass

    def do_project_assumptions(self):
        project_directory = config.connection.workspace+"/"+self.project_name
        self.assertTrue(os.path.isdir(project_directory))
        self.assertTrue(os.path.isdir(project_directory+"/config"))
        self.assertTrue(os.path.isdir(project_directory+"/src"))

class MockRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, **kwargs):
        self.server             = None
        self.path               = kwargs.get('path', None)
        self.command            = kwargs.get('command', 'POST')
        self.requestline        = None
        self.client_address     = None
        self.request_version    = None
        self.request_body       = kwargs.get('request_body', '')
        self.wfile              = MockIO()
        self.rfile              = MockIO(self.request_body)
        self.headers            = MockHeader(self.command)

    def send_response(self, foo):
        pass

    def send_header(self, foo, bar):
        pass

class MockIO(io.IOBase):
    def __init__(self, body=''):
        self.body = body

    def write(self, foo):
        pass

    def read(self, foo):
        return self.body

    def readline(self):
        return self.body

    def readlines(self):
        return self.body

class MockHeader(rfc822.Message):
    def __init__(self, request_type):
        self.request_type = request_type
        self.dict = {
            'content-type'      : 'text/json',
            'content-length'    : '10'
        }

    def getheader(self, header):
        print '>>>>>> getting head ughhhh'
        if header == 'content-type':
            if self.request_type == 'POST':
                return 'text/json'
            elif self.request_type == 'GET':
                #return 'multipart/form-data'
                return 'application/x-www-form-urlencoded'
        elif header == 'content-length':
            return 10

if __name__ == '__main__':
    unittest.main()