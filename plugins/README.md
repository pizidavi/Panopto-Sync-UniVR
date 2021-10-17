# Develop Plugins

## Project Structure

### Plugin folder

```text
- <plugin-name>
    - main.py
    - requirements.txt
```

#### main.py

```python
from utils.logger import get_logger
logger = get_logger(__name__)

class PluginName:  # <- Same name as plugins.json file!
    def __init__(self, options: dict):
        pass

    # event...
```

## Add to plugins.json file

```json
{
  "module": "<Same name as the plugin Class!>",
  "options": {
    ".": 0,
    "..": "",
    "...": []
  },
  "disable": false
}
```

## Object

### Course
```json
{
  "id": 0,
  "name": ""
}
```

### Lesson
```json
{
  "id": "",
  "name": ""
}
```

## Available events

```python
def on_download_started(course: dict, lesson: dict) -> None:
    """
    Event called when the download is started
    :param course: Course object
    :param lesson: Lesson object
    """
    pass
```

```python
def on_download(course: dict, lesson: dict, progress: int) -> None:
    """
    Event called during downloading
    :param course: Course object
    :param lesson: Lesson object
    :param progress: Download's progress | value from 0 to 100
    """
    pass
```

```python
def on_download_completed(course: dict, lesson: dict, output: str) -> None:
    """
    Event called when the download is completed
    :param course: Course object
    :param lesson: Lesson object
    :param output: Path of the downloaded file
    """
    pass
```

```python
def on_download_error(course: dict, lesson: dict, error: Exception) -> None:
    """
    Event called when an error occurs during downloading
    :param course: Course object
    :param lesson: Lesson object
    :param error: Exception
    """
    pass
```

```python
def on_download_done(course: dict, lesson: dict, output: str) -> None:
    """
    Event called when the download is done
    NOTE: Called after "on_download_completed" event
    :param course: Course object
    :param lesson: Lesson object
    :param output: Path of the downloaded file
    """
    pass
```
