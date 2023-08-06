import requests
import re
from pathlib import Path
import zapy

class API():
    def __init__(self, url, api_key):
        self.api_key = api_key
        self.url = url[:-1] if url.endswith('/') else url
        self.HTTP = requests.Session()
        self.HTTP.headers.update(
            {'X-ZAP-API-Key': self.api_key}
        )

        self.alert = zapy.alert.alert(self)
        self.acsrf = zapy.acsrf.acsrf(self)
        self.pscan = zapy.pscan.pscan(self)
        self.search = zapy.search.search(self)
        self.autoupdate = zapy.autoupdate.autoupdate(self)
        self.spider = zapy.spider.spider(self)
        self.core = zapy.core.core(self)
        self.params = zapy.params.params(self)
        self.ascan = zapy.ascan.ascan(self)
        self.context = zapy.context.context(self)
        self.httpSessions = zapy.httpSessions.httpSessions(self)
        self.Break = zapy.Break.Break(self)
        self.authentication = zapy.authentication.authentication(self)
        self.authorization = zapy.authorization.authorization(self)
        self.localProxies = zapy.localProxies.localProxies(self)
        self.ruleConfig = zapy.ruleConfig.ruleConfig(self)
        self.sessionManagement = zapy.sessionManagement.sessionManagement(self)
        self.users = zapy.users.users(self)
        self.forcedUser = zapy.forcedUser.forcedUser(self)
        self.script = zapy.script.script(self)
        self.stats = zapy.stats.stats(self)

    def close(self):
        self.HTTP.close()
    def read_key_from_fs():
        return re.search('<key>(\w+)</key>', open(f'{Path.home()}/.ZAP/config.xml').read())[1]
