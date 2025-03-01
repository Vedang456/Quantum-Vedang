# test_config.py
from api.Config import Config

config = Config()
print(config['INPUT_SHAPE'])
print(config.to_dict())