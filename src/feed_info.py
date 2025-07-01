import os
from src.constants import ETAG_FILE, LOCAL_FEED_DIR


def write_feed_information() -> None:
    # TODO: These should be figured out from the feed itself, reading the last calendar.txt expiration date or the last calendar_dates.txt
    #       expiration date, and the last feed_info.txt expiration date.
    #       This is a temporary solution until we have a more robust way to handle feed information
    start_date = "20250630"
    end_date = "20250707"

    # TODO: This should be something like the ETag value, or some linear versioning system
    with open(ETAG_FILE, 'r') as f:
        version = f.read().strip().replace('"', '')

    # If the feed_info.txt already exists, raise an error because upstream might have already created it
    if os.path.exists(os.path.join(LOCAL_FEED_DIR, 'feed_info.txt')):
        raise FileExistsError("feed_info.txt already exists. Please remove it before running the pipeline again.")


    with open(os.path.join(LOCAL_FEED_DIR, 'feed_info.txt'), 'w', newline='') as f:
        f.write(f"""feed_publisher_name,feed_publisher_url,feed_lang,default_lang,feed_start_date,feed_end_date,feed_version,feed_contact_email,feed_contact_url
"Ariel Costas Guerrero",https://github.com/arielcostas/gtfs_vigo,es,es,{start_date},{end_date},{version},ariel@costas.dev,https://github.com/arielcostas/gtfs_vigo/issues
""")