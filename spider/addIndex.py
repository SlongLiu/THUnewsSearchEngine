#-*- coding:utf-8 -*-
import jieba
import pickle
import re
from pprint import *

#打开原始文件
with open('DictFile2.pickle','rb') as DictFile2:
    Dict2 = pickle.load(DictFile2)
print(Dict2)

with open('DictFile.pickle','rb') as DictFile:
    Dict = pickle.load(DictFile)
print(Dict)

Dict['url'].extend(Dict2['url'])
Dict['title'].extend(Dict2['title'])
Dict['content'].extend(Dict2['content'])
Dict['time'].extend(Dict2['time'])
Dict['ID'] = list(range(1,len(Dict['url'])+1))
print(len(Dict['url']))

try:
    with open('DictAll.pickle', 'wb') as DictTest:
        pickle.dump(Dict, DictTest)
except IOError:
    print("Can't open the file: DictTest.pickle")

# IDmini = Dict['ID'][:100]
# titlemini = Dict['title'][:100]
# timemini = Dict['time'][:100]
# contentmini = Dict['content'][:100]
# urlmini = Dict['url'][:100]
#
# dictmini = {
#     'ID': IDmini,
#     'title': titlemini,
#     'time': timemini,
#     'content': contentmini,
#     'url': urlmini
# }
#
# try:
#     with open('DictTest.pickle', 'wb') as DictTest:
#         pickle.dump(dictmini, DictTest)
# except IOError:
#     print("Can't open the file: DictTest.pickle")

# with open('DictTest.pickle','rb') as DictTest:
#     Dict = pickle.load(DictTest)
# print(Dict)


# 建立索引
wordMap = {}
for x in Dict['ID']:
    if(x%100==0):
        print("已完成{}项".format(x))
    Dict['content'][x-1] = re.sub(r'\s+', '', Dict['content'][x-1], re.S)
    Dict['title'][x-1] = re.sub(r'\s+', '', Dict['title'][x-1], re.S)
    words = jieba.lcut_for_search(Dict['content'][x-1])
    words_title = jieba.lcut_for_search(Dict['title'][x-1])
    words.extend(words_title)
    #print(words)
    try:
        words = list(set(words))
        for each in words:
            if wordMap.__contains__(each):
                wordMap[each].append(x)
            else:
                wordMap[each] = [x,]
    except:
        print('第{}项出现错误',x)
        continue

#存储索引表
try:
    with open('Map.pickle', 'wb') as Map:
        pickle.dump(wordMap, Map)
except IOError:
    print("Can't open the file: MapTest.pickle")

pprint(wordMap)


