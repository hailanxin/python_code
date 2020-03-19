# -*- coding:utf-8 -*-
'''
Created on 2017年4月17日

@author: dsju
'''
import requests
import lxml.html as H 
from urllib import parse as urlparse
from multiprocessing import Pool
import pymysql
import re
import chardet

def get_webcontent(url):
    try:
        url = 'http://913ent.com/plus/list.php?tid=50'
        conn = pymysql.connect(host='192.168.0.6', port=3306,user='root', password="123589",db='bbs',charset='utf8')
        cur = conn.cursor()
        base_sql = "insert into websites(siteurl,pageurl,html,content)values('%s','%s','%s','%s')"
        s = requests.Session()
        r = s.get(url)
        if r.encoding == 'ISO-8859-1':
            html = r.text.replace('\r', '').replace('\n', '').replace('\'','"').replace('  ', ' ')
            encoding = re.findall('charset=(utf-8|utf8|gbk|GBK|GB2312|gb2312|UTF-8|UTF8)"', html)[0]
            r.encoding = encoding
        html = r.text.replace('\r', '').replace('\n', '').replace('\'','"').replace('  ', ' ')
        if r.url !=url and r.url != url+'/':
            return
        tree = H.document_fromstring(html)
        for ele in tree.xpath('//script'):
            ele.drop_tree()
        for ele in tree.xpath('//link '):
            ele.drop_tree()
        content = tree.text_content()
        sql = base_sql % (url, url, html, content)
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
        return
    urlparsed = urlparse.urlparse(url)
    urls_s = set(['/'])
    l = []
    for a_ele in tree.xpath('//a'):
        try:
            if not 'href' in a_ele.attrib:
                continue
            a_href = a_ele.attrib['href']
            urlparsed_t = urlparse.urlparse(a_href)
            if a_href.startswith('/'):
                if not a_href in urls_s:
                    urls_s.add(a_href)
                    a_href = urlparse.urlunparse([urlparsed[0], urlparsed[1], a_href, '', '', ''])
                    l.append(a_href)
                    print (a_href)
            if urlparsed[1] == urlparsed_t[1]:
                if not a_href in urls_s:
                    urls_s.add(a_href)
                    l.append(a_href)
                    print (a_href)
        except:
            continue
    l_len = len(l)
    l1 = []
    if l_len >= 99:
        for url_t in l[:98]:
            try:
                r = s.get(url)
                if r.encoding == 'ISO-8859-1':
                    html = r.text.replace('\r', '').replace('\n', '').replace('\'','"').replace('  ', ' ')
                    encoding = re.findall('charset=(utf-8|utf8|gbk|GBK|GB2312|gb2312|UTF-8|UTF8)"', html)[0]
                    r.encoding = encoding
                html = r.text.replace('\r', '').replace('\n', '').replace('\'','"').replace('  ', ' ')
                tree = H.document_fromstring(html)
                for ele in tree.xpath('//script'):
                    ele.drop_tree()
                for ele in tree.xpath('//link '):
                    ele.drop_tree()
                content = tree.text_content()
                sql = base_sql % (url, url_t, html, content)
                print(sql)
                cur.execute(sql)
                conn.commit()
            except:
                continue
    else:
        for url_t in l:
            try:
                r = s.get(url)
                if r.encoding == 'ISO-8859-1':
                    html = r.text.replace('\r', '').replace('\n', '').replace('\'','"').replace('  ', ' ')
                    encoding = re.findall('charset=(utf-8|utf8|gbk|GBK|GB2312|gb2312|UTF-8|UTF8)"', html)[0]
                    r.encoding = encoding
                html = r.text.replace('\r', '').replace('\n', '').replace('\'','"').replace('  ', ' ')
                tree = H.document_fromstring(html)
                for ele in tree.xpath('//script'):
                    ele.drop_tree()
                for ele in tree.xpath('//link '):
                    ele.drop_tree()
                content = tree.text_content()
                sql = base_sql % (url, url_t, html, content)
                print(sql)
                cur.execute(sql)
                conn.commit()
                if l_len <= 99:
                    for a_ele in tree.xpath('//a'):
                        if not 'href' in a_ele.attrib:
                            continue
                        a_href = a_ele.attrib['href']
                        urlparsed_t = urlparse.urlparse(a_href)
                        if a_href.startswith('/'):
                            if not a_href in urls_s:
                                urls_s.add(a_href)
                                a_href = urlparse.urlunparse([urlparsed[0], urlparsed[1], a_href, '', '', ''])
                                l1.append(a_href)
                                l_len += 1
                        if urlparsed[1] == urlparsed_t[1]:
                            if not a_href in urls_s:
                                urls_s.add(a_href)
                                l1.append(a_href)
                                l_len += 1
                        if l_len >= 99:
                            break
            except:
                continue
    for url_t in l1:
        try:
            r = s.get(url)
            if r.encoding == 'ISO-8859-1':
                html = r.text.replace('\r', '').replace('\n', '').replace('\'','"').replace('  ', ' ')
                encoding = re.findall('charset=(utf-8|utf8|gbk|GBK|GB2312|gb2312|UTF-8|UTF8)"', html)[0]
                r.encoding = encoding
            html = r.text.replace('\r', '').replace('\n', '').replace('\'','"').replace('  ', ' ')
            tree = H.document_fromstring(html)
            for ele in tree.xpath('//script'):
                ele.drop_tree()
            for ele in tree.xpath('//link '):
                ele.drop_tree()
            content = tree.text_content()
            sql = base_sql % (url, url_t, html, content)
            print(sql)
            cur.execute(sql)
            conn.commit()
        except:
            continue
if __name__ == '__main__':
    f = open('websites.txt', 'r')
    p = Pool(1)
    for url in f.readlines():
        p.apply_async(get_webcontent, args=(url.strip(),))
        break
    print ('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print ('All subprocesses done.')
    f.close()
