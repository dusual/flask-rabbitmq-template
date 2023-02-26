import requests
import random

payload = {
	"device_id": "abc",
	"client_id": "abc",
	"created_at": "2023-02-07 14:56:49.386042",
	"data": {
		"license_id": "abc",
		"preds": [
			{
				"image_frame": "YWRhZGFzZGFzZA==",
				"prob": 0.21,
                "tags": ["abc", "def"]
			},
			{
				"image_frame": "YWRhZGFzZGFzZA==",
				"prob": 0.21,
                "tags": ["abc", "def"]
			}
		]
	}
}

for i in range(1000):
	payload['data']['preds'][0]['prob'] = random.uniform(0, 1)
	payload['data']['preds'][1]['prob'] = random.uniform(0, 1)
	r = requests.post("http://localhost:8000/executor", json=payload)
	print(r.status_code)
	print(r.text)