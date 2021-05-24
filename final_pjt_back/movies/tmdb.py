# import requests

# class URLMaker:    
#     url = 'https://api.themoviedb.org/3'

#     def __init__(self, key):
#         self.key = key

#     def get_url(self, category='movie', feature= 3, **kwargs):
#         url = f'{self.url}/{category}/{feature}'
#         url += f'?api_key={self.key}'

        
#         for k, v in kwargs.items():
#             url += f'&{k}={v}'
#         print(url)
#         return url
        

#     def movie_id(self, title):
#         url = self.get_url('search', 'movie', region='KR', language='ko', query=title)
#         res = requests.get(url)
#         movie = res.json()

#         if len(movie.get('results')):
#             return movie.get('results')[0].get('id')
#         else:
#             return None
from os import name
import requests
import json
from collections import OrderedDict
from pprint import pprint

apikey = 'f9d6437bdf11eed5c220387d6687f409'
movie_list = range(0, 100)
mylist = []
cnt = 1
for num in movie_list:
    try:
        file_data = OrderedDict()
        url = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=ko-kr".format(num, apikey)
        r = requests.get(url)
        data = json.loads(r.text)
        pprint(data)
        video_url = "https://api.themoviedb.org/3/movie/{}/videos?api_key={}".format(num, apikey)
        video_r = requests.get(video_url)
        video_data = json.loads(video_r.text)
        # print(video_data)
        video_id = video_data["results"][-1]["key"]
        
        
        genre_datas = data["genres"]
        genre_ids = []
        for datas in genre_datas:
            genre_ids.append(datas["id"])


        
        print(genre_ids, data["genres"]) 

        
        if len(data["overview"]) > 10 and int(data["release_date"][:4]) >= 1980 and len(data["poster_path"]) > 10 and len(data["backdrop_path"]) > 10:
            print("??")
            file_data['model'] = 'movies.movie'
            file_data["pk"] = cnt
            file_data['fields'] = {
                "title": data["title"],
                "genres" : genre_ids,
                "original_title" : data["original_title"],
                "original_language" : data["original_language"],
                "overview" : data["overview"],
                "adult" : data["adult"],
                "budget" : data["budget"],
                "poster_path" : data["poster_path"],
                "release_date" : data["release_date"],
                "runtime" : data["runtime"],
                "vote_average" : data["vote_average"],
                "video" : video_id,
                "backdrop_path" : data["backdrop_path"],
            }
            mylist.append(file_data)
            cnt += 1
    except:
        pass
    
    with open('./fixtures/moviesdata.json', 'w', encoding="utf-8") as make_file:
        json.dump(mylist, make_file, ensure_ascii=False, indent="\t")