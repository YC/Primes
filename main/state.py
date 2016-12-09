from admin.appstate import AppState
from google.appengine.api import memcache

DEFAULT = 1
HOUR = 3600


def get_state():
    # Try to get app state from memcache
    state = memcache.get('state')
    if state:
        return state
    else:
        # Get from datastore
        state = AppState.get_by_id(DEFAULT)

        # If state is in datastore
        if state:
            # Add to memcache
            memcache.add(key="state", value=state, time=HOUR)
            return state
