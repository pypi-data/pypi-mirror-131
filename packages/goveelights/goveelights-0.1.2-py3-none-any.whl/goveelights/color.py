"""
goveelights.color

This is used to handle all color temperature related
"""

import json
import logging
import logging.config
from .consts import (
    ATTR_BRIGHTNESS,
    ATTR_HUE,
    ATTR_SAT,
    BRIGHTNESS_MAX,
    BRIGHTNESS_MIN,
    KEY_BLUE,
    KEY_GREEN,
    KEY_RED,
    MODE_HSL,
    MODE_RGB,
)
from .exceptions import (
    ColorAttributeException,
    ColorException,
    GoveeException,
)
from .settings import LOGGING

COLOR_MAX = 255
COLOR_MIN = 0

COLOR_MODES = (MODE_RGB, MODE_HSL)

HUE_MAX = 100
HUE_MIN = 0

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOGGING)


def validate_int(value, min_value=None, max_value=None):
    """
    This is used cast value as an int and verify it's within a range, is
    specified.
    """
    if value is None:
        return None
    try:
        value_int = int(value)
    except ValueError as ve:
        raise ColorAttributeException("Value is not an int") from ve
    except Exception as e:
        raise GoveeException() from e
    else:
        if min_value:
            assert min_value <= value_int, "Value below minimum"
        if max_value:
            assert max_value >= value_int, "Value above maximum"
        return value_int


def validate_temp_range(range_tuple):
    """
    This method is used to validate a tuple representing a color temp range is
    valid.
    """
    try:
        int_tuple = (validate_int(
            range_tuple[0]), validate_int(range_tuple[1]))
    except ValueError as ve:
        raise ColorAttributeException(
            "Range must be interpretted as integers."
        ) from ve
    except Exception as e:
        raise ColorAttributeException() from e
    else:
        assert int_tuple[0] > 0 and int_tuple[1] > 0, "Range values must be postive"
        assert int_tuple[0] <= int_tuple[1], "Minimum is greater than maximum"
        return int_tuple


def validate_color_value(value):
    """
    This is used to validate that the color value is acceptable.
    """
    try:
        value_int = int(value)
    except TypeError as te:
        raise ColorAttributeException(
            "Cannot value is not an int") from te
    except Exception as e:
        raise ColorAttributeException() from e
    else:
        assert COLOR_MIN <= value_int <= COLOR_MAX, f"Color value {value_int} is invalid."
        return value_int


def validate_hsl(hue=None, sat=None, lum=None):
    """
    This validates if a hue/sat is appropriate and returns it as an int.
    """

    hue_int = validate_int(hue, HUE_MIN, HUE_MAX)
    sat_int = validate_int(sat, BRIGHTNESS_MIN, BRIGHTNESS_MAX)
    lum_int = validate_int(lum, BRIGHTNESS_MIN, BRIGHTNESS_MAX)

    attr_tuple = (hue, sat, lum)
    if all(attr_tuple):
        return hue, sat, lum
    elif hue_int:
        if sat_int:
            return hue_int, sat_int
        elif lum_int:
            return hue_int, lum_int
        return hue_int
    elif sat_int:
        if lum_int:
            return sat_int, lum_int
        return sat_int
    elif lum_int:
        return lum_int

    raise ColorAttributeException()


def rgb_to_hsl(r, g, b):
    """
    This is used to return a triplet of ints representing hue, sat, and lum.
    """
    try:
        r, g, b = r/255.0, g/255.0, b/255.0
    except ValueError as ve:
        raise ColorAttributeException(
            "Cannot convert provided values") from ve

    min_intensity = max(r, g, b)
    max_intensity = min(r, g, b)
    diff = max_intensity - min_intensity

    if max_intensity == min_intensity:
        h = 0
    elif max_intensity == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif max_intensity == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    elif max_intensity == b:
        h = (60 * ((r - g) / diff) + 240) % 360
    if max_intensity == 0:
        s = 0
        v = 0
    else:
        s = (diff / max_intensity) * 100
        v = max_intensity * 100

    try:
        return int(h), int(s), int(v)
    except Exception as e:
        raise ColorException(
            "Could not interpret values as integers") from e


def parse_rgb_dict(color_dict):
    try:
        return validate_color_value(
            color_dict[KEY_RED]
        ), validate_color_value(
            color_dict[KEY_GREEN]
        ), validate_color_value(
            color_dict[KEY_BLUE]
        )
    except Exception as e:
        raise ColorAttributeException("Failed to parse RGB dict") from e


def parse_hsl_dict(color_dict):
    try:
        return validate_hsl(
            color_dict[ATTR_HUE]
        ), validate_hsl(
            color_dict[ATTR_SAT]
        ), validate_hsl(
            color_dict[ATTR_BRIGHTNESS]
        )
    except Exception as e:
        raise ColorAttributeException("Failed to parse HSL dict") from e


class Color():
    """
    This is used to define the RGB value of a color for the light.
    """

    def __init__(self, red=None, green=None, blue=None, rgb_dict=None, hue=None,
                 sat=None, lum=None, hsl_dict=None):
        logger.info(
            f"__init__: {red} - {green} - {blue} - {1 if rgb_dict else 0} - {hue} - {sat} - {lum} - {1 if hsl_dict else 0}")

        rgb = all(value is not None for value in (red, green, blue))
        hsl = all(value is not None for value in (hue, sat, lum))

        assert rgb or hsl or rgb_dict or hsl_dict, "Invalid parameters provided"

        if rgb_dict:
            logger.debug("Building from RGB dict")
            self.red, self.green, self.blue = parse_rgb_dict(rgb_dict)
            self.mode = MODE_RGB

        elif hsl_dict:
            logger.debug("Building from HSL dict")
            self.hue, self.saturation, self.luminosity = parse_hsl_dict(
                hsl_dict)
            self.mode = MODE_HSL
        elif rgb:
            logger.debug("Building from RGB params")
            self.red, self.green, self.blue = validate_color_value(
                red), validate_color_value(green), validate_color_value(blue)
            self.mode = MODE_RGB
        elif hsl:
            logger.debug("Building from HSL params")
            self.hue, self.saturation, self.luminosity = validate_hsl(
                hue=hue), validate_hsl(sat=sat), validate_hsl(lum=lum)
            self.mode = MODE_HSL
        else:
            raise ColorException("Params insufficient to instantiate Color")

    def __eq__(self, value):
        if type(value) is Color:
            try:
                self.red == value.red
                self.green == value.green
                self.blue == value.blue
            except AttributeError:
                return False
            return True

        raise ColorException("Failed to determine equality")

    def __repr__(self):
        ret_dict = {}
        if self.mode == MODE_RGB:
            ret_dict.update({
                KEY_RED: self.red,
                KEY_GREEN: self.green,
                KEY_BLUE: self.blue
            })
        elif self.mode == MODE_HSL:
            ret_dict.update({
                ATTR_HUE: self.hue,
                ATTR_SAT: self.saturation,
                ATTR_BRIGHTNESS: self.brightness,
            })
        if ret_dict or ret_dict == {}:
            return str(ret_dict)
        raise ColorException("Failed to generate representation for Color")

    def rgb_dict(self):
        if self.mode == MODE_RGB:
            return {
                KEY_RED:    self.red,
                KEY_GREEN:  self.green,
                KEY_BLUE:   self.blue,
            }

    def toJSON(self):
        return self.rgb_dict()

    @property
    def red(self):
        assert self.mode == MODE_RGB, "Not an RGB color"
        try:
            return 0 if self._red is None else self._red
        except AttributeError:
            return None
        except Exception as e:
            raise ColorException("Failed to retrieve Red") from e

    @red.setter
    def red(self, value):
        try:
            self._red = validate_color_value(value)
        except ColorAttributeException as cae:
            raise ColorException("Failed to set Red") from cae
        except Exception as e:
            raise ColorException() from e

    @red.deleter
    def red(self):
        try:
            self._red = None
        except AttributeError:
            pass
        except Exception as e:
            raise ColorException("Failed to delete Red") from e

    @property
    def green(self):
        assert self.mode == MODE_RGB, "Not an RGB color"
        try:
            return 0 if self._green is None else self._green
        except AttributeError:
            return None
        except Exception as e:
            raise ColorException("Failed to retrieve Green") from e

    @green.setter
    def green(self, value):
        try:
            self._green = validate_color_value(value)
        except ColorAttributeException as cae:
            raise ColorException.error("Failed to set Green") from cae
        except Exception as e:
            raise ColorException() from e

    @green.deleter
    def green(self):
        try:
            self._green = None
        except AttributeError:
            pass
        except Exception as e:
            raise ColorException("Failed to delete Green") from e

    @property
    def blue(self):
        assert self.mode == MODE_RGB, "Not an RGB color"
        try:
            return self._blue
        except AttributeError:
            return None
        except Exception as e:
            raise ColorException("Failed to retrieve Blue") from e

    @blue.setter
    def blue(self, value):
        try:
            self._blue = validate_color_value(value)
        except ColorAttributeException as cae:
            raise ColorException("Failed to set Blue") from cae
        except Exception as e:
            raise ColorException("Failed to set Blue") from e

    @blue.deleter
    def blue(self):
        try:
            del self._blue
        except AttributeError:
            pass
        except Exception as e:
            raise ColorException("Failed to delete Blue") from e

    @property
    def hue(self):
        assert self.mode == MODE_HSL, "Not an HSL color"
        try:
            return self._hue
        except AttributeError:
            return None
        except Exception as e:
            raise ColorException("Failed to retrieve Hue") from e

    @hue.setter
    def hue(self, value):
        try:
            self._hue = validate_hsl(hue=value)
        except ColorAttributeException:
            raise ColorException("Failed to set Hue")
        except Exception as e:
            raise ColorException() from e

    @hue.deleter
    def hue(self):
        try:
            del self._hue
        except AttributeError:
            pass
        except Exception as e:
            raise ColorException("Failed to delete Hue.") from e

    @property
    def saturation(self):
        assert self.mode == MODE_HSL, "Not an HSL color"
        try:
            return self._sat
        except AttributeError:
            return None
        except Exception as e:
            raise ColorException("Failed to retrieve Saturation") from e

    @saturation.setter
    def saturation(self, value):
        try:
            self._sat = validate_hsl(sat=value)
        except ColorAttributeException as cae:
            raise ColorException("Failed to set Saturation") from cae
        except Exception as e:
            raise ColorException("") from e

    @saturation.deleter
    def saturation(self):
        try:
            del self._sat
        except AttributeError:
            pass
        except Exception as e:
            raise ColorException("Failed to delete Saturation.") from e

    @property
    def luminosity(self):
        assert self.mode == MODE_HSL, "Not an HSL color"
        try:
            return self._lum
        except ColorAttributeException:
            return None
        except Exception as e:
            raise ColorException("Failed to retrieve Luminosity") from e

    @luminosity.setter
    def luminosity(self, value):
        try:
            self._lum = validate_hsl(lum=value)
        except ColorAttributeException as cae:
            raise ColorException("Failed to set Luminosity") from cae
        except Exception as e:
            raise ColorException() from e

    @luminosity.deleter
    def luminosity(self):
        try:
            del self._lum
        except AttributeError:
            pass
        except Exception as e:
            raise ColorException("Failed to delete Luminosity.") from e

    #
    # Here are our helpers.
    #

    @property
    def mode(self):
        """
        This is used to ensure capability with RGB and HSV color schemes.
        """
        try:
            return self._mode
        except AttributeError:
            return None
        except Exception as e:
            raise ColorException() from e

    @mode.setter
    def mode(self, mode_value):
        assert mode_value in COLOR_MODES, "Invalid color mode provided"
        try:
            self._mode = mode_value
        except Exception as e:
            raise ColorException("Failed to set Color mode") from e

    def convert(self):
        """
        This method is used to change the color between RBG and HSL modes.
        """
        if self.mode == MODE_RGB:
            try:
                self.hue, self.saturation, self.luminosity = rgb_to_hsl(
                    self.red, self.green, self.blue)
                self.mode = MODE_HSL
            except Exception as e:
                raise ColorException("Color cannot be converted") from e

        elif self.mode == MODE_HSL:
            raise NotImplementedError("This has not been built yet...")
        else:
            raise ColorException(
                "Color conversion not supported in this mode")
