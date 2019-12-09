""" Utils module """

from functools import wraps
from func_timeout import FunctionTimedOut

from starlette.responses import JSONResponse, Response
from starlette.requests import Request


def fallback(fallback_function):
    def outer_wrapper(f):

        # will preserve information about the original function.
        @wraps(f)
        def inner_wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            # TODO: Remove generic Exception type in the future :).
            except (FunctionTimedOut, Exception) as ex:
                return fallback_function()

        return inner_wrapper

    return outer_wrapper


# health checks implementation:
#   - https://inadarei.github.io/rfc-healthcheck/#rfc.section.3
#   - https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/


def check_liveness(request: Request) -> Response:
    data = {'status': 'pass', 'checks': []}
    return JSONResponse(content=data, media_type='application/health+json')


def check_readiness(request: Request) -> Response:
    data = {'status': 'pass', 'checks': []}
    return JSONResponse(content=data, media_type='application/health+json')
