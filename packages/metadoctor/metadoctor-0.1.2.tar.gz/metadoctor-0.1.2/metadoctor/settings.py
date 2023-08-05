__all__ = ['config', 'WORKING_DIRECTORY', 'CID10_FILE']

import os
from starlette.config import Config

WORKING_DIRECTORY = os.getcwd()
ENV_FILE = os.path.abspath('.env')
CID10_FILE = os.path.abspath('cid10.csv')

config = Config(env_file=ENV_FILE)
