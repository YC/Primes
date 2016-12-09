from google.appengine.ext import ndb


class AppState(ndb.Model):
    """Represents the status of the app."""
    prev_prime = ndb.IntegerProperty()
    current_number = ndb.IntegerProperty()
    current_prime_count = ndb.IntegerProperty()
