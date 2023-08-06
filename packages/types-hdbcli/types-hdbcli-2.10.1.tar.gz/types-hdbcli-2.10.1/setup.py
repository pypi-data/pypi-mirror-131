from setuptools import setup

name = "types-hdbcli"
description = "Typing stubs for hdbcli"
long_description = '''
## Typing stubs for hdbcli

This is a PEP 561 type stub package for the `hdbcli` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `hdbcli`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/hdbcli. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `df0a724c0f0ca558396aeb0f2fe755dc57c967a4`.
'''.lstrip()

setup(name=name,
      version="2.10.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['hdbcli-stubs'],
      package_data={'hdbcli-stubs': ['__init__.pyi', 'dbapi.pyi', 'resultrow.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
