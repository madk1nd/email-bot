from setuptools import setup

setup(
    name='emulator',
    py_modules=['emulator'],
    install_requires=['aiohttp'],
    entry_points={
        'console_scripts': ['emulate=emulator:main']
    }
)