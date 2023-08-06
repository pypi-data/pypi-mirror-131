from functools import partial
import sentry_sdk


class SentryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.sanitize = partial(add_to_sanitize_context, request)
        request._sanitization_context = []

        if hasattr(request, 'session') and getattr(request.session, 'session_key'):
            request.sanitize(request.session.session_key)

        if hasattr(request, 'correlation_id'):
            sentry_sdk.set_tag('correlation_id', request.correlation_id)

        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        squad = getattr(view_func, '__squad__', None)
        if squad is not None:
            sentry_sdk.set_tag('squad', squad)


def add_to_sanitize_context(request, value):
    request._sanitization_context.append(value)