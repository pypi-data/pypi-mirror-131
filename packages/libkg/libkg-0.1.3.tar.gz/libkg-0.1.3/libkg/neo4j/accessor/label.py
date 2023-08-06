from kgdt.neo4j.accessor.label import LabelGraphAccessor
from py2neo import Node

class LibKGLabelGraphAccessor(LabelGraphAccessor):

    def get_labels(self,node):
        if isinstance(node, Node):
            return list(node.labels)
        return []
