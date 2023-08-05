#!/usr/bin/env python3
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""
Find a Queue Group
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

queue = 'name_or_id'
queue = conn.dms.find_queue(name_or_id=queue)
group = 'name_or_id'
raw = conn.dms.find_group(queue=queue, name_or_id=group)
print(raw)
