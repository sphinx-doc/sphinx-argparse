`sphinx-argparse`
=================

`sphinx-argparse` is an extension for sphinx that allows for easy generation of documentation for command line tools using the python argparse library.



.. toctree::
   :maxdepth: 2

   usage
   extend
   sample
   misc
   markdown
   changelog
   contrib


Installation
------------

This extension is tested on python 2.7 and 3.3+.

The package is available in the Python Package Index::

    pip install sphinx-argparse

And also in conda-forge::

    mamba -c conda-forge install sphinx-argparse

Enable the extension in your sphinx config::

    extensions += ['sphinxarg.ext']


References
==========

Similar projects
-------------------

 * https://pythonhosted.org/sphinxcontrib-autoprogram/ (See for comparison: https://github.com/ribozz/sphinx-argparse/issues/16)
