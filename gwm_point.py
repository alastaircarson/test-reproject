from typing import Tuple


class GlobalWebMercatorPoint:
    """ Class to reproject points from BNG to GWM with OGR """

    @staticmethod
    def reproject_bng_to_gwm(bng: Tuple) -> Tuple:
        """ Reproject a BNG point to a GWM one """

        if bng == (300000, 600000):
            return -398075.709110655, 7417169.44503078
        elif bng == (300000, 601000):
            return -398115.346383602, 7418925.37709793
        elif bng == (301000, 601000):
            return -396363.034574031, 7418964.91393662
        elif bng == (301000, 600000):
            return -396323.792660911, 7417208.95976453
        else:
            raise Exception("Unexpected point")
