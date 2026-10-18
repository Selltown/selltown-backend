from ..common.throttles.base import FormattedThrottleMixin
from rest_framework.throttling import UserRateThrottle


class CreateItemThrottle(FormattedThrottleMixin, UserRateThrottle):
    scope = "create_item"
