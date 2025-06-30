import csv
import os

from src.constants import LOCAL_FEED_DIR


def process_agency() -> None:
    """
    Process the agency.txt file to do the following:
    """
    AGENCY_FILE = os.path.join(LOCAL_FEED_DIR, 'agency.txt')

    with open(AGENCY_FILE, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=',')
        header = next(csv_reader)
        agencies = [row for row in csv_reader]

        fare_url_index = header.index('agency_fare_url') if 'agency_fare_url' in header else None
        phone_index = header.index('agency_phone') if 'agency_phone' in header else None

        if fare_url_index is None:
            header.append('agency_fare_url')
            fare_url_index = header.index('agency_fare_url')
        if phone_index is None:
            header.append('agency_phone')
            phone_index = header.index('agency_phone')

    for agency in agencies:
        agency[fare_url_index] = "https://vitrasa.es/tarifas-y-titulos"
        agency[phone_index] = "+34986207474"

    with open(AGENCY_FILE, 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(header)
        for agency in agencies:
            csv_writer.writerow(agency)