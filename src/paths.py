import os

SCRIPT_PATH: str = os.path.join(os.path.dirname(os.path.abspath(__file__)))
REPO_PATH: str = os.path.join(SCRIPT_PATH, "..")
TEMPLATES_PATH: str = os.path.join(REPO_PATH, "templates")
SRC_PATH: str = os.path.join(REPO_PATH, "src")
EXAMPLE_PATH: str = os.path.join(REPO_PATH, "example")
RUN_EXAMPLE_SCRIPT_PATH: str = os.path.join(REPO_PATH, "scripts", "run_example.sh")
