## saucelab-api-client ##

saucelab-api-client - is a client for provide integration with SauceLab

General information about [SauceLab Api](https://docs.saucelabs.com/dev/api/)

**Requirements**

- requests

**Installation**

```shell
pip install saucelab-api-client
```

**Configuration**
Starting from version 0.3 you can configure saucelab client credentials with 3 way:

Way 1. Directly set credentials in class constructor

```shell
from saucelab_api_client.saucelab_api_client import SauceLab
saucelab = SauceLab('your_host', 'your_username', 'your_token')
```

Way 2. Set credentials in pytest.ini or in saucelab.ini This files must be in root folder project path Add
group [saucelab]
Add variables:
- **saucelab_username**
- **saucelab_token**
- **saucelab_host**

Example **pytest.ini** or **saucelab.ini**

```shell
[saucelab]
saucelab_username = your_username
saucelab_token = your_token
saucelab_host = your_host
```

When you add credentials to ini file:

```shell
from saucelab_api_client.saucelab_api_client import SauceLab
saucelab = SauceLab()
```

Way 3. You can set environment variables:

- SAUCELAB_USERNAME
- SAUCELAB_TOKEN
- SAUCELAB_HOST

When you add credentials to environment variables:

```shell
from saucelab_api_client.saucelab_api_client import SauceLab
saucelab = SauceLab()
```

**Features in version: 0.5**

- Supported api:
    - accounts
    - platform
    - real devices
    - real devices jobs
    - jobs
    - storage
    - sauce connect
- Powerful device filter - saucelab.devices.filter_devices()
- Added list support for parameters in devices filter
- Added driver generation
- Added base64 credentials encoding

**TODO**

- Add support:
    - performance

**Usage examples**

```shell
teams = saucelab.accounts.account_team.teams()
devices = saucelab.devices.filter_devices(min_os_version='14.4.1', max_os_version='14.9')
apps = saucelab.storage.files()
```
