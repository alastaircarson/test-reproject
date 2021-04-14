from PIL import Image
import requests
from tile_requester import TileRequester


class TileMosaic:
    """ Class to make a tile mosaic """
    TILE_SIZE = 256

    def __init__(self, tile_requester: TileRequester, zoom: int, start_x: int, end_x: int, start_y: int, end_y: int):
        self.tile_requester = tile_requester
        self.zoom = zoom
        self.start_x = start_x
        self.end_x = end_x
        self.start_y = start_y
        self.end_y = end_y

        w = end_x - start_x + 1
        h = end_y - start_y + 1
        self.image = Image.new("RGB", (w * self.TILE_SIZE, h * self.TILE_SIZE))

        for x in range(0, w):
            for y in range(0, h):
                tile_url = self._request_tile(zoom, start_x + x, start_y + y)
                tile = Image.open(requests.get(tile_url, stream=True).raw)
                self.image.paste(tile, (x * self.TILE_SIZE, y * self.TILE_SIZE))

    def image(self):
        return self.image

    def save(self, filename: str):
        self.image.save(filename)

    def _request_tile(self, zoom: int, x: int, y: int):
        return self.tile_requester.request_tile(zoom, x, y)
