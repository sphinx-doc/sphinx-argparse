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

* `<https://github.com/tox-dev/sphinx-argparse-cli>`_

  A different ``argparse``-to-docs converter released in 2021, with a
  similar result as ``sphinx-argparse`` but with very different workings.
  The project is still actively being developed by the Tox team.
  This discussion highlights the difference: `<https://github.com/tox-dev/sphinx-argparse-cli/discussions/262>`_

* `<https://github.com/sphinx-contrib/autoprogram>`_

  A predecessor to ``sphinx-argparse``, released in 2014 but not updated since 2024.
