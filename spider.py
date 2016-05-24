#!/usr/bin/env python
# coding: utf-8
import urllib.request as ur
import html2text

domain = 'http://www.liaoxuefeng.com'   #廖雪峰网站的域名
path = '/Users/blublu/Desktop/python/'    #保存路径


# 在主页上获取所有链接
f = ur.urlopen("http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000")
urls = f.read()
f.close()

# 替换所有空格回车
urls = urls.decode('utf-8')
geturl = urls.replace("\n", "")
geturl = geturl.replace(" ", "")

# 得到包含url的字符串
list = geturl.split(r'em;"><ahref="')[1:]
list.insert(0, '/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000">')

# 开始遍历url List
for line in list:
    urlpath = line.split(r'">')[0]
    urlpath = domain + urlpath
    print("GET:" + urlpath)
    f = ur.urlopen(urlpath)
    html = f.read()
    html = html.decode('utf-8')

    # 通过title确定文件名,为了避免二级目录使用空格替换'/'
    title = html.split("<title>")[1]
    title = title.split(" - 廖雪峰的官方网站</title>")[0]
    title = title.replace("/", " ")

    # 截取正文
    html = html.split(r'<div class="x-wiki-content">')[1]
    html = html.split("</div>\n    <hr>\n    <div id=\"x-wiki-prev-next\" class=\"uk-clearfix uk-margin-left uk-margin-right\">")[0]
    html = html.replace(r'src="', 'src="' + domain)

    # 转换成md格式
    h = html2text.HTML2Text()
    md = h.handle(html)

    # 输出文件
    output = open(path + "%d" % list.index(line) + '.' + title + '.md', 'wb')
    output.write(md.encode('utf-8'))
    output.close()