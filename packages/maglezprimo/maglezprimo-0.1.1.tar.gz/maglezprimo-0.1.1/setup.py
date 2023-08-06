from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='maglezprimo',
    version='0.1.1',
    description='A tool for searching & extracting information...',
    long_description=long_description,
    url='https://pypi.python.org/pypi/magr-primo',
    author='Miguel A Gonzalez',
    author_email='maglez@gmail.com',
    license='GNU GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
    ],
    keywords='primo magr r',
    packages=['primo'],
    package_dir = {'primo':'primo'},
)
