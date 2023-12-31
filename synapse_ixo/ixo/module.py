import logging
from typing import Literal, Union
import synapse as synapse
import synapse.module_api as module_api
import synapse.api.errors as errors
import synapse.events as events

logger = logging.getLogger("synapse.contrib." + __name__)


# New module API
class Module:
    """
    Main entry point. Implements the Synapse Module API.
    """

    def __init__(self, config: dict, api: module_api.ModuleApi):
        self.api = api
        self.block_events = config.get("block_events") or []
        self.api.register_spam_checker_callbacks(
            check_event_for_spam=self.check_event_for_spam,
        )

    # Callbacks for `register_spam_checker_callbacks`
    async def check_event_for_spam(
        self, event: "events.EventBase"
    ) -> Union[Literal["NOT_SPAM"], errors.Codes]:
        logger.info("check_event_for_spam!!!!!!!!!!!!!!!!!")
        if event.type in self.block_events:
            logger.info("block !!!!!!!!!!!!!!!!!")
            return errors.Codes.FORBIDDEN
        else:
            logger.info("no block !!!!!!!!!!!!!!!!!")
            return module_api.NOT_SPAM
