import scrapelib
import pytz
import datetime

class GovInfo(scrapelib.Scraper):
    BASE_URL = 'https://api.govinfo.gov'

    def __init__(self, *args, api_key='DEMO_KEY', **kwargs):
        super().__init__(*args, **kwargs)
        self.headers['X-Api-Key'] = api_key

    def collections(self):
        endpoint = '/collections'
        response = self.get(self.BASE_URL + endpoint)
        return response.json()


    def _format_path(self, path, start_time, end_time):

        utc_start_time = start_time.astimezone(pytz.utc)
        start_time_str = utc_start_time.strftime('%Y-%m-%dT%H:%M:%SZ')

        utc_end_time = end_time.astimezone(pytz.utc)
        end_time_str = utc_end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

        path = path.format(start_time=start_time_str,
                           end_time=end_time_str)

        return path


    def _bisect(self, endpoint, start_time, end_time):
        '''
        The govinfo API will only allow you to access 10000 elements from
        an endpoint. This method takes the requested start and end
        range and breaks the range into multiple smaller ranges that
        each have less than 10000 elements. By visiting all the
        smaller ranges you will be able to get all the data.
        '''

        if end_time is None:
            end_time = datetime.datetime.now(pytz.utc)

        url = self.BASE_URL + self._format_path(endpoint,
                                                start_time,
                                                end_time)
        first_page_params = {'offset':  0,
                             'pageSize': 100}

        response = self.get(url, params=first_page_params)

        count = response.json()['count']

        if count < 10000:
            if count: # skip ranges that don't have any elements
                yield url
        else:
            duration = end_time - start_time
            midpoint = start_time + (duration / 2)
            yield from self._bisect(endpoint, start_time, midpoint)
            yield from self._bisect(endpoint, midpoint, end_time)


    def congressional_hearings(self, start_time=None, end_time=None):
        endpoint = '/collections/CHRG/{start_time}/{end_time}/'

        if start_time is None:
            if end_time is not None:
                raise ValueError('if end_time is set so must start_time')

        sections = self._bisect(endpoint, start_time, end_time)

        for url in sections:
            for page in self._pages(url):
                for package in page['packages']:
                    response = self.get(package['packageLink'])
                    yield response.json()


    def _pages(self, url):
        first_page_params = {'offset':  0,
                             'pageSize': 100}

        response = self.get(url,
                            params=first_page_params)
        data = response.json()

        yield data

        next_page = data['nextPage']
        while next_page:
            response = self.get(next_page)
            data = response.json()

            yield data

            next_page = data['nextPage']
        
