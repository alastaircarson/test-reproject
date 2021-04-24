from PIL import Image
import requests
from tile_requester import TileRequester
from globalmaptiles import GlobalMercator


class TileMosaic:
    """ Class to make a tile mosaic """
    TILE_SIZE = 256

    def __init__(self, tile_requester: TileRequester, zoom: int, start_x: int, end_x: int, start_y: int, end_y: int):
        gwm = GlobalMercator()
        self.tile_requester = tile_requester
        self.zoom = zoom
        self.start_x = start_x
        self.end_x = end_x
        self.start_y = start_y
        self.end_y = end_y

        w = end_x - start_x + 1
        h = end_y - start_y + 1
        self.image = Image.new("RGB", (w * self.TILE_SIZE, h * self.TILE_SIZE))

        first = True
        for x in range(0, w):
            for y in range(0, h):
                tile_url = self._request_tile(zoom, start_x + x, start_y + y)
                tile = Image.open(requests.get(tile_url, stream=True).raw)
                # tile.save(f"t{x}{y}.png")
                self.image.paste(tile, (x * self.TILE_SIZE, y * self.TILE_SIZE))
                tile_bbox = gwm.TileBounds(start_x + x, start_y + y, zoom)
                if first:
                    self.mosaic_bbox = [tile_bbox[0], tile_bbox[1], tile_bbox[2], tile_bbox[3]]
                    first = False
                else:
                    self.mosaic_bbox[0] = min(self.mosaic_bbox[0], tile_bbox[0])
                    self.mosaic_bbox[1] = min(self.mosaic_bbox[1], tile_bbox[1])
                    self.mosaic_bbox[2] = max(self.mosaic_bbox[2], tile_bbox[2])
                    self.mosaic_bbox[3] = max(self.mosaic_bbox[3], tile_bbox[3])

    def save(self, filename: str):
        self.image.save(filename)

    def _request_tile(self, zoom: int, x: int, y: int):
        return self.tile_requester.request_tile(zoom, x, y)
