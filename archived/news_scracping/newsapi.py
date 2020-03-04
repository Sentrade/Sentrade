#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from eventregistry import *

er = EventRegistry(apiKey=)

__author__ = "Davide Locatelli"
__status__ = "Prototype"

response = requests.get('https://newsapi.org/v2/everything?'
       'q=Apple&'
       'from=2019-06-01&'
       'to=2019-08-31&'
       'apiKey=954c05db19404ee99531875f66d9d138')

print (response.json())