from .utilities import *


class Event(ABC):
    pass


class EventHandler(ABC):
    @abstractmethod
    def handle_event(self, event_to_handle: Event):
        raise NotImplementedError()
