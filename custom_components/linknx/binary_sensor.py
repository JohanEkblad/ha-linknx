"""Platform for linknx binary sensor integration."""
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_ENTITIES
from homeassistant.components.binary_sensor import PLATFORM_SCHEMA, BinarySensorEntity

_LOGGER = logging.getLogger(__name__)

DOMAIN="linknx"

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_ENTITIES, default=[]): cv.ensure_list,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the binary sensor platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    knx = hass.data[DOMAIN]['knx']
    entities = config.get(CONF_ENTITIES)
 
    # Add sensor devices from definition in ha 
    sensors = [LinknxBinarySensor(knx, sensor["id"], sensor["name"], "binary" if not ("type" in sensor) else sensor["type"]) for sensor in entities]
    add_devices(sensors) 


class LinknxBinarySensor(BinarySensorEntity):
    """Representation of Linknx Binary Sensor."""

    def __init__(self, knx, idt, name, typ):
        self._knx = knx
        self._id = idt # The id is the unique id in ha and also the linknx id
        self._name = name
        self._attrs = {}
        self._type = typ
        self._state = None

    @property
    def name(self):
        """Return the display name of this sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique id of this sensor."""
        return self._id

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def is_on(self):
        """Return True if the state in 'on'"""
        return self._state == 'on'
    
    @property
    def icon(self):
        """Return the icon to use."""
        if self._type == "workday":
            return 'mdi:calendar-weekend'
        else:
            return None

    def update(self):
        """Fetch new state data for this binary sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._knx.read(self._id)
