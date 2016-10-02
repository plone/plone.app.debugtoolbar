# -*- coding: utf-8 -*-
from zope.viewlet.viewlet import ViewletBase

class RequestViewlet(ViewletBase):

    def update(self):
        self.headers = []
        self.environ = []

        for k in sorted(self.request.environ):
            if k.upper().startswith('HTTP_'):
                header = '-'.join([x.capitalize() for x in k[5:].split('_')])
                self.headers.append((header, self.request.environ[k],))
            else:
                self.environ.append((k, self.request.environ[k],))
