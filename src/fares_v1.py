import os
from src.constants import LOCAL_FEED_DIR


def write_fares_v1() -> None:
    # If the fare_attributes.txt already exists, raise an error because upstream might have already created it
    if os.path.exists(os.path.join(LOCAL_FEED_DIR, 'fare_attributes.txt')):
        raise FileExistsError("fare_attributes.txt already exists. Please remove it before running the pipeline again.")

    with open(os.path.join(LOCAL_FEED_DIR, 'fare_attributes.txt'), 'w', newline='') as f:
        f.write(f"""fare_id,price,currency_type,payment_method,transfers,agency_id,transfer_duration
efectivo,1.63,EUR,0,0,1,0
passvigo_general,0.67,EUR,1,2,,2700""")
    
    # If the fare_rules.txt already exists, raise an error because upstream might have already created it
    if os.path.exists(os.path.join(LOCAL_FEED_DIR, 'fare_rules.txt')):
        raise FileExistsError("fare_rules.txt already exists. Please remove it before running the pipeline again.")
    
    # Extract all route IDs from routes.txt and for each, write the efectivo and passvigo_general fare rules
    with open(os.path.join(LOCAL_FEED_DIR, 'routes.txt'), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if not lines:
            raise ValueError("routes.txt is empty. Cannot extract route IDs.")
        header = lines[0].strip().split(',')
        route_id_index = header.index('route_id')

        all_route_ids = [line.split(',')[route_id_index] for line in lines[1:]]

    with open(os.path.join(LOCAL_FEED_DIR, 'fare_rules.txt'), 'w', newline='') as f:
        f.write(f"fare_id,route_id{os.linesep}")
        for route_id in all_route_ids:
            f.write(f"efectivo,{route_id}{os.linesep}")
            f.write(f"passvigo_general,{route_id}{os.linesep}")