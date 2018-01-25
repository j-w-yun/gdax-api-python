from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name = 'gdax-api',
	version = '1.2.0.dev1',
	description='GDAX public and authenticated client.',
	long_description=long_description,
	url='https://github.com/Jaewan-Yun/gdax-api-python',
	author='Jaewan Yun',
	author_email='jay50@pitt.edu',
	license='MIT',
	keywords='gdax',
	packages=find_packages(exclude=['tests']),
	install_requires=['requests']
	)