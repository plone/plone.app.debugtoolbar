Changelog
=========

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
