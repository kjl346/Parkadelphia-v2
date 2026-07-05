import pandas as pd
import numpy as np
from graph import Graph
import duckdb
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
    full_ds = pd.merge(street_centerlines,
                       street_nodes[['X','Y','intersecti','node_id']],
                       left_on=['fnode_'],
                       right_on='node_id',
                       validate='many_to_one',
                       how='left',
                       suffixes=('','_from')).rename({'X':'X_from','Y':'Y_from','intersecti':'intersecti_from'},axis=1)
    
    full_ds.rename({'X':'X_from','Y':'Y_from','intersecti':'intersecti_from'}
                   ,axis=1
                   ,inplace=True)
    
    full_ds = pd.merge(full_ds,
                       street_nodes[['X','Y','intersecti','node_id']],
                       left_on=['tnode_'],
                       right_on='node_id',
                       validate='many_to_one',
                       how='left',
                       suffixes=('','_to'))
    
    full_ds.rename({'X':'X_to','Y':'Y_to','intersecti':'intersecti_to'}
                   ,axis=1
                   ,inplace=True)

    #calc bearings
    dx = full_ds['X_to'] - full_ds['X_from']
    dy = full_ds['Y_to'] - full_ds['Y_from']
    full_ds['bearing'] = np.degrees(np.arctan2(dy,dx))

    #load streets
    philly_streets = Graph()
    print(full_ds.columns)
    for ind, data in full_ds[(full_ds.oneway.str.strip() != '')].iterrows():


        



        edge_specs = []

        if data.oneway in ('B','FT'):
            edge_specs.append((data.fnode_,
                               data.tnode_,
                               round(data.bearing,2),
                               data.intersecti_from,
                               data.intersecti_to,
                               data.r_f_add,
                               data.r_t_add))
        if data.oneway in ('B','TF'):
            opposite = (data.bearing + 180) % 360
            if opposite > 180:
                opposite -= 360
            opposite = round(opposite,2)
            edge_specs.append((data.tnode_,
                               data.fnode_,
                               opposite,
                               data.intersecti_to,
                               data.intersecti_from,
                               data.l_t_add,
                               data.l_f_add))

        for from_id, to_id, edge_bearing,f_inter,t_inter,f_block,t_block in edge_specs:
            philly_streets.add_edge(
                from_node_id=from_id,
                to_node_id=to_id,
                from_node_intersection=f_inter,
                to_node_intersection=t_inter,
                length=data.length,
                stname=data.stname,
                oneway=data.oneway,
                bearing=edge_bearing,
                f_block=f_block,
                t_block=t_block
            )
    philly_streets.build_adjacency()
    #merge streets & centerlines to get more info 
    return philly_streets

    
    
