"""
The ReverseProxied class.
module: src/config/reverse_proxied.py
"""

from wsgiref.types import StartResponse, WSGIEnvironment
from flask import Flask


class ReverseProxied:
    """
    Helper class for handling reverse proxy.
    """

    def __init__(self, app: Flask):
        self.app = app

    def __call__(self, environ: WSGIEnvironment, start_response: StartResponse):
        """
        Forward the WSGI request to the Flask app, adjusting for reverse proxy prefixes.

        Handles the `X-Script-Name` header to ensure Flask generates correct absolute URLs
        when running behind a reverse proxy (e.g., Nginx). Adjusts `SCRIPT_NAME` and `PATH_INFO`
        in the WSGI environment to account for the proxy prefix.

        :param environ: WSGI environment dictionary.
        :type environ: WSGIEnvironment
        :param start_response: start_response() callable as defined in PEP 3333
        :type start_response: StartResponse
        :return: The response from the wrapped Flask application.
        :rtype: Iterable[bytes]
        """
        script_name = environ.get("HTTP_X_SCRIPT_NAME", "")
        if script_name:
            environ["SCRIPT_NAME"] = script_name
            path_info = environ["PATH_INFO"]
            if path_info.startswith(script_name):
                environ["PATH_INFO"] = path_info[len(script_name) :]
        return self.app(environ, start_response)
