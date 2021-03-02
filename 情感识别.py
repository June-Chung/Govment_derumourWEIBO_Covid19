from aip import AipNlp
from openpyxl import load_workbook
import time
import csv

title = '高架桥'
data = load_workbook('情感识别数据/'+title+'.xlsx')
sheet = data['Sheet1']

APP_ID = '19977603'
API_KEY = 'V29fofBiufPE1gLaNRjkNEGW'
SECRET_KEY = 'S7PeE3E9uawi1jVv49AZ6FGmxaUh3x7g'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


contentset = set()
contentDic = {}
positiveScore = 0
negativeScore = 0
medialScore = 0
for cell in sheet:
    content  = cell[0].value
    try:
        if content is  None or content=='转发微博':
            content= cell[1].value
            if content is None or content=='转发微博':
                continue
            else:
                if len(content) > 1000:
                    content = content[0:1000]
                if content not in contentset:
                    contentset.add(content)
                    time.sleep(0.8)
                    result = client.sentimentClassify(content)
                    print(result)
                    classify = result['items'][0]['sentiment']
                    contentDic[content] = classify
                    if classify == 0:
                        negativeScore += 1
                    elif classify == 1:
                        medialScore += 1
                    elif classify == 2:
                        positiveScore += 1
                elif content in contentset:
                    s = contentDic[content]
                    if s == 0:
                        negativeScore += 1
                    elif s == 1:
                        medialScore += 1
                    elif s == 2:
                        positiveScore += 1
        else:
            if content not in contentset:
                content = content[0:1000]
                contentset.add(content)
                time.sleep(0.5)
                result = client.sentimentClassify(content)
                print(result)
                classify = result['items'][0]['sentiment']
                contentDic[content] = classify
                if classify == 0:
                    negativeScore += 1
                elif classify == 1:
                    medialScore += 1
                elif classify == 2:
                    positiveScore += 1
            elif content in contentset:
                s = contentDic[content]
                if s == 0:
                    negativeScore += 1
                elif s == 1:
                    medialScore += 1
                elif s == 2:
                    positiveScore += 1
    except:
        time.sleep(5)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        continue



print(title,':   ','N:: ',negativeScore,'M:: ',medialScore,'P:: ',positiveScore)

with open('emeotion.txt','a',encoding='utf-8')as ff:
        ff.writelines('\n'+title+ ':     ' + '   N:: '+str(negativeScore)+' M:: '+str(medialScore)+'    P:: '+str(positiveScore))



APP_ID = '19977603'
API_KEY = 'V29fofBiufPE1gLaNRjkNEGW'
SECRET_KEY = 'S7PeE3E9uawi1jVv49AZ6FGmxaUh3x7g'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
text = ''
text = sheet[2][0].value
# x = client.sentimentClassify(text)
content = text

if content is not None:
    print(content)
    if content is None:
        print('error')
    else:
        result = client.sentimentClassify(content)
        classify = result['items'][0]['sentiment']
        if classify == 0:
            negativeScore += 1
        elif classify == 1:
            medialScore += 1
        elif classify == 2:
            positiveScore += 1

print('N:: ', negativeScore, 'M:: ', medialScore, 'P:: ', positiveScore)
choice = int (input())
print(type(choice))

# p = x['items'][0]['positive_prob']
# n = x['items'][0]['negative_prob']
# 0:负向，1:中性，2:正向