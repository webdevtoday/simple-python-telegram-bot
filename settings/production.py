import logging.config
import os

import sentry_sdk


# Path to root folder `tele_bot`
BASE_PATH = os.path.dirname(os.path.dirname(__file__))

# TODO: enter the token from your bot here!!!
TG_TOKEN = ""

# We do not use a proxy URL on the server
TG_API_URL = None

# Currency pair for notification
NOTIFY_PAIR = ("BTC", "USD")
# Chat ID for notifications about BTC rates
NOTIFY_USER_ID = 0

# Chat ID for rate notifications $
USD_NOTIFY_USER_ID = 0

COIN_MARKET_CAP_API_KEY = ""

# Chat ID (channel owner) for feedback/requests
FEEDBACK_USER_ID = 0

# Logging
LOGGING = {
    'disable_existing_loggers': True,
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(module)s.%(funcName)s | %(asctime)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
logging.config.dictConfig(LOGGING)

# Sentry
# TODO: add your DSN from https://sentry.io
sentry_sdk.init(
    dsn="<DSN>",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    debug=True,
)
