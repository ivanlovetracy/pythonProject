# -*- coding: utf-8 -*-

#MJPEG Server for the webcam
import string,cgi,time
from os import curdir, sep
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

import cv2 as cv
import re
import sys
import imutils
import socket

capture = cv.VideoCapture(0)
ret, img1 = capture.read()

# if img1 == False :
#     print("No WebCam Found!")
#     sys.exit()

if len(sys.argv) < 2 :
    print("Usage : webcamserver ")
    cameraQuality = 100
    port = 81
else:
    cameraQuality = sys.argv[1]
    port = int(sys.argv[2])

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # global cameraQuality
        print(self.path)
        try:
            # self.path=re.sub('[^.a-zA-Z0-9]', "",str(self.path))
            #
            # if self.path=="" or self.path==None or self.path[:1]==".":
            #     return
            # if self.path.endswith(".html"):
            #     f = open(curdir + sep + self.path)
            #     self.send_response(200)
            #     self.send_header('Content-type', 'text/html')
            #     self.end_headers()
            #     self.wfile.write(f.read())
            #     f.close()
            #     return

            if self.path.endswith("stream"):
                self.send_response(200)
                self.send_header("Content-Type:","multipart/x-mixed-replace; boundary=frame")
                self.end_headers()
                # print(self.responses)
                # self.wfile.write(b"Content-Type: multipart/x-mixed-replace; boundary=--aaboundary")
                self.wfile.write(b"\r\n\r\n")
                while 1:
                    ret, img1 = capture.read()
                    if(ret == 1):
                        # print("img len=", len(img1))
                        # print("img len=", img1)
                        # img1 = cv.QueryFrame(capture)
                        # cv2mat1 = cv.EncodeImage(".jpeg", img1, (cv.CV_IMWRITE_JPEG_QUALITY, cameraQuality))
                        # JpegData1 = cv2mat1.tostring()
                        JpegData1 = cv.imencode('.jpeg', img1)[1].tobytes()
                        self.wfile.write(b"--frame\r\n")
                        self.wfile.write(b"Content-Type: image/jpeg\r\n\r\n")
                        # self.wfile.write(b"Content-length: "+str(len(JpegData1))
                        # self.wfile.write(b"\r\n\r\n" )
                        self.wfile.write(JpegData1)
                        self.wfile.write(b"\r\n\r\n\r\n")
                        time.sleep(0.1)
                return

            # if self.path.endswith(".jpeg"):
            #     f = open(curdir + sep + self.path)
            #     self.send_response(200)
            #     self.send_header('Content-type','image/jpeg')
            #     self.end_headers()
            #     self.wfile.write(f.read())
            #     f.close()
            #     return

            return

        except IOError:

            self.send_error(404,'File Not Found: %s' % self.path)

    # def do_POST(self):
    #
    #     global rootnode, cameraQuality
    #
    #     try:
    #         ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
    #         if ctype == 'multipart/form-data':
    #             query=cgi.parse_multipart(self.rfile, pdict)
    #         self.send_response(301)
    #         self.end_headers()
    #         upfilecontent = query.get('upfile')
    #         print("filecontent", upfilecontent[0])
    #         value=int(upfilecontent[0])
    #         cameraQuality=max(2, min(99, value))
    #         self.wfile.write("POST OK. Camera Set to");
    #         self.wfile.write(str(cameraQuality));
    #
    #     except :
    #
    #         pass

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):

#class ThreadedHTTPServer(HTTPServer):

    # """Handle requests in a separate thread."""

    # myname = socket.getfqdn(socket.gethostname())
    # myaddr = socket.gethostname()

    def main():
        while 1:
            try:
                server = ThreadedHTTPServer(('0.0.0.0', port), MyHandler)
                print('Starting httpServer...')
                print('See :'+ str(port) + '/stream')
                server.serve_forever()

            except KeyboardInterrupt:
                print('^C received, shutting down server')
                server.socket.close()

if __name__ == '__main__':
    ThreadedHTTPServer.main()
