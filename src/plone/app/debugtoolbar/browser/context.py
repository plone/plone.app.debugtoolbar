# -*- coding: utf-8 -*-
import types
import inspect

from zope.interface import Interface
from zope.interface import providedBy, directlyProvidedBy
from zope.component import getAdapters
from zope.publisher.interfaces import IView
from zope.viewlet.viewlet import ViewletBase

from Acquisition import aq_base
from Products.CMFCore.interfaces import IDynamicType
from Products.CMFDynamicViewFTI.interfaces import IDynamicViewTypeInformation
from Products.Five.browser.metaconfigure import ViewMixinForTemplates

class ContextViewlet(ViewletBase):

    def update(self):

        self.path = '/'.join(self.context.getPhysicalPath())
        self.cls = self.context.__class__

        self.fti = None
        self.methodAliases = None

        if IDynamicType.providedBy(self.context):
            self.fti = self.context.getTypeInfo()
            self.methodAliases = sorted(self.fti.getMethodAliases().items())

        self.defaultView = None
        self.viewMethods = []
        if IDynamicViewTypeInformation.providedBy(self.fti):
            self.defaultView = self.fti.defaultView(self.context)
            self.viewMethods = self.fti.getAvailableViewMethods(self.context)

        directly_provided = directlyProvidedBy(self.context)
        self.provided = list(providedBy(self.context).flattened())
        self.provided.sort(key=lambda i: i.__identifier__)
        self.provided = ({'dottedname': i.__identifier__,
                          'is_marker': i in directly_provided}
                          for i in self.provided)
        self.views = []

        generator = getAdapters((self.context, self.request,), Interface)
        while True:
            try:
                name, view = generator.next()

                if not IView.providedBy(view):
                    continue

                cls = view.__class__
                module = cls.__module__
                template = None

                if isinstance(view, ViewMixinForTemplates):
                    template = view.index.filename
                else:
                    for attr in ('index', 'template', '__call__'):
                        pt = getattr(view, attr, None)
                        if hasattr(pt, 'filename'):
                            template = pt.filename
                            break

                # Deal with silly Five metaclasses
                if (
                    module == 'Products.Five.metaclass' and
                    len(cls.__bases__) > 0
                ):
                    cls = cls.__bases__[0]
                elif cls == ViewMixinForTemplates:
                    cls = None

                self.views.append({
                    'name': name,
                    'class': cls,
                    'template': template,
                })
            except StopIteration:
                break
            except:
                # Some adapters don't initialise cleanly
                pass

        self.views.sort(key=lambda v: v['name'])

        self.methods = []
        self.variables = []

        _marker = object()
        for name in sorted(dir(aq_base(self.context))):
            attr = getattr(aq_base(self.context), name, _marker)
            if attr is _marker:
                continue

            # FIXME: Should we include ComputedAttribute here ? [glenfant]
            if isinstance(attr, (int, long, float, basestring, bool, list, tuple, dict, set, frozenset)):
                self.variables.append({
                    'name': name,
                    'primitive': True,
                    'value': attr,
                })
            elif (
                isinstance(attr, (types.MethodType, types.BuiltinFunctionType, types.BuiltinMethodType, types.FunctionType)) or
                attr.__class__.__name__ == 'method-wrapper',
            ):

                source = None
                if name.endswith('__roles__'):
                    # name without '__roles__' is the last in self.methods since we're in a sorted(...) loop
                    if callable(attr):
                        secu_infos = attr()
                    else:
                        secu_infos = attr
                    if secu_infos is None:
                        secu_label = 'Public'
                    else:
                        secu_label = ''
                        try:
                            secu_label += 'Roles: ' + ', '.join([r for r in secu_infos[:-1]])
                        except TypeError:
                            # Avoid "TypeError: sequence index must be
                            # integer, not 'slice'", which occurs with the
                            # ``C`` security implementation. This is a rare
                            # case. In development you normally use the
                            # ``Python`` security implementation, where this
                            # error doesn't occur.
                            pass
                        secu_label += '. Permission: ' + secu_infos[-1][1:-11]  # _x_Permission -> x
                    self.methods[-1]['secu_infos'] = secu_label
                else:
                    try:
                        source = inspect.getsourcefile(attr)
                    except TypeError:
                        None

                    signature = name + "()"
                    try:
                        signature = name + inspect.formatargspec(*inspect.getargspec(attr))
                    except TypeError:
                        pass

                    self.methods.append({
                        'signature': signature,
                        'filename': source,
                        'help': inspect.getdoc(attr),
                    })
            else:
                self.variables.append({
                    'name': name,
                    'primitive': False,
                    'value': str(attr),
                })
