import requests
import re

# 有道词典api接口
api ='https://www.thesaurus.com/browse/'

resp=requests.get(api+'human').content
