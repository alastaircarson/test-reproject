from PIL import Image
from tile_mosaic import TileMosaic
from gwm_box import GlobalWebMercatorBox
from transform import PositionTransform, SamplePointTransform, Scale, HorizontalFlip, Shift


class GlobalWebMercatorImageReprojection:
    def __init__(self, mosaic: TileMosaic, box: GlobalWebMercatorBox):
        self.mosaic = mosaic
        self.box = box
        self.test = [(0, 0), (400, 0), (400, 400), (0, 400)]
        self._create_transformation()
        self._apply_transformation()

    def _create_transformation(self):
        # Create a transformation to convert pixels of the target BNG image to the GWM mosaic image
        bng_img_to_gwm_image = PositionTransform()
        # Translate/scale image px to BNG
        bng_img_to_gwm_image = bng_img_to_gwm_image.combine(HorizontalFlip())
        bng_img_to_gwm_image = bng_img_to_gwm_image.combine(Scale(1/self.box.bng_res))
        bng_img_to_gwm_image = bng_img_to_gwm_image.combine(Shift(self.box.bng_bbox[0], self.box.bng_bbox[3]))
        self._test_coords(self.test, bng_img_to_gwm_image)

        # Transform BNG to GWM coords
        bng_gwm_transform = SamplePointTransform(
            self.box.bng_vertices[0], self.box.bng_vertices[1], self.box.bng_vertices[2],
            self.box.gwm_vertices[0], self.box.gwm_vertices[1], self.box.gwm_vertices[2])
        bng_img_to_gwm_image = bng_img_to_gwm_image.combine(bng_gwm_transform)
        self._test_coords(self.test, bng_img_to_gwm_image)

        # Translate/scale GWM coords to GWM mosaic image coords
        bng_img_to_gwm_image = bng_img_to_gwm_image.combine(
            Shift(-self.mosaic.mosaic_bbox[0], -self.mosaic.mosaic_bbox[3]))
        bng_img_to_gwm_image = bng_img_to_gwm_image.combine(Scale(1 / self.box.gwm_res))
        bng_img_to_gwm_image = bng_img_to_gwm_image.combine(HorizontalFlip())
        self._test_coords(self.test, bng_img_to_gwm_image)

        self.transform = bng_img_to_gwm_image

    def _apply_transformation(self):
        self.bng_result = self.mosaic.image.transform(
            self.box.bng_map_size,
            Image.AFFINE,
            self._get_image_transform(self.transform),
            resample=Image.BICUBIC)

    @staticmethod
    def _get_image_transform(pt):
        """ Get the PIL transform tuple from a 3x3 matrix """
        return pt.matrix[0][0], pt.matrix[1][0], pt.matrix[2][0], pt.matrix[0][1], pt.matrix[1][1], pt.matrix[2][1]

    def save(self, filename:str):
        self.bng_result.save(filename)

    @staticmethod
    def _test_coords(coords, transform):
        for coord in coords:
            out = transform.transform(coord)
            print(f"{coord[0]}, {coord[1]} -> {out[0]}, {out[1]}")
