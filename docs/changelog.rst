**********
Change log
**********

0.5.0
#####

The following enhancements to the HTML output are described on the [Usage](https://sphinx-argparse.readthedocs.io/en/latest/usage.html) page.

* Optional command index.
* Optional ``:index-groups:`` field to the directive for an command-by-group index.
* A ``full_subcommand_name`` option to print fully-qualified sub-command headings.
  This option helps when more than one sub-command offers a ``create`` or ``list`` or other
  repeated sub-command.
* Each command heading is a domain-specific link target.
  You can link to commands and sub-commands with the ``:ref:`` role, but this
  release adds support for the domain-specific role like
  ``:commands:command:`sample-directive-opts A` ``.
  The ``:commands:command:`` role supports linking from other projects through the
  intersphinx extension.

Changes

* Previously, common headings such as **Positional Arguments** were subject to a
  process that made them unique but adding a ``_repeatX`` suffix to the HREF target.
  This release continues to support those HREF targets as secondary targets so that
  bookmarks continue to work.
  However, this release prefers using fully-qualified HREF targets like
  ``sample-directive-opts-positional-arguments`` as the primary HREF so that customers
  are less likely to witness the ``_repeatX`` link in URLs.


0.4.0
#####

* Minimum python version is now 3.7 by @ashb in https://github.com/ashb/sphinx-argparse/pull/25
* Fix anchor for toc by @Blaok in https://github.com/ashb/sphinx-argparse/pull/2
* feat: find executable filename to address #16 by @tsutterley in https://github.com/ashb/sphinx-argparse/pull/17
* Test against python 3.11 too by @ashb in https://github.com/ashb/sphinx-argparse/pull/22

0.3.1
#####

 * Include tests in sdist

0.3.0
#####

 * First release from ashb/sphinx-argparse
 * Declare that parallel builds are supported (issue #131).

0.2.5
#####

 * A more verbose error message is now printed if there's an issue during importing a script (issue #102).

0.2.4
#####

 * Various bug fixes and documentation updates.

0.2.3
#####

 * Fixed a variety of issues, such as with `@replace` (issue #99). Thanks to @evgeni
 * You can now skip sections with `@skip`. Thanks to @evgeni
 * Fixed handling of the epilog

0.2.2
#####

 * CommonMark is now only imported if absolutely required. This should fix failures on read the docs. Thanks to @Chilipp for fixing this!

0.2.1
#####

 * Stopped importing `sphinx.util.compat`, which was causing issues like that seen in `#65 <https://github.com/ribozz/sphinx-argparse/issues/65>`_

0.2.0
#####

 * Section titles can now be used in tables of contents and linked to. The title itself is also used as the anchor. In the case of repeated names `_replicateX`, where `X` is a number, is prepended to ensure that all titles are uniquely linkable. This was bug `#46 <https://github.com/ribozz/sphinx-argparse/issues/46>`_.
 * The positional (aka required) and named (aka optional) option sections are now named "Positional Arguments" and "Named Arguments", for the sake of clarity (e.g., named arguments can be required). This was issue `#58 <https://github.com/ribozz/sphinx-argparse/issues/58>`_.
 * Fixed quoting of default strings (issue `#59 <https://github.com/ribozz/sphinx-argparse/issues/59>`_).
 * Added the `:noepilog:` and `:nodescription:` options, thanks to @arewm.
 * Added the `:nosubcommand:` option, thanks to @arewm.

0.1.17
######

 * Fixed handling of argument groups (this was bug `#49 <https://github.com/ribozz/sphinx-argparse/issues/49>`_). Thanks to @croth1 for reporting this bug. Note that now position arguments (also known as required arguments) within argument groups are now also handled correctly.

0.1.16
######

 * Added a `:nodefaultconst:` directive, which is similar to the `:nodefault:` directive, but applies only to `store_true`, `store_false`, and `store_const` (e.g., it will hide the "=True" part in the output, since that can be misleading to users).
 * Fixed various typos (thanks to users mikeantonacci, brondsem, and tony)
 * Format specifiers (e.g., `%(prog)s` and `%(default)s`) are now filled in (if possible) in help sections. If there's a missing keyword, then nothing will be filled in. This was issue #27.
 * The package is now a bit more robust to incorrectly spelling module names (#39, courtesy of Gabriel Falcão)
 * Added support for argparse groups (thanks to Fidel Ramirez)

0.1.15
######

 * Fixed malformed docutils DOM in manpages (Matt Boyer)


0.1.14
######

 * Support for aliasing arguments #22 (Campbell Barton)
 * Support for nested arguments #23 (Campbell Barton)
 * Support for subcommand descriptions #24 (Campbell Barton)
 * Improved parsing of content of `epilog` and `description` #25 (Louis - https://github.com/paternal)
 * Added 'passparser' option (David Hoese)

0.1.13
######

 * Bugfix: Choices are not always strings (Robert Langlois)
 * Polished small mistakes in usage documentation (Dean Malmgren)
 * Started to improve man-pages support (Zygmunt Krynicki)

0.1.12
######

 * Improved error reporting (James Anderson)

0.1.11
######

 * Fixed stupid bug, prevented things working on py3 (Alex Rudakov)
 * added tox configuration for tests

0.1.10
######

 * Remove the ugly new line in the end of usage string (Vadim Markovtsev)
 * Issue #9 Display argument choises (Proposed by Felix-neko, done by Alex Rudakov)
 * :ref: syntax for specifying path to parser instance. Issue #7 (Proposed by David Cottrell, Implemented by Alex Rudakov)
 * Updated docs to read the docs theme

0.1.9
######

Fix problem with python version comparison, when python reports it as "2.7.5+" (Alex Rudakov)

0.1.8
#####

Argparse is not required anymore separate module as of python 2.7 (Mike Gleen)

0.1.7
#####

-- Nothing -- Created by accident.

0.1.6
#####

Adding :nodefault: directive that skips default values for options (Stephen Tridgell)

0.1.5
#####

Fix issue: epilog is ignored (James Anderson - https://github.com/jamesra)

0.1.4
#####

Fix issue #3: ==SUPPRESS== in option list with no default value

0.1.2
#####

Fix issue with subcommands (by Tony Narlock - https://github.com/tony)

0.1.1
#####

Initial version
