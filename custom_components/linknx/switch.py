"""Platform for linknx switch integration."""
import logging
from time import sleep

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.switch import (
    PLATFORM_SCHEMA, SwitchEntity)
from homeassistant.const import CONF_ENTITIES

_LOGGER = logging.getLogger(__name__)

DOMAIN="linknx"

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_ENTITIES, default=[]): cv.ensure_list,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Switches"""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    knx = hass.data[DOMAIN]['knx']
    entities = config.get(CONF_ENTITIES)

    add_devices(LinknxSwitch(knx, switch["id"], switch["name"]) for switch in entities) 


class LinknxSwitch(SwitchEntity):
    """Representation of Linknx Switch."""

    def __init__(self, knx, id, name):
        """Initialize an the Switch"""
        self._knx = knx
        self._id = id # The id is the unique id in ha and also the linknx id
        self._name = name
        self._state = None

    @property
    def name(self):
        """Return the display name of this switch."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique id of this switch."""
        return self._id

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Instruct the switch to turn on."""

        self._knx.write(self._id, "on")

    def turn_off(self, **kwargs):
        """Instruct the switch to turn off."""
        self._knx.write(self._id, "off")

    def update(self):
        """Fetch new state data for this switch.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._knx.read(self._id) == "on"
