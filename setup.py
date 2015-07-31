import sys
import codecs

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import strongarm_msdns


class PyTest(TestCommand):
    # `$ python setup.py test' simply installs minimal requirements
    # and runs the tests with no fancy stuff like parallel execution.
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--doctest-modules', '--verbose',
            './strongarm_msdns', './tests'
        ]
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))


tests_require = [
    'py==1.4.30',
    'pytest==2.7.2',
    'pytest-cov==1.8.1',
]


install_requires = [
    'pywin32==219',
    'stronglib',
    'WMI==1.4.9',
]

### Conditional dependencies:

# sdist
if not 'bdist_wheel' in sys.argv:
    try:
        #noinspection PyUnresolvedReferences
        import argparse
    except ImportError:
        install_requires.append('argparse>=1.2.1')


# bdist_wheel
extras_require = {
    # http://wheel.readthedocs.org/en/latest/#defining-conditional-dependencies
    ':python_version == "2.6"'
    ' or python_version == "3.0"'
    ' or python_version == "3.1" ': ['argparse>=1.2.1'],
}


def long_description():
    with codecs.open('README.rst', encoding='utf8') as f:
        return f.read()

setup(
    name='strongarm-msdns',
    version=strongarm_msdns.__version__,
    description=strongarm_msdns.__doc__.strip(),
    long_description=long_description(),
    url='http://strongarm.io/',
    download_url='https://github.com/percipient/strongarm-msdns',
    author=strongarm_msdns.__author__,
    author_email='stephendicato@gmail.com',
    license=strongarm_msdns.__licence__,
    packages=find_packages(),
    extras_require=extras_require,
    install_requires=install_requires,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
        'Topic :: System :: Networking',
        'Topic :: Terminals',
        'Topic :: Utilities'
    ],
)
