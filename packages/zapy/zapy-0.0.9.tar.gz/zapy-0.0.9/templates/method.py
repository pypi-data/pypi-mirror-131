    def {{ METHOD_NAME }}(self, **kwargs):

            params = {
                {{ PARAMETERS_LIST }}
            }

            r = self.API.HTTP.get(
                f'{self.API.url}{{ API_PATH }}',
                params=params
            )

            #return r.json
            return json.loads(r.text)
