from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import os
import sys
import re

package_name = os.path.split(os.path.dirname(os.path.realpath(__file__)))[-1]

def get_metadata(metadata_str):
    VERSIONFILE = os.path.join(os.path.abspath(os.path.dirname(__file__)),package_name, '__init__.py')
    initfile_lines = open(VERSIONFILE, 'rt').readlines()
    VSRE = r"^%s = ['\"]([^'\"]*)['\"]" % metadata_str
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (VERSIONFILE,))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

def prepend_find_packages(*roots):
    ''' Recursively traverse nested packages under the root directories
    '''
    packages = []
    
    for root in roots:
        packages += [root]
        packages += [root + '.' + s for s in find_packages(root)]
        
    return packages

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_args_cov = self.test_args + ['--cov=%s' % package_name, '--cov-report=term', '--cov-report=html']
        self.test_suite = True

    def run_tests(self):
        import pytest
        
        try:
            errcode = pytest.main(self.test_args_cov)
        except:
            errcode = pytest.main(self.test_args)
        sys.exit(errcode)

version = get_metadata('__version__')

setup(
    name=package_name,
    version=version,
    tests_require=['pytest'],
    install_requires=[],
    cmdclass={'test': PyTest},
    packages=prepend_find_packages(package_name),
    include_package_data=True,
    package_data={'':['*.md', '*.txt', '*.cfg']},
    platforms='any',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: Apache Software License :: 2.0',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        ],
    extras_require={
        'testing': ['pytest'],
    }
)
