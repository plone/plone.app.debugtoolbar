# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

import logging


logger = logging.getLogger('plone.app.debugtoolbar upgrade')


def upgrade_1_to_2(context):
    """Remove JS and CSS resources from portal_css and portal_js registry.
    """
    def unregister_resource(registry, resource):
        if registry and registry.getResource(resource):
            registry.unregisterResource(resource)
            logger.info("Removed {0} from {1}".format(resource, registry.id))

    # Unregister JavaScript
    unregister_resource(
        getToolByName(context, 'portal_javascripts'),
        '++resource++plone.app.debugtoolbar/debugtoolbar.js'
    )

    # Unregister CSS
    unregister_resource(
        getToolByName(context, 'portal_css'),
        '++resource++plone.app.debugtoolbar/debugtoolbar.css'
    )
