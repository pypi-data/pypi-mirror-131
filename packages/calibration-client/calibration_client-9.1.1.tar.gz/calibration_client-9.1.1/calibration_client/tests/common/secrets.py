"""Test Configuration variables"""

###############################################################################
#
# Configuration to be used when running tests against a local server
#
# Local setup:
# rails s puma -b 'ssl://0.0.0.0:8443?cert=/Users/maial/development/gitlab/ITDM/calibration_catalog/config/certs/localhost.crt&key=/Users/maial/development/gitlab/ITDM/calibration_catalog/config/certs/localhost.key&verify_mode=none&no_tlsv1=false'  # noqa
###############################################################################
# __OAUTH_TOKEN_URL = 'https://127.0.0.1:8443/dev_calibration/oauth/token'
# __OAUTH_AUTHORIZE_URL = 'https://127.0.0.1:8443/dev_calibration/oauth/authorize'  # noqa
#
# __CLIENT_ID = 'PUT_HERE_YOUR_DEV_CLIENT_KEY'  # noqa
# __CLIENT_SECRET = 'PUT_HERE_YOUR_DEV_SECRET_KEY'  # noqa
# __USER_EMAIL = 'luis.maia@xfel.eu'
#
# # OAUTH2 constants
# CLIENT_OAUTH2_INFO = {
#     'EMAIL': __USER_EMAIL,
#     'CLIENT_ID': __CLIENT_ID,
#     'CLIENT_SECRET': __CLIENT_SECRET,
#     #
#     'AUTH_URL': __OAUTH_AUTHORIZE_URL,
#     'TOKEN_URL': __OAUTH_TOKEN_URL,
#     'REFRESH_URL': __OAUTH_TOKEN_URL,
#     'SCOPE': '',
# }
#
# USER_INFO = {
#     'EMAIL': __USER_EMAIL,
#     'FIRST_NAME': 'Luis',
#     'LAST_NAME': 'Maia',
#     'NAME': 'Luis Maia',
#     'NICKNAME': 'maial',
#     'PROVIDER': 'ldap',
#     'UID': 'maial'
# }
#
# BASE_API_URL = 'https://127.0.0.1:8443/dev_calibration/api/'

###############################################################################
#
# Configuration to be used when running tests against the official TEST server
#
# Remote setup:
# https://in.xfel.eu/dev_calibration
###############################################################################
__OAUTH_TOKEN_URL = 'https://in.xfel.eu/test_calibration/oauth/token'
__OAUTH_AUTHORIZE_URL = 'https://in.xfel.eu/test_calibration/oauth/authorize'

__CLIENT_ID = 'PUT_HERE_YOUR_CLIENT_KEY'  # noqa
__CLIENT_SECRET = 'PUT_HERE_YOUR_SECRET_KEY'  # noqa
__USER_EMAIL = 'luis.maia@xfel.eu'

# OAUTH2 constants
CLIENT_OAUTH2_INFO = {
    'EMAIL': __USER_EMAIL,
    'CLIENT_ID': __CLIENT_ID,
    'CLIENT_SECRET': __CLIENT_SECRET,
    #
    'AUTH_URL': __OAUTH_AUTHORIZE_URL,
    'TOKEN_URL': __OAUTH_TOKEN_URL,
    'REFRESH_URL': __OAUTH_TOKEN_URL,
    'SCOPE': '',
}

USER_INFO = {
    'EMAIL': __USER_EMAIL,
    'FIRST_NAME': 'Luis',
    'LAST_NAME': 'Maia',
    'NAME': 'Luis Maia',
    'NICKNAME': 'maial',
    'PROVIDER': 'ldap',
    'UID': 'maial'
}

BASE_API_URL = 'https://in.xfel.eu/test_calibration/api/'
