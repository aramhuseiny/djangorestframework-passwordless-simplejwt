from django import VERSION

if VERSION < (3, 2):
    default_app_config = (
        "rest_framework_passwordless_simplejwt.token_blacklist.apps.TokenBlacklistConfig"
    )
