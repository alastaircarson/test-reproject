from transform import PositionTransform, SamplePointTransform, Scale, HorizontalFlip, Shift, Rotation
import math
from PIL import Image
from tile_mosaic import TileMosaic
from tile_requester import OSMTileRequester
from globalmaptiles import GlobalMercator


def main():
    # Code to open an image, and apply a transform
    # open the image
    # image = Image.open("Ally.jpg")
    # w = image.width
    # h = image.height
    # print((w, h))
    # Create a transformation to apply to the image
    # shift = Shift(-w/2, -h/2)
    # rotate = Rotation(math.pi/2)
    # scale = Scale(2)
    # shift2 = Shift(h/2, w/2)
    # combined = PositionTransform()
    # combined = combined.combine(shift)
    # combined = combined.combine(rotate)
    # combined = combined.combine(scale)
    # combined = combined.combine(shift2)
    # inverse the transformation (to apply it)
    # t = combined.inverse()

    # Image.transform(size, method, data=None, resample=0, fill=1, fillcolor=None)
    # img2 = image.transform((h, w), Image.AFFINE, _get_image_transform(t))
    # img2.save("Test.jpg")

    # Code to create a mosaic 4x4 tile world map at level 2
    # tm = TileMosaic(OSMTileRequester(), 2, 0, 3, 0, 3)
    # tm.save("world2.png")

    # Sample coordinates to avoid caring about the transformation just now
    bng_coords = [(300000, 600000), (300000, 601000), (301000, 601000), (301000, 600000)]
    gwm_coords = [(-398075.709110655, 7417169.44503078), (-398115.346383602, 7418925.37709793),
                  (-396363.034574031, 7418964.91393662), (-396323.792660911, 7417208.95976453)]

    bng_x = [bng[0] for bng in bng_coords]
    bng_y = [bng[1] for bng in bng_coords]
    bng_box = (min(bng_x), min(bng_y), max(bng_x), max(bng_y))

    gwm_x = [gwm[0] for gwm in gwm_coords]
    gwm_y = [gwm[1] for gwm in gwm_coords]
    gwm_box = (min(gwm_x), min(gwm_y), max(gwm_x), max(gwm_y))

    # If the coords above relate to a 400x400 map, calculate the resolution
    bng_map_size = 600
    bng_res = (bng_box[2] - bng_box[0]) / bng_map_size
    print(bng_res)

    # Use the GlobalMercator class to calculate the optimal zoom level to use
    gwm = GlobalMercator()
    gwm_zoom = gwm.ZoomForPixelSize(bng_res)
    print(gwm_zoom)

    # Calculate the min/max tile x and y for the given area at the calculates zoom level
    tiles_x = []
    tiles_y = []
    for coord in gwm_coords:
        tx, ty = gwm.MetersToTile(coord[0], coord[1], gwm_zoom)
        tiles_x.append(tx)
        tiles_y.append(ty)
        print(f"{gwm_zoom} {tx} {ty}")
        # print(OSMTileRequester().request_tile(gwm_zoom, tx, ty))

    # Create a mosaic image from these tiles
    start_x = min(tiles_x)
    end_x = max(tiles_x)
    start_y = min(tiles_y)
    end_y = max(tiles_y)
    gwm_mosaic = TileMosaic(OSMTileRequester(), gwm_zoom, start_x, end_x, start_y, end_y)
    gwm_mosaic.save("mosaic.png")

    # Get the bbox for these tiles
    gwm_mosaic_box_tl = gwm.TileBounds(start_x, start_y, gwm_zoom)
    gwm_mosaic_box_tr = gwm.TileBounds(end_x, start_y, gwm_zoom)
    gwm_mosaic_box_bl = gwm.TileBounds(start_x, end_y, gwm_zoom)
    gwm_mosaic_box_br = gwm.TileBounds(end_x, end_y, gwm_zoom)
    gwm_mosaic_box = (
        min(gwm_mosaic_box_tl[0], gwm_mosaic_box_bl[0]),
        min(gwm_mosaic_box_bl[3], gwm_mosaic_box_br[3]),
        max(gwm_mosaic_box_tr[2], gwm_mosaic_box_br[2]),
        max(gwm_mosaic_box_tl[1], gwm_mosaic_box_tr[1]))

    print(gwm_mosaic_box)

    test = [(0, 0), (400, 0), (400, 400), (0, 400)]

    # Create a transformation to convert pixels of the target BNG image to the GWM mosaic image
    bng_img_to_gwm_image = PositionTransform()
    # Translate/scale image px to BNG
    bng_img_to_gwm_image = bng_img_to_gwm_image.combine(HorizontalFlip())
    bng_img_to_gwm_image = bng_img_to_gwm_image.combine(Scale(bng_res))
    bng_img_to_gwm_image = bng_img_to_gwm_image.combine(Shift(bng_box[0], bng_box[3]))
    test_coords(test, bng_img_to_gwm_image)

    # Transform BNG to GWM coords
    bng_gwm_transform = SamplePointTransform(bng_coords[0], bng_coords[1], bng_coords[2],
                                             gwm_coords[0], gwm_coords[1], gwm_coords[2])
    bng_img_to_gwm_image = bng_img_to_gwm_image.combine(bng_gwm_transform)
    test_coords(test, bng_img_to_gwm_image)

    # Translate/scale GWM coords to GWM mosaic image coords
    bng_img_to_gwm_image = bng_img_to_gwm_image.combine(Shift(-gwm_mosaic_box[0], -gwm_mosaic_box[3]))
    bng_img_to_gwm_image = bng_img_to_gwm_image.combine(Scale(1/gwm.Resolution(gwm_zoom)))
    bng_img_to_gwm_image = bng_img_to_gwm_image.combine(HorizontalFlip())

    test_coords(test, bng_img_to_gwm_image)

    bng_result = gwm_mosaic.image.transform(
        (bng_map_size, bng_map_size),
        Image.AFFINE,
        _get_image_transform(bng_img_to_gwm_image))

    bng_result.save("BNG.jpg")


def test_coords(coords, pt):
    for coord in coords:
        out = pt.transform(coord)
        print(f"{coord[0]}, {coord[1]} -> {out[0]}, {out[1]}")


def _get_image_transform(pt):
    """ Get the PIL transform tuple from a 3x3 matrix """
    return pt.matrix[0][0], pt.matrix[1][0], pt.matrix[2][0], pt.matrix[0][1], pt.matrix[1][1], pt.matrix[2][1]


if __name__ == "__main__":
    main()
