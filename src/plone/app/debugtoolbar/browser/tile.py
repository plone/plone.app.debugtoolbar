# -*- coding: utf-8 -*-
from plone.app.standardtiles.common import ProxyViewletTile


class ToolbarTile(ProxyViewletTile):
    """A footer tile."""
    manager = 'plone.portalfooter'
    viewlet = 'plone.app.debugtoolbar.toolbar'
