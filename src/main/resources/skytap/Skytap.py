#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import base64, json, requests, time

class SkytapClient(object):
    def __init__(self, skytap_authentication):
        self.url = skytap_authentication["url"]
        self.username = skytap_authentication["username"]
        self.password = skytap_authentication["password"]
        self.headers = {
            'Accept' : 'application/json',
            'Authorization' : 'Basic %s' % self.encode_authentication(self.username, self.password),
            'Content-Type' : 'application/json'
        }

    @staticmethod
    def get_client(skytap_authentication):
        return SkytapClient(skytap_authentication)

    @staticmethod
    def encode_authentication(username, password):
        return base64.b64encode("%s:%s" % (username, password))

    def open_url(self, method, url, headers=None, data=None, json_data=None):
        if headers is None:
            headers = self.headers
        return requests.request('%s' % method, url, data=data, json=json_data, headers=headers, verify=False)

    def get_response_for_endpoint(self, method, endpoint, error_message, object_id=None, json_data=None, data=None, headers=None):
        full_endpoint_url = "%s/%s" % (self.url, endpoint)
        if object_id is not None and object_id:
            full_endpoint_url = "%s/%s" % (full_endpoint_url, object_id)
        response = self.open_url(method, full_endpoint_url, headers=headers, json_data=json_data, data=data)
        if not response.status_code == 200:
            raise Exception(error_message)
        return response.text

    def skytap_userlist(self, variables):
        return self.get_response_for_endpoint("GET", "users", "Failed to retrieve user list.")

    def skytap_projectlist(self, variables):
        return self.get_response_for_endpoint("GET", "projects", "Failed to retrieve project list.")

    def skytap_templatelist(self, variables):
        return self.get_response_for_endpoint("GET", "templates", "Failed to retrieve template list.")

    def skytap_environmentlist(self, variables):
        return self.get_response_for_endpoint("GET", "configurations", "Failed to retrieve environment list.")

    def skytap_getenvironment(self, variables):
        return self.get_response_for_endpoint("GET", "configurations", "Failed to retrieve environment [%s]." % variables['environment_id'], object_id=variables['environment_id'])

    def skytap_environmentvmlist(self, variables):
        json_data = json.loads(self.skytap_getenvironment(variables))
        return json.dumps(json_data['vms'])

    def skytap_assetlist(self, variables):
        return self.get_response_for_endpoint("GET", "assets", "Failed to retrieve asset list.")

    def skytap_startenvironment(self, variables):
        if self.environment_runstate(variables, "running"):
            return
        while self.environment_runstate(variables, "busy"):
            time.sleep(5)
        data = '{"runstate": "running"}'
        return self.get_response_for_endpoint("PUT", "configurations/%s.json" % variables['environment_id'], "Failed to start environment [%s]." % variables['environment_id'], data=data)

    def skytap_waitforrunningenvironment(self, variables):
        while True:
            if self.environment_runstate(variables, "running"):
                break
            time.sleep(10)
        return self.skytap_getenvironment(variables)

    def skytap_createproject(self, variables):
        data = '{"name":"%s"}' % variables['project_name']
        return self.perform_post_operation(endpoint="projects.json",
                                                error_message="Failed to create project [%s]." % variables['project_name'],
                                                data=data)

    def skytap_createenvironment(self, variables):
        data = '{"template_id":"%s"' % variables['template_id']
        if variables['project_id'] is not None and ['project_id']:
            data += ', "project_id":"%s"' % variables['project_id']
        data += '}'
        return self.perform_post_operation(endpoint="configurations.json",
                                                error_message="Failed to create environment with template [%s]." % variables['template_id'],
                                                data=data)

    def skytap_deleteproject(self, variables):
        return self.perform_delete_operation(endpoint="projects", object_id=variables['project_id'])

    def skytap_deleteenvironment(self, variables):
        return self.perform_delete_operation(endpoint="configurations", object_id=variables['environment_id'])

    def skytap_addtemplatetoproject(self, variables):
        return self.perform_add_to_project_operation("templates", variables['project_id'], variables['template_id'])

    def skytap_addenvironmenttoproject(self, variables):
        return self.perform_add_to_project_operation("configurations", variables['project_id'], variables['environment_id'])

    def perform_post_operation(self, endpoint, error_message, object_id=None, json_data=None, data=None, headers=None):
        return self.get_response_for_endpoint(
            method='POST',
            endpoint=endpoint,
            error_message=error_message,
            object_id=object_id,
            json_data=json_data,
            data=data,
            headers=headers)

    def perform_delete_operation(self, endpoint, object_id, json_data=None, data=None, headers=None):
        return self.get_response_for_endpoint(
            method='DELETE', endpoint=endpoint,
            error_message="Failed to delete %s [%s]." % (endpoint, object_id),
            object_id=object_id,
            json_data=json_data,
            data=data,
            headers=headers)

    def perform_add_to_project_operation(self, endpoint, project_id, object_id):
        full_endpoint="projects/%s/%s/%s" % (project_id, endpoint, object_id)
        self.perform_post_operation(endpoint=full_endpoint, error_message="Failed to add %s [%s] to project [%s]." % (endpoint, object_id, project_id))

    def environment_runstate(self, variables, runstate):
        return json.loads(self.skytap_getenvironment(variables))['runstate'] == runstate
