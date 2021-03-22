# ha-linknx

This is a integration between Home Assistant (HA) and Linknx.

### Installation

The files in this project should be extracted in the HA `<config_dir>/custom_components/linknx/` (You might need to create the custom_components and linknx directories).

Add the following entry in your `<config_dir>/configuration.yaml`:

```yaml
linknx:
  host: IP or hostname for the linknx REST gateway
  port: Port for the linknx REST gategay (default = 1028)

light:
  - platform: linknx
    entities:
      - { id: "light_garage", name: "Garage Light" }
      - { id: "cook_dinner", type: "scenario", name: "Cook dinner" }

switch:
  - platform: linknx
    entities:
      - { id: "switch_library", name: "Switch library" }

sensor:
  - platform: linknx
    entities:
      - { id: "outside_light", name="Outside light", type: "lx" }
      - { id: "outside_temp", name="Outside temperature", type: "°C" }

binary_sensor:
  - platform: linknx
    entities:
      - { id: "is_holiday", name: "Is it a holiday today" }

```

The integration currently supports light, switch, sensor and binary_sensor, is't still a lot of work in progress, but currently the following attributes are supported for each HA entity:

- light
  - id: The linknx id (mandatory)
  - name: The name of the light in HA (mandatory)
  - type: "light" (default) or "scenario" - just give different icons (optional)
  - dim: The linknx id for the dimmer (3.007) - just supports up/down/stop right now (optional)
  - dimfactor: (default 15) - factor depending on how fast the dimmer dim (optional)

- switch
  - id: The linknx id (mandatory)
  - name: The name of the switch in HA (mandatory)

- sensor
  - id: The linknx id (mandatory)
  - name: The name of the sensor in HA (mandatory)
  - type: "lx" - for light or "°C" for temperature (this might change) (mandatory)

- binary_sensor
  - id The linknx id (mandatory)
  - name: The name of the binary_sensor in HA (mandatory)
  - type: "binary" (default) or "workday" (just set another icon) (optional)

This project is currently a lot of work in progress, things that will change:

- Name the sensor types differently
- Use the linknx/pyknx library instead of my own implementation

