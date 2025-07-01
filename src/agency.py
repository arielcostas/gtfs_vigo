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
        email_index = header.index('agency_email') if 'agency_email' in header else None

        if fare_url_index is None:
            header.append('agency_fare_url')
            fare_url_index = header.index('agency_fare_url')
        if phone_index is None:
            header.append('agency_phone')
            phone_index = header.index('agency_phone')
        if email_index is None:
            header.append('agency_email')
            email_index = header.index('agency_email')

    for agency in agencies:
        # If any field was added, we must make the array the same length as the header
        while len(agency) < len(header):
            agency.append('')
        agency[fare_url_index] = "https://vitrasa.es/tarifas-y-titulos"
        agency[phone_index] = "+34986207474"
        agency[email_index] = "info.vigo@avanzagrupo.com"

    with open(AGENCY_FILE, 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(header)
        for agency in agencies:
            csv_writer.writerow(agency)