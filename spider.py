#spider.py
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

identify=["品名","规格","厂家/产地"]

type_Dict={}

Item={}

Columns={}
Price_Index={}


def create_csv(text,category):
    print("create and initialize the csv file in category ",category)
    items=[]
    #find the content div
    div_start=text.find("<div class=\"content\" id=\"content\">")
    #find the table start
    table_start=text.find("table",div_start)
    #find the table End
    table_end=text.find("</table>",table_start)
    columns=[]
    #get the column name


    next_s=text.find("<tr")
    next_e=text.find("</tr>",next_s)
    index=1
    while (next_s<next_e):
        next_s=text.find("<strong>",next_s)
        e=text.find("</strong>",next_s)
        column=text[(next_s+8):e]
        next_s=text.find("<td",e)
        if column in identify:
            columns.append(column)
        if column=="今日价格":
            Price_Index[category]=index
        index+=1
    #get all the items
    tr_start=text.find("<tr",next_e)
    tr_end=text.find("</tr>",tr_start)
    td_start=0
    # print(columns)
    next_e=tr_start
    while (tr_end<table_end and tr_end!=-1):
        item=""
        td_start=text.find("<td",tr_start)
        td_end=text.find("</td>",td_start)
        for i in range(len(columns)):
            s=text.find(">",td_start)+1
            e=text.find("<",s)
            item+=text[s:e]+"_"
            td_start=text.find("<td",td_end)
            td_end=text.find("</td>",td_start)
        # print(item)
        items.append(item)
        tr_start=text.find("<tr",tr_end)
        tr_end=text.find("</tr>",tr_start)
        # print("------\n")

        Item[category]=items
        Columns[category]=columns

    #create_csv_files
    print(items)
    for item_name in items:

        s=item_name.replace("/","|")
        file_name="data/"+category+"/"+s+".csv"
        with open(file_name, "w") as my_empty_csv:
            filewriter = csv.writer(my_empty_csv)
            filewriter.writerow(['Date', 'Min_Price',"Max_Price","Average_Price"])
        print("Successfully create the file ",file_name)
    print("---------\n")


def get_price_write(text,category):
    Rows={}
    items=Item[category]
    print(len(items))
    columns=Columns[category]
    #get the date of the post
    date_s=text.find("发布日期")
    s=text.find('2',date_s)
    e=s+10

    date=text[s:e]
    div_content_start=text.find("<div class=\"content\" id=\"content\">")
    table_start=text.find("<table",div_content_start)
    table_end=text.find("</table>",table_start)

    rows_one_day={}
    starts=text.find("</tr>",table_start)
    tr_start=text.find("<tr",starts)
    tr_end=text.find("</tr>",tr_start)
    for i in range(len(items)):
        td_end=tr_start
        for j in range(Price_Index[category]):
            td_start=text.find("<td",td_end)
            td_end=text.find("</td>",td_start)
        s=text.find(">",td_start)+1
        e=text.find("<",s)
        price_str=text[s:e]
        # print("i ",price_str)
        prices=price_str.split('-')
        min_price=float(prices[0])
        max_price=float(prices[1])
        avg_price=(min_price+max_price)/2.0
        row_one_day=[]
        row_one_day.append(date)
        row_one_day.append(min_price)
        row_one_day.append(max_price)
        row_one_day.append(avg_price)
        rows_one_day[items[i]]=row_one_day

        tr_start=text.find("<tr",tr_end)
        tr_end=text.find("</tr>",tr_start)
    print(rows_one_day)
    for row in rows_one_day:
        file_name="data/"+category+"/"+row.replace('/','|')+".csv"
        with open(file_name, "a",newline='') as my_csv:
            filewriter = csv.writer(my_csv)
            filewriter.writerow(rows_one_day[row])
        print("Successfully write the file ",file_name, "for date ",rows_one_day[row][0])

    print("---------\n")

def write_csv_from_url_list(category):
    url_list=[]
    url_file_name="url/"+category+"_url.csv"
    with open(url_file_name,"r") as csvfile:
        filereader=csv.reader(csvfile)
        row_num=0
        for row in filereader:
            if row_num>0:
                url_list.append(row[1])
            row_num+=1
        # print(url_list)

        # create the csv file in the specified folder
        rs=requests.get(url_list[0],headers=headers)
        rt_page=rs.text
        print(url_list)
        print(rt_page)
        create_csv(rt_page,category)

        #iterate over all the urls in the list and write
        for url in url_list:
            rs=requests.get(url,headers=headers)
            rt_page=rs.text
            get_price_write(rt_page,category)



def main():
    write_csv_from_url_list('动力型圆柱')
    write_csv_from_url_list('车用动力电池（方形）')
    write_csv_from_url_list('废旧锂电池')
    write_csv_from_url_list('磷酸铁锂正极材料')
    write_csv_from_url_list('三元正极材料')
    write_csv_from_url_list('锰酸锂正极材料')





    # for category in URL_Dict:
    #     t=threading.Thread(target=write_csv_from_url_list,args=(category,))
    #     t.start()

if __name__=='__main__':
    #get the url and send the request
    main()


# URL_Dict={
# '动力型圆柱':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=598&fromdate=20180601&todate=20190420&order=0&x=67&y=18',
# '车用动力电池（方形）':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=596&fromdate=20180601&todate=20190420&order=0&x=52&y=11',
# '废旧锂电池':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=599&fromdate=20180601&todate=20190420&order=0&x=70&y=19',
# '磷酸铁锂正极材料':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=608&fromdate=20180601&todate=20190420&order=0&x=61&y=12',
# '三元正极材料':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=607&fromdate=20180601&todate=20190420&order=0&x=49&y=11',
# '锰酸锂正极材料':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=605&fromdate=20180601&todate=20190420&order=0&x=40&y=8',

# '钴酸锂正极材料':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=606&fromdate=20180601&todate=20190420&order=0&x=42&y=14',
# '天然石墨类负极材料':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=611&fromdate=20180601&todate=20190420&order=0&x=65&y=6',
# '人造石墨类负极材料':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=610&fromdate=20180601&todate=20190420&order=0&x=57&y=18',
# '隔膜':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=600&fromdate=20180601&todate=20190420&order=0&x=45&y=8',
# '电解液':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=603&fromdate=20180601&todate=20190420&order=0&x=64&y=9',
# '六氟磷酸锂':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=707&fromdate=20180601&todate=20190420&order=0&x=59&y=24',
# '溶剂':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=708&fromdate=20180601&todate=20190420&order=0&x=51&y=17',
# '铝箔':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=710&fromdate=20180601&todate=20190420&order=0&x=47&y=25',
# '铜箔':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=709&fromdate=20180601&todate=20190420&order=0&x=66&y=4',
# '铝塑膜':'http://www.ciaps.org.cn/quote/search.php?kw=&fields=0&catid=712&fromdate=20180601&todate=20190420&order=0&x=56&y=12'
# }
