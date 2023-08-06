    def {{ METHOD_NAME }}(self):

        r = self.API.HTTP.get(
            f'{self.API.url}{{ API_PATH }}',
        )

        #return r.json
        return json.loads(r.text)
