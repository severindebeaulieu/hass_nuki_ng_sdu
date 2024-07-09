[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

## Better support for Nuki devices in Home Assistant

### Features:
* Supported modes:
* TODO
  
## Setup

{% if not installed %}

### Installation:

* Go to HACS -> Integrations
* Click the three dots on the top right and select `Custom Repositories`
* Enter `https://github.com/TODO` as repository, select the category `Integration` and click Add
* A new custom integration shows up for installation (Nuki Lock SDU) - install it
* Restart Home Assistant

{% endif %}
  
### Configuration:

* Go to Configuration -> Integrations
* Click `Add Integration`
* Search for `Nuki Lock SDU` (not just `Nuki`, as this is the native integration from Home Assistant) and select it
* It will automatically enter the Home Assistant internal URL
* Provide web API token and click Submit
  
  
#### Web API Token:
* Go to the Nuki Web API management site at https://web.nuki.io/
* Nuki Web needs to be activated in the Nuki app - there is a link on the site that tells you how to do that
* Once activated, login on the web
* In the menu on the left, select API
* Click `Generate API token`
* Give it a name, leave the other settings as they are and click Save
* Copy the token and save it in a secure place. It will only be shown this once to you.
  
  
## Usage:

### Devices:

The integration provides several devices and entities to Home Assistant, depending on your setup. For example:

| Device            | Description                                                                                     |
|-------------------|-------------------------------------------------------------------------------------------------|
| Nuki Lock         | Providing one `lock` entity, three state sensors and eight diagnostic sensors about the lock.   |
| Nuki Web API      | Providing configuration `switch` entities for access permissions as set in the Nuki app.        |

  
### Entities:
  
#### Nuki Lock:

The entity IDs depend on the Nuki names of the lock. In the example below, it is `Wohnung`.

| Entity ID                                      | Type        | Description                                     |
|------------------------------------------------|-------------|-------------------------------------------------|
| lock.nuki_wohnung_lock                         | Control     | The main entity to control the lock             |
| binary_sensor.nuki_wohnung_door_open           | Sensor      | Shows the state of the door                     |
| binary_sensor.nuki_wohnung_locked              | Sensor      | Shows the state of the lock                     |
| sensor.nuki_wohnung_door_security_state        | Sensor      | Combines the state of the door with the lock    |
| sensor.nuki_wohnung_battery                    | Diagnostic  | Shows the battery level of the lock             |
| binary_sensor.nuki_wohnung_battery_charging    | Diagnostic  | Shows if the battery is currently charging      |
| binary_sensor.nuki_wohnung_battery_critical    | Diagnostic  | Shows if the battery has a critical level       |
| sensor.nuki_wohnung_door_state                 | Diagnostic  | Shows the state of the door                     |
| sensor.nuki_wohnung_firmware_version           | Diagnostic  | Shows the current firmware of the lock          |
| binary_sensor.nuki_wohnung_keypad_battery_critical | Diagnostic | Shows if the battery of the keypad has a critical level |
| sensor.nuki_wohnung_rssi                       | Diagnostic  | Shows the received signal strength indicator of the lock   |
| sensor.nuki_wohnung_state                      | Diagnostic  | Shows the state of the lock                     |
  
  
#### Nuki Web API:

The entity IDs depend on the authorization you have given to your devices. There will be as many `switch` entities as
there are authorizations stored on the Nuki platform. While they are all named `switch.nuki_` followed by a descriptive
name, there are three different types:

| Type                                      | Example                                          |
|-------------------------------------------|--------------------------------------------------|
| Authorization of local devices            | The keypad, which is granted access to the lock  |
| Authorization of access codes             | A code registered with the keypad                |
| Authorization of apps                     | Access granted to members of the family          |
  
  
### Services:

The integration provides the following services:
  
  
#### Service `lock.lock` 

* For a Nuki Lock, this locks the door

The attribute should appear as a `target` for the service.

| Target attribute    | Optional | Description                                           |
|---------------------|----------|-------------------------------------------------------|
| `entity_id`         |       no | Entity of the relevant lock.                          |
  
  
#### Service `lock.unlock` 

* For a Nuki Lock, this unlocks the door

The attribute should appear as a `target` for the service.

| Target attribute    | Optional | Description                                           |
|---------------------|----------|-------------------------------------------------------|
| `entity_id`         |       no | Entity of the relevant lock.                          |
  
  
#### Service `lock.open` 

* For a Nuki Lock, this unlatches the door

The attribute should appear as a `target` for the service.

| Target attribute    | Optional | Description                                           |
|---------------------|----------|-------------------------------------------------------|
| `entity_id`         |       no | Entity of the relevant lock.                          |
  
  
  

## Useful tips

### Open/unlatch Nuki lock via UI

Even though the component supports the `lock.open` service and advertises support of it, Lovelace UI doesn't show any controls to trigger. This can be achieved via simple script similar to the one below:
```yaml
alias: Nuki Lock Open
sequence:
  - device_id: 8d159025411a270ecb9024794bc54361
    domain: lock
    entity_id: lock.nuki_front_door_lock
    type: open
mode: single
icon: mdi:lock-open
```

or manually calling the service:
```yaml
type: button
entity: lock.nuki_front_door_lock
tap_action:
  action: call-service
  service: lock.open
  service_data: {}
  target:
    entity_id: lock.nuki_front_door_lock
name: Nuki
```
