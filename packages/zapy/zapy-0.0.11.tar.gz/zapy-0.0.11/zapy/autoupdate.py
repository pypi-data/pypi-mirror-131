import json

class autoupdate():
    def __init__(self, API):
        self.API = API

    def autoupdateViewLatestVersionNumber(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/view/latestVersionNumber/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateViewIsLatestVersion(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/view/isLatestVersion/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateViewInstalledAddons(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/view/installedAddons/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateViewLocalAddons(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/view/localAddons/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateViewNewAddons(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/view/newAddons/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateViewUpdatedAddons(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/view/updatedAddons/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateViewMarketplaceAddons(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/view/marketplaceAddons/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateViewOptionAddonDirectories(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/view/optionAddonDirectories/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateViewOptionDayLastChecked(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/view/optionDayLastChecked/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateViewOptionDayLastInstallWarned(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/view/optionDayLastInstallWarned/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateViewOptionDayLastUpdateWarned(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/view/optionDayLastUpdateWarned/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateViewOptionDownloadDirectory(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/view/optionDownloadDirectory/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateViewOptionCheckAddonUpdates(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/view/optionCheckAddonUpdates/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateViewOptionCheckOnStart(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/view/optionCheckOnStart/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateViewOptionDownloadNewRelease(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/view/optionDownloadNewRelease/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateViewOptionInstallAddonUpdates(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/view/optionInstallAddonUpdates/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateViewOptionInstallScannerRules(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/view/optionInstallScannerRules/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateViewOptionReportAlphaAddons(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/view/optionReportAlphaAddons/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateViewOptionReportBetaAddons(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/view/optionReportBetaAddons/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateViewOptionReportReleaseAddons(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/view/optionReportReleaseAddons/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateActionDownloadLatestRelease(self):

        r = self.API.HTTP.get(
            f'{self.API.url}/JSON/autoupdate/action/downloadLatestRelease/',
        )

        #return r.json
        return json.loads(r.text)

    def autoupdateActionInstallAddon(self, **kwargs):

            params = {
                "id": kwargs.get("id")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/autoupdate/action/installAddon/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def autoupdateActionInstallLocalAddon(self, **kwargs):

            params = {
                "file": kwargs.get("file")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/autoupdate/action/installLocalAddon/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def autoupdateActionUninstallAddon(self, **kwargs):

            params = {
                "id": kwargs.get("id")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/autoupdate/action/uninstallAddon/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def autoupdateActionSetOptionCheckAddonUpdates(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/autoupdate/action/setOptionCheckAddonUpdates/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def autoupdateActionSetOptionCheckOnStart(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/autoupdate/action/setOptionCheckOnStart/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def autoupdateActionSetOptionDownloadNewRelease(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/autoupdate/action/setOptionDownloadNewRelease/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def autoupdateActionSetOptionInstallAddonUpdates(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/autoupdate/action/setOptionInstallAddonUpdates/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def autoupdateActionSetOptionInstallScannerRules(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/autoupdate/action/setOptionInstallScannerRules/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def autoupdateActionSetOptionReportAlphaAddons(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/autoupdate/action/setOptionReportAlphaAddons/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def autoupdateActionSetOptionReportBetaAddons(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/autoupdate/action/setOptionReportBetaAddons/',
                params=params
            )

            #return r.json
            return json.loads(r.text)

    def autoupdateActionSetOptionReportReleaseAddons(self, **kwargs):

            params = {
                "Boolean": kwargs.get("Boolean")
            }

            r = self.API.HTTP.get(
                f'{self.API.url}/JSON/autoupdate/action/setOptionReportReleaseAddons/',
                params=params
            )

            #return r.json
            return json.loads(r.text)
