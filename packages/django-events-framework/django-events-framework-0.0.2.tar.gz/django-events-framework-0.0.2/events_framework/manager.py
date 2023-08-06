import logging
from django.db import transaction

logger = logging.getLogger(__name__)


class EventsManager:
    def __init__(self):
        self._events_registry = {}

    def register(self, event_model, event_type, handler):
        if event_model in self._events_registry:
            logger.info("event handler allready in registry")
            return
        self._events_registry[event_model] = {
            "type": event_type,
            "handler": handler,
        }

    def process(self):
        for event_model, props in self._events_registry.items():
            events_to_process = event_model.objects.filter(
                type=props["type"],
                processed=False,
            )
            print("here?")

            for event in events_to_process:
                with transaction.atomic():
                    for e in events_to_process.filter(pk=event.pk).select_for_update(
                        skip_locked=True
                    ):
                        print(e)
                        try:
                            props["handler"](e)
                            e.processed = True
                            e.save()
                        except Exception as e:
                            print(e)
                            logger.error(str(e))


manager = EventsManager()
