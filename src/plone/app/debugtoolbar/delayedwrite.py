# -*- coding: utf-8 -*-
import json

from zope.interface import Interface
from zope.interface import implementer
from zope.component import adapts
from zope.annotation.interfaces import IAnnotations

from plone.transformchain.interfaces import ITransform

from plone.app.debugtoolbar.browser.interfaces import IDebugToolbarLayer

def delay(request, name, fn):
    """Register a function that will be called at the end of the request.
    """

    ann = IAnnotations(request, None)
    if ann is None:
        return
    ann.setdefault('plone.app.debugtoolbar.delayed', {})[name] = fn

@implementer(ITransform)
class DelayedWriteTransformer(object):
    adapts(Interface, IDebugToolbarLayer)

    order = 9999

    def __init__(self, published, request):
        self.published = published
        self.request = request
    
    def transformUnicode(self, result, encoding):
        self.saveCookie()
        return None
    
    def transformBytes(self, result, encoding):
        self.saveCookie()
        return None

    def transformIterable(self, result, encoding):
        self.saveCookie()
        return None
    
    def saveCookie(self):
        data = self.getData()
        if data is not None:
            self.request.response.setCookie('plone.app.debugtoolbar', data, quoted=False, path='/')
        
    def getData(self):
        data = {}
        ann = IAnnotations(self.request, None)
        if ann is None:
            return data
        
        delayed = ann.get('plone.app.debugtoolbar.delayed', {})
        if not delayed:
            return None
        
        for key, fn in delayed.items():
            data[key] = fn(self.request)
        
        return json.dumps(data)
