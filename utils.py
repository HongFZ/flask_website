import pymysql
import pandas as pd
import requests
import json
import jieba
import jieba.analyse


def get_conn():
    conn = pymysql.connect(host="localhost",user="root",password="mysql980114",
    db="sufeoj1",charset="utf8")
    cursor = conn.cursor()
    return conn, cursor

def close_conn(conn, cursor):
    cursor.close()
    conn.close()

def query(sql,*args):
    conn, cursor = get_conn()
    cursor.execute(sql,args)
    result = cursor.fetchall()
    close_conn(conn, cursor)
    return result


#homework page
def get_score_data(class_id, hw_id):
    sql = 'select hw'+str(hw_id)+' from '+str(class_id)
    result = query(sql)
    return result

def get_submit_time(class_id, hw_id):
    sql = 'select hw'+str(hw_id)+'_summit from '+str(class_id)
    result = query(sql)
    return result

def fenci(text):
    jieba.load_userdict(r'D:\ZHF\Gra-Paper\Minor\addword.txt')
    stopwords = []
    with open(r'D:\ZHF\Gra-Paper\Minor\stopword.txt',encoding='UTF-8') as f:
        lines = f.readlines()
        for line in lines:
            stopwords.append(line.strip('\n'))
    fenci = jieba.lcut(text)
    final = []
    for word in fenci:
        if word not in stopwords:
            final.append(word)
    return final

def is_sensitive(text):
    words=[]
    with open(r'D:\ZHF\Gra-Paper\Minor\sensitive_word.txt',encoding='UTF-8') as f:
        lines = f.readlines()
        for line in lines:
            words.append(line.strip('\n'))
    for w in text:
        if w in words:
            return True
    return False

def get_keyword(text):
    keyword1=jieba.analyse.extract_tags(text, topK = 10, withWeight = True, allowPOS = ('ns', 'n', 'vn'))
    keyword2=jieba.analyse.textrank(text, 10, withWeight = True, allowPOS = ('ns', 'n', 'vn'))
    return keyword1,keyword2



def refresh_token():
    ak = 'IHxt1gIPAqqZGweLUb2zv6LK'	
    sk = '74bdgxtzWZhzXgE3LdtX2zIQqM1hx5Mr'	
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(ak,sk)

    res = requests.post(host)
    token = res.json()['access_token']
    return token


def sentiment_analysis(corp):
    token = '24.9ba17159dd2da49ca9a51b72cc94a14f.2592000.1590889964.282335-19352665'
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token={}'.format(token)
    data = {
            'text':corp
        }
    data = json.dumps(data)
    res = requests.post(url, data = data)
    json_data = json.loads(res.text)
    return json_data['items'][0]['positive_prob']


