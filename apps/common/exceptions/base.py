from rest_framework.views import exception_handler
from rest_framework.exceptions import Throttled


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and isinstance(exc, Throttled):
        # Keep the Retry-After header that DRF already generated,
        # but replace the detail message with our own message.
        if hasattr(exc, "custom_detail"):
            response.data["detail"] = exc.custom_detail

    return response
