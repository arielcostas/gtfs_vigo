import os


ROOT_DIR = os.path.abspath(os.path.join(__file__, '..', '..'))
LOCAL_FEED_DIR = os.path.join(ROOT_DIR, 'feed')
ETAG_FILE = os.path.join(ROOT_DIR, 'feed_last_etag.txt')
REMOTE_FEED_URL = "https://datos.vigo.org/data/transporte/gtfs_vigo.zip"