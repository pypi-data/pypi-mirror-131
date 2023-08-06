"""

goveelights.client

This contains the base class for all Govee devices.

"""

import json
import logging
import logging.config
import requests
from uuid import UUID
from .color import Color
from .consts import (
    ATTR_COLOR_TEMP_RANGE,
    KEY_ATTR_DICT,
    KEY_CMD,
    KEY_CODE,
    KEY_COLOR_TEMP,
    KEY_DATA,
    KEY_DEVICE,
    KEY_DEVICES,
    KEY_MESSAGE,
    KEY_MODEL,
    KEY_NAME,
    KEY_PROPERTIES,
    KEY_RANGE,
    KEY_RANGE_MAX,
    KEY_RANGE_MIN,
    KEY_VALUE,
    SUPPORTED_COMMANDS,
    SUPPORTED_MODELS,
)
from .exceptions import (
    ClientException,
    InvalidAPIKey,
    InvalidResponse,
)
from .settings import LOGGING

ACCEPTED_UUID_VERSION = 4

GOVEE_HEADER_DATE = "Date"
GOVEE_HEADER_CONTENT_LENGTH = "Content-Length"
GOVEE_HEADER_LIMIT_REMAINING = "Rate-Limit-Remaining"
GOVEE_HEADER_LIMIT_RESET = "Rate-Limit-Reset"
GOVEE_HEADER_LIMIT_TOTAL = "Rate-Limit-Total"
GOVEE_HEADER_RESPONSE_TIME = "X-Response-Time"
GOVEE_HEADER_TRACE_ID = "X-traceId"
GOVEE_HEADERS = (
    GOVEE_HEADER_DATE,
    GOVEE_HEADER_CONTENT_LENGTH,
    GOVEE_HEADER_LIMIT_REMAINING,
    GOVEE_HEADER_LIMIT_RESET,
    GOVEE_HEADER_LIMIT_TOTAL,
    GOVEE_HEADER_RESPONSE_TIME,
    GOVEE_HEADER_TRACE_ID,
)


HEADER_API_KEY = "Govee-API-Key"
HEADER_CONTENT_TYPE = "Content-Type"
HEADER_CONTENT_TYPE_VALUE = "application/json"

QUERY_DEVICE = "device"
QUERY_MODEL = "model"

URI_BASE = "https://developer-api.govee.com/v1"
URI_DEVICES = f"{URI_BASE}/devices"
URI_CONTROL = f"{URI_DEVICES}/control"
URI_STATE = f"{URI_DEVICES}/state"

SUCCESS_CODES = [200, 201, 202]


logger = logging.getLogger(__name__)
logging.config.dictConfig(LOGGING)


def validate_api_key(key):
    """
    This method receives a string and validates it's a UUIDv4 key. It returns
    the key as a string if it's valid, throws an error otherwise.
    """
    try:
        key_str = str(key)
        key_version = UUID(key).version
        logger.info(f"Got valid key version: {key_version}")
    except (ValueError, TypeError) as ve:
        raise InvalidAPIKey("API Key is invalid") from ve
    else:
        if key_version == ACCEPTED_UUID_VERSION:
            return key_str
        else:
            raise InvalidAPIKey("Key version is invalid")


def get_response_headers(response):
    """
    This is used to parse the response header.
    """
    return {
        attr: value for attr, value in response.headers.items() if attr in GOVEE_HEADERS
    }


class GoveeClient():
    """
    This is the base class for the Govee API hub.
    """

    def __init__(self, api_key):
        logger.info("Creating client")
        self.api_key = api_key

    @property
    def api_key(self):
        """
        This is used to access the device's API key.
        """
        try:
            return self._api_key
        except AttributeError:
            return None
        except Exception as e:
            raise ClientException() from e

    @api_key.setter
    def api_key(self, api_key):
        """
        This is used to set a client's API key, if it's valid.
        """
        logger.debug(f"setting API Key: {api_key}")
        self._api_key = validate_api_key(api_key)

    #
    # Here contains methods sending data TO the API
    #

    def validate_response(self, response):
        """
        This method is used to validate the response headers are within
        expectations.
        This returns a dict with the body of the response.
        """

        # Validate the headers look fine
        resp_headers = get_response_headers(response)
        assert response.status_code in SUCCESS_CODES, f"Invalid response code {response.status_code}"
        assert int(resp_headers[
            GOVEE_HEADER_CONTENT_LENGTH]) > 0, f"Invalid response length {response.headers[GOVEE_HEADER_CONTENT_LENGTH]}"

        # Verify response data looks good
        response_dict = json.loads(response.text)
        assert response_dict[
            KEY_CODE] in SUCCESS_CODES, f"Invalid status code in response {response_dict[KEY_CODE]}"
        logger.debug(f"Response message {response_dict[KEY_MESSAGE]}")
        return response_dict

    def get_data(self, req_uri, device_id=None, model=None):
        """
        This is used to facilitate any GET call to the API.
        """
        logger.info(f"get_data: {device_id} - {model}")
        logger.debug(f"Request Target: {req_uri}")

        try:
            req = requests.get(
                req_uri,
                headers=self._generate_headers(),
                params=GoveeClient._generate_params(device_id, model)
            )

        except Exception as e:
            logger.error(f"GET Exception: {e}")
            raise ClientException(f"Failed to request data - {e}") from e

        else:
            logger.info(f"Response: {req.status_code} - {len(req.text)}")
            logger.debug(f"Headers: {req.headers}")

            ret_dict = self.validate_response(req)[KEY_DATA]
            return ret_dict

    def put_data(self, req_uri, device_id, model, req_body):
        """
        This is responsible for sending commands intended to control a specific
        light.
        """
        logger.info(f"put_data: {device_id} - {model} - {req_body}")
        logger.debug(f"Request Target: {req_uri}")

        try:
            logger.debug(f"Request Body: {req_body} - {type(req_body)}")
            req = requests.put(
                req_uri,
                headers=self._generate_headers(),
                params=GoveeClient._generate_params(device_id, model),
                json=req_body
            )
            logger.debug(f"Got response: {req.status_code} - {req.text}")
        except Exception as e:
            logger.error(f"PUT Exception: {e}")
            raise ClientException(
                f"Failed to update device - {req.status_code}"
            ) from e
        else:
            logger.info(f"Response: {req.status_code} - {len(req.text)}")
            logger.debug(f"Headers: {req.headers}")

            ret_dict = self.validate_response(req)[KEY_DATA]
            return ret_dict

    #
    # This is just the helper stuff
    #

    def _generate_headers(self):
        """
        This is for internal use.
        This generates the headers for the request to the Govee API.
        """
        logger.debug("Generating headers")
        tmp_dict = {
            HEADER_API_KEY: self.api_key,
            HEADER_CONTENT_TYPE: HEADER_CONTENT_TYPE_VALUE,
        }
        logger.debug(f"Generated: {tmp_dict}")
        return tmp_dict

    def _generate_params(device_id=None, model=None):
        """
        This is for internal use.
        This is used to generate the parameters used in some API requests.
        """
        logger.debug("Generating params")
        if device_id and model:
            tmp_params = {
                QUERY_DEVICE: device_id,
                QUERY_MODEL: model,
            }
            logger.debug(f"Generated Params: {tmp_params}")
            return tmp_params
        # In case we don't have parameters to generate
        return None

    def _generate_payload(device_id, model, cmd, value):
        """
        This is used to generate the payload for a Device State update request.
        """
        assert model in SUPPORTED_MODELS, "Device model is not supported"

        cmd_dict = {KEY_NAME: cmd}
        if type(value) is Color:
            cmd_dict[KEY_VALUE] = value.rgb_dict()
        else:
            cmd_dict[KEY_VALUE] = value

        return {
            KEY_DEVICE: device_id,
            KEY_MODEL: model,
            KEY_CMD: cmd_dict,
        }

    #
    # This stuff is here for outside users to access.
    #

    def get_devices(self):
        """
        This is used to return an interable with Device Attributes and values
        dicts.
        """
        logger.info("Requesting devices...")
        device_list = []
        for device_dict in self.get_data(URI_DEVICES)[KEY_DEVICES]:
            tmp_dict = {}
            for prop, value in device_dict.items():
                try:
                    tmp_dict[KEY_ATTR_DICT[prop]] = value
                except KeyError:
                    if prop == KEY_PROPERTIES:
                        tmp_dict[ATTR_COLOR_TEMP_RANGE] = (
                            value[KEY_COLOR_TEMP][KEY_RANGE][KEY_RANGE_MIN], value[KEY_COLOR_TEMP][KEY_RANGE][KEY_RANGE_MAX])
            device_list.append(tmp_dict)

        return device_list

    def get_device_state(self, device_id, model):
        """
        This returns a dict with attributes and values returned by get_data.
        """
        logger.info(f"Requesting state for {device_id}")

        def flatten_dict(resp_dict):
            """
            This method is used to flatten a dict returned by get_data, to simplify the parsing process.
            """
            prop_dict = resp_dict[KEY_PROPERTIES]
            del resp_dict[KEY_PROPERTIES]
            for entry in prop_dict:
                for key, value in entry.items():
                    resp_dict[key] = value
            logger.debug(f"Flattened Dict: {resp_dict}")
            return resp_dict

        key_dict = flatten_dict(self.get_data(URI_STATE, device_id, model))
        tmp_dict = {
            KEY_ATTR_DICT[key]: value for key, value in key_dict.items()
        }

        logger.debug(f"Got dict: {tmp_dict}")
        return tmp_dict

    def update_device_state(self, device_id, model, cmd_name, value):
        """
        This is used to handle updating a device via the API. True is
        returned if the update succeeds. False if a failure is received.
        """
        logger.info(f"Updating device {device_id} - {cmd_name} - {value}")

        if cmd_name not in SUPPORTED_COMMANDS:
            raise ClientException("Command is not supported")

        req_payload = {
            KEY_DEVICE: device_id,
            KEY_MODEL: model,
            KEY_CMD: {
                KEY_NAME: cmd_name,
                KEY_VALUE: value,
            },
        }
        logger.debug(f"payload: {req_payload}")
        try:
            self.put_data(URI_CONTROL, device_id, model, req_payload)

        except Exception as e:
            raise ClientException("Failed to update device") from e

        else:
            return True

        return False
