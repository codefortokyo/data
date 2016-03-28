# -*- coding: utf-8 -*-

import sys
import time
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
    def __init__(self, portMin=8000, portMax=8100):
        self._ports = (portMin, portMax)
        self._port = None
        self._worker = None
        self._working = False

    def open(self):
        for port in range(*self._ports):
            try:
                self._worker = Worker(port)
                self._worker.start()
                self._port = port
                self._working = True
                return
            except Exception as e:
                time.sleep(0.2)

    def close(self):
        if self._working:
            self._worker.stop()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    @property
    def port(self):
        return self._port
