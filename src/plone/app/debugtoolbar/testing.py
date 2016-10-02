# -*- coding: utf-8 -*-
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class PloneAppDebugtoolbar(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import plone.app.debugtoolbar
        xmlconfig.file('configure.zcml',
                       plone.app.debugtoolbar,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.debugtoolbar:default')

PLONE_APP_DEBUGTOOLBAR_FIXTURE = PloneAppDebugtoolbar()
PLONE_APP_DEBUGTOOLBAR_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(PLONE_APP_DEBUGTOOLBAR_FIXTURE, ),
                       name="PloneAppDebugtoolbar:Integration")