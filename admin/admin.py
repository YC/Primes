from google.appengine.api import taskqueue
import webapp2
from calculate import CalculatePrime
from main.state import get_state
from appengine_config import JINJA_ENVIRONMENT
from math import floor


class AddTask(webapp2.RequestHandler):
    """Add a calculation task to the queue."""
    def __writeline(self, header, message):
        self.response.write(header + str(message) + "\n")

    def post(self):
        # Create Task
        quantity = self.request.get("quantity")
        task = taskqueue.add(url='/admin/calculate',
                             queue_name='compute-primes',
                             params={'quantity': quantity})

        # Output task properties
        self.response.headers['Content-Type'] = 'text/plain'
        self.__writeline("Task name: ", task.name)
        self.__writeline("Task eta:  ", task.eta)
        self.__writeline("Task size: ", task.size)
        self.__writeline("Task url:  ", task.url)


class HandleTask(webapp2.RequestHandler):
    """Handle the added calculation tasks."""
    def post(self):
        # Launch task
        quantity = int(self.request.get('quantity'))
        CalculatePrime().calculate(quantity)


class RenderAdmin(webapp2.RequestHandler):
    """Render admin page from template."""
    def get(self):
        # Get app state
        state = get_state()

        # Round up to nearest hundred thousand
        value = 0
        if state:
            value = int((floor(state.current_number / 100000) + 1) * 100000)

        # Output to page
        template = JINJA_ENVIRONMENT.get_template('admin/admin.html')
        self.response.write(template.render({"val": value}))


class RenderConfirm(webapp2.RequestHandler):
    """Render confirm page."""
    def post(self):
        # Get number
        number = int(self.request.get("number"))

        # Get app state
        state = get_state()

        # Determine calculation quantity
        quantity = number
        if state:
            quantity = number - state.current_number

        # Validate quantity
        if quantity <= 0:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write("Number is not valid")
            return
        if quantity > 200000:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write("Number is too large")
            return

        # Output confirmation
        template = JINJA_ENVIRONMENT.get_template('admin/confirm.html')
        self.response.write(template.render({"quantity": quantity}))

app = webapp2.WSGIApplication([
    ('/admin/queuecalculation', AddTask),
    ('/admin/calculate', HandleTask),
    ('/admin/?', RenderAdmin),
    ('/admin/verifycalculation', RenderConfirm)
    ], debug=True)
