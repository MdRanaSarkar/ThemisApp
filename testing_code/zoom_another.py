import json
from zoomus import ZoomClient
from datetime import datetime

ZOOM_API_KEY = "amEtAmG9SK2FAidkZCkgDA"
ZOOM_API_SECRET = "DZpquK0GVaojqTwnALdjI3xE5HHMc7L6"


client = ZoomClient(ZOOM_API_KEY, ZOOM_API_SECRET)

client.meeting.create(user_id='UserId from above API response', topic='My New Meeting', start_time=datetime.now())

# Find if Meeting got created
user_list = json.loads(client.user.list().content)
for user in user_list['users']:
    user_id = user['id']
    meetings = client.meeting.list(user_id=user_id).content
    print(json.loads(meetings))