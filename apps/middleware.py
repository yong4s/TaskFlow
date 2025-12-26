import logging
from http import HTTPStatus

from django.http import HttpResponse, JsonResponse

from apps.utils.exceptions import BusinessRuleError, PermissionDeniedError, ValidationError

logger = logging.getLogger(__name__)


class ExceptionHandlerMiddleware:
    """
    Centralized exception handling middleware.

    Handles domain exceptions and converts them to appropriate HTTP responses.
    Views should not handle these exceptions - let them bubble up here.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (HTTPStatus.OK <= response.status_code < HTTPStatus.MULTIPLE_CHOICES
            and request.method in ['POST', 'PUT', 'PATCH', 'DELETE']):
            logger.info('%s %s -> %s', request.method, request.path, response.status_code)

        return response

    def process_exception(self, request, exception):
        """Handle domain exceptions and convert to appropriate HTTP responses."""

        if isinstance(exception, ValidationError):
            logger.warning('ValidationError from user %s: %s', request.user, exception)

            if request.headers.get('HX-Request'):
                return HttpResponse(status=HTTPStatus.BAD_REQUEST)

            return JsonResponse({'error': 'validation_error', 'message': str(exception)}, status=HTTPStatus.BAD_REQUEST)
        if isinstance(exception, PermissionDeniedError):
            logger.warning('Access denied for user %s: %s', request.user, request.path)

            if request.headers.get('HX-Request'):
                return HttpResponse(status=HTTPStatus.FORBIDDEN)

            return JsonResponse({'error': 'permission_denied', 'message': str(exception)}, status=HTTPStatus.FORBIDDEN)
        if isinstance(exception, BusinessRuleError):
            logger.warning('Business rule violation by user %s: %s', request.user, exception)

            if request.headers.get('HX-Request'):
                return HttpResponse(status=HTTPStatus.UNPROCESSABLE_ENTITY)

            return JsonResponse(
                {'error': 'business_rule_error', 'message': str(exception)},
                status=HTTPStatus.UNPROCESSABLE_ENTITY,
            )

        return None


class HTTPMethodOverrideMiddleware:
    """
    Middleware to support HTTP method override for HTMX requests.
    Allows PATCH and DELETE methods via POST with X-HTTP-Method-Override header.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            method = request.META.get('HTTP_X_HTTP_METHOD_OVERRIDE', '').upper()
            if method in ['PUT', 'PATCH', 'DELETE']:
                request.method = method

        return self.get_response(request)
