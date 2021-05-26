import json
import os
import sys
import requests
from collections import OrderedDict
from pprint import pprint

from rest_framework.response import Response



# 유명인 찾기
client_id = "QqPmapr9zfg_3Fi05iIn"
client_secret = "awJxrIA5Np"
# url = "https://openapi.naver.com/v1/vision/face" # 얼굴감지
url = "https://openapi.naver.com/v1/vision/celebrity" # 유명인 얼굴인식
files = {'image': open('박최.png', 'rb')}
headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
response = requests.post(url,  files=files, headers=headers)
rescode = response.status_code

response_data = json.loads(response.text)
ordered_data = sorted(response_data["faces"], key=lambda x:x['celebrity']['confidence'], reverse=True)
actor_name = ordered_data[0]['celebrity']['value']
actor_confidence = ordered_data[0]['celebrity']['confidence']
if(rescode==200):
    print (response_data['faces'])
    # print (ordered_data[v])
    # print (response_data['info'])
else:
    print("Error Code:" + rescode)

# print(actor_name)
apikey = '1f4ac8ec8d56852461c1bf865cdc05a1'
movie_list = range(1)
mylist = []
cnt = 1
file_data = OrderedDict()
url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json"
param = {
    'key' : apikey,
    'peopleNm' : actor_name,    
}
r = requests.get(url, params= param)
data = json.loads(r.text)
movie_list = []
for person in data['peopleListResult']['peopleList']:
    if person['repRoleNm'] == '배우':
        listmovies = list(map(str,person['filmoNames'].split('|')))
        movie_list += listmovies
# print(movies)

context = {
    'movie_list': movie_list,
    'actor_name': actor_name,
    'actor_confidence': actor_confidence
}
print(context)
return Response(context)