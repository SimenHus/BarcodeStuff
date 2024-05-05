import requests

class DatabaseInterface:
    APIKey = 'rvDA9kSGD8d0EPk4pP9ow3z4KJ6Ihc6vGP433qWl'

    def fetch(self, ean):
        headers = {'Authorization': f'Bearer {self.APIKey}'}
        r = requests.get(f'https://kassal.app/api/v1/products/ean/{ean}', headers=headers)

        return r.json()
