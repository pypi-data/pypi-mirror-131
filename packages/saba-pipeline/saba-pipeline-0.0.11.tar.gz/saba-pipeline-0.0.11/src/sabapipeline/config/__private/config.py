from ...__private.utilities import *
from .store import DataStore, SimpleRAMDataStore


class PipelineConfig:
    def __init__(self,
                 source_triggerers_thread_count: int = 1,
                 data_store: DataStore = None
                 # ray_config=None
                 ):
        self.source_triggerers_thread_count = source_triggerers_thread_count
        self.data_store = get_not_none(data_store, SimpleRAMDataStore())
