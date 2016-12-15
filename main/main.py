import webapp2
from appengine_config import JINJA_ENVIRONMENT
from state import get_state

DEFAULT = 1


class MainPage(webapp2.RequestHandler):
    def get(self):
        # The largest prime in the datastore
        value = 0

        # If appstat is initalised, get state and largest prime
        state = get_state()
        if state:
            value = state.current_number

        # Output page
        template = JINJA_ENVIRONMENT.get_template('main/index.html')
        self.response.write(template.render({"n": value}))

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
