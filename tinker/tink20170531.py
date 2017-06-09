__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = '©2017 Collective Acuity'

from labpack.platforms.localhost import localhostClient
localhost_client = localhostClient()
for attribute in dir(localhost_client.os):
    print(getattr(localhost_client.os, attribute), attribute)
    
from platform import uname

# for attribute in dir(uname()):
#     print(getattr(uname(), attribute), attribute)

local_os = uname()
print(local_os.release)