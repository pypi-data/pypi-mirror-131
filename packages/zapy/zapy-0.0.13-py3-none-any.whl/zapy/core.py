import json

class core():
    def __init__(self, API):
        self.API = API

    def coreViewHosts(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/hosts/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewSites(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/sites/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewUrls(self, **kwargs):

            params = {
                "baseurl": kwargs.get("baseurl")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/view/urls/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreViewChildNodes(self, **kwargs):

            params = {
                "url": kwargs.get("url")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/view/childNodes/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreViewMessage(self, **kwargs):

            params = {
                "id": kwargs.get("id")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/view/message/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreViewMessages(self, **kwargs):

            params = {
                "baseurl": kwargs.get("baseurl"),
"start": kwargs.get("start"),
"count": kwargs.get("count")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/view/messages/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreViewMessagesById(self, **kwargs):

            params = {
                "ids": kwargs.get("ids")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/view/messagesById/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreViewNumberOfMessages(self, **kwargs):

            params = {
                "baseurl": kwargs.get("baseurl")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/view/numberOfMessages/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreViewMode(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/mode/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewVersion(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/version/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewExcludedFromProxy(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/excludedFromProxy/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewHomeDirectory(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/homeDirectory/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewSessionLocation(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/sessionLocation/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewProxyChainExcludedDomains(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/proxyChainExcludedDomains/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewOptionProxyChainSkipName(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/optionProxyChainSkipName/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewOptionProxyExcludedDomains(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/optionProxyExcludedDomains/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewOptionProxyExcludedDomainsEnabled(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/optionProxyExcludedDomainsEnabled/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewZapHomePath(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/zapHomePath/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewOptionMaximumAlertInstances(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/optionMaximumAlertInstances/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewOptionMergeRelatedAlerts(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/optionMergeRelatedAlerts/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewOptionAlertOverridesFilePath(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/optionAlertOverridesFilePath/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewAlert(self, **kwargs):

            params = {
                "id": kwargs.get("id")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/view/alert/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreViewAlerts(self, **kwargs):

            params = {
                "baseurl": kwargs.get("baseurl"),
"start": kwargs.get("start"),
"count": kwargs.get("count"),
"riskId": kwargs.get("riskId")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/view/alerts/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreViewAlertsSummary(self, **kwargs):

            params = {
                "baseurl": kwargs.get("baseurl")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/view/alertsSummary/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreViewNumberOfAlerts(self, **kwargs):

            params = {
                "baseurl": kwargs.get("baseurl"),
"riskId": kwargs.get("riskId")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/view/numberOfAlerts/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreViewOptionDefaultUserAgent(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/optionDefaultUserAgent/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewOptionDnsTtlSuccessfulQueries(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/optionDnsTtlSuccessfulQueries/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewOptionHttpState(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/optionHttpState/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewOptionProxyChainName(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/optionProxyChainName/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewOptionProxyChainPassword(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/optionProxyChainPassword/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewOptionProxyChainPort(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/optionProxyChainPort/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewOptionProxyChainRealm(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/optionProxyChainRealm/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewOptionProxyChainUserName(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/optionProxyChainUserName/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewOptionTimeoutInSecs(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/optionTimeoutInSecs/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewOptionHttpStateEnabled(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/optionHttpStateEnabled/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewOptionProxyChainPrompt(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/optionProxyChainPrompt/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewOptionSingleCookieRequestHeader(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/optionSingleCookieRequestHeader/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewOptionUseProxyChain(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/optionUseProxyChain/',
        )

        #return r.json
        return json.loads(r.text)

    def coreViewOptionUseProxyChainAuth(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/view/optionUseProxyChainAuth/',
        )

        #return r.json
        return json.loads(r.text)

    def coreActionAccessUrl(self, **kwargs):

            params = {
                "url": kwargs.get("url"),
"followRedirects": kwargs.get("followRedirects")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/accessUrl/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionShutdown(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/action/shutdown/',
        )

        #return r.json
        return json.loads(r.text)

    def coreActionNewSession(self, **kwargs):

            params = {
                "name": kwargs.get("name"),
"overwrite": kwargs.get("overwrite")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/newSession/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionLoadSession(self, **kwargs):

            params = {
                "name": kwargs.get("name")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/loadSession/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionSaveSession(self, **kwargs):

            params = {
                "name": kwargs.get("name"),
"overwrite": kwargs.get("overwrite")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/saveSession/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionSnapshotSession(self, **kwargs):

            params = {
                "name": kwargs.get("name"),
"overwrite": kwargs.get("overwrite")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/snapshotSession/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionClearExcludedFromProxy(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/action/clearExcludedFromProxy/',
        )

        #return r.json
        return json.loads(r.text)

    def coreActionExcludeFromProxy(self, **kwargs):

            params = {
                "regex": kwargs.get("regex")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/excludeFromProxy/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionSetHomeDirectory(self, **kwargs):

            params = {
                "dir": kwargs.get("dir")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/setHomeDirectory/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionSetMode(self, **kwargs):

            params = {
                "mode": kwargs.get("mode")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/setMode/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionGenerateRootCA(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/action/generateRootCA/',
        )

        #return r.json
        return json.loads(r.text)

    def coreActionSendRequest(self, **kwargs):

            params = {
                "request": kwargs.get("request"),
"followRedirects": kwargs.get("followRedirects")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/sendRequest/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionRunGarbageCollection(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/action/runGarbageCollection/',
        )

        #return r.json
        return json.loads(r.text)

    def coreActionDeleteSiteNode(self, **kwargs):

            params = {
                "url": kwargs.get("url"),
"method": kwargs.get("method"),
"postData": kwargs.get("postData")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/deleteSiteNode/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionAddProxyChainExcludedDomain(self, **kwargs):

            params = {
                "value": kwargs.get("value"),
"isRegex": kwargs.get("isRegex"),
"isEnabled": kwargs.get("isEnabled")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/addProxyChainExcludedDomain/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionModifyProxyChainExcludedDomain(self, **kwargs):

            params = {
                "idx": kwargs.get("idx"),
"value": kwargs.get("value"),
"isRegex": kwargs.get("isRegex"),
"isEnabled": kwargs.get("isEnabled")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/modifyProxyChainExcludedDomain/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionRemoveProxyChainExcludedDomain(self, **kwargs):

            params = {
                "idx": kwargs.get("idx")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/removeProxyChainExcludedDomain/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionEnableAllProxyChainExcludedDomains(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/action/enableAllProxyChainExcludedDomains/',
        )

        #return r.json
        return json.loads(r.text)

    def coreActionDisableAllProxyChainExcludedDomains(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/action/disableAllProxyChainExcludedDomains/',
        )

        #return r.json
        return json.loads(r.text)

    def coreActionSetOptionMaximumAlertInstances(self, **kwargs):

            params = {
                "numberOfInstances": kwargs.get("numberOfInstances")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/setOptionMaximumAlertInstances/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionSetOptionMergeRelatedAlerts(self, **kwargs):

            params = {
                "enabled": kwargs.get("enabled")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/setOptionMergeRelatedAlerts/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionSetOptionAlertOverridesFilePath(self, **kwargs):

            params = {
                "filePath": kwargs.get("filePath")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/setOptionAlertOverridesFilePath/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionEnablePKCS12ClientCertificate(self, **kwargs):

            params = {
                "filePath": kwargs.get("filePath"),
"password": kwargs.get("password"),
"index": kwargs.get("index")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/enablePKCS12ClientCertificate/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionDisableClientCertificate(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/action/disableClientCertificate/',
        )

        #return r.json
        return json.loads(r.text)

    def coreActionDeleteAllAlerts(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/core/action/deleteAllAlerts/',
        )

        #return r.json
        return json.loads(r.text)

    def coreActionDeleteAlert(self, **kwargs):

            params = {
                "id": kwargs.get("id")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/deleteAlert/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionSetOptionDefaultUserAgent(self, **kwargs):

            params = {
                "String": kwargs.get("String")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/setOptionDefaultUserAgent/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionSetOptionProxyChainName(self, **kwargs):

            params = {
                "String": kwargs.get("String")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/setOptionProxyChainName/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionSetOptionProxyChainPassword(self, **kwargs):

            params = {
                "String": kwargs.get("String")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/setOptionProxyChainPassword/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionSetOptionProxyChainRealm(self, **kwargs):

            params = {
                "String": kwargs.get("String")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/setOptionProxyChainRealm/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionSetOptionProxyChainSkipName(self, **kwargs):

            params = {
                "String": kwargs.get("String")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/setOptionProxyChainSkipName/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionSetOptionProxyChainUserName(self, **kwargs):

            params = {
                "String": kwargs.get("String")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/setOptionProxyChainUserName/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionSetOptionDnsTtlSuccessfulQueries(self, **kwargs):

            params = {
                "Integer": kwargs.get("Integer")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/setOptionDnsTtlSuccessfulQueries/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionSetOptionHttpStateEnabled(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/setOptionHttpStateEnabled/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionSetOptionProxyChainPort(self, **kwargs):

            params = {
                "Integer": kwargs.get("Integer")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/setOptionProxyChainPort/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionSetOptionProxyChainPrompt(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/setOptionProxyChainPrompt/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionSetOptionSingleCookieRequestHeader(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/setOptionSingleCookieRequestHeader/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionSetOptionTimeoutInSecs(self, **kwargs):

            params = {
                "Integer": kwargs.get("Integer")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/setOptionTimeoutInSecs/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionSetOptionUseProxyChain(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/setOptionUseProxyChain/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreActionSetOptionUseProxyChainAuth(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/core/action/setOptionUseProxyChainAuth/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreOtherProxyPac(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/OTHER/core/other/proxy.pac/',
        )

        #return r.json
        return json.loads(r.text)

    def coreOtherRootcert(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/OTHER/core/other/rootcert/',
        )

        #return r.json
        return json.loads(r.text)

    def coreOtherSetproxy(self, **kwargs):

            params = {
                "proxy": kwargs.get("proxy")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/OTHER/core/other/setproxy/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreOtherXmlreport(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/OTHER/core/other/xmlreport/',
        )

        #return r.json
        return json.loads(r.text)

    def coreOtherHtmlreport(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/OTHER/core/other/htmlreport/',
        )

        #return r.json
        return json.loads(r.text)

    def coreOtherJsonreport(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/OTHER/core/other/jsonreport/',
        )

        #return r.json
        return json.loads(r.text)

    def coreOtherMdreport(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/OTHER/core/other/mdreport/',
        )

        #return r.json
        return json.loads(r.text)

    def coreOtherMessageHar(self, **kwargs):

            params = {
                "id": kwargs.get("id")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/OTHER/core/other/messageHar/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreOtherMessagesHar(self, **kwargs):

            params = {
                "baseurl": kwargs.get("baseurl"),
"start": kwargs.get("start"),
"count": kwargs.get("count")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/OTHER/core/other/messagesHar/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreOtherMessagesHarById(self, **kwargs):

            params = {
                "ids": kwargs.get("ids")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/OTHER/core/other/messagesHarById/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def coreOtherSendHarRequest(self, **kwargs):

            params = {
                "request": kwargs.get("request"),
"followRedirects": kwargs.get("followRedirects")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/OTHER/core/other/sendHarRequest/',
                params=params
            )

            #return r.json
            return json.loads(r.text)
