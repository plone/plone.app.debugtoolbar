# -*- coding: utf-8 -*-
import re
import cgi
import threading
import traceback

from zope.component import queryMultiAdapter
from zope.publisher.browser import BrowserView
from zope.viewlet.viewlet import ViewletBase

from paste.evalexception import evalcontext
from paste.exceptions import formatter

from AccessControl import Unauthorized
from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName
from Products.PageTemplates.Expressions import getEngine
from Products.CMFPlone.PloneBaseTool import createExprContext

class Variables(object):
    """Store local variables. Allow one set of variables per user id, and
    invalidate if the path of the context changes.
    """

    def __init__(self):
        self._lock = threading.RLock()
        self._storage = {}

    def invalidate(self, context, force=False):
        with self._lock:
            userId = getSecurityManager().getUser().getId()
            if userId not in self._storage:
                return

            if force or self._storage[userId]['path'] != '/'.join(context.getPhysicalPath()):
                del self._storage[userId]

    def get(self, context):
        self.invalidate(context)

        with self._lock:
            userId = getSecurityManager().getUser().getId()
            return self._storage.get(userId, {}).get('vars', {})

    def update(self, context, variables):
        with self._lock:
            userId = getSecurityManager().getUser().getId()

            self._storage[userId] = {
                'path': '/'.join(context.getPhysicalPath()),
                'vars': variables,
            }

VARS = Variables()

def htmlQuote(v):
    # Borrowed from Paste
    if v is None:
        return ''
    return cgi.escape(str(v), 1)

def preserveWhitespace(v, quote=True):
    # Borrowed from Paste
    if quote:
        v = htmlQuote(v)

    def _repl_nbsp(match):
        if len(match.group(2)) == 1:
            return '&nbsp;'
        return match.group(1) + '&nbsp;' * (len(match.group(2))-1) + ' '

    v = v.replace('\n', '<br>\n')
    v = re.sub(r'()(  +)', _repl_nbsp, v)
    v = re.sub(r'(\n)( +)', _repl_nbsp, v)
    v = re.sub(r'^()( +)', _repl_nbsp, v)
    return '<code>%s</code>' % v

class InteractiveViewlet(ViewletBase):

    def update(self):
        VARS.invalidate(self.context, force=True)

class InteractiveResponse(BrowserView):

    def __call__(self):

        if self.request.method != 'POST':
            raise Unauthorized()

        line = self.request.form.get('line', '')
        if not line.strip():
            return ''

        line = line.rstrip() + '\n'

        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        app = portal.getPhysicalRoot()

        globs = {
            'context': self.context,
            'request': self.request,
            'portal': portal,
            'app': app,
        }

        globs.update(VARS.get(self.context))
        context = evalcontext.EvalContext({}, globs)
        output = context.exec_expr(line)
        VARS.update(self.context, globs)

        line_html = formatter.str2html(line)
        return ('<code style="color: #060">&gt;&gt;&gt;</code> '
                '%s<br />\n%s'
                % (preserveWhitespace(line_html, quote=False),
                   preserveWhitespace(output)))

class TALESResponse(BrowserView):

    def __call__(self):

        if self.request.method != 'POST':
            raise Unauthorized()

        line = self.request.form.get('line', '')
        if not line.strip():
            return ''

        line = line.rstrip() + '\n'

        expr = self.compileExpression(line)
        try:
            output = expr(self.createExpressionContext())
        except:
            output = "%s" % traceback.format_exc()

        if isinstance(output, unicode):
            output = output.encode('ascii', 'xmlcharrefreplace')
        elif not isinstance(output, str):
            output = repr(output)

        return preserveWhitespace(output)


    def createExpressionContext(self):
        """Using the Plone expression context with all its variables
        """
        context_state = queryMultiAdapter((self.context, self.request), name=u'plone_context_state')
        portal_state = queryMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        return createExprContext(context_state.folder(), portal_state.portal(), self.context)

    def compileExpression(self, text):
        return getEngine().compile(text.strip())
