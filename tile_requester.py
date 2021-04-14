from abc import ABC, abstractmethod


class TileRequester(ABC):
    """ Abstract Base Class for requesting Tiles """
    @abstractmethod
    def request_tile(self, z: int, x: int, y: int) -> str:
        """ Return the url for the given tile """
        pass


class OSMTileRequester(TileRequester):
    """ Implementation of TileRequester for OpenStreetMap """
    # Template Url for OpenStreet Map Tiles
    TEMPLATE_URL = "https://{server}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    # Tile Servers to use
    SERVERS = ['a', 'b', 'c']

    def __init__(self):
        # initialise the current server
        self.server = 0

    def request_tile(self, z: int, x: int, y: int) -> str:
        # create dict to populate template
        d = {"server": self.SERVERS[self.server], "z": z, "x": x, "y": y}
        # populate template
        url = self.TEMPLATE_URL.format(**d)
        # increment the server for round-robin requests
        self.server = (self.server + 1) % len(self.SERVERS)
        # return the url
        return url
