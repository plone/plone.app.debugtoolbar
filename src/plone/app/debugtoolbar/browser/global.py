# -*- coding: utf-8 -*-
from zope.viewlet.viewlet import ViewletBase

class GlobalViewlet(ViewletBase):

    def update(self):
        from App.config import getConfiguration
        self.debug = getConfiguration().debug_mode

        import App.config
        config = App.config.getConfiguration()

        self.config = []
        for name in sorted(config.getSectionAttributes()):

            if name in (
                'access', 'databases', 'eventlog', 'servers',
            ):
                continue

            self.config.append((name, getattr(config, name)))

        self.servers = config.servers

        self.appInfo = self.context.getPhysicalRoot()['Control_Panel']

        self.databases = []
        paths = dict([(x[1], x[0],) for x in config.dbtab.mount_paths.items()])

        for name in self.appInfo.Database.getDatabaseNames():
            db = self.appInfo.Database[name]
            dbtabEntry = config.dbtab.databases[name]

            self.databases.append({
                'name': name,
                'location': db.db_name(),
                'size': db.db_size(),
                'cacheSize': dbtabEntry.getCacheSize(),
                'mount': paths.get(name, None),
            })
