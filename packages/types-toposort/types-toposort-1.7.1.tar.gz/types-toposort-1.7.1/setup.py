from setuptools import setup

name = "types-toposort"
description = "Typing stubs for toposort"
long_description = '''
## Typing stubs for toposort

This is a PEP 561 type stub package for the `toposort` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `toposort`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/toposort. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `df0a724c0f0ca558396aeb0f2fe755dc57c967a4`.
'''.lstrip()

setup(name=name,
      version="1.7.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['toposort-stubs'],
      package_data={'toposort-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
