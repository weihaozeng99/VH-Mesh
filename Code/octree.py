class OctreeNode(object):

    MAX_CHILD_NODES = 8

    def __init__(self, **kwargs):
        self.x0 = kwargs.pop('x0')
        self.x1 = kwargs.pop('x1')
        self.y0 = kwargs.pop('y0')
        self.y1 = kwargs.pop('y1')
        self.z0 = kwargs.pop('z0')
        self.z1 = kwargs.pop('z1')

        self.root_node: OctreeNode = None
        self.parent_node: OctreeNode = None
        self.child_nodes = None

       self.objects = None
       self.guids = None

    def get_root_node(self) -> 'OctreeNode':
        return self.root_node

    def set_root_node(self, node: 'OctreeNode') -> None:
        self.root_node = node

    def get_parent_node(self) -> 'OctreeNode':
        return self.parent_node

    def set_parent_node(self, node: 'OctreeNode') -> None:
        self.parent_node = node

    def get_child_nodes(self) -> List['OctreeNode']:
        return self.child_nodes

    def set_child_nodes(self, nodes: List['OctreeNode']) -> None:
        self.child_nodes = nodes

    def can_contain_child_nodes(self) -> bool:
        update_dist = Config.World.Gameplay.update_dist

        return ((self.x1 - self.x0) > update_dist and
                (self.y1 - self.y0) > update_dist and
                (self.z1 - self.z0) > update_dist)

    def get_object(self, guid: int):
        return self.objects.get(guid, None)

    def set_object(self, obj: Union[Unit, Player]) -> None:
        if self.get_child_nodes():
            node = self._get_nearest_child_node(obj)
            node.set_object(obj)
        else:
            self.objects[obj.guid] = obj

    def should_contain_object(self, obj: Union[Unit, Player]) -> bool:
        return (self.x0 <= obj.x <= self.x1 and
                self.y0 <= obj.y <= self.y1 and
                self.z0 <= obj.z <= self.z1)

    def _get_nearest_child_node(self, obj: Union[Unit, Player]):
        for i in range(0, OctreeNode.MAX_CHILD_NODES):
            if self.child_nodes[i].should_contain_object(obj):
                return self.child_nodes[i]

class OctreeBuilder(object):

    def __init__(self, **kwargs):

        self.x0 = kwargs.pop('x0')
        self.x1 = kwargs.pop('x1')
        self.y0 = kwargs.pop('y0')
        self.y1 = kwargs.pop('y1')

        # FIXME: should get actual height for each map (use ADT, WDT, WMO for this purpose)
        self.z0 = -2000
        self.z1 = 2000

        self.root_node = OctreeNode(x0=self.x0, x1=self.x1, y0=self.y0, y1=self.y1, z0=self.z0, z1=self.z1)
        self.objects = kwargs.pop('objects', {})

    def build(self) -> OctreeNode:
        self._build_child_nodes(self.root_node, self.root_node)
        self.root_node.objects = self.objects
        return self.root_node

    def _set_objects(self) -> None:
        for obj in self.objects.values():
            self.root_node.set_object(obj)

    def _build_child_nodes(self, node: OctreeNode, root_node: OctreeNode) -> None:
        middle_x = (node.x0 + node.x1) / 2
        middle_y = (node.y0 + node.y1) / 2
        middle_z = (node.z0 + node.z1) / 2

        x = ((node.x0, middle_x), (middle_x, node.x1))
        y = ((node.y0, middle_y), (middle_y, node.y1))
        z = ((node.z0, middle_z), (middle_z, node.z1))

        child_nodes = []

        for i in range(1, OctreeNode.MAX_CHILD_NODES + 1):
            x0, x1 = x[i % 2 == 0]
            y0, y1 = y[(i & 3) % 3 == 0]
            z0, z1 = z[i > 4]

            child_node = OctreeBuilder._build_node(x0, x1, y0, y1, z0, z1)
            child_node.set_root_node(root_node)
            child_node.set_parent_node(node)

            if child_node.can_contain_child_nodes():
                self._build_child_nodes(child_node, root_node)
            else:
                child_node.guids = []

            child_nodes.append(child_node)

        node.set_child_nodes(child_nodes)

    @staticmethod
    def _build_node(x0: float, x1: float, y0: float, y1: float, z0: float, z1: float) -> OctreeNode:
        return OctreeNode(x0=x0, x1=x1, y0=y0, y1=y1, z0=z0, z1=z1)