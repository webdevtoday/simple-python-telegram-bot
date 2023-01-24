import logging

import sentry_sdk

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

sentry_sdk.init(
    dsn="<DSN>",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    debug=True,
)

try:
    # division_by_zero = 1 / 0
    raise Exception('xxx')
except Exception as e:
    sentry_sdk.capture_exception(error=e)
    raise
