#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import base64, json, urllib2

class SkytapClient(object):
    def __init__(self, skytap_authentication):
        self.url = skytap_authentication["url"]
        self.username = skytap_authentication["username"]
        self.password = skytap_authentication["password"]
        self.headers = [
            ('Accept' , 'application/json'),
            ('Authorization' , 'Basic %s' % self.encode_authentication(self.username, self.password))]

    @staticmethod
    def get_client(skytap_authentication):
        return SkytapClient(skytap_authentication)

    @staticmethod
    def encode_authentication(username, password):
        return base64.b64encode("%s:%s" % (username, password))

    def open_url(self, url, data=None, headers=None):
        open_director = urllib2.build_opener(urllib2.HTTPHandler)
        if headers is None:
            open_director.addheaders = self.headers
        else:
            open_director.addheaders = headers
        return open_director.open(url, data)

    def get_response_for_endpoint(self, endpoint, error_message, object_id=None):
        full_endpoint_url = "%s/%s" % (self.url, endpoint)
        if object_id is not None and object_id:
            full_endpoint_url = "%s/%s" % (full_endpoint_url, object_id)
        response = self.open_url(full_endpoint_url)
        if not response.getcode() == 200:
            raise Exception(error_message)
        return json.load(response)

    def skytap_userlist(self, variables):
        return self.get_response_for_endpoint("users", "Failed to retrieve user list.")
