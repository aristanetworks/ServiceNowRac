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
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
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
''' ServiceNow Client

This module provides the client for ServiceNow actions. It provides
the underlying reliable connection and defines the get and post methods
for interacting with ServiceNow REST API.
'''

import json
import logging

from logging.handlers import SysLogHandler
from .snow_session import SnowSession

# XXX
# 1) Need to create well defined errors that the caller can handle

class SnowClient(object):
    ''' Use this class to create a persistent connection to a ServiceNow
        instance.
    '''
    # pylint: disable=R0913
    def __init__(self, hostname, username, password, timeout=60, api='JSONv2'):
        self.timeout = timeout
        self.api = api
        self.instance = 'https://%s.service-now.com/' % hostname
        self.session = SnowSession()
        self.session.auth = (username, password)

        # Enables sending logging messages to the local syslog server.
        self.log = logging.getLogger('ServiceNowRac')
        sysh = SysLogHandler()
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        sysh.setFormatter(formatter)
        self.log.addHandler(sysh)

    def get(self, table, sysparm):
        ''' Make a GET request to the instance. Return the JSON response
            which is an array of records or return None if there was an error.
        '''
        url = '%s%s.do?%s&%s' % (self.instance, table, self.api, sysparm)

        # Set proper headers
        headers = {'Accept': 'application/json'}

        response = self.session.get(url, headers=headers, timeout=self.timeout)

        try:
            response = response.json()
        except ValueError:
            self.log.error('get: Request Error: Request response is not Json')
            return None

        if 'error' in response:
            self.log.error('get: Request Error: %s', response['error'])
            return None
        else:
            if 'records' in response:
                return response['records']
            else:
                return response

    def post(self, table, sysparm, data):
        ''' Make a POST request to the instance. Return the JSON response
            or return None if there was an error in the request or in any
            record returned.
        '''
        url = '%s%s.do?%s&%s' % (self.instance, table, self.api, sysparm)

        response = self.session.post(url, data=json.dumps(data),
                                     timeout=self.timeout)

        try:
            response = response.json()
        except ValueError:
            self.log.error('post: Request Error: Request response is not Json')
            return None

        if 'records' in response:
            # Check every record returned to see if there is an error
            # message in the record. If one record has an error then
            # return None, otherwise return all the records
            for record in response['records']:
                if '__error' in record:
                    self.log.error('Record Error: %s',
                                   record['__error']['message'])
                    return None
            return response['records']
        else:
            if 'error' in response:
                self.log.error('post: Request Error: %s', response['error'])
            return None
