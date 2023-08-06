from py2neo import Node, Relationship
from kgdt.neo4j.accessor.base import GraphAccessor


class LibKGGraphAccessor(GraphAccessor):


    def is_node(self, node):
        if isinstance(node,Node):
            return True
        else:
            return False


    def is_relation(self, relation):
        if isinstance(relation, Relationship):
            return True
        else:
            return False


    def get_node_properties(self, node):
        if not isinstance(node, Node):
            return {}
        return dict(node)


    def find_nodes_by_label_property(self, label, limit=5, **properties):
        result = []
        cypher_start = 'MATCH (n:`{}`{{'.format(label)
        cypher = cypher_start
        for property_name, property_value in properties.items():
            temp = "`{}`:'{}',".format(property_name, property_value)
            cypher = cypher + temp
        cypher = cypher[:-1]
        cypher_end = '}})RETURN n LIMIT {}'.format(limit)
        cypher = cypher + cypher_end
        if not properties:
            cypher = cypher_start[:-1] + cypher_end[1:]
        try:
            result = (i['n'] for i in self.graph.run(cypher).data())
            return result
        except Exception as error:
            print(error)
            return result


    def find_nodes_by_label(self, label, limit=5):
        return self.find_nodes_by_label_property(label, limit)


    def find_nodes_by_name(self, name):
        result = []
        labels = ['project', 'project version', 'project version dependency', 'repository',
                  'repository dependency', 'tag', 'platform']
        for labels_ in labels:
            temp = self.find_nodes_by_label_name(labels_, name)
            for temp_ in temp:
                result.append(temp_)
        return result


    def find_nodes_by_label_name(self, label, name, limit=5):
        result = []
        if label == 'platform':
            property = {"platform name": name}
            result = self.find_nodes_by_label_property(label, limit, **property)
        if label == 'project':
            property = {"project name": name}
            result = self.find_nodes_by_label_property(label, limit, **property)
        if label == 'project version':
            property = {"project name": name}
            result = self.find_nodes_by_label_property(label, limit, **property)
        if label == 'repository':
            property = {"repository name with owner": name}
            result = self.find_nodes_by_label_property(label, limit, **property)
        if label == 'tag':
            property = {"tag name": name}
            result = self.find_nodes_by_label_property(label, limit, **property)
        if label == 'project version dependency':
            property = {"project version dependency name": name}
            result = self.find_nodes_by_label_property(label, limit, **property)
        return result

    def find_node_by_id(self, node_id):
        cypher = 'MATCH (n)  where id(n)={} RETURN n LIMIT 1'.format(node_id)
        result = [i['n'] for i in self.graph.run(cypher).data()]
        return result

    def find_relations_by_node_id(self, node_id):
        cypher = 'Match n = (p)- [r] - (q) where id(p) = {}  return p, r, q'.format(node_id)
        result = [[i['p'], i['r'], i['q']] for i in self.graph.run(cypher).data()]
        return result


    def find_out_relations_by_node_id(self, node_id):
        cypher = 'Match n = (p)- [r] -> (q) where id(p) = {}  return p, r, q'.format(node_id)
        result = [[i['p'], i['r'], i['q']] for i in self.graph.run(cypher).data()]
        return result


    def find_in_relations_by_node_id(self, node_id):
        cypher = 'Match n = (p)- [r] -> (q) where id(q) = {}  return p, r, q'.format(node_id)
        result = [[i['p'], i['r'], i['q']] for i in self.graph.run(cypher).data()]
        return result


    def find_relations_by_node_id_relation_label(self, node_id, relation_type):
        cypher = 'Match n = (p)- [r:`{}`] - (q) where id(p) = {}  return p, r, q'.format(relation_type, node_id)
        result = [[i['p'], i['r'], i['q']] for i in self.graph.run(cypher).data()]
        return result


    def find_out_relations_by_node_id_relation_label(self, node_id, relation_type):
        cypher = 'Match n = (p)- [r:`{}`] -> (q) where id(p) = {}  return p, r, q'.format(relation_type, node_id)
        result = [[i['p'], i['r'], i['q']] for i in self.graph.run(cypher).data()]
        return result


    def find_in_relations_by_node_id_relation_label(self, node_id, relation_type):
        cypher = 'Match n = (p)- [r:`{}`] -> (q) where id(q) = {}  return p, r, q'.format(relation_type, node_id)
        result = [[i['p'], i['r'], i['q']] for i in self.graph.run(cypher).data()]
        return result


    def find_only_relations_by_relation_id(self, relation_id):
        cypher = 'Match ()- [r] -> () where id(r) = {}  return r'.format(relation_id)
        result = [i['r'] for i in self.graph.run(cypher).data()]
        return result


    def get_all_ids(self, start, end, size):
        cypher = 'match(n) where id(n)>{} and id(n)<{} return id(n) limit {}'.format(start, end, size)
        result = [i['id(n)'] for i in self.graph.run(cypher).data()]
        return result
