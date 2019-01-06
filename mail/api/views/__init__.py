from pkgutil import walk_packages
from importlib import import_module
from aiohttp import web

routes = web.RouteTableDef()

for m in walk_packages(path=__path__):
    import_module('.' + m.name, __name__)
