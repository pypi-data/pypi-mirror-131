from setuptools import setup

name = "types-click-spinner"
description = "Typing stubs for click-spinner"
long_description = '''
## Typing stubs for click-spinner

This is a PEP 561 type stub package for the `click-spinner` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `click-spinner`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/click-spinner. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `df0a724c0f0ca558396aeb0f2fe755dc57c967a4`.
'''.lstrip()

setup(name=name,
      version="0.1.7",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['click_spinner-stubs'],
      package_data={'click_spinner-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
