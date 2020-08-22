#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 1999-2018 Alibaba Group Holding Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


try:
    from .core import create_mars_cluster, to_mars_dataframe, \
        persist_mars_dataframe, run_script_in_mars, run_mars_job, \
        list_mars_instances
except ImportError:
    create_mars_cluster = None
    to_mars_dataframe = None
    persist_mars_dataframe = None
    run_script_in_mars = None
    run_mars_job = None
    list_mars_instances = None

try:
    from . import dataframe
except ImportError:
    dataframe = None

try:
    from . import tensor
except ImportError:
    tensor = None

try:
    from . import actors
except ImportError:
    actors = None

try:
    from mars.executor import register
    from mars.remote.core import RemoteFunction
    from .core import execute_with_odps_context
    from .run_script import RunScript

    register(RemoteFunction, execute_with_odps_context(RemoteFunction.execute))
    register(RunScript, execute_with_odps_context(RunScript.execute))
except ImportError:
    pass


INTERNAL_PATTERN = '\/[^\.]+\.[^\.-]+\.[^\.-]+\-[^\.-]+\.'

