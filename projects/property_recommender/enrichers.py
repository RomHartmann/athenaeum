"""These are methods used to enrich the existing data for better recommendations."""
import logging


class BaseEnricher:
    """Base class for ability to enrich text."""

    def __init__(self):
        pass

    def run(self, *args, **kwargs):
        raise NotImplementedError


class ReverseGeolocationEnricher(BaseEnricher):
    """Given street address, reverse geolocate to get latlong."""

    def __init__(self):
        super().__init__()

    def run(self, street_address):
        """Convert street address to latlong.

        :param street_address: The street address to reverse geocode.
        :type street_address: str
        :return: The latlong in format "lat,long"
        :rtype: str
        """
        pass  # TODO


class ImageEnricher(BaseEnricher):
    """Run all images through some google image processing."""

    def __init__(self):
        super().__init__()

    def run(self, image_path):
        """

        :param image_path: Path of image to process.
        :type image_path: str
        :return: Text explaining what is in the image.
        :rtype: str  # TODO?
        """
        pass  # TODO
