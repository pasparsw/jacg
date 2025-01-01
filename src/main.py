import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging

from src.jacg import Jacg

LOGGER = logging.getLogger("GeneratorMain")


if __name__ == '__main__':
    jacg: Jacg = Jacg()

    jacg.run()
