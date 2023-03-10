'''
Author: 顺虞
Date: 2023-02-04
Help: https://github.com/liu1272/nonebot-plugin-stupidjdsd/
QQ: 1265257855
'''


from email import header
from urllib.parse import urlencode
import requests
import json
import random
import time
import urllib


'''
下方填写key 需抓包  key在更换微信登录后会改变 具体有效期尚未可知
'''
key =  '把我删了填上你的key哦~'
key=urllib.parse.unquote(key)
session = requests.session()
headers = {
  'Host': 'jdsd.gzhu.edu.cn',
  'Accept': '*/*',
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
  'Referer': 'https://servicewechat.com/wxb78a5743a9eed5bf/15/page-frame.html',
  'Accept-Encoding': 'gzip, deflate, br',
  'content-type': 'application/x-www-form-urlencoded'
}
session.headers = headers
url = "https://jdsd.gzhu.edu.cn/coctl_gzhu/index_wx.php"


def get_info():
    flag = False
    proxies = {'http': 'http://localhost:1181', 'https': 'http://localhost:1181'}
    info_data = {
        'route':'user_info',
        'key':key
    }
    #res = session.post(url, proxies=proxies,data = info_data, verify=False).json()
    res = session.post(url,data = info_data).json()
    info = {}
    if res['status'] == 1:
        flag = True
        info['name'] = res['re']['user_name']
        info['today'] = res['re']['per_day_credits']
        info['total'] = res['re']['credits']
    return (flag, info)


def signin():
    signin_data = {
        'route':'signin',
        'key':key
    }
    res = session.post(url,data = signin_data).json()


def train():
    get_id_data = {
        'route':'train_list_get',
        'diff' : '0',
        'key' : key
    }
    question = session.post(url,data = get_id_data).json()
    ans = []
    for i in question['re']['question_bag']:
        ans.append([i['num'],"1"])
    train_id = question['re']['train_id']
    train_data = {
        'route':'train_finish',
        'train_id':train_id,
        'train_result' : json.dumps(ans),
        'key':key
    }
    res = session.post(url,data = train_data).json()
    if res['status'] == 1:
        return True
    else:
        return False


def read():
    read_data = {
    'route' : 'classic_time',
        'addtime' : 0,
        'type':1,
        'key' : key
    }

    for i in range(1,6):
        read_data['type']=i
        read_data['addtime'] = 0
        begin = session.post(url, data = read_data)
        read_data['addtime'] = 91
        end = session.post(url, data = read_data)


def vs():
    print('[+]即将开始匹配 需要花费一定时间 请耐心等待')
    vs_find_data = {
        'route':'get_counterpart',
        'key':key,
        'counter':0,
        'find_type':0
    }
    add = 0
    i = 0
    ct = 0
    while(1):
        
        vs_find_data['counter'] = i
        res = session.post(url,data = vs_find_data).json()
        if res['status'] == 1:
            game_key = res['question_bag']['gaming_key']
            break
        i += 1
        if i > 10:
            i = 0
    alive_data = {
        'route':'ask_opponent_score',
        'key':key,
        'gaming_key':game_key
    }
    for i in range(150):
        print("\r[+]{}%".format(round((i/150)*100,1)),end='')
        time.sleep(1)
        alive_res = session.post(url,alive_data)
        if alive_res.json()['status'] == 2:
            add += 1
        if add >= 10:
            break
    question_num = get_question_num(res)
    post_answer(question_num,get_answer(question_num))
    print('')
    if(add==0):
        print("[+]得分失败，重新开始匹配")
        vs()




def get_question_num(res):
    question = []
    for i in res['question_bag']['question_arr']:
        question.append(i['num'])
    return question

def get_answer(num):
    get_answer_data={
        'route':'ascertain_answer',
        'key':key,
        'gaming_key':'777777',
        'question_id':'.coctl',
        'answer_id':'q',
        'question_num':num,
        'current_time':'0'
    }
    ans_data = session.post(url,data=get_answer_data).json()
    return ans_data['test_item2']['answer']

def post_answer(num,answer):
    post_answer_data={
        'route':'ascertain_answer',
        'key':key,
        'gaming_key':'777777',
        'question_id':'.coctl',
        'answer_id':answer,
        'question_num':num,
        'current_time':str(random.randint(100,180))
    }
    ans_data = session.post(url,data=post_answer_data).json()



def bark(flag,message = None):
    #修改bark_url推送到自己手机(iOS only)
    bark_url = ''
    global text1,text2
    if flag:
        text1 = '{}刷分成功/'.format(time.strftime("%Y-%m-%d", time.localtime()))
        text2 = '返回信息:{}'.format(message)
    else:
        text1 = '{}刷分失败了快去看看/'.format(time.strftime("%Y-%m-%d", time.localtime()))
        text2 = '快看看'
    requests.post(bark_url+'/'+text1+text2)


if __name__ == '__main__':
    try:
        flag, info = get_info()
        if not flag:
            raise Exception("[+]登录失败 请验证key")
        print("[+]{}同学您好,您目前的积分为:{}".format(info['name'],info['total']))
        signin()
        print('[+]已完成签到')
        for i in range(15):
            train()
        print('[+]已完成每日一题')
        read()
        print('[+]已完成阅读')
        vs()
        print('[+]已完成匹配')
        flag, info = get_info()
        string = "[+]今日获得:{} 总积分:{}".format(info['today'],info['total'])
        print(string)
        #bark(1,message = string)
    except Exception as e:
        print(e)
        #bark(0,message = e)
