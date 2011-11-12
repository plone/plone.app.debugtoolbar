from zope.viewlet.viewlet import ViewletBase

class ContextViewlet(ViewletBase):

    def update(self):
        
        self.path = '/'.join(self.context.getPhysicalPath())
        self.cls = self.context.__class__
