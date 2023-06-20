import requests
import json
def nuditydetectionresult(img_dir):
    params = {
    'models': 'nudity-2.0',
    'api_user': '708482299',
    'api_secret': 'WWGyXX67SuGr2qE8JMmm'
    }
    # files = {'media': open(img_dir, 'rb')}
    files = open(img_dir)
    r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)

    output = json.loads(r.text)
    return output
