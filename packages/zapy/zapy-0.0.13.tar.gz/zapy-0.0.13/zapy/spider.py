import json

class spider():
    def __init__(self, API):
        self.API = API

    def spiderViewStatus(self, **kwargs):

            params = {
                "scanId": kwargs.get("scanId")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/view/status/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderViewResults(self, **kwargs):

            params = {
                "scanId": kwargs.get("scanId")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/view/results/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderViewFullResults(self, **kwargs):

            params = {
                "scanId": kwargs.get("scanId")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/view/fullResults/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderViewScans(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/scans/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewExcludedFromScan(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/excludedFromScan/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewAllUrls(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/allUrls/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewAddedNodes(self, **kwargs):

            params = {
                "scanId": kwargs.get("scanId")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/view/addedNodes/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderViewDomainsAlwaysInScope(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/domainsAlwaysInScope/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionDomainsAlwaysInScope(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionDomainsAlwaysInScope/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionDomainsAlwaysInScopeEnabled(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionDomainsAlwaysInScopeEnabled/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionHandleParameters(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionHandleParameters/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionMaxChildren(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionMaxChildren/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionMaxDepth(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionMaxDepth/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionMaxDuration(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionMaxDuration/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionMaxParseSizeBytes(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionMaxParseSizeBytes/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionMaxScansInUI(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionMaxScansInUI/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionRequestWaitTime(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionRequestWaitTime/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionScope(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionScope/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionScopeText(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionScopeText/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionSkipURLString(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionSkipURLString/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionThreadCount(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionThreadCount/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionUserAgent(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionUserAgent/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionAcceptCookies(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionAcceptCookies/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionHandleODataParametersVisited(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionHandleODataParametersVisited/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionParseComments(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionParseComments/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionParseGit(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionParseGit/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionParseRobotsTxt(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionParseRobotsTxt/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionParseSVNEntries(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionParseSVNEntries/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionParseSitemapXml(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionParseSitemapXml/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionPostForm(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionPostForm/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionProcessForm(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionProcessForm/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionSendRefererHeader(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionSendRefererHeader/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderViewOptionShowAdvancedDialog(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/view/optionShowAdvancedDialog/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderActionScan(self, **kwargs):

            params = {
                "url": kwargs.get("url"),
"maxChildren": kwargs.get("maxChildren"),
"recurse": kwargs.get("recurse"),
"contextName": kwargs.get("contextName"),
"subtreeOnly": kwargs.get("subtreeOnly")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/scan/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionScanAsUser(self, **kwargs):

            params = {
                "contextId": kwargs.get("contextId"),
"userId": kwargs.get("userId"),
"url": kwargs.get("url"),
"maxChildren": kwargs.get("maxChildren"),
"recurse": kwargs.get("recurse"),
"subtreeOnly": kwargs.get("subtreeOnly")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/scanAsUser/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionPause(self, **kwargs):

            params = {
                "scanId": kwargs.get("scanId")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/pause/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionResume(self, **kwargs):

            params = {
                "scanId": kwargs.get("scanId")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/resume/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionStop(self, **kwargs):

            params = {
                "scanId": kwargs.get("scanId")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/stop/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionRemoveScan(self, **kwargs):

            params = {
                "scanId": kwargs.get("scanId")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/removeScan/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionPauseAllScans(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/action/pauseAllScans/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderActionResumeAllScans(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/action/resumeAllScans/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderActionStopAllScans(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/action/stopAllScans/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderActionRemoveAllScans(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/action/removeAllScans/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderActionClearExcludedFromScan(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/action/clearExcludedFromScan/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderActionExcludeFromScan(self, **kwargs):

            params = {
                "regex": kwargs.get("regex")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/excludeFromScan/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionAddDomainAlwaysInScope(self, **kwargs):

            params = {
                "value": kwargs.get("value"),
"isRegex": kwargs.get("isRegex"),
"isEnabled": kwargs.get("isEnabled")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/addDomainAlwaysInScope/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionModifyDomainAlwaysInScope(self, **kwargs):

            params = {
                "idx": kwargs.get("idx"),
"value": kwargs.get("value"),
"isRegex": kwargs.get("isRegex"),
"isEnabled": kwargs.get("isEnabled")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/modifyDomainAlwaysInScope/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionRemoveDomainAlwaysInScope(self, **kwargs):

            params = {
                "idx": kwargs.get("idx")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/removeDomainAlwaysInScope/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionEnableAllDomainsAlwaysInScope(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/action/enableAllDomainsAlwaysInScope/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderActionDisableAllDomainsAlwaysInScope(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/spider/action/disableAllDomainsAlwaysInScope/',
        )

        #return r.json
        return json.loads(r.text)

    def spiderActionSetOptionHandleParameters(self, **kwargs):

            params = {
                "String": kwargs.get("String")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionHandleParameters/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionScopeString(self, **kwargs):

            params = {
                "String": kwargs.get("String")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionScopeString/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionSkipURLString(self, **kwargs):

            params = {
                "String": kwargs.get("String")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionSkipURLString/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionUserAgent(self, **kwargs):

            params = {
                "String": kwargs.get("String")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionUserAgent/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionAcceptCookies(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionAcceptCookies/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionHandleODataParametersVisited(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionHandleODataParametersVisited/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionMaxChildren(self, **kwargs):

            params = {
                "Integer": kwargs.get("Integer")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionMaxChildren/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionMaxDepth(self, **kwargs):

            params = {
                "Integer": kwargs.get("Integer")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionMaxDepth/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionMaxDuration(self, **kwargs):

            params = {
                "Integer": kwargs.get("Integer")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionMaxDuration/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionMaxParseSizeBytes(self, **kwargs):

            params = {
                "Integer": kwargs.get("Integer")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionMaxParseSizeBytes/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionMaxScansInUI(self, **kwargs):

            params = {
                "Integer": kwargs.get("Integer")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionMaxScansInUI/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionParseComments(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionParseComments/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionParseGit(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionParseGit/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionParseRobotsTxt(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionParseRobotsTxt/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionParseSVNEntries(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionParseSVNEntries/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionParseSitemapXml(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionParseSitemapXml/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionPostForm(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionPostForm/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionProcessForm(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionProcessForm/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionRequestWaitTime(self, **kwargs):

            params = {
                "Integer": kwargs.get("Integer")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionRequestWaitTime/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionSendRefererHeader(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionSendRefererHeader/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionShowAdvancedDialog(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionShowAdvancedDialog/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def spiderActionSetOptionThreadCount(self, **kwargs):

            params = {
                "Integer": kwargs.get("Integer")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/spider/action/setOptionThreadCount/',
                params=params
            )

            #return r.json
            return json.loads(r.text)
