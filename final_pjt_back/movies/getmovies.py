import requests
from tmdb import URLMaker
from pprint import pprint
import json

mykey_url = URLMaker('f9d6437bdf11eed5c220387d6687f409')
url = mykey_url.get_url(region='KR', language='ko')

res = requests.get(url)
movies = res.json()
data = json.loads(res.text)

print(type(movies))
pprint(data)

# Python 객체를 JSON 데이터로 쓰기, 직렬화, 인코딩: json.dumps()
# with open("student_file.json", "w") as json_file:

#     json.dump(student_data, json_file)

file_path = "./moviesdata.json"

with open(file_path, 'w', encoding="utf-8") as outfile:
    
    json.dump(data, outfile, ensure_ascii=False)



