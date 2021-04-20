from globalmaptiles import GlobalMercator
from gwm_point import GlobalWebMercatorPoint
from typing import Tuple


class GlobalWebMercatorBox:
    """ Transforms a bbox from BNG to GWM, and calculates the closest zoom level and required tiles """

    # Takes in a BNG bbox (left, bottom, right, top) and image size (width, height)
    def __init__(self, bng_bbox: list, image_size: Tuple[int, int]):
        self.bng_res = (bng_bbox[2] - bng_bbox[0]) / image_size[0]
        self.bng_bbox = bng_bbox
        self.bng_map_size = image_size

        # Calculate corners BL, TL, TR, BR
        self.bng_vertices = [(bng_bbox[0], bng_bbox[1]),
                             (bng_bbox[0], bng_bbox[3]),
                             (bng_bbox[2], bng_bbox[3]),
                             (bng_bbox[2], bng_bbox[1])]

        self.gwm_vertices = []
        for vertice in self.bng_vertices:
            self.gwm_vertices.append(GlobalWebMercatorPoint.reproject_bng_to_gwm(vertice))

        gwm_x = [gwm[0] for gwm in self.gwm_vertices]
        gwm_y = [gwm[1] for gwm in self.gwm_vertices]
        gwm_bbox = (min(gwm_x), min(gwm_y), max(gwm_x), max(gwm_y))

        # Use the GlobalMercator class to calculate the optimal zoom level to use
        gwm = GlobalMercator()
        self.gwm_zoom = gwm.ZoomForPixelSize(self.bng_res)
        self.gwm_res = gwm.Resolution(self.gwm_zoom)

        # Calculate the Tile min/max values (Tiles go top -> bottom)
        self.start_x, self.start_y = gwm.MetersToTile(gwm_bbox[0], gwm_bbox[3], self.gwm_zoom)
        self.end_x, self.end_y = gwm.MetersToTile(gwm_bbox[2], gwm_bbox[1], self.gwm_zoom)

    def get_bng_resolution(self):
        return self.bng_res

    def get_gwm_resolution(self):
        return self.gwm_res

    def get_gwm_zoom_level(self):
        return self.gwm_zoom
