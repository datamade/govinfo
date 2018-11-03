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


    def congressional_hearings(self, start_time, end_time=None):
        endpoint = '/collections/CHRG/{start_time}/{end_time}'

        if start_time is None:
            if end_time is not None:
                raise ValueError('if end_time is set so must start_time')

        if end_time is None:
            end_time = datetime.datetime.now(pytz.utc)

        url = self.BASE_URL + self._format_path(endpoint, start_time, end_time)

        # we may need to check for duplicates here
        for page in self._pages(url):
            for package in page['packages']:
                response = self.get(package['packageLink'])
                yield response.json()


    def _pages(self, url):
        page_size = 100

        first_page_params = {'offset':  0,
                             'pageSize': page_size}

        response = self.get(url,
                            params=first_page_params)
        data = response.json()

        yield data

        url_template = url.lsplit('/', 1)[0] + '/{end_time}'

        while len(data['packages']) == page_size:
            # the API results are sorted in descending order by timestamp
            # so we can paginate through results by making the end_time
            # filter earlier and earlier
            earliest_timestamp = data['packages'][-1]['lastModified']
            url =  url_template.format(end_time=earliest_timestamp)

            response = self.get(url,
                                params=first_page_params)
            data = response.json()

            yield data
