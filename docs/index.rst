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

This extension works with Python 3.10 or later and Sphinx 5.1 or later.

The package is available in the `Python Package Index`_::

    pip install sphinx-argparse

And also in `conda-forge`_::

    mamba -c conda-forge install sphinx-argparse

Enable the extension in your sphinx config::

    extensions = [
        ...,
        'sphinxarg.ext',
    ]

.. _Python Package Index: https://pypi.org/project/sphinx-argparse/
.. _conda-forge: https:://github.com/conda-forge/sphinx-argparse-feedstock/


References
==========

Similar projects
-------------------

 * https://pythonhosted.org/sphinxcontrib-autoprogram/ (See for comparison: https://github.com/ribozz/sphinx-argparse/issues/16)
