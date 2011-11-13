.. contents::

Introduction
============

``plone.app.debugtoolbar`` provides a wealth of debug information about a
running Plone site at your fingertips. Simply install it in your build
(e.g. by adding it to the ``eggs`` list in your Buildout and re-running
buildout) and install it into your Plone site.

You should now see a ``Debug`` link at the top of your site. Click it to open
the debug drawer. Click on a panel to view relevant information.

Panels include:

* Context, showing information about the current content object
* Zope, showing information about how the Zope server is configured
* Published, showing information about the page template or view that was
  published
* Request, showing information about the request that produced the current page
* Response, showing informationa about the response that produced the current
  page
* Theme, showing information about the current theme and browser layers
* User, showing information about the current user
* Versions, listing the versions of every package known to the Zope process
* Workflow, showing information about workflow and security

Integration
===========

Each panels is included as a viewlet. You can register new panels using a
viewlet registration like this::

    <browser:viewlet
        name="plone.app.debugtoolbar.somepanel"
        manager="plone.app.debugtoolbar.browser.interfaces.IDebugToolbarViewletManager"
        class=".somepanel.SomePanelViewlet"
        template="somepanel.pt"
        permission="zope2.View"
        layer="plone.app.debugtoolbar.browser.interfaces.IDebugToolbarLayer"
        />

See ``plone.app.debugtoolbar.browser`` for plenty of examples of panels.