import  os
import re
import json

def calculate_similarity_and_writeINTOtxt(blogdir,blogpath,commentSimi_storepath):
    blog_list = new_cleanArticle(blogpath)
    # print(blog_list[0])
    tmp_list=[]
    # for blo in blog_list:
    #     print('show: ',blo)
    for blog in blog_list:
        article = blog[-1]
        article_type=blog[1]
        article_id = blog[0]
        article_topic = blog[2]
        article_ate = blog[3]
        article_orig = blog[4]
        article_pic = blog[5]
        article_time = blog[6]
        print(article)
        article_v = get_article_vec(article)
        # print(article_id)
        print(commentSimi_storepath+"/"+article_id+".json")
        if os.path.exists(commentSimi_storepath+"/"+article_id+".json"):
            # print(article_id)
            # print('11111')
            with open(commentSimi_storepath+"/"+article_id+".json",'r+',encoding='utf-8')as f:
                commentVec_dic = json.load(f)
            percent_sum = 0

            if len(commentVec_dic) != 0:
                for id,comVec in commentVec_dic.items():
                    percent_sum += CosSimilar(article_v,comVec)
                this_article_mean_similar = percent_sum/len(commentVec_dic)
            else:
                this_article_mean_similar = -1

            tmp = [article_id,this_article_mean_similar,article_type,article_orig,article_topic,article_ate,article_pic,article_time,article]
            tmp_list.append(tmp)
            # print(tmp_list)
            print(blogdir+"文本相似度2.txt",'sssssssssssssssssssssssssss')
            with open(blogdir+"文本相似度2.txt",'w+',encoding='utf-8')as f:
                f.write("微博id" + " " + "评论平均相关度" + " " + "辟谣类型" + " " + "原创与否"+" "+"是否带话题"+" "+"是否有@"+" "+"是否有图片"+" "+"微博内容" + "\n")
                for item in tmp_list:
                    print(item)
                    f.write(item[0]+" "+str(item[1])+" "+item[2]+" "+item[3]+" "+item[4]+" "+item[5]+" "+item[6]+" "+item[7]+" "+item[8]+"\n")
        else:
            # print(article_id)
            print('222222')

def process_():
    maindir = '微博与评论'
    # maindir ='news/没有相似文本的'
    dirlist = os.listdir(maindir)
    for dirname in dirlist:
        child_dirpath = maindir + '/' + dirname
        fabu_filelist = os.listdir(child_dirpath)
        for filename in fabu_filelist:
            if filename[-3:-1] == 'cs':
                blogdir = child_dirpath + '/'
                blogpath = blogdir + filename
                comment_store_dir = './commentV/' + dirname
                if os.path.exists(comment_store_dir):
                    # calculate_similarity_and_writeINTOtxt(blogdir,blogpath,comment_store_dir)
                    process_2(blogdir,blogpath,comment_store_dir)
                else:
                    print('不存在路径',comment_store_dir)


def new_cleanArticle(blogpath):
    with open(blogpath, 'r+', encoding='utf-8')as f:
        data = f.readlines()
    blog_all = []
    datan = data[1:]
    # print('s', datan)
    for i in range(len(datan)):
        if datan[i][0] != '原' and datan[i][0] != '转' and i + 1 < len(datan) and datan[i + 1][0] != '原' and datan[i + 1][0] != '转':
            xon = datan[i]

            if re.search('"http://.*\.video\.weibocdn\.com/.*\"',xon) or re.search(r"http..*\.jpg",xon):
                blog_pic = '1'
            else:
                blog_pic = '2'
            con, i = re.subn('"http://.*\.video\.weibocdn\.com/.*\"', '', xon)
            # con.replace(r'\"http://f.video\..*,video\"','')
            conlist = con.strip().split(',')
            # print(conlist)
            blog_id = conlist[0]
            blog_cont = conlist[1]
            blog_type = conlist[-1]
            blog_orig = conlist[-9]
            blog_time = conlist[-6]
            blog_cont = blog_cont.replace(r"http..*\.jpg", "")
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
            print(blog_id)
            blog_all.append([blog_id, blog_type, blog_topic, blog_ate, blog_orig, blog_pic, blog_time, blog_cont])

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
            blog_cont = blog_cont.replace(r"http..*\.jpg", "")
            # 是否有带话题#xxxxx#
            if re.match("#.*#", blog_cont):
                blog_topic = "1"
            else:
                blog_topic = "0"
            if re.match(".*@.*", blog_cont):
                blog_ate = "1"
            else:
                blog_ate = "0"
            blog_all.append([blog_id, blog_type, blog_topic, blog_ate, blog_orig, blog_pic, blog_time, blog_cont])

        elif datan[i][0] != '原' and datan[i][0] != '转' and i + 1 < len(datan) and datan[i + 1][0] == '转':
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
            blog_cont = blog_cont.replace(r"http..*\.jpg", "")
            # 是否有带话题#xxxxx#
            if re.match("#.*#", blog_cont):
                blog_topic = "1"
            else:
                blog_topic = "0"
            if re.match(".*@.*", blog_cont):
                blog_ate = "1"
            else:
                blog_ate = "0"
            blog_all.append([blog_id, blog_type, blog_topic, blog_ate, blog_orig, blog_pic, blog_time, blog_cont])

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
            print('conlist', conlist)
            blog_id = conlist[0]
            blog_cont = conlist[1]
            blog_type = conlist[-1]
            blog_orig = conlist[-9]
            blog_time = conlist[-6]
            blog_cont = blog_cont.replace(r"http..*\.jpg", "")
            # 是否有带话题#xxxxx#
            if re.match(r".*#.*#*", blog_cont):
                blog_topic = "1"
            else:
                blog_topic = "0"
            if re.match(r".*@.*", blog_cont):
                blog_ate = "1"
            else:
                blog_ate = "0"
            print(blog_id)
            blog_all.append([blog_id, blog_type, blog_topic, blog_ate, blog_orig, blog_pic, blog_time, blog_cont])

        else:
            # print(len(blog_all))
            # print('3')
            continue

    return blog_all

def process_2(blogdir,blogpath,commentSimi_storepath):
    blog_list = new_cleanArticle(blogpath)
    tmp_list = []
    with open(blogdir + "文本相似度.txt", 'r+', encoding='utf-8')as f:
        datatemp = f.readlines()
    datas = datatemp[1:]
    if len(datas)!= 0 :
        article_simi_dic = {}
        for item in datas:
            xlist = item.strip().split(' ')
            article_simi_dic[xlist[0]] = xlist[1]
        for blog in blog_list:
            article = blog[-1]
            article_type = blog[1]
            article_id = blog[0]
            article_topic = blog[2]
            article_ate = blog[3]
            article_orig = blog[4]
            article_pic = blog[5]
            article_time = blog[6]
            # print(article_id)
            if article_id in article_simi_dic:
                tmp = [article_id, article_simi_dic[article_id], article_type, article_orig, article_topic, article_ate,
                           article_pic, article_time, article]
                tmp_list.append(tmp)
            else:
                continue


        print(blogdir + "文本相似度2.txt", 'sssssssssssssssssssssssssss')
        with open(blogdir + "文本相似度2.txt", 'w+', encoding='utf-8')as f:
                f.write("微博id" + " " + "评论平均相关度" + " " + "辟谣类型" + " " + "原创与否" + " " + "是否带话题" + " " + "是否有@" + " " + "是否有图片" + " " + "微博内容" + "\n")
                for item in tmp_list:
                    print(item)
                    f.write(item[0] + " " + str(item[1]) + " " + item[2] + " " + item[3] + " " + item[4] + " " + item[5] + " " + item[6] + " " + item[7] + " " + item[8] + "\n")
    else:
        print('22222')


if __name__ == '__main__':
    process_()