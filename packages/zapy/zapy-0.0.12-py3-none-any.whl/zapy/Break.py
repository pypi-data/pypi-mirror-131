import json

class Break():
    def __init__(self, API):
        self.API = API

    def breakViewIsBreakAll(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/break/view/isBreakAll/',
        )

        #return r.json
        return json.loads(r.text)

    def breakViewIsBreakRequest(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/break/view/isBreakRequest/',
        )

        #return r.json
        return json.loads(r.text)

    def breakViewIsBreakResponse(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/break/view/isBreakResponse/',
        )

        #return r.json
        return json.loads(r.text)

    def breakViewHttpMessage(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/break/view/httpMessage/',
        )

        #return r.json
        return json.loads(r.text)

    def breakActionBreak(self, **kwargs):

            params = {
                "type": kwargs.get("type"),
"state": kwargs.get("state"),
"scope": kwargs.get("scope")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/break/action/break/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def breakActionSetHttpMessage(self, **kwargs):

            params = {
                "httpHeader": kwargs.get("httpHeader"),
"httpBody": kwargs.get("httpBody")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/break/action/setHttpMessage/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def breakActionContinue(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/break/action/continue/',
        )

        #return r.json
        return json.loads(r.text)

    def breakActionStep(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/break/action/step/',
        )

        #return r.json
        return json.loads(r.text)

    def breakActionDrop(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/break/action/drop/',
        )

        #return r.json
        return json.loads(r.text)

    def breakActionAddHttpBreakpoint(self, **kwargs):

            params = {
                "string": kwargs.get("string"),
"location": kwargs.get("location"),
"match": kwargs.get("match"),
"inverse": kwargs.get("inverse"),
"ignorecase": kwargs.get("ignorecase")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/break/action/addHttpBreakpoint/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def breakActionRemoveHttpBreakpoint(self, **kwargs):

            params = {
                "string": kwargs.get("string"),
"location": kwargs.get("location"),
"match": kwargs.get("match"),
"inverse": kwargs.get("inverse"),
"ignorecase": kwargs.get("ignorecase")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/break/action/removeHttpBreakpoint/',
                params=params
            )

            #return r.json
            return json.loads(r.text)
