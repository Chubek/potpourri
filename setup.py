from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent
INSTALL_REQUIRES = (HERE / "requirements.txt").read_text().splitlines()

setup(
   name='potpourri',
   version='0.1.0',
   author='Chubak Bidpaa',
   author_email='chubak.bidpaa@octoshrew.com',
   packages=['potpourri', 'potpourri.scripts'],
   url='https://github.com/OctoShrew/potpourri',
   license='LICENSE',
   description='A feature-rich web scraper',
   long_description=open('README.md').read(),
   install_requires=INSTALL_REQUIRES,
)