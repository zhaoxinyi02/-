import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def get_book_name():
    name=input("请输入小说名字")
    name=quote(name,encoding="gbk")#这个要编下码，具体情况可以实践一下就知道了
    return name

def search(name):
    url="https://www.bqg.org/modules/article/search.php?searchkey="+name
    h={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39"
    }

    #搜索结果
    r=requests.get(url=url,headers=h)
    s=BeautifulSoup(r.text,"html.parser")
    return s

def get_book_names(s):
    booknames=[]
    for jieguo in s.find_all(name="span",attrs={"class":"s2"}):
        for bookname in jieguo.find_all(name="a"):
            booknames.append(bookname.string)
    return booknames

def get_book_hrefs(s):
    bookhrefs=[]
    for jieguo in s.find_all(name="span",attrs={"class":"s2"}):
        for booknumber in jieguo.find_all(name="a"):
            bookhrefs.append(booknumber.get("href"))
    return bookhrefs

def give_book_numbers():
    numbers=[]
    for xuhao in range(1,20):
        numbers.append(str(xuhao))
    return numbers

def Print(nu_it,na_it):
    while True:
        try:
            print(next(nu_it)+"."+next(na_it))
        except:
            break
#书本页面

def get_book_number():
    b=int(input("请输入小说序号"))
    return b

def get_book_code(bookhrefs,b):
    h = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39"
    }
    url=bookhrefs[b-1]
    r=requests.get(url=url,headers=h)
    s=BeautifulSoup(r.text,"html.parser")
    return s

def get_book_zhangjiemingzi(s):
    zj = []
    for dds in s.find_all(name="dd"):
        for a in dds.find_all(name="a"):
            zj.append(a.string)
    del zj[0:12]
    return zj

def get_zhangjie_hrefs(s):
    zjh = []
    for dds in s.find_all(name="dd"):
        for a in dds.find_all(name="a"):
            zjh.append(a.get("href"))
    del zjh[0:12]
    return zjh

def download(zjh,bookhrefs,zj,b):
    cishu=0
    h = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39"
    }
    for u in zjh:
        url=bookhrefs[b-1]+u
        r=requests.get(url=url,headers=h)
        s=BeautifulSoup(r.text,"html.parser")
        wzs=[]
        cishu+=1
        for c in s.find_all(name="div",attrs={"id":"content","name":"content"}):
            with open(str(cishu)+str(zj[cishu-1])+".txt","w",encoding="utf-8")as f:
                f.write(c.text)
            print(zj[cishu-1],"已下载完成！")


def main():
    #1.通过输入得到搜索的书名
    #2.构造网址，得到搜索页面的源代码
    #3.得到搜索页面显示的书籍名字，网址，并为每本书编号显示在终端，方便用户输入序号进行下载
    #4.输入序号，重新构造网址，并得到这本书的页面源代码
    #5.解析书本页面源代码并得到每一章的网址
    #6.构造每一章的网址并得到源代码
    #7.解析得到书文字并保存txt文档
    name = get_book_name()
    code = search(name=name)
    names = get_book_names(s=code)
    hrefs = get_book_hrefs(s=code)
    numbers = give_book_numbers()
    na_it = iter(names)
    nu_it = iter(numbers)
    Print(nu_it, na_it)
    b = get_book_number()
    code = get_book_code(bookhrefs=hrefs,b=b)
    zj = get_book_zhangjiemingzi(s=code)
    zjh = get_zhangjie_hrefs(s=code)
    download(zjh, hrefs, zj, b)


if __name__ == "__main__":
    main()
