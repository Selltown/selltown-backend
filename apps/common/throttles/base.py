from rest_framework.exceptions import Throttled
from ...utils import format_wait_time


class FormattedThrottleMixin:
    def throttle_failure(self):
        wait = self.wait()

        if wait is not None:
            message = (
                "Too many requests. " f"Please try again in {format_wait_time(wait)}."
            )
        else:
            message = "Too many requests. Please try again later."

        exception = Throttled(
            wait=wait,
            detail=message,
        )

        # Store our message separately so the custom exception
        # handler can use it.
        exception.custom_detail = message

        raise exception
