from channels.generic.websocket import WebsocketConsumer
import json
import csv
import xlrd
import os

import time

chatconsumer = []

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        #chatconsumer['ChatConsumer'] = self
        chatconsumer.append(self)

    def disconnect(self, close_code):
        chatconsumer = []


    def receive(self, bytes_data):
        pass
        # file = bytes_data
        # file_name = str(file)
        # print(file_name)
        # test_list = list()
        # # csv
        # if file_name.endswith("csv"):
        #     file_data = file.read().decode("utf-8")
        #     lines = file_data.split("\n")
        #     with open("data/predict_results.csv".format(os.path.splitext(file_name)[0]), "w", encoding="gb18030",
        #               newline="") as wf:
        #         tar_csv = csv.writer(wf, doublequote=False, escapechar="\\")
        #         num_i = 0
        #         for line in lines:
        #             num_i += 1
        #             fields = line.split(",")
        #             # 规定只包含标题和内容两列
        #             if len(fields) != 2:
        #                 continue
        #             content = ""
        #             for field in fields:
        #                 content += field
        #             ###lgl
        #             start_time = time.clock()
        #             predict_label = prediction_model(content)
        #             end_time = time.clock()
        #             cost_time = "{:.3f}秒".format(end_time - start_time)
        #             fields.append(predict_label)
        #             fields.append(cost_time)
        #             ###lgl
        #             ###lr
        #             # cost_time = str(end_time - start_time) + "秒"
        #             # predict_label = prediction_model(content)
        #             # fields.append(predict_label)
        #             ###lr
        #             if len(fields) == 4:
        #                 test_list.append(fields)
        #                 # 预测结果写入
        #                 tar_csv.writerow(fields)
        #                 ###lgl
        #                 # if len(test_list) == 5:
        #                 # return render(request, "index.html", {"test_list": test_list})
        #                 self.send(text_data=json.dumps({
        #                     'message': '预测了第{}条，准备上传'.format(num_i),
        #                     "title": fields[0],
        #                     "content": fields[1],
        #                     "classfy": fields[2],
        #                     "time": fields[3],
        #                 }))
        #                 # return render(request, "index.html", {"test_list": test_list})
        #                 test_list = []
        #                 ###lgl
        # # xlsx
        # elif file_name.endswith("xlsx"):
        #     # pass
        #     file_data = xlrd.open_workbook(filename=None, file_contents=file.read())
        #     sheet_names = file_data.sheet_names()
        #     with open("data/predict_results.csv".format(os.path.splitext(file_name)[0]), "w", encoding="gb18030",
        #               newline="") as wf:
        #         tar_csv = csv.writer(wf, doublequote=False, escapechar="\\")
        #         for sheet_name in sheet_names:
        #             sheet = file_data.sheet_by_name(sheet_name)
        #             # 忽略第一行
        #             for i in range(1, sheet.nrows):
        #                 line = sheet.row_values(i)
        #                 if len(line) != 2:
        #                     continue
        #                 content = ""
        #                 for item in line:
        #                     content += item
        #                 ###lgl
        #                 start_time = time.clock()
        #                 predict_label = prediction_model(content)
        #                 end_time = time.clock()
        #                 cost_time = "{:.3f}秒".format(end_time - start_time)
        #                 line.append(predict_label)
        #                 line.append(cost_time)
        #                 ###lgl
        #                 ###lr
        #                 # cost_time = str(end_time - start_time) + "秒"
        #                 # predict_label = prediction_model(content)
        #                 # line.append(predict_label)
        #                 ###lr
        #                 if len(line) == 4:
        #                     test_list.append(line)
        #                     # 预测结果写入
        #                     tar_csv.writerow(line)
        # 其他文件格式
        # else:
        #     messages.error(request, "请上传正确的文件格式:csv/xlsx!")
        #     return HttpResponseRedirect(reverse(index))
        # if text_data_json['input_module'] == '1' :
        #     input_file_name = text_data_json['input_file_name']
        #     bytes_data = text_data_json['content']
        #     print(bytes_data)
        #     #
        #     #     self.send(text_data=json.dumps({
        #     #         'message': message
        #     #     }))
        #     with open("./tokenizer.csv","wb") as code:
        #         code.write(bytes_data)
        #
        #     #测试数据
        #     # file_data = file.read().decode("utf-8")
        #     # lines = file_data.split("\n")
        #     lines = open("./tokenizer.csv", "r", encoding="utf-8")
        #     test_list = list()
        #     self.send(text_data=json.dumps({
        #         'message': '测试开始'
        #     }))
        #     print("开始预测")
        #     with open("data/predict_results.csv".format(os.path.splitext('tokenizer.csv')[0]), "w", encoding="gb18030",
        #               newline="") as wf:
        #         tar_csv = csv.writer(wf, doublequote=False, escapechar="\\")
        #         num_i = 0
        #         for line in lines:
        #             num_i += 1
        #             fields = line.split(",")
        #             # 规定只包含标题和内容两列
        #             if len(fields) != 2:
        #                 continue
        #             content = ""
        #             for field in fields:
        #                 content += field
        #             ###lgl
        #             start_time = time.clock()
        #             predict_label = prediction_model(content)
        #             end_time = time.clock()
        #             cost_time = "{:.3f}秒".format(end_time - start_time)
        #             fields.append(predict_label)
        #             fields.append(cost_time)
        #
        #             if len(fields) == 4:
        #                 #test_list.append(fields)
        #                 # 预测结果写入
        #                 tar_csv.writerow(fields)
        #                 print(fields[0])
        #                 ###lgl
        #                 # if len(test_list) == 5:
        #                 # return render(request, "index.html", {"test_list": test_list})
        #                 #print("预测了1条，准备上传")
        #                 self.send(text_data=json.dumps({
        #                     'message': '预测了第{}条，准备上传'.format(num_i),
        #                     "title": fields[0],
        #                     "content": fields[1],
        #                     "classfy": fields[2],
        #                     "time": fields[3],
        #                 }))
        #                 # return render(request, "index.html", {"test_list": test_list})
        #                 test_list = []
        #                 ###lgl
        #     lines.close()
        #     #file = new File([bytes_data], 'noname', {type: bytes_data.type})
        #     self.send(text_data=json.dumps({
        #         'message': '测试完毕'
        #     }))

    # def receive(self, bytes_data, text_data):
    #     print(text_data)
    #     #file_data = bytes_data #.read().decode("utf-8")
    #
    #     with open("./tokenizer.csv","wb") as code:
    #         code.write(bytes_data)
    #
    #     #测试数据
    #     # file_data = file.read().decode("utf-8")
    #     # lines = file_data.split("\n")
    #     lines = open("./tokenizer.csv", "r", encoding="utf-8")
    #     test_list = list()
    #     self.send(text_data=json.dumps({
    #         'message': '测试开始'
    #     }))
    #     print("开始预测")
    #     with open("data/predict_results.csv".format(os.path.splitext('tokenizer.csv')[0]), "w", encoding="gb18030",
    #               newline="") as wf:
    #         tar_csv = csv.writer(wf, doublequote=False, escapechar="\\")
    #         num_i = 0
    #         for line in lines:
    #             num_i += 1
    #             fields = line.split(",")
    #             # 规定只包含标题和内容两列
    #             if len(fields) != 2:
    #                 continue
    #             content = ""
    #             for field in fields:
    #                 content += field
    #             ###lgl
    #             start_time = time.clock()
    #             predict_label = prediction_model(content)
    #             end_time = time.clock()
    #             cost_time = "{:.3f}秒".format(end_time - start_time)
    #             fields.append(predict_label)
    #             fields.append(cost_time)
    #
    #             if len(fields) == 4:
    #                 #test_list.append(fields)
    #                 # 预测结果写入
    #                 tar_csv.writerow(fields)
    #                 print(fields[0])
    #                 ###lgl
    #                 # if len(test_list) == 5:
    #                 # return render(request, "index.html", {"test_list": test_list})
    #                 #print("预测了1条，准备上传")
    #                 self.send(text_data=json.dumps({
    #                     'message': '预测了第{}条，准备上传'.format(num_i),
    #                     "title": fields[0],
    #                     "content": fields[1],
    #                     "classfy": fields[2],
    #                     "time": fields[3],
    #                 }))
    #                 # return render(request, "index.html", {"test_list": test_list})
    #                 test_list = []
    #                 ###lgl
    #     lines.close()
    #     #file = new File([bytes_data], 'noname', {type: bytes_data.type})
    #     self.send(text_data=json.dumps({
    #         'message': '测试完毕'
    #     }))

    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = '运维咖啡吧：' + text_data_json['message']
    #
    #     self.send(text_data=json.dumps({
    #         'message': message
    #     }))
