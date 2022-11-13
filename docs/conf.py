# Sphinx documentation build configuration file
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinxarg.ext',
]
exclude_patterns = ['_build']

project = 'sphinx-argparse'
copyright = '2017, Alex Rudakov, Devon Ryan, and contributors'
release = version = '0.2.5'

# -- Options for HTML output ---------------------------------------------------

html_theme = 'furo'
pygments_style = 'sphinx'

htmlhelp_basename = 'sphinxargparsedoc'

# -- Options for LaTeX output --------------------------------------------------

latex_documents = [
    (
        'index',
        'sphinx-argparse.tex',
        'sphinx-argparse Documentation',
        'Alex Rudakov, Devon Ryan, and contributors',
        'manual',
    ),
]

# -- Options for manual page output --------------------------------------------

man_pages = [
    (
        'index',
        'sphinx-argparse',
        'sphinx-argparse Documentation',
        ['Alex Rudakov', 'Devon Ryan'],
        True,
    )
]

# -- Options for Texinfo output ------------------------------------------------

texinfo_documents = [
    (
        'index',
        'sphinx-argparse',
        'sphinx-argparse Documentation',
        'Alex Rudakov, Devon Ryan, and contributors',
        'sphinx-argparse',
        'A sphinx extension that automatically documents argparse commands and options.',
        'Miscellaneous',
    ),
]
