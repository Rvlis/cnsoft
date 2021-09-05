"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, messages
from django.urls import path, reverse
from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect, FileResponse
import csv
import os
import shutil
import xlrd
import openpyxl
# 预测方法
from prediction import prediction_fun
import time
#websocket linking
from mysite.consumers import chatconsumer
import json
import threading
from django.urls import path

import connectMySQL
from pymysql.converters import escape_string

# 数据库的数据行数
forecastdataLen = 0
"""清空指定目录"""
def clear_dir(dir_path="tmp"):
    """清空指定目录
    Args:
        dir_path: 目录路径，default="tmp"
    Returns:
        None
    """
    try:
        shutil.rmtree(dir_path)
        os.makedirs(dir_path)
    except:
        pass

def batch_class(file_data,file_name,forecastdataLen):
    sheet_names = file_data.sheet_names()
    # sheet = file_data.sheet_by_name("类别")
    sheet = file_data.sheet_by_index(0)
    # 完整预测条目：[编号, channel, title, content]
    complete_predict_line = list()

    # 对列名单独处理
    columns_name = sheet.row_values(0)
    complete_predict_line.append(columns_name)
    # 记录预测条数
    num_i = 0
    total_num = sheet.nrows - 1
    # 忽略第一行列名
    for i in range(1, sheet.nrows):
        num_i = i
        line = sheet.row_values(i)
        text = ""
        # 拼接标题和内容后放入模型预测
        for item in line[2:]:
            text += item

        # 记录预测时间
        start_time = time.clock()
        # 预测
        predict_label = prediction_fun(text)
        end_time = time.clock()
        cost_time = end_time - start_time
        # print("预测第{}条".format(num_i))
        # print("<" + str(line[0]) + ">" + line[2])
        # 存放完整条目
        complete_predict_line.append([int(line[0]), predict_label, line[2], line[3]])

        sql = "insert into forecastdata values ({},\"{}\",\"{}\",\"{}\",{})".format(num_i + forecastdataLen,
                                                                                    escape_string(predict_label),
                                                                                    escape_string(line[2]),
                                                                                    escape_string(line[3]), cost_time)
        connectMySQL.insertData(sql)

        # item_list.append([int(line[0]), predict_label, line[2], line[3]])
        # 通过websocket链接向前端发送分类预测结果
        chatconsumer[0].send(text_data=json.dumps({
            'num_i': '{}'.format(num_i),
            'percentage': '{:.2f}'.format(num_i * 100 / total_num),
            "title": line[2],
            "content": line[3],
            "classfy": predict_label,
            "time": "{:.4f}秒".format(cost_time),
            "total_num": total_num,
            # "is_stop": False,
        }))

    # 填充channel
    clear_dir()
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "类别"
    for i in range(len(complete_predict_line)):
        for j in range(len(complete_predict_line[i])):
            sheet.cell(i + 1, j + 1, value=str(complete_predict_line[i][j]))
    workbook.save("tmp/{}".format(file_name))
    # return item_list
    # return HttpResponse(request)
"""实现批量上传后的处理功能，包括文件格式验证、读取、预测、填充channel、文件保存"""
def batch_upload(request):
    """实现批量上传后的处理功能，包括文件格式验证、读取、预测、填充channel、文件保存
    Args:
        request: request请求
    Returns:
        item_list: list, [[编号，channel，title，content], ...], 存放预测后的所有条目
    """
    print("批量预测")
    #item_list = []
    # 文件格式验证
    try:
        file = request.FILES["csv-xls"]
    except:
        messages.error(request, "上传格式有误,请重新上传!")
        return HttpResponseRedirect(reverse(newsClassify))
    
    # 读取
    file_name = str(file)
    if file_name.endswith("xlsx"):
        global forecastdataLen
        forecastdataLen = connectMySQL.forecastdataLen()
        file_data = xlrd.open_workbook(filename=None, file_contents=file.read())

        # 多线程
        t1 = threading.Thread(target=batch_class, args=(file_data,file_name,forecastdataLen,))
        t1.start()
        # batch_class(file_data,file_name,forecastdataLen)

    if file_name.endswith("csv"):
        forecastdataLen = connectMySQL.forecastdataLen()
        file_data = file.read().decode("gbk")
        print(file_name)
        # 多线程
        t1 = threading.Thread(target=batch_csv, args=(file_data, file_name, forecastdataLen,))
        t1.start()

def batch_csv(file_data,file_name,forecastdataLen):
    test_list = list()
    lines = file_data.split("\n")
    with open("tmp/{}".format(file_name), "w", encoding="gb18030",
              newline="") as wf:
        tar_csv = csv.writer(wf, doublequote=False, escapechar="\\")
        num_i = 0
        total_num = len(lines)
        for line in lines:
            num_i += 1
            fields = line.split(",")
            # 规定只包含标题和内容两列
            content = ""
            for field in fields:
                content += field
                if len(fields) > 2:
                    fields[1] += fields[len(fields) - 1]
                    del fields[len(fields) - 1]

            start_time = time.clock()
            predict_label = predict_label = prediction_fun(content)
            end_time = time.clock()
            cost_time = "{:.4f}秒".format(end_time - start_time)
            fields.append(predict_label)
            fields.append(cost_time)
            print("预测第{}".format(num_i))

            # 存放完整条目
            sql = "insert into forecastdata values ({},\"{}\",\"{}\",\"{}\",{})".format(num_i + forecastdataLen,
                                                                                        escape_string(
                                                                                            predict_label),
                                                                                        escape_string(fields[0]),
                                                                                        escape_string(fields[1]),
                                                                                        end_time - start_time)
            connectMySQL.insertData(sql)

            ###lgl
            if len(fields) == 4:
                print(fields[0])
                test_list.append(fields)
                # 预测结果写入
                tar_csv.writerow(fields)
                ###lgl
                chatconsumer[0].send(text_data=json.dumps({
                    'num_i': '{}'.format(num_i),
                    'percentage': '{:.2f}'.format(num_i * 100 / total_num),
                    "title": fields[0],
                    "content": fields[1],
                    "classfy": fields[2],
                    "time": fields[3],
                    "total_num": total_num,
                    # "is_stop": False,
                }))
                test_list = []
                ###lgl

"""实现单例输入后的预测功能"""
def single_input(request):
    """实现单例输入后的预测功能
    Args:
        request: request请求
    Returns：
        item_list: 不同于批量预测后的item_list, 只包含单条预测的结果，且条目信息包括标题、内容、预测标签和用时：[[title, content, label, time]]
    """
    #item_list = []
    print("单例预测")
    title = request.POST.get("title", "")
    content = request.POST.get("content", "")
    # 规定新闻标题和内容非空
    if title == "" or content == "":
        messages.error(request, "新闻标题和内容不能为空！")
        return HttpResponseRedirect(reverse(newsClassify))
    
    # 拼接标题和内容，传入模型预测，计算预测时长
    text = title + " " + content
    start_time = time.clock()
    predict_label = prediction_fun(text)
    end_time = time.clock()
    cost_time = end_time - start_time

    # 数据库操作
    global forecastdataLen
    forecastdataLen = connectMySQL.forecastdataLen()
    # print(forecastdataLen)
    sql = "insert into forecastdata values ({},\"{}\",\"{}\",\"{}\",{})".format(1 + forecastdataLen,
                                                                                    escape_string(predict_label),
                                                                                    escape_string(title),
                                                                                    escape_string(content), cost_time)
    connectMySQL.insertData(sql)

    # forecastdataLen = connectMySQL.forecastdataLen()
    # print(forecastdataLen)

    # 通过websocket链接向前端发送分类预测结果
    chatconsumer[0].send(text_data=json.dumps({
        'num_i': '1',
        #'percentage': '{:.2f}'.format(1),
        "title": title,
        "content": content,
        "classfy": predict_label,
        "time": "{:.4f}秒".format(cost_time),
        "total_num": 1,
        # "true_class": 'x',
        # "is_stop": False,
    }))

    #item_list.append([title, content, predict_label, cost_time])
    #return item_list
    #return HttpResponse(request)

def newsClassify(request):
    """
    index页面：
        - 批量输入：上传、预测结果翻页展示、预测结果下载
        - 单例输入：标题/内容，预测标签，耗时
    """
    #item_list = []
    if request.method == "POST":
        # 批量上传
        if "batch" in request.POST:
            batch_upload(request)
            #item_list = batch_upload(request)
            
        # 单例输入
        elif "single" in request.POST:
            single_input(request)
            #item_list = single_input(request)
            
    #return render(request, "index_ll.html", {"item_list": item_list})
    return HttpResponse(request)

# 预测结果下载
def download(request):
    """
    预测结果的下载
    """
    file_names = os.listdir("tmp/")
    # data目录下预测结果文件数量不唯一的情况
    if len(file_names) != 1:
        messages.error(request, "预测过程有误，请重新上传！")
        # 清空data目录
        clear_dir()
        return HttpResponseRedirect(reverse(newsClassify))

    file = open("tmp/{}".format(file_names[0]), "rb")
    # response = FileResponse(file, filename=str(file_names[0]))
    response = FileResponse(file, filename=str("预测结果.xlsx"))
    response['Content-Type'] = 'application/octet-stream'
   # response['Content-Disposition'] = 'attachment;'  #'{}"'.format(file_names[0])
   #  print(response.filename)
    return response

#q前端加载index.html
def load_index(request):
    return render(request, 'index.html')

# 查数据库
def skipPage(request):
    page_num = request.POST.get('pageNum', 0)
    page_num = int(page_num)

    # user_id = request.session.get('user_id', 0)

    sql = " select * from forecastdata where id = {} ".format(page_num+forecastdataLen)
    itemData = connectMySQL.selectOneData(sql)
    # print(itemData)

    return_param = {}
    try:
        # 数据库操作
        return_param['status'] = 200
        return_param['msg'] = 'success'
        return_param['itemData'] = itemData
    except Exception as e:
        return_param['status'] = 500
        return_param['msg'] = 'fail'
    return HttpResponse(json.dumps(return_param))

    # chatconsumer[0].send(text_data=json.dumps({
    #     'num_i': '{}'.format(page_num),
    #     # 'percentage': '{:.2f}'.format(num_i * 100 / total_num),
    #     "title": itemData[2],
    #     "content": itemData[3],
    #     "classfy": itemData[1],
    #     "time": "{:.4f}秒".format(itemData[4]),
    #     # "total_num": total_num,
    #     # "is_stop": False,
    # }))
    # return HttpResponse(request)

urlpatterns = [
    path('', load_index),
    path('newsInput', newsClassify),
    path('download/', download),
    path('skipPage', skipPage),
    # path('', index),
    # path("download/", download)
]

from django.conf.urls import static
from mysite import settings
urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
