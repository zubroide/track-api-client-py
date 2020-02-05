## Python client for track-api

Available methods list specified in track-api swagger
https://gitlab.com/zubroid/omnicomm/track-api

### Installation
Install "track-api-client-py" via pip, add it to requirements.txt

### Usage
```python
from track_api_client.client import ApiClient as TrackApiClient
client = TrackApiClient(
    'http://track_api_domain/api/v1/track/',
    'secret_key'
)
r = client.get_track_points(terminal_id=1, start_at=1, limit=3)
print(r)
```