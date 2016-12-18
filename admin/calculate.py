from appstate import AppState
from main.prime import Prime
import time
from math import sqrt, floor, ceil
import logging
from google.appengine.ext import ndb
from google.appengine.api import memcache


STARTING_PRIME = 2
DEFAULT = 1


class CalculatePrime():
    """Class for determining primality and storing the calculated results."""
    def calculate(self, quantity):
        """Calculate and store a certain amount of primes."""
        # Start timer
        start = time.clock()

        # Do not cache numbers
        context = ndb.get_context()
        context.set_cache_policy(lambda key: key.kind() != 'Prime')

        # Get application state
        state = self.__get_state()

        # Get range
        current = state.current_number + 1
        new = current + quantity - 1

        # Get bound for sieve divisors
        bound = int(floor(sqrt(new)))

        # If necessary, compute primes which are less or equal to bound
        if bound > state.current_number:
            self.calculate(bound - current + 1)
            state = self.__get_state()
            current = state.current_number + 1

        # Perform sieve (using prime numbers less than or equal to bound)
        d = {}
        query = Prime.query().filter(Prime.key <= ndb.Key('Prime', bound))
        qo = ndb.QueryOptions(keys_only=True)
        for key in query.iter(options=qo, keys_only=True):
            # Get value of prime
            prime = key.id()

            # Store multiples of prime numbers in dictionary
            for i in range(current // prime, int(ceil(new / prime)) + 1):
                if i == 1:
                    continue

                product = i * prime
                if product not in d:
                    d[product] = prime

        # Add results to database
        prev_prime = state.prev_prime
        prev_prime_entity = None
        number_of_primes = state.current_prime_count
        for num in range(current, new + 1):
            # If number is prime
            if num not in d:
                # Increment count
                number_of_primes += 1

                # Init entity
                n = Prime(id=num, prev_prime=prev_prime, next_prime=None,
                          number_of_primes=number_of_primes)

                # Add to database
                if prev_prime_entity:
                    prev_prime_entity.next_prime = num
                    prev_prime_entity.put()
                    prev_prime_entity = None

                # update_next_prime is more expensive (more writes) because
                # it performs updates, so it should only be used for the
                # first prime of a task
                if prev_prime < current:
                    self.__update_next_prime(prev_prime, num)

                # Update latest (found) prime variable
                prev_prime = num
                prev_prime_entity = n

        # Add last prime of task to datastore
        if prev_prime_entity:
            prev_prime_entity.put()

        # Update and Store State in datastore and memcache
        state.current_prime_count = number_of_primes
        state.current_number = new
        state.prev_prime = prev_prime
        state.put()
        memcache.set(key="state", value=state, time=3600)

        # Log Success
        logging.info('Calculation for range %d-%d finished in %fs' % (current,
                     new, (time.clock() - start)))

    def __update_next_prime(self, prev, next_prime):
        """Update the next prime field for a given number."""
        n = Prime.get_by_id(prev)
        n.next_prime = next_prime
        n.put()

    def __get_state(self):
        """Gets and returns the application state."""
        # Attempt to get state of app from datastore
        state = AppState.get_by_id(DEFAULT)

        # If app has been initalised
        if state is not None:
            return state

        # Store 2 (first prime)
        Prime(id=STARTING_PRIME, prev_prime=None, next_prime=None,
              number_of_primes=1).put()

        # Return created state entity
        return AppState(current_number=STARTING_PRIME,
                        current_prime_count=1,
                        prev_prime=2,
                        id=DEFAULT)
