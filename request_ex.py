import requests
import base64
import time


resp = requests.post('http://127.0.0.1:5000/upscale', params={
    'input_path': 'lama_300px.png',
    'output_path': 'lama_600px.png'
})
resp_data = resp.json()
print(resp_data)
task_id = resp_data.get('task_id')
print(task_id)
#

# status = 'PENDING'
#
# while status not in {'SUCCESS', 'FAILURE'}:
#     response = requests.get(f'http://127.0.0.1:5000/upscale/{task_id}').json()
#     status = response['status']
#     result = response['result']
#     print(result, status)
#
# resp = requests.get(f'http://127.0.0.1:5000/upscale/{task_id}')
# print(resp.json())
# time.sleep(3)
# #
# resp = requests.get(f'http://127.0.0.1:5000/upscale/{task_id}')
# print(resp.json())
# #
# #
# file = 'lama_600px.png'
# #
# resp = requests.get(
#     f'http://127.0.0.1:5000//upscale/processed/{file}')
#
# print(resp.json())
