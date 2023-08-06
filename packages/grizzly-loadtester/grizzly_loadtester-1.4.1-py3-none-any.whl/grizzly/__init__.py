__version__ = '1.4.1'

try:
    from gevent.monkey import patch_all
    patch_all()
except:
    pass  # setup.py that is importing __version__
