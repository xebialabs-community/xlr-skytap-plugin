#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import ast, base64, json, requests, time

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

    def skytap_startenvironment(self, variables):
        if self.environment_runstate(variables, "running"):
            return
        while self.environment_runstate(variables, "busy"):
            time.sleep(5)
        data = '{"runstate": "running"}'
        return self.get_response_for_endpoint("PUT", "configurations/%s.json" % variables['environment_id'], "Failed to start environment [%s]." % variables['environment_id'], data=data)

    def skytap_stopenvironment(self, variables):
        if self.environment_runstate(variables, "stopped"):
            return
        while self.environment_runstate(variables, "busy"):
            time.sleep(10)
        data = '{"runstate": "stopped"}'
        stop_json = json.loads(self.get_response_for_endpoint("PUT", "configurations/%s.json" % variables['environment_id'], "Failed to stop environment [%s]." % variables['environment_id'], data=data))
        error = stop_json['error']
        print "error : %s\n" % error
        if error != "":
            print "retrying stop."
            if variables['retry_on_failure']:
                while True:
                    print "retry...\n"
                    time.sleep(10)
                    stop_json = json.loads(self.get_response_for_endpoint("PUT", "configurations/%s.json" % variables['environment_id'], "Failed to stop environment [%s]." % variables['environment_id'], data=data))
                    error = stop_json['error']
                    if error == "":
                        break
            else:
                raise Exception(error)
        return json.dumps(stop_json)

    def skytap_waitforrunningenvironment(self, variables):
        while True:
            if self.environment_runstate(variables, "running"):
                break
            time.sleep(10)
        return self.skytap_getenvironment(variables)

    def skytap_waitforstoppedenvironment(self, variables):
        while True:
            if self.environment_runstate(variables, "stopped"):
                break
            time.sleep(10)
        return self.skytap_getenvironment(variables)

    def skytap_assetlist(self, variables):
        return self.get_response_for_endpoint("GET", "assets", "Failed to retrieve asset list.")

    def skytap_createproject(self, variables):
        data = '{"name":"%s"}' % variables['project_name']
        return self.get_response_for_endpoint("POST", "projects.json", "Failed to create project [%s]." % variables['project_name'], data=data)

    def skytap_createenvironment(self, variables):
        data = '{"template_id":"%s"' % variables['template_id']
        if variables['project_id'] is not None and ['project_id']:
            data += ', "project_id":"%s"' % variables['project_id']
        data += '}'
        return self.get_response_for_endpoint("POST", "configurations.json", "Failed to create environment with template [%s]." % variables['template_id'], data=data)

    def skytap_deleteproject(self, variables):
        return self.get_response_for_endpoint("DELETE", "projects", "Failed to delete project [%s]." % variables['project_id'], object_id=variables['project_id'])

    def skytap_deleteenvironment(self, variables):
        return self.get_response_for_endpoint("DELETE", "configurations", "Failed to delete environment [%s]." % variables['environment_id'], object_id=variables['environment_id'])

    def skytap_addtemplatetoproject(self, variables):
        return self.get_response_for_endpoint("POST", "projects/%s/templates/%s   " % (variables['project_id'], variables['template_id']), "Failed to add template [%s] to project [%s]." % (variables['template_id'], variables['project_id']))

    def skytap_addenvironmenttoproject(self, variables):
        return self.get_response_for_endpoint("POST", "projects/%s/configurations/%s   " % (variables['project_id'], variables['environment_id']), "Failed to add environment [%s] to project [%s]." % (variables['environment_id'], variables['project_id']))

    def environment_runstate(self, variables, runstate):
        print "passed runstate : %s" % runstate
        print "actual runstate : %s" %json.loads(self.skytap_getenvironment(variables))['runstate']
        return json.loads(self.skytap_getenvironment(variables))['runstate'] == runstate