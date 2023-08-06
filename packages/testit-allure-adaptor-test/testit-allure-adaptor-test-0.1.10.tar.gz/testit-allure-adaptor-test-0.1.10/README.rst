Allure report adaptor for Test IT
==================================
.. image:: https://img.shields.io/pypi/v/testit-allure-adaptor?style=plastic
        :target: https://pypi.org/project/testit-allure-adaptor/

.. image:: https://img.shields.io/pypi/dm/testit-allure-adaptor?style=plastic
        :target: https://pypi.org/project/testit-allure-adaptor/

.. image:: https://img.shields.io/pypi/pyversions/testit-allure-adaptor?style=plastic
        :target: https://pypi.org/project/testit-allure-adaptor/

.. image:: https://img.shields.io/github/contributors/testit-tms/testit-allure-adaptor?style=plastic
        :target: https://github.com/testit-tms/testit-allure-adaptor

Installation
=============
Clone this project and open the console in the project directory:

.. code:: bash

    $ pip install testit-allure-adaptor

Usage
======

.. code:: bash

    $ testit --resultsdir allure-results

    $ testit --help

Changes in update 0.1.9
========================

- Fixed the sequence of steps before and after
- The namespace value has been removed from the section, only the classname value is used

Changes in update 0.1.8
========================

- Fixed mapping for results' fields from **newman-reporter-allure**
