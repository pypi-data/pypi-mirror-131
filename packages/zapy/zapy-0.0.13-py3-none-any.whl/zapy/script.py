import json

class script():
    def __init__(self, API):
        self.API = API

    def scriptViewListEngines(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/script/view/listEngines/',
        )

        #return r.json
        return json.loads(r.text)

    def scriptViewListTypes(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/script/view/listTypes/',
        )

        #return r.json
        return json.loads(r.text)

    def scriptViewListScripts(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/script/view/listScripts/',
        )

        #return r.json
        return json.loads(r.text)

    def scriptViewGlobalVar(self, **kwargs):

            params = {
                "varKey": kwargs.get("varKey")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/script/view/globalVar/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def scriptViewGlobalVars(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/script/view/globalVars/',
        )

        #return r.json
        return json.loads(r.text)

    def scriptViewScriptVar(self, **kwargs):

            params = {
                "scriptName": kwargs.get("scriptName"),
"varKey": kwargs.get("varKey")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/script/view/scriptVar/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def scriptViewScriptVars(self, **kwargs):

            params = {
                "scriptName": kwargs.get("scriptName")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/script/view/scriptVars/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def scriptActionEnable(self, **kwargs):

            params = {
                "scriptName": kwargs.get("scriptName")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/script/action/enable/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def scriptActionDisable(self, **kwargs):

            params = {
                "scriptName": kwargs.get("scriptName")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/script/action/disable/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def scriptActionLoad(self, **kwargs):

            params = {
                "scriptName": kwargs.get("scriptName"),
"scriptType": kwargs.get("scriptType"),
"scriptEngine": kwargs.get("scriptEngine"),
"fileName": kwargs.get("fileName"),
"scriptDescription": kwargs.get("scriptDescription"),
"charset": kwargs.get("charset")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/script/action/load/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def scriptActionRemove(self, **kwargs):

            params = {
                "scriptName": kwargs.get("scriptName")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/script/action/remove/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def scriptActionRunStandAloneScript(self, **kwargs):

            params = {
                "scriptName": kwargs.get("scriptName")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/script/action/runStandAloneScript/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def scriptActionClearGlobalVar(self, **kwargs):

            params = {
                "varKey": kwargs.get("varKey")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/script/action/clearGlobalVar/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def scriptActionClearGlobalVars(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/script/action/clearGlobalVars/',
        )

        #return r.json
        return json.loads(r.text)

    def scriptActionClearScriptVar(self, **kwargs):

            params = {
                "scriptName": kwargs.get("scriptName"),
"varKey": kwargs.get("varKey")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/script/action/clearScriptVar/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def scriptActionClearScriptVars(self, **kwargs):

            params = {
                "scriptName": kwargs.get("scriptName")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/script/action/clearScriptVars/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def scriptActionSetScriptVar(self, **kwargs):

            params = {
                "scriptName": kwargs.get("scriptName"),
"varKey": kwargs.get("varKey"),
"varValue": kwargs.get("varValue")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/script/action/setScriptVar/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def scriptActionSetGlobalVar(self, **kwargs):

            params = {
                "varKey": kwargs.get("varKey"),
"varValue": kwargs.get("varValue")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/script/action/setGlobalVar/',
                params=params
            )

            #return r.json
            return json.loads(r.text)
