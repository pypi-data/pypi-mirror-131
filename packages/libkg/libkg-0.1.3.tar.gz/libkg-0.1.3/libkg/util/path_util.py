# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: Lenovo
@Email: 21212010059@m.fudan.edu.cn
@Created: 2021/12/17
------------------------------------------
@Modify: 2021/12/17
------------------------------------------
@Description:
"""
import os
from definitions import ROOT_DIR

class PathUtil:

    @staticmethod
    def neo4j_config_json_path():
        return os.path.join(ROOT_DIR, 'neo4j_config.json')
