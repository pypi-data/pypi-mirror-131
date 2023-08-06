from setuptools import setup

with open('README.md', 'rb') as f:
    long_descr = f.read().decode('utf-8')

setup(
    name = 'apollo-tylerhm',
    packages = ['apollo'],
    entry_points = {
        'console_scripts': ['apollo = apollo.apollo:_cli']
    },
    version = '0.0.6',
    description = 'Apollo checker. The most feared of all the gods',
    long_description = long_descr,
    author = 'Tyler Hostler-Mathis',
    author_email = 'tylerhm.dev@gmail.com',
    url = 'https://github.com/TylerMathis/apollo',
)
