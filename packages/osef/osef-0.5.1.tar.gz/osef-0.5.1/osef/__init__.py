"""Package containing all osef tools"""
import logging

from . import parser
from . import saver
from . import streamer
from . import types

logging.basicConfig(format="[%(asctime)s] %(levelname)s: %(message)s")
