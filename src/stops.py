

import csv
import os

from src.constants import LOCAL_FEED_DIR


def process_stops() -> None:
    """
    Process the stops.txt file to do the following:
    - Remove any non-numeric characters from the stop_code field
    - Add a stop_url field with a URL to the stop's page on the infobus system (http://infobus.vitrasa.es:8002/Default.aspx?parada=<id>)
    """
    STOPS_FILE = os.path.join(LOCAL_FEED_DIR, 'stops.txt')
    with open(STOPS_FILE, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=',')
        header = next(csv_reader)
        stops = [row for row in csv_reader]
        
        stop_code_index = header.index('stop_code')
        stop_url_index = header.index('stop_url') if 'stop_url' in header else None

        if stop_code_index is None:
            raise ValueError("The 'stop_code' column is missing from the stops.txt file.")
        if stop_url_index is None:
            header.append('stop_url')
            stop_url_index = len(header) - 1

    for stop in stops:
        stop_code = stop[stop_code_index]
        stop_code = ''.join(filter(str.isdigit, stop_code))
        stop_code = int(stop_code) if stop_code else 0
        stop_url = f"http://infobus.vitrasa.es:8002/Default.aspx?parada={stop_code}"
        if stop_url_index is not None:
            stop[stop_url_index] = stop_url
        else:
            stop.append(stop_url)

    with open(STOPS_FILE, 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(header)
        for stop in stops:
            csv_writer.writerow(stop)