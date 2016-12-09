# Code samples from:
# https://cloud.google.com/appengine/docs/python/tools/appstats
# https://cloud.google.com/appengine/docs/python/getting-started/generating-dynamic-content-templates
# Licensed under Apache 2.0

import jinja2
import os

# Jinja
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# Appstats
appstats_CALC_RPC_COSTS = True


def webapp_add_wsgi_middleware(app):
    from google.appengine.ext.appstats import recording
    app = recording.appstats_wsgi_middleware(app)
    return app
