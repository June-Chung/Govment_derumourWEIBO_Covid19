from aip import AipNlp
from openpyxl import load_workbook
import time
import csv
import os
import json
import re
APP_ID = '19977603'
API_KEY = 'V29fofBiufPE1gLaNRjkNEGW'
SECRET_KEY = 'S7PeE3E9uawi1jVv49AZ6FGmxaUh3x7g'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

result = {}
def clean_article(filepath,emotiondic):
    # print(filepath)
    with open(filepath, 'r+', encoding='utf-8')as f:
        data = f.readlines()
    blog_all = []
    datan = data[1:]
    print('s',datan)
    for i in range(len(datan)):
        if datan[i][0] != '原' and datan[i][0] != '转' and i + 1 < len(datan) and datan[i + 1][0] != '原' and datan[i+1][0] !='转':
            xon = datan[i]
            if re.search('"http://.*\.video\.weibocdn\.com/.*\"',xon) or re.search(r"http..*\.jpg",xon):
                blog_pic = '1'
            else:
                blog_pic = '2'
            con, i = re.subn('"http://.*\.video\.weibocdn\.com/.*\"', '', xon)
            conlist = con.strip().split(',')
            # print(conlist)
            blog_id = conlist[0]
            blog_cont = conlist[1]
            blog_type = conlist[-1]
            blog_orig = conlist[-9]
            blog_time = conlist[-6]
            blog_fclSUM = int(conlist[-2]) + int(conlist[-3]) + int(conlist[-4])
            # blog_cont = blog_cont.replace(r"http..*\.jpg", "")
            #是否有带话题#xxxxx#
            if re.match(r".*#.*#*",blog_cont):
                blog_topic = "1"
            else:
                blog_topic = "0"
            if re.match(r".*@.*",blog_cont):
                blog_ate = "1"
            else:
                blog_ate = "0"
            # print('1')
            # print(blog_id)
            signal = blog_id+'.csv'
            if signal in emotiondic:
                blogcomment_Emotion = emotiondic[signal]
                blog_all.append([blog_id, blogcomment_Emotion,blog_type, blog_topic,blog_ate,blog_orig,blog_pic,blog_time,blog_fclSUM])

        elif datan[i][0] != '原' and datan[i][0] != '转' and i + 1 < len(datan) and datan[i + 1][0] == '原':
            con = datan[i]
            con_next1 = datan[i + 2]
            if re.search('"http://.*\.video\.weibocdn\.com/.*\"', con_next1) or re.search(r"http..*\.jpg", con_next1):
                blog_pic = '1'
            else:
                blog_pic = '2'
            con_next, i = re.subn('"http://f\.video\.weibocdn\.com/.*\"', '', con_next1)
            # print(con)
            conlist = con.strip().split(',')
            blog_id = conlist[0]
            blog_cont = conlist[1]
            con_next_list = con_next.strip().split(',')
            # print(con_next_list)
            blog_type = con_next_list[-1]
            blog_cont += ","
            blog_cont += con_next_list[0]
            # print(blog_cont)
            blog_orig = con_next_list[-9]
            blog_time = con_next_list[-6]
            blog_fclSUM = int(con_next_list[-2]) + int(con_next_list[-3]) + int(con_next_list[-4])
            # 是否有带话题#xxxxx#
            if re.match("#.*#", blog_cont):
                blog_topic = "1"
            else:
                blog_topic = "0"
            if re.match(".*@.*", blog_cont):
                blog_ate = "1"
            else:
                blog_ate = "0"
            signal = blog_id + '.csv'
            if signal in emotiondic:
                blogcomment_Emotion = emotiondic[signal]
                blog_all.append(
                    [blog_id, blogcomment_Emotion, blog_type, blog_topic, blog_ate, blog_orig, blog_pic, blog_time,
                     blog_fclSUM])

        elif datan[i][0] != '原' and datan[i][0] != '转' and i + 1 < len(datan) and datan[i + 1][0] == '转' :
            con = datan[i]
            con_next1 = datan[i + 1]
            if re.search('"http://.*\.video\.weibocdn\.com/.*\"', con_next1) or re.search(r"http..*\.jpg", con_next1):
                blog_pic = '1'
            else:
                blog_pic = '2'
            con_next, i = re.subn('"http://f\.video\.weibocdn\.com/.*\"', '', con_next1)
            # print(con)
            conlist = con.strip().split(',')
            blog_id = conlist[0]
            blog_cont = conlist[1]
            con_next_list = con_next.strip().split(',')
            # print(con_next_list)
            blog_type = con_next_list[-1]
            blog_cont += ","
            blog_cont += con_next_list[0]
            # print(blog_cont)
            blog_orig = con_next_list[-9]
            blog_time = con_next_list[-6]
            blog_fclSUM = int(con_next_list[-2]) + int(con_next_list[-3]) + int(con_next_list[-4])
            # 是否有带话题#xxxxx#
            if re.match("#.*#", blog_cont):
                blog_topic = "1"
            else:
                blog_topic = "0"
            if re.match(".*@.*", blog_cont):
                blog_ate = "1"
            else:
                blog_ate = "0"
            signal = blog_id + '.csv'
            if signal in emotiondic:
                blogcomment_Emotion = emotiondic[signal]
                blog_all.append(
                    [blog_id, blogcomment_Emotion, blog_type, blog_topic, blog_ate, blog_orig, blog_pic, blog_time,
                     blog_fclSUM])

        elif datan[i][0] != '原' and datan[i][0] != '转' and i + 1 == len(datan):
            xon = datan[i]
            # print(xon)
            if re.search('"http://.*\.video\.weibocdn\.com/.*\"', xon) or re.search(r"http..*\.jpg", xon):
                blog_pic ='1'
            else:
                blog_pic = '2'
            con, i = re.subn('"http://.*\.video\.weibocdn\.com/.*\"', '', xon)
            # con.replace(r'\"http://f.video\..*,video\"','')
            conlist = con.strip().split(',')
            # print('conlist',conlist)
            blog_id = conlist[0]
            blog_cont = conlist[1]
            blog_type = conlist[-1]
            blog_orig = conlist[-9]
            blog_time = conlist[-6]
            blog_fclSUM = int(conlist[-2]) + int(conlist[-3]) + int(conlist[-4])
            # 是否有带话题#xxxxx#
            if re.match(r".*#.*#*", blog_cont):
                blog_topic = "1"
            else:
                blog_topic = "0"
            if re.match(r".*@.*", blog_cont):
                blog_ate = "1"
            else:
                blog_ate = "0"
            # print('1')
            signal = blog_id + '.csv'
            if signal in emotiondic:
                blogcomment_Emotion = emotiondic[signal]
                blog_all.append(
                    [blog_id, blogcomment_Emotion, blog_type, blog_topic, blog_ate, blog_orig, blog_pic, blog_time,
                     blog_fclSUM])

        else:
            continue

    return blog_all

def loadprocessComment(path):

    comfilelist = os.listdir(path)
    for fname in comfilelist:
        print('发布:::::::::::',path+'/'+fname)
        with open(path+'/'+fname,'r+',encoding='utf-8')as f:
            data = f.readlines()
        datan = data[1:]
        tmpresult = []
        if len(datan) == 0:
            result[fname] = -1
            continue
        try:
            #读取所有评论，清洗评论，然后识别情感倾向，将结果临时存入数组
            for line in datan:
                conlist = line.strip().split(',')
                commentContent = conlist[-3]
                cleaned_content = cleancontent(commentContent)
                if cleaned_content != "":
                    rslt = detectEmotion(cleaned_content)
                    tmpresult.append(rslt)
                    time.sleep(0.2)
                else:
                    tmpresult.append(-1)
        except:
            pass
        finally:
            # print(devideEmotion(tmpresult))
            print(tmpresult)
        if len(tmpresult) == 0:
            result[fname] = -1
        else:
            result[fname] = devideEmotion(tmpresult)

    with open(path+'/评论情感值.json','w+',encoding='utf-8')as f:
            f.writelines(json.dumps(result))

def devideEmotion(list):
    negativeone = list.count(-1)
    positiveone = list.count(1)
    tow = list.count(2)
    zero = list.count(0)
    tl = [negativeone,positiveone,tow,zero]
    maxn =  max(tl)
    if negativeone == maxn:
        return -1
    elif positiveone == maxn:
        return 1
    elif tow == maxn:
        return 2
    elif zero == maxn:
        return 0

def detectEmotion(content):
    print(content)
    time.sleep(0.5)
    result = client.sentimentClassify(content)
    result = result['items'][0]['sentiment']
    return result

def cleancontent(string):
    cleaned = string.replace(" ", "")
    cleaned = cleaned.replace("\xa0", "")
    if cleaned[-4:] == '来自网页' or cleaned == '//' or cleaned=='信息发布微平台':
        return ""
    else:
        return cleaned

def process_():
    maindir = '补充'
    # maindir = 'demo'
    pathlist = os.listdir(maindir)
    for fabupath in pathlist:
        childpath = maindir+'/'+fabupath
        innnerfilelist = os.listdir(childpath)
        # print(innnerfilelist)
        for fname in innnerfilelist:
            if fname[-4:] == 'ment':
                # print(fname)
                path = childpath + '/' + fname
                loadprocessComment(path)

def generateFile(maindir,fabupath):
    fnamelist = os.listdir(maindir+'/'+fabupath)
    for fn in fnamelist:
        if fn[-3:] == 'csv':
            filepath = maindir + '/' +fabupath + '/' + fn
            emotionfilepath = maindir + '/' +fabupath + '/' + fabupath+'tempcomment'+ '/' +'评论情感值.json'
            with open(emotionfilepath,'r+',encoding='utf-8')as ff:
                emotiondic = json.load(ff)
            bloglist = clean_article(filepath,emotiondic)

            with open(maindir + '/' +fabupath+"/情感值.txt",'w+',encoding='utf-8')as f:
                f.write("微博id" + " " + "微博评论情感值" + " " +"辟谣类型" + " " + "原创与否"+" "+"是否带话题"+" "+"是否有@"+" "+"是否有图片"+" "+"微博内容" + "\n")
                for item in bloglist:
                    # print(item)
                    f.write(item[0]+" "+str(item[1])+" "+" "+item[2]+" "+item[3]+" "+item[4]+" "+item[5]+" "+item[6]+" "+item[7]+" "+item[8]+"\n")

def process2_():
    maindir = '补充'
    dirlist = os.listdir(maindir)
    for dirname  in dirlist:
        generateFile(maindir,dirname)


def likeforwardcomFile(maindir,fabupath):
    fnamelist = os.listdir(maindir + '/' + fabupath)
    for fn in fnamelist:
        if fn[-3:] == 'csv':
            filepath = maindir + '/' + fabupath + '/' + fn
            emotionfilepath = maindir + '/' + fabupath + '/' + fabupath + 'tempcomment' + '/' + '评论情感值.json'
            with open(emotionfilepath, 'r+', encoding='utf-8')as ff:
                emotiondic = json.load(ff)
            bloglist = clean_article(filepath, emotiondic)
            with open(maindir + '/' + fabupath + "/粉丝评论点赞.txt", 'w+', encoding='utf-8')as f:
                f.write(
                    "微博id" + " " + "微博评论情感值" + " " + "辟谣类型" + " " + "原创与否" + " " + "是否带话题" + " " + "是否有@" + " " + "是否有图片" + " " + "评论转发点赞总数" + "\n")
                for item in bloglist:
                    # print(item)
                    f.write(item[0] + " " + str(item[1]) + " " + " " + item[2] + " " + item[3] + " " + item[4] + " " + item[5] + " " + item[6] + " " + item[7] + " " + str(item[8]) + "\n")


def process3_():
    maindir = '微博与评论'
    dirlist = os.listdir(maindir)
    for dirname  in dirlist:
        likeforwardcomFile(maindir,dirname)

if __name__ =='__main__':
    # lst = [0, 0, 0, 0, 0, 0, 2, -1, 0, 0, 0, 2, 2, 2, 0, 0]
    # print(devideEmotion(lst))

    # process_()
    # process2_()
    process3_()