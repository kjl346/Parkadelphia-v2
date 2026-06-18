import sys
from pathlib import Path as FilePath
print()
print(sys.executable)
import pandas as pd
import numpy as np
from graph import Graph,Path


DATA_DIR = FilePath(__file__).resolve().parent.parent / 'data'


def main():
    parking_permit_blocks = pd.read_csv(DATA_DIR / 'residential_parking_permit_blocks.csv')
    street_nodes = pd.read_csv(DATA_DIR / 'Street_Nodes.csv')
    street_centerlines = pd.read_csv(DATA_DIR / 'Street_Centerline.csv')
    complete_streets = pd.read_csv(DATA_DIR / 'CompleteStreets.csv')
    full_ds = pd.merge(street_centerlines,street_nodes[['X','Y','intersecti','node_id']],left_on=['fnode_'],right_on='node_id',validate='many_to_one',how='left',suffixes=('','_from')).rename({'X':'X_from','Y':'Y_from','intersecti':'intersecti_from'},axis=1)
    full_ds  = pd.merge(full_ds,street_nodes[['X','Y','intersecti','node_id']],left_on=['tnode_'],right_on='node_id',validate='many_to_one',how='left',suffixes=('','_to')).rename({'X':'X_to','Y':'Y_to','intersecti':'intersecti_to'},axis=1)
    dx = full_ds['X_to'] - full_ds['X_from']
    dy = full_ds['Y_to'] - full_ds['Y_from']
    full_ds['bearing'] = np.degrees(np.arctan2(dy,dx))
    philly_streets = Graph()
    for ind, data in full_ds[(full_ds.oneway.str.strip() != '')].iterrows():
        fnode = data.fnode_
        tnode = data.tnode_
        length = data.length
        stname = data.stname
        oneway = data.oneway
        from_intersection = data.intersecti_from
        to_intesection = data.intersecti_to
        bearing = data.bearing
        opposite = (bearing + 180) % 360
        if opposite > 180:
            opposite -= 360
        if oneway == 'B':
            philly_streets.add_edge(from_node_id=fnode,
                                    to_node_id=tnode,
                                    from_node_intersection = from_intersection,
                                    to_node_intersection = to_intesection,
                                    length=length,
                                    stname = stname,
                                    oneway=oneway,
                                    bearing=bearing)
            philly_streets.add_edge(from_node_id=tnode,
                                    to_node_id=fnode,
                                    from_node_intersection = from_intersection,
                                    to_node_intersection = to_intesection,
                                    length=length,
                                    stname = stname,
                                    oneway=oneway,
                                    bearing=opposite)
        elif oneway == 'TF':
            philly_streets.add_edge(from_node_id=tnode,
                                    to_node_id=fnode,
                                    from_node_intersection = from_intersection,
                                    to_node_intersection = to_intesection,
                                    length=length,
                                    stname = stname,
                                    oneway=oneway,
                                    bearing=opposite)
        elif oneway == 'FT':
            philly_streets.add_edge(from_node_id=fnode,
                                    to_node_id=tnode,
                                    from_node_intersection = from_intersection,
                                    to_node_intersection = to_intesection,
                                    length=length,
                                    stname = stname,
                                    oneway=oneway,
                                    bearing=bearing)
    philly_streets.build_adjacency()
    x = philly_streets.show_node_adjacency(3)
    path = philly_streets.bfs_search(x.to_node_obj[0])
    print(path)
    print(path.distance)
            

if __name__ == '__main__':
    main()
