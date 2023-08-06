# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: Lenovo
@Email: 21212010059@m.fudan.edu.cn
@Created: 2021/11/02
------------------------------------------
@Modify: 2021/11/02
------------------------------------------
@Description:
"""
import os

from libkg.transfer.neo4j import  LibKGBatchNeo4jImporter
from libkg.neo4j.factory import LibKGGraphInstanceFactory
from libkg.neo4j.accessor.base import LibKGGraphAccessor
from libkg.neo4j.accessor.index import LibKGIndexGraphAccessor

class ThirdLibraryBuilder:

    def __init__(self, neo4j_config_file):
        self.factory = LibKGGraphInstanceFactory(neo4j_config_file)

    def build(self, neo4j_admin_location, database_name, csv_file_2_labels,
                commend_stop, commend_start,
                constraint_label_2_property_name,
                import_relation_list,
                index_label_2_property_name):

        batch_neo4j_Importer = LibKGBatchNeo4jImporter(LibKGGraphAccessor())
        print("start : import node by neo4j-admin")
        batch_neo4j_Importer.batch_import_nodes_by_neo4j_admin(neo4j_admin_location, database_name, csv_file_2_labels)
        print("end : import node by neo4j-admin")

        print("start : restart the neo4j")
        os.system(commend_stop)
        os.system(commend_start)
        print("end : restart the neo4j")

        print("start : connect to neo4j")
        graph = self.factory.create_py2neo_graph_by_server_id(1)
        print("end : connect to neo4j")

        print("start : create constarint_unique")
        for constraint_label , constraint_property_name in constraint_label_2_property_name.items():
           LibKGIndexGraphAccessor(graph).create_constraint_unique(constraint_label, constraint_property_name)
        print("end : create constarint_unique")

        print("start : import relations from csv")
        batch_neo4j_Importer = LibKGBatchNeo4jImporter(LibKGGraphAccessor(graph))
        for import_relation in import_relation_list:
            batch_neo4j_Importer.batch_import_relations_from_csv(import_relation[0], import_relation[1],
                                                                 import_relation[2], import_relation[3])
        print("end : import relations from csv")

        print("start : create index")
        for index_label, index_property_name in index_label_2_property_name.items():
            LibKGIndexGraphAccessor(graph).create_index(index_label, index_property_name)
        print("end : create index")


