import json

class params():
    def __init__(self, API):
        self.API = API

    def paramsViewParams(self, **kwargs):

            params = {
                "site": kwargs.get("site")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/params/view/params/',
                params=params
            )

            #return r.json
            return json.loads(r.text)
