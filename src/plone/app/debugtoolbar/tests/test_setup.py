# -*- coding: utf-8 -*-
from plone.app.debugtoolbar.testing import PLONE_APP_DEBUGTOOLBAR_INTEGRATION_TESTING  # noqa: E501
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):

    layer = PLONE_APP_DEBUGTOOLBAR_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.qi_tool = get_installer(self.portal, self.request)

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        pid = 'plone.app.debugtoolbar'
        self.assertTrue(
            self.qi_tool.is_product_installed(pid),
            'package appears not to have been installed',
        )
