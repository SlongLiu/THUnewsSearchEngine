from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
import jieba
from functools import reduce
from .models import Article,Word
import datetime,time
# Create your views here.

def redtitle(text, wordlist):
    newtext = text
    for word in wordlist:
        if newtext.find(word) != -1:
            newtext = newtext.replace(word, '<font color="#FF3300">'+word+'</font>')
    return newtext

def redcontent(text, wordlist):
    newtext = text
    length = len(text)
    minpos = length+10
    for word in wordlist:
        tmp = newtext.find(word)
        if tmp != -1:
            if tmp < minpos:
                minpos = tmp
    if (minpos > 20) & (minpos < length+1):
        newtext = '...'+newtext[minpos-20:minpos+180]+'...'
    else:
        newtext = newtext[0:200]+'...'
    for word in wordlist:
        if newtext.find(word) != -1:
            newtext = newtext.replace(word, '<font color="#FF3300">'+word+'</font>')
    #print(newtext)
    return newtext


def result(request, text, starttime, endtime):
    # return render(request, 'index.html')
    print('in result:',text,starttime,endtime)
    wordList = text.strip().split(' ')
    searchList = []
    articleList = set()
    for x in wordList:
        searchList.extend(jieba.lcut(x))
    searchList = list(set(searchList))
    #单词的列表
    for x in searchList:
        try:
            curWord = Word.objects.get(pk=x)
        except:
            continue
        if articleList:
            articleList = articleList & set(curWord.m_article.filter(m_time__range=(starttime,endtime)))
        else:
            articleList = set(curWord.m_article.filter(m_time__range=(starttime,endtime)))
    articleList = list(articleList)
    #生成文章结果的列表
    articleList = sorted(articleList, key=lambda x: x.m_time, reverse=True)
    lengthArticle = len(articleList)
    if lengthArticle:
        dicts = [{
            'url': each.m_url,
            'title': redtitle(each.m_title, wordList),
            'content': redcontent(each.m_content, wordList),
        } for each in articleList]
        # 显示红色文字
        print(dicts)
        paginator = Paginator(dicts, 20)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)

        return render(request, 'result.html', {
            'num': lengthArticle,
            'text': text,
            'starttime': starttime,
            'endtime': endtime,
            'contacts': contacts
        })
    else:
        return render(request,'notfound.html')




def search(request):
    if request.method=='GET':
        return render(request,'index.html')
    else:
        text = request.POST.get('text', None)
        label = request.POST.get('select', None)
        starttime = request.POST.get('starttime', None)
        endtime = request.POST.get('endtime', None)
        print(starttime,endtime)
        if starttime=='':
            starttime = '2010-01-01'
        if endtime=='':
            endtime = time.strftime('%Y-%m-%d')
        print('starttime=',starttime,'endtime=',endtime)
        if text:
            return HttpResponseRedirect(reverse('result',args=(text,starttime,endtime)))
        else:
            return render(request, 'index.html')

def index(request):
    return render(request, 'index.html')