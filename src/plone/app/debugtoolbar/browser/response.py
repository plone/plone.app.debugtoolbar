# -*- coding: utf-8 -*-
from zope.viewlet.viewlet import ViewletBase
from plone.app.debugtoolbar.delayedwrite import delay

def captureHeaders(request):
    headers = []

    for k in sorted(request.response.headers):
        header = '-'.join([x.capitalize() for x in k.split('-')])
        headers.append((header, request.response.headers[k],))
    
    return headers

def captureStatus(request):
    return request.response.status

class ResponseViewlet(ViewletBase):

    def update(self):
        delay(self.request, 'response_headers', captureHeaders)
        delay(self.request, 'response_status', captureStatus)
