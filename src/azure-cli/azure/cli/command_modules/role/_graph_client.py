# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import json

from azure.cli.core.util import send_raw_request
from azure.cli.core.auth.util import resource_to_scopes


class GraphClient:
    def __init__(self, cli_ctx):
        self.cli_ctx = cli_ctx
        self.scopes = resource_to_scopes(cli_ctx.cloud.endpoints.microsoft_graph_resource_id)

        # https://graph.microsoft.com/ (AzureCloud)
        self.resource = cli_ctx.cloud.endpoints.microsoft_graph_resource_id

        # https://graph.microsoft.com/v1.0
        self.base_url = cli_ctx.cloud.endpoints.microsoft_graph_resource_id + 'v1.0'

    def _send(self, method, url, param=None, body=None):
        url = self.base_url + url

        if body:
            body = json.dumps(body)

        list_result = []
        is_list_result = False

        while True:
            r = send_raw_request(self.cli_ctx, method, url, resource=self.resource, uri_parameters=param, body=body)
            if r.text:
                dic = r.json()

                # The result is a list. Add value to list_result.
                if 'value' in dic:
                    is_list_result = True
                    list_result.extend(dic['value'])

                # Follow nextLink if available
                if '@odata.nextLink' in dic:
                    url = dic['@odata.nextLink']
                    continue

                # Result a list
                if is_list_result:
                    # 'value' can be empty list [], so we can't determine if the result is a list only by
                    # bool(list_result)
                    return list_result

                # Return a single object
                return r.json()
            else:
                return None

    # id is python built-in name: https://docs.python.org/3/library/functions.html#id
    # filter is python built-in name: https://docs.python.org/3/library/functions.html#filter

    def application_create(self, body):
        # https://docs.microsoft.com/en-us/graph/api/application-post-applications
        result = self._send("POST", "/applications", body=body)
        return result

    def application_get(self, id):
        # https://docs.microsoft.com/en-us/graph/api/application-get
        result = self._send("GET", "/applications/{id}".format(id=id))
        return result

    def application_list(self, filter=None):
        # https://docs.microsoft.com/en-us/graph/api/application-list
        result = self._send("GET", "/applications?$filter={}".format(filter))
        return result

    def application_delete(self, id):
        # https://docs.microsoft.com/en-us/graph/api/application-delete
        result = self._send("DELETE", "/applications/{id}".format(id=id))
        return result

    def application_patch(self, id, body):
        # https://docs.microsoft.com/en-us/graph/api/application-update
        result = self._send("PATCH", "/applications/{id}".format(id=id), body=body)
        return result

    def application_owner_add(self, id, body):
        # https://docs.microsoft.com/en-us/graph/api/application-post-owners
        result = self._send("POST", "/applications/{id}/owners/$ref".format(id=id), body=body)
        return result

    def application_owner_list(self, id):
        # https://docs.microsoft.com/en-us/graph/api/application-list-owners
        result = self._send("GET", "/applications/{id}/owners".format(id=id))
        return result

    def application_owner_remove(self, id):
        # https://docs.microsoft.com/en-us/graph/api/application-delete-owners
        result = self._send("DELETE", "/applications/{id}/owners/{id}/$ref".format(id=id))
        return result

    def application_password_create(self, id):
        # https://docs.microsoft.com/en-us/graph/api/application-addpassword
        result = self._send("POST", "/applications/{id}/addPassword".format(id=id))
        return result

    def application_password_delete(self, id):
        # https://docs.microsoft.com/en-us/graph/api/application-addpassword
        result = self._send("POST", "/applications/{id}/removePassword".format(id=id))
        return result

    def service_principal_create(self, body):
        # https://docs.microsoft.com/en-us/graph/api/serviceprincipal-post-serviceprincipals
        result = self._send("POST", "/servicePrincipals", body=body)
        return result

    def service_principal_get(self, id):
        # https://docs.microsoft.com/en-us/graph/api/application-get
        result = self._send("GET", "/servicePrincipals/{id}".format(id=id))
        return result

    def service_principal_list(self, filter=None):
        # https://docs.microsoft.com/en-us/graph/api/application-list
        result = self._send("GET", "/servicePrincipals?$filter={}".format(filter))
        return result

    def service_principal_delete(self, id):
        # https://docs.microsoft.com/en-us/graph/api/application-delete
        result = self._send("DELETE", "/servicePrincipals/{id}".format(id=id))
        return result

    def service_principal_owner_list(self, id):
        # https://docs.microsoft.com/en-us/graph/api/serviceprincipal-list-owners
        result = self._send("GET", "/servicePrincipals/{id}/owners".format(id=id))
        return result

    def owned_objects_list(self):
        # https://docs.microsoft.com/en-us/graph/api/user-list-ownedobjects
        result = self._send("GET", "/me/ownedObjects")
        return result

    def signed_in_user_get(self):
        # https://docs.microsoft.com/en-us/graph/api/user-get
        result = self._send("GET", "/me")
        return result

    def directory_object_get_by_ids(self, body):
        # https://docs.microsoft.com/en-us/graph/api/directoryobject-getbyids
        result = self._send("POST", "/directoryObjects/getByIds", body=body)
        return result
