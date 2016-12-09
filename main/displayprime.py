import webapp2
from prime import Prime
from google.appengine.ext import ndb
from state import get_state
from appengine_config import JINJA_ENVIRONMENT


class Page(webapp2.RequestHandler):
    """Handles queries for numbers."""
    def post(self):
        """Handle requests from the home page."""
        # Get input
        number = self.request.get("number")

        # Ensure that input is numeric
        if number.isdigit() and number is not None:
            self.get(number)
        else:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write("The input is not a valid number")

    def get(self, inputnum=None):
        """Output information on given number."""
        def output_message(message):
            """Output message to page."""
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write(message)

        # Invalid get request
        if inputnum is None:
            self.response.set_status(500)
            return

        # Validate input
        if len(inputnum) > 18:
            output_message("Number is too large")
            return

        # Parse Number
        number = int(inputnum)

        # 0
        if number == 0:
            output_message("0 is not prime")
            return

        # Check to see if number has been processed
        state = get_state()
        if state:
            if (number > state.prev_prime):
                output_message("Number has not been processed yet")
                return
        else:
            output_message("App has not been initalised")
            return

        # Perform query (for the first prime which is >= to given number)
        query = Prime.query().filter(Prime.key >= ndb.Key('Prime', number))
        qo = ndb.QueryOptions(limit=1)
        result_list = query.fetch(options=qo)

        # If query is successful
        if result_list:
            # Get result and build output
            result = result_list[0]
            template_dictionary = {}

            # Add number to dictionary
            template_dictionary["n"] = number

            # If the number is prime
            if result.key.id() == number:
                template_dictionary["isPrime"] = True
                template_dictionary["dateAdded"] = result.date_added
                template_dictionary["prevPrime"] = result.prev_prime
                template_dictionary["nextPrime"] = result.next_prime
                template_dictionary["numPrimes"] = result.number_of_primes
            # If not, use the next prime to output limited information
            else:
                template_dictionary["isPrime"] = False
                template_dictionary["prevPrime"] = result.prev_prime
                template_dictionary["nextPrime"] = result.key.id()
                template_dictionary["numPrimes"] = result.number_of_primes - 1

            # Output to page
            template = JINJA_ENVIRONMENT.get_template('main/view.html')
            self.response.write(template.render(template_dictionary))
        else:
            output_message("Number has not been processed yet")
            return

app = webapp2.WSGIApplication([('/(\d+?)', Page), ('/view', Page)], debug=True)
