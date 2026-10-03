from ..common.throttles.base import FormattedThrottleMixin
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class RegistrationThrottle(FormattedThrottleMixin, AnonRateThrottle):
    scope = "registration"


class LoginThrottle(FormattedThrottleMixin, AnonRateThrottle):
    scope = "login"


class OTPThrottle(FormattedThrottleMixin, AnonRateThrottle):
    scope = "otp"


class LogoutThrottle(FormattedThrottleMixin, UserRateThrottle):
    scope = "logout"


class PasswordResetRequestThrottle(FormattedThrottleMixin, AnonRateThrottle):
    scope = "password_reset_request"


class PasswordResetVerifyThrottle(FormattedThrottleMixin, AnonRateThrottle):
    scope = "password_reset_verify"
