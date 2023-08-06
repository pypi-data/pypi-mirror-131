# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: zhouzhong
@Email: 21212010059@m.fudan.edu.cn
@Created: 2021/10/27
------------------------------------------
@Modify: 2021/10/27
------------------------------------------
@Description:
"""
from unittest import TestCase
from libkg.models.thirdlibrary import ThirdLibrary
from definitions import ROOT_DIR
import os.path
from libkg.transfer.neo4j import LibKGBatchNeo4jImporter
import pandas as pd

from libkg.neo4j.accessor.base import GraphAccessor



class TestThirdLibrary(TestCase):

    def setUp(self):
        """Set up test fixtures, if any."""
        project_header = 'project ID,project platform,project name,created timestamp,updated timestamp,description,keywords,homepage URL,licenses,repository URL,project versions count,sourcerank,latest release publish timestamp,latest release number,package manager ID,dependent projects count,language,status,last synced timestamp,dependent repositories count,repository ID'.split(
            ',')
        project_version_header = 'project version ID,project version platform,project name,project ID,project version number,published timestamp,created timestamp,updated timestamp'.split(
            ',')
        project_version_dependency_header = 'project version dependency ID,project version platform,project name,project ID,project version number,project version ID,project version dependency name,project version dependency platform,project version dependency kind,optional dependency,project version dependency requirements,dependency project ID'.split(
            ',')
        data = pd.read_csv(os.path.join(ROOT_DIR, 'data', 'project_test.csv'), dtype=object)
        data.to_csv(os.path.join(r'neo4j-community-4.2.0', 'import', 'project_test.csv'), header=project_header,
                    index=False)
        data = pd.read_csv(os.path.join(ROOT_DIR, 'data', 'project_version_test.csv'), dtype=object)
        data.to_csv(os.path.join(r'neo4j-community-4.2.0', 'import', 'project_version_test.csv'),
                    header=project_version_header, index=False)
        data = pd.read_csv(os.path.join(ROOT_DIR, 'data', 'project_version_dependency_test.csv'), dtype=object)
        data.to_csv(os.path.join(r'neo4j-community-4.2.0', 'import', 'project_version_dependency_test.csv'),
                    header=project_version_dependency_header, index=False)

        thirdlibrary = ThirdLibrary(os.path.join(ROOT_DIR, 'neo4j_config.json'), 1)
        graphac = GraphAccessor(thirdlibrary.graph)
        importor = LibKGBatchNeo4jImporter(graphac)
        importor.batch_import_nodes_from_csv(1000, 'project_test.csv', {'project'},
                                             {'project ID': 'project ID', 'project name': 'project name'})
        importor.batch_import_nodes_from_csv(1000, 'project_version_test.csv', {'project version'},
                                             {'project version ID': 'project version ID',
                                              'project name': 'project name', 'project ID': 'project ID'})
        importor.batch_import_nodes_from_csv(1000, 'project_version_dependency_test.csv',
                                             {'project version dependency'},
                                             {'project version dependency ID': 'project version dependency ID',
                                              'project version ID': 'project version ID',
                                              'project version dependency name': 'project version dependency name',
                                              'project ID': 'project ID',
                                              'dependency project ID': 'dependency project ID'})

        match_nodes = [[{'project version'}, 'project version ID', 'project version ID'],
                       [{'project'}, 'project ID', 'project ID']]
        relations = [[2, 'has project version', 1]]
        importor.batch_import_relations_from_csv(1000, 'project_version_test.csv', match_nodes, relations)
        match_nodes = [[{'project'}, 'project ID', 'project ID'],
                       [{'project version'}, 'project version ID', 'project version ID'],
                       [{'project version dependency'}, 'project version dependency ID',
                        'project version dependency ID'],
                       [{'project'}, 'project ID', 'dependency project ID']
                       ]

        relations = [[1, 'has project version dependency', 3],
                     [2, 'has project version dependency', 3],
                     [3, 'depend on project', 4]
                     ]
        importor.batch_import_relations_from_csv(1000, 'project_version_dependency_test.csv', match_nodes, relations)

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_find_entities(self):
        thirdlibrary = ThirdLibrary(os.path.join(ROOT_DIR, 'neo4j_config.json'), 1)
        entity = thirdlibrary.find_entities_by_label('project version')
        print("find entities by label")
        for entity_ in entity:
            print(entity_)

        entity = thirdlibrary.find_entities_by_name("ae")
        print("find entities by name")
        for entity_ in entity:
            print(entity_)

        entity = thirdlibrary.find_entities_by_label_name('project', "ae")
        print("find entities by label and name")
        for entity_ in entity:
            print(entity_)

        entity = thirdlibrary.find_entities_by_label_property("project", **{"project name": "ae"})
        print("find entities by label and properties")
        for entity_ in entity:
            print(entity_)

    def test_find_relations(self):
        thirdlibrary = ThirdLibrary(os.path.join(ROOT_DIR, 'neo4j_config.json'), 1)
        entity = thirdlibrary.find_entities_by_label_name('project version', 'ae')
        entity_t = entity[0]

        entity = thirdlibrary.find_relations_by_entity(entity_t)
        for entity_ in entity:
            print(entity_)

        entity = thirdlibrary.find_in_relations_by_entity(entity_t)
        for entity_ in entity:
            print(entity_)

        entity = thirdlibrary.find_out_relations_by_entity(entity_t)
        for entity_ in entity:
            print(entity_)

        entity = thirdlibrary.find_relations_by_entity_relation_label(entity_t, "has project version dependency")
        for entity_ in entity:
            print(entity_)

























