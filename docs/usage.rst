===========
Basic usage
===========

This extension adds the "argparse" directive::

    .. argparse::
       :module: my.module
       :func: my_func_that_returns_a_parser
       :prog: fancytool

The `module`, `func` and `prog` options are required.

`func` is a function that returns an instance of the `argparse.ArgumentParser` class.

Alternatively, one can use :ref: like this::

    .. argparse::
       :ref: my.module.my_func_that_returns_a_parser
       :prog: fancytool

In this case :ref: points directly to argument parser instance.

For this directive to work, you should point it to the function that will return a pre-filled `ArgumentParser`.
Something like::

    def my_func_that_return_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument('foo', default=False, help='foo help')
        parser.add_argument('bar', default=False)

        subparsers = parser.add_subparsers()

        subparser = subparsers.add_parser('install', help='install help')
        subparser.add_argument('ref', type=str, help='foo1 help')
        subparser.add_argument('--upgrade', action='store_true', default=False, help='foo2 help')

        return parser

.. note::
    We will use this example as a reference for every example in this document.

To document a file that is not part of a module, use :filename::

    .. argparse::
       :filename: script.py
       :func: my_func_that_returns_a_parser
       :prog: script.py

The 'filename' option could be absolute path or a relative path under current
working dir.

\:module\:
    Module name, where the function is located

\:func\:
    Function name

\:ref\:
    A combination of :module: and :func:

\:filename\:
    A file name, in cases where the file to be documented is not part of a module.

\:prog\:
    The name of your tool (or how it should appear in the documentation). For example, if you run your script as
    `./boo --some args` then \:prog\: will be "boo"

That's it. Directives will render positional arguments, options and sub-commands.

.. _about-subcommands:

About Sub-Commands
==================

Sub-commands are limited to one level. But, you can always output help for subcommands separately::

    .. argparse::
       :module: my.module
       :func: my_func_that_return_parser
       :prog: fancytool
       :path: install

This will render same doc for "install" subcommand.

Nesting level is unlimited::

    .. argparse::
       :module: my.module
       :func: my_func_that_return_parser
       :prog: fancytool
       :path: install subcomand1 subcommand2 subcommand3


Other useful directives
=======================

:nodefault: Do not show any default values.

:nodefaultconst: Like nodefault:, except it applies only to arguments of types `store_const`, `store_true` and `store_false`.

:nosubcommands: Do not show subcommands.

:noepilog: Do not parse the epilogue, which can be useful if it contains text that could be incorrectly parse as reStructuredText.

:nodescription: Do not parse the description, which can be useful if it contains text that could be incorrectly parse as reStructuredText.

:passparser: This can be used if you don't have a function that returns an argument parser, but rather adds commands to it (`:func:` is then that function).

:index-groups: This option is related to grouping related commands in an index.


Printing Fully Qualified Sub-Command Headings
=============================================

By default, when a command has sub-commands, such as ``fancytool install`` shown in the
:ref:`about-subcommands` section, the heading for the sub-command does not include the command name.
For instance, the the heading is **install** rather than **fancytool install**.

If you prefer to show the full command, **fancytool install**, then you can enable
the option in the ``conf.py`` for your project:

.. code-block:: python

   sphinx_argparse_conf = {
     "full_subcommand_name": True,
   }


Indices
=======

The extension supports two types of optional indices.
The first type of index is a simple index that provides a list of all the commands in the project by fully qualified name and a link to each command.
The second type of index enables you to group related commands into groups and then provide a list of the commands and a link to each command.
By default, no index is created.

Simple Command Index
--------------------

To enable the simple command index, add the following to the project ``conf.py`` file:

.. code-block:: python

    sphinx_argparse_conf = {
      "build_commands_index": True,
      "commands_index_in_toctree": True,
    }

The first option, ``build_commands_index``, instructs the extension to create the index.
For an HTML build, the index is created with the file name ``commands-index.html`` in the output directory.
You can reference the index from other files with the ``:ref:`commands-index``` markup.

The second option, ``commands_index_in_toctree``, enables you to reference the the index in a ``toctree`` directive.
By default, you cannot reference indices generated by extensions in a ``toctree``.
When you enable this option, the extension creates a temporary file that is named ``commands-index.rst`` in the source directory of your project.
Sphinx locates the temporary file and that makes it possible to reference the file in the ``toctree``.
When the Sphinx build finishes, the extension removes the temporary file from the source directory.

Commands by Group Index
-----------------------

To enable the more complex index, add the following to the project ``conf.py`` file:

.. code-block:: python

    sphinx_argparse_conf = {
      "build_commands_by_group_index": True,
      "commands_by_group_index_in_toctree": True,
    }

Add the ``:index-groups:`` option to the ``argparse`` directive in your documentation files.
Specify one or more groups that the command belongs to (comma-separated).

.. code-block:: reStructuredText

    .. argparse::
       :filename: ../test/sample.py
       :func: parser
       :prog: sample
       :index-groups: Basic Commands

For an HTML build, the index is created with the file name ``commands-by-group.html`` in the output directory.
You can cross reference the index from other files with the ``:ref:`commands-by-group``` role.

Like the simple index, the ``commands_by_group_index_in_toctree`` option enables you to reference the index in ``toctree`` directives.

This index has two more options.

.. code-block:: python

    sphinx_argparse_conf = {
      "commands_by_group_index_in_toctree": True,
      "commands_by_group_index_file_suffix": "by-service",
      "commands_by_group_index_title": "Commands by Service",
    }

The ``commands_by_group_index_file_suffix`` option overrides the default index name of ``commands-by-group.html``.
The value ``commands-`` is concatenated with the value you specify.
In the preceding sample, the index file name is created as ``commands-by-service.html``.
If you specify this option, the default reference of ``:ref:`commands-by-group``` is overridden with the value that you create.

The ``commands_by_group_index_title`` option overides the default first-level heading for the file.
The default heading is "Commands by Group".
The value you specify replaces the default value.

Customizing the Indices
-----------------------

By default, indices are created with the ``domainindex.html`` template.
If you want to customize the appearance of an index, copy the default ``domainindex.html`` file for your theme to the ``_templates`` directory in your project and modify it.

If you want to customize both indices, but one template cannot accommodate both of them, you can create an additional index template, such as ``customindex.html``.
You can configure Sphinx to use the additional template for an index by modifying the ``conf.py`` for the project like the following example.

.. code-block:: python

   def page_template(app: "Sphinx", pagename, templatename, context, doctree) -> str:
       if pagename == "commands-by-group":
           return "customindex.html"
       else:
           return templatename

   def setup(app: "Sphinx"):
       app.connect('html-page-context', page_template)

For more information, refer to the Sphinx documentation for :ref:`sphinx:templating` and the :doc:`sphinx:extdev/appapi`.
