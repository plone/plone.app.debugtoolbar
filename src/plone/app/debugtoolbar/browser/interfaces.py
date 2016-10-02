# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager

class IDebugToolbarLayer(Interface):
    """Browser layer marker interface
    """

class IDebugToolbarViewletManager(IViewletManager):
    """Marker interface for the debug toolbar viewlet manager
    """
