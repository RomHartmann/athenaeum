"""Parsers that scrape online sources and load them into ES format."""
import logging
import datetime
import requests
import re
import os

from bs4 import BeautifulSoup

from . import BaseParser


# TODO
class ScraperParser(BaseParser):
    """Scrape a given site and parser for elasticsearch."""

    def __init__(self, url):
        """Scrape url.

        :param url: The url we want to scrape for listings.
        :type url: str
        """
        super().__init__()
        self.url = url

    def deserialize(self, *args, **kwargs):
        raise NotImplementedError

    def run(self, *args, **kwargs):
        raise NotImplementedError


class BcresParser(ScraperParser):
    """Scrape listings from https://bcres.paragonrels.com."""

    def __init__(self, url):
        """Scrape url.

        :param url: The url we want to scrape for listings.
        :type url: str
        """
        super().__init__(url)

    def deserialize(self, page):
        """Parse and format each listing to elasticsearch format.

        :param page: Beautiful Soup object containing the web content of the report.
        :type page: bs4.element.Tag
        :return: ES formatted data.
        :rtype: dict
        """
        es_data = {
            "id": f"",
            "indexed_at": datetime.datetime.now(),
            "url": "",
            "source_name": "bcres.paragonrels.com",
            "source_person": "Miguel Faulkner",
            "source_company": "Rennie",
            "source_webhost": "bcres",
            "listing_number": csv_item.get("ML #"),
            "status": csv_item.get("Status"),
            "street_address": csv_item.get("Address"),
            "suburb": csv_item.get("SUB/AREA"),
            "price": float(csv_item.get("Price").replace("$", "").replace(",", "")),
            "list_date": datetime.datetime.strptime(csv_item.get("List Date"), "%m/%d/%Y"),
            "days_on_market": int(csv_item.get("DOM") or 0),
            "total_bedrooms": int(csv_item.get("Tot BR") or 0),
            "total_baths": int(csv_item.get("Tot Baths") or 0),
            "total_square_foot": int(csv_item.get("TotFlArea") or 0),
            "year_built": int(csv_item.get("Yr Blt") or 0),
            "age": int(csv_item.get("Age") or 0),
            "locker": locker,
            "total_parking": int(csv_item.get("TotalPrkng") or 0),
            "strat_fee": float(csv_item.get("StratMtFee").replace("$", "").replace(",", "")),
            "dwelling_type": csv_item.get("TypeDwel"),
            "bylaw_restrictions": csv_item.get("Bylaw Restrictions"),
            "pets_allowed": False if "PETN" in csv_item.get("Bylaw Restrictions") else True,
            "rent_allowed": False if "RENN" in csv_item.get("Bylaw Restrictions") else True
        }

        if self.validate_schema:
            self.do_validate_schema(es_data)

        return es_data

    def run(self):
        """Load page and format all entries for ES.

        :return: Elasticsearch formatted payload containing all listings.
        :rtype: list of dict
        """
        es_data = []
        with self.headless_render_page(self.url) as browser:
            listings = self.get_list_of_listings(self.url)
            for listing in listings:
                listing_report = self.render_listing(browser, listing)
                # es_data.append(self.deserialize(listing_report))

        browser.quit()  # TODO make sure this happens
        return es_data

    @staticmethod
    def get_list_of_listings(url):
        """Given original URL, navigate page and fetch list of listing objects.

        :param url: The page url.
        :type url: str
        :return: A list of all listings.
        :rtype: list of bs4.element.Tag
        """
        logging.info(f"Fetching outer page from '{url}")
        outer_res = requests.get(url)
        outer_soup = BeautifulSoup(outer_res.content, 'html.parser')

        listings_src_frame = outer_soup.find('frame', attrs={'name': 'left'})
        listings_src = listings_src_frame.attrs['src']
        logging.info(f"listings source: '{listings_src}'")

        parsed_outer_url = '/'.join(url.split('/')[0:-1])
        parsed_listings_src = f"{parsed_outer_url}/{listings_src}"
        logging.info(f"Fetching frame page from '{parsed_listings_src}'")

        logging.info("Fetching inner frame for listings")
        inner_resp = requests.get(parsed_listings_src)
        inner_soup = BeautifulSoup(inner_resp.content, 'html.parser')

        listings = inner_soup.findAll("tr", {"id": re.compile(r'Row\d.*')})
        logging.info(f"Found {len(listings)} listings")

        return listings

    @staticmethod
    def render_listing(browser, listing):
        """Render a listing via navigating iframes and fetching data.

        :param browser: The selenium headless browser
        :type browser: selenium.webdriver.chrome.webdriver.WebDriver
        :param listing: The navigator to the report we want.
        :type listing: bs4.element.Tag
        :return: Beautiful Soup of the listing report.
        :rtype: bs4.element.Tag
        """
        listing_id = listing.attrs['id']
        logging.debug(f"Rendering row id '{listing_id}'")

        left_frame = browser.find_element_by_xpath('//frame[@name="left"]')
        browser.switch_to.frame(left_frame)

        click_script = listing.select('a')[0].attrs['onclick']
        browser.execute_script(click_script)

        browser.switch_to.default_content()
        main_frame = browser.find_element_by_xpath('//frame[@name="fraDetail"]')
        browser.switch_to.frame(main_frame)
        listing_content_raw = browser.page_source
        listing_soup = BeautifulSoup(listing_content_raw, 'html.parser')
        listing_report = listing_soup.find(id="divHtmlReport")

        return listing_report

    @staticmethod
    def headless_render_page(url):
        """Headlessly render the page such that we can load iframes and do clicky things.

        :param url: URL to render.
        :type url: str
        :return: Selenium browser.
        :rtype: selenium.webdriver.chrome.webdriver.WebDriver
        """
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        options = Options()
        # options.headless = True  # TODO
        chromedriver_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "drivers",
            "chromedriver"
        )

        browser = webdriver.Chrome(chromedriver_path, chrome_options=options)
        browser.get(url)

        return browser

