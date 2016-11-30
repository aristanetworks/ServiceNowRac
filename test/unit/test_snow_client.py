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
''' Unit Tests for SnowClient
'''
import unittest

from requests.exceptions import HTTPError, TooManyRedirects

from httmock import HTTMock

from ServiceNowRac.snow_client import SnowClient
from ServiceNowRac.snow_session import MaxRetryError

from test.unit.mock_defs import http_return_302, http_return_404, \
    http_return_502, http_timeout_error, http_connection_error, \
    snow_table_getkeys, snow_request_json_no_record, snow_post_json_valid, \
    snow_post_json_no_payload, snow_invalid_sysparm_action, \
    snow_invalid_insert, snow_bad_json_return, http_too_many_redirects


DATA = {
    'category'           : 'Request',
    'comments'           : 'Test Comments',
    'description'        : 'Test generate Incident',
    'impact'             : '3',
    'priority'           : '3',
    'short_description'  : 'Test generate Incident',
    'reason'             : 'Network Requirements',
    'state'              : 'New',
    'type'               : 'Routine',
}

class TestSnowClient(unittest.TestCase):
    ''' Tests the ServiceNow Client using Mock tests
    '''
    def setUp(self):
        self.client = SnowClient('servicenow-instance',
                                 'admin',
                                 'admin')

    def test_00_get_by_query(self):
        ''' Verify data returned via 'get'
        '''
        with HTTMock(snow_table_getkeys):
            resp = self.client.get('incident', 'sysparm_action=getKeys')
        self.assertEqual(len(resp), 50)

    def test_01_get_302(self):
        ''' Verify 'get' handling of HTTP302 with retry
        '''
        client = SnowClient('servicenow-instance',
                            'admin',
                            'admin', api='')

        with HTTMock(http_return_302):
            with self.assertRaises(MaxRetryError):
                client.get('incident', 'sysparm_action=getKeys')

    def test_02_get_404(self):
        ''' Verify 'get' handing of HTTP404
        '''
        with HTTMock(http_return_404):
            self.assertRaises(HTTPError, self.client.get, 'incident',
                              'sysparm_action=getKeys')

    def test_03_get_502(self):
        ''' Verify 'get' handing of HTTP404
        '''
        with HTTMock(http_return_502):
            self.assertRaises(MaxRetryError, self.client.get, 'incident',
                              'sysparm_action=getKeys')

    def test_04_get_too_many_redirects(self):
        ''' Verify 'get' handing of TooManyRedirects
        '''
        with HTTMock(http_too_many_redirects):
            self.assertRaises(TooManyRedirects, self.client.get, 'incident',
                              'sysparm_action=getKeys')

    def test_05_get_json_ret_error(self):
        ''' Verify 'get' handling of error status in json
        '''
        with HTTMock(snow_invalid_sysparm_action):
            resp = self.client.get('incident', 'sysparm_action=dummy')
        self.assertEqual(resp, None)

    def test_06_get_json_no_record(self):
        ''' Verify 'get' handling of json with no record
        '''
        with HTTMock(snow_request_json_no_record):
            resp = self.client.get('incident', 'sysparm_action=get')
        self.assertEqual(resp, {u'status': u'pass'})

    def test_07_get_bad_json(self):
        ''' Verify 'get' handling of json with no record
        '''
        with HTTMock(snow_bad_json_return):
            resp = self.client.get('incident', 'sysparm_action=get')
        self.assertEqual(resp, None)

    def test_08_get_timeout(self):
        ''' Verify 'get' handling of Timeout
        '''
        with HTTMock(http_timeout_error):
            self.assertRaises(MaxRetryError,
                              self.client.get, 'incident',
                              'sysparm_action=getKeys')

    def test_09_get_connection_error(self):
        ''' Verify 'get' handling of ConnectionError
        '''
        with HTTMock(http_connection_error):
            self.assertRaises(MaxRetryError,
                              self.client.get, 'incident',
                              'sysparm_action=getKeys')

    def test_10_post_valid_data(self):
        ''' Verify 'post' handling of valid insert
        '''
        with HTTMock(snow_post_json_valid):
            resp = self.client.post('incident', 'sysparm_action=insert', DATA)
        self.assertNotEqual(resp, None)

    def test_11_post_no_payload(self):
        ''' Verify 'post' handling of no payload returns NoneType
        '''
        payload = None
        with HTTMock(snow_post_json_no_payload):
            resp = self.client.post('incident', 'sysparm_action=insert',
                                    payload)
        self.assertEqual(resp, None)

    def test_12_post_302(self):
        ''' Verify 'post' handing of HTTP302
        '''
        client = SnowClient('servicenow-instance',
                            'admin',
                            'admin', api='')

        with HTTMock(http_return_302):
            with self.assertRaises(MaxRetryError):
                client.post('incident', 'sysparm_action=insert', DATA)

    def test_13_post_404(self):
        ''' Verify 'post' handing of HTTP404
        '''
        with HTTMock(http_return_404):
            self.assertRaises(HTTPError,
                              self.client.post, 'incident',
                              'sysparm_action=insert', DATA)

    def test_14_post_json_ret_error(self):
        ''' Verify 'post' handling of error status in json
        '''
        payload = {}
        with HTTMock(snow_invalid_sysparm_action):
            resp = self.client.post('incident', 'sysparm_action=dummy',
                                    payload)
        self.assertEqual(resp, None)

    def test_15_post_bad_json(self):
        ''' Verify 'get' handling of json with no record
        '''
        data = {
            'comments'           : 'Test Comments',
            'description'        : 'Test generate Incident',
        }
        with HTTMock(snow_bad_json_return):
            resp = self.client.post('incident', 'sysparm_action=insert', data)
        self.assertEqual(resp, None)

    def test_16_post_record_error(self):
        ''' Verify 'post' handling of record with __error returns NoneType
        '''
        payload = {}
        with HTTMock(snow_invalid_insert):
            resp = self.client.post('incident', 'sysparm_action=insert',
                                    payload)
        self.assertEqual(resp, None)

    def test_17_post_timeout(self):
        ''' Verify 'post' handling of Timeout
        '''
        with HTTMock(http_timeout_error):
            self.assertRaises(MaxRetryError,
                              self.client.post, 'incident',
                              'sysparm_action=insert', DATA)

    def test_18_post_connection_error(self):
        ''' Verify 'post' handling of ConnectionError
        '''
        with HTTMock(http_connection_error):
            self.assertRaises(MaxRetryError,
                              self.client.post, 'incident',
                              'sysparm_action=insert', DATA)

if __name__ == '__main__':
    unittest.main()
