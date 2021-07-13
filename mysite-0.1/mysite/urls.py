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


def batch_upload(request):
    """实现批量上传后的处理功能，包括文件格式验证、读取、预测、填充channel、文件保存
    Args:
        request: request请求
    Returns:
        item_list: list, [[编号，channel，title，content], ...], 存放预测后的所有条目
    """

    item_list = []
    # 文件格式验证
    try:
        file = request.FILES["csv-xls"]
    except:
        messages.error(request, "上传格式有误,请重新上传!")
        return HttpResponseRedirect(reverse(index))
    
    # 读取
    file_name = str(file)
    if file_name.endswith("xlsx"):
        file_data = xlrd.open_workbook(filename=None, file_contents=file.read())
        sheet_names = file_data.sheet_names()
        sheet = file_data.sheet_by_name("类别")
        # 完整预测条目：[编号, channel, title, content]
        complete_predict_line = list()

        # 对列名单独处理
        columns_name = sheet.row_values(0)
        complete_predict_line.append(columns_name)

        # 忽略第一行列名
        for i in range(1,sheet.nrows):
            line = sheet.row_values(i)
            text = ""
            # 拼接标题和内容后放入模型预测
            for item in line[2:]:
                text += item
            
            # 预测
            predict_label = prediction_fun(text)
            # 存放完整条目
            complete_predict_line.append([int(line[0]), predict_label, line[2], line[3]])
            item_list.append([int(line[0]), predict_label, line[2], line[3]])

        # 填充channel
        clear_dir()
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "类别"
        for i in range(len(complete_predict_line)):
            for j in range(len(complete_predict_line[i])):
                sheet.cell(i+1, j+1, value=str(complete_predict_line[i][j]))
        workbook.save("tmp/{}".format(file_name))
        return item_list


def single_input(request):
    """实现单例输入后的预测功能
    Args:
        request: request请求
    Returns：
        item_list: 不同于批量预测后的item_list, 只包含单条预测的结果，且条目信息包括标题、内容、预测标签和用时：[[title, content, label, time]]
    """
    item_list = []
    title = request.POST.get("title", "")
    content = request.POST.get("content", "")
    # 规定新闻标题和内容非空
    if title == "" or content == "":
        messages.error(request, "新闻标题和内容不能为空！")
        return HttpResponseRedirect(reverse(index))
    
    # 拼接标题和内容，传入模型预测
    text = title + " " + content
    start_time = time.clock()
    predict_label = prediction_fun(text)
    end_time = time.clock()
    cost_time = str(end_time-start_time)+"秒"

    item_list.append([title, content, predict_label, cost_time])
    return item_list


def index(request):
    """
    index页面：
        - 批量输入：上传、预测结果翻页展示、预测结果下载
        - 单例输入：标题/内容，预测标签，耗时
    """
    item_list = []
    if request.method == "POST":
        # 批量上传
        if "batch" in request.POST:
            item_list = batch_upload(request)
            
        # 单例输入
        elif "single" in request.POST:
            item_list = single_input(request)
            
    return render(request, "index.html", {"item_list": item_list})


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
        return HttpResponseRedirect(reverse(index))

    file = open("data/{}".format(file_names[0]), "rb")
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(file_names[0])
    return response

urlpatterns = [
    path('', index),
    path("download/", download)
]
