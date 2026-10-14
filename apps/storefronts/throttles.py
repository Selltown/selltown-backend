from ..common.throttles.base import FormattedThrottleMixin
from rest_framework.throttling import UserRateThrottle


class CreateStorefrontThrottle(FormattedThrottleMixin, UserRateThrottle):
    scope = "create_storefront"
