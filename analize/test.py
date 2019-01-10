import requests as rq

print(rq.get("https://music.163.com/api/v1/resource/comments/R_SO_4_440310367?offset=0&limit=200").content)