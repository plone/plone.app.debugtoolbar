Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

1.4.0 (2024-03-19)
------------------

New features:


- Added more improvements about i18n support [macagua]

  Updated Spanish translation [macagua]

  Updated the documentation [macagua]

  Upgraded the buildout configuration to Plone 6.0 version [macagua] (#31)


1.3.0 (2022-12-02)
------------------

Bug fixes:


- Add support for Python 3.11 [pbauer] (#30)


1.2.3 (2021-12-29)
------------------

Bug fixes:


- Fix missing zcml directive when `plone.app.standardtiles` is installed.
  [petschki] (#18)
- Fix brackets in toolbar-help
  [djowett] (#25)
- Fix a compatibility issue with Python 3.8 (#27)


1.2.2 (2020-04-20)
------------------

Bug fixes:


- Minor packaging updates. (#1)


1.2.0 (2019-01-09)
------------------

New features:

- Prepare for Python 2 / 3 compatibility [jmevissen]


1.1.4 (2018-03-07)
------------------

Bug fixes:

- Remove unittest2 dependency
  [kakshay21]

- Make it work in chrome, as '<script />' no longer works.
  [jaroel]


1.1.3 (2017-07-03)
------------------

Bug fixes:

- Fix problem with debugtoolbar panel opening on click but immediately closing again.
  [sunew]


1.1.2 (2017-03-31)
------------------

Bug fixes:

- Fix imports from Globals that was removed in Zope4
  [pbauer]

- Add coding headers on python files.
  [gforcada]

1.1.1 (2016-08-17)
------------------

Bug fixes:

- Use zope.interface decorator.
  [gforcada]


1.1.0 (2016-06-07)
------------------

New:

- Add a ``plone.app.debugtoolbar.toolbar`` tile for displaying in plone.app.blocks layouts.
  [thet]

- Plone 5 compatibility: Don't register JS and CSS but include them inline.
  Includes upgrade step.
  [thet]

- Added panel with catalog info: indexed values and metadata of the current
  object.
  [sunew]


1.0 (2014-08-13)
----------------

- Fix ``scrollHeight`` for the interactive prompt for jQuery 1.7+. Now,
  executing code jumps again to the latest prompt message.
  [thet]

- Removed 'xxx__roles__' methods from Context / Methods viewlet and added
  roles + permission for each method when available.
  [glenfant]

- Emphasize marker interfaces in context view
  [glenfant]

- Provide same variables as in portal_actions in TAL tests
  [glenfant]

- Fix themelayer. Use IBrowserSkinType instead of generic
  Interface which can return an real utility instead of an
  iface and broke the page rendering. Skin Layer must inherits
  from IBrowserSkinType
  [toutpt]


1.0a3 (2013-02-06)
------------------

- completed i18n support and added it translation

- add reload panel
  [vangheem]

- added Spanish translation and Uninstall GenericSetup profile
  [macagua]

- completed i18n support and added it translation
  [giacomos]

- replace checkboxes with mark symbols in permission matrix
  [gaudenz]

- permission matrix display improvements
  [gaudenz]

1.0a2 (13/11/2011)
------------------

- Add interactive code debugging
  [optilude]

- Add TALES tester
  [optilude]

- Add details of context methods and attributes
  [optilude]

1.0a1 (13/11/2011)
------------------

- Initial release
  [optilude]
