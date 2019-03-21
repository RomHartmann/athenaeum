"""Parsers that load up CSVs from different formats and load them into ES format."""
import logging
import datetime
import csv
import os

from . import BaseParser


class CsvParser(BaseParser):
    """Parses CSVs and serialize them for elasticsearch indexer."""

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

        self.data = self.load_csv()

    def load_csv(self):
        """Load csv into memory.

        :return: The csv as python list of dicts.
        :rtype: csv.DictReader
        """
        # TODO use generator?
        logging.info(f"Loading up CSV from {os.path.abspath(self.file_path)}")
        with open(self.file_path, 'r') as f:
            reader = csv.DictReader(f)
            data = [d for d in reader]

        logging.info(f"Loaded up {len(data)} rows from csv.")

        return data

    def deserialize(self, csv_item):
        """Format each loaded csv row to elasticsearch format.

        :param csv_item: Raw parsed csv.
        :type csv_item: DictReader
        :return: ES formatted data.
        :rtype: dict
        """
        raise NotImplementedError

    def run(self):
        raise NotImplementedError


class MlsParser(CsvParser):
    """Parse CSVs from MSL source."""

    def __init__(self, file_path):
        """Load up a CSV from MSL source.

        :param file_path: The path to the csv file.
        :type file_path: str
        """
        super().__init__(file_path)

    def deserialize(self, csv_item):
        """Format each loaded csv row to elasticsearch format.

        :param csv_item: Raw parsed csv.
        :type csv_item: DictReader
        :return: ES formatted data.
        :rtype: dict
        """
        if not csv_item.get("Locker"):
            locker = None
        elif csv_item.get("Locker").lower() == 'y':
            locker = True
        else:
            locker = False

        es_data = {
            "id": f"msl_{csv_item.get('ML #')}",
            "indexed_at": datetime.datetime.now(),
            "source_name": "MSL",
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
        """Load up CSV and format it for Elasticsearch.

        :return: Elasticsearch formatted payload containing all CSV rows.
        :rtype: list of dict
        """
        # TODO use generators
        es_data = []
        for csv_item in self.data:
            es_data.append(self.deserialize(csv_item))

        logging.info("Finished parsing csv rows")

        return es_data
