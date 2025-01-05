import sys

from src.paths import SRC_PATH

def init_autogen_code_test():
    if SRC_PATH not in sys.path:
        sys.path.append(SRC_PATH)
