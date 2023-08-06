"""
goveelights.device

This is the base class for Govee devices that use the API.

"""
import re
import logging
import logging.config

from .color import (
    Color,
    validate_temp_range,
)
from .consts import (
    POWER_STATES,
    SUPPORTED_MODELS,
    SUPPORTED_COMMANDS,
    ATTR_POWER_STATE,
    ATTR_BRIGHTNESS,
    ATTR_COLOR,
    ATTR_COLOR_TEMP,
    BRIGHTNESS_MAX,
    BRIGHTNESS_MIN,
    ONLINE_STATES,
    ATTR_DEVICE_NAME,
    ATTR_ID,
)
from .exceptions import (
    DeviceException,
    InvalidState,
    InvalidValue,
)
from .settings import LOGGING

MODE_TEMP = "temp"
MODE_COLOR = "color"
DEVICE_MODES = [MODE_TEMP, MODE_COLOR]
REGEX_DEVICE_ID = "^[a-fA-F0-9]{2}(:[a-fA-F0-9]{2}){7}$"

ALLOWED_MODES = (MODE_TEMP, MODE_COLOR)

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOGGING)


def validate_device_id(value):
    """
    This is used to validate that the device_id meets the Govee format.
    If it does, device_id is returned, None otherwise.
    """
    try:
        value_str = str(value)
    except Exception as e:
        raise InvalidValue("Cannot process Device ID") from e
    else:
        if re.match(REGEX_DEVICE_ID, value_str):
            return value_str
        else:
            raise InvalidValue("Device ID is not acceptable")
    raise InvalidValue("Invalid Device Id")


def validate_power_state(value):
    """
    This is used to validate device power states.
    """
    if value in POWER_STATES:
        return value

    raise InvalidValue("Power state is not valid")


def validate_brightness(value):
    """
    This is used to validate the brightness is an int between 1 and 100.
    """
    try:
        value_int = int(value)
    except ValueError as ve:
        raise InvalidValue("Brightness is not an int") from ve
    except Exception as e:
        raise InvalidValue("Cannot process Brightness") from e
    else:
        if BRIGHTNESS_MIN <= value_int <= BRIGHTNESS_MAX:
            return value_int
        else:
            raise InvalidValue("Brightness is not acceptable")

    raise InvalidValue("Invalid Brightness")


def validate_color(color):
    """
    This is used to validate color values are correct
    """
    if type(color) is dict:
        color = Color(rgb_dict=color)
    elif type(color) is not Color:
        raise InvalidValue("Invalid type for color.")

    return color


def validate_color_temp(value, min=0, max=0):
    """
    This is used to validate a provided Color Temp is within the specified
    range.
    """
    if not type(value) is int and type(min) is int and type(max) is int:
        raise InvalidValue("Provided values are not ints")

    if min:
        if max and max < min:
            raise InvalidValue("Value is not within Color Temp Range")
        if value < min:
            raise InvalidValue("Value is not within Color Temp Range")
    if max:
        if value > max:
            raise InvalidValue("Value is not within Color Temp Range")

    return value


class GoveeDevice():
    """
    This is the base class for an API compatible Govee device.
    This is the digital representation of the physical device.
    """

    attr_validator = {
        ATTR_POWER_STATE: validate_power_state,
        ATTR_BRIGHTNESS: validate_brightness,
        ATTR_COLOR: validate_color,
        ATTR_COLOR_TEMP: validate_color_temp,
    }

    def __init__(self, hub=None, device_id=None, device_dict=None, initialized=True):
        """
        The user may create an instance by providing a device ID or a dict
        containing the device info, provided by Govee.
        """
        logger.info(f"Creating device {device_id} - ")

        # Need to make sure this exists
        self._color_temp_range = (None, None)

        # Manually create a device
        if device_id:
            try:
                self.id = device_id
                if hub:
                    hub.register_device(self)
            except Exception as e:
                raise DeviceException(
                    "Failed to set device ID") from e

        # Create a device from Govee data
        elif device_dict:
            for key, value in device_dict.items():
                logger.debug(f"Attempting to set {key}={value}")
                try:
                    setattr(self, key, value)
                except Exception as e:
                    raise DeviceException("Unknown Error") from e
                else:
                    logger.debug("Success")

        # Make sure we set the device_id
            try:
                device_id = self.id
                if hub:
                    hub.register_device(self)
            except Exception as e:
                raise InvalidState(
                    "Failed to find Device ID") from e
        else:
            raise DeviceException("Insufficient data to create device")

        self.initialized = initialized
        logger.debug("Device build successful")

    def __repr__(self):
        try:
            if hasattr(self, ATTR_DEVICE_NAME):
                return str(self.device_name)
            elif hasattr(self, ATTR_ID):
                return str(self.id)
            return "Unconfigured Device"
        except AttributeError:
            return "Broken Device"
        except Exception as e:
            raise DeviceException("Failed to generate representation") from e

    # Decorator used to facilitate API requesting updates
    def api_update(attr):
        def wrapper(func):
            def initialize_check_and_update(*args, **kwargs):
                # We're only going to use this for instance methods
                device = args[0]
                # This is just here as a hot fix.
                if attr == ATTR_COLOR_TEMP:
                    value = type(device).attr_validator[attr](
                        args[1],
                        device.color_temp_range[0],
                        device.color_temp_range[1]
                    )
                else:
                    value = type(device).attr_validator[attr](args[1])
                args = (args[0],) + (value,) + args[2:]
                try:
                    if device.initialized:
                        if attr == ATTR_COLOR:
                            if not device.hub.control_device(
                                device,
                                attr,
                                value.rgb_dict()
                            ):
                                return None
                        else:
                            if not device.hub.control_device(
                                device,
                                attr,
                                value
                            ):
                                return None

                    return func(*args, **kwargs)
                except AttributeError as ae:
                    raise DeviceException("Device does not have a hub") from ae

            return initialize_check_and_update
        return wrapper

    #
    # These are Govee device properties
    #

    @property
    def hub(self):
        """
        This is used to provide access to the hub a device is registered with.
        """
        try:
            return self._hub
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException("Failed to retrieve hub") from e

    @property
    def id(self):
        """
        This is the unique ID used to identify the device. Govee identifies it
        as the MAC address, but it has 8 octets.
        """
        try:
            return self._device_id
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException("Failed to retrieve ID") from e

    @id.setter
    def id(self, device_id):
        """
        Set the Device ID iff it's not set.
        """
        try:
            self._device_id = validate_device_id(device_id)
        except Exception as e:
            raise DeviceException("Failed to set ID") from e

    @property
    def model(self):
        try:
            return self._model
        except AttributeError:
            return None

        except Exception as e:
            raise DeviceException("Failed to retrieve Model") from e

    @model.setter
    def model(self, model_name):
        try:
            if model_name not in SUPPORTED_MODELS:
                raise DeviceException("Invalide model provided")
            self._model = model_name
        except Exception as e:
            raise DeviceException("Failed to set Model") from e

    @property
    def device_name(self):
        try:
            return self._device_name
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException("Failed to retrieve Device Name") from e

    @device_name.setter
    def device_name(self, device_name):
        try:
            self._device_name = device_name
        except Exception as e:
            raise DeviceException("Failed to retrieve Device Name") from e

    @property
    def controllable(self):
        try:
            return self._controllable
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException("Failed to retrieve Controllable") from e

    @controllable.setter
    def controllable(self, is_controllable=False):
        try:
            self._controllable = bool(is_controllable)
        except Exception as e:
            raise DeviceException("Failed to set Controllable") from e

    @property
    def retrievable(self):
        try:
            return self._retrievable
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException("Failed to retrieve Retrievable") from e

    @retrievable.setter
    def retrievable(self, is_retrievable=True):
        try:
            self._retrievable = bool(is_retrievable)
        except Exception as e:
            raise DeviceException("Failed to set Retrievable") from e

    @property
    def supported_commands(self):
        try:
            return self._supported_commands
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException(
                "Failed to retrieve Supported Commands") from e

    @supported_commands.setter
    def supported_commands(self, command_iterable):
        """
        This is responsible for reading in supported commands for an iterable.
        """
        try:
            self._supported_commands = [
                x for
                x in command_iterable
                if x in SUPPORTED_COMMANDS
            ]
        except Exception as e:
            raise DeviceException("Failed to set Suppoerted Commands") from e

    @property
    def color_temp_range(self):
        """
        The permitted range of color temperatures
        """
        try:
            return self._color_temp_range
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException("Failed to retrieve Color Temp Range") from e

    @color_temp_range.setter
    def color_temp_range(self, range_tuple):
        """
        The permitted range of color temperatures
        """
        logger.debug(f"color_temp_range: {range_tuple}")
        try:
            # self._color_temp_range = validate_temp_range(range_tuple)
            self._color_temp_range = range_tuple
        except Exception as e:
            raise DeviceException("Failed to set Color Temp Range") from e

    @property
    def allowed_modes(self):
        try:
            return self._allowed_modes
        except AttributeError:
            return []
        except Exception as e:
            raise DeviceException("Failed to retrieve Allowed Modes") from e

    @allowed_modes.setter
    def allowed_modes(self, modes):
        if not all(mode in DEVICE_MODES for mode in modes):
            raise InvalidValue("Invalid device mode identified.")
        try:
            self._allowed_modes = modes
        except Exception as e:
            raise DeviceException("Failed to set Allowed Modes") from e

    #
    # Device state information below here
    #

    @property
    def online(self):
        """
        This is used to safely retrieve the online attribute of the device.
        """
        try:
            return self._online
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException("Failed to retrieve Online") from e

    @online.setter
    def online(self, is_online):
        # assert self.retrievable, "Online status is not retrievable."
        try:
            if bool(is_online) in ONLINE_STATES:
                self._online = is_online
            else:
                raise DeviceException("Online State is invalid")
        except Exception as e:
            raise DeviceException("Failed to set Online") from e

    @property
    def registered(self):
        """
        This is just a simple check to make sure the device is registered.
        """
        try:
            if self.hub:
                return True
            else:
                return False
        except AttributeError:
            return False
        except Exception as e:
            raise DeviceException(
                "Failed to retrieve Registration Flag") from e

    @property
    def power_state(self):
        try:
            return self._power_state
        # Warn that the attribute does not exist
        except AttributeError:
            return None
        # Raise a DeviceException if anything else happens
        except Exception as e:
            raise DeviceException(
                "Failed to retrieve power state") from e

    @power_state.setter
    @api_update(ATTR_POWER_STATE)
    def power_state(self, power_state):
        """
        This is used to set the power state for a device.
        It raises an AssertionError if the power state provided is invalid.
        It raises a DeviceException if any other Exception is raised.
        """
        try:
            self._power_state = power_state
        except Exception as e:
            raise DeviceException("Failed to set Power State") from e

    @property
    def brightness(self):
        try:
            return self._brightness
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException("Failed to retrieve brightness") from e

    @brightness.setter
    @api_update(ATTR_BRIGHTNESS)
    def brightness(self, brightness):
        """
        This is used to update the brightness of the device if the hub is able
        to handle the request.
        """
        try:
            self._brightness = brightness
        except Exception as e:
            raise DeviceException("Failed to set Brightness") from e

    @property
    def color_mode(self):
        try:
            return self._color_mode
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException("Failed to retrieve Color Mode") from e

    @color_mode.setter
    def color_mode(self, mode):
        """
        This is used to set the current color mode of a device.
        """
        try:
            # if mode not in self.allowed_modes:
            #    raise InvalidState("Mode is not permitted")
            self._color_mode = mode
        except Exception as e:
            raise DeviceException("Failed to set Color Mode") from e

    @property
    def color(self):
        """
        This is used to retrieve the color of a device.
        """
        try:
            if self.color_mode == MODE_COLOR:
                return self._color
            else:
                return None
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException("Failed to retrieve Color") from e

    @color.setter
    @api_update(ATTR_COLOR)
    def color(self, color):
        """
        This is used to handle setting the color of a device.
        """
        try:
            self._color = color
            self.color_mode = MODE_COLOR
        except Exception as e:
            raise DeviceException("Failed to set Color") from e

    @property
    def color_temp(self):
        """
        This is used to retrieve the device's color temp value, if in color
        temp mode.
        If the device is not in color temp mode, it raises an error.
        """
        try:
            if self.color_mode == MODE_TEMP:
                return self._color_temp
            else:
                return None
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException("Failed to retrieve Color Temp") from e

    @color_temp.setter
    @api_update(ATTR_COLOR_TEMP)
    def color_temp(self, color_temp):
        """
        This is used to handle setting the color temp of a device.
        """
        try:
            self._color_temp = color_temp
            self.color_mode = MODE_TEMP
        except Exception as e:
            raise DeviceException(
                "Failed to set Color Temp") from e

    @property
    def initialized(self):
        """
        This is used to indicate whether a device has been initialized and
        therefore communicates with the client.
        """
        try:
            return self._initialized
        except AttributeError:
            return False

    @initialized.setter
    def initialized(self, init_status):
        """
        This is used to control whether a device has been initialized.
        """
        try:
            self._initialized = bool(init_status)
        except ValueError:
            raise DeviceException("Status must be boolean")

    #
    # This is used for any communication with the hub.
    #

    def refresh(self):
        """
        This is called to refresh device data.
        The method relies on calling the hub to update the device itself.
        """
        logger.info("Refreshing device...")
        try:
            self.hub.refresh_device(self.id)
        except Exception as e:
            raise DeviceException("Unable to refresh device") from e
