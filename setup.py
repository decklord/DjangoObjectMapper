from os.path import abspath, dirname, join, normpath

from setuptools import find_packages, setup


setup(

    # Basic package information:
    name = 'django-object-mapper',
    version = '0.1',
    packages = find_packages(),

    # Packaging options:
    zip_safe = False,
    include_package_data = True,

    # Package dependencies:
    install_requires = ['Django>=1.5.0'],

    # Metadata for PyPI:
    author = 'Camilo Lopez',
    author_email = 'camilo.lopez.a@gmail.com',
    license = 'UNLICENSE',
    url = 'http://decklord.tumblr.com',
    keywords = 'django mapper class dictionary',
    description = 'Simple mapper class to transform from random a custom class to Django object.',
    long_description = open(normpath(join(dirname(abspath(__file__)),
        'README.md'))).read()

)