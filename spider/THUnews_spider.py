#-*- coding:utf-8 -*-


import logging
import requests
from bs4 import BeautifulSoup
from gevent import monkey,sleep
from gevent.pool import Pool
from queue import Queue
import time
import re
import pickle
import lxml
from lxml import etree
import pandas as pd
import pprint

monkey.patch_all()

def get_logger():
    """
    创建日志实例
    """
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    logger = logging.getLogger("monitor")
    logger.setLevel(LOG_LEVEL)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

LOG_LEVEL = logging.INFO    # 日志等级
POOL_MAXSIZE = 8  # 线程池最大容量
logger = get_logger()

START_URL = 'http://news.tsinghua.edu.cn/publish/thunews/9649/index_{}.html'
HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
}

class THUspider:
    '''
    一只可爱的清华小爬虫
    '''

    def __init__(self):
        self.count = 1 #记录当前爬取的数据数
        self.ID = []
        self.set = set()
        self.page = [] #网页
        self.dict = {
            'title': [],
            'time': [],
            'content': [],
            'url': []
        }
        # self.title = [] #标题
        # self.time = []
        # self.content = []

        self.desc_url_queue = Queue()  # 线程池队列
        self.pool = Pool(POOL_MAXSIZE)  # 线程池管理线程,最大协程数

    def spider(self):
        '''
        爬虫入口
        :return:
        '''
        urls = [START_URL.format(p) for p in range(1,573)]
        #共573页
        for url in urls:
            logger.info("爬取第 {} 页".format(urls.index(url) + 1))
            html = requests.get(url=url, headers=HEADERS)
            if html.status_code!=200:
                if urls.index(url)==0:
                    html = requests.get(url='http://news.tsinghua.edu.cn/publish/thunews/9649/index.html', headers=HEADERS)
                else:
                    print('page',urls.index(url)+1,html.status_code)
            html = html.content.decode('utf8')
            bs = BeautifulSoup(html,'lxml')
            news = bs.find_all('a','jiequ')
            for new in news:
                self.desc_url_queue.put(new['href'])
                #print(new['href'])
        #打印队列长度
        logger.info("队列长度为 {} ".format(self.desc_url_queue.qsize()))

    def news_get(self):
        '''
        爬取新闻的详细信息
        '''
        while True:
            url = self.desc_url_queue.get()
            html = requests.get(url='http://news.tsinghua.edu.cn'+url, headers = HEADERS)
            print('count=',self.count,' code=',html.status_code)
            if html.status_code == 200:
                webpage = html.content.decode('utf8')
                try:
                    tree = etree.HTML(webpage)
                    #title = re.search(r'<title>([^<]+)</title>',webpage).group(1)
                    title = tree.xpath('/html/head/title')[0].text
                    time_all = tree.xpath('/html/body/div[1]/div/section[1]/article/div/div/text()')[0].replace(u'\u3000',u' ').strip()
                    time = time_all.split(' ')[0].replace('年','.').replace('月','.').replace('日','.')[:10]
                    content_list = tree.xpath('/html/body/div[1]/div/section[1]/article/p/text()')
                    content = ''.join(content_list)
                    print(title,time)
                    #self.page.append(webpage)
                    #self.ID.append(url)
                    self.dict['title'].append(title)
                    self.dict['time'].append(time)
                    self.dict['content'].append(content)
                    self.dict['url'].append('http://news.tsinghua.edu.cn'+url)
                    self.count += 1
                except:
                    print('ERROR IN: '+'http://news.tsinghua.edu.cn'+url)
            self.desc_url_queue.task_done()

    def execute_more_tasks(self, target):
        """
        协程池接收请求任务,可以扩展把解析,存储耗时操作加入各自队列,效率最大化

        :param target: 任务函数
        :param count: 启动线程数量
        """
        for i in range(POOL_MAXSIZE):
            self.pool.apply_async(target)

    def create_csv(self):
        self.dict['ID']=list(range(1,len(self.dict['url'])+1))
        print(self.dict)
        myData = pd.DataFrame(self.dict)
        myData.to_csv('myData.csv',index = False,encoding='utf8',columns=['ID','title','time','url','content'])


    def save_data(self):
        # try:
        #     with open("IDFile.pickle", "wb") as IDFile:
        #         pickle.dump(self.ID, IDFile)
        # except IOError:
        #     print("Can't open the file: IDFile.pickle")

        try:
            with open('DictFile.pickle', 'wb') as DictFile:
                pickle.dump(self.dict, DictFile)
        except IOError:
            print("Can't open the file: DictFile.pickle")



    def run(self):
        """
        多线程爬取数据
        """
        self.spider()
        self.execute_more_tasks(self.news_get)
        self.desc_url_queue.join()  # 主线程阻塞,等待队列清空
        self.create_csv()
        self.save_data()

if __name__ == "__main__":
    spider = THUspider()

    start = time.time()
    spider.run()
    logger.info("总耗时 {} 秒".format(time.time() - start))