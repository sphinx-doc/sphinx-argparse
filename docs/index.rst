``sphinx-argparse``
===================

`sphinx-argparse` is an extension for Sphinx_ that allows for
easy generation of documentation for command line tools using
Python's argparse_ library.

.. _Sphinx: https://www.sphinx-doc.org/
.. _argparse: https://docs.python.org/3/library/argparse.html

.. toctree::
   :hidden:
   :maxdepth: 1

   usage
   extend
   sample
   misc
   markdown
   changelog


Installation
------------

This extension works with Python 3.10 or later and Sphinx 5.1 or later.

The package is available in the `Python Package Index`_:

.. code:: shell

   pip install sphinx-argparse

And also in `conda-forge`_:

.. code:: shell

   mamba -c conda-forge install sphinx-argparse

Enable the extension in your sphinx config:

.. code:: python

    extensions = [
        ...,
        'sphinxarg.ext',
    ]

.. _Python Package Index: https://pypi.org/project/sphinx-argparse/
.. _conda-forge: https:://github.com/conda-forge/sphinx-argparse-feedstock/


Contribute
----------

Any help is welcome!

Most wanted:

* Additional features
* Bug fixes
* Examples

Contributions are gratefully accepted through `GitHub pull requests`_.
Please report any bugs as issues on GitHub.

.. _GitHub pull requests: https://github.com/sphinx-doc/sphinx-argparse/

Don't forget to run tests before committing:

.. code:: shell

   pytest


Similar projects
-------------------

* https://pypi.org/project/sphinxcontrib-autoprogram/
  (See a comparison: https://github.com/sphinx-doc/sphinx-argparse/issues/16)
