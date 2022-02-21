# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


project = 'qt-handy'
copyright = '2022, Zsolt Kovari'
author = 'Zsolt Kovari'

version = '0.1.0'

extensions = [
    'sphinx_rtd_theme',
    'sphinx_copybutton',
]

templates_path = ['_templates']

exclude_patterns = []

html_theme = "sphinx_rtd_theme"

html_static_path = ['_static']

rst_epilog = f'''
.. |project| replace:: `Qt Handy <https://www.github.com/plotlyst/qt-handy/>`__
.. |qtpy| replace:: `QtPy <https://pypi.org/project/QtPy/>`__
.. |license| replace:: `MIT <https://github.com/plotlyst/qt-handy/blob/main/LICENSE>`__

'''
