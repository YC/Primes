from google.appengine.api import taskqueue
import webapp2
from calculate import CalculatePrime


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

# Add and handle tasks
app = webapp2.WSGIApplication([
    ('/admin/queuecalculation', AddTask),
    ('/admin/calculate', HandleTask)
    ], debug=True)
