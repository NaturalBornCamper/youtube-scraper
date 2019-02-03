import configparser
import re
from os.path import join

config = configparser.ConfigParser()
config.read('config.ini')

print(config.get('DEFAULT', 'BOB', fallback=""))

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
YOUTUBE_API_KEY = config.get('API', 'YOUTUBE_API_KEY', fallback="")
API_DELAY_BETWEEN_REQUESTS = 2.0

# Search params
MAX_RESULTS = "5"

SCRAPING_FOLDER = join("D:", "Training", "Sentdex", "Django Web Development with Python")

AUTO_RENAMING_MIN_SCORE = 0.95
AUTO_IGNORING_MAX_SCORE = 0.60


class REGEXES:
    VIDEO_ID = re.compile(r'(.*?)\b([a-zA-Z0-9_\-]{11})?$')
    ALPHANUM_FILTER = r"[^a-zA-Z0-9]+"

