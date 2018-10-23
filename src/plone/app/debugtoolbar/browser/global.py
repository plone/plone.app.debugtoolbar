# -*- coding: utf-8 -*-
from zope.viewlet.viewlet import ViewletBase
from zc.lockfile import LockError

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

        # BBB: import for Zope2
        try:
            self.servers = config.servers
        except AttributeError:
            self.servers = []

        # BBB: import for Zope2
        try:
            self.appInfo = self.context.getPhysicalRoot()['Control_Panel']
        except KeyError:
            self.appInfo = self.context.getPhysicalRoot().Control_Panel

        self.databases = []
        paths = dict([(x[1], x[0],) for x in config.dbtab.mount_paths.items()])

        for db in config.databases:
            name = db.name
            # BBB: import for Zope2
            try:
                real_db = self.appInfo.Database[name]
                dbtabEntry = config.dbtab.databases[name]

                self.databases.append({
                    'name': name,
                    'location': real_db.db_name(),
                    'size': real_db.db_size(),
                    'cacheSize': dbtabEntry.getCacheSize(),
                    'mount': paths.get(name, None),
                })
            except LockError:
                # lock error when trying to access database
                # https://github.com/zopefoundation/Zope/issues/360
                db_config = db.config
                self.databases.append({
                    'name': name,
                    'location': 'TODO could not access db',
                    'size': 'TODO could not access db',
                    'cacheSize': db_config.cache_size,
                    'mount': paths.get(name, None),
                })
