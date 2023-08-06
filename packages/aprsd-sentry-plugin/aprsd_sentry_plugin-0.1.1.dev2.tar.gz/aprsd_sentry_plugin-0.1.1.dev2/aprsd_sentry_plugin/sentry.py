import logging

import sentry_sdk
from aprsd import messaging, plugin, trace
from sentry_sdk.integrations.flask import FlaskIntegration

import aprsd_sentry_plugin


LOG = logging.getLogger("APRSD")


class SentryPlugin(plugin.APRSDPluginBase):

    enabled = False

    def setup(self):
        """Allows the plugin to do some 'setup' type checks in here.

        If the setup checks fail, set the self.enabled = False.  This
        will prevent the plugin from being called when packets are
        received."""
        # Do some checks here?
        self.enabled = True
        try:
            self.config.exists(["services", "sentry", "dsn"])
        except Exception as ex:
            LOG.error(f"Failed to find config services.sentry.dsn {ex}")
            self.enabled = False
            return

        dsn = self.config.get("services.sentry.dsn")
        LOG.info(f"Initializing Sentry to DSN {dsn}")

        sentry_sdk.init(
            dsn=dsn,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=1.0,
            integrations=[FlaskIntegration()],
            release=f"APRSD_SENTRY@{aprsd_sentry_plugin.__version__}",
        )

    def filter(self, packet):
        return messaging.NULL_MESSAGE

    @trace.trace
    def process(self, packet):
        pass
