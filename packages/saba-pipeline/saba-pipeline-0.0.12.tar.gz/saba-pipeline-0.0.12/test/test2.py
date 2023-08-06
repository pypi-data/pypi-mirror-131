from src.sabapipeline.config import DataStore, SimpleRAMDataStore

data_store: DataStore = SimpleRAMDataStore()
my_data_store: DataStore = data_store.get_branch("ali:", value_generator=lambda x: f'value for {x}')
print(my_data_store["saeed"])
print(my_data_store["asghar"])
print(my_data_store["ahmad"])
b = 2

