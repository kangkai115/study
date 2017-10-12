#-*-coding utf-8 -*-
import requests
from lxml import etree
import pandas as pd
from urllib import parse
import urllib
import hashlib
import json
import xlrd
def read_add(file):
    wb = xlrd.open_workbook(file)
    sh = wb.sheet_by_index(0)
    columnValueList = sh.col_values(9)
    return columnValueList


def add_to_coordinate(sightlist):
     # 以get请求为例http://api.map.baidu.com/geocoder/v2/?address=百度大厦&output=json&ak=yourak
    ak = 'xlilEwu8BzuBrj8GWLuTGkQSamlCgjVF'
    coordinate_data=[]
    add_error=[]
    i=1
    for add in sightlist:

        print(i,'+',add)
        i+=1
        queryStr = '/geocoder/v2/?address='+add+'&output=json&ak='+ak
        # 对queryStr进行转码，safe内的保留字符不转换
        encodedStr = urllib.parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
        # 在最后直接追加上yoursk
        rawStr = encodedStr + 'ZQix2AjX8tr7ohDuLusyMLDKoYaYHRzC'
        # md5计算出的sn值7de5a22212ffaa9e326444c75a58f9a0
        # 最终合法请求url是http://api.map.baidu.com/geocoder/v2/?address=百度大厦&output=json&ak=yourak&sn=7de5a22212ffaa9e326444c75a58f9a0
        coordinate=hashlib.md5(urllib.parse.quote_plus(rawStr).encode('utf-8')).hexdigest()
        get_coordinate_url='http://api.map.baidu.com/geocoder/v2/?address='+add+'&output=json&ak='+ak+'&sn='+coordinate
        json_data = requests.get(get_coordinate_url).json()
        print(json_data)
        try:
            json_geo = json_data['result']['location']
            dict_hot={'count':100}
            json_geo=dict(json_geo,**dict_hot)
            # json_geo.append(int(add(5))*100)
            coordinate_data.append(json_geo)
        # coordinate_data.append(int(add(5))*100)
        except (IndentationError,KeyError):
            add_error.append(add)
    return coordinate_data,add_error
def save(data):
    data1 =json.dumps(data)#list的data（地址转坐标的List）转换为json格式，以便存储
    with open('./map.json','w') as f:
        f.write(data1)


file='F:\kf\gdmx2.xls'

sightlist=read_add(file)
print(sightlist)
map_point_json,add_error=add_to_coordinate(sightlist)
save(map_point_json)
print(add_error)




