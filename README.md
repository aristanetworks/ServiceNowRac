# Arista ServiceNow REST API Client

#### Table of Contents

1. [Overview] (#overview)
    * [Requirements] (#requirements)
2. [Installation] (#installation)
3. [Getting Started] (#getting-started)
    * [Example] (#example)
4. [Testing] (#testing)
5. [License] (#license)

# Overview

The ServiceNowRac package provides a python REST API client for communicating with a ServiceNow instance. 
The package contains the following classes:

* SnowClient - Use this class to create a persistent connection to a ServiceNow instance.
* SnowTable - Use this class to perform operations on existing tables.

## Requirements

* Tables in the ServiceNow instance need to allow web access for the user.
* Currently has only be tested on Centos7, should work on most Unix systems.

# Installation

XXX - Need to test the package builds and update this section

FOR NOW: To install the python scripts:

* Change directory to the top level directory.
* make clean
* python setup.py 

# Getting Started

Once the package has been installed you can run the following example to verify that everything has been installed properly.

## Example

Creating a connection to a ServiceNow instance and creating a record in the change_request table.

```
from ServiceNowRac.snow_client import SnowClient
from ServiceNowRac.snow_table import SnowTable

# ServiceNow Instance information
hostname = 'service_now_instance_hostname'
username = 'service_now_username'
password = 'service_now_password'

# Connect to Service Now
snow_server = SnowClient(hostname, username, password)
snow_chg_reqs = SnowTable('change_request', snow_server)

# Create the change request dict
data = {
    'approval'           : 'requested',
    'assigned_to'        : username,
    'category'           : 'Hardware',
    'comments'           : 'Created a change request',
    'description'        : 'Created a change request description',
    'impact'             : '3',
    'priority'           : '3',
    'reason'             : 'Network Requirements',
    'requested_by'       : username,
    'type'               : 'Routine',
}
records = snow_chg_reqs.insert(data)
assert len(records) == 1

# Verify that the change request record that prints out below was created
# on your ServiceNow instance.
print records[0]
```

# Testing

XXX None yet

# License

Copyright (c) 2016, Arista Networks, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Arista Networks nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ARISTA NETWORKS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
