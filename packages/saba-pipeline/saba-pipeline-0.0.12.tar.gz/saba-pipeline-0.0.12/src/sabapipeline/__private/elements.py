import time
from queue import Queue

from .utilities import *
from .concepts import Event, EventHandler
from ..config import DataStore


class InternalPipelineElement(ABC):
    def __init__(self):
        self.data_store: DataStore = None

    def set_data_store(self, data_store: DataStore):
        self.data_store = data_store


class EventListener(InternalPipelineElement, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def process_event(self, event: Event) -> None:
        raise NotImplementedError()


class EventGenerator(InternalPipelineElement, ABC):
    def __init__(self):
        super().__init__()
        self.event_handler: Optional[EventHandler] = None

    def process_generated_event(self, event: Event) -> None:
        if self.event_handler is None:
            raise Exception  # TODO
        else:
            self.event_handler.handle_event(event)


class EventSource(EventGenerator, ABC):
    pass


class TriggererEventSource(EventSource, ABC):
    @abstractmethod
    def start_generating(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def stop_generating(self) -> None:
        raise NotImplementedError()


class TriggerableEventSource(EventSource, ABC):
    def __init__(self):
        super().__init__()
        self.priority: int = 1

    @abstractmethod
    def get_event(self) -> Optional[Event]:
        raise NotImplementedError()

    def get_event_generator_function(self) -> Optional[Callable[[], None]]:
        event: Optional[Event] = self.get_event()
        if event is None:
            return None
        return lambda: self.process_generated_event(event)


class TriggerableEventBatchSource(TriggerableEventSource, ABC):
    def __init__(self):
        super().__init__()
        self.queue: Queue = Queue()

    @abstractmethod
    def get_event_batch(self) -> List[Event]:
        raise NotImplementedError()

    def get_event(self) -> Optional[Event]:
        if self.queue.empty():
            [self.queue.put(x) for x in self.get_event_batch()]
        if self.queue.empty():
            return None
        return self.queue.get(block=False)


class EventSink(EventListener):
    @abstractmethod
    def drown_event(self, event: Event) -> None:
        raise NotImplementedError()

    def process_event(self, event: Event) -> None:
        self.drown_event(event)


class EventAnalyzer(EventGenerator, EventListener):
    @abstractmethod
    def analyze_event(self, input_event: Event, output_event_handler: EventHandler) -> None:
        raise NotImplementedError()

    def process_event(self, event: Event) -> None:
        self.analyze_event(event, self.event_handler)
