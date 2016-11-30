# pylint: disable=unused-argument
# pylint: disable=wrong-import-position
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

''' Mock defs
'''
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../lib'))
import json

from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from httmock import response, urlmatch

from testlib import get_fixture_data

NETLOC = r'servicenow-instance.service-now.com'
HEADERS = {'content-type': 'application/json'}

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do')
def http_return_302(url, request):
    ''' Mock RESTful GET call.
    '''
    return response(302, '', HEADERS, None, 5, request)

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do')
def http_return_404(url, request):
    ''' Mock http return 404
    '''
    return response(404, '', HEADERS, None, 5, request)

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do')
def http_return_502(url, request):
    ''' Mock http return 502
    '''
    return response(502, '', HEADERS, None, 5, request)

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do')
def http_timeout_error(url, request):
    ''' Mock TestTimeout
    '''
    raise Timeout('TestTimeout')

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do')
def http_connection_error(url, request):
    ''' Mock ConnectionError
    '''
    raise ConnectionError('Connection Error')

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do')
def http_too_many_redirects(url, request):
    ''' Mock TooManyRedirects
    '''
    raise TooManyRedirects('Gazillion')

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do')
def snow_invalid_sysparm_action(url, request):
    ''' Mock json error status.
    '''
    content_json = json.dumps({
        'error' : 'Invalid sysparm_action',
        'reason' : 'Some reason'
    })
    return response(200, content_json, HEADERS, None, 5, request)

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do')
def snow_bad_json_return(url, request):
    ''' Mock invalid json reply
    '''
    return response(200, '{"":"":}', HEADERS, None, 5, request)

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do', method='GET')
def snow_request_json_no_record(url, request):
    ''' Mock json return with no {'record':[{}...]} format
    '''
    content_json = json.dumps({'status' : 'pass'})
    return response(200, content_json, HEADERS, None, 5, request)

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do', method='GET')
def snow_empty_record_list(url, request):
    ''' Mock json return with empty record list {'record':[]}
    '''
    content_json = json.dumps({u'records': []})
    return response(200, content_json, HEADERS, None, 5, request)

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do', method='POST')
def snow_post_json_valid(url, request):
    ''' Mock valid json reply
    '''
    content_json = get_fixture_data('incident_table_insert.json')
    return response(200, content_json, HEADERS, None, 5, request)

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do', method='POST')
def snow_post_json_no_payload(url, request):
    ''' Mock json error response.
    '''
    content_json = json.dumps({
        'reason' : 'No data',
        'error' : 'Request JSON object for insert cannot be null.'
    })
    return response(200, content_json, HEADERS, None, 5, request)

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do', method='POST')
def snow_invalid_insert(url, request):
    ''' Mock table error.
    '''
    content_json = get_fixture_data('incident_table_insert_error.json')
    return response(200, content_json, HEADERS, None, 5, request)

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do',
          query='JSONv2&sysparm_action=getKeys',
          method='GET')
def snow_table_getkeys(url, request):
    ''' Mock GET for getKeys
    '''
    content_json = get_fixture_data('incident_table_getKeys.json')
    return response(200, content_json, HEADERS, None, 5, request)

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do', method='POST')
def snow_table_insert(url, request):
    ''' Mock POST insert request reponse
    '''
    content_json = get_fixture_data('incident_table_insert.json')
    return response(200, content_json, HEADERS, None, 5, request)

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do', method='POST')
def snow_table_insert_multiple(url, request):
    ''' Mock POST insert multiple request response
    '''
    content_json = get_fixture_data('incident_table_insert_multiple.json')
    return response(200, content_json, HEADERS, None, 5, request)

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do', query='JSONv2',
          method='GET')
def snow_table_get(url, request):
    ''' Mock GET request for incident table
    '''
    content_json = get_fixture_data('incident_table_sysid.json')
    return response(200, content_json, HEADERS, None, 5, request)

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do', method='GET')
def snow_table_getrecords(url, request):
    ''' Mock GET for table records
    '''
    content_json = get_fixture_data('incident_table_records.json')
    return response(200, content_json, HEADERS, None, 5, request)

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do', method='POST')
def snow_table_update(url, request):
    ''' Mock POST table update request response
    '''
    content_json = get_fixture_data('incident_table_update_record.json')
    return response(200, content_json, HEADERS, None, 5, request)

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do', method='POST')
def snow_table_delete(url, request):
    ''' Mock POST table delete request response
    '''
    content_json = get_fixture_data('incident_table_delete_record.json')
    return response(200, content_json, HEADERS, None, 5, request)

@urlmatch(scheme='https', netloc=NETLOC, path='/incident.do', method='POST')
def snow_table_delete_multiple(url, request):
    ''' Mock POST delete multiple request response
    '''
    content_json = json.dumps({"records" : [{"count" : 5}]})
    return response(200, content_json, HEADERS, None, 5, request)
