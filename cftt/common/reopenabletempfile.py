# -*- coding: utf-8 -*-

import util
import base
import tempfile
import os


class ReopenableTempFile(base.BaseAttribute):
    _known_options = set(('mode', 'bufsize', 'suffix', 'prefix', 'dir'))

    def __init__(self, **kwargs):
        super(ReopenableTempFile, self).__init__()
        self._file = None
        self.attr(kwargs)

    def __enter__(self):
        self._file = tempfile.NamedTemporaryFile(delete=False,
                                                 **self._attributes)
        return self._file

    def __exit__(self, exc_type, exc_value, traceback):
        self._file.close()
        os.remove(self._file.name)

    @property
    def file(self):
        if self._file is None:
            return None
        return self._file.file

    def close(self):
        if self._file is not None:
            return self._file.close()

    def flush(self):
        if self._file is not None:
            return self._file.flush()

    def fileno(self):
        if self._file is not None:
            return self._file.fileno()

    def next(self):
        if self._file is not None:
            return self._file.next()

    def read(self, *args, **kwargs):
        if self._file is not None:
            return self._file.read(*args, **kwargs)

    def readline(self, *args, **kwargs):
        if self._file is not None:
            return self._file.readline(*args, **kwargs)

    def readlines(self, *args, **kwargs):
        if self._file is not None:
            return self._file.readlines(*args, **kwargs)

    def seek(self, *args, **kwargs):
        if self._file is not None:
            return self._file.seek(*args, **kwargs)

    def tell(self):
        if self._file is not None:
            return self._file.tell()

    def truncate(self, *args, **kwargs):
        if self._file is not None:
            return self._file.truncate(*args, **kwargs)

    def write(self, *args, **kwargs):
        if self._file is not None:
            return self._file.write(*args, **kwargs)

    def writelines(self, *args, **kwargs):
        if self._file is not None:
            return self._file.writelines(*args, **kwargs)

    @property
    def closed(self):
        if self._file is not None:
            return self._file.closed

    @property
    def encoding(self):
        if self._file is not None:
            return self._file.encoding

    @property
    def mode(self):
        if self._file is not None:
            return self._file.mode

    @property
    def name(self):
        if self._file is not None:
            return self._file.name
