from importlib.metadata import distributions
from Products.CMFCore.utils import getToolByName
from zope.viewlet.viewlet import ViewletBase


class VersionsViewlet(ViewletBase):

    def update(self):
        packages = []
        self.ploneVersion = None

        for distribution in distributions():
            name = distribution.name
            if name is None:
                # broken/incomplete distribution metadata
                continue
            packages.append(
                {
                    "name": name,
                    "version": distribution.version,
                }
            )

            if name.lower() == "plone":
                self.ploneVersion = distribution.version
            elif self.ploneVersion is None and name.lower() == "products.cmfplone":
                self.ploneVersion = distribution.version

        self.packages = sorted(packages, key=lambda x: x["name"].lower())

        mt = getToolByName(self.context, "portal_migration")
        self.needUpgrading = mt.needUpgrading()
