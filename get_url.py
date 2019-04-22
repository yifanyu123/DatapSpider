#get_url.py
import requests
import time
import csv
import threading

headers={
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'Hm_lvt_027abba4fa06127e733eb2ee2d1c6598=1555818056; DWk_forward_url=http%3A%2F%2Fwww.ciaps.org.cn%2F; __51cke__=; DWk_auth=ADEBMA1hDTYAYgFSAG0JYVBrVGFVLQd1C2RSO1YkAQkAMFBRCGFaYQJpVDkAMghqVDkIbwM6BjFVNwQ4U21SYwA3ATANaw0wAGoBaAA4CThQNFQ3VWIHMQsyUjNWZgFiADZQPQhfWmE; DWk_userid=69201; DWk_username=longyunlu; __tins__17089721=%7B%22sid%22%3A%201555821440777%2C%20%22vd%22%3A%2021%2C%20%22expires%22%3A%201555825025869%7D; __51laig__=39; Hm_lpvt_027abba4fa06127e733eb2ee2d1c6598=1555823226',
'Host': 'www.ciaps.org.cn',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}
URL_Dict={
'动力型圆柱':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=598&fromdate=20180601&todate=20190420&order=0&x=67&y=18',
'车用动力电池（方形）':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=596&fromdate=20180601&todate=20190420&order=0&x=52&y=11',
'废旧锂电池':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=599&fromdate=20180601&todate=20190420&order=0&x=70&y=19',
'磷酸铁锂正极材料':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=608&fromdate=20180601&todate=20190420&order=0&x=61&y=12',
'三元正极材料':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=607&fromdate=20180601&todate=20190420&order=0&x=49&y=11',
'锰酸锂正极材料':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=605&fromdate=20180601&todate=20190420&order=0&x=40&y=8',
'钴酸锂正极材料':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=606&fromdate=20180601&todate=20190420&order=0&x=42&y=14',
'天然石墨类负极材料':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=611&fromdate=20180601&todate=20190420&order=0&x=65&y=6',
'人造石墨类负极材料':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=610&fromdate=20180601&todate=20190420&order=0&x=57&y=18',
'隔膜':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=600&fromdate=20180601&todate=20190420&order=0&x=45&y=8',
'电解液':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=603&fromdate=20180601&todate=20190420&order=0&x=64&y=9',
'六氟磷酸锂':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=707&fromdate=20180601&todate=20190420&order=0&x=59&y=24',
'溶剂':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=708&fromdate=20180601&todate=20190420&order=0&x=51&y=17',
'铝箔':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=710&fromdate=20180601&todate=20190420&order=0&x=47&y=25',
'铜箔':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=709&fromdate=20180601&todate=20190420&order=0&x=66&y=4',
'铝塑膜':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=712&fromdate=20180601&todate=20190420&order=0&x=56&y=12'
}

pagenum_Dict={
'动力型圆柱':12,
'车用动力电池（方形）':6,
'废旧锂电池':17,
'磷酸铁锂正极材料':12,
'三元正极材料':12,
'锰酸锂正极材料':12,
'钴酸锂正极材料':12,
'天然石墨类负极材料':12,
'人造石墨类负极材料':12,
'隔膜':12,
'电解液':12,
'六氟磷酸锂':12,
'溶剂':12,
'铝箔':12,
'铜箔':12,
'铝塑膜':12
}

def create_url_csv(category):
    file_name="url/"+category+"_url.csv"
    with open(file_name,"w") as empty_csv:
        filewriter=csv.writer(empty_csv)
        filewriter.writerow(["Date","Url"])

def get_url_write(category,page):
    urls=[]
    src_url=URL_Dict[category]+"&page="+str(page)
    rs= requests.get(src_url,headers=headers)
    rt_page=rs.text
    # print(rt_page)
    div_start=rt_page.find("<div class=\"catlist\">")
    ul_start=rt_page.find("<ul",div_start)
    ul_end=rt_page.find("</ul>",ul_start)
    extracted_text=rt_page[ul_start:ul_end]

    s=extracted_text.find("<li",)
    e=extracted_text.find("</li>",s)

    while (e<len(extracted_text) and e!=-1 and s!=-1):
        date_s=extracted_text.find('2',s)
        date=extracted_text[date_s:date_s+10]
        a_s=extracted_text.find("<a",s)

        url_s=extracted_text.find('\"',a_s)+1
        url_e=extracted_text.find('\"',url_s)
        url=extracted_text[url_s:url_e]
        print(url)
        urls.append([date,url])

        s=extracted_text.find("<li class=\"catlist_li\">",e)
        e=extracted_text.find("</li>",s)
    #reverse the list so that the date was ordered
    urls.reverse()

    file_name="url/"+category+"_url.csv"
    with open(file_name,"a",newline='') as csvfile:
        filewriter=csv.writer(csvfile)
        for my_url in urls:
            filewriter.writerow(my_url)

#thread function
def write_to_csv(category):
    pages=pagenum_Dict[category]
    for page in range(pages,0,-1):
        get_url_write(category,page)

def write_to_csv_files():
    for category in URL_Dict:
        write_to_csv(category)


def create_csv_files():
    for category in URL_Dict:
        create_url_csv(category)


if __name__=='__main__':
    #get the url and send the request
    for category in URL_Dict:
        print(category)
        t=threading.Thread(target=write_to_csv, args=(category,))
        t.start()
