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
''' ServiceNow Table API
    Class containing ServiceNow Table API calls
'''

class SnowTable(object):
    ''' Use this class to perform operations on existing tables.
    '''

    def __init__(self, table, connection):
        self.table = table
        self.conn = connection

    def get(self, sys_id):
        ''' Query a single record from the targeted table by specifying the
            sys_id and return the record and its fields. If the query fails
            then None is returned otherwise the json response is returned.
        '''
        # A sysparm_action is optional for get
        sysparm = 'sysparm_sys_id=%s' % sys_id
        response = self.conn.get(self.table, sysparm)
        if response:
            return response[0]
        return None

    def get_keys(self, query):
        ''' Query the targeted table using an encoded query string and return
            a comma delimited list of sys_id values. If the query fails
            then None is returned otherwise the json response is returned.
        '''
        sysparm = 'sysparm_action=getKeys&sysparm_query=%s' % query
        return self.conn.get(self.table, sysparm)

    def get_records(self, query):
        ''' Query the targeted table using an encoded query string and return
            all matching records and their fields. If the query fails
            then None is returned otherwise the json response is returned.
        '''
        sysparm = 'sysparm_action=getRecords&sysparm_query=%s' % query
        return self.conn.get(self.table, sysparm)

    def insert(self, data):
        ''' Create one new record. If insertion fails then None is returned
            otherwise the json response is returned.
        '''
        sysparm = 'sysparm_action=insert'
        return self.conn.post(self.table, sysparm, data)

    def insert_multiple(self, data):
        ''' Create multiple new records. Format of payload should model
            { "records" : [ { ... }, { ... } ] }
        '''
        if not isinstance(data, list):
            raise TypeError('Invalid type. insert_multiple requires list of '
                            'records.')

        sysparm = 'sysparm_action=insertMultiple'
        records = {'records': data}
        return self.conn.post(self.table, sysparm, records)

    def update(self, data, query):
        ''' Update existing records filtered by the encoded query string.
        '''
        sysparm = 'sysparm_action=update&sysparm_query=%s' % query
        return self.conn.post(self.table, sysparm, data)

    def delete(self, sys_id):
        ''' Delete a record specifying its sys_id.
        '''
        sysparm = 'sysparm_action=deleteRecord'
        data = {'sysparm_sys_id' : sys_id}
        return self.conn.post(self.table, sysparm, data)

    def delete_multiple(self, query):
        ''' Delete multiple records filtered by an encoded query string.
        '''
        sysparm = 'sysparm_action=deleteMultiple'
        data = {'sysparm_query' : query}
        return self.conn.post(self.table, sysparm, data)
