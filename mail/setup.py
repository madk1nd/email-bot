from setuptools import setup

setup(
	name='apimail',
	packages=['api'],
	install_requires=['aiohttp', 'aiohttp_swagger', 'motor', 'simple-crypt'],
	entry_points={
		'console_scripts': ['apimail=api.application:main'],
	},
)
