import os
import setuptools


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name='sphinx-argparse-nni',
    version=get_version('sphinxarg4nni/__init__.py'),
    author='Ash Berlin-Taylor, Yuge Zhang',
    author_email='ash_github@firemirror.com, scottyugochang@gmail.com',
    description='A sphinx extension that automatically documents argparse commands and options, tailored for NNI',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/ultmaster/sphinx-argparse',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Sphinx :: Extension',
    ],
    python_requires='>=3.6',
    install_requires=[
        "sphinx>=1.2.0"
    ]
)
