from collections import defaultdict,deque
import pandas as pd
class Node: 
    def __init__(self, id,intersection):
        self.id = int(id)
        self.intersection = intersection
        
class Edge:
    def __init__(self, from_node, to_node, length, stname, oneway,bearing):
        self.from_node = from_node
        self.to_node = to_node
        self.length = length
        self.stname = stname
        self.oneway = oneway
        self.bearing = bearing

class Path:
    def __init__(self,starting_node):
        self.distance = 0
        self.current_bearing = 0
        self.visited_edge = []
        self.path_nodes = [starting_node]
        self.current_node = starting_node
        self.starting_node = starting_node

    def drive_edge(self,edge):
        self.path_nodes.append(edge.to_node)
        self.current_node = edge.to_node
        self.visited_edge.append(edge)
        self.current_bearing = edge.bearing
        self.distance+=edge.distance
    
    def __str__(self):
        path = []
        path.append((self.starting_node.id))
        for edge in self.visited_edge:
            path.append('->')
            path.append(edge.stname)
            path.append('->')
            path.append(edge.to_node)
        print(''.join(path))
        return

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.adjacency = {}

    def get_or_create_node(self,node_id: int,intersection):
        
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id,intersection)
        return self.nodes[node_id]
    def add_edge(self, 
                    from_node_id,
                    from_node_intersection,
                    to_node_id,
                    to_node_intersection, 
                    length, 
                    stname, 
                    oneway,
                    bearing):
        from_node = self.get_or_create_node(from_node_id,
                                            from_node_intersection)
        to_node = self.get_or_create_node(to_node_id,
                                          to_node_intersection)
        edge = Edge(from_node = from_node,
                        to_node =  to_node, 
                        length = length,  
                        stname = stname,
                        oneway = oneway,
                        bearing=bearing)
        self.edges.append(edge)
    def build_adjacency(self):
        adjacency = defaultdict(list)
        for edge in self.edges:
            adjacency[edge.from_node].append(edge)
        self.adjacency=adjacency
    def show_node_adjacency(self, node_id,rows = []):
        
        
        node = self.nodes.get(node_id,'')
        for edge in self.adjacency.get(node, []):
            rows.append({
            "from_node": edge.from_node.id,
            "to_node": edge.to_node.id,
            'from_intersection':edge.from_node.intersection,
            'to_intersection':edge.to_node.intersection,
            "street_name": edge.stname,
            "length": edge.length,
            "oneway": edge.oneway,
            'bearing' : edge.bearing,
            'edge':edge
        })
        return pd.DataFrame(rows)
    def search(self,current_node,start_node,path,distance):
        if distance == 0 :
            current_node = start_node 
            best_loop = None
        if distance > 10000:
            return 
        if current_node == start_node:
            return 

        
        for ind,next_edge in self.show_node_adjacency(current_node):
            search(next_edge.to_node,start_node,)
    def get_neighbors(self,start_node,max_depth =2):
        visited = {start_node}
        queue = ([(start_node,0)])
        result = []

        while queue:
            node, depth = queue.popleft()
            for node in self.adjacency.get(node,[]):
                pass