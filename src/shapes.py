import csv

import os
from src.constants import LOCAL_FEED_DIR
import pandas as pd

def process_shapes() -> None:
    """
    Process the shapes.txt file.

    For each route, check the shape `shape_dist_traveled`, and ensure it varies for each 
    `shape_pt_sequence`, avoiding duplicate shape_dist_traveled values.
    """
    SHAPES_FILE = os.path.join(LOCAL_FEED_DIR, 'shapes.txt')
    temp_output = SHAPES_FILE + ".tmp"

    grouped_chunks = {}

    # Process in chunks
    for chunk in pd.read_csv(SHAPES_FILE, chunksize=100_000):
        # Group by shape_id in this chunk
        for shape_id, group in chunk.groupby("shape_id"):
            if shape_id not in grouped_chunks:
                grouped_chunks[shape_id] = []
            grouped_chunks[shape_id].append(group)

    # Now process each complete shape_id group
    changed_distances = 0
    with open(temp_output, 'w', newline='') as f_out:
        header_written = False
        for shape_id, group_list in grouped_chunks.items():
            df = pd.concat(group_list).sort_values("shape_pt_sequence").reset_index(drop=True)

            # Fix duplicate shape_dist_traveled values
            prev_dist = None
            for i in range(len(df)):
                dist = df.loc[i, "shape_dist_traveled"]
                if prev_dist is not None and dist <= prev_dist:
                    changed_distances += 1
                    df.loc[i, "shape_dist_traveled"] = prev_dist + 1  # Add 1 meter (or adjust as needed)
                prev_dist = df.loc[i, "shape_dist_traveled"]

            # Write to output
            df.to_csv(f_out, index=False, header=not header_written)
            header_written = True

    os.replace(temp_output, SHAPES_FILE)
    print(f"Processed shapes.txt - {changed_distances} shape_dist_traveled values adjusted to ensure uniqueness.")