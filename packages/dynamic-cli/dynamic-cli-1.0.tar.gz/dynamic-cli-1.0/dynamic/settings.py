import os
from pathlib import Path

NOTION_URL = "https://www.notion.so/"
LOGIN_PATH = NOTION_URL + "/login"
DATA_DIR = os.environ.get(
    "DYNAMIC_DATA_DIR", str(Path(os.path.expanduser("~")).joinpath(".dynamic"))
)
PLAYBOOK_FILE = str(Path(DATA_DIR).joinpath("playbook.json"))
TOKEN_FILE_PATH = str(Path(DATA_DIR).joinpath("tokenv2_cookie"))

try:
    os.makedirs(DATA_DIR)
except FileExistsError:
    pass

if not os.path.isfile(TOKEN_FILE_PATH):
    open(TOKEN_FILE_PATH, "w").close()
