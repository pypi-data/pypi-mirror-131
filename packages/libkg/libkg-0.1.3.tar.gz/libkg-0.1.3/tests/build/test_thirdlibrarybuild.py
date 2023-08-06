# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: Lenovo
@Email: 21212010059@m.fudan.edu.cn
@Created: 2021/11/05
------------------------------------------
@Modify: 2021/11/05
------------------------------------------
@Description:
"""


from unittest import TestCase


from libkg.build.thirdlibrarybuild import ThirdLibraryBuilder
from definitions import ROOT_DIR
import os

class TestThirdLibraryBuilder(TestCase):

    def test_build(self):


        thirdlibrarybuilder = ThirdLibraryBuilder(os.path.join(ROOT_DIR, 'neo4j_config.json'))
        neo4j_admin_location = r"D:\neo4j\Soft\neo4j-community-4.3.5\bin\neo4j-admin"
        database_name = "thirdlibrary"
        csv_file_2_labels = {r"D:\neo4j\Soft\neo4j-community-4.3.5\import\person.csv": {"person"},
                             r"D:\neo4j\Soft\neo4j-community-4.3.5\import\good.csv": {"good"}}
        commend_stop = r'D:\neo4j\Soft\neo4j-community-4.3.5\bin\neo4j stop'
        commend_start = r'D:\neo4j\Soft\neo4j-community-4.3.5\bin\neo4j start'
        constraint_label_2_property_name = {"person": "person id", "good": "good name"}
        index_label_2_property_name = {"person": "person name", "good": "good id"}
        import_relation_list = [[
                                1000,
                                "relation.csv",
                                [[{'person'}, 'person id', 'person id'], [{'good'}, 'good id', 'good id']],
                                [[1, 'like eat', 2], [2, 'belong to', 1]]
                                ]]

        thirdlibrarybuilder.build(neo4j_admin_location, database_name, csv_file_2_labels,
                                  commend_stop, commend_start,
                                  constraint_label_2_property_name,
                                  import_relation_list,
                                  index_label_2_property_name)




