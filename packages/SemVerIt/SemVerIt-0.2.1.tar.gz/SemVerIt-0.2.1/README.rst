.. image:: https://img.shields.io/pypi/status/SemVerIt
    :alt: PyPI - Status

.. image:: https://img.shields.io/pypi/wheel/SemVerIt
    :alt: PyPI - Wheel

.. image:: https://img.shields.io/pypi/pyversions/SemVerIt
    :alt: PyPI - Python Version

.. image:: https://img.shields.io/github/v/release/hendrikdutoit/SemVerIt
    :alt: GitHub release (latest by date)

.. image:: https://img.shields.io/github/license/hendrikdutoit/SemVerIt
    :alt: License

.. image:: https://img.shields.io/github/issues-raw/hendrikdutoit/SemVerIt
    :alt: GitHub issues

.. image:: https://img.shields.io/pypi/dm/BEETest21
    :alt: PyPI - Downloads

.. image:: https://img.shields.io/github/search/hendrikdutoit/SemVerIt/GitHub hit
    :alt: GitHub Searches

.. image:: https://img.shields.io/codecov/c/gh/hendrikdutoit/SemVerIt
    :alt: CodeCov
    :target: https://app.codecov.io/gh/hendrikdutoit/SemVerIt

.. image:: https://img.shields.io/github/workflow/status/hendrikdutoit/SemVerIt/Pre-Commit
    :alt: GitHub Actions - Pre-Commit
    :target: https://github.com/hendrikdutoit/SemVerIt/actions/workflows/pre-commit.yaml

.. image:: https://img.shields.io/github/workflow/status/hendrikdutoit/SemVerIt/CI
    :alt: GitHub Actions - CI
    :target: https://github.com/hendrikdutoit/SemVerIt/actions/workflows/ci.yaml

.. image:: https://img.shields.io/pypi/v/SemVerIt
    :alt: PyPi

Manipulate semantic versioning (SemVer)

    Manipulate semantic version numbers. Create a new version number, initialize it with an, existing number or alternatively read it from an existing project setup.py file. See also https://semver.org/

=======
Testing
=======

This project uses ``pytest`` to run tests and also to test docstring examples.

Install the test dependencies.

.. code-block:: bash

    $ pip install - r requirements_test.txt

Run the tests.

.. code-block:: bash

    $ pytest tests
    === XXX passed in SSS seconds ===

==========
Developing
==========

This project uses ``black`` to format code and ``flake8`` for linting. We also support ``pre-commit`` to ensure these have been run. To configure your local environment please install these development dependencies and set up the commit hooks.

.. code-block:: bash

    $ pip install black flake8 pre-commit
    $ pre-commit install

=========
Releasing
=========

Releases are published automatically when a tag is pushed to GitHub.

.. code-block:: bash

    # Set next version number
    export RELEASE = x.x.x
    
    # Create tags
    git commit --allow -empty -m "Release $RELEASE"
    git tag -a $RELEASE -m "Version $RELEASE"
    
    # Push
    git push upstream --tags

