"""
Support for INSTEON dimmers via PowerLinc Modem.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/switch.insteon/
"""
import asyncio
import logging

from homeassistant.components.insteon import InsteonEntity
from homeassistant.components.switch import SwitchDevice

DEPENDENCIES = ['insteon']

_LOGGER = logging.getLogger(__name__)


@asyncio.coroutine
def async_setup_platform(hass, config, async_add_entities,
                         discovery_info=None):
    """Set up the INSTEON device class for the hass platform."""
    insteon_modem = hass.data['insteon'].get('modem')

    address = discovery_info['address']
    device = insteon_modem.devices[address]
    state_key = discovery_info['state_key']

    state_name = device.states[state_key].name

    _LOGGER.debug('Adding device %s entity %s to Switch platform',
                  device.address.hex, device.states[state_key].name)

    new_entity = None
    if state_name == 'openClosedRelay':
        new_entity = InsteonOpenClosedDevice(device, state_key)
    else:
        new_entity = InsteonSwitchDevice(device, state_key)

    if new_entity is not None:
        async_add_entities([new_entity])


class InsteonSwitchDevice(InsteonEntity, SwitchDevice):
    """A Class for an Insteon device."""

    @property
    def is_on(self):
        """Return the boolean response if the node is on."""
        return bool(self._insteon_device_state.value)

    @asyncio.coroutine
    def async_turn_on(self, **kwargs):
        """Turn device on."""
        self._insteon_device_state.on()

    @asyncio.coroutine
    def async_turn_off(self, **kwargs):
        """Turn device off."""
        self._insteon_device_state.off()


class InsteonOpenClosedDevice(InsteonEntity, SwitchDevice):
    """A Class for an Insteon device."""

    @property
    def is_on(self):
        """Return the boolean response if the node is on."""
        return bool(self._insteon_device_state.value)

    @asyncio.coroutine
    def async_turn_on(self, **kwargs):
        """Turn device on."""
        self._insteon_device_state.open()

    @asyncio.coroutine
    def async_turn_off(self, **kwargs):
        """Turn device off."""
        self._insteon_device_state.close()
