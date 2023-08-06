from collections import deque
from multiprocessing.pool import ThreadPool
from time import sleep

from ..config import PipelineConfig
from .bus import *
from .elements import *


class Pipeline:
    def __init__(self,
                 sources: List[EventSource] = None,
                 sinks: Dict[EventSink, List[Type]] = None,
                 analyzers: Dict[EventAnalyzer, List[Type]] = None,
                 other_generators: List[EventGenerator] = None,
                 other_listeners: Dict[EventListener, List[Type]] = None,
                 config: PipelineConfig = None
                 ):
        sources = get_not_none(sources, [])
        sinks = get_not_none(sinks, {})
        analyzers = get_not_none(analyzers, {})
        other_generators = get_not_none(other_generators, [])
        other_listeners = get_not_none(other_listeners, {})

        self.event_listeners: Dict[EventListener, List[Type]] = {**other_listeners, **sinks, **analyzers}
        self.event_generators: List[EventGenerator] = other_generators + sources + list(analyzers.keys())

        self.bus: EventBus = EventBus()
        for generator in self.event_generators:
            generator.event_handler = self.bus
        for listener in self.event_listeners:
            for t in self.event_listeners[listener]:
                self.bus.add_listener(listener, t)

        self.config: PipelineConfig = get_not_none(config, PipelineConfig())

        all_pipeline_elements: Set[InternalPipelineElement] = set(self.event_generators).union(self.event_listeners.keys())
        for element in all_pipeline_elements:
            element.set_data_store(self.config.data_store)

        # self.use_ray = (ray_config is not None)
        # self.ray_config = ray_config
        # if self.use_ray:
        #     # ray.init(address='ray://192.168.242.92:31001')  # server
        #     ray.init(address='ray://192.168.243.216:10001')  # banaei

    def start(self):
        # if self.use_ray:
        #     ray.get(start_pipeline_module_with_ray.remote(self))
        # else:
        #     self.start_directly()
        self.__start_event_sources()

    def stop(self):
        self.__stop_event_sources()

    def __start_event_sources(self):
        self.__start_triggerer_sources()
        self.__start_triggering_triggerable_sources()

    def __stop_event_sources(self):
        self.__stop_triggerer_sources()

    def __start_triggerer_sources(self):
        for generator in self.event_generators:
            if isinstance(generator, TriggererEventSource):
                generator.start_generating()

    def __stop_triggerer_sources(self):
        for generator in self.event_generators:
            if isinstance(generator, TriggererEventSource):
                generator.stop_generating()

    def __start_triggering_triggerable_sources(self):
        triggerable_sources = \
            [generator for generator in self.event_generators if isinstance(generator, TriggerableEventSource)]
        priorities = list(set(map(lambda x: x.priority, triggerable_sources)))
        priorities.sort()
        prioritised_sources = [deque([source for source in triggerable_sources if source.priority == priority])
                               for priority in priorities]
        self.triggering_triggerable_sources = True
        max_queue_size = 2 * self.config.source_triggerers_thread_count
        with ThreadPool(processes=self.config.source_triggerers_thread_count) as p:
            while self.triggering_triggerable_sources:
                # noinspection PyProtectedMember
                while p._inqueue.qsize() > max_queue_size:
                    sleep(0.001)
                event_generator_function: Optional[Callable[[], None]] = None
                for priority_sources in prioritised_sources:
                    for i in range(len(priority_sources)):
                        event_generator_function = priority_sources[i].get_event_generator_function()
                        if event_generator_function is not None:
                            priority_sources.rotate(-i - 1)
                            break
                    if event_generator_function is not None:
                        break
                if event_generator_function is not None:
                    p.apply_async(event_generator_function)

    def __stop_triggering_triggerable_sources(self):
        self.triggering_triggerable_sources = False

# @ray.remote
# def start_pipeline_module_with_ray(pipeline_module: Pipeline):
#     pipeline_module.start_directly()
