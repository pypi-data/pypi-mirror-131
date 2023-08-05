from datetime import datetime

from twisted.internet import reactor
from scrapy.settings import Settings
from scrapy.crawler import CrawlerRunner

from .spiders.ote_electricity import DayMarketPricesSpider


class Ote:
    def __init__(self, log_enabled=None, log_level=None):
        # NOTE: We create settings "manually", not using
        # "scrapy.utils.project.get_project_settings" so we don't have to
        # bundle scrapy.cfg with the ote package.
        self._settings = Settings()
        self._settings.setmodule('ote.settings', priority='project')

        # Override settings if needed
        if log_enabled is not None:
            self._settings["LOG_ENABLED"] = log_enabled
        if log_level is not None:
            self._settings["LOG_LEVEL"] = log_level

    def getDayMarketPrices(self, date_from, date_to=None):
        """ Get electricity prices for the specified time period.  If `date_to`
            is not specified return consumption data from `date_from` till today.

            `date_from` and `date_to` must be datetime.date-compatible objects.
        """
        items = []

        def _item_scraped(item):
            items.append(item)

        runner = CrawlerRunner(self._settings)
        deferred = runner.crawl(
            DayMarketPricesSpider,
            date_from=date_from,
            date_to=date_to,
            cb_item_scraped=_item_scraped,
        )
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run(installSignalHandlers=False)  # the script will block here until the crawling is finished

        return {datetime.combine(item["date"], item["time"]).isoformat(): item["price"] for item in items}
