from AccessControl import getSecurityManager
from zope.viewlet.viewlet import ViewletBase

class UserViewlet(ViewletBase):

    def update(self):
        securityManager = getSecurityManager()

        self.user = securityManager.getUser()
        self.fullname = self.user.getProperty('fullname')
