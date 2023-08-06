from setuptools import setup

name = "types-html5lib"
description = "Typing stubs for html5lib"
long_description = '''
## Typing stubs for html5lib

This is a PEP 561 type stub package for the `html5lib` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `html5lib`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/html5lib. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `df0a724c0f0ca558396aeb0f2fe755dc57c967a4`.
'''.lstrip()

setup(name=name,
      version="1.1.3",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['html5lib-stubs'],
      package_data={'html5lib-stubs': ['__init__.pyi', '_ihatexml.pyi', '_inputstream.pyi', '_tokenizer.pyi', '_trie/__init__.pyi', '_trie/_base.pyi', '_trie/py.pyi', '_utils.pyi', 'constants.pyi', 'filters/__init__.pyi', 'filters/alphabeticalattributes.pyi', 'filters/base.pyi', 'filters/inject_meta_charset.pyi', 'filters/lint.pyi', 'filters/optionaltags.pyi', 'filters/sanitizer.pyi', 'filters/whitespace.pyi', 'html5parser.pyi', 'serializer.pyi', 'treeadapters/__init__.pyi', 'treeadapters/genshi.pyi', 'treeadapters/sax.pyi', 'treebuilders/__init__.pyi', 'treebuilders/base.pyi', 'treebuilders/dom.pyi', 'treebuilders/etree.pyi', 'treebuilders/etree_lxml.pyi', 'treewalkers/__init__.pyi', 'treewalkers/base.pyi', 'treewalkers/dom.pyi', 'treewalkers/etree.pyi', 'treewalkers/etree_lxml.pyi', 'treewalkers/genshi.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
