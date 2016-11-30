#
# Copyright (c) 2016, Arista Networks, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
#   Neither the name of Arista Networks nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# 'AS IS' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ARISTA NETWORKS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
''' Unit Tests for Table api
'''
import unittest

from requests.exceptions import HTTPError

from httmock import HTTMock

from ServiceNowRac.snow_client import SnowClient
from ServiceNowRac.snow_table import SnowTable

from test.unit.mock_defs import snow_table_get, http_return_404, \
    snow_table_getkeys, snow_table_getrecords, snow_table_insert, \
    snow_table_update, snow_table_delete, snow_table_delete_multiple, \
    snow_empty_record_list, snow_table_insert_multiple

class TestSnowTable(unittest.TestCase):
    ''' Tests the ServiceNow table api using Mock tests
    '''
    def setUp(self):
        client = SnowClient('servicenow-instance',
                            'admin',
                            'admin')
        self.table = SnowTable('incident', client)

    def test_00_get(self):
        ''' Test 'get' return
        '''
        with HTTMock(snow_table_get):
            sysid = '9c573169c611228700193229fff72400'
            data = self.table.get(sysid)

        self.assertEqual(data['sys_id'], '9c573169c611228700193229fff72400')

    def test_01_get_http_404_error(self):
        ''' Test 'get' with 404 return
        '''
        sysid = '9c573169c611228700193229fff72400'
        with HTTMock(http_return_404):
            self.assertRaises(HTTPError, self.table.get, sysid)

    def test_02_get_empty_record_return(self):
        ''' Test 'get' with 404 return
        '''
        sysid = '9c573169c611228700193229fff72400'
        with HTTMock(snow_empty_record_list):
            resp = self.table.get(sysid)

        self.assertEqual(resp, None)

    def test_03_get_keys(self):
        ''' Verify 'get_keys' functionality
        '''
        with HTTMock(snow_table_getkeys):
            data = self.table.get_keys('name=Arista Networks')

        self.assertEqual(len(data), 50)

    def test_04_get_records(self):
        ''' Verify 'get_records' functionality
        '''
        with HTTMock(snow_table_getrecords):
            data = self.table.get_records('name=Arista Networks')

        self.assertEqual(len(data), 52)

    def test_05_insert(self):
        ''' Verify 'insert' functionality
        '''
        data = {
            'category'           : 'Request',
            'comments'           : 'Test Comments',
            'description'        : 'Test generate Incident',
            'short_description'  : 'Test generate Incident',
            'state'              : 'New',
        }

        with HTTMock(snow_table_insert):
            resp = self.table.insert(data)[0]

        self.assertEqual(resp['short_description'], 'Test generate Incident')

    def test_06_insert_invalid_type(self):
        ''' Verify 'insert_multiple' fails on non-list arg
        '''
        with self.assertRaises(TypeError):
            self.table.insert_multiple(dict())
        with self.assertRaises(TypeError):
            self.table.insert_multiple(str())
        with self.assertRaises(TypeError):
            self.table.insert_multiple(int())

    def test_07_insert_multiple(self):
        ''' Verify 'insert_multiple' functionality
        '''
        data = []
        for i in range(5):
            description = 'Systest Generated: Test %d' % i
            data.append({'short_description': description})

        with HTTMock(snow_table_insert_multiple):
            resp = self.table.insert_multiple(data)
        self.assertEqual(len(resp), 5)

    def test_08_update(self):
        ''' Verify 'update' functionality
        '''
        data = {
            'category'           : 'Request',
            'comments'           : '',
        }

        query = 'sys_id=fcdd6f9613b22200a57c70a76144b0ec'
        with HTTMock(snow_table_update):
            resp = self.table.update(data, query)[0]

        self.assertEqual(resp['comments'], '')

    def test_09_delete(self):
        ''' Verify 'delete' functionality
        '''
        with HTTMock(snow_table_delete):
            sysid = 'aad67f9613b22200a57c70a76144b0ee'
            data = self.table.delete(sysid)[0]

        self.assertEqual(data['sys_id'], 'aad67f9613b22200a57c70a76144b0ee')

    def test_10_delete_multiple(self):
        ''' Verify 'delete_multiple' functionality
        '''
        with HTTMock(snow_table_delete_multiple):
            resp = self.table.delete_multiple(
                'short_descriptionSTARTSWITHSystest Generated')

        self.assertEqual(resp[0]['count'], 5)

if __name__ == '__main__':
    unittest.main()
