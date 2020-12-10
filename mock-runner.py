from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import time
import os
import json
import requests

# PORT_NUMBER =  int(os.getenv("VCAP_APP_PORT")) #8999
PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

    #Handler for the GET requests
    def do_GET(self):
        path = self.path
        content_length = 0
        for i in self.headers:
            if i.lower() == "Content-Length".lower():
                content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        resp = "resource/default.json"
        type = 'text/xml;charset=utf-8'
        sleeptime = 0.020
        if "ExampleService" in path:
            resp = "resource/default.xml"
            type = 'text/xml;charset=utf-8'
            sleeptime = 0.850
        elif "/cinema/ticket" in path:
            resp = "resource/ticket.json"
            type = 'application/json;charset=utf-8'
            sleeptime = 0.350
        elif "/hello" in path and "messagetype=me" in  path:
            if  "abc" in path:
                resp = "resources/rest-mock-response.json"
                sleeptime = 0.250
            elif  "cde" in path:
                resp = "resource/rest-mock-response-1.json"
                sleeptime = 0.250
            else:
                resp = "resources/default.json"
                sleeptime = 0.780
            type = 'application/json;charset=utf-8'
        elif "/cinema/v1/tickets" in path:
            resp = "resource/rest-mock-response.json"
            type = 'application/json;charset=utf-8'
            sleeptime = 0.200
        file1 = open(resp,"r").read()
        time.sleep(sleeptime)
        self.send_response(200)
        self.send_header('Content-type',type)
        self.end_headers()
        self.wfile.write(file1)

    def do_POST(self):
        path = self.path
        content_length = 0
        for i in self.headers:
            if i.lower() == "Content-Length".lower():
                content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        resp = "resource/soap-mock-response.xml"
        type = 'text/xml;charset=utf-8'
        responseheaders = {}
        sleeptime = 0.020
        if ("ExampleService" in path and ( "getProblem" in (self.rfile.read(int(self.headers.getheader('content-length', 0)))) )):                    
            resp = "resources/soap-mock-response.xml"
            type = 'text/xml;charset=utf-8'
            sleeptime = 0.100
        elif "/FortuneService/" in path:
            if "messagetype=IVR" in path:
                resp = "resource/rest-mock-response.json"
                sleeptime = 0.250
            else:
                resp = "resource/default.json"
                sleeptime = 0.780
            type = 'application/json;charset=utf-8'
       

        if resp.__class__==dict:
            file1 = json.dumps(resp)
        else:
            file1 = open(resp,"r").read()
        time.sleep(sleeptime)
        self.send_response(200)
        self.send_header('Content-type',type)
        self.end_headers()
        self.wfile.write(file1)

    def getttsresponse(self,body):
        ttsURL = "https://example.com"+self.path
        header = {'Authorization':self.headers['Authorization'],
                  'Content-Type':self.headers['Content-Type']}
        response = requests.post(ttsURL, headers=header, data=body)
        return response.json()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    server = ThreadedHTTPServer(('', PORT_NUMBER), myHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()