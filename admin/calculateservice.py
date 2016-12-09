import webapp2


class CalculateService(webapp2.RequestHandler):
    """Do nothing on instance startup."""
    def get(self):
        pass

app = webapp2.WSGIApplication([('/_ah/start', CalculateService)], debug=False)
