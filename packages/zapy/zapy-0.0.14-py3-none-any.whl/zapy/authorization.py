import json

class authorization():
    def __init__(self, API):
        self.API = API

    def authorizationViewGetAuthorizationDetectionMethod(self, **kwargs):

            params = {
                "contextId": kwargs.get("contextId")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/authorization/view/getAuthorizationDetectionMethod/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def authorizationActionSetBasicAuthorizationDetectionMethod(self, **kwargs):

            params = {
                "contextId": kwargs.get("contextId"),
"headerRegex": kwargs.get("headerRegex"),
"bodyRegex": kwargs.get("bodyRegex"),
"statusCode": kwargs.get("statusCode"),
"logicalOperator": kwargs.get("logicalOperator")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/authorization/action/setBasicAuthorizationDetectionMethod/',
                params=params
            )

            #return r.json
            return json.loads(r.text)
