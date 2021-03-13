""" linknx """

from homeassistant.const import EVENT_HOMEASSISTANT_START
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from . import linknx

DOMAIN="linknx"

CONF_HOST = "host"
CONF_PORT = "port"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema({
            vol.Required(CONF_HOST): cv.string,
            vol.Optional(CONF_PORT, default=1028): cv.positive_int,
        })
    },
    extra=vol.ALLOW_EXTRA,
)

def setup(hass, config):
    """linknx general config"""
    conf = config[DOMAIN]
    host = conf.get(CONF_HOST)
    port = conf.get(CONF_PORT)
    knx = linknx.Linknx(host, port)
    hass.data[DOMAIN] = {"knx":knx}

    return True

