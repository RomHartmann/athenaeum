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

    def deserialize(self, rep, url):
        """Parse and format each listing to elasticsearch format.

        :param rep: Beautiful Soup object containing the web content of the listing report.
        :type rep: bs4.element.Tag
        :return: ES formatted data.
        :rtype: dict
        """
        # import pdb; pdb.set_trace()
        listing_number = rep.find('div', attrs={"style": "top:122px;left:4px;width:124px;height:13px;"}).text
        bylaws = rep.find('div', attrs={"style": "top:816px;left:248px;width:210px;height:23px;"}).text
        es_data = {
            "id": f"msl_{listing_number}",
            "indexed_at": datetime.datetime.now(),
            "url": url,
            "source_name": "bcres.paragonrels.com",
            "source_person": rep.find('div', attrs={"style": "top:21px;left:147px;width:463px;height:27px;"}).text,
            "source_company": rep.find('div', attrs={"style": "top:45px;left:147px;width:463px;height:13px;"}).text,
            "source_webhost": "bcres",
            "listing_number": listing_number,
            "status": rep.find('div', attrs={"style": "top:109px;left:4px;width:105px;height:13px;"}).text,
            "construction": rep.find('div', attrs={"style": "top:396px;left:75px;width:286px;height:12px;"}).text,
            "street_address": rep.find('div', attrs={"style": "top:110px;left:134px;width:482px;height:17px;"}).text,
            "suburb": rep.find('div', attrs={"style": "top:126px;left:134px;width:481px;height:13px;"}).text,
            "suburb_area": rep.find('div', attrs={"style": "top:139px;left:134px;width:480px;height:13px;"}),
            "postal_code": rep.find('div', attrs={"style": "top:152px;left:132px;width:484px;height:13px;"}),
            "price": float(rep.find('div', attrs={"style": "top:129px;left:555px;width:146px;height:13px;"}).text.replace("$", "").replace(",", "")),
            "original_price": float(rep.find('div', attrs={"style": "top:171px;left:677px;width:88px;height:15px;"}).text.replace("$", "").replace(",", "")),
            "list_date": None,
            "days_on_market": None,
            "total_bedrooms": int(rep.find('div', attrs={"style": "top:203px;left:530px;width:51px;height:13px;"}).text or 0),
            "total_baths": int(rep.find('div', attrs={"style": "top:219px;left:530px;width:50px;height:13px;"}).text or 0),
            "Basement": int(rep.find('div', attrs={"style": "top:840px;left:258px;width:199px;height:25px;"}).text or 0),
            "total_square_foot": int(rep.find('div', attrs={"style": "top:840px;left:120px;width:50px;height:12px;"}).text or 0),
            "fireplaces": int(rep.find('div', attrs={"style": "top:480px;left:330px;width:30px;height:13px;"}).text or 0),
            "year_built": int(rep.find('div', attrs={"style": "top:187px;left:698px;width:39px;height:13px;"}).text or 0),
            "age": int(rep.find('div', attrs={"style": "top:203px;left:698px;width:65px;height:13px;"}).text or 0),
            "locker": rep.find('div', attrs={"style": "top:408px;left:603px;width:159px;height:12px;"}).text,
            "total_parking": int(rep.find('div', attrs={"style": "top:384px;left:432px;width:20px;height:12px;"}).text or 0),
            "strat_fee": float(rep.find('div', attrs={"style": "top:267px;left:530px;width:67px;height:13px;"}).text.replace("$", "").replace(",", "")),
            "gross_taxes": float(rep.find('div', attrs={"style": "top:235px;left:698px;width:65px;height:13px;"}).text.replace("$", "").replace(",", "")),
            "dwelling_type": rep.find('div', attrs={"style": "top:151px;left:4px;width:137px;height:15px;"}).text,
            "bylaw_restrictions": bylaws,
            "features": rep.find('div', attrs={"style": "top:591px;left:75px;width:689px;height:20px;"}).text,
            "amenities": rep.find('div', attrs={"style": "top:556px;left:3px;width:53px;height:15px;"}).text,
            "pets_allowed": False if "Pets Not Allowed" in bylaws else True,
            "rent_allowed": False if "Rentals Not Allowed" in bylaws else True,
            "description": rep.find('div', attrs={"style": "top:891px;left:4px;width:758px;height:75px;"}).text
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
                import pdb; pdb.set_trace()
                listing_url = listing  # TODO
                es_formatted_data = self.deserialize(listing_report, listing_url)
                es_data.append(es_formatted_data)

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

