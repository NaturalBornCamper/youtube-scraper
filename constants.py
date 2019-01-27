import configparser
import re
from os.path import join

config = configparser.ConfigParser()
config.read('config.ini')

print(config.get('DEFAULT', 'BOB', fallback=""))

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
YOUTUBE_API_KEY = config.get('API', 'YOUTUBE_API_KEY', fallback="")
API_DELAY_BETWEEN_REQUESTS = 0.5

# Search params
MAX_RESULTS = "10"

SCRAPING_FOLDER = join("D:", "Training", "Sentdex", "Python 3 Basics Tutorial Series")

AUTO_RENAMING_MIN_SCORE = 0.95
AUTO_IGNORING_MAX_SCORE = 0.60


class REGEXES:
    VIDEO_ID = re.compile(r'(.*?)\b([a-zA-Z0-9_\-]{11})?$')
    ALPHANUM_FILTER = r"[^a-zA-Z0-9]+"


class COLORS:
    RESET = "\u001b[0m"
    UNDERLINE_WHITE = "\u001b[37;4m"
    BLACK = "\u001b[30m"
    RED = "\u001b[31m"
    GREEN = "\u001b[32m"
    YELLOW = "\u001b[33m"
    BLUE = "\u001b[34m"
    MAGENTA = "\u001b[35m"
    CYAN = "\u001b[36m"
    WHITE = "\u001b[37m"
    BRIGHT_BLACK = "\u001b[30;1m"
    BRIGHT_RED = "\u001b[31;1m"
    BRIGHT_GREEN = "\u001b[32;1m"
    BRIGHT_YELLOW = "\u001b[33;1m"
    BRIGHT_BLUE = "\u001b[34;1m"
    BRIGHT_MAGENTA = "\u001b[35;1m"
    BRIGHT_CYAN = "\u001b[36;1m"
    BRIGHT_WHITE = "\u001b[37;1m"
