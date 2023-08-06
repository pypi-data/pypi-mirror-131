# serviceregistry
Service Registry for python apps

For instance during the lifecycle of the application you want 2 things:
1. store system variables
2. store service with certain initialization code and initialize them on boot of the application

let's look an example to understand this further..

# installation
pip install serviceregistry

# how to use

```python

from serviceregistry.services import Container, Registry
import meerkat.configurations.app.settings

def create_container(app):
    container = Container()

    container.set(settings.Props.FALCON, app)
    return container


def boot(container):
    service_registry = Registry()

    for service in settings.services:
        service_registry.register(service)

    service_registry.boot(container)


container = create_container(create_app())
boot(container)


```

here we define the props enum as constants to a system vars

```python
# settings.py
from serviceregistry.services import Props as BaseProps

services = [
    LoggingService(),
    EnvironmentService(),
]


class Props(BaseProps):
    DI_PROVIDER = 0
    FALCON = 1

    APP_URL = "APP_URL"

    MONGO_HOST = "MONGO_HOST"
    MONGO_PORT = "MONGO_PORT"
    MONGO_DB = "MONGO_DB"
```

and here is the environment service, which registers certain system variables from environment variables

```python
import os

from serviceregistry.services import BootableService, Container


class EnvironmentService(BootableService):
    def boot(self, container: Container):
        from meerkat.configurations.app.settings import Props

        container.set(Props.APP_URL, os.environ.get(Props.APP_URL.value))

        container.set(Props.MONGO_HOST, os.environ.get(Props.MONGO_HOST.value))
        container.set(Props.MONGO_PORT, os.environ.get(Props.MONGO_PORT.value))
        container.set(Props.MONGO_DB, os.environ.get(Props.MONGO_DB.value))

```

Logging service

```python
import logging as registry_logging

import sys
import serviceregistry.services


class LoggingService(serviceregistry.services.BootableService):
    def boot(self):
        registry_logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=registry_logging.DEBUG,
        )

        registry_logging.getLogger().addHandler(
            registry_logging.StreamHandler(sys.stdout)
        )

```
