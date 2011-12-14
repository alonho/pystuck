from setuptools import setup
from pystuck import README

setup(name='pystuck',
      version='0.1',
      classifiers = ["Development Status :: 4 - Beta",
                     "Intended Audience :: Developers",
                     "License :: OSI Approved :: BSD License",
                     "Programming Language :: Python :: 2.7"],
      description=README,
      author='Alon Horev',
      author_email='alon@horev.net',
      packages=['pystuck'],
      install_requires=['rpyc>=3', 'ipython'],
      license='BSD',
      url='https://github.com/alonho/pystuck',
      entry_points={'console_scripts': ['pystuck=pystuck:main']})
