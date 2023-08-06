from libkg.neo4j.factory import LibKGGraphInstanceFactory
from libkg.neo4j.accessor.base import LibKGGraphAccessor
from libkg.neo4j.accessor.index import LibKGIndexGraphAccessor
from libkg.neo4j.accessor.label import LibKGLabelGraphAccessor
from libkg.neo4j.accessor.metadata import LibKGMetadataGraphAccessor
from libkg.models.node import Tag, Platform, Project, ProjectVersion, ProjectVersionDependency, Repository, RepositoryDependency

class ThirdLibrary():


    def __init__(self, neo4j_config_path, choice):
        self.graph_instance_factory = LibKGGraphInstanceFactory(neo4j_config_path)
        self.graph = self.graph_instance_factory.create_py2neo_graph_by_server_name(choice)
        if self.graph is None:
            self.graph = self.graph_instance_factory.create_py2neo_graph_by_server_id(choice)
        if self.graph is not None:
            self.graphaccessor = LibKGGraphAccessor(self.graph)
            self.indexgraphaccessor = LibKGIndexGraphAccessor(self.graph)
            self.labelgraphaccessor = LibKGLabelGraphAccessor(self.graph)
            self.metadatagraphaccessor = LibKGMetadataGraphAccessor(self.graph)


    def wrapper_nodes(self, nodes):
        result = []
        for node in nodes:
            node = self.wrapper_node(node)
            result.append(node)
        return result

    def wrapper_relation(self, relation):
        return relation


    def is_entity(self, entity):
        if isinstance(entity, Project) or isinstance(entity, ProjectVersion) or isinstance(entity, ProjectVersionDependency) or \
            isinstance(entity, Repository) or isinstance(entity, RepositoryDependency) or isinstance(entity, Tag) or isinstance(entity, Platform):
            return True
        return False

    def wrapper_node(self, node):
        if self.graphaccessor.is_node(node):
            if 'project' in self.labelgraphaccessor.get_labels(node):
                return Project(self.graphaccessor.get_id(node), self.graphaccessor.get_node_properties(node))
            if 'project version' in self.labelgraphaccessor.get_labels(node):
                return ProjectVersion(self.graphaccessor.get_id(node), self.graphaccessor.get_node_properties(node))
            if 'project version dependency' in self.labelgraphaccessor.get_labels(node):
                return ProjectVersionDependency(self.graphaccessor.get_id(node), self.graphaccessor.get_node_properties(node))
            if 'platform' in self.labelgraphaccessor.get_labels(node):
                return Platform(self.graphaccessor.get_id(node), self.graphaccessor.get_node_properties(node))
            if 'repository' in self.labelgraphaccessor.get_labels(node):
                return Repository(self.graphaccessor.get_id(node), self.graphaccessor.get_node_properties(node))
            if 'repository dependency' in self.labelgraphaccessor.get_labels(node):
                return RepositoryDependency(self.graphaccessor.get_id(node), self.graphaccessor.get_node_properties(node))
            if 'tag' in self.labelgraphaccessor.get_labels(node):
                return Tag(self.graphaccessor.get_id(node), self.graphaccessor.get_node_properties(node))
            return None

    def find_entities_by_id(self, node_id):
        return self.wrapper_nodes(self.graphaccessor.find_node_by_id(node_id))


    def find_entities_by_label_property(self, label, limit=5, **property):
        return self.wrapper_nodes(self.graphaccessor.find_nodes_by_label_property(label, limit, **property))


    def find_entities_by_label(self, label, limit=5):
        return self.wrapper_nodes(self.graphaccessor.find_nodes_by_label(label, limit))


    def find_entities_by_name(self, name):
        return self.wrapper_nodes(self.graphaccessor.find_nodes_by_name(name))


    def find_entities_by_label_name(self, label, name, limit=5):
        return self.wrapper_nodes(self.graphaccessor.find_nodes_by_label_name(label, name, limit))


    def find_relations_by_entity(self, entity):
        result = []
        if self.is_entity(entity):
            try:
                id = entity.identity
                result = self.graphaccessor.find_relations_by_node_id(id)
                for result_ in result:
                    result_[0] = self.wrapper_node(result_[0])
                    result_[1] = self.wrapper_relation(result_[1])
                    result_[2] = self.wrapper_node(result_[2])
                return result
            except BaseException:
                print(BaseException)
                return result
        return result


    def find_out_relations_by_entity(self, entity):
        result = []
        if self.is_entity(entity):
            try:
                id = entity.identity
                result = self.graphaccessor.find_out_relations_by_node_id(id)
                for result_ in result:
                    result_[0] = self.wrapper_node(result_[0])
                    result_[1] = self.wrapper_relation(result_[1])
                    result_[2] = self.wrapper_node(result_[2])
                return result
            except BaseException:
                print(BaseException)
                return result
        return result

    def find_out_relations_by_node_id(self, node_id):
        result = []
        try:
            result = self.graphaccessor.find_out_relations_by_node_id(node_id)
            for result_ in result:
                result_[0] = self.wrapper_node(result_[0])
                result_[1] = self.wrapper_relation(result_[1])
                result_[2] = self.wrapper_node(result_[2])
            return result
        except BaseException:
            print(BaseException)
            return result


    def find_in_relations_by_entity(self, entity):
        result = []
        if self.is_entity(entity):
            try:
                id = entity.identity
                result = self.graphaccessor.find_in_relations_by_node_id(id)
                for result_ in result:
                    result_[0] = self.wrapper_node(result_[0])
                    result_[1] = self.wrapper_relation(result_[1])
                    result_[2] = self.wrapper_node(result_[2])
                return result
            except BaseException:
                print(BaseException)
                return result
        return result


    def find_relations_by_entity_relation_label(self, entity, relation_label):
        result = []
        if self.is_entity(entity):
            try:
                id = entity.identity
                result = self.graphaccessor.find_relations_by_node_id_relation_label(id, relation_label)
                for result_ in result:
                    result_[0] = self.wrapper_node(result_[0])
                    result_[1] = self.wrapper_relation(result_[1])
                    result_[2] = self.wrapper_node(result_[2])
                return result
            except BaseException:
                print(BaseException)
                return result
        return result


    def find_out_relations_by_entity_relation_label(self, entity, relation_label):
        result = []
        if self.is_entity(entity):
            try:
                id = entity.identity
                result = self.graphaccessor.find_out_relations_by_node_id_relation_label(id, relation_label)
                for result_ in result:
                    result_[0] = self.wrapper_node(result_[0])
                    result_[1] = self.wrapper_relation(result_[1])
                    result_[2] = self.wrapper_node(result_[2])
                return result
            except BaseException:
                print(BaseException)
                return result
        return result


    def find_in_relations_by_entity_relation_label(self, entity, relation_label):
        result = []
        if self.is_entity(entity):
            try:
                id = entity.identity
                result = self.graphaccessor.find_in_relations_by_node_id_relation_label(id, relation_label)
                for result_ in result:
                    result_[0] = self.wrapper_node(result_[0])
                    result_[1] = self.wrapper_relation(result_[1])
                    result_[2] = self.wrapper_node(result_[2])
                return result
            except BaseException:
                print(BaseException)
                return result
        return result

    def get_all_ids(self, start, end, size=10000):
        return self.graphaccessor.get_all_ids(start, end, size)


