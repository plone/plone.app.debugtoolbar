# -*- coding: utf-8 -*-
from zope.publisher.interfaces import IView
from zope.viewlet.viewlet import ViewletBase
from zope.pagetemplate.interfaces import IPageTemplateSubclassing

class PublishedViewlet(ViewletBase):

    def update(self):
        self.published = self.request.get('PUBLISHED', None)
        
        self.name = getattr(self.published, '__name__', None)
        if self.name is None:
            self.name = getattr(self.published, 'id', None)
        
        self.cls = self.published.__class__

        self.filename = None

        if IPageTemplateSubclassing.providedBy(self.published):
            self.filename = self.published.pt_source_file()
        
        if IView.providedBy(self.published):
            # Look for a page template
            for attr in ('index', 'template', '__call__'):
                pt = getattr(self.published, attr, None)
                if hasattr(pt, 'filename'):
                    self.filename = pt.filename
                    break
