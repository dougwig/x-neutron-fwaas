# Copyright (c) 2013 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import contextlib
import mock

from neutron_fwaas.services.firewall.agents import firewall_agent_api as api
from neutron_fwaas.services.firewall.drivers import fwaas_base as base_driver
from neutron.tests import base


class NoopFwaasDriver(base_driver.FwaasDriverBase):
    """Noop Fwaas Driver.

    Firewall driver which does nothing.
    This driver is for disabling Fwaas functionality.
    """

    def create_firewall(self, apply_list, firewall):
        pass

    def delete_firewall(self, apply_list, firewall):
        pass

    def update_firewall(self, apply_list, firewall):
        pass

    def apply_default_policy(self, apply_list, firewall):
        pass


class TestFWaaSAgentApi(base.BaseTestCase):
    def setUp(self):
        super(TestFWaaSAgentApi, self).setUp()

        self.api = api.FWaaSPluginApiMixin(
            'topic',
            'host')

    def test_init(self):
        self.assertEqual(self.api.host, 'host')

    def _test_firewall_method(self, method_name, **kwargs):
        with contextlib.nested(
            mock.patch.object(self.api.client, 'call'),
            mock.patch.object(self.api.client, 'prepare'),
        ) as (
            rpc_mock, prepare_mock
        ):
            prepare_mock.return_value = self.api.client
            getattr(self.api, method_name)(mock.sentinel.context, 'test',
                                           **kwargs)

        prepare_args = {}
        prepare_mock.assert_called_once_with(**prepare_args)

        rpc_mock.assert_called_once_with(mock.sentinel.context, method_name,
                                         firewall_id='test', host='host',
                                         **kwargs)

    def test_set_firewall_status(self):
        self._test_firewall_method('set_firewall_status', status='fake_status')

    def test_firewall_deleted(self):
        self._test_firewall_method('firewall_deleted')
