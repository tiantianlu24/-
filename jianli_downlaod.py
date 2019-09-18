import urllib.request
import urllib.parse
from lxml import etree
import os
import time

jl_list = []
down_list = []
# 发送请求
def handle_request(url,page):
    if page == 1:
        url_1 = url + ".html"
    else:
        url_1 = url + "_" +str(page) + ".html"
    headers = {
        "User-Agent": " Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
    }
    request = urllib.request.Request(url=url_1, headers=headers)
    return request

# 分析对象
def parse_content(content):
    tree = etree.HTML(content)
    # print(tree)
    jl_list = tree.xpath('//div[@id="main"]//div[@class="box col3 ws_block"]//a/@href')
    # print(jl_list)
    headers = {
        "User-Agent": " Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
    }
    for page_inside in range (1,21):
        down_url = str(jl_list[page_inside-1])+"#down"
        # print(down_url)
        # 构建 down请求
        request = urllib.request.Request(url=down_url,headers=headers)
        down_content = urllib.request.urlopen(request).read().decode()
        tree_down = etree.HTML(down_content)
        # 找到页面中的下载包，获取地址
        down_list = tree_down.xpath('//div[@class = "down_wrap"]//ul//li/a/@href')
        # print(len(down_list))
        # print(down_list)
        # 遍历+输出
        for jl_download in down_list:
            down_jl(jl_download)

# 下载
def down_jl(jl_download):
    # 创建文件夹
    dirpath = "jianli"
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    # 文件
    filename = os.path.basename(jl_download)
    filepath = os.path.join(dirpath,filename)

    headers = {
        "User-Agent": " Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
    }
    request = urllib.request.Request(url=jl_download, headers=headers)
    response = urllib.request.urlopen(request)
    with open(filename,"wb") as fp:
        fp.write(response.read())
    time.sleep(1)

def main():
    start_page = int(input("起始页"))
    end_page = int(input("末尾页"))
    url = "http://sc.chinaz.com/jianli/free"
    # print(url)
    for page in range(start_page,end_page+1):
        request = handle_request(url,page)
        content = urllib.request.urlopen(request).read().decode()
        # print(content)
        parse_content(content)

if __name__ == '__main__':
    main()
