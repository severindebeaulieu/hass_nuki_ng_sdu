from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.entity import EntityCategory

import logging

from . import NukiEntity
from .constants import DOMAIN
from .states import DoorSensorStates, LockStates, LockModes

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    entities = []
    data = entry.as_dict()
    coordinator = hass.data[DOMAIN][entry.entry_id]

    for dev_id in coordinator.data.get("devices", {}):
        entities.append(BatteryLow(coordinator, dev_id))
        if coordinator.device_supports(dev_id, "batteryCharging"):
            entities.append(BatteryCharging(coordinator, dev_id))
        entities.append(LockState(coordinator, dev_id))
        if coordinator.device_supports(dev_id, "keypadBatteryCritical"):
            entities.append(KeypadBatteryLow(coordinator, dev_id))
        if coordinator.device_supports(dev_id, "doorsensorStateName"):
            entities.append(DoorState(coordinator, dev_id))
    async_add_entities(entities)
    return True


class BatteryLow(NukiEntity, BinarySensorEntity):
    def __init__(self, coordinator, device_id):
        super().__init__(coordinator, device_id)
        self.set_id("binary_sensor", "battery_low")
        self.set_name("Battery Critical")

    @property
    def is_on(self) -> bool:
        return self.last_state.get("batteryCritical", False)

    @property
    def device_class(self) -> str:
        return "battery"

    @property
    def entity_category(self):
        return EntityCategory.DIAGNOSTIC


class BatteryCharging(NukiEntity, BinarySensorEntity):
    def __init__(self, coordinator, device_id):
        super().__init__(coordinator, device_id)
        self.set_id("binary_sensor", "battery_charging")
        self.set_name("Battery Charging")
        self._attr_device_class = "battery_charging"

    @property
    def is_on(self) -> bool:
        return self.last_state.get("batteryCharging", False)

    @property
    def entity_category(self):
        return EntityCategory.DIAGNOSTIC


class KeypadBatteryLow(NukiEntity, BinarySensorEntity):
    def __init__(self, coordinator, device_id):
        super().__init__(coordinator, device_id)
        self.set_id("binary_sensor", "keypad_battery_low")
        self.set_name("Keypad Battery Critical")

    @property
    def is_on(self) -> bool:
        return self.last_state.get("keypadBatteryCritical", False)

    @property
    def device_class(self) -> str:
        return "battery"

    @property
    def entity_category(self):
        return EntityCategory.DIAGNOSTIC

class LockState(NukiEntity, BinarySensorEntity):
    def __init__(self, coordinator, device_id):
        super().__init__(coordinator, device_id)
        self.set_id("binary_sensor", "state")
        self.set_name("Locked")
        self._attr_device_class = "lock"

    @property
    def is_on(self) -> bool:
        currentMode = LockModes(self.last_state.get("mode", LockModes.DOOR_MODE.value))
        currentState = LockStates(self.last_state.get("state", LockStates.UNDEFINED.value))
        return currentState != LockStates.LOCKED or currentMode != LockModes.DOOR_MODE

    @property
    def extra_state_attributes(self):
        return {
            "timestamp": self.last_state.get("timestamp")
        }


class DoorState(NukiEntity, BinarySensorEntity):
    def __init__(self, coordinator, device_id):
        super().__init__(coordinator, device_id)
        self.set_id("binary_sensor", "door_state")
        self.set_name("Door Open")
        self._attr_device_class = "door"

    @property
    def is_on(self) -> bool:
        current = DoorSensorStates(self.last_state.get(
            "doorsensorState", DoorSensorStates.UNKNOWN.value))
        return current != DoorSensorStates.DOOR_CLOSED
