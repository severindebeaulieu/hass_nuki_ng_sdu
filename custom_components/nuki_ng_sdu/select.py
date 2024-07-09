from email.policy import default
from homeassistant.components.select import SelectEntity
from homeassistant.helpers.entity import EntityCategory

import logging

from . import NukiEntity
from .constants import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass,
    entry,
    async_add_entities
):
    entities = []
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(entities)
    return True