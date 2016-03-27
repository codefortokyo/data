# -*- coding: utf-8 -*-

import sys
import SimpleHTTPServer
import SocketServer
import threading


class Worker(threading.Thread):
    def __init__(self, port=8000):
        super(Worker, self).__init__()
        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        self.httpd = SocketServer.TCPServer(("", port), Handler)

    def run(self):
        self.httpd.serve_forever()

    def stop(self):
        self.httpd.shutdown()


class AsyncFileServer(object):
    def __init__(self, port=8000):
        self._worker = Worker(port)

    def open(self):
        self._worker.start()

    def close(self):
        self._worker.stop()

    def __enter__(self):
        self.open()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
