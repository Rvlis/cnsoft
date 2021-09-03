"""
raw_data_classification
"""

import csv
import os

def raw_data_classification(raw_data_path):
    label_dict = {
        "100": "民生",
        "101": "文化",
        "102": "娱乐",
        "103": "体育",
        "104": "财经",
        "106": "房产",
        "107": "汽车",
        "108": "教育",
        "109": "科技",
        "110": "军事",
        "112": "旅游",
        "113": "国际",
        "114": "股票",
        "115": "农业",
        "116": "游戏"       
    }
    label_num = {
        "财经": 0,
        "房产": 0,
        "教育": 0,
        "科技": 0,
        "军事": 0,
        "汽车": 0,
        "体育": 0,
        "游戏": 0,
        "娱乐": 0,
        "其他": 0
    }

    label_set = set(["财经", "房产", "教育", "科技", "军事", "汽车", "体育", "游戏", "娱乐", "其他"])



    cj_csv = csv.writer(open("./data/财经.csv", "w", newline="", encoding="gb18030"), doublequote=False, escapechar="\\")
    fc_csv = csv.writer(open("./data/房产.csv", "w", newline="", encoding="gb18030"), doublequote=False, escapechar="\\")
    jy_csv = csv.writer(open("./data/教育.csv", "w", newline="", encoding="gb18030"), doublequote=False, escapechar="\\")
    kj_csv = csv.writer(open("./data/科技.csv", "w", newline="", encoding="gb18030"), doublequote=False, escapechar="\\")
    js_csv = csv.writer(open("./data/军事.csv", "w", newline="", encoding="gb18030"), doublequote=False, escapechar="\\")
    qc_csv = csv.writer(open("./data/汽车.csv", "w", newline="", encoding="gb18030"), doublequote=False, escapechar="\\")
    ty_csv = csv.writer(open("./data/体育.csv", "w", newline="", encoding="gb18030"), doublequote=False, escapechar="\\")
    yx_csv = csv.writer(open("./data/游戏.csv", "w", newline="", encoding="gb18030"), doublequote=False, escapechar="\\")
    yl_csv = csv.writer(open("./data/娱乐.csv", "w", newline="", encoding="gb18030"), doublequote=False, escapechar="\\")
    qt_csv = csv.writer(open("./data/其他.csv", "w", newline="", encoding="gb18030"), doublequote=False, escapechar="\\")

    # set去重
    cj_set = set()
    fc_set = set()
    jy_set = set()
    kj_set = set()
    js_set = set()
    qc_set = set()
    ty_set = set()
    yx_set = set()
    yl_set = set()
    qt_set = set()



    MAX_LENGTH = 0
    FLAG = False

    with open(raw_data_path, encoding="utf-8") as rf:
        lines = rf.readlines()
        for line in lines:
            FLAG = False
            line = line.strip().split("_!_")
            # print(line)
            # os.system("pause")
            # 限定长度
            if len(line[3]) > 50:
                continue
            label = label_dict[line[1]]
            if label == "财经":
                if line[3] not in cj_set: 
                    cj_csv.writerow([line[3], label])
                    cj_set.add(line[3])
                    FLAG = True
            elif label == "房产":
                # fc_csv.writerow([line[3], label])
                if line[3] not in fc_set: 
                    fc_csv.writerow([line[3], label])
                    fc_set.add(line[3])
                    FLAG = True
            elif label == "教育":
                # jy_csv.writerow([line[3], label])
                if line[3] not in jy_set: 
                    jy_csv.writerow([line[3], label])
                    jy_set.add(line[3])
                    FLAG = True
            elif label == "科技":
                # kj_csv.writerow([line[3], label])
                if line[3] not in kj_set: 
                    kj_csv.writerow([line[3], label])
                    kj_set.add(line[3])
                    FLAG = True
            elif label == "军事":
                # js_csv.writerow([line[3], label])
                if line[3] not in js_set: 
                    js_csv.writerow([line[3], label])
                    js_set.add(line[3])
                    FLAG = True
            elif label == "汽车":
                # qc_csv.writerow([line[3], label])
                if line[3] not in qc_set: 
                    qc_csv.writerow([line[3], label])
                    qc_set.add(line[3])
                    FLAG = True
            elif label == "体育":
                # ty_csv.writerow([line[3], label])
                if line[3] not in ty_set: 
                    ty_csv.writerow([line[3], label])
                    ty_set.add(line[3])
                    FLAG = True
            elif label == "游戏":
                # yx_csv.writerow([line[3], label])
                if line[3] not in yx_set: 
                    yx_csv.writerow([line[3], label])
                    yx_set.add(line[3])
                    FLAG = True
            elif label == "娱乐":
                # yl_csv.writerow([line[3], label])
                if line[3] not in yl_set: 
                    yl_csv.writerow([line[3], label])
                    yl_set.add(line[3])
                    FLAG = True
            else:
                # qt_csv.writerow([line[3], "其他"])
                if line[3] not in qt_set: 
                    qt_csv.writerow([line[3], "其他"])
                    qt_set.add(line[3])
                    FLAG = True

            if label in label_set and FLAG:
                label_num[label] = label_num[label] + 1
            elif label not in label_set and FLAG:
                label_num["其他"] = label_num["其他"] + 1

            if len(line[3]) > MAX_LENGTH:
                MAX_LENGTH = len(line[3])

        for item in label_num.items():
            print(item)

    print("MAX_LENGTH is", MAX_LENGTH)

raw_data_classification("./toutiao_cat_data.txt")
