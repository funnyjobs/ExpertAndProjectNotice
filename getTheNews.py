import httpx
import tkinter as tk
import tkinter.messagebox
import sqlite3 as sl
from tkinter import *
from tkinter import ttk
import webbrowser
import re
#定义检索的词汇
keywords = ["专家","入库","项目","申报","课题","征集"]
'''
{"网站名称":"url"}
'''
url_dict = {
    "烟台市公共资源交易网-通知公告":"http://ggzyjy.yantai.gov.cn/tzgg/index.jhtml",
    "烟台市财政局-通知公告":"https://czj.yantai.gov.cn/col/col3296/index.html",
    "烟台市科技局-通知公告":"https://kjj.yantai.gov.cn/col/col16248/index.html",
    "烟台市工业和信息化局-通知公告":"https://jxw.yantai.gov.cn/col/col2208/index.html",
    "烟台市大数据局-通知公告":"https://dsjj.yantai.gov.cn/col/col33025/index.html",
    "山东省工业和信息化厅-通知公告":"http://gxt.shandong.gov.cn/col/col15201/index.html",
    "山东省大数据局-通知公告":"http://bdb.shandong.gov.cn/col/col76147/index.html",
    "山东省科学技术厅-通知公告":"http://kjt.shandong.gov.cn/col/col13360/index.html"
}
def write_sqlite(title,url,state=0):
    conn_write = sl.connect('news')
    cs_write = conn_write.cursor()
    sql_insert = "INSERT INTO news_state(title,url,state) values('{}'".format(
        title) + ",'{}'".format(url)+ ",'{}')".format(state)
    cs_write.execute(sql_insert)
    conn_write.commit()
    cs_write.close()
    conn_write.close()
def update_sqlite(title,url,state):
    conn_write = sl.connect('news')
    cs_write = conn_write.cursor()
    sql_insert = "UPDATE news_state SET state='{}'".format(state)+" WHERE title='{}'".format(title)
    cs_write.execute(sql_insert)
    conn_write.commit()
    cs_write.close()
    conn_write.close()
def getTheNewsInfoForGGZY(url_in):
    # {"title":"url"}
    return_info = {}
    start_index = url_in.find("//")
    end_index = url_in.find(".cn")
    host_ = url_in[start_index + 2:end_index + 3]
    print(host_)
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "",
        "Host": host_,
        "User-Agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36"
    }
    with httpx.Client(headers=headers) as client:
        response = client.get(url_in)
    pattern_notice = r"<div class=\"article-content\">(.*?)<div id=\"page\"></div>"
    result = re.findall(pattern_notice, response.text, re.DOTALL)
    pattern_notice_next = r"<a (.*?)>"
    result_next = re.findall(pattern_notice_next, result[0], re.DOTALL)
    for i_result in range(len(result_next)):
        for i_keywords in range(len(keywords)):
            if result_next[i_result].find(keywords[i_keywords])!=-1:
                pattern_notice_href = r"href=\"(.*?)\""
                result_href = re.findall(pattern_notice_href, result_next[i_result], re.DOTALL)
                pattern_notice_title = r"title=\"(.*?)\""
                result_title = re.findall(pattern_notice_title, result_next[i_result], re.DOTALL)
                return_info[result_title[0]] = result_href[0]
    return return_info
def getTheNewsInfo(url_in):
    #{"title":"url"}
    return_info = {}
    start_index = url_in.find("//")
    end_index = url_in.find(".cn")
    host_ = url_in[start_index+2:end_index+3]
    print(host_)
    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        "Cookie":"",
        "Host":host_,
        "User-Agent":"Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36"
    }
    with httpx.Client(headers=headers) as client:
        response = client.get(url_in)
    print(response.text)
    pattern_notice = r"<record>(.*?)</record>"
    # 进行匹配
    result = re.findall(pattern_notice, response.text,re.DOTALL)
    for i_result in range(len(result)):
        for i_keywords in range(len(keywords)):
            if result[i_result].find(keywords[i_keywords])!=-1:
                pattern_href = r"href=\"(.*?)\""
                result_url = re.findall(pattern_href, result[i_result], re.DOTALL)
                if result_url:
                    if result_url[0].find("http")==-1:
                        temp_url = host_ + result_url[0]
                    else:
                        temp_url = result_url[0]
                else:
                    temp_url = url_in
                pattern_title = r"title=\"(.*?)\""
                result_title = re.findall(pattern_title, result[i_result], re.DOTALL)
                if result_title:
                    temp_title = result_title[0]
                else:
                    pattern_a = r"<a(.*?)</a>"
                    result_a = re.findall(pattern_a, result[i_result], re.DOTALL)
                    if result_a:
                        title_start_index = result_a[0].find('>')
                        temp_title = result_a[0][title_start_index+1:].replace("<s></s>","")
                    else:
                        temp_title = result[i_result]
                return_info[temp_title] = temp_url
                break
    return return_info
def initTreeview():
    print("initTreeview")
    temp_i = -1
    for key in url_dict.keys():
        temp_i = temp_i + 1
        print(key, url_dict[key])
        tree.insert('', temp_i, iid=url_dict[key], text=key,open=True)
        #爬取并选择添加
        if key == "烟台市公共资源交易网-通知公告":
            r_dict = getTheNewsInfoForGGZY(url_dict[key])
        else:
            r_dict = getTheNewsInfo(url_dict[key])
        temp_j = -1
        conn = sl.connect('news')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM news_state")
        rows = cursor.fetchall()
        tree.tag_configure("green",background="green")
        for key_r in r_dict.keys():
            temp_j = temp_j + 1
            #未出现是0，已经出现是1，出现且未点击过是2
            have_exist = 0
            for row in rows:
                if row[0] == key_r and row[2] == 1:
                    have_exist = 1
                    break
                if row[0] == key_r and row[2] == 0:
                    have_exist = 2
                    break
            if have_exist == 0:
                tree.insert(url_dict[key], temp_j, iid=r_dict[key_r], text=key_r, open=True,tags=("green"))
                write_sqlite(key_r,r_dict[key_r])
                print("add:ddddddddddddddddddddddd")
            elif have_exist == 2:
                tree.insert(url_dict[key], temp_j, iid=r_dict[key_r], text=key_r, open=True, tags=("green"))
            else:
                tree.insert(url_dict[key], temp_j, iid=r_dict[key_r], text=key_r, open=True)
def onSelect(e):
    widgetObj = e.widget  # 取得控件
    itemselected = widgetObj.selection()[0]  # 取得选项
    item_select = e.widget.focus()
    tree.tag_configure("white", background="white")
    if item_select is not None:
        tree.item(item_select, tags=("white"))
    else:
        print("no")
    selectText = widgetObj.item(itemselected, "text")
    if selectText.find("-通知公告")!=-1:
        return
    update_sqlite(selectText,itemselected,1)
    if itemselected.find("http://")!=-1:
        open_website(itemselected)
    else:
        open_website("http://"+itemselected)
    print(itemselected)
def open_website(url):
    webbrowser.open(url)
    #webbrowser.open('https://www.google.com')
####设计界面#####
root = tk.Tk()
entry_text = StringVar()
root.title("专家入库和项目申请通知消息探测")
#设置窗口最大化，且不可改变大小
#root_width=root.winfo_screenwidth()
root_height=root.winfo_screenheight()
root.geometry('{0}x{1}+0+0'.format(400,root_height-200))
root.resizable(False, False)
#第一层区域分布，纵向三列
frame_c1=tk.Frame(root, width=400, height=root_height-200, bg='#81D4FA')
frame_c1.grid(row=0, column=0, columnspan=40, rowspan=88,sticky=tk.W+tk.N)
# Create a Treeview
scrollbar_v = Scrollbar(frame_c1,orient=VERTICAL)
scrollbar_v.pack(side=RIGHT, fill=Y)
scrollbar_h = Scrollbar(frame_c1,orient= HORIZONTAL)
scrollbar_h.pack(side=BOTTOM, fill=X)
tree = ttk.Treeview(frame_c1,height=42,selectmode='browse',yscrollcommand=scrollbar_v.set,xscrollcommand=scrollbar_h.set)
tree.heading("#0",text="专家入库和项目申请消息列表")
tree.column("#0",width=400)
scrollbar_v.config(command=tree.yview)
scrollbar_h.config(command=tree.xview)
tree.config(yscrollcommand=scrollbar_v.set,xscrollcommand=scrollbar_h.set)
tree.pack(expand=YES,fill=tk.BOTH)
tree.Scrollable = False
tree.Scrollable = True
root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)
frame_c1.rowconfigure(0,weight=1)
tree.bind("<<TreeviewSelect>>",onSelect)
initTreeview()
root.mainloop()