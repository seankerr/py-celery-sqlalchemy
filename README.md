# celery-sqlalchemy

SQLAlchemy model serialization for celery.

### Install

```sh
pip install celery-sqlalchemy
```

### How does it work?

Any model or list of models passed to a celery task as a direct argument will be
serialized/deserialized by the `json+sqlalchemy` content type serializer provided by
`celery-sqlalchemy`.

### Behind the scenes

The [orjson](https://github.com/ijl/orjson) library is used behind the scenes to handle
serialization of Python types.

### Usage

By default `celery-sqlalchemy` will configure Celery to use the `json+sqlalchemy`
content type for all tasks and no further configuration is needed.

```python
from celery_sqlalchemy import initialize

# setup celery
celery = ...

# initialize celery-sqlalchemy
initialize(celery)

# dispatch a task
task.delay(Model())
```

### Using the json+sqlalchemy content type in combination with other content types

The first way of doing this is by specifying the `json+sqlalchemy` content type as
the default task serializer.

```python
from celery_sqlalchemy import initialize

# setup celery
celery = ...

# initialize celery-sqlalchemy without the `apply_serializer` setting
initialize(celery, apply_serializer=False)

# combine the json+sqlalchemy content type with your other content types
celery.conf.accept_content = ["json+sqlalchemy", "your content type"]
celery.conf.result_accept_content = ["json+sqlalchemy", "your content type"]

# set the default task serializer
celery.conf.task_serializer = "json+sqlalchemy"

# dispatch a model task
task.delay(Model())

# dispatch a task using another content type
author = "Alan Watts"
title = "Become What You Are"

task.apply_async((author, title), serializer="your content type")
```

The other way of doing this is by not specifying the default task serializer, and
instead using `apply_async()` to dispatch all tasks.

```python
from celery_sqlalchemy import initialize

# setup celery
celery = ...

# initialize celery-sqlalchemy without the `apply_serializer` setting
initialize(celery, apply_serializer=False)

# combine the json+sqlalchemy content type with your other content types
celery.conf.accept_content = ["json+sqlalchemy", "your content type"]
celery.conf.result_accept_content = ["json+sqlalchemy", "your content type"]

# dispatch a model task
task.apply_async((Model(), Model()), serializer="json+sqlalchemy")

# dispatch a task using another content type
author = "Alan Watts"
title = "Become What You Are"

task.apply_async((author, title), serializer="your content type")
```

### Changelog

- **0.1.0**
  - Initial version with support for common Python types.
