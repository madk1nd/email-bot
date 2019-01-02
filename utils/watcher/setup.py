from setuptools import setup

setup(
    name='watch',
    py_modules=['watcher'],
    install_requires=['watchdog'],
    entry_points={
        'console_scripts': ['watch=watcher:main']
    }
)
