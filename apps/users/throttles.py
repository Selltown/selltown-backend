from ..common.throttles.base import FormattedThrottleMixin
from rest_framework.throttling import AnonRateThrottle


class RegistrationThrottle(FormattedThrottleMixin, AnonRateThrottle):
    scope = "registration"


class LoginThrottle(FormattedThrottleMixin, AnonRateThrottle):
    scope = "login"
