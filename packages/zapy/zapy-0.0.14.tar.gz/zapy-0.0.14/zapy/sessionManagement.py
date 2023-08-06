import json

class sessionManagement():
    def __init__(self, API):
        self.API = API

    def sessionManagementViewGetSupportedSessionManagementMethods(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/sessionManagement/view/getSupportedSessionManagementMethods/',
        )

        #return r.json
        return json.loads(r.text)

    def sessionManagementViewGetSessionManagementMethodConfigParams(self, **kwargs):

            params = {
                "methodName": kwargs.get("methodName")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/sessionManagement/view/getSessionManagementMethodConfigParams/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def sessionManagementViewGetSessionManagementMethod(self, **kwargs):

            params = {
                "contextId": kwargs.get("contextId")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/sessionManagement/view/getSessionManagementMethod/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def sessionManagementActionSetSessionManagementMethod(self, **kwargs):

            params = {
                "contextId": kwargs.get("contextId"),
"methodName": kwargs.get("methodName"),
"methodConfigParams": kwargs.get("methodConfigParams")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/sessionManagement/action/setSessionManagementMethod/',
                params=params
            )

            #return r.json
            return json.loads(r.text)
