from setuptools import setup

with open('requirements.txt') as file:
    requirements = file.read().split('\n')

with open('README.md', 'r') as file:
    long_description = file.read()

VERSION = '0.1'
AUTHOR = 'Manuel Cabral'
EMAIL = 'cabral.manuel@yandex.com'
DESCRIPTION = 'Obtención de datos sobre el COVID-19'
LICENSE = 'apache-2.0'

setup(
  name = 'codavi',
  packages = ['codavi'],
  version = VERSION,
  license = LICENSE,
  description = DESCRIPTION,
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  author = AUTHOR,
  author_email = EMAIL,
  url = 'https://github.com/manucabral/Codavi',
  keywords = ['python', 'covid', 'covid-19', 'covid-argentina', 'covid-data'],
  install_requires = requirements,
  python_requires = '>= 3.4',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.9',
    'Operating System :: Unix',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
  ],
)