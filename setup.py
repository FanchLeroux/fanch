import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(
      name = "fanch",
      version = "0.1",
      author = "François Leroux",
      author_email = "francois.leroux.pro@gmail.com",
      description = "custom set of functions",
      #license = read('LICENSE.txt'),
      keywords = "adaptive optics",
      #url = "https://github.com/...",
      install_requires = install_requires,
      packages = [
                  'fanch'
                 ],
    package_dir = {'fanch': 'fanch'},
    data_files = [
                  ('', ['README.md', 'requirements.txt'])
                 ],
    classifiers = [
                   'Development Status :: 3 - Alpha',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: Developers',
                   'Topic :: Scientific/Engineering :: Physics',
                   'Programming Language :: Python',
                   #'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
                  ],
    python_requires = '>=3.8.20',
)
