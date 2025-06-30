# From the script path, ./feed
import tempfile
import requests
import os
import shutil

from src.constants import ETAG_FILE, LOCAL_FEED_DIR, REMOTE_FEED_URL


def check_new_available() -> bool:
    """Check if there is a new feed available."""
    headers = {}
    if os.path.exists(ETAG_FILE):
        with open(ETAG_FILE, 'r') as f:
            etag = f.read().strip()
            headers['If-None-Match'] = etag

    response = requests.head(REMOTE_FEED_URL, headers=headers)
    if response.status_code == 200:
        return True
    elif response.status_code == 304:
        return False
    else:
        raise Exception(f"Unexpected status code: {response.status_code}")


def download_feed() -> None:
    response = requests.get(REMOTE_FEED_URL)
    if response.status_code == 200:
        with open(ETAG_FILE, 'w') as f:
            f.write(response.headers.get('ETag', ''))
        
        temporary_workdir = tempfile.mkdtemp()
        with open(temporary_workdir + '/gtfs_vigo.zip', 'wb') as f:
            f.write(response.content)
        import zipfile
        with zipfile.ZipFile(temporary_workdir + '/gtfs_vigo.zip', 'r') as zip_ref:
            zip_ref.extractall(LOCAL_FEED_DIR)
        print("Feed downloaded and extracted successfully.")
    else:
        raise Exception(f"Unexpected status code: {response.status_code}")


def maybe_download_feed(force: bool) -> bool:
    """
    Check if a new feed is available and download it if so.
    Returns True if a new feed was downloaded, False otherwise.
    """
    if check_new_available() or force:
        shutil.rmtree(LOCAL_FEED_DIR) if os.path.exists(LOCAL_FEED_DIR) else None
        os.makedirs(LOCAL_FEED_DIR, exist_ok=True)
        download_feed()
        return True
    return False
