import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="periodicgw",
  version="1.0",
  author="Scott K. Hansen, Lian Zhou",
  author_email='skh@bgu.ac.il',
  description="Generates doubly-periodic random 2D Darcy flow fields with arbitrary mean flow direction",
  license_files=('LICENSE.txt',),
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  url='https://gitlab.com/scottkalevhansen/periodic-gw',
  install_requires=['numpy','matplotlib','scipy'],
)