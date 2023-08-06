import json
import requests
import os, socket, urllib3
from yangke.base import get_temp_para, web_available


def ask(question: str):
    """
    一个思知的对话机器人，但貌似准确度很低
    :param question:
    :return:
    """
    sess = requests.get('https://api.ownthink.com/bot?spoken={}'.format(question))
    answer = sess.text
    answer = json.loads(answer)
    return answer


def ask_baidu(question: str):
    """
    百度的对话机器人，详情参见百度 机器人对话API文档，https://ai.baidu.com/ai-doc/UNIT/qk38gggxg

    Unit主页 https://ai.baidu.com/unit/home

    :param question:
    :return: 问题答案的列表，每一个列表都对应一个可能的答案
    """

    def get_token(tries=0):
        """
        获取access_token，因为百度Unit智能对话定制与服务平台访问需要access_token才能使用

        :return: 返回百度的access_token
        """
        # client_id为官网获取的API Key，client_secret 为官网获取的Secret Key
        host = 'https://aip.baidubce.com/oauth/2.0/token?' \
               'grant_type=client_credentials&' \
               'client_id=KBK6CpyAIaxcfURZiDTPHFyv&' \
               'client_secret=bwvENVUj7XtXqGVGyYieqH8F20KhKRjw'
        try:
            resp = requests.get(host)
            if resp:
                print(resp.json())
                acc_token = resp.json().get('access_token')  # 一般access_token一个月有效期
                return acc_token
            else:
                if tries < 3:  # 如果失败，则重试3次
                    return get_token(tries + 1)
                if web_available():
                    raise Exception("向百度请求access_token参数失败，请核对百度相关接口是否已经更改！")
                else:
                    raise Exception("网络似乎没有连接，请检查重试！")
        except (requests.exceptions.ConnectionError, socket.gaierror, urllib3.exceptions.NewConnectionError,
                urllib3.exceptions.MaxRetryError) as e:
            raise Exception("网络似乎没有连接，请检查重试！")

    access_token = get_temp_para('access_token', expires_in=2500000, get_func=get_token)
    url = 'https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=' + access_token  # 机器人对话API，沙盒环境
    # url = 'https://aip.baidubce.com/rpc/2.0/unit/bot/chat?access_token=' + access_token  # 技能对话API

    post_data = {
        "log_id": "7758521",
        "version": "2.0",
        # "service_id": "S10000",
        "skill_ids": ["1033038"],
        "session_id": "",
        "request": {
            "query": question,
            "user_id": "UNIT_DEV_YK"
        },
        "dialog_state": {"contexts": {"SYS_REMEMBERED_SKILLS": ["1033038"]}}
    }
    post_data = str(post_data).replace("'", '"').encode('utf-8')

    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=post_data, headers=headers)
    result = []  # 答案的列表
    if response:
        print(response.json())
        response_list = response.json().get('result').get('response_list')
        for res in response_list:
            action = res.get('action_list')[0]  # action_list是一个列表，这里去列表第一项，如果以后遇到多答案的问题，再更新
            result.append(action.get('say'))

    return result


# def glove():

if __name__ == "__main__":
    import re

    qingming_dict = {}
    for year in range(1990, 2100):
        ans = ask_baidu(f'{year}年清明节是几月几号')[0]
        ans = re.findall(".*月(.)日.*", ans)
        while len(ans) == 0:
            ans = ask_baidu(f'{year}年清明节是几月几号')[0]
            ans = re.findall(".*月(.)日.*", ans)
        qingming_dict[str(year)] = ans[0]
    print(qingming_dict)