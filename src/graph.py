from collections import defaultdict,deque
import pandas as pd
class Node: 
    def __init__(self, id,intersection):
        self.id = int(id)
        self.intersection = intersection
    def __repr__(self):
        return f"Node(id={self.id}, intersection='{self.intersection}')"

        
class Edge:
    def __init__(self, from_node, to_node, length, stname, oneway,bearing):
        self.from_node = from_node
        self.to_node = to_node
        self.length = length
        self.stname = stname
        self.oneway = oneway
        self.bearing = bearing
    def __repr__(self):
        return (
            f"Edge(from={self.from_node.id}, to={self.to_node.id}, "
            f"street='{self.stname}', length={self.length}, "
            f"oneway='{self.oneway}', bearing={self.bearing})"
        )

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
        self.distance+=edge.length

    def copy(self):
        path = Path(self.starting_node)
        path.distance = self.distance
        path.current_bearing = self.current_bearing
        path.visited_edge = self.visited_edge.copy()
        path.path_nodes = self.path_nodes.copy()
        path.current_node = self.current_node
        return path
    
    def __repr__(self):
        path = []
        path.append(self.starting_node.intersection)
        for edge in self.visited_edge:
            path.append(' -> ')
            path.append(edge.stname)
            path.append(' -> ')
            path.append(edge.to_node.intersection)
        
        return ''.join(path)
    

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
    def show_node_adjacency(self, node_id,rows = None):
        if rows is None:
            rows = []

        node = node_id if isinstance(node_id, Node) else self.nodes.get(node_id,'')
        for edge in self.adjacency.get(node, []):
            rows.append({
            "from_node": edge.from_node.id,
            'from_node_obj':edge.from_node,
            "to_node": edge.to_node.id,
            'to_node_obj':edge.to_node,
            'from_intersection':edge.from_node.intersection,
            'to_intersection':edge.to_node.intersection,
            "street_name": edge.stname,
            "length": edge.length,
            "oneway": edge.oneway,
            'bearing' : edge.bearing,
            'edge':edge
        })
        return pd.DataFrame(rows)
    def bfs_search(self,start_node,uturns = False):
        starting_path = deque([Path(starting_node=start_node)])

        while starting_path:
            current_path = starting_path.popleft()

            if current_path.distance > 0 and current_path.starting_node.id == current_path.current_node.id:
                return current_path

            for edge in self.adjacency.get(current_path.current_node, []):
                if (edge.to_node in current_path.path_nodes and edge.to_node.id != start_node.id) or ((edge.stname in [x.stname for x in current_path.visited_edge]) and not(uturns)):
                    continue
                new_path = current_path.copy()
                new_path.drive_edge(edge)
                starting_path.append(new_path)

        return None


    def query_streets(self,stname):
        
        pass

    def get_neighbors(self,start_node,max_depth =2):
        visited = {start_node}
        queue = ([(start_node,0)])
        result = []

        while queue:
            node, depth = queue.popleft()
            for node in self.adjacency.get(node,[]):
                pass
