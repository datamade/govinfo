import scrapelib
import pytz

class GovInfo(scrapelib.Scraper):
    BASE_URL = 'https://api.govinfo.gov'

    def __init__(self, *args, api_key='DEMO_KEY', **kwargs):
        super().__init__(*args, **kwargs)
        self.headers['X-Api-Key'] = api_key

    def collections(self):
        endpoint = '/collections'
        response = self.get(self.BASE_URL + endpoint)
        return response.json()

    def congressional_hearings(self, start_time):
        endpoint = '/collections/CHRG/{start_time}/'

        utc_start_time = start_time.astimezone(pytz.utc)
        start_time_str = utc_start_time.strftime('%Y-%m-%dT%H:%M:%SZ')

        endpoint = endpoint.format(start_time=start_time_str)

        for page in self._pages(endpoint):
            for package in page['packages']:
                response = self.get(package['packageLink')
                yield response.json()

    def _pages(self, endpoint):
        first_page_params = {'offset':  0,
                             'pageSize': 100}

        response = self.get(self.BASE_URL + endpoint,
                            params=first_page_params)
        data = response.json()

        yield data

        next_page = data['nextPage']
        while next_page:
            response = self.get(next_page)
            data = response.json()

            yield data

            next_page = data['nextPage']
        
