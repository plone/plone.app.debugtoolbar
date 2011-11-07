import pkg_resources
from zope.viewlet.viewlet import ViewletBase

class VersionsViewlet(ViewletBase):

    def update(self):
        packages = []
        for distribution in pkg_resources.working_set:
            name = distribution.project_name
            packages.append({
                'name': name,
                'version':distribution.version,
            })
            
        self.packages = sorted(packages, key=lambda x: x['name'].lower())
