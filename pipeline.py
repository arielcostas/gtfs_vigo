import argparse
from src import agency, shapes, stops
from src.download import maybe_download_feed
from src.feed_info import write_feed_information
import os

if __name__ != "__main__":
    raise ImportError("This script is not meant to be imported. Run it as a standalone script.")

parser = argparse.ArgumentParser(
    description="Vigo GTFS pipeline script to download, process and prepare the GTFS feed for use."
)
parser.add_argument(
    "--force-download",
    action="store_true",
    help="Force download the GTFS feed even if it is already up to date.",
)

args = parser.parse_args()

feed_downloaded = maybe_download_feed(args.force_download)
if feed_downloaded == False:
    print("New feed not downloaded. See you next time!")
    os._exit(0)

print("Feed downloaded successfully. Processing...")

write_feed_information()
print("Wrote feed_info.txt")

stops.process_stops()
print("Removed stop code letters from stops.txt")

agency.process_agency()
print("Added fare_url and phone to agency.txt")

shapes.process_shapes()
print("Added shape_id and shape_name to shapes.txt")