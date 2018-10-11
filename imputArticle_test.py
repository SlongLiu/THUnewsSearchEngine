#-*- coding:utf-8 -*-

import pickle

#文章数据
# article = {
#     'ID': [1,2,3,4,5],
#     'title': ['大桑娜','大','丰富','二维','分到'],
#     'time': ['2013.09.20','2018.08.03','2014.03.06','2015.10.30','2017.06.06'],
#     'content': ['dasdoasdjsa\nagfd',
#                 'sdoasjdasd\nfkjfaoosf',
#                 'dopjfofsfiosdoisdfnsdofndsovnds',
#                 'dkopkfposjfmpodsjfpodsjfpodsjfpodsjposdjvpodsjvdsf',
#                 'djwujqdjiodjsifndjskfnsut339r3n fdiew9iro ewini wj 2 '],
#     'url':['https://www.cnblogs.com/cindy-cindy/p/6720196.html',
#            'https://www.cnblogs.com/vampirejt/p/4159267.html',
#            'https://blog.csdn.net/tulip527/article/details/8737835',
#            'https://blog.csdn.net/xjian32123/article/details/78964085',
#            'https://github.com/marcobiedermann/search-engine-optimization']
# }
with open('spider/Dict.pickle','rb') as DictTest:
    article = pickle.load(DictTest)
print(article)

# from django.conf import settings
# settings.configure()

import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myProject2.settings")
django.setup()

import datetime
import pprint
from searchEngine.models import Article
# import django
# django.setup()
while True:
    num = article['time'].count('')
    if num==0:
        break
    else:
        pos = article['time'].index('')
        article['time'][pos]='2018.09.18' #ddl

article['time'] = [datetime.datetime.strptime(p[:10], '%Y.%m.%d') for p in article['time'] ]
pprint.pprint(article)
for x in article['ID']:
    Article.objects.get_or_create(m_ID=x,
                       m_url=article['url'][x-1],
                       m_title=article['title'][x-1],
                       m_time=article['time'][x-1],
                       m_content=article['content'][x-1])
    print(x)

