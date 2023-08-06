"""

goveelights.hub

This contains the engine for the goveelights package.

"""
import logging
import logging.config

from .client import GoveeClient
from .consts import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR,
    ATTR_COLOR_TEMP,
    ATTR_POWER_STATE,
    CMD_BRIGHT,
    CMD_COLOR,
    CMD_COLOR_TEMP,
    CMD_TURN,
)
from .device import (
    GoveeDevice,
)
from .exceptions import (
    ClientException,
    DeviceException,
    GoveeHubException,
    RefreshException,

)
from .settings import LOGGING

ATTR_CMD_DICT = {
    ATTR_BRIGHTNESS: CMD_BRIGHT,
    ATTR_COLOR: CMD_COLOR,
    ATTR_COLOR_TEMP: CMD_COLOR_TEMP,
    ATTR_POWER_STATE: CMD_TURN,
}

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOGGING)


class GoveeHub():
    """
    This hub contains all the logic to use the Govee API and supervise devices.
    """

    def __init__(self, device_client):
        logger.info("Creating hub")
        self.client = device_client
        self._devices = {}

    @property
    def devices(self):
        """
        This is where all devices for an account are stored.
        """
        # Need to have a request submitted if nothing is present.
        logger.info('Getting Devices for hub')
        try:
            return self._devices
        except AttributeError:
            logger.warn("devices attribute is not set")
            return None
        except Exception as e:
            raise GoveeHubException.error("Failed to acces devices") from e

    def register_device(self, device):
        """
        This is used to register a device with the hub so the hub may manage it.
        """
        logger.info(f"Registering device {device.id}")
        assert issubclass(
            device.__class__, GoveeDevice
        ), "Device must be a subclass of GoveeDevice."

        try:
            self._devices[device.id] = device

            # self._devices[device.id].registered = True

            device._hub = self
        except Exception as e:
            raise GoveeHubException.error("Failed to register device") from e

    def register_devices(self, device_generator):
        for device in device_generator:
            self.register_device(device)

    @property
    def client(self):
        """
        This is the client that the hub uses to communicate with Govee.
        """
        try:
            return self._client
        except AttributeError as ae:
            raise GoveeHubException.warn("Client not set") from ae
        except Exception as e:
            raise GoveeHubException(
                "Failed to retrieve client") from e

    @client.setter
    def client(self, client):
        """
        This receives a GoveeClient instance.
        """
        if issubclass(type(client), GoveeClient):
            self._client = client
        else:
            raise GoveeHubException("Client is not a GoveeClient Subclass.")

    #
    # Here contains methods used to interface with the client
    #

    def refresh_device(self, device):
        """
        This is used to request a device's current properties from the client
        and update the device accordingly.
        A RefreshException is thrown if there's an exception encountered while
        updating the device.
        """
        logger.info(f"Refreshing device: {device.id}")

        try:
            for attr, value in self.client.get_device_state(device.id, device.model).items():
                logger.debug(f"Setting {attr} = {value}")
                setattr(device, attr, value)
        except ClientException as ce:
            raise RefreshException(
                f"Failed to fetch data: {device.id}") from ce
        except DeviceException as de:
            raise RefreshException(
                f"Failed to update: {device.id}") from de
        except Exception as e:
            raise RefreshException() from e

    def control_device(self, device, attr, value):
        """
        This is used to facilitate an API call when attempting to update
        a device.
        """
        logger.info(f"control_device: {device} - {attr} - {value}")

        try:
            if self.client.update_device_state(
                    device.id, device.model, ATTR_CMD_DICT[attr], value):
                return True
        except AttributeError as e:  # This may need to be changed.
            raise GoveeHubException(
                f"Failed to update: {device} - {attr}") from e

        return False

    #
    # Here are methods used to manage associated devices.
    #

    def build_devices(self):
        """
        This is responsible for automatically creating the devices associated
        with the hub. It requests dicts containing device information from the
        client.
        """
        self.register_devices(GoveeDevice(self, device_dict=device_dict)
                              for device_dict in self.client.get_devices())
