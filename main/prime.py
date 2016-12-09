from google.appengine.ext import ndb


class Prime(ndb.Model):
    """Represents a number."""
    prev_prime = ndb.IntegerProperty('p', indexed=False)
    next_prime = ndb.IntegerProperty('n')
    date_added = ndb.DateTimeProperty('d', auto_now_add=True, indexed=False)
    number_of_primes = ndb.IntegerProperty('c')
