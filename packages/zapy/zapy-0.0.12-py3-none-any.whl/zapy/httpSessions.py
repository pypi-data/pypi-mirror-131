import json

class httpSessions():
    def __init__(self, API):
        self.API = API

    def httpSessionsViewSites(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/httpSessions/view/sites/',
        )

        #return r.json
        return json.loads(r.text)

    def httpSessionsViewSessions(self, **kwargs):

            params = {
                "site": kwargs.get("site"),
"session": kwargs.get("session")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/httpSessions/view/sessions/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def httpSessionsViewActiveSession(self, **kwargs):

            params = {
                "site": kwargs.get("site")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/httpSessions/view/activeSession/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def httpSessionsViewSessionTokens(self, **kwargs):

            params = {
                "site": kwargs.get("site")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/httpSessions/view/sessionTokens/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def httpSessionsViewDefaultSessionTokens(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/httpSessions/view/defaultSessionTokens/',
        )

        #return r.json
        return json.loads(r.text)

    def httpSessionsActionCreateEmptySession(self, **kwargs):

            params = {
                "site": kwargs.get("site"),
"session": kwargs.get("session")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/httpSessions/action/createEmptySession/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def httpSessionsActionRemoveSession(self, **kwargs):

            params = {
                "site": kwargs.get("site"),
"session": kwargs.get("session")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/httpSessions/action/removeSession/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def httpSessionsActionSetActiveSession(self, **kwargs):

            params = {
                "site": kwargs.get("site"),
"session": kwargs.get("session")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/httpSessions/action/setActiveSession/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def httpSessionsActionUnsetActiveSession(self, **kwargs):

            params = {
                "site": kwargs.get("site")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/httpSessions/action/unsetActiveSession/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def httpSessionsActionAddSessionToken(self, **kwargs):

            params = {
                "site": kwargs.get("site"),
"sessionToken": kwargs.get("sessionToken")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/httpSessions/action/addSessionToken/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def httpSessionsActionRemoveSessionToken(self, **kwargs):

            params = {
                "site": kwargs.get("site"),
"sessionToken": kwargs.get("sessionToken")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/httpSessions/action/removeSessionToken/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def httpSessionsActionSetSessionTokenValue(self, **kwargs):

            params = {
                "site": kwargs.get("site"),
"session": kwargs.get("session"),
"sessionToken": kwargs.get("sessionToken"),
"tokenValue": kwargs.get("tokenValue")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/httpSessions/action/setSessionTokenValue/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def httpSessionsActionRenameSession(self, **kwargs):

            params = {
                "site": kwargs.get("site"),
"oldSessionName": kwargs.get("oldSessionName"),
"newSessionName": kwargs.get("newSessionName")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/httpSessions/action/renameSession/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def httpSessionsActionAddDefaultSessionToken(self, **kwargs):

            params = {
                "sessionToken": kwargs.get("sessionToken"),
"tokenEnabled": kwargs.get("tokenEnabled")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/httpSessions/action/addDefaultSessionToken/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def httpSessionsActionSetDefaultSessionTokenEnabled(self, **kwargs):

            params = {
                "sessionToken": kwargs.get("sessionToken"),
"tokenEnabled": kwargs.get("tokenEnabled")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/httpSessions/action/setDefaultSessionTokenEnabled/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def httpSessionsActionRemoveDefaultSessionToken(self, **kwargs):

            params = {
                "sessionToken": kwargs.get("sessionToken")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/httpSessions/action/removeDefaultSessionToken/',
                params=params
            )

            #return r.json
            return json.loads(r.text)
