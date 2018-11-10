# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from zope.viewlet.viewlet import ViewletBase

import pkg_resources


class VersionsViewlet(ViewletBase):

    def update(self):
        packages = []
        self.ploneVersion = None

        for distribution in pkg_resources.working_set:
            name = distribution.project_name
            packages.append({
                'name': name,
                'version': distribution.version,
            })

            if name.lower() == 'plone':
                self.ploneVersion = distribution.version
            elif self.ploneVersion is None and name.lower() == 'products.cmfplone':  # noqa: E501
                self.ploneVersion = distribution.version

        self.packages = sorted(packages, key=lambda x: x['name'].lower())

        mt = getToolByName(self.context, 'portal_migration')
        self.needUpgrading = mt.needUpgrading()
