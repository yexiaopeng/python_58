# -*- coding: UTF-8 -*-
import requests
import re
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class spider(object):
    def __init__(self):
        print("开始获取页面url")

    # 获取页面的 html 代码数据
    def getSource(self,url):
        html = requests.get(url)
        return html.text
    # 替换 url中的页面编号，生成 “下一页” 的url
    def changePage(self,url,total_page):
        now_page = int(re.search('pn(\d+)', url, re.S).group(1))
        page_group = []
        for i in range(now_page, total_page + 1):
            link = re.sub('pn\d+', 'pn%s' % i, url, re.S)
            page_group.append(link)
        return page_group

    # 根据正则表达式，获取页面数据中的有用信息
    def getEveryClass(self,source):
        everyclassBig = re.findall(r'fuzhou.58.com/huishou/(.*?).shtml',source,re.S)
        infoAdd = []
        ids = list(set(everyclassBig))
        for each in  ids:
            # everyclass = re.findall(r'<a href=\'(.*?)\'', each, re.S)
            infoAdd.append(each)
        return  infoAdd

    # 存储最终的有用信息
    def saveInfo(self,eachclass):
        f = open(u'全抚州手机回收信息', 'a')
        i = 0
        for each in eachclass:
            f.writelines (each['name'])
            f.writelines (',')
            f.writelines(each['pone'])
            f.writelines('\n')
        f.close()


if __name__ == '__main__':

    # 存储商家信息页面的 url
    getBussineDataUrlInfo = []
    dataaa = []
    bussineDataUrlInfo = []
    f = open(u'全抚州手机回收信息', 'a')
    f.close()
    os.remove(u'全抚州手机回收信息')

    # 手机回收信息的第一个页面
    firstUrl = 'http://fuzhou.58.com/ershoushichang/pn1/'
    # new spider
    fiveEightSpider = spider()
    # 遍历 “下一页"
    allLink = fiveEightSpider.changePage(firstUrl,40)
    # 处理 allLink 存储的每一个页面

    for link in allLink:
        print("正在处理的页面:"+link)
        html = fiveEightSpider.getSource(link)
        everyclass = fiveEightSpider.getEveryClass(html)
        # 截取 所有商家信息显示的页面
        for each in everyclass:
            getBussineDataUrlInfo.append(each)

            # 调试存储
            # f = open('info.txt', 'a')
            # for each in getBussineDataUrlInfo:
            #     for eeach in each:
            #         f.writelines('url:' + eeach + '\n')
            # f.close()

    # 访问每一个商家信息显示的页面 获取商家的信息
    num = 0
    idsnew = list(set(getBussineDataUrlInfo))
    for each in idsnew:
        num = num + 1
        print("NO",num)

        # 商家信息字典  姓名 name 联系方式 pone 服务区域 workplace 类型 workType
        bussineDict = {}
        html_new = "http://fuzhou.58.com/huishou/"+each+".shtml"
        bussInfoHtml = requests.get(html_new)
        name = re.findall(r'linkman:\'(.*?)\'',bussInfoHtml.text,re.S)
        pone = re.findall(r'<span class="l_phone">(.*?)<em>',bussInfoHtml.text,re.S)
        bussineDict['name'] = name
        bussineDict['pone'] = pone
        dataaa.append(bussineDict)

    fiveEightSpider.saveInfo(dataaa)


    # fiveEightSpider.saveInfo(getBussineDataUrlInfo)
