import sys
import os

from shutil import rmtree
from setuptools import find_packages, setup, Command

from distutils.core import setup, Extension

# The directory containing this file
HERE = os.path.dirname(__file__)

NAME = 'fastlz5'
DESCRIPTION = "fastlz version 5"
URL = 'https://github.com/zackees/python-fastlz5'
EMAIL = 'dont@email.me'
AUTHOR = 'Zach Vorhies'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.0.1'

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fd:
    README = fd.read()
    

class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        pass

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(HERE, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(VERSION))
        os.system('git push --tags')
        sys.exit()


setup(
    name=NAME,
    version=VERSION,
    description='Python wrapper for FastLZ, a lightning-fast lossless '
                'compression library.',
    author=AUTHOR,
    url=URL,
    license='BSD License',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Archiving :: Compression',
        'Topic :: Utilities'
    ],
    ext_modules = [
        Extension(
            'fastlz',
            sources=['fastlz.c', 'fastlz/fastlz.c'],
            include_dirs=['fastlz']
        )
    ]
)
