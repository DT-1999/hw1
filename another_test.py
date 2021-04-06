# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 13:58:31 2021

@author: ustc
"""
from flask import Flask, render_template
import requests
import json
import time
import random
import re
from bs4 import BeautifulSoup

def getjson(location,page_num=0):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.16) Gecko/20201130 Firefox/3.5.16'}
    restaurant = {'q':'美食',
                  'region': location,
                  'scope': '2',
                  'page-size':20,
                  'page_num': page_num,
                  'output':'json',
                  #'ak':'8Aoqw1l43V8GTCniw0coFWVPVBgPYRjO'
                  'ak':'DDtVK6HPruSSkqHRj5gTk0rc'
                  }
    r = requests.get("http://api.map.baidu.com/place/v2/search",params=restaurant,headers= headers)
    decodejson = json.loads(r.text)
    #print(decodejson)
    return decodejson


class resturants_of_city:
    def __init__ (self,city,region1,region2,region3,region4):
        self.city = city
        self.region1 = region1
        self.region2 = region2
        self.region3 = region3
        self.region4 = region4  
        
    def search_and_show(self):
        region_list = {self.region1,self.region2,self.region3,self.region4}
        best1=most_popular1=most_expensive1={'rank':1,'name':'0','image':'0','address':'0','price':0,'overall_rating':0,'comment_num':0}
        best2=most_popular2=most_expensive2={'rank':2,'name':'0','image':'0','address':'0','price':0,'overall_rating':0,'comment_num':0}
        best3=most_popular3=most_expensive3={'rank':3,'name':'0','image':'0','address':'0','price':0,'overall_rating':0,'comment_num':0}
        
        for each_region in region_list:
            not_last_page = True
            page_num = 0
            while not_last_page:
                decodejson = getjson(self.city + each_region,page_num)
                print(each_region,page_num)
                time.sleep(random.random())#restriction of baidu API
                try:
                    decodejson['total']       #last page 
                    if decodejson['total']!=0:
                        for each_place in decodejson['results']:
                            place = each_place['name']
                            address = each_place['address']
                            try:
                                price = float(each_place['detail_info']['price']  )  #dictionary in dictionary
                            except:
                                price = 0
                            try:
                                rating = float(each_place['detail_info']['overall_rating'] )   
                            except:
                                rating = 0
                            try:
                                comment_num = int(each_place['detail_info']['comment_num'] )   
                            except:
                                comment_num = 0
                            
                            output = '\t'.join([place,address,str(price),str(rating),str(comment_num)]) + '\r\n'
                            #print(output)
                            with open('restaurants.txt', 'a+', encoding='UTF-8') as f:
                                f.write(output)
                                f.close()
                            
                            new={'rank':0,'name':place,'image':'0','address':address,'price':price,'overall_rating':rating,'comment_num':comment_num}
                            
                            if price>=most_expensive1['price']:
                               most_expensive3 = most_expensive2
                               most_expensive2 = most_expensive1
                               most_expensive1 = new
                            elif price>=most_expensive2['price']:
                               most_expensive3 = most_expensive2
                               most_expensive2 = new 
                            elif price>=most_expensive3['price']:
                               most_expensive3 = new                        
        
                            if rating>=best1['overall_rating']:
                                best3 = best2
                                best2 = best1
                                best1 = new
                            elif rating>=best2['overall_rating']:
                                best3 = best2
                                best2 = new
                            elif rating>=best3['overall_rating']:
                                best3 =new
        
                            if comment_num>=most_popular1['comment_num']:
                               most_popular3 = most_popular2
                               most_popular2 = most_popular1
                               most_popular1 = new
                            elif comment_num>=most_popular2['comment_num']:
                               most_popular3 = most_popular2
                               most_popular2 = new
                            elif comment_num>=most_popular3['comment_num']:
                               most_popular3 = new                                       
                            
                        page_num=page_num+1
                    else:
                        not_last_page = False
                except:
                    not_last_page = False
       
        best1['rank']=most_popular1['rank']=most_expensive1['rank']=1
        best2['rank']=most_popular2['rank']=most_expensive2['rank']=2
        best3['rank']=most_popular3['rank']=most_expensive3['rank']=3
        
        new = [most_expensive1['name'],most_expensive2['name'],most_expensive3['name'],most_popular1['name'],most_popular2['name'],most_popular3['name'],best1['name'],best2['name'],best3['name']]
        
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT6.1; en-US; rv:1.9.1.6) Gecko/20201201 Firefox/3.5.6'}
        cookie="fspop=test; cye=hefei; _lxsdk_cuid=178970e9127c8-0a7e2614614ad4-4c3f237d-144000-178970e9127c8; _lxsdk=178970e9127c8-0a7e2614614ad4-4c3f237d-144000-178970e9127c8; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1617540449,1617603737,1617612171,1617712454; _hc.v=2d291f0f-f5e3-68c0-5121-15b43625688f.1617442019; s_ViewType=10; cy=110; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=178a72d1497-b7-792-6c3%7C%7C105; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1617712942"
        cookie_dict = {i.split("=")[0]:i.split("=")[-1] for i in cookie.split("; ")}
        
        i=0
        str2 = ['0']*10
        for name in new:
            link = 'https://www.dianping.com/search/keyword/110/0_' + name    
            proxies ={'http':'http://49.70.17.135'}
            response =requests.get(link, proxies=proxies)
            r = requests.get(link, headers =headers, cookies =cookie_dict, timeout=1)
            soup = BeautifulSoup(r.text,"lxml")
            time.sleep(random.random())
            html =r.text
            #print(html)
            try:
                result = re.search('src="https://.*?/>',html)
                str1 = result.group()
            except:
                result = re.search('src="http://.*?/>',html)
                str1 = result.group()

            str1=str1.lstrip('src="')
            str1=str1.rstrip('"/>')
            print(name)
            print(str1)
            str2[i]=str1
            i=i+1
        
        most_popular = [most_popular1,most_popular2,most_popular3]
        most_expensive = [most_expensive1,most_expensive2,most_expensive3]
        best = [best1,best2,best3]
        i=0
        
        for a in most_expensive: 
            a['image']=str2[i]
            i=i+1
        
        for a in most_popular: 
            a['image']=str2[i]
            i=i+1    
        
        for a in best: 
            a['image']=str2[i]
            i=i+1    
    
        print(most_popular)
        print(most_expensive)
        print(best)
        
        app = Flask(__name__)
        
        @app.route("/")
        def index():
            return render_template('index.html')
        @app.route("/best")
        def index1():
            return render_template('module1.html', restaurants=best)
        @app.route("/most_popular")
        def index2():
            return render_template('module1.html', restaurants=most_popular)
        @app.route("/most_expensive")
        def index3():
            return render_template('module1.html', restaurants=most_expensive)                       

        app.run()
        
if __name__=="main":
    print('??')