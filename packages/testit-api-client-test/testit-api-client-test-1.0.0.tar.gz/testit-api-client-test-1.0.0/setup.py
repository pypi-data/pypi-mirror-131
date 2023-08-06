from setuptools import setup

setup(
    name='testit-api-client-test',
    version='1.0.0',
    description='API-client for Test IT',
    long_description=open('README.rst').read(),
    url='https://pypi.org/project/testit-api-client-test/',
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
    py_modules=['testit', 'testit_api_client_test'],
    packages=['testit_api_client_test'],
    package_dir={'testit_api_client_test': 'src'},
    install_requires=['requests']
)
