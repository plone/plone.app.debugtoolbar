# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.interface import directlyProvidedBy
from zope.component import queryUtility
from zope.viewlet.viewlet import ViewletBase
from zope.publisher.interfaces.browser import IBrowserSkinType

from Products.CMFCore.utils import getToolByName


class ThemeViewlet(ViewletBase):

    def update(self):
        
        skins = getToolByName(self.context, 'portal_skins')
        url = getToolByName(self.context, 'portal_url')

        defaultSkin = skins.getDefaultSkin()
        requestVariable = skins.getRequestVarname()

        self.portal_url = url()
        self.portal = url.getPortalObject()

        # CMF skin
        self.themeName = self.request.get(requestVariable, defaultSkin)
        self.skinPaths = dict(skins.getSkinPaths()).get(self.themeName, '').split(',')

        # Browser layers
        self.themeLayer = queryUtility(IBrowserSkinType, name=self.themeName)
        self.layers = list(directlyProvidedBy(self.request).flattened())

        # CSS/JS composition
        self.css = getToolByName(self.context, 'portal_css')
        self.js = getToolByName(self.context, 'portal_javascripts')