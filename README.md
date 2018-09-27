# GovInfo
A Python wrapper for the govinfo API.

You'll need an API key from https://api.data.gov/

## Example
```python
import datetime

import govinfo
import pytz

scraper = govinfo.GovInfo(api_key='YOUR_SECRET_API_KEY')

# Prints out all the different types of collections available
# in the govinfo API
print(scraper.collections())

# Iterate through every congressional hearing
#
# For congressional hearings you need a specify a start
# date time with a timezone
start_time = datetime.datetime(1990, 1, 1, 0, 0, tzinfo=pytz.utc)

for hearing in scraper.congressional_hearings(start_time):
    print(hearing)
```