#pipe line monkeypatch
#https://stackoverflow.com/a/69489056/14632651
from django.core.servers.basehttp import WSGIServer
WSGIServer.handle_error = lambda *args, **kwargs: None