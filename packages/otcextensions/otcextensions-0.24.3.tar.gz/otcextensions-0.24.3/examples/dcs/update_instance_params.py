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
Update Distributed Cache Service Instance
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


params = [
    {
        'param_id': '1',
        'param_name': 'timeout',
        'default_value': '0',
        'value_range': '0-7200',
        'value_type': 'Interger',
        'param_value': '11'
    },
    {
        'param_id': '2',
        'param_name': 'maxmemory-policy',
        'default_value': 'noeviction',
        'value_range':
            'volatile-lru,allkeys-lru,volatile-random,'
            'allkeys-random,volatile-ttl,noeviction',
        'value_type': 'Enum',
        'param_value': 'allkeys-random'
    }
]
instance = 'name_or_id'
instance = conn.dcs.find_instance(instance)
conn.dcs.update_instance_params(
    instance=instance,
    params=params
)
