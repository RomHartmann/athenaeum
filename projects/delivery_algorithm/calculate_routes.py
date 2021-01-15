""""""


class Location:

    def __init__(self, address):
        self.address = address
        self.lat, self.long = self.reverse_geocode(address)

    @staticmethod
    def reverse_geocode(address):
        """Get the latlong from the given address

        :param address:
        :type address:
        :return:
        :rtype:
        """
        return []


class Driver:

    def __init__(self, capacity):
        self.capacity = capacity


def calculate_routes(sources, destinations, drivers):
    """

    1) Cluster destinations around number of sources
    2) For each cluster, calculate best routes given number of drivers
    3) Output an ordered list of destinations for each driver
        - Or output actual route for driver? TODO talk to drivers
    4) ? Write source-destination pair to db?

    :param sources: Coordinates of sources
    :type sources:
    :param destinations: Coordinates of destinations
    :type destinations:
    :param drivers: Number of drivers available
    :type drivers: list of Driver
    :return:
    :rtype:
    """
    pass


def format_route_for_drivers(routes):
    """

    Enrich the route with delivery instructions (name, phone, buzzer etc)

    :param routes:
    :type routes:
    :return:
    :rtype:
    """








