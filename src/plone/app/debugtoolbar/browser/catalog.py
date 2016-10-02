# -*- coding: utf-8 -*-
from zope.viewlet.viewlet import ViewletBase

from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName

class CatalogViewlet(ViewletBase):

    def update(self):

        self.indices = []
        self.metadata = []

        ct = getToolByName(self.context, 'portal_catalog')

        # get the catalog record (brain) of the object
        path = '/'.join(self.context.getPhysicalPath())
        result = ct.searchResults(path={'query': path, 'depth': 0})

        if result and len(result) > 0:
            brain = result[0]
            for key, value in ct.getIndexDataForRID(brain.getRID()).items():
                self.indices.append({'name': key, 'value': value})
            self.indices.sort(key=lambda k: k['name'])
            for key, value in ct.getMetadataForRID(brain.getRID()).items():
                self.metadata.append({'name': key, 'value': value})
            self.metadata.sort(key=lambda k: k['name'])
        else:
            brain = None

        self.catalogStatus = brain
