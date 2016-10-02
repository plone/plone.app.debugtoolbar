# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from zope.component import getMultiAdapter
from zope.viewlet.viewlet import ViewletBase

try:
    import plone.reload
    RELOAD_INSTALLED = True
except:
    RELOAD_INSTALLED = False


class ReloadViewlet(ViewletBase):
    reload_installed = RELOAD_INSTALLED

    def update(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                       name="plone_portal_state")
        portal = portal_state.portal()
        app = aq_parent(portal)
        self.code_url = '%s/@@reload?action=code' % app.absolute_url()
        self.zcml_url = '%s/@@reload?action=zcml' % app.absolute_url()

        self.css_url = '%s/portal_css/cookResources' % (
            portal.absolute_url())
        self.js_url = '%s/portal_javascripts/cookResources' % (
            portal.absolute_url())
