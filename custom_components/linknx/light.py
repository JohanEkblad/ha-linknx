"""Platform for linknx light integration."""
import logging
from time import sleep

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
# Import the device class from the component that you want to support
from homeassistant.components.light import (
    PLATFORM_SCHEMA, ATTR_BRIGHTNESS, SUPPORT_BRIGHTNESS, LightEntity)
from homeassistant.const import CONF_INCLUDE, CONF_ENTITIES

_LOGGER = logging.getLogger(__name__)

DOMAIN="linknx"

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_INCLUDE, default=''): cv.string,
    vol.Optional(CONF_ENTITIES, default=[]): cv.ensure_list,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Awesome Light platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    knx = hass.data[DOMAIN]['knx']
    entities = config.get(CONF_ENTITIES)

    # Add devices from definition in ha 
    add_devices(LinknxLight(knx, light["id"], "" if not ("dim" in light) else light["dim"], 15 if not ("dimfactor" in light) else light["dimfactor"], "light" if not ("type" in light) else light["type"], light["name"]) for light in entities) 


class LinknxLight(LightEntity):
    """Representation of Linknx Light."""

    def __init__(self, knx, id, dim, dimfactor, typ, name):
        """Initialize an AwesomeLight."""
        self._knx = knx
        self._id = id # The id is the unique id in ha and also the linknx id
        self._dim = dim
        self._dimfactor = dimfactor
        self._type = typ
        self._name = name
        self._state = None
        self._brightness = 0 

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique id of this light."""
        return self._id

    @property
    def icon(self):
        """Return the icon to use."""
        if self._type == "light":
            if self._dim == "":
                return 'mdi:lightbulb' 
            else: 
                return 'mdi:lightbulb-on'
        elif self._type == "scenario":
            return 'mdi:lightbulb-group'
        else:
            return None

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Instruct the light to turn on."""

        self._knx.write(self._id, "on")
        if ATTR_BRIGHTNESS in kwargs:
            brightness=kwargs[ATTR_BRIGHTNESS]
            delta = brightness - self._brightness
            _LOGGER.warning("Current brightness="+str(self._brightness)+" setting to "+str(brightness)+" kwargs="+str(kwargs))

            if delta > 0 : # Send up
                millis=delta*self._dimfactor
                self._knx.write(self._dim,"up")
                sleep(millis/1000.0)
                self._knx.write(self._dim,"stop")
            else: # Send down
                millis=-delta*self._dimfactor
                self._knx.write(self._dim,"down")
                sleep(millis/1000.0)
                self._knx.write(self._dim,"stop")
            self._brightness=brightness


    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self._knx.write(self._id, "off")

    @property
    def supported_features(self):
        """Return supported features"""
        if self._dim != "":
            return SUPPORT_BRIGHTNESS
        else:
            return 0

    @property
    def brightness(self):
        return self._brightness

    def update(self):
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._knx.read(self._id) == 'on'
