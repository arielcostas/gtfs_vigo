import os
from src.constants import ETAG_FILE, LOCAL_FEED_DIR


def write_information() -> None:
    dates = get_first_last_feed_day()
    start_date = dates[0]
    end_date = dates[1]

    with open(ETAG_FILE, 'r') as f:
        version = f.read().strip().replace('"', '')

    # If the feed_info.txt already exists, raise an error because upstream might have already created it
    if os.path.exists(os.path.join(LOCAL_FEED_DIR, 'feed_info.txt')):
        raise FileExistsError("feed_info.txt already exists. Please remove it before running the pipeline again.")


    with open(os.path.join(LOCAL_FEED_DIR, 'feed_info.txt'), 'w', newline='') as f:
        f.write(f"""feed_publisher_name,feed_publisher_url,feed_lang,default_lang,feed_start_date,feed_end_date,feed_version,feed_contact_email,feed_contact_url
"Ariel Costas Guerrero",https://github.com/arielcostas/gtfs_vigo,es,es,{start_date},{end_date},{version},ariel@costas.dev,https://github.com/arielcostas/gtfs_vigo/issues
""")
        
    # If the attributions.txt already exists, raise an error because upstream might have already created it
    if os.path.exists(os.path.join(LOCAL_FEED_DIR, 'attributions.txt')):
        raise FileExistsError("attributions.txt already exists. Please remove it before running the pipeline again.")


    with open(os.path.join(LOCAL_FEED_DIR, 'attributions.txt'), 'w', newline='') as f:
        f.write(f"""attribution_id,agency_id,organization_name,is_producer,is_operator,is_authority,attribution_url,attribution_email
"vitrasa",1,"Vitrasa",1,1,0,"https://vitrasa.es","info.vigo@avanzagrupo.com"
"concello",1,"Concello de Vigo",0,0,1,"https://www.vigo.org","opendata@vigo.org"
"arielcostas",1,"Ariel Costas Guerrero",0,0,0,"https://github.com/arielcostas/gtfs_vigo","ariel@costas.dev"
""")
        

def get_first_last_feed_day() -> tuple[str, str]:
    """
    Get the first and last feed day from the feed_info.txt file.
    """
    first_date_seen = None
    last_date_seen = None

    if os.path.exists(os.path.join(LOCAL_FEED_DIR, 'calendar.txt')):
        with open(os.path.join(LOCAL_FEED_DIR, 'calendar.txt'), 'r') as f:
            rows = f.readlines()
        header = [r.strip() for r in rows[0].strip().split(',')]
        start_date_index = header.index('start_date')
        end_date_index = header.index('end_date')
        if len(rows) < 2:
            print("Warning: calendar.txt is empty or has no data rows.")
        for row in rows[1:]:
            start_date = row.strip().split(',')[start_date_index]
            end_date = row.strip().split(',')[end_date_index]
            if first_date_seen is None or start_date < first_date_seen:
                first_date_seen = start_date
            if last_date_seen is None or end_date > last_date_seen:
                last_date_seen = end_date
    
    if os.path.exists(os.path.join(LOCAL_FEED_DIR, 'calendar_dates.txt')):
        with open(os.path.join(LOCAL_FEED_DIR, 'calendar_dates.txt'), 'r') as f:
            rows = f.readlines()
        header = [r.strip() for r in rows[0].strip().split(',')]
        date_index = header.index('date')
        exception_type_index = header.index('exception_type') if 'exception_type' in header else None
        for row in rows[1:]:
            if exception_type_index is not None and row.strip().split(',')[exception_type_index] != '1':
                continue
            date = row.strip().split(',')[date_index]
            if first_date_seen is None or date < first_date_seen:
                first_date_seen = date
            if last_date_seen is None or date > last_date_seen:
                last_date_seen = date

    return (first_date_seen, last_date_seen)