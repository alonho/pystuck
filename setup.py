from setuptools import setup

README = """
pystuck.py is a utility for analyzing stuck python programs (or just hardcore debugging).

in order to debug a python program (hence, the debugee),
add this line anywhere at startup: import pystuck; pystuck.run_server().

this script is the client, once invoked it connects to the debuggee
and prints the debugee's threads stack traces (good for most cases).
in addition, it opens an ipython prompt with an rpyc connection that provides
access to the debuggee's modules (good for inspecting variables)."""

setup(name='pystuck',
      version='0.3',
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
