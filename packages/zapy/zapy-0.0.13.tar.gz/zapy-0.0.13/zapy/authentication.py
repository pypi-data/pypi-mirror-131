import json

class authentication():
    def __init__(self, API):
        self.API = API

    def authenticationViewGetSupportedAuthenticationMethods(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/authentication/view/getSupportedAuthenticationMethods/',
        )

        #return r.json
        return json.loads(r.text)

    def authenticationViewGetAuthenticationMethodConfigParams(self, **kwargs):

            params = {
                "authMethodName": kwargs.get("authMethodName")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/authentication/view/getAuthenticationMethodConfigParams/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def authenticationViewGetAuthenticationMethod(self, **kwargs):

            params = {
                "contextId": kwargs.get("contextId")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/authentication/view/getAuthenticationMethod/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def authenticationViewGetLoggedInIndicator(self, **kwargs):

            params = {
                "contextId": kwargs.get("contextId")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/authentication/view/getLoggedInIndicator/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def authenticationViewGetLoggedOutIndicator(self, **kwargs):

            params = {
                "contextId": kwargs.get("contextId")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/authentication/view/getLoggedOutIndicator/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def authenticationActionSetAuthenticationMethod(self, **kwargs):

            params = {
                "contextId": kwargs.get("contextId"),
"authMethodName": kwargs.get("authMethodName"),
"authMethodConfigParams": kwargs.get("authMethodConfigParams")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/authentication/action/setAuthenticationMethod/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def authenticationActionSetLoggedInIndicator(self, **kwargs):

            params = {
                "contextId": kwargs.get("contextId"),
"loggedInIndicatorRegex": kwargs.get("loggedInIndicatorRegex")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/authentication/action/setLoggedInIndicator/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def authenticationActionSetLoggedOutIndicator(self, **kwargs):

            params = {
                "contextId": kwargs.get("contextId"),
"loggedOutIndicatorRegex": kwargs.get("loggedOutIndicatorRegex")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/authentication/action/setLoggedOutIndicator/',
                params=params
            )

            #return r.json
            return json.loads(r.text)
