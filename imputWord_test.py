#-*- coding:utf-8 -*-

# word = {
#     'dop': [3],
#     't': [5],
#     'as': [1,2],
#     'sd': [1,2,3,4],
#     '大': [1,2],
#     '分到': [5]
# }
import pickle
with open('spider/Map.pickle','rb') as MapTest:
    word = pickle.load(MapTest)
print(len(word))

import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myProject2.settings")
django.setup()

import datetime
import pprint
from searchEngine.models import Article,Word
import time

starttime = time.time()

count = 0
for each_word in word:
    if (count%500==0):
        print('已完成{}项'.format(count),'用时{}秒'.format(time.time() - starttime))
    Word.objects.get_or_create(m_word = each_word)
    count += 1