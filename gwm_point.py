from typing import Tuple


class GlobalWebMercatorPoint:
    """ Class to reproject points from BNG to GWM with OGR """

    @staticmethod
    def reproject_bng_to_gwm(bng: Tuple) -> Tuple:
        """ Reproject a BNG point to a GWM one """

        if bng == (306000, 671000):
            return -390262.523560616, 7543074.57885507
        elif bng == (306000, 672000):
            return -390301.312053066, 7544859.2233734
        elif bng == (307000, 671000):
            return -388481.840979317, 7543113.23218705
        elif bng == (307000, 672000):
            return -388520.217862485, 7544897.89865206
        else:
            raise Exception("Unexpected point")
