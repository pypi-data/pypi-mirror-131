__version__ = '1.4.0'

try:
    from gevent.monkey import patch_all
    patch_all()
except:
    pass  # setup.py that is importing __version__
