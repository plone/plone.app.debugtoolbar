import json

from zope.interface import Interface
from zope.interface import implements
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

class DelayedWriteTransformer(object):
    implements(ITransform)
    adapts(Interface, IDebugToolbarLayer)

    order = 9999

    varname = "PLONE_APP_DEBUGTOOLBAR_DATA"

    def __init__(self, published, request):
        self.published = published
        self.request = request
    
    def transformUnicode(self, result, encoding):
        return result.replace(u'var %s = {};' % self.varname,
                              u'var %s = %s;' % (self.varname, self.getData()))
    
    def transformBytes(self, result, encoding):
        return result.replace('var %s = {};' % self.varname,
                              'var %s = %s;' % (self.varname, self.getData()))

    def transformIterable(self, result, encoding):
        res = []
        for r in result:
            res.append(self.transformBytes(r, encoding))
        return res
        
    def getData(self):
        data = {}
        ann = IAnnotations(self.request, None)
        if ann is None:
            return data
        
        delayed = ann.get('plone.app.debugtoolbar.delayed', {})
        for key, fn in delayed.items():
            data[key] = fn(self.request)
        
        return json.dumps(data)
