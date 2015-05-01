"""
This script runs the sdk application using a development server.
"""

from os import environ
from sdk import app

import sdk.views, sdk.utils, sdk.biodb, sdk.user, sdk.config


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
