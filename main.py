from tile_mosaic import TileMosaic
from tile_requester import OSMTileRequester
from gwm_box import GlobalWebMercatorBox
from gwm_image_reprojection import GlobalWebMercatorImageReprojection


def main():
    # Sample coordinates to avoid caring about the transformation just now
    bng_bbox = [306000, 671000, 307000, 672000]
    bng_map_size = (600, 600)
    tile_requester = OSMTileRequester()

    print(bng_bbox)
    print(bng_map_size)

    gwm_box = GlobalWebMercatorBox(bng_bbox, bng_map_size)

    print(gwm_box.bng_res)
    print(gwm_box.gwm_res)
    print(gwm_box.gwm_zoom)
    print(f"{gwm_box.start_x} -> {gwm_box.end_x}")
    print(f"{gwm_box.start_y} -> {gwm_box.end_y}")

    gwm_mosaic = TileMosaic(tile_requester,
                            gwm_box.gwm_zoom,
                            gwm_box.start_x, gwm_box.end_x,
                            gwm_box.start_y, gwm_box.end_y)
    gwm_mosaic.save("mosaic.png")

    # Get the bbox for these tiles
    print(gwm_mosaic.mosaic_bbox)

    reprojection = GlobalWebMercatorImageReprojection(gwm_mosaic, gwm_box)
    reprojection.save("bng.png")
    reprojection.save_world_file("bng.pngw")


if __name__ == "__main__":
    main()
