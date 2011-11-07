from zope.viewlet.viewlet import ViewletBase

class ResponseViewlet(ViewletBase):

    def update(self):
        self.headers = []

        for k in sorted(self.request.response.headers):
            header = '-'.join([x.capitalize() for x in k.split('-')])
            self.headers.append((header, self.request.response.headers[k],))
