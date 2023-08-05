from setuptools import setup, Command
import sys


VERSION = '0.5.1.post0'


def read(fname):
    # makes sure that setup can be executed from a different location
    import os.path
    _here = os.path.abspath(os.path.dirname(__file__))
    return open(os.path.join(_here, fname)).read()

# make sure that versions match before uploading anything to the cheeseshop
if 'upload' in sys.argv or 'register' in sys.argv:
    import pytest_localserver
    assert pytest_localserver.VERSION == VERSION


class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import sys, subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)

setup(
    name='pytest-localserver',
    version=VERSION,
    author='Sebastian Rahlf',
    author_email='basti@redtoad.de',
    maintainer='David Zaslavsky',
    maintainer_email='diazona@ellipsix.net',
    license='MIT License',
    description='py.test plugin to test server connections locally.',
    long_description=read('README.rst'),
    url='https://github.com/pytest-dev/pytest-localserver',

    packages=['pytest_localserver'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*',
    install_requires=[
        'werkzeug>=0.10'
    ],
    cmdclass={'test': PyTest},
    tests_require=[
        'pytest>=2.0.0',
        'requests'
    ],
    entry_points={
        'pytest11': ['localserver = pytest_localserver.plugin']
    },

    zip_safe=False,
    include_package_data=True,

    keywords='py.test pytest server localhost http smtp',
    classifiers=[
        'Framework :: Pytest',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Testing'
    ]
)
