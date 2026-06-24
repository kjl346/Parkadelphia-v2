import pandas as pd
import numpy as np
from graph import Graph
def build_graph(
        streets_path,
        streets_centerline_path,
        nodes_path,
        parking_permit_blocks_path,
        meters_path
        ):
    #load data
    parking_permit_blocks = pd.read_csv(parking_permit_blocks_path)
    street_nodes = pd.read_csv(nodes_path)
    street_centerlines = pd.read_csv(streets_centerline_path)
    complete_streets = pd.read_csv(streets_path)
    meters = pd.read_csv(meters_path)
    
    #Merge tables
    full_ds = pd.merge(street_centerlines,street_nodes[['X','Y','intersecti','node_id']],left_on=['fnode_'],right_on='node_id',validate='many_to_one',how='left',suffixes=('','_from')).rename({'X':'X_from','Y':'Y_from','intersecti':'intersecti_from'},axis=1)
    full_ds  = pd.merge(full_ds,street_nodes[['X','Y','intersecti','node_id']],left_on=['tnode_'],right_on='node_id',validate='many_to_one',how='left',suffixes=('','_to')).rename({'X':'X_to','Y':'Y_to','intersecti':'intersecti_to'},axis=1)

    #calc bearings
    dx = full_ds['X_to'] - full_ds['X_from']
    dy = full_ds['Y_to'] - full_ds['Y_from']
    full_ds['bearing'] = np.degrees(np.arctan2(dy,dx))

    #load streets
    philly_streets = Graph()
    print(full_ds.columns)
    for ind, data in full_ds[(full_ds.oneway.str.strip() != '')].iterrows():
        fnode = data.fnode_
        tnode = data.tnode_
        length = data.length
        stname = data.stname
        oneway = data.oneway
        from_intersection = data.intersecti_from
        to_intesection = data.intersecti_to
        bearing = round(data.bearing,2)
        l_hundred = data.l_hundred
        r_hundred = data.r_hundred
        opposite = (bearing + 180) % 360
        if opposite > 180:
            opposite -= 360
        opposite = round(opposite,2)
        if oneway == 'B':
            philly_streets.add_edge(from_node_id=fnode,
                                    to_node_id=tnode,
                                    from_node_intersection = from_intersection,
                                    to_node_intersection = to_intesection,
                                    length=length,
                                    stname = stname,
                                    oneway=oneway,
                                    bearing=bearing,
                                    block = r_hundred)
            philly_streets.add_edge(from_node_id=tnode,
                                    to_node_id=fnode,
                                    from_node_intersection = from_intersection,
                                    to_node_intersection = to_intesection,
                                    length=length,
                                    stname = stname,
                                    oneway=oneway,
                                    bearing=opposite,
                                    block = l_hundred)
        elif oneway == 'TF':
            philly_streets.add_edge(from_node_id=tnode,
                                    to_node_id=fnode,
                                    from_node_intersection = from_intersection,
                                    to_node_intersection = to_intesection,
                                    length=length,
                                    stname = stname,
                                    oneway=oneway,
                                    bearing=opposite,
                                    block = l_hundred)
        elif oneway == 'FT':
            philly_streets.add_edge(from_node_id=fnode,
                                    to_node_id=tnode,
                                    from_node_intersection = from_intersection,
                                    to_node_intersection = to_intesection,
                                    length=length,
                                    stname = stname,
                                    oneway=oneway,
                                    bearing=bearing,
                                    block = r_hundred)
    philly_streets.build_adjacency()
    #merge streets & centerlines to get more info 
    return philly_streets

    
    
