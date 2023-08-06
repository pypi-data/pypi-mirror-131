from setuptools import setup

setup(
    name='testit-allure-adaptor-test',
    version='0.1.10',
    description='Allure report adaptor for Test IT',
    long_description=open('README.rst').read(),
    url='https://pypi.org/project/testit-allure-adaptor-test/',
    author='Pavel Butuzov',
    author_email='pavel.butuzov@testit.software',
    license='Apache-2.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    packages=['testit_allure_adaptor_test'],
    package_data={'testit_allure_adaptor_test': ['../connection_config.ini']},
    package_dir={'testit_allure_adaptor_test': 'src'},
    install_requires=['testit-api-client'],
    entry_points={'console_scripts': ['testit_test = testit_allure_adaptor_test.__main__:console_main']}
)
