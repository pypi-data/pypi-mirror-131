# python-ote

Electricity prices scraper for OTE (ote-cr.cz)

## Install

```
pip install python-ote
```

## Usage

```
from ote import Ote
from dateutil import parser

# Create client
ote = Ote()
```

Use `getDayMarketPrices(date_from, date_to)` method to get electricity prices
for the given time range. It accepts a `date_from` and optionally a `date_to`,
both of which have to be a [datetime.date](https://docs.python.org/3/library/datetime.html#datetime.date)
object. If `date_to` is not specified the method returns data to today.

```
# Get water consumption data from the specified date to now
date_from = parser.parse('2020-08-01').date()
data = ote.getDayMarketPrices(date_from);

# Get water consumption data for a date interval
date_from = parser.parse('2020-08-01').date()
date_to = parser.parse('2020-08-11').date()
data = ote.getDayMarketPrices(date_from, date_to);

# Get water consumption data for a specific date (just 1 day)
date = parser.parse('2020-08-01').date()
data = ote.getDayMarketPrices(date, date);
```

Keep in mind the library is using [Scrapy](https://scrapy.org) internally which
means it is scraping the OTE website. If OTE comes to think you are abusing the
website they may block your IP address.


# License

See [LICENSE](./LICENSE).
