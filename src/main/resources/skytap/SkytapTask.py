#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from skytap.Skytap import SkytapClient

skytap = SkytapClient.get_client(skytap_authentication)
method = str(task.getTaskType()).lower().replace('.', '_')
call = getattr(skytap, method)
output = call(locals())