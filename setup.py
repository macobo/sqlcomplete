import re
import ast
from setuptools import setup, find_packages

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('sqlcomplete/version.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

description = 'Smart autocomplete for sql'

setup(
    name='sqlcomplete',
    author='Karl-Aksel Puulmann',
    author_email='oxymaccy@gmail.com',
    version=version,
    license='LICENSE',
    packages=find_packages(),
    package_data={'sqlcomplete': ['language/definition/postgresql']},
    description=description,
    # long_description=open('README.rst').read(),
    install_requires=[
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: SQL',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
