import json

class localProxies():
    def __init__(self, API):
        self.API = API

    def localProxiesViewAdditionalProxies(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/localProxies/view/additionalProxies/',
        )

        #return r.json
        return json.loads(r.text)

    def localProxiesActionAddAdditionalProxy(self, **kwargs):

            params = {
                "address": kwargs.get("address"),
"port": kwargs.get("port"),
"behindNat": kwargs.get("behindNat"),
"alwaysDecodeZip": kwargs.get("alwaysDecodeZip"),
"removeUnsupportedEncodings": kwargs.get("removeUnsupportedEncodings")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/localProxies/action/addAdditionalProxy/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def localProxiesActionRemoveAdditionalProxy(self, **kwargs):

            params = {
                "address": kwargs.get("address"),
"port": kwargs.get("port")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/localProxies/action/removeAdditionalProxy/',
                params=params
            )

            #return r.json
            return json.loads(r.text)
