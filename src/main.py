import sys
from pathlib import Path as FilePath
print()
print(sys.executable)
import pandas as pd
import numpy as np
from graph import Graph,Path
from data.load_data import build_graph


DATA_DIR = FilePath(__file__).resolve().parent.parent / 'data'


def main():
    parking_permit_blocks_path = DATA_DIR / 'residential_parking_permit_blocks.csv'
    nodes_path = DATA_DIR / 'Street_Nodes.csv'
    street_centerlines_path = DATA_DIR / 'Street_Centerline.csv'
    streets_path = DATA_DIR / 'CompleteStreets.csv'
    meters_path = DATA_DIR / 'parking_meter_and_kiosk_inventory.csv'

    philly_streets = build_graph(streets_path = streets_path,
                streets_centerline_path = street_centerlines_path,
                nodes_path = nodes_path,
                parking_permit_blocks_path = parking_permit_blocks_path,
                meters_path = meters_path)

    

    print(philly_streets.block_index)
    x = philly_streets.show_node_adjacency(3)
    print(x.head())
    path = philly_streets.bfs_search(x.to_node_obj[0])
    print(philly_streets.query_streets('arch st'
                                        #,exact=False
                                       )[1]
                                       )
    
            

if __name__ == '__main__':
    main()
