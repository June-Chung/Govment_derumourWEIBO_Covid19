import os
import shutil
import scipy.stats

def cal_expection(mlist):

    return sum(mlist)/len(mlist)

def cal_virance(mlist):

    m2list = [i**2 for i in mlist]
    e2_x = cal_expection(m2list)
    ex = cal_expection(mlist)
    return e2_x-(ex**2)

def cov(x,y):

    XY = [x*y for x,y in zip(x,y)]
    E_XY = cal_expection(XY)
    E_X = cal_expection(x)
    E_Y = cal_expection(y)
    D_X = cal_virance(x)
    D_Y = cal_virance(y)

    # print(D_X,D_Y)
    if D_Y ==0 or D_X == 0:
        return 0
    else:
        cov = (E_XY - (E_X * E_Y)) / ((D_X**0.5) * (D_Y**0.5))
    return  cov

def relevanceCalcu():
    maindir = 'news/temp'

    R_type2simi = 0
    R_time2simi = 0
    R_pic2simi = 0
    R_eta2simi = 0
    R_topic2simi = 0
    R_origin2simi = 0
    filecount = 0
    filelist = os.listdir(maindir)
    print(len(filelist))
    for fabu in filelist:
        includingdir = maindir + '/' + fabu
        flist = os.listdir(includingdir)
        for f in  flist:
            if f == '文本相似度.txt':
                print(includingdir+'/'+f)
                with open(includingdir+'/'+f,'r+',encoding='utf-8')as ff:
                    data = ff.readlines()

                datan  = data[1:]
                if len(datan)>=1:
                    simiVec = [float(i.strip().split(" ")[1]) for i in datan]
                    typeVec = [int(i.strip().split(" ")[2])for i in datan]
                    topicVec = [int(i.strip().split(" ")[4]) for i in datan]
                    ateVec = [int(i.strip().split(" ")[5]) for i in datan]
                    picVec = [int(i.strip().split(" ")[6]) for i in datan]
                    originVec = []
                    peak_timeVec = []
                    for i in datan:
                        if i.strip().split(" ")[3] == 'TRUE':
                            originVec.append(1)
                        else:
                            originVec.append(0)

                    for i in datan:
                        times = i.strip().split(" ")[8].split(":")[0]
                        # print(times)
                        hour = int(times)
                        if (hour >= 21 and hour <= 22) or (hour >= 14 and hour <= 15) or (hour >= 11 and hour <= 12):
                            peak_timeVec.append(1)
                        else:
                            peak_timeVec.append(0)
                    R_type2simi += cov(typeVec,simiVec)
                    R_time2simi += cov(peak_timeVec,simiVec)
                    R_pic2simi += cov(picVec,simiVec)
                    R_eta2simi += cov(ateVec,simiVec)
                    R_topic2simi += cov(topicVec,simiVec)
                    R_origin2simi += cov(originVec,simiVec)
                    filecount += 1
                else:
                    print('xxxxxxxxxxxxx'+ includingdir+'/'+f)

    return {"filecount":filecount,"R_type2simi":R_type2simi/filecount,"R_time2simi": R_time2simi/filecount,"R_pic2simi":R_pic2simi/filecount,
            "R_eta2simi":R_eta2simi/filecount,  "R_topic2simi": R_topic2simi/filecount,"R_origin2simi":R_origin2simi/filecount}


#博主粉丝数发博数关注数与微博点赞评论转发的关系
def relevance_FLC_FanBlogFollow():
    maindir = '微博与评论'
    blognum = []
    fannum = []
    followingnum = []
    filelist = os.listdir(maindir)
    simiv = 0
    count =0
    simil = []
    for fabu in filelist:
        includingdir = maindir + '/' + fabu
        flist = os.listdir(includingdir)
        if '粉丝评论点赞.txt' not in flist:
            continue
        else:
            for f in flist:
                if f != '粉丝评论点赞.txt' and f[-3:-1] == 'tx' and f[1:3].isdigit():
                    # print(includingdir+'/'+f)
                    with open(includingdir+'/'+f,'r+',encoding='utf-8')as ff:
                        data = ff.readlines()

                    datan = data[0:6]
                    blognum.append(float(datan[3].strip().split("：")[1]))
                    fannum.append(float(datan[-1].strip().split("：")[1]))
                    followingnum.append(float(datan[-2].strip().split("：")[1]))

                if f == '粉丝评论点赞.txt':
                    print(includingdir+'/'+f)
                    with open(includingdir+'/'+f,'r+',encoding='utf-8')as ff:
                        data = ff.readlines()
                    datan = data[1:]
                    if len(datan)>= 1:
                        templ = [float(i.strip().split(" ")[-1]) for i in datan]
                        tempv = sum(templ) / len(templ)
                        simil.append(tempv)
                    else:
                        simil.append(0)
    return {"微博数与评论转发点赞总数":scipy.stats.spearmanr(blognum,simil),"粉丝数与评论转发点赞总数":scipy.stats.spearmanr(fannum,simil),
            "博主关注数与评论转发点赞总数":scipy.stats.spearmanr(followingnum,simil)}


def relevanceEmoiton():
    maindir = '微博与评论'
    filelist = os.listdir(maindir)
    print(len(filelist))
    emotionVec = []
    typeVec = []
    topicVec = []
    ateVec = []
    picVec = []
    originVec = []
    peak_timeVec = []
    for fabu in filelist:
        includingdir = maindir + '/' + fabu
        flist = os.listdir(includingdir)
        for f in flist:
            if f == '粉丝评论点赞.txt':
                print(includingdir + '/' + f)
                with open(includingdir + '/' + f, 'r+', encoding='utf-8')as ff:
                    data = ff.readlines()

                datan = data[1:]
                print([int(i.strip().split(" ")[3]) for i in datan])
                if len(datan) >= 1:
                    for i in datan:
                        emotionVec.append(float(i.strip().split(" ")[1]))
                        typeVec.append(int(i.strip().split(" ")[3]) )
                        topicVec.append(int(i.strip().split(" ")[4]))
                        ateVec.append(int(i.strip().split(" ")[5]))
                        picVec.append(int(i.strip().split(" ")[-4]))
                        if i.strip().split(" ")[6] == 'TRUE':
                            originVec.append(1)
                        else:
                            originVec.append(0)
                        times = i.strip().split(" ")[9].split(":")[0]
                        # print(times)
                        hour = int(times)
                        if (hour >= 21 and hour <= 22) or (hour >= 14 and hour <= 15) or (hour >= 11 and hour <= 12):
                            peak_timeVec.append(1)
                        else:
                            peak_timeVec.append(0)
                else:
                    print('xxxxxxxxxxxxx' + includingdir + '/' + f)
    # print(R_pic2simi)
    res = {"type与情感": scipy.stats.spearmanr(emotionVec, typeVec), "topic与情感": scipy.stats.spearmanr(emotionVec, topicVec),
           "ate与情感": scipy.stats.spearmanr(emotionVec, ateVec), "pic与情感": scipy.stats.spearmanr(emotionVec, picVec),
           "origin与情感": scipy.stats.spearmanr(emotionVec, originVec),
           "peaktime与情感": scipy.stats.spearmanr(emotionVec, peak_timeVec)}
    return res

def relevance_Emotion_FBF():
    maindir = '微博与评论'
    blognum = []
    fannum = []
    followingnum = []
    filelist = os.listdir(maindir)
    emotionl = []
    for fabu in filelist:
        includingdir = maindir + '/' + fabu
        flist = os.listdir(includingdir)
        if '文本相似度.txt' not in flist:
            continue
        else:
            for f in flist:
                if f != '文本相似度.txt' and f[-3:-1] == 'tx' and f[1:3].isdigit():
                    # print(includingdir+'/'+f)
                    with open(includingdir + '/' + f, 'r+', encoding='utf-8')as ff:
                        data = ff.readlines()

                    datan = data[0:6]
                    blognum.append(float(datan[3].strip().split("：")[1]))
                    fannum.append(float(datan[-1].strip().split("：")[1]))
                    followingnum.append(float(datan[-2].strip().split("：")[1]))

                if f == '情感值.txt':
                    # print(includingdir+'/'+f)
                    with open(includingdir + '/' + f, 'r+', encoding='utf-8')as ff:
                        data = ff.readlines()
                    datan = data[1:]
                    if len(datan) >= 1:
                        templ = [float(i.strip().split(" ")[1]) for i in datan]
                        tempv = sum(templ) / len(templ)
                        emotionl.append(tempv)
                    else:
                        emotionl.append(0)

    res = {"微博数与情感": scipy.stats.spearmanr(emotionl, blognum), "粉丝数与情感": scipy.stats.spearmanr(emotionl, fannum),
           "关注数与情感": scipy.stats.spearmanr(emotionl, followingnum)}
    return res

def relevanceLIKEFORWARDCOM():
    maindir = '微博与评论'
    filelist = os.listdir(maindir)
    print(len(filelist))
    emotionVec = []
    typeVec = []
    topicVec = []
    ateVec = []
    picVec = []
    originVec = []
    peak_timeVec = []
    FLSVec  =[]
    for fabu in filelist:
        includingdir = maindir + '/' + fabu
        flist = os.listdir(includingdir)
        for f in flist:
            if f == '粉丝评论点赞.txt':
                print(includingdir + '/' + f)
                with open(includingdir + '/' + f, 'r+', encoding='utf-8')as ff:
                    data = ff.readlines()

                datan = data[1:]
                print([int(i.strip().split(" ")[3]) for i in datan])
                if len(datan) >= 1:
                    for i in datan:
                        emotionVec.append(float(i.strip().split(" ")[1]))
                        FLSVec.append(int(i.strip().split(" ")[-1]))
                        typeVec.append(int(i.strip().split(" ")[3]))
                        topicVec.append(int(i.strip().split(" ")[4]))
                        ateVec.append(int(i.strip().split(" ")[5]))
                        if int(i.strip().split(" ")[7]) == 0:
                            picVec.append(2)
                        else:
                            picVec.append(int(i.strip().split(" ")[7]))
                        if i.strip().split(" ")[6] == 'TRUE':
                            originVec.append(1)
                        else:
                            originVec.append(0)
                        times = i.strip().split(" ")[9].split(":")[0]
                        # print(times)
                        hour = int(times)
                        if (hour >= 21 and hour <= 22) or (hour >= 14 and hour <= 15) or (hour >= 11 and hour <= 12):
                            peak_timeVec.append(1)
                        else:
                            peak_timeVec.append(0)
                else:
                    print('xxxxxxxxxxxxx' + includingdir + '/' + f)
    # print(R_pic2simi)
    res = {"type与微博点赞评论转发数": scipy.stats.spearmanr(emotionVec, FLSVec), "topic与微博点赞评论转发数": scipy.stats.spearmanr(FLSVec, topicVec),
           "ate与微博点赞评论转发数": scipy.stats.spearmanr(FLSVec, ateVec), "pic与微博点赞评论转发数": scipy.stats.spearmanr(FLSVec, picVec),
           "origin与微博点赞评论转发数": scipy.stats.spearmanr(FLSVec, originVec),
           "peaktime与微博点赞评论转发数": scipy.stats.spearmanr(FLSVec, peak_timeVec)}
    return res

def patchProce():
    maindir = 'news/newtmp'
    destinationdir = 'news/temp'
    filelist = os.listdir(maindir)
    for fabu in filelist:
        includingdir = maindir + '/' + fabu
        flist = os.listdir(includingdir)
        for f in flist:
            if f != '文本相似度.txt' and f[-3:-1] == 'tx' and f[1:3].isdigit():
                sourcePath = includingdir + '/' + f
                destinationpath = destinationdir + '/' + fabu + '/' + f
                shutil.copyfile(sourcePath,destinationpath)

def getlist(wholelist,index):

    result = []
    for line  in wholelist:
       x =  line.strip().split()
       result.append(float(x[index]))

    return result

def Relevance_configurationEmotion():

    maindir = '微博与评论'
    fabulist = os.listdir(maindir)

    R_e2s = 0.0
    filecount = 0
    emovec = []
    simivec = []
    for fabuname in fabulist:
        similpath = maindir+'/'+fabuname + '/文本相似度.txt'
        emotionpath = maindir+'/'+fabuname + '/粉丝评论点赞.txt'
        if os.path.exists(similpath):
            with open(similpath,'r+',encoding='utf-8')as f:
                datasimi = f.readlines()
            with open(emotionpath,'r+',encoding='utf-8')as f:
                dataemo = f.readlines()
            datasimi = datasimi[1:]
            dataemo = dataemo[1:]
            if len(datasimi)>=1:
                emovec.extend(getlist(dataemo,-1))
                simivec.extend(getlist(datasimi,1))

    return scipy.stats.spearmanr(emovec,simivec)

def relevance_detailType_emotion_FSL():
    maindir = '微博与评论'
    filelist = os.listdir(maindir)
    print(len(filelist))
    type1 = []
    type1_emotion = []
    type1_fcl = []
    type2 = []
    type2_emotion = []
    type2_fcl = []
    type3 = []
    type3_emotion = []
    type3_fcl = []

    for fabu in filelist:
        includingdir = maindir + '/' + fabu
        flist = os.listdir(includingdir)
        for f in flist:
            if f == '粉丝评论点赞.txt':
                # print(includingdir + '/' + f)
                with open(includingdir + '/' + f, 'r+', encoding='utf-8')as ff:
                    data = ff.readlines()

                datan = data[1:]
                if len(datan)>0:
                    for i in datan:
                        if int(i.strip().split(" ")[3]) == 1:
                            type1.append(1)
                            type1_emotion.append(float(i.strip().split(" ")[1]))
                            type1_fcl.append(int(i.strip().split(" ")[-1]))
                        elif int(i.strip().split(" ")[3]) == 2:
                            type2.append(2)
                            type2_emotion.append(float(i.strip().split(" ")[1]))
                            type2_fcl.append(int(i.strip().split(" ")[-1]))
                        elif int(i.strip().split(" ")[3]) == 3:
                            type3.append(3)
                            type3_emotion.append(float(i.strip().split(" ")[1]))
                            type3_fcl.append(int(i.strip().split(" ")[-1]))

    res = {"type1与情感": scipy.stats.spearmanr(type1, type1_emotion),
           "type1与点赞转发评论数": scipy.stats.spearmanr(type1, type1_fcl),
           "type2与情感": scipy.stats.spearmanr(type2, type2_emotion),
           "type2与点赞转发评论数": scipy.stats.spearmanr(type2, type2_fcl),
           "type3与情感": scipy.stats.spearmanr(type3, type3_emotion),
           "type3与点赞转发评论数": scipy.stats.spearmanr(type3,type3_fcl)}
    return res


def relevance_FLS_Configuration():
    maindir = '微博与评论'
    fabulist = os.listdir(maindir)

    R_e2s = 0.0
    filecount = 0
    emovec = []
    simivec = []
    for fabuname in fabulist:
        similpath = maindir + '/' + fabuname + '/文本相似度.txt'
        emotionpath = maindir + '/' + fabuname + '/粉丝评论点赞.txt'
        if os.path.exists(similpath):
            with open(similpath, 'r+', encoding='utf-8')as f:
                datasimi = f.readlines()
            with open(emotionpath, 'r+', encoding='utf-8')as f:
                dataFLS = f.readlines()
            datasimi = datasimi[1:]
            dataemo = dataFLS[1:]
            if len(datasimi) >= 1:
                emovec.extend(getlist(dataemo, -1))
                simivec.extend(getlist(datasimi, 1))

    return scipy.stats.spearmanr(emovec, simivec)


if __name__ == '__main__':
    #相关度1：
    # x= relevanceCalcu()
    # print(x)

    #各大变量与情感之间的关系
    # y = relevanceEmoiton()
    # for k,v in y.items():
    #     print(k,v)

    #粉丝数关注数发博数与微博情感
    # z = relevanceFanBlogFollow()
    # for k,v in z.items():
    #     print(k,v)
    # print(z)

    #评论点赞转发数与各大变量的关系
    # d = relevanceLIKEFORWARDCOM()
    # for k,v in d.items():
    #     print(k,v)

    #情感与认知程度：
    # es = Relevance_configurationEmotion()
    # print(es)

    #情感与博主的粉丝数微博数和关注数：
    # S = relevance_Emotion_FBF()
    # for k,v in S.items():
    #     print(k,v)

    # 博主粉丝数发博数关注数与微博点赞评论转发的关系
    # d = relevance_FLC_FanBlogFollow()
    # for k,v in d.items():
    #     print(k,v)

    #辟谣各个类型与情感，点赞转发评论数的关系
    # c = relevance_detailType_emotion_FSL()
    # for k,v in c.items():
    #     print(k,v)

    #点赞转发与认知程度：
    f = relevance_FLS_Configuration()
    print("点赞转发与认知程度:   ",f)