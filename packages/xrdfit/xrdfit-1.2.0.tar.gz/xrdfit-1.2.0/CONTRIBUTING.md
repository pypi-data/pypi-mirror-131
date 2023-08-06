# Contributing

We welcome bug reports, feature requests and suggestions for improvement made to this package. Below are some guidelines to keep in mind when requesting or making changes.

## Reporting Issues

If you encounter a problem with the code, please open an issue on the project's GitHub issue board: https://github.com/LightForm-group/xrdfit/issues

You should include details about what version of ``xrdfit`` you are using, what you are attempting to do, details of the error you encountered and if possible a [minimal working example](https://en.wikipedia.org/wiki/Minimal_working_example) that shows the problem.

## Coding style

This project uses the PEP8 standard for formatting Python code with the exception that the maximum line length is 120 characters.

Docstrings are formatted in the reStructuredText format. These are automatically harvested by the Sphinx autodoc extension and form the API documentation at Read The Docs: (https://xrdfit.readthedocs.io/en/latest/)

## Release guidelines

Releases follow the [semver](https://semver.org/) numbering scheme.

When releasing a new version the following need to be updated:
* Update version number in setup.py
* Update version number in docs/config.py
* Add tag to git repo of the version number prefixed by the letter “v”
* Draft release on GitHub for that tag with a list of changes since the last version
* Upload new version to PyPi