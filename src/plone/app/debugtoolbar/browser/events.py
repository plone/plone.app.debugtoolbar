import os

from zope.viewlet.viewlet import ViewletBase

from datetime import datetime

import zope.event
import zope.component
from zope.interface import Interface
from zope.app.publication.interfaces import IBeforeTraverseEvent


_events_log = []


def clear_events_log(context, event):
    global _events_log
    _events_log = []


gsm = zope.component.getGlobalSiteManager()
gsm.registerHandler(clear_events_log, (Interface, IBeforeTraverseEvent))


default_blacklist = [
    'zope.contentprovider.interfaces.BeforeUpdateEvent',
    'zope.schema.fieldproperty.FieldUpdatedEvent',
    'z3c.form.widget.AfterWidgetUpdateEvent',
    'z3c.form.events.DataExtractedEvent',
    'z3c.form.action.ActionSuccessful',
]
blacklist = os.environ.get('TOOLBAR_EVENTS_BLACKLIST', '').split() or default_blacklist


def notify(event):
    """ Notify all subscribers of ``event``.
    """
    global _events_log

    start = datetime.now()

    for subscriber in zope.event.subscribers:
        subscriber(event)

    end = datetime.now()
    duration = end - start

    fq_name = '%s.%s' % (event.__class__.__module__, event.__class__.__name__)
    if fq_name not in blacklist:
        _events_log.append(dict(event=event, duration=duration))


class EventsViewlet(ViewletBase):

    def update(self):
        global _events_log

        # Copy list items, events_log is cleared every request.
        self.events = _events_log[:]

        self.blacklist = blacklist
