"""Platform for linknx sensor integration."""
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_INCLUDE, CONF_ENTITIES, TEMP_CELSIUS, LIGHT_LUX, DEVICE_CLASS_TEMPERATURE, DEVICE_CLASS_ILLUMINANCE
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DOMAIN="linknx"

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_ENTITIES, default=[]): cv.ensure_list,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Sensor platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    knx = hass.data[DOMAIN]['knx']
    entities = config.get(CONF_ENTITIES)
 
    # Add sensor devices from definition in ha 
    sensors = [LinknxSensor(knx, sensor["id"], sensor["name"], sensor["type"]) for sensor in entities]
    add_devices(sensors) 


class LinknxSensor(Entity):
    """Representation of Linknx Sensor."""

    def __init__(self, knx, idt, name, typ):
        self._knx = knx
        self._id = idt # The id is the unique id in ha and also the linknx id
        self._name = name
        self._attrs = {}
        self._type = typ
        self._state = None
        self._available = False

    @property
    def name(self):
        """Return the display name of this sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique id of this sensor."""
        return self._id

    @property
    def device_info(self):
        """Return device information."""
        return {
            'identifiers': {
                (DOMAIN, self.unique_id)
            },
            'name': self.name
        }

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state
    
    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attrs

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        if self._type == TEMP_CELSIUS:
            return DEVICE_CLASS_TEMPERATURE
        elif self._type == LIGHT_LUX:
            return DEVICE_CLASS_ILLUMINANCE
        else:
            return None

        
    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._type
    
    @property
    def icon(self):
        """Return the icon to use."""
        if self._type == TEMP_CELSIUS:
            return 'mdi:thermometer'
        elif self._type == LIGHT_LUX:
            return 'mdi:eye'
        else:
            return None

    @property
    def available(self):
        """Return True if entity is available."""
        return self._available

    def update(self):
        """Fetch new state data for this sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        state = self._knx.read(self._id)
        
        if self._type == TEMP_CELSIUS:
            self._state = state
            self._attrs['Temperature'] = state
        elif self._type == LIGHT_LUX:
            self._state = state
            self._attrs['Illuminance'] = state
        else:
            _LOGGER.error("KNX we got into else")
            self._state=state
        self._available = True

